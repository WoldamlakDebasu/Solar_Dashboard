# SolarSense Pro - Deployment Guide

This guide provides step-by-step instructions for deploying the SolarSense Pro Solar IoT Dashboard in various environments.

## 🚀 Quick Deployment (Recommended)

### Prerequisites
- Python 3.11 or higher
- 2GB RAM minimum, 4GB recommended
- 10GB disk space
- Internet connection for initial setup

### One-Command Deployment

1. **Extract the application**
   ```bash
   unzip solarsense-pro.zip
   cd solar-iot-backend
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Start the application**
   ```bash
   python src/main.py
   ```

4. **Access the dashboard**
   Open your browser and go to: `http://localhost:5000`

## 🔧 Manual Deployment

### Step 1: Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration

1. **Environment Variables** (Optional)
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key-here
   export DATABASE_URL=sqlite:///app.db
   ```

2. **Database Setup**
   ```bash
   # Database is automatically created on first run
   # No additional setup required for SQLite
   ```

### Step 3: Start the Application

```bash
python src/main.py
```

The application will be available at `http://localhost:5000`

## 🌐 Production Deployment

### Using Gunicorn (Recommended)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn configuration**
   ```bash
   # gunicorn.conf.py
   bind = "0.0.0.0:5000"
   workers = 4
   worker_class = "sync"
   timeout = 30
   max_requests = 1000
   max_requests_jitter = 100
   ```

3. **Start with Gunicorn**
   ```bash
   gunicorn -c gunicorn.conf.py src.main:app
   ```

### Using Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   CMD ["python", "src/main.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t solarsense-pro .
   docker run -p 5000:5000 solarsense-pro
   ```

### Using Nginx (Reverse Proxy)

1. **Install Nginx**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Configure Nginx**
   ```nginx
   # /etc/nginx/sites-available/solarsense
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/solarsense /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## ☁️ Cloud Deployment

### AWS Deployment

1. **EC2 Instance Setup**
   - Launch Ubuntu 22.04 LTS instance
   - Security group: Allow HTTP (80) and HTTPS (443)
   - Instance type: t3.medium or larger

2. **Application Deployment**
   ```bash
   # Connect to EC2 instance
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3.11 python3.11-venv python3-pip -y
   
   # Upload and extract application
   scp -i your-key.pem solarsense-pro.zip ubuntu@your-ec2-ip:~/
   unzip solarsense-pro.zip
   cd solar-iot-backend
   
   # Follow manual deployment steps
   ```

3. **SSL Certificate (Let's Encrypt)**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

### Azure Deployment

1. **Create App Service**
   ```bash
   az webapp create \
     --resource-group myResourceGroup \
     --plan myAppServicePlan \
     --name solarsense-pro \
     --runtime "PYTHON|3.11"
   ```

2. **Deploy Application**
   ```bash
   az webapp deployment source config-zip \
     --resource-group myResourceGroup \
     --name solarsense-pro \
     --src solarsense-pro.zip
   ```

### Google Cloud Platform

1. **App Engine Deployment**
   ```yaml
   # app.yaml
   runtime: python311
   
   env_variables:
     FLASK_ENV: production
   
   handlers:
   - url: /.*
     script: auto
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

## 🔒 Security Configuration

### SSL/HTTPS Setup

1. **Generate SSL Certificate**
   ```bash
   # Using Let's Encrypt
   sudo certbot certonly --standalone -d your-domain.com
   ```

2. **Configure Flask for HTTPS**
   ```python
   # In src/main.py
   if __name__ == '__main__':
       app.run(
           host='0.0.0.0', 
           port=5000, 
           ssl_context='adhoc',  # For development
           debug=False
       )
   ```

### Firewall Configuration

```bash
# Ubuntu/Debian
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## 📊 Monitoring & Logging

### Application Monitoring

1. **Health Check Endpoint**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Log Configuration**
   ```python
   import logging
   
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s %(levelname)s %(message)s',
       handlers=[
           logging.FileHandler('app.log'),
           logging.StreamHandler()
       ]
   )
   ```

### System Monitoring

1. **Install monitoring tools**
   ```bash
   sudo apt install htop iotop nethogs -y
   ```

2. **Monitor resources**
   ```bash
   # CPU and memory usage
   htop
   
   # Disk I/O
   iotop
   
   # Network usage
   nethogs
   ```

## 🔄 Backup & Recovery

### Database Backup

```bash
# Backup SQLite database
cp src/database/app.db backup/app_$(date +%Y%m%d_%H%M%S).db

# Automated backup script
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp src/database/app.db "$BACKUP_DIR/app_$DATE.db"
find "$BACKUP_DIR" -name "app_*.db" -mtime +7 -delete
```

### Application Backup

```bash
# Full application backup
tar -czf solarsense_backup_$(date +%Y%m%d).tar.gz solar-iot-backend/
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 5000
   sudo lsof -i :5000
   
   # Kill process
   sudo kill -9 <PID>
   ```

2. **Permission denied**
   ```bash
   # Fix file permissions
   chmod +x src/main.py
   
   # Fix directory permissions
   chmod -R 755 solar-iot-backend/
   ```

3. **Module not found**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

### Log Analysis

```bash
# View application logs
tail -f app.log

# View system logs
sudo journalctl -u nginx -f
sudo journalctl -u gunicorn -f
```

## 📞 Support

For deployment assistance:
- **Email**: support@solarsense.ae
- **Documentation**: Check README.md for detailed information
- **Issues**: Report technical issues with deployment logs

## 🔄 Updates

### Application Updates

1. **Backup current version**
   ```bash
   cp -r solar-iot-backend solar-iot-backend.backup
   ```

2. **Deploy new version**
   ```bash
   # Extract new version
   unzip solarsense-pro-v1.1.0.zip
   
   # Copy database and config
   cp solar-iot-backend.backup/src/database/app.db solar-iot-backend/src/database/
   
   # Restart application
   sudo systemctl restart gunicorn
   ```

### Zero-Downtime Updates

1. **Blue-Green Deployment**
   - Deploy new version to separate environment
   - Test thoroughly
   - Switch traffic using load balancer

2. **Rolling Updates**
   - Update one server at a time
   - Verify health before proceeding
   - Rollback if issues detected

---

**Note**: This deployment guide covers the most common scenarios. For enterprise deployments or custom requirements, please contact our support team for personalized assistance.


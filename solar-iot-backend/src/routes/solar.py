from flask import Blueprint, jsonify
from datetime import datetime, timedelta
import random
import math

solar_bp = Blueprint('solar', __name__)

def generate_solar_data():
    """Generate realistic solar generation data for the day"""
    data = []
    current_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for hour in range(24):
        time_str = current_time.strftime('%H:%M')
        
        # Solar generation follows a bell curve during daylight hours
        if 6 <= hour <= 18:
            # Peak at noon (hour 12)
            solar_factor = math.sin(math.pi * (hour - 6) / 12)
            base_solar = 85 * solar_factor  # Max 85kW
            # Add some randomness
            solar = max(0, base_solar + random.uniform(-10, 10))
        else:
            solar = 0
        
        # Energy consumption varies throughout the day
        if 6 <= hour <= 22:
            base_consumption = 35 + 15 * math.sin(math.pi * (hour - 6) / 16)
        else:
            base_consumption = 15
        
        consumption = max(5, base_consumption + random.uniform(-5, 5))
        
        data.append({
            'time': time_str,
            'solar': round(solar, 1),
            'consumption': round(consumption, 1)
        })
        
        current_time += timedelta(hours=1)
    
    return data

@solar_bp.route('/metrics', methods=['GET'])
def get_solar_metrics():
    """Get current solar system metrics"""
    # Generate realistic current values
    current_solar = random.uniform(45, 95) if 6 <= datetime.now().hour <= 18 else 0
    current_consumption = random.uniform(25, 45)
    
    # Calculate daily totals
    daily_solar = random.uniform(450, 650)  # kWh
    daily_consumption = random.uniform(280, 380)  # kWh
    
    # Cost savings (AED per kWh rate ~0.38)
    cost_savings = (daily_solar * 0.38)
    
    # CO2 reduction (kg CO2 per kWh ~0.5)
    co2_reduction = daily_solar * 0.5
    
    return jsonify({
        'solar_generation': {
            'current': round(current_solar, 1),
            'daily': round(daily_solar, 1),
            'unit': 'kW',
            'change': '+12%'
        },
        'energy_consumption': {
            'current': round(current_consumption, 1),
            'daily': round(daily_consumption, 1),
            'unit': 'kW',
            'change': '-8%'
        },
        'cost_savings': {
            'daily': round(cost_savings, 0),
            'monthly': round(cost_savings * 30, 0),
            'unit': 'AED',
            'change': '+15%'
        },
        'co2_reduction': {
            'daily': round(co2_reduction, 1),
            'monthly': round(co2_reduction * 30, 1),
            'unit': 'kg',
            'change': '+22%'
        }
    })

@solar_bp.route('/energy-data', methods=['GET'])
def get_energy_data():
    """Get hourly energy generation and consumption data"""
    return jsonify({
        'data': generate_solar_data(),
        'last_updated': datetime.now().isoformat()
    })

@solar_bp.route('/weather', methods=['GET'])
def get_weather_data():
    """Get current weather conditions"""
    return jsonify({
        'temperature': 27,
        'condition': 'Partly Cloudy',
        'wind_speed': 12,
        'cloud_cover': 35,
        'uv_index': 8,
        'forecast': {
            'description': 'Excellent conditions for solar generation today.',
            'peak_generation': '95 kW at 1:00 PM'
        }
    })

@solar_bp.route('/system-status', methods=['GET'])
def get_system_status():
    """Get system component status"""
    return jsonify({
        'components': [
            {
                'name': 'Solar Inverters',
                'status': 'online',
                'value': '4/4 Active'
            },
            {
                'name': 'IoT Sensors',
                'status': 'online',
                'value': '28/30 Connected'
            },
            {
                'name': 'Data Collection',
                'status': 'online',
                'value': '99.8% Uptime'
            },
            {
                'name': 'Security',
                'status': 'warning',
                'value': 'Certificate Expiring'
            }
        ],
        'overall_health': 'Excellent'
    })


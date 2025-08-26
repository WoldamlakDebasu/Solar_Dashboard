from flask import Blueprint, jsonify
from datetime import datetime
import random

ai_bp = Blueprint('ai', __name__)

# Predefined AI insights with different priorities and types
INSIGHTS_POOL = [
    {
        'type': 'optimization',
        'title': 'Energy Optimization Opportunity',
        'message': 'HVAC system running 15% above optimal levels. Adjusting setpoint could save AED 450/month.',
        'priority': 'medium',
        'action': 'Optimize HVAC',
        'potential_savings': 450
    },
    {
        'type': 'maintenance',
        'title': 'Predictive Maintenance Alert',
        'message': 'Solar panel efficiency decreased by 3% in Zone B. Cleaning recommended within 7 days.',
        'priority': 'high',
        'action': 'Schedule Cleaning',
        'potential_savings': 200
    },
    {
        'type': 'insight',
        'title': 'Peak Load Optimization',
        'message': 'Shifting 20% of non-critical loads to off-peak hours could reduce costs by AED 280/month.',
        'priority': 'low',
        'action': 'Configure Schedule',
        'potential_savings': 280
    },
    {
        'type': 'success',
        'title': 'Efficiency Achievement',
        'message': 'Solar self-consumption increased by 12% this month. Excellent progress toward sustainability goals.',
        'priority': 'info',
        'action': 'View Details',
        'potential_savings': 0
    },
    {
        'type': 'optimization',
        'title': 'Battery Storage Optimization',
        'message': 'Battery charging schedule can be optimized for 18% better efficiency during peak hours.',
        'priority': 'medium',
        'action': 'Optimize Battery',
        'potential_savings': 320
    },
    {
        'type': 'maintenance',
        'title': 'Inverter Performance Alert',
        'message': 'Inverter #3 showing 5% efficiency drop. Inspection recommended to prevent further degradation.',
        'priority': 'high',
        'action': 'Schedule Inspection',
        'potential_savings': 150
    },
    {
        'type': 'insight',
        'title': 'Weather-Based Optimization',
        'message': 'Upcoming cloudy period detected. Pre-charging batteries recommended for optimal energy management.',
        'priority': 'low',
        'action': 'Pre-charge Batteries',
        'potential_savings': 100
    }
]

@ai_bp.route('/insights', methods=['GET'])
def get_ai_insights():
    """Get AI-powered insights and recommendations"""
    # Select 4-6 random insights
    num_insights = random.randint(4, 6)
    selected_insights = random.sample(INSIGHTS_POOL, min(num_insights, len(INSIGHTS_POOL)))
    
    # Add unique IDs and timestamps
    for i, insight in enumerate(selected_insights):
        insight['id'] = i + 1
        insight['timestamp'] = datetime.now().isoformat()
    
    return jsonify({
        'insights': selected_insights,
        'total_potential_savings': sum(insight['potential_savings'] for insight in selected_insights),
        'last_updated': datetime.now().isoformat()
    })

@ai_bp.route('/predictions', methods=['GET'])
def get_predictions():
    """Get AI predictions for energy generation and consumption"""
    # Generate predictions for next 7 days
    predictions = []
    
    for day in range(7):
        # Simulate weather impact on solar generation
        weather_factor = random.uniform(0.7, 1.0)
        predicted_solar = random.uniform(400, 600) * weather_factor
        predicted_consumption = random.uniform(280, 380)
        
        predictions.append({
            'day': day + 1,
            'date': (datetime.now() + datetime.timedelta(days=day)).strftime('%Y-%m-%d'),
            'predicted_solar': round(predicted_solar, 1),
            'predicted_consumption': round(predicted_consumption, 1),
            'weather_factor': round(weather_factor, 2),
            'net_savings': round((predicted_solar - predicted_consumption) * 0.38, 2)
        })
    
    return jsonify({
        'predictions': predictions,
        'confidence_level': random.uniform(85, 95),
        'model_version': '2.1.0',
        'last_updated': datetime.now().isoformat()
    })

@ai_bp.route('/anomalies', methods=['GET'])
def get_anomalies():
    """Get detected anomalies in the system"""
    anomalies = []
    
    # Randomly generate some anomalies
    if random.random() < 0.3:  # 30% chance of anomaly
        anomaly_types = [
            {
                'type': 'performance_drop',
                'description': 'Unusual drop in solar panel efficiency detected in Zone A',
                'severity': 'medium',
                'confidence': 0.87
            },
            {
                'type': 'consumption_spike',
                'description': 'Energy consumption 25% higher than expected for current time',
                'severity': 'low',
                'confidence': 0.92
            },
            {
                'type': 'inverter_issue',
                'description': 'Inverter voltage fluctuations outside normal range',
                'severity': 'high',
                'confidence': 0.95
            }
        ]
        
        anomalies = random.sample(anomaly_types, random.randint(1, 2))
        for i, anomaly in enumerate(anomalies):
            anomaly['id'] = i + 1
            anomaly['timestamp'] = datetime.now().isoformat()
    
    return jsonify({
        'anomalies': anomalies,
        'total_count': len(anomalies),
        'last_scan': datetime.now().isoformat()
    })

@ai_bp.route('/optimization-suggestions', methods=['GET'])
def get_optimization_suggestions():
    """Get AI-powered optimization suggestions"""
    suggestions = [
        {
            'category': 'Energy Management',
            'suggestion': 'Implement load balancing during peak solar hours',
            'impact': 'High',
            'estimated_savings': 'AED 380/month'
        },
        {
            'category': 'Maintenance',
            'suggestion': 'Schedule preventive cleaning every 6 weeks',
            'impact': 'Medium',
            'estimated_savings': 'AED 220/month'
        },
        {
            'category': 'System Upgrade',
            'suggestion': 'Add battery storage for better energy independence',
            'impact': 'High',
            'estimated_savings': 'AED 650/month'
        }
    ]
    
    return jsonify({
        'suggestions': suggestions,
        'total_potential_savings': 1250,
        'implementation_priority': 'High',
        'last_updated': datetime.now().isoformat()
    })


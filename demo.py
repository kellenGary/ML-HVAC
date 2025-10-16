#!/usr/bin/env python3
"""
Demo script to show sample usage of the HVAC system with Streamlit display.

This script creates sample data to demonstrate the Streamlit dashboard
without needing actual Bluetooth hardware.
"""

from data_store import SensorDataStore
import random
import time
from datetime import datetime, timedelta

def generate_sample_data(num_readings=100):
    """Generate sample sensor readings for demo purposes."""
    print("🔧 Generating sample HVAC sensor data...")
    
    store = SensorDataStore('sensor_data.json')
    
    # Clear any existing data
    store.clear_readings()
    
    # Set a target temperature
    store.set_target_temperature(22.0)
    
    # Generate readings over the past 2 hours
    base_time = datetime.now()
    base_temp = 22.0
    base_humidity = 45
    
    print(f"Creating {num_readings} readings spanning 2 hours...")
    
    for i in range(num_readings):
        # Calculate time offset (spread over 2 hours)
        minutes_ago = int((num_readings - i) * (120 / num_readings))
        
        # Simulate realistic temperature variations
        # Temperature fluctuates around base with some trend
        temp_variation = random.uniform(-2.0, 2.0)
        temp = base_temp + temp_variation + (i / num_readings * 0.5)  # Slight warming trend
        
        # Humidity variations
        humidity_variation = random.randint(-8, 8)
        humidity = max(20, min(80, base_humidity + humidity_variation))
        
        # Add the reading with backdated timestamp
        import json
        with open('sensor_data.json', 'r') as f:
            data = json.load(f)
        
        timestamp = (base_time - timedelta(minutes=minutes_ago)).isoformat()
        
        data['readings'].append({
            'timestamp': timestamp,
            'temperature': round(temp, 2),
            'humidity': humidity
        })
        
        with open('sensor_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        if (i + 1) % 20 == 0:
            print(f"  Generated {i + 1}/{num_readings} readings...")
    
    readings = store.get_readings()
    print(f"\n✅ Successfully generated {len(readings)} sample readings")
    print(f"   Temperature range: {min(r['temperature'] for r in readings):.1f}°C - {max(r['temperature'] for r in readings):.1f}°C")
    print(f"   Humidity range: {min(r['humidity'] for r in readings)}% - {max(r['humidity'] for r in readings)}%")
    print(f"   Target temperature: {store.get_target_temperature()}°C")
    print("\n📊 You can now run: streamlit run streamlit_app.py")
    print("   to view the dashboard at http://localhost:8501")

if __name__ == "__main__":
    generate_sample_data(100)

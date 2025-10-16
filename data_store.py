"""
Data storage module for HVAC sensor readings.

This module handles storing and retrieving temperature and humidity data
in a JSON file for use by the Streamlit display.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class SensorDataStore:
    """Stores and retrieves sensor data in JSON format."""
    
    def __init__(self, data_file: str = "sensor_data.json"):
        """Initialize the data store.
        
        Args:
            data_file: Path to the JSON file for storing data
        """
        self.data_file = data_file
        self._ensure_data_file()
    
    def _ensure_data_file(self) -> None:
        """Ensure the data file exists, create if necessary."""
        if not os.path.exists(self.data_file):
            self._write_data({"readings": [], "settings": {"target_temp": 22.0}})
    
    def _read_data(self) -> Dict:
        """Read data from the JSON file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"readings": [], "settings": {"target_temp": 22.0}}
    
    def _write_data(self, data: Dict) -> None:
        """Write data to the JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_reading(self, temperature: float, humidity: int) -> None:
        """Add a new sensor reading.
        
        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage
        """
        data = self._read_data()
        
        reading = {
            "timestamp": datetime.now().isoformat(),
            "temperature": round(temperature, 2),
            "humidity": humidity
        }
        
        data["readings"].append(reading)
        
        # Keep only last 1000 readings to prevent file from growing too large
        if len(data["readings"]) > 1000:
            data["readings"] = data["readings"][-1000:]
        
        self._write_data(data)
    
    def get_readings(self, limit: Optional[int] = None) -> List[Dict]:
        """Get sensor readings.
        
        Args:
            limit: Maximum number of readings to return (most recent)
            
        Returns:
            List of readings, each containing timestamp, temperature, and humidity
        """
        data = self._read_data()
        readings = data.get("readings", [])
        
        if limit and len(readings) > limit:
            return readings[-limit:]
        return readings
    
    def get_target_temperature(self) -> float:
        """Get the target temperature setting.
        
        Returns:
            Target temperature in Celsius
        """
        data = self._read_data()
        return data.get("settings", {}).get("target_temp", 22.0)
    
    def set_target_temperature(self, temp: float) -> None:
        """Set the target temperature.
        
        Args:
            temp: Target temperature in Celsius
        """
        data = self._read_data()
        if "settings" not in data:
            data["settings"] = {}
        data["settings"]["target_temp"] = round(temp, 1)
        self._write_data(data)
    
    def clear_readings(self) -> None:
        """Clear all sensor readings."""
        data = self._read_data()
        data["readings"] = []
        self._write_data(data)


import os
import platform
from dotenv import load_dotenv
from typing import Optional


class DeviceConnectionError(Exception):
    """Raised when device connection fails."""
    pass


class PacketParsingError(Exception):
    """Raised when packet parsing fails."""
    pass


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


class Config:
    """Configuration class that handles environment variables with validation and fallbacks."""
    
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get values from environment variables with validation
        self.device_name = self._get_required_env('DEVICE_NAME', 'LYWSD03MMC')
        
        # Conditionally set MAC address based on OS
        self.current_os = platform.system()
        if self.current_os == "Darwin":  # macOS
            self.device_address = self._get_required_env('DEVICE_ADDRESS_MACOS')
        else:
            self.device_address = self._get_required_env('DEVICE_ADDRESS')
            
        self.temperature_humidity_uuid = self._get_required_env(
            'TEMPERATURE_HUMIDITY_UUID',
            'ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6'  # Default UUID for LYWSD03MMC
        )
        
        # Sensor calibration - sensor is off by 2.7 deg C
        self.temp_correction = 2.7
        
        # Expected packet interval in milliseconds
        self.packet_interval = 1000
    
    def _get_required_env(self, key: str, default: Optional[str] = None) -> str:
        """Get environment variable with optional default value."""
        value = os.getenv(key, default)
        if value is None:
            raise ConfigurationError(f"Required environment variable '{key}' is missing")
        return value
    
    @property
    def device_info(self) -> dict:
        """Get device information as a dictionary."""
        return {
            'name': self.device_name,
            'address': self.device_address,
            'uuid': self.temperature_humidity_uuid,
            'os': self.current_os
        }

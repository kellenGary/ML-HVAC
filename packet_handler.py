import datetime
from typing import Optional, Tuple
from bleak import BleakClient

from contants import Config, PacketParsingError
from packet_timer import PacketTimer
from data_store import SensorDataStore


def _parse_sensor_data(data: bytes, temp_correction: float) -> Tuple[float, int]:
    """Parse raw sensor data into temperature and humidity values.
    
    Args:
        data: Raw bytes from the sensor
        temp_correction: Temperature correction offset
        
    Returns:
        Tuple of (temperature in Celsius, humidity percentage)
        
    Raises:
        PacketParsingError: If data format is invalid
    """
    if len(data) < 5:
        raise PacketParsingError(f"Received data is too short: {len(data)} bytes, expected at least 5")
    
    try:
        temp_raw = int.from_bytes(data[0:2], byteorder='little', signed=True)
        humidity_raw = int.from_bytes(data[2:3], byteorder='little')
        
        temperature = temp_raw / 100.0 - temp_correction  # Temperature in Celsius
        humidity = humidity_raw  # Humidity as percentage
        
        return temperature, humidity
    except Exception as e:
        raise PacketParsingError(f"Failed to parse sensor data: {e}")


async def parse_packet(
    client: BleakClient,
    config: Config,
    packet_timer: PacketTimer,
    data_store: Optional[SensorDataStore] = None
) -> Optional[Tuple[float, int]]:
    """Read and parse a packet from the HVAC sensor.
    
    Args:
        client: Connected Bluetooth client
        config: Configuration object containing device settings
        packet_timer: PacketTimer instance for tracking intervals
        data_store: Optional data store for persisting readings
        
    Returns:
        Tuple of (temperature, humidity) if successful, None otherwise
        
    Raises:
        PacketParsingError: If packet parsing fails
    """
    try:
        # Read from the temperature/humidity characteristic
        data = await client.read_gatt_char(config.temperature_humidity_uuid)
        
        # Record packet timing
        interval = packet_timer.record_packet()

        
        
        # Parse the sensor data
        temperature, humidity = _parse_sensor_data(data, config.temp_correction)
        
        # Save to data store if provided
        if data_store is not None:
            data_store.add_reading(temperature, humidity)
        
        # Display the results
        print(f"🌡️  Temperature: {temperature:.1f}°C ({temperature * 9/5 + 32:.1f}°F)")
        print(f"💧 Humidity: {humidity}%")
        print(f"📅 Time: {datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
        
        if interval is not None:
            print(f"⏱️  Interval since last packet: {interval:.3f} seconds")
            print(f"📊 Average interval: {packet_timer.get_average_interval():.3f} seconds")
        
        # Show detailed stats every 10 packets
        if len(packet_timer.packet_times) % 10 == 0 and len(packet_timer.packet_times) > 0:
            packet_timer.print_detailed_stats()
        
        return temperature, humidity
        
    except PacketParsingError:
        # Re-raise parsing errors as-is
        raise
    except Exception as e:
        raise PacketParsingError(f"Error reading temperature/humidity: {e}")
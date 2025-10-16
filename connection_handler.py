
import asyncio
import datetime
from typing import Optional
from bleak import BleakClient, BleakScanner

from contants import Config, DeviceConnectionError
from packet_handler import parse_packet
from packet_timer import PacketTimer
from data_store import SensorDataStore


async def scan_for_device(device_name: str = "LYWSD03MMC") -> Optional[str]:
    """Scan for Bluetooth devices and return the address of the target device.
    
    Args:
        device_name: Name of the device to scan for
        
    Returns:
        Device address if found, None otherwise
    """
    print(f"Scanning for {device_name} device...")
    devices = await BleakScanner.discover(timeout=10.0)
    
    for device in devices:
        if device.name == device_name:
            print(f"Found {device_name}: {device.address} (RSSI: signal strength)")
            return device.address
        else:
            print(f"Found device: {device.name} - {device.address}")
    
    print(f"{device_name} device not found in scan")
    return None


async def connect_and_read_sensor(
    config: Config,
    packet_timer: PacketTimer,
    duration_minutes: int = 5,
    data_store: Optional[SensorDataStore] = None
) -> None:
    """Connect to the HVAC sensor and read data for the specified duration.
    
    Args:
        config: Configuration object containing device settings
        packet_timer: PacketTimer instance for tracking intervals
        duration_minutes: How long to monitor in minutes
        data_store: Optional data store for persisting readings
        
    Raises:
        DeviceConnectionError: If connection to device fails
    """
    device_info = config.device_info
    print(f"Connecting to {device_info['name']} device")
    print(f"MAC Address: {device_info['address']}")
    print(f"Will monitor for {duration_minutes} minutes to calculate packet intervals")
    print("=" * 60)
    
    try:
        async with BleakClient(device_info['address']) as client:
            print(f"Connected: {client.is_connected}")
            
            start_time = datetime.datetime.now()
            end_time = start_time + datetime.timedelta(minutes=duration_minutes)
            
            while client.is_connected and datetime.datetime.now() < end_time:
                print(f"\nAttempting to read temperature/humidity data...")
                await parse_packet(client, config, packet_timer, data_store)
                await asyncio.sleep(config.packet_interval)
            
            # Print final statistics
            print("\n" + "🏁 FINAL PACKET INTERVAL ANALYSIS ".center(80, "="))
            packet_timer.print_detailed_stats()
            print("="*80)
            
    except Exception as e:
        raise DeviceConnectionError(f"Failed to connect to device: {e}")

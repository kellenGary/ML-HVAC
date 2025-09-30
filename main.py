from bleak import BleakClient, BleakScanner
import asyncio
import platform

# Your LYWSD03MMC device details
DEVICE_NAME = "LYWSD03MMC"
if platform.system() == "Windows":
    DEVICE_ADDRESS = "A4:C1:38:7C:C8:2B"  # Windows format
else:
    DEVICE_ADDRESS = "F03CB50C-479B-58DE-BACF-1636D43EE92A"  # macOS format

# LYWSD03MMC service and characteristic UUIDs
TEMPERATURE_HUMIDITY_UUID = "ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6"  # Temperature/Humidity characteristic

async def connect_and_read_sensor():
    print(f"Connecting to LYWSD03MMC device: {DEVICE_NAME}")
    print(f"MAC Address: {DEVICE_ADDRESS}")
    
    try:
        async with BleakClient(DEVICE_ADDRESS) as client:
            print(f"Connected: {client.is_connected}")
            print("\nAttempting to read temperature/humidity data...")
            
            # Try to read from the temperature/humidity characteristic
            try:
                data = await client.read_gatt_char(TEMPERATURE_HUMIDITY_UUID)
                # Parse the data (LYWSD03MMC format)
                if len(data) >= 5:
                    temp_raw = int.from_bytes(data[0:2], byteorder='little', signed=True)
                    humidity_raw = int.from_bytes(data[2:3], byteorder='little')
                    
                    temperature = temp_raw / 100.0  # Temperature in Celsius
                    humidity = humidity_raw  # Humidity as percentage
                    
                    print(f"\n🌡️  Temperature: {temperature:.1f}°C ({temperature * 9/5 + 32:.1f}°F)")
                    print(f"💧 Humidity: {humidity}%")
                    
                else:
                    print("Received data is too short to parse")
                    
            except Exception as e:
                print(f"Error reading temperature/humidity: {e}")
                
                # Try to find and read other characteristics
                print("\nTrying to read from other characteristics...")
                for service in client.services:
                    for characteristic in service.characteristics:
                        if "read" in characteristic.properties:
                            try:
                                data = await client.read_gatt_char(characteristic.uuid)
                                print(f"Characteristic {characteristic.uuid}: {data.hex()}")
                            except Exception as char_error:
                                print(f"Could not read {characteristic.uuid}: {char_error}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        print("\nTrying to scan for the device again...")
        await scan_for_device()

async def scan_for_device():
    print("Scanning for LYWSD03MMC device...")
    devices = await BleakScanner.discover(timeout=5.0)
    
    for device in devices:
        if device.name == "LYWSD03MMC":
            print(f"Found LYWSD03MMC: {device.address} (RSSI: signal strength)")
            return device.address
        else:
            print(f"Found device: {device.name} - {device.address}")
    
    print("LYWSD03MMC device not found in scan")
    return None

async def main():
    print("LYWSD03MMC Temperature/Humidity Reader")
    print("=" * 50)
    await connect_and_read_sensor()

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from contants import Config, ConfigurationError
from connection_handler import connect_and_read_sensor
from packet_timer import PacketTimer
from data_store import SensorDataStore


async def main():
    """Main entry point for the HVAC monitoring application."""
    try:
        # Initialize configuration
        config = Config()
        
        print("LYWSD03MMC Temperature/Humidity Reader with Packet Interval Analysis")
        print("=" * 70)
        print(f"Running on: {config.current_os}")
        print(f"Using device address: {config.device_address}")
        
        # Create packet timer instance
        packet_timer = PacketTimer()
        
        # Create data store for Streamlit display
        data_store = SensorDataStore()
        
        # You can adjust the monitoring duration here (in minutes)
        monitoring_duration = 5  # Monitor for 5 minutes by default
        
        print(f"Starting packet interval analysis for {monitoring_duration} minutes...")
        print("💾 Data will be saved for Streamlit display")
        print("Press Ctrl+C to stop early and see results")
        
        await connect_and_read_sensor(
            config=config,
            packet_timer=packet_timer,
            duration_minutes=monitoring_duration,
            data_store=data_store
        )
        
    except ConfigurationError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please check your environment variables or create a .env file")
        return
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoring stopped by user")
        # Still show stats if we have any data
        if 'packet_timer' in locals() and packet_timer.packet_times:
            stats = packet_timer.get_stats()
            print("\n" + "📊 PARTIAL RESULTS ".center(60, "="))
            print(f"📦 Packets received: {stats['total_packets']}")
            if stats['average_interval'] > 0:
                print(f"⏱️  Average interval: {stats['average_interval']:.3f} seconds")
            print("="*60)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

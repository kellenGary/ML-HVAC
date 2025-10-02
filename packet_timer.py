import datetime
from typing import List, Dict, Union


class PacketTimer:
    """
    A class to track and analyze packet timing intervals for Bluetooth devices.
    
    This class records timestamps of received packets and calculates various
    statistics about the intervals between packets, including average, min, max
    intervals and packets per time unit estimates.
    """
    
    def __init__(self):
        self.packet_times: List[datetime.datetime] = []
        self.intervals: List[float] = []
    
    def record_packet(self) -> Union[float, None]:
        """
        Record the time a packet was received and calculate interval from previous packet.
        
        Returns:
            Union[float, None]: The interval in seconds since the last packet, or None if this is the first packet
        """
        current_time = datetime.datetime.now()
        self.packet_times.append(current_time)
        
        # Calculate interval if we have at least 2 packets
        if len(self.packet_times) >= 2:
            interval = (current_time - self.packet_times[-2]).total_seconds()
            self.intervals.append(interval)
            return interval
        return None
    
    def get_average_interval(self) -> float:
        """
        Get the average time between packets in seconds.
        
        Returns:
            float: Average interval in seconds, or 0.0 if no intervals recorded
        """
        if not self.intervals:
            return 0.0
        return sum(self.intervals) / len(self.intervals)
    
    def get_stats(self) -> Dict[str, float]:
        """
        Get comprehensive timing statistics.
        
        Returns:
            Dict[str, float]: Dictionary containing:
                - total_packets: Number of packets received
                - average_interval: Average time between packets (seconds)
                - min_interval: Shortest interval (seconds)
                - max_interval: Longest interval (seconds)
                - total_runtime: Total monitoring time (seconds)
        """
        if not self.intervals:
            return {
                "total_packets": len(self.packet_times),
                "average_interval": 0.0,
                "min_interval": 0.0,
                "max_interval": 0.0,
                "total_runtime": 0.0
            }
        
        total_runtime = (self.packet_times[-1] - self.packet_times[0]).total_seconds() if len(self.packet_times) >= 2 else 0.0
        
        return {
            "total_packets": len(self.packet_times),
            "average_interval": self.get_average_interval(),
            "min_interval": min(self.intervals),
            "max_interval": max(self.intervals),
            "total_runtime": total_runtime
        }
    
    def reset(self) -> None:
        """Reset all recorded data to start fresh."""
        self.packet_times.clear()
        self.intervals.clear()
    
    def get_packets_per_minute(self) -> float:
        """
        Calculate estimated packets per minute based on average interval.
        
        Returns:
            float: Estimated packets per minute, or 0.0 if no data
        """
        avg_interval = self.get_average_interval()
        if avg_interval > 0:
            return 60.0 / avg_interval
        return 0.0
    
    def get_packets_per_hour(self) -> float:
        """
        Calculate estimated packets per hour based on average interval.
        
        Returns:
            float: Estimated packets per hour, or 0.0 if no data
        """
        avg_interval = self.get_average_interval()
        if avg_interval > 0:
            return 3600.0 / avg_interval
        return 0.0
    
    def print_detailed_stats(self) -> None:
        """Print detailed statistics in a formatted way."""
        stats = self.get_stats()
        
        print("\n" + "📊 PACKET TIMING STATISTICS ".center(60, "="))
        print(f"📦 Total packets received: {stats['total_packets']}")
        print(f"⏱️  Average interval: {stats['average_interval']:.3f} seconds")
        print(f"⚡ Minimum interval: {stats['min_interval']:.3f} seconds")
        print(f"🐌 Maximum interval: {stats['max_interval']:.3f} seconds")
        print(f"🕐 Total monitoring time: {stats['total_runtime']:.1f} seconds")
        
        if stats['average_interval'] > 0:
            print(f"📊 Packets per minute: {self.get_packets_per_minute():.1f}")
            print(f"📊 Packets per hour: {self.get_packets_per_hour():.1f}")
        
        print("="*60)
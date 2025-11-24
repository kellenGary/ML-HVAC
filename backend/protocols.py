"""
Protocol interfaces for HVAC monitoring system.

This module defines the contracts that different components should follow,
improving testability and maintainability through clear interface definitions.
"""

from typing import Protocol, Optional, Tuple, Dict
from bleak import BleakClient
from packet_timer import PacketTimer
from contants import Config


class PacketParser(Protocol):
    """Protocol for packet parsing functionality."""
    
    async def parse_packet(
        self,
        client: BleakClient,
        config: Config,
        packet_timer: PacketTimer
    ) -> Optional[Tuple[float, int]]:
        """Parse a packet from the sensor and return temperature/humidity data."""
        ...


class ConnectionHandler(Protocol):
    """Protocol for connection handling functionality."""
    
    async def connect_and_read_sensor(
        self,
        config: Config,
        packet_timer: PacketTimer,
        duration_minutes: int = 5
    ) -> None:
        """Connect to sensor and read data for specified duration."""
        ...


class TimerInterface(Protocol):
    """Protocol for packet timing functionality."""
    
    def record_packet(self) -> Optional[float]:
        """Record packet timestamp and return interval since last packet."""
        ...
    
    def get_stats(self) -> Dict[str, float]:
        """Get comprehensive timing statistics."""
        ...
    
    def reset(self) -> None:
        """Reset all recorded data."""
        ...
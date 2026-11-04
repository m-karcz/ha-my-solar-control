"""
Runtime data types for my_solar_control.

Access pattern: entry.runtime_data.client / entry.runtime_data.coordinator
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import MySolarControlApiClient
    from .coordinator import MySolarControlDataUpdateCoordinator


type MySolarControlConfigEntry = ConfigEntry[MySolarControlData]


@dataclass
class MySolarControlData:
    """Runtime data stored on the config entry after a successful setup."""

    client: MySolarControlApiClient
    coordinator: MySolarControlDataUpdateCoordinator
    integration: Integration

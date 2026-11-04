"""Binary sensor platform for my_solar_control."""

from typing import TYPE_CHECKING

from .entity import MySolarControlBinarySensor
from .filter import ENTITY_DESCRIPTIONS as FILTER_DESCRIPTIONS
from .weekend import ENTITY_DESCRIPTIONS as WEEKEND_DESCRIPTIONS

# Read-only platform: the coordinator already serializes the fetch.
PARALLEL_UPDATES = 0

if TYPE_CHECKING:
    from custom_components.my_solar_control.data import MySolarControlConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

ENTITY_DESCRIPTIONS = (*FILTER_DESCRIPTIONS, *WEEKEND_DESCRIPTIONS)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MySolarControlConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        MySolarControlBinarySensor(entry.runtime_data.coordinator, description) for description in ENTITY_DESCRIPTIONS
    )

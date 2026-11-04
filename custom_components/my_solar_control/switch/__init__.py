"""Switch platform for my_solar_control."""

from typing import TYPE_CHECKING

from .example_switch import ENTITY_DESCRIPTIONS, MySolarControlSwitch

# Acts on the device: the coordinator does not limit outbound calls.
PARALLEL_UPDATES = 1

if TYPE_CHECKING:
    from custom_components.my_solar_control.data import MySolarControlConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MySolarControlConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        MySolarControlSwitch(entry.runtime_data.coordinator, description) for description in ENTITY_DESCRIPTIONS
    )

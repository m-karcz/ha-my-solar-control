"""
Custom integration to integrate my_solar_control with Home Assistant.

For more details about this integration, please refer to:
https://github.com/m-karcz/ha-my-solar-control
"""

from typing import TYPE_CHECKING

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import async_track_time_change
from homeassistant.loader import async_get_loaded_integration

from .api import MySolarControlApiClient
from .const import DOMAIN
from .coordinator import MySolarControlDataUpdateCoordinator
from .data import MySolarControlData
from .service_actions import async_setup_services

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import MySolarControlConfigEntry

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.FAN,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """
    Register the service actions.

    Returns:
        True once the actions are registered.

    """
    async_setup_services(hass)
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MySolarControlConfigEntry,
) -> bool:
    """
    Set up a config entry.

    Returns:
        True once the coordinator has data and every platform is forwarded.

    """
    client = MySolarControlApiClient(
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        session=async_get_clientsession(hass),
    )

    coordinator = MySolarControlDataUpdateCoordinator(hass, entry)

    entry.runtime_data = MySolarControlData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.async_on_unload(
        async_track_time_change(hass, coordinator.async_refresh_weekend, hour=0, minute=0, second=0),
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: MySolarControlConfigEntry,
) -> bool:
    """
    Unload a config entry.

    Returns:
        True if every platform unloaded cleanly.

    """
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

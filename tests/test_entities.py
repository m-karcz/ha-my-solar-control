"""Tests for the entities the example integration exposes."""

from datetime import datetime
from unittest.mock import AsyncMock

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry, async_fire_time_changed

from custom_components.my_solar_control.api import MySolarControlApiClientError
from custom_components.my_solar_control.const import CONF_FILTER_REPLACEMENT_THRESHOLD
from homeassistant.components.fan import DOMAIN as FAN_DOMAIN, SERVICE_SET_PERCENTAGE
from homeassistant.const import ATTR_ENTITY_ID, STATE_UNAVAILABLE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.util import dt as dt_util


async def test_entities_read_the_coordinator_payload(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """Every entity takes its state from the payload the client built."""
    # seed = 1 * 47 + 1 * 13 = 60
    assert hass.states.get("sensor.demo_filter_life_remaining").state == "40"
    assert hass.states.get("binary_sensor.demo_filter_replacement_needed").state == "off"
    assert hass.states.get("select.demo_fan_speed").state == "auto"
    assert hass.states.get("switch.demo_child_lock").state == "off"
    assert hass.states.get("number.demo_target_humidity").state == "50.0"


@pytest.mark.parametrize("config_entry", [{CONF_FILTER_REPLACEMENT_THRESHOLD: 50}], indirect=True)
@pytest.mark.usefixtures("init_integration")
async def test_filter_replacement_follows_the_threshold_option(hass: HomeAssistant) -> None:
    """A threshold above the remaining filter life turns the warning on."""
    assert hass.states.get("binary_sensor.demo_filter_replacement_needed").state == "on"


async def test_fan_is_the_main_feature_entity(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The fan carries the device name alone, not a repeated name."""
    state = hass.states.get("fan.demo")

    assert state is not None
    assert state.attributes["friendly_name"] == "demo"


async def test_led_display_is_disabled_by_default(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The noisy diagnostic switch is not created until the user enables it."""
    entry = er.async_get(hass).async_get("switch.demo_led_display")

    assert entry is not None
    assert entry.disabled_by is er.RegistryEntryDisabler.INTEGRATION


async def test_write_failure_raises_translated_error(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
    mock_api: AsyncMock,
) -> None:
    """A failing device call surfaces as a translated HomeAssistantError."""
    mock_api.side_effect = MySolarControlApiClientError("boom")

    with pytest.raises(HomeAssistantError) as err:
        await hass.services.async_call(
            FAN_DOMAIN,
            SERVICE_SET_PERCENTAGE,
            {ATTR_ENTITY_ID: "fan.demo", "percentage": 100},
            blocking=True,
        )

    assert err.value.translation_key == "fan_speed_set_failed"


async def test_entities_go_unavailable_when_the_poll_fails(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
    mock_api: AsyncMock,
) -> None:
    """A failed refresh makes the entities unavailable rather than stale."""
    mock_api.side_effect = MySolarControlApiClientError("boom")

    await init_integration.runtime_data.coordinator.async_refresh()
    await hass.async_block_till_done()

    assert hass.states.get("sensor.demo_filter_life_remaining").state == STATE_UNAVAILABLE


async def test_weekend_sensor_turns_on_at_local_midnight_without_a_poll(
    hass: HomeAssistant,
    freezer: FrozenDateTimeFactory,
    config_entry: MockConfigEntry,
    mock_api: AsyncMock,
) -> None:
    """The weekend sensor follows the local calendar and flips at midnight without calling the device again."""
    local_zone = dt_util.get_time_zone(hass.config.time_zone)
    freezer.move_to(datetime(2026, 11, 6, 23, 59, tzinfo=local_zone))
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.demo_weekend").state == "off"

    midnight = datetime(2026, 11, 7, tzinfo=local_zone)
    freezer.move_to(midnight)
    async_fire_time_changed(hass, midnight)
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.demo_weekend").state == "on"
    assert mock_api.call_count == 1

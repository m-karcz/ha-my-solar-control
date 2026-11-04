"""Fan speed select for my_solar_control."""

from custom_components.my_solar_control.api import FAN_SPEEDS
from custom_components.my_solar_control.const import DOMAIN
from custom_components.my_solar_control.entity import MySolarControlEntity
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.exceptions import ServiceValidationError

ENTITY_DESCRIPTIONS: tuple[SelectEntityDescription, ...] = (
    SelectEntityDescription(
        key="fan_speed",
        translation_key="fan_speed",
        options=list(FAN_SPEEDS),
    ),
)


class MySolarControlFanSpeedSelect(SelectEntity, MySolarControlEntity):
    """Select entity for the device's fan speed."""

    @property
    def current_option(self) -> str | None:
        """Return the fan speed read from coordinator data."""
        return self.coordinator.data.get("fan_speed")

    async def async_select_option(self, option: str) -> None:
        """Write the fan speed to the device."""
        if option not in FAN_SPEEDS:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="invalid_fan_speed",
                translation_placeholders={"speed": option},
            )

        await self._async_write(lambda client: client.async_set_fan_speed(option), "fan_speed_set_failed")

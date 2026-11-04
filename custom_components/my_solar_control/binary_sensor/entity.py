"""Binary sensor entity for my_solar_control."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from custom_components.my_solar_control.entity import MySolarControlEntity
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription


@dataclass(frozen=True, kw_only=True)
class MySolarControlBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a binary sensor and how to read it from coordinator data."""

    value_fn: Callable[[dict[str, Any]], bool | None]


class MySolarControlBinarySensor(BinarySensorEntity, MySolarControlEntity):
    """Binary sensor backed by one value in the coordinator payload."""

    entity_description: MySolarControlBinarySensorEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return the value read from coordinator data."""
        return self.entity_description.value_fn(self.coordinator.data)

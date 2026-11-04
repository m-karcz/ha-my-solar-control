"""Sensor entity for my_solar_control."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from custom_components.my_solar_control.entity import MySolarControlEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.typing import StateType


@dataclass(frozen=True, kw_only=True)
class MySolarControlSensorEntityDescription(SensorEntityDescription):
    """Describes a sensor and how to read it from coordinator data."""

    value_fn: Callable[[dict[str, Any]], StateType]


class MySolarControlSensor(SensorEntity, MySolarControlEntity):
    """Sensor backed by one value in the coordinator payload."""

    entity_description: MySolarControlSensorEntityDescription

    @property
    def native_value(self) -> StateType:
        """Return the value read from coordinator data."""
        return self.entity_description.value_fn(self.coordinator.data)

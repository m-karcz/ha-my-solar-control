"""Filter maintenance binary sensor descriptions for my_solar_control."""

from homeassistant.components.binary_sensor.const import BinarySensorDeviceClass

from .entity import MySolarControlBinarySensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[MySolarControlBinarySensorEntityDescription, ...] = (
    MySolarControlBinarySensorEntityDescription(
        key="filter_replacement",
        translation_key="filter_replacement",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda data: data.get("filter_replacement"),
    ),
)

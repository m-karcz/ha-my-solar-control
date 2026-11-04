"""Weekend binary sensor descriptions for my_solar_control."""

from .entity import MySolarControlBinarySensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[MySolarControlBinarySensorEntityDescription, ...] = (
    MySolarControlBinarySensorEntityDescription(
        key="is_weekend",
        translation_key="is_weekend",
        value_fn=lambda data: data.get("is_weekend"),
    ),
)

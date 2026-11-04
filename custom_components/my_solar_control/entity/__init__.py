"""
Entity package for my_solar_control.

Architecture:
    All platform entities inherit from (PlatformEntity, MySolarControlEntity).
    MRO order matters — platform-specific class first, then the integration base.
    Entities read data from coordinator.data and NEVER call the API client directly.
    Unique IDs follow the pattern: {entry_id}_{description.key}

See entity/base.py for the MySolarControlEntity base class.
"""

from .base import MySolarControlEntity

__all__ = ["MySolarControlEntity"]

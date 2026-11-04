"""
API package for my_solar_control.

Exception hierarchy:
    MySolarControlApiClientError (base)
    ├── MySolarControlApiClientCommunicationError (network/timeout)
    │   └── MySolarControlApiClientRateLimitError (429, carries retry_after)
    └── MySolarControlApiClientAuthenticationError (401/403)

The coordinator maps them onto ConfigEntryAuthFailed and UpdateFailed; nothing else
in the integration imports this package.
"""

from .client import (
    FAN_SPEEDS,
    MySolarControlApiClient,
    MySolarControlApiClientAuthenticationError,
    MySolarControlApiClientCommunicationError,
    MySolarControlApiClientError,
    MySolarControlApiClientRateLimitError,
)

__all__ = [
    "FAN_SPEEDS",
    "MySolarControlApiClient",
    "MySolarControlApiClientAuthenticationError",
    "MySolarControlApiClientCommunicationError",
    "MySolarControlApiClientError",
    "MySolarControlApiClientRateLimitError",
]

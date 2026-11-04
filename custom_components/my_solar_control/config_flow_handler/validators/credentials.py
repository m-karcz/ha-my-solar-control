"""Credential validation for the config flow."""

from typing import TYPE_CHECKING

from custom_components.my_solar_control.api import MySolarControlApiClient
from homeassistant.helpers.aiohttp_client import async_get_clientsession

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


async def validate_credentials(hass: HomeAssistant, username: str, password: str) -> None:
    """
    Test the credentials against the API.

    Args:
        hass: The Home Assistant instance.
        username: The username to validate.
        password: The password to validate.

    Raises:
        MySolarControlApiClientAuthenticationError: If the credentials are rejected.
        MySolarControlApiClientCommunicationError: If the API cannot be reached.
        MySolarControlApiClientError: For any other API failure.

    """
    client = MySolarControlApiClient(
        username=username,
        password=password,
        session=async_get_clientsession(hass),
    )
    await client.async_get_data()


__all__ = ["validate_credentials"]

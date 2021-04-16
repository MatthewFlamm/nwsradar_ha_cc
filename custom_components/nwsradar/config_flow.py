"""Config flow for National Weather Service (NWS) radar integration."""
import logging

import voluptuous as vol
from homeassistant import config_entries

from . import unique_id

# pylint: disable=unused-import
from .const import CONF_NEXRAD, CONF_STATION, CONF_TYPE, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for National Weather Service (NWS)."""

    # Start w v2 so that old integration configs dont cause issuea
    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
    _config = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # To enable other styles later
        self._config = {CONF_TYPE: CONF_NEXRAD}
        return await self.async_step_nexrad()

    async def async_step_nexrad(self, user_input=None):
        """Standard or enhanced step."""
        errors = {}
        if user_input is not None:
            self._config.update(user_input)
            title = unique_id(self._config)
            await self.async_set_unique_id(title)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=title, data=self._config)
        data_schema = vol.Schema(
            {
                vol.Required(CONF_STATION): str,
            }
        )
        return self.async_show_form(
            step_id="nexrad", data_schema=data_schema, errors=errors
        )

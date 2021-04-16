"""National Weather Service Radar integration."""
import asyncio
import datetime
import logging

import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pynwsradar import Nexrad

from .const import CONF_STATION, CONF_TYPE, DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["camera"]
SCAN_INTERVAL = datetime.timedelta(minutes=10)


def unique_id(config):
    """Return unique_id from config."""
    return f"{config[CONF_STATION]} {config[CONF_TYPE]}"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up nwsradar integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a National Weather Service entry."""
    hass_data = hass.data.setdefault(DOMAIN, {})

    station = entry.data[CONF_STATION]
    radar = Nexrad(station)

    radar_update = Debouncer(
        hass, _LOGGER, cooldown=60, immediate=True, function=radar.update
    )
    await radar_update.async_call()

    _LOGGER.debug("layers: %s", radar.layers)
    if radar.layers is None:
        raise ConfigEntryNotReady

    hass_data[entry.entry_id] = {"radar": radar, "radar_update": radar_update}

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    return unload_ok

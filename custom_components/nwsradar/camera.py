"""Provide animated GIF loops of NWS radar imagery."""
import logging
from datetime import timedelta

from homeassistant.components.camera import Camera
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import unique_id
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the nwsradar camera platform."""

    radar = hass.data[DOMAIN][entry.entry_id]["radar"]
    radar_update = hass.data[DOMAIN][entry.entry_id]["radar_update"]

    layers = radar.layers
    entities = []

    def update_data_factory(layer, radar_update):
        async def async_update_data():
            _LOGGER.debug("Updating radar info.")
            await radar_update.async_call()
            _LOGGER.debug("Updating layer info.")
            await hass.async_add_executor_job(layer.update_image(num=6))

        return async_update_data

    for layer_obj in layers.values():
        update_coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=f"{layer_obj.name} data",
            update_method=update_data_factory(layer_obj, radar_update),
            update_interval=MIN_TIME_BETWEEN_UPDATES,
        )

        if "cref" in layer_obj.name:
            await update_coordinator.async_refresh()
        entities.append(
            NWSRadarCam(
                unique_id(entry.data), layer_obj.name, update_coordinator, layer_obj
            )
        )
    async_add_entities(entities, False)


class NWSRadarCam(Camera):
    """A camera component producing animated NWS radar GIFs."""

    def __init__(self, id_unique, name, coordinator, cam):
        """Initialize the component."""
        super().__init__()
        self._name = name
        self._unique_id = id_unique
        self._cam = cam
        self._coordinator = coordinator

    @property
    def should_poll(self):
        return False

    def camera_image(self):
        """Return the current NWS radar loop"""
        _LOGGER.debug("display image")
        return self._cam.image()

    @property
    def name(self):
        """Return the component name."""
        return self._name

    @property
    def unique_id(self):
        """Return unique_id."""
        return f"{self._unique_id} {self._name}"

    @property
    def available(self):
        """Return availabilty of data."""
        return self._coordinator.last_update_success

    async def async_update(self):
        """Manual update entity."""
        await self._coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def entity_registry_enabled_default(self):
        if "cref" in self._name:
            return True
        return False

from unittest.mock import Mock

from homeassistant import config_entries
from homeassistant.components import camera
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.nwsradar.const import DOMAIN
from tests.const import NWSRADAR_CONFIG


async def test_camera(hass, mock_nexrad_data):

    entry = MockConfigEntry(domain=DOMAIN, data=NWSRADAR_CONFIG, version=2)
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("camera.klwx_cref")

    assert state
    assert state.state == "idle"
    image = await camera.async_get_image(hass, "camera.klwx_cref")
    assert image.content == b"test"

    assert mock_nexrad_data[1].call_count == 1
    assert mock_nexrad_data[2].call_count == 1

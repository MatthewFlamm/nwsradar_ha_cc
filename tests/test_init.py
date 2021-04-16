"""Tests for init module."""
from homeassistant.components.camera import DOMAIN as CAMERA_DOMAIN
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.nwsradar.const import DOMAIN
from tests.const import NWSRADAR_CONFIG


async def test_unload_entry(hass, mock_nexrad_data):
    """Test that nws setup with config yaml."""
    entry = MockConfigEntry(domain=DOMAIN, data=NWSRADAR_CONFIG, version=2)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert mock_nexrad_data[0].call_count == 1

    assert len(hass.states.async_entity_ids(CAMERA_DOMAIN)) == 1
    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 1

    assert await hass.config_entries.async_unload(entries[0].entry_id)
    assert await hass.config_entries.async_remove(entries[0].entry_id)
    await hass.async_block_till_done()
    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 0
    assert len(hass.states.async_entity_ids(CAMERA_DOMAIN)) == 0
    assert len(hass.states.async_entity_ids(DOMAIN)) == 0

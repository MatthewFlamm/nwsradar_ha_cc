"""Fixtures for National Weather Service Radar tests."""
from unittest.mock import patch

import pytest
from pytest_homeassistant_custom_component.common import load_fixture

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture
def mock_nexrad_data():
    data = load_fixture("station.xml")
    with patch(
        "custom_components.nwsradar.Nexrad._get_data", return_value=data
    ) as mock_nexrad_data, patch(
        "pynwsradar.nexrad.Layer.update_image"
    ) as mock_layer_update, patch(
        "pynwsradar.nexrad.Layer.image", return_value=b"test"
    ) as mock_layer_image:
        yield mock_nexrad_data, mock_layer_update, mock_layer_image

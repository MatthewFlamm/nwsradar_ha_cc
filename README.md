# nwsradar

Custom integration for NWS radar for Home Assistant.

## Installation

* This custom integration can be installed and managed using HACS.
* If you want to manually install, place files in the `custom_components/nwsradar/` folder into `path/to/haconfig/custom_components/nwsradar/`

## Configuration

Use UI to configure: **Configuration** -> **Integrations** -> **National Weather Service (NWS) Radar**

Works with picture-entity card:

```
- type: picture-entity
  entity: camera.vwx  # use your entity name
```

## Change log

# Configuration

Main configuration class for the IFC-to-CityGML conversion process.
Manages the mapping rules for buildings and bridges.

### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| lod | `string` | ✅ | [Lod](#lod) |  | The desired CityGML LOD level. |
| building_mapping | `object` or `null` |  | [BuildingMapping](#buildingmapping) | `null` | Specific mapping rules for building conversion. |
| bridge_mapping | `object` or `null` |  | [BridgeMapping](#bridgemapping) | `null` | Specific mapping rules for bridge conversion. |
| generic_mapping | `array` or `null` |  | [EntityMapping](#entitymapping) | `null` | Specific mapping rules for generic conversion. |


---

# Definitions

## BridgeMapping

Configuration for mapping IFC elements connected to IfcBridges to CityGML bridge components.

#### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| bridge_constructive_element | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for structural bridge elements like piers, abutments, or decks. |
| bridge_installation | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for bridge installations such as drainage systems or lighting. |
| bridge_furniture | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for bridge furniture like railings or signs. |
| bridge_room | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for enclosed spaces. |
| door | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for doors. |
| window | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for windows. |

## BuildingMapping

Configuration for mapping IFC elements connected to IfcBuildings to CityGML building components.

#### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| building_constructive_element | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for structural building elements such as walls, slabs, or columns. |
| building_installation | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for building installations and fixed technical equipment. |
| building_furniture | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for furniture. |
| building_room | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for spatial units and rooms. |
| door | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for doors. |
| window | `array` |  | [EntityMapping](#entitymapping) | `[]` | Mapping for windows. |

## EntityMapping

Defines the mapping between an IFC entity and its associated property sets.

#### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| entity | `string` | ✅ | string |  | The name of the IFC entity (e.g., 'IfcWall' or 'IfcBeam'). |
| property_sets | `array` |  | string | `[]` | A list of property set names to be extracted for this entity. |

## Lod

The available lods.

#### Type: `string`

**Possible Values:** `LOD_0` or `LOD_1` or `LOD_2` or `LOD_3`


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).

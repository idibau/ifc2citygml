# Configuration

Main configuration class of the IFC-to-CityGML conversion process.

### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| lod | `string` | ✅ | [Lod](#lod) |  | The desired CityGML LOD level. |
| building_mapping | `object` or `null` |  | [BuildingMapping](#buildingmapping) | `null` | Specific mapping rules of building elements. |
| bridge_mapping | `object` or `null` |  | [BridgeMapping](#bridgemapping) | `null` | Specific mapping rules of bridge elements. |
| other_construction_mapping | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Specific mapping rules of other construction elements. |
| generic_mapping | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Specific mapping rules of generic elements. |


---

# Definitions

## BridgeMapping

Specifies the mapping of bridges based on IFC elements connected to IfcBridges.

#### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| bridge_attributes | `object` or `null` |  | [GenericAttributeMapping](#genericattributemapping) | `null` | Mapping of bridge attributes. |
| bridge_part_attributes | `object` or `null` |  | [GenericAttributeMapping](#genericattributemapping) | `null` | Mapping of bridge part attributes. |
| bridge_constructive_element | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of structural bridge elements like piers, abutments, or decks. |
| bridge_installation | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of bridge installations such as drainage systems or lighting. |
| bridge_furniture | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of bridge furniture like railings or signs. |
| bridge_room | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of enclosed spaces. |
| door | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of doors. |
| window | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of windows. |

## BuildingMapping

Specifies the mapping of buildings based on IFC elements connected to IfcBuildings.

#### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| building_attributes | `object` or `null` |  | [GenericAttributeMapping](#genericattributemapping) | `null` | Mapping of building attributes. |
| storey_attributes | `object` or `null` |  | [GenericAttributeMapping](#genericattributemapping) | `null` | Mapping of storey attributes. |
| building_constructive_element | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of structural building elements such as walls, slabs, or columns. |
| building_installation | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of building installations and fixed technical equipment. |
| building_furniture | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of furniture. |
| building_room | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of spatial units and rooms. |
| door | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of doors. |
| window | `array` |  | [FeatureMapping](#featuremapping) | `[]` | Mapping of windows. |

## FeatureMapping

Specifies the mapping of features based on specific IFC elements.

#### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| entity | `string` | ✅ | string |  | The IFC entity of the element (e.g., 'IfcWall' or 'IfcBeam'). |
| predefined_type | `string` or `null` |  | string | `null` | The predefined type of the element. |
| object_type | `string` or `null` |  | string | `null` | The object type of the IFC element. |
| generic_attributes | `object` or `null` |  | [GenericAttributeMapping](#genericattributemapping) | `null` | Mapping of generic attributes. |

## GenericAttributeMapping

Specifies the mapping of generic attributes based on IFC properties and IFC attributes.

#### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| properties | `array` |  | string | `[]` | A list of IFC properties to be extracted. (pset_name.property_name) |
| attributes | `array` |  | string | `[]` | A list of IFC attributes to be extracted. |

## Lod

The available lods.

#### Type: `string`

**Possible Values:** `LOD_0` or `LOD_1` or `LOD_2` or `LOD_3`


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).

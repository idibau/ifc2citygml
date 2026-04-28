import os
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_yaml import parse_yaml_raw_as
from typing import List, Optional

from configuration.lod import Lod


class GenericAttributeMapping(BaseModel):
    """
    Specifies the mapping of generic attributes based on IFC properties and IFC attributes.
    """
    properties: List[str] = Field(
        default_factory=list,
        json_schema_extra={"default": []},
        description="A list of IFC properties to be extracted. (pset_name.property_name)"
    )
    attributes: List[str] = Field(
        default_factory=list,
        json_schema_extra={"default": []},
        description="A list of IFC attributes to be extracted."
    )


class FeatureMapping(BaseModel):
    """
    Specifies the mapping of features based on specific IFC elements.
    """
    entity: str = Field(..., description="The IFC entity of the element (e.g., 'IfcWall' or 'IfcBeam').")
    predefined_type: Optional[str] = Field(None, description="The predefined type of the element.")
    object_type: Optional[str] = Field(None, description="The object type of the IFC element.")
    generic_attributes: Optional[GenericAttributeMapping] = Field(None, description="Mapping of generic attributes.")


class BuildingMapping(BaseModel):
    """
    Specifies the mapping of buildings based on IFC elements connected to IfcBuildings.
    """
    building_attributes: Optional[GenericAttributeMapping] = Field(None,
                                                                 description="Mapping of building attributes.")
    storey_attributes: Optional[GenericAttributeMapping] = Field(None,
                                                             description="Mapping of storey attributes.")
    building_constructive_element: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of structural building elements such as walls, slabs, or columns."
    )
    building_installation: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of building installations and fixed technical equipment."
    )
    building_furniture: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of furniture."
    )
    building_room: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of spatial units and rooms."
    )
    door: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of doors."
    )
    window: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of windows."
    )


class BridgeMapping(BaseModel):
    """
    Specifies the mapping of bridges based on IFC elements connected to IfcBridges.
    """
    bridge_attributes: Optional[GenericAttributeMapping] = Field(None,
                                                                 description="Mapping of bridge attributes.")
    bridge_part_attributes: Optional[GenericAttributeMapping] = Field(None,
                                                             description="Mapping of bridge part attributes.")
    bridge_constructive_element: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of structural bridge elements like piers, abutments, or decks."
    )
    bridge_installation: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of bridge installations such as drainage systems or lighting."
    )
    bridge_furniture: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of bridge furniture like railings or signs."
    )
    bridge_room: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of enclosed spaces."
    )
    door: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of doors."
    )
    window: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping of windows."
    )


class Configuration(BaseModel):
    """
    Main configuration class of the IFC-to-CityGML conversion process.
    """
    lod: Lod = Field(..., description="The desired CityGML LOD level.")
    building_mapping: Optional[BuildingMapping] = Field(
        None,
        description="Specific mapping rules of building elements."
    )
    bridge_mapping: Optional[BridgeMapping] = Field(
        None,
        description="Specific mapping rules of bridge elements."
    )
    other_construction_mapping: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Specific mapping rules of other construction elements."
    )
    generic_mapping: List[FeatureMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Specific mapping rules of generic elements."
    )

    @classmethod
    def load(cls, path: str) -> "Configuration":
        text = Path(path).read_text()
        expanded = os.path.expandvars(text)
        return parse_yaml_raw_as(cls, expanded)

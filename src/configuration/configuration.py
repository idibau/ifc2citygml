import os
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_yaml import parse_yaml_raw_as
from typing import List, Optional

from configuration.lod import Lod


class EntityMapping(BaseModel):
    """
    Defines the mapping between an IFC entity and its associated property sets.
    """
    entity: str = Field(..., description="The name of the IFC entity (e.g., 'IfcWall' or 'IfcBeam').")
    property_sets: List[str] = Field(
        default_factory=list,
        json_schema_extra={"default": []},
        description="A list of property set names to be extracted for this entity."
    )


class BuildingMapping(BaseModel):
    """
    Configuration for mapping IFC elements connected to IfcBuildings to CityGML building components.
    """
    building_constructive_element: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for structural building elements such as walls, slabs, or columns."
    )
    building_installation: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for building installations and fixed technical equipment."
    )
    building_furniture: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for furniture."
    )
    building_room: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for spatial units and rooms."
    )
    door: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for doors."
    )
    window: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for windows."
    )


class BridgeMapping(BaseModel):
    """
    Configuration for mapping IFC elements connected to IfcBridges to CityGML bridge components.
    """
    bridge_constructive_element: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for structural bridge elements like piers, abutments, or decks."
    )
    bridge_installation: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for bridge installations such as drainage systems or lighting."
    )
    bridge_furniture: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for bridge furniture like railings or signs."
    )
    bridge_room: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for enclosed spaces."
    )
    door: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for doors."
    )
    window: List[EntityMapping] = Field(
        default_factory=list, json_schema_extra={"default": []},
        description="Mapping for windows."
    )


class Configuration(BaseModel):
    """
    Main configuration class for the IFC-to-CityGML conversion process.
    Manages the mapping rules for buildings and bridges.
    """
    lod: Lod = Field(..., description="The desired CityGML LOD level.")
    building_mapping: Optional[BuildingMapping] = Field(
        None,
        description="Specific mapping rules for building conversion."
    )
    bridge_mapping: Optional[BridgeMapping] = Field(
        None,
        description="Specific mapping rules for bridge conversion."
    )
    generic_mapping: Optional[List[EntityMapping]] = Field(
        None,
        description="Specific mapping rules for generic conversion."
    )

    @classmethod
    def load(cls, path: str) -> "Configuration":
        text = Path(path).read_text()
        expanded = os.path.expandvars(text)
        return parse_yaml_raw_as(cls, expanded)

import os
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_yaml import parse_yaml_raw_as
from typing import List, Optional


class EntityMapping(BaseModel):
    entity: str = Field(..., description="")
    property_sets: List[str] = Field(default_factory=list, json_schema_extra={"default": []},
                                     description="")


class BuildingMapping(BaseModel):
    building_constructive_element: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []},
                                                               description="")
    building_installation: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []},
                                                       description="")
    building_furniture: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []},
                                                    description="")
    building_room: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []}, description="")
    door: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []}, description="")
    window: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []}, description="")


class BridgeMapping(BaseModel):
    bridge_constructive_element: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []},
                                                             description="")
    bridge_installation: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []},
                                                     description="")
    bridge_furniture: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []},
                                                  description="")
    bridge_room: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []}, description="")
    door: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []}, description="")
    window: List[EntityMapping] = Field(default_factory=list, json_schema_extra={"default": []}, description="")


class Configuration(BaseModel):
    building_mapping: Optional[BuildingMapping] = Field(None, description="Database configuration")
    bridge_mapping: Optional[BridgeMapping] = Field(None, description="STAC configuration for external data sources")

    @classmethod
    def load(cls, path: str) -> "Configuration":
        text = Path(path).read_text()
        expanded = os.path.expandvars(text)
        return parse_yaml_raw_as(cls, expanded)


config = Configuration.load("/workspace/config.yml")

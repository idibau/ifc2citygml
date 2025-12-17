# 3D-GIS-BIM

<!-- TOC -->

* [3D-GIS-BIM](#3d-gis-bim)
    * [Project description](#project-description)
    * [Getting started](#getting-started)
    * [Getting started (Development)](#getting-started-development)
    * [Mapping](#mapping)

<!-- TOC -->

## Project description

...

## Getting started

Build the docker image:

```console
docker build -t ifc2gml .
```

Run the docker container:

```console
docker run --rm -v .:/workspace/data ifc2gml data/input.ifc data/output.gml
```

The tool is executed by running main.py. It expect the following parameters:

1. Path to the input IFC file
2. Path to the output GML file
3. Center the model in the output GML (optional boolean flag)

## Getting started (Development)

Build and run docker container or build and open a container with your IDE (e.g., VSCode, PyCharm)

```console
docker-compose -f docker-compose-dev.yml up 
```

Install pip packages (Run in container at /workspace)

```console
pip install --no-cache-dir --upgrade -r /workspace/requirements.txt
```

## Mapping

The following Ifc entities are considered during the conversion. Prerequisite: The elements are assigned to a building.

| Target GML Class                                                | Corresponding IFC Entities                                                                                                                             |
|:----------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Building**                                                    | `IfcBuilding`                                                                                                                                          |
| **Storey**                                                      | `IfcBuildingStorey`                                                                                                                                    |
| **Bridge**                                                      | `IfcBridge`                                                                                                                                            |
| **BridgePart**                                                  | `IfcBridgePart`                                                                                                                                        |
| **BuildingConstructionElement** / **BridgeConstructionElement** | `IfcBeam`, `IfcColumn`, `IfcFooting`, `IfcMember`, `IfcPlate`, `IfcWall`, `IfcWallStandardCase`, `IfcRoof`, `IfcCurtainWall`, `IfcSlab`, `IfcCovering` |
| **BuildingInstallation** / **BridgeInstallation**               | `IfcRailing`, `IfcRamp`, `IfcRampFlight`, `IfcStair`, `IfcStairFlight`, `IfcBuildingElementProxy`, `IfcBuildingElementComponent`, `IfcPile`            |
| **BuildingRoom** / **BridgeRoom**                               | `IfcSpace`                                                                                                                                             |
| **BuildingFurniture** /  **BridgeFurniture**                    | `IfcFurnishingElement`                                                                                                                                 |
| **Door**                                                        | `IfcDoor`                                                                                                                                              |
| **Window**                                                      | `IfcWindow`                                                                                                                                            |


## Georeferencing

CityGML requires the use of global coordinates. To convert the IFC model correctly, the Georeferencing information must be accurately processed. Supported are the following coordinate reference systems:

- LO_GEO_REF_30
    - IfcObjectPlacement of an IfcSpatialStructureElement contains georeferencing
- LO_GEO_REF_40
    - IfcGeometricRepresentation context of IfcProject contains georeferencing
- LO_GEO_REF_50
    - IfcMapConversion defines georeferencing of the "SurveyPoint", including coordinate system parameters

For every supported georeferencing the tool applies a transformation matrix to all geometries in the model, converting them from local values into global values.
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

    IfcBuildingStorey
    =================
    Storey

    BuildingConstructionElement    
    ===========================
    IfcBeam
    IfcColumn
    IfcFooting
    IfcMember
    IfcPlate
    IfcWall
    IfcWallStandardCase
    IfcRoof
    IfcCurtainWall
    IfcSlab
    IfcCovering

    BuildingInstallation
    ====================
    IfcRailing
    IfcRamp
    IfcRampFlight
    IfcStair
    IfcStairFlight
    IfcBuildingElementProxy
    IfcBuildingElementComponent
    IfcPile

    BuildingRoom
    ============
    IfcSpace
    
    BuildingFurniture
    =================
    IfcFurnishingElement

    Door
    ====
    IfcDoor

    Window
    ======
    IfcWindow
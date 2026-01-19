# 3D-GIS-BIM

<!-- TOC -->
* [3D-GIS-BIM](#3d-gis-bim)
  * [Project description](#project-description)
  * [Getting started](#getting-started)
  * [Getting started (Development)](#getting-started-development)
  * [Configuration](#configuration)
    * [Configuration Sections](#configuration-sections)
    * [Spatial Structure](#spatial-structure)
    * [Property Mapping](#property-mapping)
    * [Technical documentation](#technical-documentation)
  * [Georeferencing](#georeferencing)
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
docker run --rm -v .:/data -w /data ifc2gml input.ifc output.gml
```

The tool is executed by running main.py. It expect the following parameters:

1. Path to the input IFC file
2. Path to the output GML file

The tool uses a [default configuration](config.yml). To use your own, you can map a specific file from your host machine
to the
exact location where the tool expects its configuration.

```console
docker run --rm -v .:/data -v ./my_local_config.yml:/workspace/config.yml -w /data ifc2gml input.ifc output.gml
```

## Getting started (Development)

Build and run docker container or build and open a container with your IDE (e.g., VSCode, PyCharm)

```console
docker-compose -f docker-compose-dev.yml up 
```

Install pip packages (Run in container at /workspace)

```console
pip install --no-cache-dir --upgrade -r /workspace/requirements.txt
```

## Configuration

The conversion process is managed through a configuration file that defines which **IFC entities** and **PropertySets**
are included in the transformation.

### Configuration Sections

The configuration is divided into two primary sections:

* **Building Configuration:** Targets all `IfcProduct` entities associated with an `IfcBuilding`.
* **Bridge Configuration:** Targets all `IfcProduct` entities associated with an `IfcBridge`.
* **Other Construction Configuration:** Targets all other `IfcProduct` entities that were not processed by the previous
  two sections.
* **Generic Configuration:** Targets all other `IfcProduct` entities that were not processed by the previous three
  sections.

### Spatial Structure

The converter automatically recognizes spatial structures defined within the IFC file:

* **Buildings:** `IfcBuildingStorey` structures are identified.
* **Bridges:** `IfcBridgePart` structures are identified.

Note: To ensure compatibility and simplicity in the output, any nested spatial hierarchies are flattened
to a single level during the conversion.

### Property Mapping

For each entity defined in the configuration, you can specify which **Properties** should be transferred. These
properties are automatically mapped to **Generic Attribute Sets** within the resulting CityGML file. Use this notation
to configure the properties: \$pset.\$property.

### Technical documentation

The technical documentation can be found [here](configuration_schema.md). To generate the document "configuration
schema" do the following:

Generate json schema:

```
with open("configuration.json", "w") as stream:
    import json
    json.dump(Configuration.model_json_schema(), stream, indent=4)
```

Generate markdown with [jsonschema-markdown](https://pypi.org/project/jsonschema-markdown/):

```
jsonschema-markdown configuration.json > configuration_schema.md --no-empty-columns
```

## Georeferencing

CityGML requires the use of global coordinates. To convert the IFC model correctly, the Georeferencing information must
be accurately processed. Supported are the following coordinate reference systems:

- **LO_GEO_REF_30**
    - IfcObjectPlacement of an IfcSpatialStructureElement contains georeferencing
- **LO_GEO_REF_40**
    - IfcGeometricRepresentation context of IfcProject contains georeferencing
- **LO_GEO_REF_50**
    - IfcMapConversion defines georeferencing of the "SurveyPoint", including coordinate system parameters

For every supported georeferencing the tool applies a transformation matrix to all geometries in the model, converting
them from local values into global values.
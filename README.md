docker build -t ifc2gml .

docker run --rm -v .:/workspace ifc2gml input.ifc output.gml
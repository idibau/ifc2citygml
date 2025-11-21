docker build -t ifc2gml .

docker run --rm -v .:/data ifc2gml /data/input.ifc /data/output.gml
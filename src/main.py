import argparse
import pathlib

import ifcopenshell

from core.ifc_to_gml import convert


def main():
    parser = argparse.ArgumentParser(description="Convert IFC to GML")
    parser.add_argument("input", type=pathlib.Path, help="Path to the input IFC file")
    parser.add_argument("output", type=pathlib.Path, help="Path to the output GML file")
    args = parser.parse_args()

    print(f"Reading file: {args.input}")
    model = ifcopenshell.open(str(args.input))

    print("Converting...")
    document = convert(model, args.input.stem)

    print(f"Writing GML: {args.output}")
    document.write(str(args.output))

    print("Done")


if __name__ == "__main__":
    main()

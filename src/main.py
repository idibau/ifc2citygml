import argparse
import logging
import pathlib
import sys

import ifcopenshell

from core.ifc_to_gml import convert

logging_format = "%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s"
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter(logging_format))

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(stream_handler)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Convert IFC to GML")
    parser.add_argument("input", type=pathlib.Path, help="Path to the input IFC file")
    parser.add_argument("output", type=pathlib.Path, help="Path to the output GML file")
    parser.add_argument(
        "--center-model",
        action="store_true",
        help="Center the model in the output GML (optional boolean flag)"
    )
    args = parser.parse_args()

    logger.info(f"Reading IFC: {args.input}")
    model = ifcopenshell.open(str(args.input))

    logger.info("Converting")
    document = convert(model, args.input.stem, args.center_model)

    logger.info(f"Writing GML: {args.output}")
    document.write(str(args.output))

    logger.info("Done")


if __name__ == "__main__":
    main()

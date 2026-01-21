import argparse
import logging
import pathlib
import sys
from datetime import datetime

import ifcopenshell

from configuration.configuration import Configuration
from core.ifc_to_gml import convert
from model.document import Document

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
    args = parser.parse_args()

    file_handler = logging.FileHandler(f"{datetime.now().isoformat()}.log")
    root_logger.addHandler(file_handler)

    logger.info(f"Reading IFC: {args.input}")
    model = ifcopenshell.open(str(args.input))

    logger.info("Converting")

    config = Configuration.load("/workspace/config.yml")
    with Document(args.input.stem, str(args.output)) as document:
        convert(model, document, config)

    logger.info("Done")


if __name__ == "__main__":
    main()

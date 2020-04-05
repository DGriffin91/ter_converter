import numpy as np
import os
import imageio
import struct
import argparse
from pathlib import Path


def scan(header, token, nbytes, fmt, offset=0):
    pos = header.find(token) - 0 + offset + len(token)
    return struct.unpack(fmt, header[pos : pos + nbytes])[0]


def convert(
    input_file_path, output_file_path, use_base_height, use_height_scale, convert_log_scale
):

    print("--- Data Loading     ---")
    f = open(Path(input_file_path), "rb")

    header = f.read(83)

    width = scan(header, b"XPTS", 2, "H")
    height = scan(header, b"YPTS", 2, "H")

    size = scan(header, b"SIZE", 2, "H")
    scale = scan(header, b"SCAL", 2, "H")
    radius = scan(header, b"CRAD", 4, ">i")
    mode = scan(header, b"CRVM", 4, ">f")
    height_scale = scan(header, b"ALTW", 2, "H", offset=0)
    base_height = scan(header, b"ALTW", 2, "H", offset=2)

    print(
        "Width: ",
        width,
        "Height: ",
        height,
        "Size: ",
        size,
        "Scale: ",
        scale,
        "Radius: ",
        radius,
        "Mode: ",
        mode,
        "Height scale: ",
        height_scale,
        "Base height: ",
        base_height,
    )

    print("--- Data Formatting  ---")

    data = np.fromfile(f, dtype=">i2")
    data = data.reshape((width, height)).astype(np.float32)

    print("--- Data Processing  ---")

    if use_base_height:
        data += base_height
    if use_height_scale:
        data *= height_scale
    data = (data / 65535) + 1.0
    if convert_log_scale:
        data = np.log10(data)
    data = data + 0.5

    print("--- Data Writing     ---")

    imageio.imwrite(Path(output_file_path), data)


if __name__ == "__main__":

    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    parser = argparse.ArgumentParser(prog="python ter_converter.py")
    parser.add_argument("-i", dest="input_file_path", help="input file path", required=True)
    parser.add_argument("-o", dest="output_file_path", help="output file path", required=True)
    parser.add_argument(
        "use_base_height",
        help="use base height",
        type=str2bool,
        default=False,
        const=True,
        nargs="?",
    )
    parser.add_argument(
        "use_height_scale",
        help="use height scale",
        type=str2bool,
        default=False,
        const=True,
        nargs="?",
    )
    parser.add_argument(
        "convert_log_scale",
        help="convert log scale",
        type=str2bool,
        default=False,
        const=True,
        nargs="?",
    )
    args = parser.parse_args()

    convert(
        args.input_file_path,
        args.output_file_path,
        args.use_base_height,
        args.use_height_scale,
        args.convert_log_scale,
    )

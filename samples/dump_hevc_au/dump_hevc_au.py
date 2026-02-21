#!/usr/bin/env python3
"""
Dump H.265/HEVC access units.

This sample parses an H.265/HEVC elementary stream and dumps each access unit
to a separate file. It also prints the NAL unit types contained in each AU.

HEVC NAL unit header (2 bytes):
  forbidden_zero_bit    (1 bit)
  nal_unit_type         (6 bits)
  nuh_layer_id          (6 bits)
  nuh_temporal_id_plus1 (3 bits)

nal_unit_type = (first_byte >> 1) & 0x3F
"""

import os
import sys
import shutil
import click

from avblocks import (
    Library, Transcoder, MediaSocket, MediaPin, MediaSample,
    VideoStreamInfo, StreamType, ErrorFacility
)


# Network Abstraction Layer Unit Type Definitions per H.265/HEVC spec (ITU-T H.265 Table 7-1)
NALU_TYPES = {
    0:  "TRAIL_N",
    1:  "TRAIL_R",
    2:  "TSA_N",
    3:  "TSA_R",
    4:  "STSA_N",
    5:  "STSA_R",
    6:  "RADL_N",
    7:  "RADL_R",
    8:  "RASL_N",
    9:  "RASL_R",
    16: "BLA_W_LP",
    17: "BLA_W_RADL",
    18: "BLA_N_LP",
    19: "IDR_W_RADL",
    20: "IDR_N_LP",
    21: "CRA_NUT",
    32: "VPS_NUT",
    33: "SPS_NUT",
    34: "PPS_NUT",
    35: "AUD_NUT",
    36: "EOS_NUT",
    37: "EOB_NUT",
    38: "FD_NUT",
    39: "PREFIX_SEI",
    40: "SUFFIX_SEI",
}


def get_nalu_type(first_byte: int) -> int:
    """Get NAL unit type from first header byte.
    
    nal_unit_type occupies bits [6:1] of the first header byte.
    """
    return (first_byte >> 1) & 0x3F


def get_nalu_type_name(nalu_type: int) -> str:
    """Get NAL unit type name."""
    return NALU_TYPES.get(nalu_type, f"RSV_{nalu_type}")


def print_nalu_header(byte: int):
    """Print HEVC NAL unit header information."""
    nalu_type = get_nalu_type(byte)
    print(f"  {get_nalu_type_name(nalu_type)}")


def print_nalus(data: bytes):
    """Parse and print NAL units from an access unit buffer."""
    pos = 0
    size = len(data)
    
    while size > 1:
        # Check for 3-byte start code prefix (0x000001)
        if size >= 3 and data[pos] == 0 and data[pos + 1] == 0 and data[pos + 2] == 1:
            if size >= 4:
                print_nalu_header(data[pos + 3])
            pos += 3
            size -= 3
        # Check for 4-byte start code prefix (0x00000001)
        elif size >= 4 and data[pos] == 0 and data[pos + 1] == 0 and data[pos + 2] == 0 and data[pos + 3] == 1:
            if size >= 5:
                print_nalu_header(data[pos + 4])
            pos += 4
            size -= 4
        else:
            pos += 1
            size -= 1


def write_au_file(output_dir: str, au_index: int, data: bytes):
    """Write an access unit to a file."""
    filepath = os.path.join(output_dir, f"au_{au_index:04d}.h265")
    with open(filepath, 'wb') as f:
        f.write(data)


def delete_directory(dir_path: str):
    """Delete a directory if it exists."""
    try:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    except OSError:
        pass


def make_dir(dir_path: str) -> bool:
    """Create directory if it doesn't exist."""
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return True
    except OSError:
        return False


def print_error(action: str, error) -> None:
    """Print error information."""
    if action:
        print(f"{action}: ", end="")
    
    if error.facility == ErrorFacility.Success:
        print("Success")
        return
    
    print(f"{error.message or ''}, facility:{error.facility} code:{error.code} hint:{error.hint or ''}")


def parse_h265_stream(input_file: str, output_dir: str) -> bool:
    """Parse H.265 stream and dump access units."""
    delete_directory(output_dir)
    
    in_socket = MediaSocket()
    in_socket.file = input_file
    
    # Create an output socket with one video pin configured for H.265
    out_pin = MediaPin()
    out_vsi = VideoStreamInfo()
    out_vsi.stream_type = StreamType.H265
    out_pin.stream_info = out_vsi
    
    out_socket = MediaSocket()
    out_socket.pins.add(out_pin)
    
    with Transcoder() as transcoder:
        transcoder.inputs.add(in_socket)
        transcoder.outputs.add(out_socket)
        
        res = transcoder.open()
        print_error("transcoder open", transcoder.error)
        
        if not res:
            return False
        
        if not make_dir(output_dir):
            print(f"cannot create output directory: {output_dir}")
            return False
        
        au_index = 0
        sample = MediaSample()
        
        while True:
            res, _ = transcoder.pull(sample)
            if not res:
                break
            
            # Each call to transcoder.pull returns one Access Unit.
            # The Access Unit may contain one or more NAL units.
            au_data = bytes(sample.buffer.data)
            print(f"AU #{au_index}, {len(au_data)} bytes")
            write_au_file(output_dir, au_index, au_data)
            print_nalus(au_data)
            au_index += 1
        
        transcoder.close()
    
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input file (HEVC/H.265)',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_dir',
              help='Output directory',
              type=click.Path())
def main(input_file: str, output_dir: str):
    """Dump H.265/HEVC access units."""
    
    # Set default options if not provided
    if not input_file or not output_dir:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../../assets/vid/foreman_qcif.h265")
        if not output_dir:
            output_dir = os.path.join(script_dir, "../../output/dump_hevc_au")
        
        print("Using default options:")
        print(f"  --input {input_file}")
        print(f"  --output {output_dir}")
        print()
    
    # Validate options
    print(f"--input: {input_file}")
    print(f"--output: {output_dir}")
    
    Library.initialize()
    
    # Set license information. Without this AVBlocks runs in Demo mode.
    # Library.set_license("<license-string>")
    
    result = parse_h265_stream(input_file, output_dir)
    
    Library.shutdown()
    
    if result:
        print(f"\nSuccessfully parsed input file: {input_file}")
        print(f"Output directory: {output_dir}")
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

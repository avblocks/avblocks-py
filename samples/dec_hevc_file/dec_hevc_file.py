#!/usr/bin/env python3
"""
Decode H.265/HEVC file to YUV.

This sample decodes an H.265/HEVC video file to raw YUV format using AVBlocks.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaInfo, MediaSocket, MediaPin,
    VideoStreamInfo, StreamType, ColorFormat, ErrorFacility
)


def delete_file(filename: str):
    """Delete a file if it exists."""
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except OSError:
        pass


def print_error(action: str, error) -> None:
    """Print error information."""
    if action:
        print(f"{action}: ", end="")
    
    if error.facility == ErrorFacility.Success:
        print("Success")
        return
    
    print(f"{error.message or ''}, facility:{error.facility} code:{error.code} hint:{error.hint or ''}")


def create_output_socket(output_file: str) -> MediaSocket:
    """Create output socket for YUV file."""
    socket = MediaSocket()
    socket.file = output_file
    socket.stream_type = StreamType.UncompressedVideo
    
    pin = MediaPin()
    socket.pins.add(pin)
    
    vsi = VideoStreamInfo()
    pin.stream_info = vsi
    
    vsi.stream_type = StreamType.UncompressedVideo
    vsi.color_format = ColorFormat.YUV420
    
    return socket


def decode(input_file: str, output_file: str) -> bool:
    """Decode H.265/HEVC file to YUV."""
    # Transcoder will fail if output exists (by design)
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open input file with MediaInfo
    media_info = MediaInfo()
    media_info.inputs[0].file = input_file
    
    if not media_info.open():
        print_error("MediaInfo.open()", media_info.error)
        return False
    
    in_socket = MediaSocket.from_media_info(media_info)
    out_socket = create_output_socket(output_file)
    
    # Create transcoder
    with Transcoder() as transcoder:
        transcoder.allow_demo_mode = True
        transcoder.inputs.add(in_socket)
        transcoder.outputs.add(out_socket)
        
        res = transcoder.open()
        print_error("Transcoder open", transcoder.error)
        if not res:
            return False
        
        res = transcoder.run()
        print_error("Transcoder run", transcoder.error)
        if not res:
            return False
        
        transcoder.close()
        print_error("Transcoder close", transcoder.error)
    
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input HEVC / H.265 file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='Output YUV file',
              type=click.Path())
def main(input_file: str, output_file: str):
    """Decode H.265/HEVC file to YUV."""
    
    # Set default options if not provided
    if not input_file or not output_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../../assets/vid/foreman_qcif.h265")
        if not output_file:
            output_file = os.path.join(script_dir, "../../output/dec_hevc_file/foreman_qcif.yuv")
        
        print("Using default options:")
        print(f"  --input {input_file}")
        print(f"  --output {output_file}")
        print()
    
    # Validate options
    print(f"--input: {input_file}")
    print(f"--output: {output_file}")
    
    Library.initialize()
    
    # Set license information. Without this AVBlocks runs in Demo mode.
    # Library.set_license("<license-string>")
    
    result = decode(input_file, output_file)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

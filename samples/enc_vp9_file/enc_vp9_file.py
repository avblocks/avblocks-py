#!/usr/bin/env python3
"""
Encode YUV file to VP9/IVF.

This sample encodes a raw YUV video file to VP9 format in an IVF container using AVBlocks.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaSocket, MediaPin,
    VideoStreamInfo, StreamType, ColorFormat, ScanType, ErrorFacility
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


# Color format mapping
COLOR_FORMATS = {
    'yuv420': ColorFormat.YUV420,
    'yv12': ColorFormat.YV12,
    'nv12': ColorFormat.NV12,
    'yuv422': ColorFormat.YUV422,
    'bgra32': ColorFormat.BGRA32,
    'bgr24': ColorFormat.BGR24,
}


def create_input_socket(input_file: str, width: int, height: int, 
                        fps: float, color_format: int) -> MediaSocket:
    """Create input socket for YUV file."""
    socket = MediaSocket()
    socket.stream_type = StreamType.UncompressedVideo
    socket.file = input_file
    
    pin = MediaPin()
    socket.pins.add(pin)
    
    vsi = VideoStreamInfo()
    pin.stream_info = vsi
    
    vsi.stream_type = StreamType.UncompressedVideo
    vsi.scan_type = ScanType.Progressive
    vsi.frame_width = width
    vsi.frame_height = height
    vsi.color_format = color_format
    vsi.frame_rate = fps
    
    return socket


def create_output_socket(output_file: str) -> MediaSocket:
    """Create output socket for VP9/IVF file."""
    socket = MediaSocket()
    socket.file = output_file
    socket.stream_type = StreamType.IVF
    
    pin = MediaPin()
    socket.pins.add(pin)
    
    vsi = VideoStreamInfo()
    pin.stream_info = vsi
    
    vsi.stream_type = StreamType.VP9
    
    return socket


def encode(input_file: str, output_file: str, width: int, height: int,
           fps: float, color_format: int) -> bool:
    """Encode YUV file to VP9/IVF."""
    # Transcoder will fail if output exists (by design)
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create input socket
    in_socket = create_input_socket(input_file, width, height, fps, color_format)
    
    # Create output socket
    out_socket = create_output_socket(output_file)
    
    # Create transcoder
    with Transcoder() as transcoder:
        transcoder.allow_demo_mode = True
        transcoder.inputs.add(in_socket)
        transcoder.outputs.add(out_socket)
        
        if not transcoder.open():
            print_error("Transcoder open", transcoder.error)
            return False
        
        if not transcoder.run():
            print_error("Transcoder run", transcoder.error)
            return False
        
        transcoder.close()
    
    return True


def parse_frame_size(frame_size: str) -> tuple:
    """Parse frame size string (e.g., '176x144') to (width, height) tuple."""
    parts = frame_size.lower().split('x')
    if len(parts) != 2:
        raise ValueError(f"Invalid frame size: {frame_size}")
    return int(parts[0]), int(parts[1])


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input YUV file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='Output IVF file',
              type=click.Path())
@click.option('-r', '--rate', 'fps',
              help='Input frame rate',
              default=30.0,
              type=float)
@click.option('-f', '--frame', 'frame_size',
              help='Input frame size (e.g., 176x144)',
              default='176x144',
              type=str)
@click.option('-c', '--color', 'color_format',
              help='Input color format',
              default='yuv420',
              type=click.Choice(list(COLOR_FORMATS.keys()), case_sensitive=False))
@click.option('--colors', 'list_colors',
              help='List supported input color formats',
              is_flag=True)
def main(input_file: str, output_file: str, fps: float, frame_size: str, 
         color_format: str, list_colors: bool):
    """Encode YUV file to VP9/IVF."""
    
    # List color formats if requested
    if list_colors:
        print("Supported color formats:")
        for name in COLOR_FORMATS:
            print(f"  {name}")
        return
    
    # Parse frame size
    try:
        width, height = parse_frame_size(frame_size)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Set default options if not provided
    if not input_file or not output_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../../assets/vid/foreman_qcif.yuv")
        if not output_file:
            output_file = os.path.join(script_dir, "../../output/enc_vp9_file/foreman_qcif.ivf")
        
        print("Using default options:")
        print(f"  --input {input_file}")
        print(f"  --output {output_file}")
        print(f"  --rate {fps}")
        print(f"  --frame {frame_size}")
        print(f"  --color {color_format}")
        print()
    
    # Validate options
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Frame rate: {fps}")
    print(f"Frame size: {width}x{height}")
    print(f"Color format: {color_format}")
    
    Library.initialize()
    
    # Set license information. To run AVBlocks in demo mode, comment the next line out
    # Library.set_license("<license-string>")
    
    result = encode(input_file, output_file, width, height, fps, 
                   COLOR_FORMATS[color_format.lower()])
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

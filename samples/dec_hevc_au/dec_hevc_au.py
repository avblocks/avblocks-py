#!/usr/bin/env python3
"""
Decode H.265/HEVC access units to YUV.

This sample decodes a sequence of H.265 access unit files to raw YUV format.
Each AU file contains a single NAL unit (e.g., au_0000.h265, au_0001.h265, etc.).
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaInfo, MediaSocket, MediaPin,
    VideoStreamInfo, MediaSample, MediaBuffer, StreamType, 
    ColorFormat, ScanType, ErrorFacility
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


def build_au_path(input_dir: str, index: int) -> str:
    """Build the path to an access unit file."""
    pattern = "au_{:04d}.h265"
    return os.path.join(input_dir, pattern.format(index))


def create_output_socket(output_file: str, color_format: int) -> MediaSocket:
    """Create output socket for YUV file."""
    socket = MediaSocket()
    socket.file = output_file
    socket.stream_type = StreamType.UncompressedVideo
    
    pin = MediaPin()
    socket.pins.add(pin)
    
    vsi = VideoStreamInfo()
    pin.stream_info = vsi
    
    vsi.stream_type = StreamType.UncompressedVideo
    vsi.color_format = color_format
    vsi.scan_type = ScanType.Progressive
    
    return socket


def configure_transcoder(transcoder: Transcoder, au_file: str, output_file: str, color_format: int) -> bool:
    """Configure transcoder using the first AU file."""
    media_info = MediaInfo()
    media_info.inputs[0].file = au_file
    
    if not media_info.open():
        print_error("MediaInfo open", media_info.error)
        return False
    
    # Create input socket from media info
    in_socket = MediaSocket.from_media_info(media_info)
    in_socket.file = None
    
    # Create output socket
    out_socket = create_output_socket(output_file, color_format)
    
    transcoder.inputs.add(in_socket)
    transcoder.outputs.add(out_socket)
    
    return True


def decode_aus(input_dir: str, output_file: str, color_format: int) -> bool:
    """Decode H.265 access units to YUV."""
    # Delete output file if exists
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    first_au_file = build_au_path(input_dir, 0)
    if not os.path.exists(first_au_file):
        print(f"First AU file not found: {first_au_file}")
        return False
    
    with Transcoder() as transcoder:
        transcoder.allow_demo_mode = True
        
        # Configure transcoder using first AU file
        if not configure_transcoder(transcoder, first_au_file, output_file, color_format):
            return False
        
        if not transcoder.open():
            print_error("Transcoder open", transcoder.error)
            return False
        
        # Process all AU files
        i = 0
        while True:
            au_file = build_au_path(input_dir, i)
            if not os.path.exists(au_file):
                break
            
            with open(au_file, 'rb') as f:
                data = f.read()
            
            sample = MediaSample()
            sample.buffer = MediaBuffer(data)
            
            if not transcoder.push(0, sample):
                print_error("Transcoder push", transcoder.error)
                return False
            
            i += 1
        
        if not transcoder.flush():
            print_error("Transcoder flush", transcoder.error)
            return False
        
        transcoder.close()
    
    print(f"Output file: {output_file}")
    return True


# Color format mapping
COLOR_FORMATS = {
    'yuv420': ColorFormat.YUV420,
    'yv12': ColorFormat.YV12,
    'nv12': ColorFormat.NV12,
    'yuv422': ColorFormat.YUV422,
    'bgra32': ColorFormat.BGRA32,
    'bgr24': ColorFormat.BGR24,
}


@click.command()
@click.option('-i', '--input', 'input_dir', 
              help='Input directory containing AU files (au_0000.h265, au_0001.h265, ...)',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='Output YUV file',
              type=click.Path())
@click.option('-c', '--color', 'color_format',
              help='Output color format (yuv420, yv12, nv12, yuv422, bgra32, bgr24)',
              default='yuv420',
              type=click.Choice(list(COLOR_FORMATS.keys()), case_sensitive=False))
def main(input_dir: str, output_file: str, color_format: str):
    """Decode H.265/HEVC access units to YUV."""
    
    # Set default options if not provided
    if not input_dir or not output_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_dir:
            input_dir = os.path.join(script_dir, "../../assets/vid/foreman_qcif.h265.au")
        if not output_file:
            output_file = os.path.join(script_dir, "../../output/dec_hevc_au/foreman_qcif.yuv")
        
        print("Using default options:")
        print(f"  --input {input_dir}")
        print(f"  --output {output_file}")
        print(f"  --color {color_format}")
        print()
    
    # Validate options
    print(f"--input: {input_dir}")
    print(f"--output: {output_file}")
    print(f"--color: {color_format}")
    
    Library.initialize()
    
    # Set license information. Without this AVBlocks runs in Demo mode.
    # Library.set_license("<license-string>")
    
    result = decode_aus(input_dir, output_file, COLOR_FORMATS[color_format.lower()])
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

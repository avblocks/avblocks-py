#!/usr/bin/env python3
"""
Decode VP9/IVF file to YUV.

This sample decodes a VP9/IVF video file to raw YUV format using AVBlocks.
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
    vsi = VideoStreamInfo()
    vsi.stream_type = StreamType.UncompressedVideo
    vsi.color_format = ColorFormat.YUV420
    
    pin = MediaPin()
    pin.stream_info = vsi
    
    socket = MediaSocket()
    socket.file = output_file
    socket.stream_type = StreamType.UncompressedVideo
    socket.pins.add(pin)
    
    return socket


def decode(input_file: str, output_file: str) -> bool:
    """Decode VP9/IVF file to YUV."""
    # Transcoder will fail if output exists (by design)
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with MediaInfo() as media_info:
        media_info.inputs[0].file = input_file
        
        if not media_info.open():
            print_error("MediaInfo open", media_info.error)
            return False
        
        # Create input socket from media info
        in_socket = MediaSocket.from_media_info(media_info)
        media_info.close()
        
        # Create output socket
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
    
    print(f"Output: {output_file}")
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input VP9/IVF file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='Output YUV file',
              type=click.Path())
def main(input_file: str, output_file: str):
    """Decode VP9/IVF file to YUV."""
    
    # Set default options if not provided
    if not input_file or not output_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../../assets/vid/foreman_qcif_vp9.ivf")
        if not output_file:
            output_file = os.path.join(script_dir, "../../output/dec_vp9_file/foreman_qcif.yuv")
        
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

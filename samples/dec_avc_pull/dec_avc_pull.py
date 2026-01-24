#!/usr/bin/env python3
"""
Decode H.264/AVC file to YUV using pull mode.

This sample decodes an H.264/AVC video file to raw YUV frames using the pull mode
(manually pulling decoded frames and writing to output file).
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaSocket, MediaPin,
    VideoStreamInfo, MediaSample, StreamType, 
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


def decode(input_file: str, output_file: str) -> bool:
    """Decode H.264/AVC file to YUV using pull mode."""
    # Delete output file if exists
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create input socket from file
    in_socket = MediaSocket()
    in_socket.file = input_file
    
    # Create output socket with one YUV 4:2:0 video pin
    out_stream_info = VideoStreamInfo()
    out_stream_info.stream_type = StreamType.UncompressedVideo
    out_stream_info.color_format = ColorFormat.YUV420
    out_stream_info.scan_type = ScanType.Progressive
    
    out_pin = MediaPin()
    out_pin.stream_info = out_stream_info
    
    out_socket = MediaSocket()
    out_socket.stream_type = StreamType.UncompressedVideo
    out_socket.pins.add(out_pin)
    
    # Create transcoder
    with Transcoder() as transcoder:
        transcoder.allow_demo_mode = True
        transcoder.inputs.add(in_socket)
        transcoder.outputs.add(out_socket)
        
        if not transcoder.open():
            print_error("Transcoder open", transcoder.error)
            return False
        
        yuv_frame = MediaSample()
        frame_counter = 0
        
        with open(output_file, 'wb') as outfile:
            while True:
                res, _ = transcoder.pull(yuv_frame)
                if res:
                    # Each call to transcoder.pull returns a raw YUV 4:2:0 frame
                    outfile.write(bytes(yuv_frame.buffer.data))
                    frame_counter += 1
                else:
                    break
            
            print_error("Transcoder pull", transcoder.error)
        
        transcoder.close()
        
        print(f"Frames decoded: {frame_counter}")
        print(f"Output file: {output_file}")
    
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input H.264/AVC file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='Output YUV file',
              type=click.Path())
def main(input_file: str, output_file: str):
    """Decode H.264/AVC file to YUV using pull mode."""
    
    # Set default options if not provided
    if not input_file or not output_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../assets/vid/foreman_qcif.h264")
        if not output_file:
            output_file = os.path.join(script_dir, "../output/dec_avc_pull/foreman_qcif.yuv")
        
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

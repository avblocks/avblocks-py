#!/usr/bin/env python3
"""
Demux WebM file.

This sample demuxes a WebM file into separate audio and video WebM files.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaInfo, MediaSocket,
    MediaType, ErrorFacility, PinConnection
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


def generate_output_transcoder(input_file: str, output_base: str) -> Transcoder:
    """Generate transcoder with output filenames based on stream types."""
    media_info = MediaInfo()
    media_info.inputs[0].file = input_file
    
    if not media_info.open():
        print_error("MediaInfo open", media_info.error)
        return None
    
    in_socket = MediaSocket.from_media_info(media_info)
    
    media_info.close()
    
    transcoder = Transcoder()
    transcoder.allow_demo_mode = True
    transcoder.inputs.add(in_socket)
    
    audio = False
    video = False
    
    for pin in in_socket.pins:
        stream_info = pin.stream_info
        
        if stream_info.media_type == MediaType.Audio and not audio:
            audio = True
            filename = output_base + ".aud.webm"
        elif stream_info.media_type == MediaType.Video and not video:
            video = True
            filename = output_base + ".vid.webm"
        else:
            # Disable this pin - we don't need other streams
            pin.connection = PinConnection.Disabled
            continue
        
        out_socket = MediaSocket()
        out_socket.pins.add(pin)
        delete_file(filename)
        out_socket.file = filename
        
        transcoder.outputs.add(out_socket)
        
        print(f"Output file: {filename}")
    
    return transcoder


def demux_webm(input_file: str, output_base: str) -> bool:
    """Demux WebM file into separate audio and video files."""
    # Create output directory if needed
    output_dir = os.path.dirname(output_base)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    transcoder = generate_output_transcoder(input_file, output_base)
    
    if transcoder is None:
        return False
    
    with transcoder:
        if not transcoder.open():
            print_error("Transcoder open", transcoder.error)
            return False
        
        if not transcoder.run():
            print_error("Transcoder run", transcoder.error)
            return False
        
        transcoder.close()
    
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input WebM file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_base',
              help='Output file base name (without extension)',
              type=click.Path())
def main(input_file: str, output_base: str):
    """Demux WebM file into separate audio and video files."""
    
    # Set default options if not provided
    if not input_file or not output_base:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../../assets/mov/big-buck-bunny_trailer_vp8_vorbis.webm")
        if not output_base:
            output_base = os.path.join(script_dir, "../../output/demux_webm_file/big-buck-bunny_trailer_vp8_vorbis")
        
        print("Using default options:")
        print(f"  --input {input_file}")
        print(f"  --output {output_base}")
        print()
    
    # Validate options
    print(f"Input file: {input_file}")
    print(f"Output file: {output_base}")
    
    Library.initialize()
    
    # Set license information. Without this AVBlocks runs in Demo mode.
    # Library.set_license("<license-string>")
    
    result = demux_webm(input_file, output_base)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

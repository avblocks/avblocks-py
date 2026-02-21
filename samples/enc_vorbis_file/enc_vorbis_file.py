#!/usr/bin/env python3
"""
Encode WAV file to Vorbis/OGG.

This sample encodes a WAV audio file to Vorbis format in an OGG container using AVBlocks.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaSocket, MediaPin,
    AudioStreamInfo, StreamType, ErrorFacility
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
    """Create output socket for Vorbis/OGG file."""
    # create stream info to describe the output audio stream
    asi = AudioStreamInfo()
    asi.stream_type = StreamType.Vorbis

    # The default bitrate is 128000. You can set it to 192000, 256000, etc.
    # asi.bitrate = 192000

    # Optionally set the sampling rate and the number of the channels, e.g. 44.1 Khz, Mono 
    # asi.sample_rate = 44100
    # asi.channels = 1

    # create a pin using the stream info 
    pin = MediaPin()
    pin.stream_info = asi

    # finally create a socket for the output container format which is OGG in this case
    socket = MediaSocket()
    socket.stream_type = StreamType.OGG
    socket.pins.add(pin)
    socket.file = output_file

    return socket


def encode(input_file: str, output_file: str) -> bool:
    """Encode WAV file to Vorbis/OGG."""
    # Transcoder will fail if output exists (by design)
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create input socket
    in_socket = MediaSocket()
    in_socket.file = input_file
    
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


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input WAV file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='Output OGG file',
              type=click.Path())
def main(input_file: str, output_file: str):
    """Encode WAV file to Vorbis/OGG."""
    
    # Set default options if not provided
    if not input_file or not output_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../../assets/aud/equinox-48KHz.wav")
        if not output_file:
            output_file = os.path.join(script_dir, "../../output/enc_vorbis_file/equinox-48KHz.ogg")
        
        print("Using default options:")
        print(f"  --input {input_file}")
        print(f"  --output {output_file}")
        print()
    
    # Validate options
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    
    Library.initialize()
    
    # Set license information. Without this AVBlocks runs in Demo mode.
    # Library.set_license("<license-string>")
    
    result = encode(input_file, output_file)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

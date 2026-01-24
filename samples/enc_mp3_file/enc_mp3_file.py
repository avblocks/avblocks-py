#!/usr/bin/env python3
"""
Encode WAV file to MP3.

This sample encodes a WAV audio file to MP3 format using AVBlocks.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaSocket, MediaPin,
    AudioStreamInfo, StreamType, StreamSubType, ErrorFacility
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
    """Create output socket for MP3 file."""
    socket = MediaSocket()
    socket.file = output_file
    socket.stream_type = StreamType.MPEG_Audio
    socket.stream_sub_type = StreamSubType.MPEG_Audio_Layer3
    
    pin = MediaPin()
    socket.pins.add(pin)
    
    asi = AudioStreamInfo()
    pin.stream_info = asi
    
    asi.stream_type = StreamType.MPEG_Audio
    asi.stream_sub_type = StreamSubType.MPEG_Audio_Layer3
    
    # The default bitrate is 128000. You can set it to 192000, 256000, etc.
    # asi.bitrate = 192000
    
    # You can change the number of channels
    # asi.channels = 1
    # or the sampling rate
    # asi.sample_rate = 44100
    
    return socket


def encode(input_file: str, output_file: str) -> bool:
    """Encode WAV file to MP3."""
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
              help='Output MP3 file',
              type=click.Path())
def main(input_file: str, output_file: str):
    """Encode WAV file to MP3."""
    
    # Set default options if not provided
    if not input_file or not output_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../assets/aud/Hydrate-Kenny_Beltrey.wav")
        if not output_file:
            output_file = os.path.join(script_dir, "../output/enc_mp3_file/Hydrate-Kenny_Beltrey.mp3")
        
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
    
    result = encode(input_file, output_file)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

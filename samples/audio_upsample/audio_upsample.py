#!/usr/bin/env python3
"""
Upsample audio from 44.1 KHz to 48 KHz.

This sample upsamples an audio file from 44.1 KHz to 48 KHz using AVBlocks.
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
    """Create output socket for upscaled audio."""
    socket = MediaSocket()
    socket.file = output_file
    socket.stream_type = StreamType.MPEG_Audio
    socket.stream_sub_type = StreamSubType.MPEG_Audio_Layer3
    
    # Create stream info to describe the output audio stream
    asi = AudioStreamInfo()
    asi.stream_type = StreamType.MPEG_Audio
    asi.stream_sub_type = StreamSubType.MPEG_Audio_Layer3
    
    # Set the output sampling rate to 48 KHz (48000 Hz)
    # This will trigger resampling from the input sample rate (e.g., 44.1 KHz)
    asi.sample_rate = 48000
    
    # Optionally set the bitrate (default is 128000)
    # asi.bitrate = 192000
    
    # Optionally set the number of channels
    # asi.channels = 1  # Mono
    
    # Create a pin using the stream info
    pin = MediaPin()
    pin.stream_info = asi
    
    # The pin allows you to specify additional parameters for the encoder
    # for example, change the stereo mode, e.g. Joint Stereo
    # pin.params.add(Param.Encoder.Audio.MPEG1.StereoMode, StereoMode.Joint)
    
    # Finally create a socket for the output container format which is MP3 in this case
    socket.stream_type = StreamType.MPEG_Audio
    socket.stream_sub_type = StreamSubType.MPEG_Audio_Layer3
    
    socket.pins.add(pin)
    
    return socket


def upsample(input_file: str, output_file: str) -> bool:
    """Upsample audio file from 44.1 KHz to 48 KHz."""
    # Transcoder will fail if output exists (by design)
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Initialize the library
    Library.initialize()
    
    try:
        # Create input socket
        in_socket = MediaSocket()
        in_socket.file = input_file
        
        # Create output socket with 48 KHz sample rate
        out_socket = create_output_socket(output_file)
        
        # Create transcoder
        transcoder = Transcoder()
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
    
    finally:
        # Shutdown the library
        Library.shutdown()
    
    return True


@click.command()
@click.option('-i', '--input', 'input_file', required=True, help='Input MP3 file.')
@click.option('-o', '--output', 'output_file', required=True, help='Output MP3 file.')
def main(input_file: str, output_file: str):
    """Upsample audio file from 44.1 KHz to 48 KHz.
    
    Examples:
        \b
        ./audio-upsample --input input.mp3 --output output.mp3
        \b
        ./audio-upsample -i input.mp3 -o output.mp3
    """
    if not upsample(input_file, output_file):
        sys.exit(1)


if __name__ == '__main__':
    main()

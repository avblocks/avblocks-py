#!/usr/bin/env python3
"""
Re-encode a media file.

This sample demonstrates how to force re-encoding of audio and/or video
streams even when the input and output formats match.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaInfo, MediaSocket, MediaPin, MediaType,
    Param, Use, ErrorFacility
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


def re_encode(input_file: str, output_file: str, force_audio: bool, force_video: bool) -> bool:
    """Re-encode a media file."""
    # Delete output file if it exists
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    transcoder = Transcoder()
    
    # In order to use the production release for testing (without a valid license),
    # the transcoder demo mode must be enabled.
    transcoder.allow_demo_mode = True
    
    # Get input format using MediaInfo
    media_info = MediaInfo()
    media_info.inputs[0].file = input_file
    
    if not media_info.open():
        print_error("Open MediaInfo", media_info.error)
        return False
    
    # Add Inputs
    input_socket = MediaSocket.from_media_info(media_info)
    transcoder.inputs.add(input_socket)
    
    media_info.close()
    
    # Add Outputs
    # Create output socket
    output_socket = MediaSocket()
    in_socket = transcoder.inputs[0]
    
    output_socket.stream_type = in_socket.stream_type
    output_socket.file = output_file
    
    # Add pins with ReEncode parameter set to Use.On
    for in_pin in in_socket.pins:
        si = in_pin.stream_info.clone()
        pin = MediaPin()
        pin.stream_info = si.clone()
        
        if si.media_type == MediaType.Video and force_video:
            pin.params[Param.ReEncode] = Use.On
        
        if si.media_type == MediaType.Audio and force_audio:
            pin.params[Param.ReEncode] = Use.On
        
        output_socket.pins.add(pin)
    
    transcoder.outputs.add(output_socket)
    
    # Open transcoder
    result = transcoder.open()
    print_error("Open Transcoder", transcoder.error)
    if not result:
        return False
    
    # Run transcoder
    result = transcoder.run()
    print_error("Run Transcoder", transcoder.error)
    if not result:
        return False
    
    transcoder.close()
    
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='input file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='output file',
              type=click.Path())
@click.option('-a', '--audio', 'force_audio', is_flag=True, default=False,
              help='Force audio re-encoding.')
@click.option('-v', '--video', 'force_video', is_flag=True, default=False,
              help='Force video re-encoding.')
def main(input_file: str, output_file: str, force_audio: bool, force_video: bool):
    """Re-encode a media file with optional forced re-encoding of audio and/or video."""
    
    # Set default options if not provided
    if not input_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        input_file = os.path.join(script_dir, "../../assets/mov/big_buck_bunny_trailer.mp4")
        output_file = os.path.join(script_dir, "../../output/re_encode/big_buck_bunny_trailer.mp4")
        
        print("Using default options: ")
        print(f"re-encode --input {input_file} --output {output_file}", end="")
        if force_audio:
            print(" --audio", end="")
        if force_video:
            print(" --video", end="")
        print()
    
    # Validate options
    error = False
    
    print("Input file: ", end="")
    if not input_file:
        print("[not set]")
        error = True
    else:
        print(input_file)
    
    print("Output file: ", end="")
    if not output_file:
        print("[not set]")
        error = True
    else:
        print(output_file)
    
    print(f"Re-encode audio forced: {'yes' if force_audio else 'no'}")
    print(f"Re-encode video forced: {'yes' if force_video else 'no'}")
    
    if error:
        click.echo("\nUse --help for usage information.")
        sys.exit(1)
    
    Library.initialize()
    
    # Set license information. To run AVBlocks in demo mode, comment the next line out
    # Library.set_license("<license-string>")
    
    result = re_encode(input_file, output_file, force_audio, force_video)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

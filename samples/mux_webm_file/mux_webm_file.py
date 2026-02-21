#!/usr/bin/env python3
"""
Mux audio and video streams from WebM files into a single WebM container.

This sample shows how to combine separate Vorbis audio and VP8 video streams
from WebM files into a single WebM file.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaSocket, MediaPin,
    AudioStreamInfo, VideoStreamInfo,
    StreamType, ErrorFacility
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


def webm_mux(audio_files: tuple, video_files: tuple, output_file: str) -> bool:
    """Mux audio and video files into WebM."""
    # Delete output file if it exists
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    transcoder = Transcoder()
    
    # Transcoder demo mode must be enabled,
    # in order to use the production release for testing (without a valid license)
    transcoder.allow_demo_mode = True
    
    # Create output socket
    output_socket = MediaSocket()
    output_socket.file = output_file
    output_socket.stream_type = StreamType.WebM
    
    # audio
    for audio_file in audio_files:
        output_pin = MediaPin()
        asi = AudioStreamInfo()
        asi.stream_type = StreamType.Vorbis
        output_pin.stream_info = asi
        
        output_socket.pins.add(output_pin)
        
        input_socket = MediaSocket()
        input_socket.file = audio_file
        input_socket.stream_type = StreamType.WebM
        transcoder.inputs.add(input_socket)
        
        print(f"Muxing audio input: {audio_file}")
    
    # video
    for video_file in video_files:
        output_pin = MediaPin()
        vsi = VideoStreamInfo()
        vsi.stream_type = StreamType.VP8
        output_pin.stream_info = vsi
        
        output_socket.pins.add(output_pin)
        
        input_socket = MediaSocket()
        input_socket.file = video_file
        input_socket.stream_type = StreamType.WebM
        transcoder.inputs.add(input_socket)
        
        print(f"Muxing video input: {video_file}")
    
    transcoder.outputs.add(output_socket)
    
    # Open transcoder
    if not transcoder.open():
        print_error("Open Transcoder", transcoder.error)
        return False
    
    # Run transcoder
    if not transcoder.run():
        print_error("Run Transcoder", transcoder.error)
        return False
    
    transcoder.close()
    
    print(f"Output file: {output_file}")
    
    return True


@click.command()
@click.option('-a', '--audio', 'audio_files', multiple=True,
              help='Input Vorbis/WebM files. Could be a list of files.',
              type=click.Path(exists=True))
@click.option('-v', '--video', 'video_files', multiple=True,
              help='Input VP8/WebM files. Could be a list of files.',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='Output WebM file',
              type=click.Path())
def main(audio_files: tuple, video_files: tuple, output_file: str):
    """Mux audio and video streams from WebM files into a single WebM container."""
    
    # Set default options if not provided
    if not audio_files and not video_files:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        video_file = os.path.join(script_dir, "../../assets/vid/big-buck-bunny_trailer_vp8_vorbis.vid.webm")
        audio_file = os.path.join(script_dir, "../../assets/aud/big-buck-bunny_trailer_vp8_vorbis.aud.webm")
        output_file = os.path.join(script_dir, "../../output/mux_webm_file/big-buck-bunny_trailer.webm")
        
        audio_files = (audio_file,)
        video_files = (video_file,)
        
        print("Using default options: ")
        print(f"mux_webm_file --audio {audio_file} --video {video_file} --output {output_file}")
        print()
    
    # Validate options
    error = False
    
    print("Audio files: ")
    if audio_files:
        for f in audio_files:
            print(f"   {f}")
    else:
        print("[not set]")
        error = True
    
    print("Video files: ")
    if video_files:
        for f in video_files:
            print(f"   {f}")
    else:
        print("[not set]")
        error = True
    
    print("Output file: ", end="")
    if not output_file:
        print("[not set]")
        error = True
    else:
        print(output_file)
    
    if error:
        click.echo("\nUse --help for usage information.")
        sys.exit(1)
    
    Library.initialize()
    
    # Set license information. To run AVBlocks in demo mode, comment the next line out
    # Library.set_license("<license-string>")
    
    result = webm_mux(audio_files, video_files, output_file)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

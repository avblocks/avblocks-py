#!/usr/bin/env python3
"""
Upsample an MP3 audio clip from 44.1 KHz to 48 KHz.

This sample demonstrates the basic AVBlocks audio upsampling workflow with
hardcoded input and output file paths (no command line parsing).
"""

import os
import sys

from avblocks import (
    Library, MediaInfo, MediaSocket, Transcoder,
    AudioStreamInfo, ErrorFacility
)


def print_error(action: str, error) -> None:
    """Print error information."""
    if action:
        print(f"{action}: ", end="")

    if error.facility == ErrorFacility.Success:
        print("Success")
        return

    print(f"{error.message or ''}, facility:{error.facility} code:{error.code} hint:{error.hint or ''}")


def upsample(input_path: str, output_path: str) -> bool:
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Delete output file if it exists (transcoder will fail otherwise)
    if os.path.exists(output_path):
        os.remove(output_path)

    # Create MediaInfo to probe the input file
    with MediaInfo() as media_info:
        media_info.inputs[0].file = input_path

        if not media_info.open():
            print_error("Open MediaInfo", media_info.error)
            return False

        # Create input socket from probed media info
        input_socket = MediaSocket.from_media_info(media_info)

        # Clone the input socket to start with identical output configuration
        output_socket = input_socket.clone()
        output_socket.file = output_path

        # Get the output audio pin and set sample rate to 48 KHz
        if len(output_socket.pins) > 0:
            out_audio_pin = output_socket.pins[0]
            out_audio_stream = out_audio_pin.stream_info
            if isinstance(out_audio_stream, AudioStreamInfo):
                out_audio_stream.sample_rate = 48000

        # Create Transcoder and configure it
        with Transcoder() as transcoder:
            transcoder.allow_demo_mode = True
            transcoder.inputs.add(input_socket)
            transcoder.outputs.add(output_socket)

            if not transcoder.open():
                print_error("Transcoder open", transcoder.error)
                return False

            if not transcoder.run():
                print_error("Transcoder run", transcoder.error)
                transcoder.close()
                return False

            transcoder.close()

    return True


def main():
    # Hardcoded input and output file paths (no command line parsing)
    # Paths are relative to the working directory from which the sample is run
    input_path = "kahvi011_kennybeltrey-hydrate.mp3"
    output_path = "kahvi011_kennybeltrey-hydrate_48Khz.mp3"

    Library.initialize()

    # Set license information. To run AVBlocks in demo mode, comment the next line out
    # Library.set_license("<license-string>")

    result = upsample(input_path, output_path)

    Library.shutdown()

    return 0 if result else 1


if __name__ == '__main__':
    sys.exit(main())

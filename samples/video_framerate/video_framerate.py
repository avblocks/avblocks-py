#!/usr/bin/env python3
"""
Change the frame rate of a video.

This sample demonstrates how to use AVBlocks to change the frame rate
of a video file.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaInfo, MediaSocket,
    VideoStreamInfo, MediaType, ErrorFacility
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


def change_video_framerate(
    input_file: str,
    output_file: str,
    frame_rate: float
) -> bool:
    """Change the frame rate of a video file.

    Args:
        input_file: Path to the input MP4 file.
        output_file: Path to the output MP4 file.
        frame_rate: Target frame rate in frames per second.

    Returns:
        True on success, False on error.
    """
    # Delete output file if it exists
    delete_file(output_file)

    # Create output directory if needed
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open input file with MediaInfo
    media_info = MediaInfo()
    media_info.inputs[0].file = input_file

    if not media_info.open():
        print_error("Open MediaInfo", media_info.error)
        return False

    # Create input socket
    input_socket = MediaSocket.from_media_info(media_info)

    # Create output socket (same layout as input, to be modified below)
    output_socket = MediaSocket.from_media_info(media_info)
    output_socket.file = output_file

    media_info.close()

    # Find the output video pin and update the frame rate
    for pin in output_socket.pins:
        if pin.stream_info.media_type != MediaType.Video:
            continue

        vsi = pin.stream_info
        if not isinstance(vsi, VideoStreamInfo):
            continue

        vsi.frame_rate = frame_rate
        break

    # Create and run the transcoder
    transcoder = Transcoder()
    transcoder.allow_demo_mode = True
    transcoder.inputs.add(input_socket)
    transcoder.outputs.add(output_socket)

    result = transcoder.open()
    print_error("Open Transcoder", transcoder.error)
    if not result:
        return False

    result = transcoder.run()
    print_error("Run Transcoder", transcoder.error)
    if not result:
        transcoder.close()
        return False

    transcoder.close()

    print(f"Output: {output_file}")
    return True


@click.command()
@click.option('-i', '--input', 'input_file',
              help='MP4 input file.',
              type=click.Path())
@click.option('-o', '--output', 'output_file',
              help='MP4 output file.',
              type=click.Path())
@click.option('-f', '--frame-rate', default=30.0,
              help='Target frame rate (fps). (default: 30.0)',
              type=float)
def main(
    input_file: str,
    output_file: str,
    frame_rate: float
):
    """Change the frame rate of a video."""
    # Set default options if not provided
    if not input_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, '../../assets/vid/big_buck_bunny_trailer.vid.mp4')
        output_file = os.path.join(script_dir, '../../output/video_framerate/big_buck_bunny_30fps.mp4')

        print('Using defaults:')
        print(
            f'video-framerate --input {input_file} --output {output_file}'
            f' --frame-rate {frame_rate}'
        )

    error = False

    print(f'Input file:   {input_file or "[not set]"}')
    if not input_file:
        error = True

    print(f'Output file:  {output_file or "[not set]"}')
    if not output_file:
        error = True

    print(f'Frame rate:   {frame_rate}')

    if frame_rate <= 0.0:
        print('Error: Frame rate must be positive.')
        error = True

    if error:
        click.echo('\nUse --help for usage information.')
        sys.exit(1)

    Library.initialize()

    # Set license information. To run AVBlocks in demo mode, comment the next line out.
    # Library.set_license("<license-string>")

    result = change_video_framerate(input_file, output_file, frame_rate)

    Library.shutdown()

    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

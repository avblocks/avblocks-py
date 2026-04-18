#!/usr/bin/env python3
"""
Upscale a video to Full HD (1920x1080) using bicubic interpolation.

This sample demonstrates how to use AVBlocks to upscale a video file to a
larger resolution using the bicubic interpolation method.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaInfo, MediaSocket,
    VideoStreamInfo, MediaType, Param, InterpolationMethod, ErrorFacility
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


def upscale_video(
    input_file: str,
    output_file: str,
    width: int,
    height: int
) -> bool:
    """Upscale a video file to the specified dimensions.

    Args:
        input_file: Path to the input MP4 file.
        output_file: Path to the output MP4 file.
        width: Target frame width in pixels.
        height: Target frame height in pixels.

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

    # Find the output video pin and update frame size + interpolation method
    for pin in output_socket.pins:
        if pin.stream_info.media_type != MediaType.Video:
            continue

        vsi = pin.stream_info
        if not isinstance(vsi, VideoStreamInfo):
            continue

        vsi.frame_width = width
        vsi.frame_height = height

        # Cubic is best for upscaling (highest quality)
        pin.params[Param.Video.Resize.InterpolationMethod] = int(InterpolationMethod.Cubic)

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
@click.option('-w', '--width', default=1920,
              help='Target width (pixels). (default: 1920)',
              type=int)
@click.option('-h', '--height', default=1080,
              help='Target height (pixels). (default: 1080)',
              type=int)
def main(
    input_file: str,
    output_file: str,
    width: int,
    height: int
):
    """Upscale a video to Full HD (1920x1080) using bicubic interpolation."""
    # Set default options if not provided
    if not input_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, '../../assets/vid/big_buck_bunny_trailer.vid.mp4')
        output_file = os.path.join(script_dir, '../../output/video_upscale/big_buck_bunny_1080p.mp4')

        print('Using defaults:')
        print(
            f'video-upscale --input {input_file} --output {output_file}'
            f' --width {width} --height {height}'
        )

    error = False

    print(f'Input file:   {input_file or "[not set]"}')
    if not input_file:
        error = True

    print(f'Output file:  {output_file or "[not set]"}')
    if not output_file:
        error = True

    print(f'Width:        {width}')
    print(f'Height:       {height}')

    if error:
        click.echo('\nUse --help for usage information.')
        sys.exit(1)

    Library.initialize()

    # Set license information. To run AVBlocks in demo mode, comment the next line out.
    # Library.set_license("<license-string>")

    result = upscale_video(input_file, output_file, width, height)

    Library.shutdown()

    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

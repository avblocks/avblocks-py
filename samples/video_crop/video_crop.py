#!/usr/bin/env python3
"""
Crop a video by removing pixels from the edges.

This sample demonstrates how to use AVBlocks to crop a video file by removing
a specified number of pixels from each edge of the frame.
"""

import math
import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaInfo, MediaSocket,
    VideoStreamInfo, MediaType, Param, ErrorFacility
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


def crop_video(
    input_file: str,
    output_file: str,
    crop_left: int,
    crop_right: int,
    crop_top: int,
    crop_bottom: int
) -> bool:
    """Crop a video file by removing pixels from the specified edges.

    Args:
        input_file: Path to the input MP4 file.
        output_file: Path to the output MP4 file.
        crop_left: Pixels to remove from the left edge.
        crop_right: Pixels to remove from the right edge.
        crop_top: Pixels to remove from the top edge.
        crop_bottom: Pixels to remove from the bottom edge.

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

    # Find the output video pin and update frame size + display ratio
    for pin in output_socket.pins:
        if pin.stream_info.media_type != MediaType.Video:
            continue

        vsi = pin.stream_info
        if not isinstance(vsi, VideoStreamInfo):
            continue

        new_width = vsi.frame_width - crop_left - crop_right
        new_height = vsi.frame_height - crop_top - crop_bottom

        # Update output frame dimensions to reflect the crop
        vsi.frame_width = new_width
        vsi.frame_height = new_height

        # Update display ratio to match the new frame dimensions
        g = math.gcd(new_width, new_height)
        vsi.display_ratio_width = new_width // g
        vsi.display_ratio_height = new_height // g

        # Set crop parameters on this pin
        pin.params.add(Param.Video.Crop.Left, crop_left)
        pin.params.add(Param.Video.Crop.Right, crop_right)
        pin.params.add(Param.Video.Crop.Top, crop_top)
        pin.params.add(Param.Video.Crop.Bottom, crop_bottom)

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
@click.option('--crop-left', default=60,
              help='Pixels to crop from left. (default: 60)',
              type=int)
@click.option('--crop-right', default=60,
              help='Pixels to crop from right. (default: 60)',
              type=int)
@click.option('--crop-top', default=0,
              help='Pixels to crop from top. (default: 0)',
              type=int)
@click.option('--crop-bottom', default=0,
              help='Pixels to crop from bottom. (default: 0)',
              type=int)
def main(
    input_file: str,
    output_file: str,
    crop_left: int,
    crop_right: int,
    crop_top: int,
    crop_bottom: int
):
    """Crop a video by removing pixels from the edges."""
    # Set default options if not provided
    if not input_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, '../../assets/vid/big_buck_bunny_trailer.vid.mp4')
        output_file = os.path.join(script_dir, '../../output/video_crop/cropped.mp4')

        print('Using defaults:')
        print(
            f'video-crop --input {input_file} --output {output_file}'
            f' --crop-left {crop_left} --crop-right {crop_right}'
            f' --crop-top {crop_top} --crop-bottom {crop_bottom}'
        )

    error = False

    print(f'Input file:   {input_file or "[not set]"}')
    if not input_file:
        error = True

    print(f'Output file:  {output_file or "[not set]"}')
    if not output_file:
        error = True

    print(f'Crop left:    {crop_left}')
    print(f'Crop right:   {crop_right}')
    print(f'Crop top:     {crop_top}')
    print(f'Crop bottom:  {crop_bottom}')

    if error:
        click.echo('\nUse --help for usage information.')
        sys.exit(1)

    Library.initialize()

    # Set license information. To run AVBlocks in demo mode, comment the next line out.
    # Library.set_license("<license-string>")

    result = crop_video(input_file, output_file, crop_left, crop_right, crop_top, crop_bottom)

    Library.shutdown()

    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

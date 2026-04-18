#!/usr/bin/env python3
"""
Add black border padding around a video.

This sample demonstrates how to use AVBlocks to add padding around a video
by specifying the number of pixels to add on each edge of the frame.
"""

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


def pad_video(
    input_file: str,
    output_file: str,
    width: int,
    height: int,
    pad_left: int,
    pad_right: int,
    pad_top: int,
    pad_bottom: int,
    pad_color: int
) -> bool:
    """Add padding around a video file.

    Args:
        input_file: Path to the input MP4 file.
        output_file: Path to the output MP4 file.
        width: Target output frame width in pixels (0 = auto).
        height: Target output frame height in pixels (0 = auto).
        pad_left: Pixels to add on the left edge.
        pad_right: Pixels to add on the right edge.
        pad_top: Pixels to add on the top edge.
        pad_bottom: Pixels to add on the bottom edge.
        pad_color: Padding color in ARGB32 format.

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

    # Find the output video pin and update frame size + padding parameters
    for pin in output_socket.pins:
        if pin.stream_info.media_type != MediaType.Video:
            continue

        vsi = pin.stream_info
        if not isinstance(vsi, VideoStreamInfo):
            continue

        # Compute output dimensions if not specified
        out_width = width if width > 0 else vsi.frame_width + pad_left + pad_right
        out_height = height if height > 0 else vsi.frame_height + pad_top + pad_bottom

        vsi.frame_width = out_width
        vsi.frame_height = out_height

        # Set padding parameters
        pin.params[Param.Video.Pad.Left] = pad_left
        pin.params[Param.Video.Pad.Right] = pad_right
        pin.params[Param.Video.Pad.Top] = pad_top
        pin.params[Param.Video.Pad.Bottom] = pad_bottom
        pin.params[Param.Video.Pad.Color] = pad_color

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
@click.option('-w', '--width', default=0,
              help='Target width (pixels). 0 = input width + left + right. (default: 0)',
              type=int)
@click.option('-h', '--height', default=0,
              help='Target height (pixels). 0 = input height + top + bottom. (default: 0)',
              type=int)
@click.option('-l', '--left', 'pad_left', default=100,
              help='Left padding (pixels). (default: 100)',
              type=int)
@click.option('-r', '--right', 'pad_right', default=100,
              help='Right padding (pixels). (default: 100)',
              type=int)
@click.option('-t', '--top', 'pad_top', default=100,
              help='Top padding (pixels). (default: 100)',
              type=int)
@click.option('-b', '--bottom', 'pad_bottom', default=100,
              help='Bottom padding (pixels). (default: 100)',
              type=int)
@click.option('-c', '--color', 'pad_color', default=0xFF000000,
              help='Padding color (ARGB32). (default: 0xFF000000)',
              type=int)
def main(
    input_file: str,
    output_file: str,
    width: int,
    height: int,
    pad_left: int,
    pad_right: int,
    pad_top: int,
    pad_bottom: int,
    pad_color: int
):
    """Add black border padding around a video."""
    # Set default options if not provided
    if not input_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, '../../assets/vid/big_buck_bunny_trailer.vid.mp4')
        output_file = os.path.join(script_dir, '../../output/video_pad/big_buck_bunny_padded.mp4')

        print('Using defaults:')
        print(
            f'video-pad --input {input_file} --output {output_file}'
            f' --left {pad_left} --right {pad_right}'
            f' --top {pad_top} --bottom {pad_bottom}'
            f' --color {pad_color}'
        )

    error = False

    print(f'Input file:   {input_file or "[not set]"}')
    if not input_file:
        error = True

    print(f'Output file:  {output_file or "[not set]"}')
    if not output_file:
        error = True

    print(f'Width:        {width} (0 = auto)')
    print(f'Height:       {height} (0 = auto)')
    print(f'Pad left:     {pad_left}')
    print(f'Pad right:    {pad_right}')
    print(f'Pad top:      {pad_top}')
    print(f'Pad bottom:   {pad_bottom}')
    print(f'Pad color:    0x{pad_color:08X}')

    if error:
        click.echo('\nUse --help for usage information.')
        sys.exit(1)

    Library.initialize()

    # Set license information. To run AVBlocks in demo mode, comment the next line out.
    # Library.set_license("<license-string>")

    result = pad_video(
        input_file, output_file,
        width, height,
        pad_left, pad_right, pad_top, pad_bottom,
        pad_color
    )

    Library.shutdown()

    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

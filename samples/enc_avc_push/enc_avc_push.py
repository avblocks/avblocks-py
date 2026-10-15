#!/usr/bin/env python3
"""
Encode YUV file to H.264/AVC using push mode.

This sample encodes a raw YUV video file to H.264/AVC format using the push mode.
It first reads the YUV file with a "reader" transcoder and pulls the raw frames,
then pushes those frames to an "encoder" transcoder.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaSocket, MediaPin, MediaSample,
    VideoStreamInfo, StreamType, StreamSubType,
    ColorFormat, ScanType, ErrorFacility, CodecError
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


# Color format descriptors
COLOR_FORMATS = [
    (ColorFormat.YV12, "yv12", "Planar Y, V, U (4:2:0) (note V,U order!)"),
    (ColorFormat.NV12, "nv12", "Planar Y, merged U->V (4:2:0)"),
    (ColorFormat.YUY2, "yuy2", "Composite Y->U->Y->V (4:2:2)"),
    (ColorFormat.UYVY, "uyvy", "Composite U->Y->V->Y (4:2:2)"),
    (ColorFormat.YUV411, "yuv411", "Planar Y, U, V (4:1:1)"),
    (ColorFormat.YUV420, "yuv420", "Planar Y, U, V (4:2:0)"),
    (ColorFormat.YUV422, "yuv422", "Planar Y, U, V (4:2:2)"),
    (ColorFormat.YUV444, "yuv444", "Planar Y, U, V (4:4:4)"),
    (ColorFormat.Y411, "y411", "Composite Y, U, V (4:1:1)"),
    (ColorFormat.Y41P, "y41p", "Composite Y, U, V (4:1:1)"),
    (ColorFormat.BGR32, "bgr32", "Composite B->G->R"),
    (ColorFormat.BGRA32, "bgra32", "Composite B->G->R->A"),
    (ColorFormat.BGR24, "bgr24", "Composite B->G->R"),
    (ColorFormat.BGR565, "bgr565", "Composite B->G->R, 5 bit per B & R, 6 bit per G"),
    (ColorFormat.BGR555, "bgr555", "Composite B->G->R->A, 5 bit per component, 1 bit per A"),
    (ColorFormat.BGR444, "bgr444", "Composite B->G->R->A, 4 bit per component"),
    (ColorFormat.GRAY, "gray", "Luminance component only"),
    (ColorFormat.YUV420A, "yuv420a", "Planar Y, U, V, Alpha (4:2:0)"),
    (ColorFormat.YUV422A, "yuv422a", "Planar Y, U, V, Alpha (4:2:2)"),
    (ColorFormat.YUV444A, "yuv444a", "Planar Y, U, V, Alpha (4:4:4)"),
    (ColorFormat.YVU9, "yvu9", "Planar Y, V, U, 9 bits per sample"),
]


def get_color_by_name(name: str):
    """Get color format ID by name, or None if not found."""
    for color_id, color_name, _ in COLOR_FORMATS:
        if color_name.lower() == name.lower():
            return color_id
    return None


def print_colors():
    """Print supported color formats."""
    print("\nCOLORS")
    print("---------")
    for _, name, desc in COLOR_FORMATS:
        print(f"{name:<20} {desc}")
    print()


def create_yuv_video_info(width: int, height: int, fps: float,
                          color_format: int) -> VideoStreamInfo:
    """Create stream info for raw YUV video."""
    vsi = VideoStreamInfo()
    vsi.stream_type = StreamType.UncompressedVideo
    vsi.frame_rate = fps
    vsi.frame_width = width
    vsi.frame_height = height
    vsi.color_format = color_format
    vsi.scan_type = ScanType.Progressive
    return vsi


def create_yuv_reader_socket(input_file: str, width: int, height: int,
                             fps: float, color_format: int) -> MediaSocket:
    """Create the YUV reader input socket (reads the YUV file)."""
    socket = MediaSocket()
    socket.stream_type = StreamType.UncompressedVideo
    socket.file = input_file

    pin = MediaPin()
    pin.stream_info = create_yuv_video_info(width, height, fps, color_format)
    socket.pins.add(pin)

    return socket


def create_h264_encoder_input_socket(width: int, height: int, fps: float,
                                     color_format: int) -> MediaSocket:
    """Create the H.264 encoder input socket (no file, frames are pushed)."""
    socket = MediaSocket()
    socket.stream_type = StreamType.UncompressedVideo

    pin = MediaPin()
    pin.stream_info = create_yuv_video_info(width, height, fps, color_format)
    socket.pins.add(pin)

    return socket


def create_h264_encoder_output_socket(output_file: str, width: int, height: int,
                                      fps: float, color_format: int) -> MediaSocket:
    """Create the H.264 encoder output socket (writes the H.264 file)."""
    socket = MediaSocket()
    socket.file = output_file
    socket.stream_type = StreamType.H264
    socket.stream_sub_type = StreamSubType.AVC_Annex_B

    vsi = VideoStreamInfo()
    vsi.stream_type = StreamType.H264
    vsi.stream_sub_type = StreamSubType.AVC_Annex_B
    vsi.frame_rate = fps
    vsi.frame_width = width
    vsi.frame_height = height
    vsi.color_format = color_format
    vsi.scan_type = ScanType.Progressive

    pin = MediaPin()
    pin.stream_info = vsi
    socket.pins.add(pin)

    return socket


def encode_h264_stream(yuv_reader: Transcoder, h264_encoder: Transcoder) -> bool:
    """Pull raw YUV frames from the reader and push them to the encoder."""
    yuv_frame = MediaSample()

    while True:
        res, _ = yuv_reader.pull(yuv_frame)
        if not res:
            break

        if not h264_encoder.push(0, yuv_frame):
            print_error("H264 encoder push", h264_encoder.error)
            return False

    # Check for EOS from the YUV reader
    error = yuv_reader.error
    if error.facility != ErrorFacility.Codec or error.code != CodecError.EOS:
        print_error("YUV reader pull", error)
        return False

    # Flush the encoder to finalize the output
    if not h264_encoder.flush():
        print_error("H264 encoder flush", h264_encoder.error)
        return False

    return True


def encode(input_file: str, output_file: str, width: int, height: int,
           fps: float, color_format: int) -> bool:
    """Encode YUV file to H.264/AVC using push mode."""
    # Transcoder will fail if output exists (by design)
    delete_file(output_file)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create YUV reader transcoder (reads from file, frames are pulled)
    yuv_in_socket = create_yuv_reader_socket(input_file, width, height, fps, color_format)

    yuv_out_socket = MediaSocket()
    yuv_out_socket.stream_type = StreamType.UncompressedVideo
    yuv_out_pin = MediaPin()
    yuv_out_pin.stream_info = create_yuv_video_info(width, height, fps, color_format)
    yuv_out_socket.pins.add(yuv_out_pin)

    with Transcoder() as yuv_reader:
        yuv_reader.allow_demo_mode = True
        yuv_reader.inputs.add(yuv_in_socket)
        yuv_reader.outputs.add(yuv_out_socket)

        res = yuv_reader.open()
        print_error("YUV reader open", yuv_reader.error)
        if not res:
            return False

        # Create H.264 encoder transcoder (frames are pushed)
        h264_in_socket = create_h264_encoder_input_socket(width, height, fps, color_format)
        h264_out_socket = create_h264_encoder_output_socket(
            output_file, width, height, fps, color_format)

        with Transcoder() as h264_encoder:
            h264_encoder.allow_demo_mode = True
            h264_encoder.inputs.add(h264_in_socket)
            h264_encoder.outputs.add(h264_out_socket)

            res = h264_encoder.open()
            print_error("H264 encoder open", h264_encoder.error)
            if not res:
                yuv_reader.close()
                return False

            res = encode_h264_stream(yuv_reader, h264_encoder)
            if not res:
                h264_encoder.close()
                yuv_reader.close()
                return False

            h264_encoder.close()
            print_error("H264 encoder close", h264_encoder.error)

        yuv_reader.close()
        print_error("YUV reader close", yuv_reader.error)

    return True


def parse_frame_size(frame_size: str):
    """Parse frame size string (e.g., '176x144'). Returns (width, height) or None."""
    if not frame_size:
        return None

    parts = frame_size.split('x')
    if len(parts) != 2:
        return None

    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


@click.command()
@click.option('-i', '--input', 'input_file',
              help='input YUV file',
              type=click.Path())
@click.option('-o', '--output', 'output_file',
              help='output H264 file',
              type=click.Path())
@click.option('-r', '--rate', 'fps',
              help='input frame rate',
              type=float)
@click.option('-f', '--frame', 'frame_size',
              help='input frame sizes <width>x<height>')
@click.option('-c', '--color', 'color_name',
              help='input color format. Use --colors to list all supported color formats')
@click.option('--colors', 'list_colors', is_flag=True,
              help='list COLOR constants')
def main(input_file: str, output_file: str, fps: float, frame_size: str,
         color_name: str, list_colors: bool):
    """Encode YUV file to H.264/AVC using push mode."""

    if list_colors:
        print_colors()
        sys.exit(0)

    # Set default options if no arguments are provided
    if len(sys.argv) == 1:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, "../../assets/vid/foreman_qcif.yuv")
        output_file = os.path.join(script_dir, "../../output/enc_avc_push/foreman_qcif.h264")
        fps = 30.0
        frame_size = "176x144"
        color_name = "yuv420"

        print("Using default options:")
        print(f"enc-avc-push --input {input_file} --output {output_file} "
              f"--rate {fps} --frame {frame_size} --color {color_name}")

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

    print("Input frame size: ", end="")
    size = parse_frame_size(frame_size)
    if size is None:
        print("[not set / incorrect]")
        error = True
    else:
        width, height = size
        print(frame_size)

    print("Input color format: ", end="")
    color_id = get_color_by_name(color_name) if color_name else None
    if color_id is None:
        print("[not set / incorrect]")
        error = True
    else:
        print(color_name)

    print("Output frame rate: ", end="")
    if not fps:
        print("[not set]")
        error = True
    else:
        print(fps)

    if error:
        click.echo("\nUse --help for usage information.")
        sys.exit(1)

    Library.initialize()

    # Set license information. To run AVBlocks in demo mode, comment the next line out
    # Library.set_license("<license-string>")

    result = encode(input_file, output_file, width, height, fps, color_id)

    Library.shutdown()

    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

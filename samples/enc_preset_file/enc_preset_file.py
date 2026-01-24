#!/usr/bin/env python3
"""
Encode raw YUV video file to compressed video using AVBlocks presets.

Shows how to convert a raw YUV video file to a compressed video file.
The format of the output is configured with an AVBlocks preset.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaSocket, MediaPin,
    VideoStreamInfo, StreamType, ColorFormat, ScanType,
    ErrorFacility, Preset
)


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

# Preset descriptors (name, file extension)
PRESETS = [
    (Preset.Video.DVD.NTSC_16x9_MP2, "mpg"),
    (Preset.Video.DVD.NTSC_16x9_PCM, "mpg"),
    (Preset.Video.DVD.NTSC_4x3_MP2, "mpg"),
    (Preset.Video.DVD.NTSC_4x3_PCM, "mpg"),
    (Preset.Video.DVD.PAL_16x9_MP2, "mpg"),
    (Preset.Video.DVD.PAL_4x3_MP2, "mpg"),
    (Preset.Video.iPad.H264_576p, "mp4"),
    (Preset.Video.iPad.H264_720p, "mp4"),
    (Preset.Video.iPad.MPEG4_480p, "mp4"),
    (Preset.Video.iPhone.H264_480p, "mp4"),
    (Preset.Video.iPhone.MPEG4_480p, "mp4"),
    (Preset.Video.iPod.H264_240p, "mp4"),
    (Preset.Video.iPod.MPEG4_240p, "mp4"),
    (Preset.Video.Generic.MP4.Base_H264_AAC, "mp4"),
    (Preset.Video.AppleLiveStreaming.H264_480p, "ts"),
    (Preset.Video.AppleLiveStreaming.H264_720p, "ts"),
    (Preset.Video.AndroidPhone.H264_360p, "mp4"),
    (Preset.Video.AndroidPhone.H264_720p, "mp4"),
    (Preset.Video.AndroidTablet.H264_720p, "mpg"),
    (Preset.Video.AndroidTablet.WebM_VP8_720p, "webm"),
    (Preset.Video.VCD.NTSC, "mpg"),
    (Preset.Video.VCD.PAL, "mpg"),
    (Preset.Video.Generic.WebM.Base_VP8_Vorbis, "webm"),
]


def get_color_by_name(name: str):
    """Get color format ID by name."""
    for color_id, color_name, _ in COLOR_FORMATS:
        if color_name.lower() == name.lower():
            return color_id
    return None


def get_preset_extension(preset_name: str) -> str:
    """Get file extension for a preset."""
    for name, ext in PRESETS:
        if name.lower() == preset_name.lower():
            return ext
    return "mp4"  # default


def print_colors():
    """Print supported color formats."""
    print("\nCOLORS")
    print("---------")
    for _, name, desc in COLOR_FORMATS:
        print(f"{name:<20} {desc}")
    print()


def print_presets():
    """Print supported presets."""
    print("\nPRESETS")
    print("-----------")
    for name, ext in PRESETS:
        print(f"{name:<30} .{ext}")
    print()


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


def parse_frame_size(frame_size: str):
    """Parse frame size string (e.g., '176x144') into width and height."""
    try:
        parts = frame_size.lower().split('x')
        if len(parts) != 2:
            return None, None
        return int(parts[0]), int(parts[1])
    except (ValueError, AttributeError):
        return None, None


def encode(input_file: str, output_file: str, width: int, height: int, 
           fps: float, color_id, preset_name: str) -> bool:
    """Encode raw YUV video to compressed video using preset."""
    # Delete output file if it exists
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    transcoder = Transcoder()
    
    # Transcoder demo mode must be enabled,
    # in order to use the OEM release for testing (without a valid license).
    transcoder.allow_demo_mode = True
    
    # Configure input
    # The input stream frame rate determines the playback speed
    in_stream = VideoStreamInfo()
    in_stream.stream_type = StreamType.UncompressedVideo
    in_stream.frame_rate = fps
    in_stream.frame_width = width
    in_stream.frame_height = height
    in_stream.color_format = color_id
    in_stream.scan_type = ScanType.Progressive
    
    in_pin = MediaPin()
    in_pin.stream_info = in_stream
    
    in_socket = MediaSocket()
    in_socket.stream_type = StreamType.UncompressedVideo
    in_socket.file = input_file
    in_socket.pins.add(in_pin)
    
    transcoder.inputs.add(in_socket)
    
    # Configure output
    out_socket = MediaSocket.from_preset(preset_name)
    if out_socket is None:
        print(f"Invalid preset: {preset_name}")
        return False
    
    out_socket.file = output_file
    transcoder.outputs.add(out_socket)
    
    # Open transcoder
    if not transcoder.open():
        print_error("Open Transcoder", transcoder.error)
        return False
    
    # Run transcoder
    if not transcoder.run():
        print_error("Run Transcoder", transcoder.error)
        transcoder.close()
        return False
    
    transcoder.close()
    
    print("Encoding completed successfully.")
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='input YUV file',
              type=click.Path())
@click.option('-o', '--output', 'output_file',
              help='output file',
              type=click.Path())
@click.option('-r', '--rate', 'fps',
              help='input frame rate',
              type=float)
@click.option('-f', '--frame', 'frame_size',
              help='input frame size (e.g., 176x144)')
@click.option('-c', '--color', 'color_name',
              help='input color space. Use --colors to list all supported input color spaces.')
@click.option('--colors', 'list_colors', is_flag=True,
              help='list supported input color spaces')
@click.option('-p', '--preset', 'preset_name',
              help='output preset id.')
@click.option('--presets', 'list_presets', is_flag=True,
              help='list supported presets')
def main(input_file: str, output_file: str, fps: float, frame_size: str,
         color_name: str, list_colors: bool, preset_name: str, list_presets: bool):
    """Encode raw YUV video file to compressed video using AVBlocks presets."""
    
    if list_colors:
        print_colors()
        sys.exit(0)
    
    if list_presets:
        print_presets()
        sys.exit(0)
    
    # Set default options if not provided
    use_defaults = not all([input_file, output_file, fps, frame_size, color_name, preset_name])
    
    if use_defaults:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../../assets/vid/foreman_qcif.yuv")
        if not output_file:
            output_file = os.path.join(script_dir, "../../output/enc_preset_file/foreman_qcif.mp4")
        if not fps:
            fps = 30.0
        if not frame_size:
            frame_size = "176x144"
        if not color_name:
            color_name = "yuv420"
        if not preset_name:
            preset_name = Preset.Video.Generic.MP4.Base_H264_AAC
        
        print("Using default options:")
        print(f"  --input {input_file}")
        print(f"  --output {output_file}")
        print(f"  --rate {fps}")
        print(f"  --frame {frame_size}")
        print(f"  --color {color_name}")
        print(f"  --preset {preset_name}")
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
    
    print("Input frame size: ", end="")
    width, height = parse_frame_size(frame_size) if frame_size else (None, None)
    if width is None or height is None:
        print("[not set / incorrect]")
        error = True
    else:
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
    
    result = encode(input_file, output_file, width, height, fps, color_id, preset_name)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

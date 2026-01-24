#!/usr/bin/env python3
"""
Create a video slideshow from a series of images.

Shows how to make a video clip from a sequence of images.
The input is a series of JPEG images. The output is configured with an AVBlocks preset.
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaInfo, MediaSocket, MediaPin,
    MediaBuffer, MediaSample, Preset, ErrorFacility
)


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


def get_preset_by_name(preset_name: str):
    """Get preset descriptor by name."""
    for name, ext in PRESETS:
        if name.lower() == preset_name.lower():
            return (name, ext)
    return None


def print_presets():
    """Print supported presets."""
    print()
    print("PRESETS")
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


def get_image_path(input_dir: str, image_number: int) -> str:
    """Get image file path for a given image number."""
    return os.path.join(input_dir, f"cube{image_number:04d}.jpeg")


def encode(input_dir: str, output_file: str, preset_id: str, file_extension: str) -> bool:
    """Encode images into a video slideshow."""
    out_filename = f"{output_file}.{file_extension}"
    image_count = 250
    input_frame_rate = 25.0
    
    transcoder = Transcoder()
    
    # In order to use the OEM release for testing (without a valid license),
    # the transcoder demo mode must be enabled.
    transcoder.allow_demo_mode = True
    
    try:
        delete_file(out_filename)
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(out_filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Configure Input
        media_info = MediaInfo()
        media_info.inputs[0].file = get_image_path(input_dir, 0)
        
        result = media_info.open()
        print_error("Open MediaInfo", media_info.error)
        if not result:
            return False
        
        vid_info = media_info.outputs[0].pins[0].stream_info.clone()
        vid_info.frame_rate = input_frame_rate
        
        pin = MediaPin()
        pin.stream_info = vid_info
        
        socket = MediaSocket()
        socket.pins.add(pin)
        
        transcoder.inputs.add(socket)
        
        media_info.close()
        
        # Configure Output
        socket = MediaSocket.from_preset(preset_id)
        socket.file = out_filename
        
        transcoder.outputs.add(socket)
        
        # Encode Images
        result = transcoder.open()
        print_error("Open Transcoder", transcoder.error)
        if not result:
            return False
        
        for i in range(image_count):
            image_path = get_image_path(input_dir, i)
            
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            media_buffer = MediaBuffer(image_data)
            media_sample = MediaSample()
            media_sample.start_time = i / input_frame_rate
            media_sample.buffer = media_buffer
            
            if not transcoder.push(0, media_sample):
                print_error("Push Transcoder", transcoder.error)
                return False
        
        result = transcoder.flush()
        print_error("Flush Transcoder", transcoder.error)
        if not result:
            return False
        
        transcoder.close()
        print(f'Output video: "{out_filename}"')
        
    except Exception as ex:
        print(str(ex))
        return False
    
    return True


@click.command()
@click.option('-i', '--input', 'input_dir',
              help='Input directory containing images for the slideshow.')
@click.option('-o', '--output', 'output_file',
              help='Output filename (without extension). The extension is added based on the preset.')
@click.option('-p', '--preset', 'preset_id',
              help='output preset id.')
@click.option('--presets', 'list_presets', is_flag=True,
              help='list supported input presets')
def main(input_dir: str, output_file: str, preset_id: str, list_presets: bool):
    """Create a video slideshow from a series of JPEG images."""
    
    if list_presets:
        print_presets()
        sys.exit(0)
    
    # Set default options if not provided
    if not input_dir:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        input_dir = os.path.join(script_dir, "../../assets/img")
        output_file = os.path.join(script_dir, "../../output/slideshow/cube")
        preset_id = Preset.Video.Generic.MP4.Base_H264_AAC  # "mp4.h264.aac"
        
        print("Using default options: ")
        print(f" --input {input_dir} --output {output_file} --preset {preset_id}")
    
    # Validate options
    error = False
    
    print("Input dir: ", end="")
    if not input_dir:
        print("[not set]")
        error = True
    else:
        print(input_dir)
    
    print("Output file: ", end="")
    if not output_file:
        print("[not set]")
        error = True
    else:
        print(output_file)
    
    if error:
        click.echo("\nUse --help for usage information.")
        sys.exit(1)
    
    # Get filename extension from preset descriptor
    preset = get_preset_by_name(preset_id)
    if preset is None:
        print("\nPreset not found!")
        sys.exit(1)
    
    file_extension = preset[1]
    
    Library.initialize()
    
    # Set license information. To run AVBlocks in demo mode, comment the next line out
    # Library.set_license("<license-string>")
    
    result = encode(input_dir, output_file, preset_id, file_extension)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

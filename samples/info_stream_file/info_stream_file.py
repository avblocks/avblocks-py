#!/usr/bin/env python3
"""
Display detailed stream information about a media file.

This sample shows how to use MediaInfo to get detailed information
about the audio and video streams in a media file.
"""

import os
import sys
import click

from avblocks import (
    Library, MediaInfo, AudioStreamInfo, VideoStreamInfo,
    StreamType, StreamSubType, MediaType, ColorFormat, ScanType, BitrateMode
)

def get_stream_type_name(stream_type: int) -> str:
    """Get a human-readable name for stream type."""
    type_names = {
        StreamType.Unknown: "Unknown",
        StreamType.LPCM: "LPCM",
        StreamType.ALAW_PCM: "ALAW_PCM",
        StreamType.MULAW_PCM: "MULAW_PCM",
        StreamType.VIDEO_DVD_PCM: "VIDEO_DVD_PCM",
        StreamType.AC3: "AC3",
        StreamType.DTS: "DTS",
        StreamType.MPEG_Audio: "MPEG_Audio",
        StreamType.Vorbis: "Vorbis",
        StreamType.AAC: "AAC",
        StreamType.AMRNB: "AMRNB",
        StreamType.AMRWB: "AMRWB",
        StreamType.G726_ADPCM: "G726_ADPCM",
        StreamType.WMA: "WMA",
        StreamType.WMA_Professional: "WMA_Professional",
        StreamType.WMA_Lossless: "WMA_Lossless",
        StreamType.UncompressedVideo: "UncompressedVideo",
        StreamType.MPEG1_Video: "MPEG1_Video",
        StreamType.MPEG2_Video: "MPEG2_Video",
        StreamType.MPEG4_Video: "MPEG4_Video",
        StreamType.H261: "H261",
        StreamType.H263: "H263",
        StreamType.H264: "H264",
        StreamType.H265: "H265",
        StreamType.WMV: "WMV",
        StreamType.MJPEG: "MJPEG",
        StreamType.VC1: "VC1",
        StreamType.AVS: "AVS",
        StreamType.VP8: "VP8",
        StreamType.VP9: "VP9",
        StreamType.AV1: "AV1",
        StreamType.AV2: "AV2",
        StreamType.Theora: "Theora",
        StreamType.AVI: "AVI",
        StreamType.MP4: "MP4",
        StreamType.ASF: "ASF",
        StreamType.MPEG_PS: "MPEG_PS",
        StreamType.MPEG_TS: "MPEG_TS",
        StreamType.MPEG_PES: "MPEG_PES",
        StreamType.WAVE: "WAVE",
        StreamType.FLV: "FLV",
        StreamType.OGG: "OGG",
        StreamType.WebM: "WebM",
        StreamType.IVF: "IVF",
        StreamType.BMP: "BMP",
        StreamType.PNG: "PNG",
        StreamType.JPEG: "JPEG",
        StreamType.TIFF: "TIFF",
        StreamType.GIF: "GIF",
        StreamType.Teletext: "Teletext",
        StreamType.MPEG_PSI_PACKETS: "MPEG_PSI_PACKETS",
        StreamType.MPEG_TS_PACKETS: "MPEG_TS_PACKETS",
    }
    return type_names.get(stream_type, f"StreamType({stream_type})")


def get_stream_sub_type_name(stream_sub_type: int) -> str:
    """Get a human-readable name for stream sub type."""
    sub_type_names = {
        StreamSubType.Unknown: "Unknown",
        StreamSubType.None_: "None",
        StreamSubType.AAC_ADTS: "AAC_ADTS",
        StreamSubType.AAC_ADIF: "AAC_ADIF",
        StreamSubType.AAC_MP4: "AAC_MP4",
        StreamSubType.AVCC: "AVCC",
        StreamSubType.HVCC: "HVCC",
        StreamSubType.MPEG_TS_BDAV: "MPEG_TS_BDAV",
        StreamSubType.MPEG_Audio_Layer1: "MPEG_Audio_Layer1",
        StreamSubType.MPEG_Audio_Layer2: "MPEG_Audio_Layer2",
        StreamSubType.MPEG_Audio_Layer3: "MPEG_Audio_Layer3",
        StreamSubType.G726_RFC3551: "G726_RFC3551",
        StreamSubType.G726_AAL2: "G726_AAL2",
        StreamSubType.MPEG1_System: "MPEG1_System",
        StreamSubType.MPEG2_System: "MPEG2_System",
        StreamSubType.AVC_Annex_B: "AVC_Annex_B",
        StreamSubType.HEVC_Annex_B: "HEVC_Annex_B",
        StreamSubType.AAC_RAW: "AAC_RAW",
    }
    return sub_type_names.get(stream_sub_type, f"StreamSubType({stream_sub_type})")


def get_media_type_name(media_type: int) -> str:
    """Get a human-readable name for media type."""
    type_names = {
        MediaType.Unknown: "Unknown",
        MediaType.Audio: "Audio",
        MediaType.Video: "Video",
    }
    return type_names.get(media_type, f"MediaType({media_type})")


def get_color_format_name(color_format: int) -> str:
    """Get a human-readable name for color format."""
    format_names = {
        ColorFormat.Unknown: "Unknown",
        ColorFormat.YV12: "YV12",
        ColorFormat.NV12: "NV12",
        ColorFormat.YUY2: "YUY2",
        ColorFormat.UYVY: "UYVY",
        ColorFormat.YUV411: "YUV411",
        ColorFormat.YUV420: "YUV420",
        ColorFormat.YUV422: "YUV422",
        ColorFormat.YUV444: "YUV444",
        ColorFormat.Y411: "Y411",
        ColorFormat.Y41P: "Y41P",
        ColorFormat.BGR32: "BGR32",
        ColorFormat.BGR24: "BGR24",
        ColorFormat.BGR565: "BGR565",
        ColorFormat.BGR555: "BGR555",
        ColorFormat.BGR444: "BGR444",
        ColorFormat.GRAY: "GRAY",
        ColorFormat.YUV420A: "YUV420A",
        ColorFormat.YUV422A: "YUV422A",
        ColorFormat.YUV444A: "YUV444A",
        ColorFormat.YVU9: "YVU9",
        ColorFormat.BGRA32: "BGRA32",
    }
    return format_names.get(color_format, f"ColorFormat({color_format})")


def get_scan_type_name(scan_type: int) -> str:
    """Get a human-readable name for scan type."""
    type_names = {
        ScanType.Unknown: "Unknown",
        ScanType.Progressive: "Progressive",
        ScanType.TopFieldFirst: "TopFieldFirst",
        ScanType.BottomFieldFirst: "BottomFieldFirst",
    }
    return type_names.get(scan_type, f"ScanType({scan_type})")


def get_bitrate_mode_name(bitrate_mode: int) -> str:
    """Get a human-readable name for bitrate mode."""
    mode_names = {
        BitrateMode.Unknown: "Unknown",
        BitrateMode.CBR: "CBR",
        BitrateMode.VBR: "VBR",
        BitrateMode.ABR: "ABR",
    }
    return mode_names.get(bitrate_mode, f"BitrateMode({bitrate_mode})")


def print_video(vsi: VideoStreamInfo):
    """Print video stream information."""
    print(f"bitrate: {vsi.bitrate} mode: {get_bitrate_mode_name(vsi.bitrate_mode)}")
    print(f"color format: {get_color_format_name(vsi.color_format)}")
    print(f"display ratio: {vsi.display_ratio_width}:{vsi.display_ratio_height}")
    print(f"frame bottom up: {vsi.frame_bottom_up}")
    print(f"frame size: {vsi.frame_width}x{vsi.frame_height}")
    print(f"frame rate: {vsi.frame_rate:.3f}")
    print(f"scan type: {get_scan_type_name(vsi.scan_type)}")


def print_audio(asi: AudioStreamInfo):
    """Print audio stream information."""
    print(f"bitrate: {asi.bitrate} mode: {get_bitrate_mode_name(asi.bitrate_mode)}")
    print(f"bits per sample: {asi.bits_per_sample}")
    print(f"bytes per frame: {asi.bytes_per_frame}")
    print(f"channel layout: {asi.channel_layout:08X}")
    print(f"channels: {asi.channels}")
    print(f"flags: {asi.pcm_flags:08X}")
    print(f"sample rate: {asi.sample_rate}")


def print_streams(media_info: MediaInfo):
    """Print all stream information from a MediaInfo object."""
    for socket in media_info.outputs:
        print(f"container: {get_stream_type_name(socket.stream_type)}")
        print(f"streams: {len(socket.pins)}")

        for stream_index, pin in enumerate(socket.pins):
            si = pin.stream_info
            
            print()
            print(f"stream #{stream_index} {get_media_type_name(si.media_type)}")
            print(f"type: {get_stream_type_name(si.stream_type)}")
            print(f"subtype: {get_stream_sub_type_name(si.stream_sub_type)}")
            print(f"id: {si.id}")
            print(f"duration: {si.duration:.3f}")
            
            if si.media_type == MediaType.Video:
                print_video(si)
            elif si.media_type == MediaType.Audio:
                print_audio(si)
            else:
                print()

        print()


def av_info(input_file: str) -> bool:
    """Get stream information from a media file."""
    media_info = MediaInfo()
    media_info.inputs[0].file = input_file
    
    if media_info.open():
        print_streams(media_info)
        media_info.close()
    else:
        print(f"{media_info.error.message or ''}, facility:{media_info.error.facility} code:{media_info.error.code} hint:{media_info.error.hint or ''}")
    
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input media file',
              type=click.Path(exists=True))
def main(input_file: str):
    """Display stream information about a media file."""
    
    # Set default options if not provided
    if not input_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, "../../assets/mov/big_buck_bunny_trailer.mp4")
        
        print("Using default options:")
        print(f"  --input {input_file}")
        print()
    
    Library.initialize()
    
    # Set license information. To run AVBlocks in demo mode, comment the next line out
    # Library.set_license("<license-string>")
    
    result = av_info(input_file)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

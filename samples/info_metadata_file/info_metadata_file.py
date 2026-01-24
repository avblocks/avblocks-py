#!/usr/bin/env python3
"""
Display metadata information and save embedded pictures from a media file.

This sample shows how to use MediaInfo to extract metadata attributes
(title, artist, album, etc.) and embedded pictures (album art) from 
audio/video files.
"""

import os
import sys
import click

from avblocks import (
    Library, MediaInfo, MetaPictureType
)


def get_picture_type_name(picture_type: int) -> str:
    """Get a human-readable name for picture type."""
    type_names = {
        MetaPictureType.Other: "Other",
        MetaPictureType.FileIcon: "File Icon",
        MetaPictureType.OtherFileIcon: "Other File Icon",
        MetaPictureType.FrontCover: "Front Cover",
        MetaPictureType.BackCover: "Back Cover",
        MetaPictureType.LeafletPage: "Leaflet Page",
        MetaPictureType.Media: "Media",
        MetaPictureType.LeadArtist: "Lead Artist",
        MetaPictureType.Artist: "Artist",
        MetaPictureType.Conductor: "Conductor",
        MetaPictureType.Band: "Band",
        MetaPictureType.Composer: "Composer",
        MetaPictureType.TextWriter: "Text Writer",
        MetaPictureType.RecordingLocation: "Recording Location",
        MetaPictureType.DuringRecording: "During Recording",
        MetaPictureType.DuringPerformance: "During Performance",
        MetaPictureType.VideoCapture: "Video Capture",
        MetaPictureType.BrightColoredFish: "Bright Colored Fish",
        MetaPictureType.Illustration: "Illustration",
        MetaPictureType.ArtistLogotype: "Artist Logotype",
        MetaPictureType.PublisherLogotype: "Publisher Logotype",
    }
    return type_names.get(picture_type, f"Unknown({picture_type})")


def get_file_extension_from_mime(mime_type: str) -> str:
    """Get file extension from MIME type."""
    mime_to_ext = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/bmp": ".bmp",
        "image/tiff": ".tiff",
    }
    return mime_to_ext.get(mime_type.lower(), ".bin")


def print_metadata(media_info: MediaInfo, output_dir: str | None = None):
    """Print metadata and optionally save pictures."""
    print(f"File: {media_info.inputs[0].file}")
    print()
    
    # Access metadata from the first output socket
    if len(media_info.outputs) == 0 or len(media_info.outputs[0].pins) == 0:
        print("No streams found")
        return
    
    socket = media_info.outputs[0]
    metadata = socket.metadata
    
    if metadata is None:
        print("No metadata found")
        return
    
    # Print attributes
    print("=== Metadata Attributes ===")
    if len(metadata.attributes) == 0:
        print("  (none)")
    else:
        for attr in metadata.attributes:
            name = attr.name if attr.name else "(unknown)"
            value = attr.value if attr.value else ""
            print(f"  {name}: {value}")
    
    print()
    
    # Print and optionally save pictures
    print(f"=== Embedded Pictures ({len(metadata.pictures)}) ===")
    if len(metadata.pictures) == 0:
        print("  (none)")
    else:
        for i, pic in enumerate(metadata.pictures):
            pic_type_name = get_picture_type_name(pic.picture_type)
            mime = pic.mime_type if pic.mime_type else "unknown"
            desc = pic.description if pic.description else ""
            size = len(pic.bytes) if pic.bytes else 0
            
            print(f"  Picture #{i}:")
            print(f"    Type: {pic_type_name}")
            print(f"    MIME: {mime}")
            if desc:
                print(f"    Description: {desc}")
            print(f"    Size: {size} bytes")
            
            # Save picture if output directory is specified
            if output_dir and pic.bytes:
                # Create output directory if needed
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                ext = get_file_extension_from_mime(mime)
                filename = f"picture_{i}{ext}"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(pic.bytes)
                
                print(f"    Saved to: {filepath}")
            
            print()


def info_metadata(input_file: str, output_dir: str | None = None) -> bool:
    """Get metadata from a media file."""
    # Create MediaInfo object
    media_info = MediaInfo()
    media_info.inputs[0].file = input_file
    
    if not media_info.open():
        print(f"Failed to open: {input_file}")
        return False
    
    print_metadata(media_info, output_dir)
    
    media_info.close()
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input media file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_dir',
              help='Output directory for pictures (optional)',
              type=click.Path())
def main(input_file: str, output_dir: str):
    """Display metadata and save pictures from a media file."""
    
    # Set default options if not provided
    if not input_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, "../assets/aud/Hydrate-Kenny_Beltrey.ogg")
        
        print("Using default options:")
        print(f"  --input {input_file}")
        if output_dir:
            print(f"  --output {output_dir}")
        print()
    
    Library.initialize()
    
    # Set license information. Without this AVBlocks runs in Demo mode.
    # Library.set_license("<license-string>")
    
    result = info_metadata(input_file, output_dir)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()

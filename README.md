# avblocks-py

AVBlocks Python SDK

Docs: [https://doc.avblocks.com/python/latest](https://doc.avblocks.com/python/latest)

# Usage

## Getting Started

### Installation

#### Prerequisites

- Python 3.9 or higher
- pip or uv package manager

AVBlocks Python SDK is not distributed via PyPI. Install it directly from the GitHub repository.

#### Install with pip

```bash
pip install git+https://github.com/avblocks/avblocks-py.git@3.4.0.2
```

#### Install with uv

From within your project directory:

```bash
uv add git+https://github.com/avblocks/avblocks-py.git --tag 3.4.0.2
```

This adds `avblocks` as a dependency in your `pyproject.toml`.

### Library Initialization

Before using any AVBlocks functionality, initialize the library:

```python
from avblocks import Library

Library.initialize()

# Set license information. AVBlocks runs in demo mode if license is not set. 
# Library.set_license("<license-string>")

# Your code here

Library.shutdown()
```

## Core Concepts

### MediaSocket

A `MediaSocket` represents an input or output media endpoint. It describes:
- The media file location (`file` property)
- The stream type (`stream_type` property)
- One or more media pins (`pins` collection)

```python
from avblocks import MediaSocket, StreamType

socket = MediaSocket()
socket.file = "input.mp4"
socket.stream_type = StreamType.UncompressedVideo
```

### MediaPin

A `MediaPin` represents a single media stream (audio or video) within a `MediaSocket`. Each pin contains:
- Stream information (`stream_info` property) - describes the format and characteristics of the stream
- Stream configuration for encoding/decoding

**Key Properties:**
- `stream_info` - Contains detailed format information (VideoStreamInfo or AudioStreamInfo)

Example for video input:
```python
from avblocks import MediaPin, VideoStreamInfo, StreamType, ColorFormat, ScanType

pin = MediaPin()
vsi = VideoStreamInfo()
pin.stream_info = vsi

vsi.stream_type = StreamType.UncompressedVideo
vsi.frame_width = 176
vsi.frame_height = 144
vsi.color_format = ColorFormat.YUV420
vsi.frame_rate = 30.0
vsi.scan_type = ScanType.Progressive

socket.pins.add(pin)
```

### MediaInfo

`MediaInfo` is used to extract metadata and stream information from media files without processing the content.

**Key Features:**
- Extract audio/video stream details
- Read file metadata (title, artist, album, etc.)
- No transcoding required

```python
from avblocks import MediaInfo

info = MediaInfo()
info.inputs[0].file = "input.mp4"

if info.open():
    # Access stream information
    for pin in info.outputs[0].pins:
        stream_info = pin.stream_info
        # Process stream info
    
    # Access metadata
    for attr in info.outputs[0].metadata:
        print(f"{attr.name}: {attr.value}")
    
    info.close()
else:
    # Handle error
    error = info.error
```

## Common Operations

### Media Information Extraction

#### Stream Information
```python
from avblocks import MediaInfo, MediaType

info = MediaInfo()
info.inputs[0].file = input_file

if info.open():
    for pin in info.outputs[0].pins:
        si = pin.stream_info
        
        if si.media_type == MediaType.Video:
            vsi = si  # VideoStreamInfo
            print(f"Video: {vsi.frame_width}x{vsi.frame_height}")
            print(f"  Frame Rate: {vsi.frame_rate}")
            print(f"  Color Format: {vsi.color_format}")
        elif si.media_type == MediaType.Audio:
            asi = si  # AudioStreamInfo
            print(f"Audio: {asi.sample_rate}Hz, {asi.channels} channels")
            print(f"  Bits Per Sample: {asi.bits_per_sample}")
    
    info.close()
```

#### Metadata Extraction
```python
from avblocks import MediaInfo

info = MediaInfo()
info.inputs[0].file = input_file

if info.open():
    for attr in info.outputs[0].metadata:
        print(f"{attr.name}: {attr.value}")
    info.close()
```

### Video Encoding

#### Encode Raw YUV to H.264/AVC
```python
from avblocks import (MediaSocket, MediaPin, VideoStreamInfo, 
                      Transcoder, StreamType, ColorFormat, ScanType)

# Create input socket for raw YUV
in_vsi = VideoStreamInfo()
in_vsi.stream_type = StreamType.UncompressedVideo
in_vsi.scan_type = ScanType.Progressive
in_vsi.frame_width = 176
in_vsi.frame_height = 144
in_vsi.color_format = ColorFormat.YUV420
in_vsi.frame_rate = 30.0

in_pin = MediaPin()
in_pin.stream_info = in_vsi

in_socket = MediaSocket()
in_socket.stream_type = StreamType.UncompressedVideo
in_socket.file = "input.yuv"
in_socket.pins.add(in_pin)

# Create output socket for H.264
out_vsi = VideoStreamInfo()
out_vsi.stream_type = StreamType.H264
out_vsi.frame_width = 176
out_vsi.frame_height = 144
out_vsi.frame_rate = 30.0

out_pin = MediaPin()
out_pin.stream_info = out_vsi

out_socket = MediaSocket()
out_socket.stream_type = StreamType.H264
out_socket.file = "output.h264"
out_socket.pins.add(out_pin)

# Encode
transcoder = Transcoder()
transcoder.inputs.add(in_socket)
transcoder.outputs.add(out_socket)

if transcoder.open():
    if transcoder.run():
        print("Encoding successful")
    transcoder.close()
```

#### Encode with Preset
```python
from avblocks import MediaSocket, Transcoder, Preset

in_socket = MediaSocket()
in_socket.file = "input.yuv"
# ... configure input

out_socket = MediaSocket()
out_socket.file = "output.mp4"
out_socket.preset = Preset.Video.Generic.MP4.Base_H264_AAC

transcoder = Transcoder()
transcoder.inputs.add(in_socket)
transcoder.outputs.add(out_socket)

if transcoder.open():
    transcoder.run()
    transcoder.close()
```

### Video Decoding

#### Decode H.264 to Raw YUV
```python
from avblocks import (MediaSocket, MediaPin, VideoStreamInfo, 
                      Transcoder, StreamType, ColorFormat)

# Create input socket for H.264
in_socket = MediaSocket()
in_socket.stream_type = StreamType.H264
in_socket.file = "input.h264"

# Create output socket for raw YUV
out_vsi = VideoStreamInfo()
out_vsi.stream_type = StreamType.UncompressedVideo
out_vsi.color_format = ColorFormat.YUV420

out_pin = MediaPin()
out_pin.stream_info = out_vsi

out_socket = MediaSocket()
out_socket.stream_type = StreamType.UncompressedVideo
out_socket.file = "output.yuv"
out_socket.pins.add(out_pin)

# Decode
transcoder = Transcoder()
transcoder.inputs.add(in_socket)
transcoder.outputs.add(out_socket)

if transcoder.open():
    transcoder.run()
    transcoder.close()
```

### Audio Encoding

#### Encode WAV to AAC (ADTS)
```python
from avblocks import MediaSocket, Transcoder, StreamType, StreamSubType

in_socket = MediaSocket()
in_socket.file = "input.wav"

out_socket = MediaSocket()
out_socket.stream_type = StreamType.Aac
out_socket.stream_sub_type = StreamSubType.AacAdts
out_socket.file = "output.aac"

transcoder = Transcoder()
transcoder.inputs.add(in_socket)
transcoder.outputs.add(out_socket)

if transcoder.open():
    transcoder.run()
    transcoder.close()
```

#### Encode WAV to MP3
```python
from avblocks import MediaSocket, Transcoder, StreamType

in_socket = MediaSocket()
in_socket.file = "input.wav"

out_socket = MediaSocket()
out_socket.file = "output.mp3"
out_socket.stream_type = StreamType.Mp3

transcoder = Transcoder()
transcoder.inputs.add(in_socket)
transcoder.outputs.add(out_socket)

if transcoder.open():
    transcoder.run()
    transcoder.close()
```

### Container Operations

#### Demux MP4 File
```python
from avblocks import MediaSocket, Transcoder, StreamType

# Extract video and audio streams from MP4

# Input
in_socket = MediaSocket()
in_socket.file = "input.mp4"

# Output for video stream
video_out = MediaSocket()
video_out.stream_type = StreamType.H264
video_out.file = "video.mp4"

# Output for audio stream
audio_out = MediaSocket()
audio_out.file = "audio.mp4"
audio_out.stream_type = StreamType.Aac

transcoder = Transcoder()
transcoder.inputs.add(in_socket)
transcoder.outputs.add(video_out)
transcoder.outputs.add(audio_out)

if transcoder.open():
    transcoder.run()
    transcoder.close()
```

#### Mux MP4 File
```python
from avblocks import MediaSocket, Transcoder

# Combine separate audio and video files into MP4 container

# Video input
video_in = MediaSocket()
video_in.file = "video.h264.mp4"

# Audio input
audio_in = MediaSocket()
audio_in.file = "audio.aac.mp4"

# Combined output
out_socket = MediaSocket()
out_socket.file = "output.mp4"

transcoder = Transcoder()
transcoder.inputs.add(video_in)
transcoder.inputs.add(audio_in)
transcoder.outputs.add(out_socket)

if transcoder.open():
    transcoder.run()
    transcoder.close()
```

### Error Handling

```python
from avblocks import Transcoder, ErrorInfo

def print_error(action: str, error: ErrorInfo):
    if error:
        print(f"Error: {action}")
        print(f"  Facility: {error.facility}")
        print(f"  Code: {error.code}")
        print(f"  Message: {error.message}")
        print(f"  Hint: {error.hint}")

transcoder = Transcoder()
transcoder.inputs.add(in_socket)
transcoder.outputs.add(out_socket)

if not transcoder.open():
    print_error("Open Transcoder", transcoder.error)
    return False

if not transcoder.run():
    print_error("Run Transcoder", transcoder.error)
    transcoder.close()
    return False

transcoder.close()
```

## Available Samples

See [samples/README.md](./samples/README.md) for a complete list of working examples including:

- **Media Info**: Extract stream information and metadata
- **Encoding**: AAC, MP3, H.264/AVC, with presets
- **Decoding**: H.264 to YUV
- **Container Operations**: Demux/Mux MP4 files
- **Misc**: Re-encoding, slideshow generation

# Development

## Setup

### macOS

1. [Download Core and Assets on macOS](./docs/download-avblocks-core-and-assets-mac.md) 
2. [Setup for macOS](./docs/setup-mac.md)

### Linux

1. [Download Core and Assets on Linux](./docs/download-avblocks-core-and-assets-linux.md)
2. [Setup for Linux](./docs/setup-linux.md)

### Windows

1. [Download Core and Assets on Windows](./docs/download-avblocks-core-and-assets-windows.md) 
2. [Setup for Windows](./docs/setup-windows.md)

## Run

### Create virtual environment

macOS:

```bash
source configure.sh
```

Linux:

```bash
source configure.sh
```

Windows:

```powershell
. .\configure.ps1
```

### Run Samples

See [README](./samples/README.md) in the `samples` subdirectory. 

# How to obtain Commercial License

See [License Options](https://avblocks.com/license/) for details.

We offer discounts for:

- Competitive product
- Startup
- Educational institution
- Open source project

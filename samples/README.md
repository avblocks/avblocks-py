# AVBlocks Python Samples

This directory contains sample applications demonstrating the AVBlocks Python SDK capabilities.

## Running Samples

All samples are installed as command-line tools when you install the package:

```bash
# Install the package in development mode
pip install --editable .

# Run any sample
dec-aac-adts-file --help
```

Or run directly with Python:

```bash
python -m samples.dec_aac_adts_file.dec_aac_adts_file --help
```

## Sample Categories

### Audio Decoding

| Sample | Description |
|--------|-------------|
| [dec_aac_adts_file](dec_aac_adts_file/) | Decode AAC ADTS to WAV |
| [dec_aac_adts_pull](dec_aac_adts_pull/) | Decode AAC ADTS to WAV using pull mode |
| [dec_g711_alaw_file](dec_g711_alaw_file/) | Decode G.711 A-law to WAV |
| [dec_g711_ulaw_file](dec_g711_ulaw_file/) | Decode G.711 μ-law to WAV |
| [dec_mp3_file](dec_mp3_file/) | Decode MP3 to WAV |
| [dec_opus_file](dec_opus_file/) | Decode Opus to WAV |
| [dec_vorbis_file](dec_vorbis_file/) | Decode Vorbis to WAV |

### Video Decoding

| Sample | Description |
|--------|-------------|
| [dec_avc_file](dec_avc_file/) | Decode H.264/AVC to raw YUV |
| [dec_avc_pull](dec_avc_pull/) | Decode H.264/AVC to YUV using pull mode |
| [dec_avc_au](dec_avc_au/) | Decode H.264 access units from directory |
| [dec_hevc_file](dec_hevc_file/) | Decode H.265/HEVC to raw YUV |
| [dec_hevc_au](dec_hevc_au/) | Decode H.265 access units from directory |
| [dec_vp8_file](dec_vp8_file/) | Decode VP8 (IVF) to raw YUV |
| [dec_vp9_file](dec_vp9_file/) | Decode VP9 (IVF) to raw YUV |

### Audio Encoding

| Sample | Description |
|--------|-------------|
| [enc_aac_adts_file](enc_aac_adts_file/) | Encode WAV to AAC ADTS |
| [enc_aac_adts_pull](enc_aac_adts_pull/) | Encode WAV to AAC ADTS using pull mode |
| [enc_aac_adts_push](enc_aac_adts_push/) | Encode WAV to AAC ADTS using push mode |
| [enc_g711_alaw_file](enc_g711_alaw_file/) | Encode WAV to G.711 A-law |
| [enc_g711_ulaw_file](enc_g711_ulaw_file/) | Encode WAV to G.711 μ-law |
| [enc_mp3_file](enc_mp3_file/) | Encode WAV to MP3 |
| [enc_mp3_pull](enc_mp3_pull/) | Encode WAV to MP3 using pull mode |
| [enc_mp3_push](enc_mp3_push/) | Encode WAV to MP3 using push mode |
| [enc_opus_file](enc_opus_file/) | Encode WAV to Opus (OGG) |
| [enc_vorbis_file](enc_vorbis_file/) | Encode WAV to Vorbis (OGG) |

### Video Encoding

| Sample | Description |
|--------|-------------|
| [enc_avc_file](enc_avc_file/) | Encode raw YUV to H.264/AVC |
| [enc_avc_pull](enc_avc_pull/) | Encode raw YUV to H.264 using pull mode |
| [enc_hevc_file](enc_hevc_file/) | Encode raw YUV to H.265/HEVC |
| [enc_hevc_pull](enc_hevc_pull/) | Encode raw YUV to H.265 using pull mode |
| [enc_vp8_file](enc_vp8_file/) | Encode raw YUV to VP8 (IVF) |
| [enc_vp9_file](enc_vp9_file/) | Encode raw YUV to VP9 (IVF) |

### Container Operations

| Sample | Description |
|--------|-------------|
| [demux_mp4_file](demux_mp4_file/) | Demux MP4 into separate audio/video streams |
| [mux_mp4_file](mux_mp4_file/) | Mux audio and video into MP4 container |
| [demux_webm_file](demux_webm_file/) | Demux WebM into separate audio/video streams |
| [mux_webm_file](mux_webm_file/) | Mux audio and video into WebM container |

### Media Information

| Sample | Description |
|--------|-------------|
| [info_stream_file](info_stream_file/) | Display stream information (codecs, resolution, etc.) |
| [info_metadata_file](info_metadata_file/) | Display metadata and extract embedded pictures |

### Audio Processing

| Sample | Description |
|--------|-------------|
| [audio_upsample](audio_upsample/) | Upsample audio from 44.1 KHz to 48 KHz |

### Video Processing

| Sample | Description |
|--------|-------------|
| [video_crop](video_crop/) | Crop a video by removing pixels from the edges |
| [video_framerate](video_framerate/) | Change the frame rate of a video |
| [video_pad](video_pad/) | Add black border padding around a video |
| [video_upscale](video_upscale/) | Upscale a video to Full HD (1920x1080) using bicubic interpolation |

### Utilities

| Sample | Description |
|--------|-------------|
| [enc_preset_file](enc_preset_file/) | Encode using AVBlocks presets |
| [re_encode](re_encode/) | Remux media with optional forced re-encoding |
| [slideshow](slideshow/) | Create video slideshow from images |
| [dump_avc_au](dump_avc_au/) | Dump H.264/AVC stream into access unit files |
| [dump_hevc_au](dump_hevc_au/) | Dump H.265/HEVC stream into access unit files |

## Processing Modes

### File Mode
The simplest approach - specify input and output files, and the transcoder handles everything:
- `dec-aac-adts-file`, `enc-mp3-file`, etc.

### Pull Mode  
Pull encoded/decoded samples one at a time for custom processing:
- `dec-avc-pull`, `enc-aac-adts-pull`, etc.
- Useful for streaming, frame-by-frame analysis, or custom containers

### Push Mode
Push data to the encoder/decoder manually:
- `enc-aac-adts-push`, `enc-mp3-push`
- Useful for real-time encoding from live sources

## Common Options

Most samples support these options:

| Option | Description |
|--------|-------------|
| `-i`, `--input` | Input file path |
| `-o`, `--output` | Output file path |
| `--help` | Show help message |

If no options are provided, samples use sensible defaults with files from the `assets/` directory.

## License

Samples run in demo mode by default. For production use, set your license:

```python
Library.set_license("<your-license-string>")
```

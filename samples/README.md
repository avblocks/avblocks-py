# AVBlocks Python Samples

This directory contains sample applications demonstrating the AVBlocks Python SDK capabilities.

## Running Samples

All samples are installed as command-line tools when you install the package:

```bash
# Install the package in development mode
pip install -e .

# Run any sample
dec-aac-adts-file --help
```

Or run directly with Python:

```bash
python -m samples.dec-aac-adts-file.dec-aac-adts-file --help
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

### Video Decoding

| Sample | Description |
|--------|-------------|
| [dec_avc_file](dec_avc_file/) | Decode H.264/AVC to raw YUV |
| [dec_avc_pull](dec_avc_pull/) | Decode H.264/AVC to YUV using pull mode |
| [dec_avc_au](dec_avc_au/) | Decode H.264 access units from directory |

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

### Video Encoding

| Sample | Description |
|--------|-------------|
| [enc_avc_file](enc_avc_file/) | Encode raw YUV to H.264/AVC |
| [enc_avc_pull](enc_avc_pull/) | Encode raw YUV to H.264 using pull mode |

### Container Operations

| Sample | Description |
|--------|-------------|
| [demux_mp4_file](demux_mp4_file/) | Demux MP4 into separate audio/video streams |
| [mux_mp4_file](mux_mp4_file/) | Mux audio and video into MP4 container |

### Media Information

| Sample | Description |
|--------|-------------|
| [info_stream_file](info_stream_file/) | Display stream information (codecs, resolution, etc.) |
| [info_metadata_file](info_metadata_file/) | Display metadata and extract embedded pictures |

### Utilities

| Sample | Description |
|--------|-------------|
| [enc_preset_file](enc_preset_file/) | Encode using AVBlocks presets |
| [re_encode](re_encode/) | Re-encode media with optional forced re-encoding |
| [slideshow](slideshow/) | Create video slideshow from images |

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

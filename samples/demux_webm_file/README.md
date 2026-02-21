## demux_webm_file

Shows how to extract the audio and video streams from a WebM file and save to two separate WebM files, one for the audio, and one for the video.

### Command Line

```sh
demux-webm-file --input <webm file> --output <output filename without extension>
```

### Examples

#### Bash

List options:

```sh
demux-webm-file --help
```

Extract the audio and video streams from `./assets/mov/big-buck-bunny_trailer_vp8_vorbis.webm` and save to `./output/demux_webm_file/big-buck-bunny_trailer_vp8_vorbis.aud.webm` and `./output/demux_webm_file/big-buck-bunny_trailer_vp8_vorbis.vid.webm`:

```sh
mkdir -p ./output/demux_webm_file

demux-webm-file \
    --input ./assets/mov/big-buck-bunny_trailer_vp8_vorbis.webm \
    --output ./output/demux_webm_file/big-buck-bunny_trailer_vp8_vorbis
```

#### PowerShell

List options:

```powershell
demux-webm-file --help
```

Extract the audio and video streams from `./assets/mov/big-buck-bunny_trailer_vp8_vorbis.webm` and save to `./output/demux_webm_file/big-buck-bunny_trailer_vp8_vorbis.aud.webm` and `./output/demux_webm_file/big-buck-bunny_trailer_vp8_vorbis.vid.webm`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/demux_webm_file

demux-webm-file `
    --input ./assets/mov/big-buck-bunny_trailer_vp8_vorbis.webm `
    --output ./output/demux_webm_file/big-buck-bunny_trailer_vp8_vorbis
```

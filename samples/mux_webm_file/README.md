## mux_webm_file

Shows how to multiplex Vorbis audio file and VP8 video file into a WebM file.

### Command Line

```sh
mux-webm-file --audio <Vorbis_file>.webm --video <VP8_file>.webm --output <output>.webm
```

### Examples

#### Bash

List options:

```sh
mux-webm-file --help
```

Multiplex the WebM files `./assets/aud/big-buck-bunny_trailer_vp8_vorbis.aud.webm` and `./assets/vid/big-buck-bunny_trailer_vp8_vorbis.vid.webm` into a WebM file `big-buck-bunny_trailer.webm`:

```sh
mkdir -p ./output/mux_webm_file

mux-webm-file \
    --audio ./assets/aud/big-buck-bunny_trailer_vp8_vorbis.aud.webm \
    --video ./assets/vid/big-buck-bunny_trailer_vp8_vorbis.vid.webm \
    --output ./output/mux_webm_file/big-buck-bunny_trailer.webm
```

#### PowerShell

List options:

```powershell
mux-webm-file --help
```

Multiplex the WebM files `./assets/aud/big-buck-bunny_trailer_vp8_vorbis.aud.webm` and `./assets/vid/big-buck-bunny_trailer_vp8_vorbis.vid.webm` into a WebM file `big-buck-bunny_trailer.webm`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/mux_webm_file

mux-webm-file `
    --audio ./assets/aud/big-buck-bunny_trailer_vp8_vorbis.aud.webm `
    --video ./assets/vid/big-buck-bunny_trailer_vp8_vorbis.vid.webm `
    --output ./output/mux_webm_file/big-buck-bunny_trailer.webm
```

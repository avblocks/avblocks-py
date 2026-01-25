## enc_preset_file

Shows how to convert a raw YUV video file and to a compressed video file. The format of the output is configured with an AVBlocks preset.

### Command Line

```sh
enc-preset-file --frame <width>x<height> --rate <fps> --color <COLOR> --input <file> --output <filename_without_extension> [--preset <PRESET>] [--colors] [--presets]
```

### Examples

#### Bash

List options:

```sh
enc-preset-file --help
```

List supported color spaces for input:

```sh
enc-preset-file --colors
```

List supported presets:

```sh
enc-preset-file --presets
```

Encode a raw YUV video from `./assets/vid/foreman_qcif.yuv` to a H.264 video in an MP4 container in `./output/enc_preset_file/foreman_qcif.mp4`:

```sh
mkdir -p ./output/enc_preset_file

enc-preset-file \
    --input ./assets/vid/foreman_qcif.yuv \
    --frame 176x144 --rate 30 --color yuv420 \
    --output ./output/enc_preset_file/foreman_qcif \
    --preset ipad.mp4.h264.720p
```

#### PowerShell

List options:

```powershell
enc-preset-file --help
```

List supported color spaces for input:

```powershell
enc-preset-file --colors
```

List supported presets:

```powershell
enc-preset-file --presets
```

Encode a raw YUV video from `./assets/vid/foreman_qcif.yuv` to a H.264 video in an MP4 container in `./output/enc_preset_file/foreman_qcif.mp4`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_preset_file

enc-preset-file `
    --input ./assets/vid/foreman_qcif.yuv `
    --frame 176x144 --rate 30 --color yuv420 `
    --output ./output/enc_preset_file/foreman_qcif `
    --preset ipad.mp4.h264.720p
```

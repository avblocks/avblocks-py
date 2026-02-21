## enc_hevc_file

How to convert a raw YUV video file to a compressed H.265 / HEVC video file.

### Command Line

```sh
enc-hevc-file --frame <width>x<height> --rate <fps> --color <color> --input <file.yuv> --output <file.h265> [--colors]
```

### Examples

#### Bash

List options:

```sh
enc-hevc-file --help
```

List supported color formats:

```sh
enc-hevc-file --colors
```

Encode a raw YUV video from `./assets/vid/foreman_qcif.yuv` to a H.265 video in `./output/enc_hevc_file/foreman_qcif.h265`:

```sh
mkdir -p ./output/enc_hevc_file

enc-hevc-file \
    --input ./assets/vid/foreman_qcif.yuv \
    --output ./output/enc_hevc_file/foreman_qcif.h265 \
    --frame 176x144 \
    --rate 30 \
    --color yuv420
```

#### PowerShell

List options:

```powershell
enc-hevc-file --help
```

List supported color formats:

```powershell
enc-hevc-file --colors
```

Encode a raw YUV video from `./assets/vid/foreman_qcif.yuv` to a H.265 video in `./output/enc_hevc_file/foreman_qcif.h265`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_hevc_file

enc-hevc-file `
    --input ./assets/vid/foreman_qcif.yuv `
    --output ./output/enc_hevc_file/foreman_qcif.h265 `
    --frame 176x144 `
    --rate 30 `
    --color yuv420
```

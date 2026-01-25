## enc_avc_pull

Encode raw YUV video file to AVC / H.264 Annex B video file using `Transcoder.Pull`.

### Command Line

```sh
enc-avc-pull --frame <width>x<height> --rate <fps> --color <COLOR> --input <file.yuv> --output <file.h264> [--colors]
```

### Examples

#### Bash

List options:

```sh
enc-avc-pull --help
```

List supported color spaces:

```sh
enc-avc-pull --colors
```

Encode a raw YUV video from `./assets/vid/foreman_qcif.yuv` to a H.264 video in `./output/enc_avc_pull/foreman_qcif.h264`:

```sh
mkdir -p ./output/enc_avc_pull

enc-avc-pull \
    --input ./assets/vid/foreman_qcif.yuv \
    --output ./output/enc_avc_pull/foreman_qcif.h264 \
    --frame 176x144 \
    --rate 30 \
    --color yuv420
```

#### PowerShell

List options:

```powershell
enc-avc-pull --help
```

List supported color spaces:

```powershell
enc-avc-pull --colors
```

Encode a raw YUV video from `./assets/vid/foreman_qcif.yuv` to a H.264 video in `./output/enc_avc_pull/foreman_qcif.h264`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_avc_pull

enc-avc-pull `
    --input ./assets/vid/foreman_qcif.yuv `
    --output ./output/enc_avc_pull/foreman_qcif.h264 `
    --frame 176x144 `
    --rate 30 `
    --color yuv420
```

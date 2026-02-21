## enc_hevc_pull

Encode raw YUV video file to HEVC / H.265 Annex B video file using `Transcoder.Pull`.

### Command Line

```sh
enc-hevc-pull --frame <width>x<height> --rate <fps> --color <color> --input <file.yuv> --output <file.h265> [--colors]
```

### Examples

#### Bash

List options:

```sh
enc-hevc-pull --help
```

List supported color formats:

```sh
enc-hevc-pull --colors
```

Encode a raw YUV video from `./assets/vid/foreman_qcif.yuv` to a H.265 video in `./output/enc_hevc_pull/foreman_qcif.h265`:

```sh
mkdir -p ./output/enc_hevc_pull

enc-hevc-pull \
    --input ./assets/vid/foreman_qcif.yuv \
    --output ./output/enc_hevc_pull/foreman_qcif.h265 \
    --frame 176x144 \
    --rate 30 \
    --color yuv420
```

#### PowerShell

List options:

```powershell
enc-hevc-pull --help
```

List supported color formats:

```powershell
enc-hevc-pull --colors
```

Encode a raw YUV video from `./assets/vid/foreman_qcif.yuv` to a H.265 video in `./output/enc_hevc_pull/foreman_qcif.h265`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_hevc_pull

enc-hevc-pull `
    --input ./assets/vid/foreman_qcif.yuv `
    --output ./output/enc_hevc_pull/foreman_qcif.h265 `
    --frame 176x144 `
    --rate 30 `
    --color yuv420
```

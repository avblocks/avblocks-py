## dec_avc_au

How to use the `Transcoder.Push` method to decode a sequence of H.264 Access Units to YUV uncompressed file.

### Command Line

```sh
dec-avc-au --input <directory> --output <file.yuv> [--color <COLOR>]
```

### Examples

#### Bash

List options:

```sh
dec-avc-au --help
```

List supported color formats:

```sh
dec-avc-au --colors
```

Decode the H.264 Access Units from `./assets/vid/foreman_qcif.h264.au/` into output file `./output/dec_avc_au/foreman_qcif.yuv`:

```sh
mkdir -p ./output/dec_avc_au

dec-avc-au \
    --input ./assets/vid/foreman_qcif.h264.au \
    --output ./output/dec_avc_au/foreman_qcif.yuv \
    --color yuv420
```

#### PowerShell

List options:

```powershell
dec-avc-au --help
```

List supported color formats:

```powershell
dec-avc-au --colors
```

Decode the H.264 Access Units from `./assets/vid/foreman_qcif.h264.au/` into output file `./output/dec_avc_au/foreman_qcif.yuv`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dec_avc_au

dec-avc-au `
    --input ./assets/vid/foreman_qcif.h264.au `
    --output ./output/dec_avc_au/foreman_qcif.yuv `
    --color yuv420
```

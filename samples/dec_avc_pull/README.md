## dec_avc_pull

How to use the `Transcoder.Pull` method to decode AVC / H.264 compressed file to YUV uncompressed file.

### Command Line

```sh
dec-avc-pull --input <file.h264> --output <file.yuv>
```

### Examples

#### Bash

List options:

```sh
dec-avc-pull --help
```

Decode the input file `./assets/vid/foreman_qcif.h264` into output file `./output/dec_avc_pull/foreman_qcif.yuv`:

```sh
mkdir -p ./output/dec_avc_pull

dec-avc-pull \
    --input ./assets/vid/foreman_qcif.h264 \
    --output ./output/dec_avc_pull/foreman_qcif.yuv
```

#### PowerShell

List options:

```powershell
dec-avc-pull --help
```

Decode the input file `./assets/vid/foreman_qcif.h264` into output file `./output/dec_avc_pull/foreman_qcif.yuv`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dec_avc_pull

dec-avc-pull `
    --input ./assets/vid/foreman_qcif.h264 `
    --output ./output/dec_avc_pull/foreman_qcif.yuv
```

## dec_avc_file

How to use the `Transcoder.Run` method to decode AVC / H.264 compressed file to YUV uncompressed file.

### Command Line

```sh
dec-avc-file --input <file.h264> --output <file.yuv>
```

### Examples

#### Bash

List options:

```sh
dec-avc-file --help
```

Decode the input file `./assets/vid/foreman_qcif.h264` into output file `./output/dec_avc_file/foreman_qcif.yuv`:

```sh
mkdir -p ./output/dec_avc_file

dec-avc-file \
    --input ./assets/vid/foreman_qcif.h264 \
    --output ./output/dec_avc_file/foreman_qcif.yuv
```

#### PowerShell

List options:

```powershell
dec-avc-file --help
```

Decode the input file `./assets/vid/foreman_qcif.h264` into output file `./output/dec_avc_file/foreman_qcif.yuv`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dec_avc_file

dec-avc-file `
    --input ./assets/vid/foreman_qcif.h264 `
    --output ./output/dec_avc_file/foreman_qcif.yuv
```

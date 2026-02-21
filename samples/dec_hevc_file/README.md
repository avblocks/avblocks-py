## dec_hevc_file

How to use the `Transcoder.Run` method to decode an H.265 / HEVC file to YUV uncompressed file.

### Command Line

```sh
dec-hevc-file --input <file.h265> --output <file.yuv>
```

### Examples

#### Bash

List options:

```sh
dec-hevc-file --help
```

Decode the input file `./assets/vid/foreman_qcif.h265` into output file `./output/dec_hevc_file/foreman_qcif.yuv`:

```sh
mkdir -p ./output/dec_hevc_file

dec-hevc-file \
    --input ./assets/vid/foreman_qcif.h265 \
    --output ./output/dec_hevc_file/foreman_qcif.yuv
```

#### PowerShell

List options:

```powershell
dec-hevc-file --help
```

Decode the input file `./assets/vid/foreman_qcif.h265` into output file `./output/dec_hevc_file/foreman_qcif.yuv`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dec_hevc_file

dec-hevc-file `
    --input ./assets/vid/foreman_qcif.h265 `
    --output ./output/dec_hevc_file/foreman_qcif.yuv
```

## dec_vp8_file

Decode VP8/IVF file and save output to raw YUV file.

### Command Line

```sh
dec-vp8-file --input <ivf file> --output <yuv file>
```

### Examples

#### Bash

List options:

```sh
dec-vp8-file --help
```

Decode the input file `./assets/vid/foreman_qcif_vp8.ivf` into output file `./output/dec_vp8_file/foreman_qcif.yuv`:

```sh
mkdir -p ./output/dec_vp8_file

dec-vp8-file \
    --input ./assets/vid/foreman_qcif_vp8.ivf \
    --output ./output/dec_vp8_file/foreman_qcif.yuv
```

#### PowerShell

List options:

```powershell
dec-vp8-file --help
```

Decode the input file `./assets/vid/foreman_qcif_vp8.ivf` into output file `./output/dec_vp8_file/foreman_qcif.yuv`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dec_vp8_file

dec-vp8-file `
    --input ./assets/vid/foreman_qcif_vp8.ivf `
    --output ./output/dec_vp8_file/foreman_qcif.yuv
```

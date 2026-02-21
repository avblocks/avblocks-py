## dec_vp9_file

Decode VP9/IVF file and save output to raw YUV file.

### Command Line

```sh
dec-vp9-file --input <ivf file> --output <yuv file>
```

### Examples

#### Bash

List options:

```sh
dec-vp9-file --help
```

Decode the input file `./assets/vid/foreman_qcif_vp9.ivf` into output file `./output/dec_vp9_file/foreman_qcif.yuv`:

```sh
mkdir -p ./output/dec_vp9_file

dec-vp9-file \
    --input ./assets/vid/foreman_qcif_vp9.ivf \
    --output ./output/dec_vp9_file/foreman_qcif.yuv
```

#### PowerShell

List options:

```powershell
dec-vp9-file --help
```

Decode the input file `./assets/vid/foreman_qcif_vp9.ivf` into output file `./output/dec_vp9_file/foreman_qcif.yuv`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dec_vp9_file

dec-vp9-file `
    --input ./assets/vid/foreman_qcif_vp9.ivf `
    --output ./output/dec_vp9_file/foreman_qcif.yuv
```

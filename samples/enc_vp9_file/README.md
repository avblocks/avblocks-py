## enc_vp9_file

How to convert a raw YUV video file to a compressed VP9/IVF video file.

### Command Line

```sh
enc-vp9-file --frame <width>x<height> --rate <fps> --color <color> --input <file.yuv> --output <file.ivf> [--colors]
```

### Examples

#### Bash

List options:

```sh
enc-vp9-file --help
```

List supported color formats:

```sh
enc-vp9-file --colors
```

Encode the input file `./assets/vid/foreman_qcif.yuv` into output file `./output/enc_vp9_file/foreman_qcif.ivf`:

```sh
mkdir -p ./output/enc_vp9_file

enc-vp9-file \
    --input ./assets/vid/foreman_qcif.yuv \
    --output ./output/enc_vp9_file/foreman_qcif.ivf \
    --frame 176x144 \
    --rate 30 \
    --color yuv420
```

#### PowerShell

List options:

```powershell
enc-vp9-file --help
```

List supported color formats:

```powershell
enc-vp9-file --colors
```

Encode the input file `./assets/vid/foreman_qcif.yuv` into output file `./output/enc_vp9_file/foreman_qcif.ivf`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_vp9_file

enc-vp9-file `
    --input ./assets/vid/foreman_qcif.yuv `
    --output ./output/enc_vp9_file/foreman_qcif.ivf `
    --frame 176x144 `
    --rate 30 `
    --color yuv420
```

## enc_avc_push

How to encode a raw YUV video file to an H.264/AVC Annex B video file using `Transcoder.push`. A reader transcoder pulls the raw frames and an encoder transcoder takes them with push.

### Command Line

```sh
enc-avc-push --frame <width>x<height> --rate <fps> --color <color> --input <file.yuv> --output <file.h264> [--colors]
```

### Examples

#### Bash

List options:

```sh
enc-avc-push --help
Usage: enc-avc-push [OPTIONS]

  Encode YUV file to H.264/AVC using push mode.

Options:
  -i, --input PATH   input YUV file
  -o, --output PATH  output H264 file
  -r, --rate FLOAT   input frame rate
  -f, --frame TEXT   input frame sizes <width>x<height>
  -c, --color TEXT   input color format. Use --colors to list all supported
                     color formats
  --colors           list COLOR constants
  --help             Show this message and exit.
```

List supported color formats for input:

```sh
enc-avc-push --colors

COLORS
---------
yv12                 Planar Y, V, U (4:2:0) (note V,U order!)
nv12                 Planar Y, merged U->V (4:2:0)
yuy2                 Composite Y->U->Y->V (4:2:2)
uyvy                 Composite U->Y->V->Y (4:2:2)
yuv411               Planar Y, U, V (4:1:1)
yuv420               Planar Y, U, V (4:2:0)
yuv422               Planar Y, U, V (4:2:2)
yuv444               Planar Y, U, V (4:4:4)
y411                 Composite Y, U, V (4:1:1)
y41p                 Composite Y, U, V (4:1:1)
bgr32                Composite B->G->R
bgra32               Composite B->G->R->A
bgr24                Composite B->G->R
bgr565               Composite B->G->R, 5 bit per B & R, 6 bit per G
bgr555               Composite B->G->R->A, 5 bit per component, 1 bit per A
bgr444               Composite B->G->R->A, 4 bit per component
gray                 Luminance component only
yuv420a              Planar Y, U, V, Alpha (4:2:0)
yuv422a              Planar Y, U, V, Alpha (4:2:2)
yuv444a              Planar Y, U, V, Alpha (4:4:4)
yvu9                 Planar Y, V, U, 9 bits per sample
```

Encode the input file `./assets/vid/foreman_qcif.yuv` into output file `./output/enc_avc_push/foreman_qcif.h264`:

```sh
mkdir -p ./output/enc_avc_push

enc-avc-push \
    --input ./assets/vid/foreman_qcif.yuv \
    --output ./output/enc_avc_push/foreman_qcif.h264 \
    --frame 176x144 --rate 30 --color yuv420
```

#### PowerShell

List options:

```powershell
enc-avc-push --help
```

List supported color formats for input:

```powershell
enc-avc-push --colors
```

Encode the input file `./assets/vid/foreman_qcif.yuv` into output file `./output/enc_avc_push/foreman_qcif.h264`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_avc_push

enc-avc-push `
    --input ./assets/vid/foreman_qcif.yuv `
    --output ./output/enc_avc_push/foreman_qcif.h264 `
    --frame 176x144 --rate 30 --color yuv420
```

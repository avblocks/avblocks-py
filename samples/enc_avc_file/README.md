## enc_avc_file

How to convert a raw YUV video file to a compressed H.264 video file.   

### Command Line

```sh
enc-avc-file --frame <width>x<height> --rate <fps> --color <color> --input <file.yuv> --output <file.h264> [--colors]
```

### Examples

List options:

```sh
enc-avc-file --help
```

List supported color spaces for input:

```sh
enc-avc-file --colors
```

Encode the input file `./assets/vid/foreman_qcif.yuv` into output file `./output/enc_avc_file/foreman_qcif.h264`:

```sh
mkdir -p ./output/enc_avc_file

enc-avc-file \
    --input ./assets/vid/foreman_qcif.yuv \
    --output ./output/enc_avc_file/foreman_qcif.h264 \
    --frame 176x144 --rate 30 --color yuv420
```

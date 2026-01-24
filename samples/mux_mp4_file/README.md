## mux_mp4_file

Shows how to multiplex AAC audio file and AVC / H.264 video file into a MP4 file.

### Command Line

```sh
mux-mp4-file --audio <AAC_file>.mp4 --video <H264_file>.mp4 --output <output>.mp4
```

### Examples

List options:

```sh
mux-mp4-file --help
```

Multiplex the MP4 files `./assets/aud/big_buck_bunny_trailer.aud.mp4` and `./assets/vid/big_buck_bunny_trailer.vid.mp4` into a MP4 file `mux_mp4_file.mp4`:

```sh
mkdir -p ./output/mux_mp4_file

mux-mp4-file \
    --audio ./assets/aud/big_buck_bunny_trailer.aud.mp4 \
    --video ./assets/vid/big_buck_bunny_trailer.vid.mp4 \
    --output ./output/mux_mp4_file/big_buck_bunny_trailer.mp4
```

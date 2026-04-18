## video_pad

Add black border padding around a video.

### Command Line

```sh
video-pad [--left <pixels>] [--right <pixels>] [--top <pixels>] [--bottom <pixels>] [--color <ARGB32>] [--width <pixels>] [--height <pixels>] --input <input.mp4> --output <output.mp4>
```

### Examples

#### Linux/macOS

List options:

```sh
video-pad --help
```

Add 100 pixels of black padding on all sides of `./assets/vid/big_buck_bunny_trailer.vid.mp4` and save to `./output/video_pad/big_buck_bunny_padded.mp4`:

```sh
mkdir -p ./output/video_pad

video-pad \
    --input ./assets/vid/big_buck_bunny_trailer.vid.mp4 \
    --output ./output/video_pad/big_buck_bunny_padded.mp4 \
    --left 100 \
    --right 100 \
    --top 100 \
    --bottom 100
```

#### Windows (PowerShell)

List options:

```powershell
video-pad --help
```

Add 100 pixels of black padding on all sides of `./assets/vid/big_buck_bunny_trailer.vid.mp4` and save to `./output/video_pad/big_buck_bunny_padded.mp4`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/video_pad

video-pad `
    --input ./assets/vid/big_buck_bunny_trailer.vid.mp4 `
    --output ./output/video_pad/big_buck_bunny_padded.mp4 `
    --left 100 `
    --right 100 `
    --top 100 `
    --bottom 100
```

### Notes

- When `--width` and `--height` are not specified (or set to 0), the output frame dimensions are computed automatically as input dimensions plus the padding on each side.
- The padding color is specified in ARGB32 format (e.g. `0xFF000000` for opaque black).

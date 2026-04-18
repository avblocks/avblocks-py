## video_upscale

Upscale a video to Full HD (1920x1080) using bicubic interpolation.

### Command Line

```sh
video-upscale [--width <pixels>] [--height <pixels>] --input <input.mp4> --output <output.mp4>
```

### Examples

#### Linux/macOS

List options:

```sh
video-upscale --help
```

Upscale `./assets/vid/big_buck_bunny_trailer.vid.mp4` to 1920x1080 and save to `./output/video_upscale/big_buck_bunny_1080p.mp4`:

```sh
mkdir -p ./output/video_upscale

video-upscale \
    --input ./assets/vid/big_buck_bunny_trailer.vid.mp4 \
    --output ./output/video_upscale/big_buck_bunny_1080p.mp4 \
    --width 1920 \
    --height 1080
```

#### Windows (PowerShell)

List options:

```powershell
video-upscale --help
```

Upscale `./assets/vid/big_buck_bunny_trailer.vid.mp4` to 1920x1080 and save to `./output/video_upscale/big_buck_bunny_1080p.mp4`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/video_upscale

video-upscale `
    --input ./assets/vid/big_buck_bunny_trailer.vid.mp4 `
    --output ./output/video_upscale/big_buck_bunny_1080p.mp4 `
    --width 1920 `
    --height 1080
```

### Notes

- Bicubic (`InterpolationMethod.Cubic`) is used for best upscaling quality.

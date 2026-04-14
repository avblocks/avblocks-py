## video_crop

Crop a video by removing pixels from the edges.

### Command Line

```sh
video-crop [--crop-left <pixels>] [--crop-right <pixels>] [--crop-top <pixels>] [--crop-bottom <pixels>] --input <input.mp4> --output <output.mp4>
```

### Examples

#### Linux/macOS

List options:

```sh
video-crop --help
```

Crop `./assets/vid/big_buck_bunny_trailer.vid.mp4` from 16:9 (480×270) to 4:3 (360×270) by removing 60 pixels from each side and save to `./output/video_crop/cropped.mp4`:

```sh
mkdir -p ./output/video_crop

video-crop \
    --input ./assets/vid/big_buck_bunny_trailer.vid.mp4 \
    --output ./output/video_crop/cropped.mp4 \
    --crop-left 60 \
    --crop-right 60
```

#### Windows (PowerShell)

List options:

```powershell
video-crop --help
```

Crop `./assets/vid/big_buck_bunny_trailer.vid.mp4` from 16:9 (480×270) to 4:3 (360×270) by removing 60 pixels from each side and save to `./output/video_crop/cropped.mp4`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/video_crop

video-crop `
    --input ./assets/vid/big_buck_bunny_trailer.vid.mp4 `
    --output ./output/video_crop/cropped.mp4 `
    --crop-left 60 `
    --crop-right 60
```

### Notes

- Crop values should ideally be even numbers for proper alignment with video codec block sizes.
- The output frame dimensions and display ratio are updated automatically to reflect the crop.

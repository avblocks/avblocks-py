## video_framerate

Change the frame rate of a video.

### Command Line

```sh
video-framerate [--frame-rate <fps>] --input <input.mp4> --output <output.mp4>
```

### Examples

#### Linux/macOS

List options:

```sh
video-framerate --help
```

Change the frame rate of `./assets/vid/big_buck_bunny_trailer.vid.mp4` to 30 fps and save to `./output/video_framerate/big_buck_bunny_30fps.mp4`:

```sh
mkdir -p ./output/video_framerate

video-framerate \
    --input ./assets/vid/big_buck_bunny_trailer.vid.mp4 \
    --output ./output/video_framerate/big_buck_bunny_30fps.mp4 \
    --frame-rate 30.0
```

#### Windows (PowerShell)

List options:

```powershell
video-framerate --help
```

Change the frame rate of `./assets/vid/big_buck_bunny_trailer.vid.mp4` to 30 fps and save to `./output/video_framerate/big_buck_bunny_30fps.mp4`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/video_framerate

video-framerate `
    --input ./assets/vid/big_buck_bunny_trailer.vid.mp4 `
    --output ./output/video_framerate/big_buck_bunny_30fps.mp4 `
    --frame-rate 30.0
```

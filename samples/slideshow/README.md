## slideshow

Shows how to make a video clip from a sequence of images. The input is a series of JPEG images. The output is configured with an AVBlocks preset.

### Command Line

```sh
slideshow --input <directory> --output <filename_without_extension> --preset <preset_id>
```

### Examples

#### Bash

List options:

```sh
slideshow --help
```

List supported presets:

```sh
slideshow --presets
```

Create an MP4 / H.264 clip from a sequence of images in the `./assets/img` folder using the `mp4.h264.aac` preset:

```sh
mkdir -p ./output/slideshow

slideshow \
    --input ./assets/img \
    --output ./output/slideshow/cube \
    --preset mp4.h264.aac
```

#### PowerShell

List options:

```powershell
slideshow --help
```

List supported presets:

```powershell
slideshow --presets
```

Create an MP4 / H.264 clip from a sequence of images in the `./assets/img` folder using the `mp4.h264.aac` preset:

```powershell
New-Item -ItemType Directory -Force -Path ./output/slideshow

slideshow `
    --input ./assets/img `
    --output ./output/slideshow/cube `
    --preset mp4.h264.aac
```

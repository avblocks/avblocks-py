## re_encode

Takes an MP4 input and re-encodes the audio and video streams back into MP4 output. It shows how to force encoding of individual streams even when it is not needed.

### Command Line

```sh
re-encode [--audio] [--video] --input <mp4_file.mp4> --output <mp4_file.mp4> 
```

### Examples

#### Bash

List options:

```sh
re-encode --help
```

Re-encode the `./assets/mov/big_buck_bunny_trailer.mp4` file. Only the video stream will be re-encoded, the audio stream will be copied as is:

```sh
mkdir -p ./output/re_encode

re-encode \
    --video \
    --input ./assets/mov/big_buck_bunny_trailer.mp4 \
    --output ./output/re_encode/big_buck_bunny_trailer.mp4
```

#### PowerShell

List options:

```powershell
re-encode --help
```

Re-encode the `./assets/mov/big_buck_bunny_trailer.mp4` file. Only the video stream will be re-encoded, the audio stream will be copied as is:

```powershell
New-Item -ItemType Directory -Force -Path ./output/re_encode

re-encode `
    --video `
    --input ./assets/mov/big_buck_bunny_trailer.mp4 `
    --output ./output/re_encode/big_buck_bunny_trailer.mp4
```

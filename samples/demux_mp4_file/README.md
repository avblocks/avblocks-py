## demux_mp4_file

Shows how to extract the audio and video streams from MP4 file and save to two separate MP4 files, one for the audio, and one for the video.

### Command Line

```sh
demux-mp4-file --input <input_mp4_file> --output <output_mp4_filename_without_extension>
```

### Examples

#### Bash

List options:

```sh
demux-mp4-file --help
```

Extract the audio and video streams from `./assets/mov/big_buck_bunny_trailer.mp4` and save to `./output/demux_mp4_file/big_buck_bunny_trailer.aud.mp4` and `./output/demux_mp4_file/big_buck_bunny_trailer.vid.mp4`:

```sh
mkdir -p ./output/demux_mp4_file

demux-mp4-file \
    --input ./assets/mov/big_buck_bunny_trailer.mp4 \
    --output ./output/demux_mp4_file/big_buck_bunny_trailer
```

#### PowerShell

List options:

```powershell
demux-mp4-file --help
```

Extract the audio and video streams from `./assets/mov/big_buck_bunny_trailer.mp4` and save to `./output/demux_mp4_file/big_buck_bunny_trailer.aud.mp4` and `./output/demux_mp4_file/big_buck_bunny_trailer.vid.mp4`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/demux_mp4_file

demux-mp4-file `
    --input ./assets/mov/big_buck_bunny_trailer.mp4 `
    --output ./output/demux_mp4_file/big_buck_bunny_trailer
```

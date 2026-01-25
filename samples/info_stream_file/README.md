## info_stream_file

How to use the MediaInfo API to extract audio / video stream information from a media file.

### Command Line

```sh
info-stream-file --input <any_media_file>
```

### Examples

#### Bash

List options:

```sh
info-stream-file --help
```

List the audio and video streams of the `./assets/mov/big_buck_bunny_trailer.mp4` movie trailer:

```sh
info-stream-file \
    --input ./assets/mov/big_buck_bunny_trailer.mp4
```

#### PowerShell

List options:

```powershell
info-stream-file --help
```

List the audio and video streams of the `./assets/mov/big_buck_bunny_trailer.mp4` movie trailer:

```powershell
info-stream-file `
    --input ./assets/mov/big_buck_bunny_trailer.mp4
```

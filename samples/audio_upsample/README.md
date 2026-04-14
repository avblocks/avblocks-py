## audio_upsample

How to upsample audio from 44.1 KHz to 48 KHz.

### Command Line

```sh
audio-upsample --input <mp3 file> --output <mp3 file>
```

### Examples

#### Bash

List options:

```sh
audio-upsample --help
```

Upsample the input file `./assets/aud/Hydrate-Kenny_Beltrey.mp3` into output file `./output/audio_upsample/Hydrate-Kenny_Beltrey-48khz.mp3`:

```sh
mkdir -p ./output/audio_upsample

audio-upsample \
    --input ./assets/aud/Hydrate-Kenny_Beltrey.mp3 \
    --output ./output/audio_upsample/Hydrate-Kenny_Beltrey-48khz.mp3
```

#### PowerShell

List options:

```powershell
audio-upsample --help
```

Upsample the input file `./assets/aud/Hydrate-Kenny_Beltrey.mp3` into output file `./output/audio_upsample/Hydrate-Kenny_Beltrey-48khz.mp3`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/audio_upsample

audio-upsample `
    --input ./assets/aud/Hydrate-Kenny_Beltrey.mp3 `
    --output ./output/audio_upsample/Hydrate-Kenny_Beltrey-48khz.mp3
```

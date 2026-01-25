## enc_mp3_push

Encode WAV file to MP3 file using `Transcoder.Push`.

### Command Line

```sh
enc-mp3-push --input <wav file> --output <mp3 file>
```

### Examples

#### Bash

List options:

```sh
enc-mp3-push --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_mp3_push/equinox-48KHz.mp3`:

```sh
mkdir -p ./output/enc_mp3_push

enc-mp3-push \
    --input ./assets/aud/equinox-48KHz.wav \
    --output ./output/enc_mp3_push/equinox-48KHz.mp3
```

#### PowerShell

List options:

```powershell
enc-mp3-push --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_mp3_push/equinox-48KHz.mp3`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_mp3_push

enc-mp3-push `
    --input ./assets/aud/equinox-48KHz.wav `
    --output ./output/enc_mp3_push/equinox-48KHz.mp3
```

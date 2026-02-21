## enc_opus_file

How to encode WAV file to Opus OGG file.

### Command Line

```sh
enc-opus-file --input <wav file> --output <opus file>
```

### Examples

#### Bash

List options:

```sh
enc-opus-file --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_opus_file/equinox-48KHz.opus`:

```sh
mkdir -p ./output/enc_opus_file

enc-opus-file \
    --input ./assets/aud/equinox-48KHz.wav \
    --output ./output/enc_opus_file/equinox-48KHz.opus
```

#### PowerShell

List options:

```powershell
enc-opus-file --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_opus_file/equinox-48KHz.opus`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_opus_file

enc-opus-file `
    --input ./assets/aud/equinox-48KHz.wav `
    --output ./output/enc_opus_file/equinox-48KHz.opus
```

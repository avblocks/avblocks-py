## enc_vorbis_file

How to encode WAV file to Vorbis OGG file.

### Command Line

```sh
enc-vorbis-file --input <wav file> --output <ogg file>
```

### Examples

#### Bash

List options:

```sh
enc-vorbis-file --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_vorbis_file/equinox-48KHz.ogg`:

```sh
mkdir -p ./output/enc_vorbis_file

enc-vorbis-file \
    --input ./assets/aud/equinox-48KHz.wav \
    --output ./output/enc_vorbis_file/equinox-48KHz.ogg
```

#### PowerShell

List options:

```powershell
enc-vorbis-file --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_vorbis_file/equinox-48KHz.ogg`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_vorbis_file

enc-vorbis-file `
    --input ./assets/aud/equinox-48KHz.wav `
    --output ./output/enc_vorbis_file/equinox-48KHz.ogg
```

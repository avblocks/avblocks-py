## enc_aac_adts_file

How to encode WAV file to AAC file in Audio Data Transport Stream (ADTS) format.

### Command Line

```sh
enc-aac-adts-file --input <wav file> --output <aac file>
```

### Examples

#### Bash

List options:

```sh
enc-aac-adts-file --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_aac_adts_file/equinox-48KHz.adts.aac`:

```sh
mkdir -p ./output/enc_aac_adts_file

enc-aac-adts-file \
    --input ./assets/aud/equinox-48KHz.wav \
    --output ./output/enc_aac_adts_file/equinox-48KHz.adts.aac
```

#### PowerShell

List options:

```powershell
enc-aac-adts-file --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_aac_adts_file/equinox-48KHz.adts.aac`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_aac_adts_file

enc-aac-adts-file `
    --input ./assets/aud/equinox-48KHz.wav `
    --output ./output/enc_aac_adts_file/equinox-48KHz.adts.aac
```

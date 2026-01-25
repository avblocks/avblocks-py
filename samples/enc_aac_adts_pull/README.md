## enc_aac_adts_pull

Encode WAV file to AAC file in Audio Data Transport Stream (ADTS) format using `Transcoder.Pull`.

### Command Line

```sh
enc-aac-adts-pull --input <wav file> --output <aac file>
```

### Examples

#### Bash

List options:

```sh
enc-aac-adts-pull --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_aac_adts_pull/equinox-48KHz.adts.aac`:

```sh
mkdir -p ./output/enc_aac_adts_pull

enc-aac-adts-pull \
    --input ./assets/aud/equinox-48KHz.wav \
    --output ./output/enc_aac_adts_pull/equinox-48KHz.adts.aac
```

#### PowerShell

List options:

```powershell
enc-aac-adts-pull --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_aac_adts_pull/equinox-48KHz.adts.aac`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_aac_adts_pull

enc-aac-adts-pull `
    --input ./assets/aud/equinox-48KHz.wav `
    --output ./output/enc_aac_adts_pull/equinox-48KHz.adts.aac
```

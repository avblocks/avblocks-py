## enc_g711_alaw_file

Encode WAV file to G.711 A-law WAV file.

### Command Line

```sh
enc-g711-alaw-file --input <wav file> --output <g711 alaw wav file>
```

### Examples

#### Bash

List options:

```sh
enc-g711-alaw-file --help
```

Encode the input file `./assets/aud/express-dictate_8000_s16_1ch_pcm.wav` into output file `./output/enc_g711_alaw_file/express-dictate_g711_alaw.wav`:

```sh
mkdir -p ./output/enc_g711_alaw_file

enc-g711-alaw-file \
    --input ./assets/aud/express-dictate_8000_s16_1ch_pcm.wav \
    --output ./output/enc_g711_alaw_file/express-dictate_g711_alaw.wav
```

#### PowerShell

List options:

```powershell
enc-g711-alaw-file --help
```

Encode the input file `./assets/aud/express-dictate_8000_s16_1ch_pcm.wav` into output file `./output/enc_g711_alaw_file/express-dictate_g711_alaw.wav`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_g711_alaw_file

enc-g711-alaw-file `
    --input ./assets/aud/express-dictate_8000_s16_1ch_pcm.wav `
    --output ./output/enc_g711_alaw_file/express-dictate_g711_alaw.wav
```

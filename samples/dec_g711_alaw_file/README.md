## dec_g711_alaw_file

Decode G.711 A-law WAV file to PCM WAV file.

### Command Line

```sh
dec-g711-alaw-file --input <g711 alaw wav file> --output <wav file>
```

### Examples

#### Bash

List options:

```sh
dec-g711-alaw-file --help
```

Decode the input file `./assets/aud/express-dictate_8000_s8_1ch_alaw.wav` into output file `./output/dec_g711_alaw_file/express-dictate_8000_s16_1ch_pcm.wav`:

```sh
mkdir -p ./output/dec_g711_alaw_file

dec-g711-alaw-file \
    --input ./assets/aud/express-dictate_8000_s8_1ch_alaw.wav \
    --output ./output/dec_g711_alaw_file/express-dictate_8000_s16_1ch_pcm.wav
```

#### PowerShell

List options:

```powershell
dec-g711-alaw-file --help
```

Decode the input file `./assets/aud/express-dictate_8000_s8_1ch_alaw.wav` into output file `./output/dec_g711_alaw_file/express-dictate_8000_s16_1ch_pcm.wav`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dec_g711_alaw_file

dec-g711-alaw-file `
    --input ./assets/aud/express-dictate_8000_s8_1ch_alaw.wav `
    --output ./output/dec_g711_alaw_file/express-dictate_8000_s16_1ch_pcm.wav
```

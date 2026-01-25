## enc_g711_ulaw_file

Encode WAV file to G.711 μ-law WAV file.

### Command Line

```sh
enc-g711-ulaw-file --input <wav file> --output <g711 ulaw wav file>
```

### Examples

#### Bash

List options:

```sh
enc-g711-ulaw-file --help
```

Encode the input file `./assets/aud/express-dictate_8000_s16_1ch_pcm.wav` into output file `./output/enc_g711_ulaw_file/express-dictate_g711_ulaw.wav`:

```sh
mkdir -p ./output/enc_g711_ulaw_file

enc-g711-ulaw-file \
    --input ./assets/aud/express-dictate_8000_s16_1ch_pcm.wav \
    --output ./output/enc_g711_ulaw_file/express-dictate_g711_ulaw.wav
```

#### PowerShell

List options:

```powershell
enc-g711-ulaw-file --help
```

Encode the input file `./assets/aud/express-dictate_8000_s16_1ch_pcm.wav` into output file `./output/enc_g711_ulaw_file/express-dictate_g711_ulaw.wav`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/enc_g711_ulaw_file

enc-g711-ulaw-file `
    --input ./assets/aud/express-dictate_8000_s16_1ch_pcm.wav `
    --output ./output/enc_g711_ulaw_file/express-dictate_g711_ulaw.wav
```

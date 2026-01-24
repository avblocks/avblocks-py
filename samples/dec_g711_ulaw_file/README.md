## dec_g711_ulaw_file

Decode G.711 μ-law WAV file to PCM WAV file.

### Command Line

```sh
dec-g711-ulaw-file --input <g711 ulaw wav file> --output <wav file>
```

### Examples

List options:

```sh
dec-g711-ulaw-file --help
```

Decode the input file `./assets/aud/express-dictate_8000_s8_1ch_ulaw.wav` into output file `./output/dec_g711_ulaw_file/express-dictate_8000_s16_1ch_pcm.wav`:

```sh
mkdir -p ./output/dec_g711_ulaw_file

dec-g711-ulaw-file \
    --input ./assets/aud/express-dictate_8000_s8_1ch_ulaw.wav \
    --output ./output/dec_g711_ulaw_file/express-dictate_8000_s16_1ch_pcm.wav
```

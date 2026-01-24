## enc_mp3_pull

Encode WAV file to MP3 file using `Transcoder.Pull`.

### Command Line

```sh
enc-mp3-pull --input <wav file> --output <mp3 file>
```

### Examples

List options:

```sh
enc-mp3-pull --help
```

Encode the input file `./assets/aud/equinox-48KHz.wav` into output file `./output/enc_mp3_pull/equinox-48KHz.mp3`:

```sh
mkdir -p ./output/enc_mp3_pull

enc-mp3-pull \
    --input ./assets/aud/equinox-48KHz.wav \
    --output ./output/enc_mp3_pull/equinox-48KHz.mp3
```

## dec_aac_adts_pull

Decode AAC file in Audio Data Transport Stream (ADTS) format using `Transcoder.Pull` and save output to WAV file.

### Command Line

```sh
dec-aac-adts-pull --input <aac file> --output <wav file>
```

### Examples

List options:

```sh
dec-aac-adts-pull --help
```

Decode the input file `./assets/aud/Hydrate-Kenny_Beltrey.adts.aac` into output file `./output/dec_aac_adts_pull/Hydrate-Kenny_Beltrey.wav`:

```sh
mkdir -p ./output/dec_aac_adts_pull

dec-aac-adts-pull \
    --input ./assets/aud/Hydrate-Kenny_Beltrey.adts.aac \
    --output ./output/dec_aac_adts_pull/Hydrate-Kenny_Beltrey.wav
```

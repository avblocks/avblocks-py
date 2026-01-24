## dec_mp3_file

Decode MP3 file and save output to WAV file.

### Command Line

```sh
dec-mp3-file --input <mp3 file> --output <wav file>
```

### Examples

List options:

```sh
dec-mp3-file --help
```

Decode the input file `./assets/aud/Hydrate-Kenny_Beltrey.mp3` into output file `./output/dec_mp3_file/Hydrate-Kenny_Beltrey.wav`:

```sh
mkdir -p ./output/dec_mp3_file

dec-mp3-file \
    --input ./assets/aud/Hydrate-Kenny_Beltrey.mp3 \
    --output ./output/dec_mp3_file/Hydrate-Kenny_Beltrey.wav
```

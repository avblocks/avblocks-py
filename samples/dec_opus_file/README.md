## dec_opus_file

Decode Opus OGG file and save output to WAV file.

### Command Line

```sh
dec-opus-file --input <opus file> --output <wav file>
```

### Examples

#### Bash

List options:

```sh
dec-opus-file --help
```

Decode the input file `./assets/aud/Everybody-TBB.opus` into output file `./output/dec_opus_file/Everybody-TBB.wav`:

```sh
mkdir -p ./output/dec_opus_file

dec-opus-file \
    --input ./assets/aud/Everybody-TBB.opus \
    --output ./output/dec_opus_file/Everybody-TBB.wav
```

#### PowerShell

List options:

```powershell
dec-opus-file --help
```

Decode the input file `./assets/aud/Everybody-TBB.opus` into output file `./output/dec_opus_file/Everybody-TBB.wav`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dec_opus_file

dec-opus-file `
    --input ./assets/aud/Everybody-TBB.opus `
    --output ./output/dec_opus_file/Everybody-TBB.wav
```

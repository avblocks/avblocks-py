## dec_vorbis_file

Decode Vorbis OGG file and save output to WAV file.

### Command Line

```sh
dec-vorbis-file --input <ogg file> --output <wav file>
```

### Examples

#### Bash

List options:

```sh
dec-vorbis-file --help
```

Decode the input file `./assets/aud/Hydrate-Kenny_Beltrey.ogg` into output file `./output/dec_vorbis_file/Hydrate-Kenny_Beltrey.wav`:

```sh
mkdir -p ./output/dec_vorbis_file

dec-vorbis-file \
    --input ./assets/aud/Hydrate-Kenny_Beltrey.ogg \
    --output ./output/dec_vorbis_file/Hydrate-Kenny_Beltrey.wav
```

#### PowerShell

List options:

```powershell
dec-vorbis-file --help
```

Decode the input file `./assets/aud/Hydrate-Kenny_Beltrey.ogg` into output file `./output/dec_vorbis_file/Hydrate-Kenny_Beltrey.wav`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dec_vorbis_file

dec-vorbis-file `
    --input ./assets/aud/Hydrate-Kenny_Beltrey.ogg `
    --output ./output/dec_vorbis_file/Hydrate-Kenny_Beltrey.wav
```

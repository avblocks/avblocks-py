## dec_aac_adts_file

Decode AAC file in Audio Data Transport Stream (ADTS) format and save output to WAV file.

### Command Line

```sh
dec-aac-adts-file --input <aac file> --output <wav file>
```

### Examples

#### Bash

List options:

```sh
dec-aac-adts-file --help
```

Decode the input file `./assets/aud/Hydrate-Kenny_Beltrey.adts.aac` into output file `./output/dec_aac_adts_file/Hydrate-Kenny_Beltrey.wav`:

```sh
mkdir -p ./output/dec_aac_adts_file

dec-aac-adts-file \
    --input ./assets/aud/Hydrate-Kenny_Beltrey.adts.aac \
    --output ./output/dec_aac_adts_file/Hydrate-Kenny_Beltrey.wav
```

#### PowerShell

List options:

```powershell
dec-aac-adts-file --help
```

Decode the input file `./assets/aud/Hydrate-Kenny_Beltrey.adts.aac` into output file `./output/dec_aac_adts_file/Hydrate-Kenny_Beltrey.wav`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dec_aac_adts_file

dec-aac-adts-file `
    --input ./assets/aud/Hydrate-Kenny_Beltrey.adts.aac `
    --output ./output/dec_aac_adts_file/Hydrate-Kenny_Beltrey.wav
```

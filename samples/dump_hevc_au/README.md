## dump_hevc_au

How to split an H.265/HEVC elementary stream into Access Units and dump each Access Unit to a separate file, while also parsing and printing the NAL units within each Access Unit.

### Command Line

```sh
dump-hevc-au --input <h265 file> --output <folder>
```

### Examples

#### Bash

List options:

```sh
dump-hevc-au --help
```

Parse the H.265 file `./assets/vid/foreman_qcif.h265` and dump Access Units to `./output/dump_hevc_au/`:

```sh
mkdir -p ./output/dump_hevc_au

dump-hevc-au \
    --input ./assets/vid/foreman_qcif.h265 \
    --output ./output/dump_hevc_au
```

#### PowerShell

List options:

```powershell
dump-hevc-au --help
```

Parse the H.265 file `./assets/vid/foreman_qcif.h265` and dump Access Units to `./output/dump_hevc_au/`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dump_hevc_au

dump-hevc-au `
    --input ./assets/vid/foreman_qcif.h265 `
    --output ./output/dump_hevc_au
```

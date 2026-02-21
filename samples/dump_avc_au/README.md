## dump_avc_au

How to split an H.264/AVC elementary stream into Access Units and dump each Access Unit to a separate file, while also parsing and printing the NAL units within each Access Unit.

### Command Line

```sh
dump-avc-au --input <h264 file> --output <folder>
```

### Examples

#### Bash

List options:

```sh
dump-avc-au --help
```

Parse the H.264 file `./assets/vid/foreman_qcif.h264` and dump Access Units to `./output/dump_avc_au/`:

```sh
mkdir -p ./output/dump_avc_au

dump-avc-au \
    --input ./assets/vid/foreman_qcif.h264 \
    --output ./output/dump_avc_au
```

#### PowerShell

List options:

```powershell
dump-avc-au --help
```

Parse the H.264 file `./assets/vid/foreman_qcif.h264` and dump Access Units to `./output/dump_avc_au/`:

```powershell
New-Item -ItemType Directory -Force -Path ./output/dump_avc_au

dump-avc-au `
    --input ./assets/vid/foreman_qcif.h264 `
    --output ./output/dump_avc_au
```

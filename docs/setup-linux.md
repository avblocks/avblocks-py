# Setup for Linux

> Scripts are `bash`

## Ubuntu

### Compilers

```bash
sudo apt install build-essential
```

### Libraries

These libraries are required by AVBlocks:

#### Ubuntu 24.04 / 22.04 / 20.04

```bash
sudo apt-get install libjpeg8 libtiff5 libpng16-16 libtbb2
```

#### Ubuntu 18.04 / 16.04

```bash
sudo apt-get install libjpeg8 libtiff5 libpng12-0 libtbb2
```

### uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Visual Studio Code

Install via Snap Store:

```bash
sudo snap install --classic code
```

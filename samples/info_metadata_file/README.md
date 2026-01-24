## info_metadata_file

How to use the MediaInfo and Metadata APIs to extract metadata information from a media file.

### Command Line

```sh
info-metadata-file --input <any_media_file>
```

### Examples

List options:

```sh
info-metadata-file --help
```

Extract the metadata from the `./assets/aud/Hydrate-Kenny_Beltrey.ogg` song:

```sh
info-metadata-file \
    --input ./assets/aud/Hydrate-Kenny_Beltrey.ogg
```

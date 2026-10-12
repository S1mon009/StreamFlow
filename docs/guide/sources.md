# Playlists and file sources

StreamFlow supports playlist URLs, TXT files containing multiple URLs, and YAML
files that define one or more groups with their own download settings.

## Playlist detection

Playlist detection is intentionally simple.

The application checks whether the supplied URL contains:

```text
list=
```

If the parameter is present, the source is treated as a playlist.

## Playlist directory

When a playlist is detected, StreamFlow asks the user for a playlist folder name.

The folder is created inside the configured download directory.

Conceptually:

```text
Downloads/
└── My Playlist/
    ├── Video 1.mkv
    ├── Video 2.mkv
    └── Video 3.mkv
```

The output template is based on the media title:

```text
%(title)s.%(ext)s
```

## TXT source

A TXT source is useful when multiple URLs need to be downloaded.

Example:

```text
videos.txt
```

Contents:

```text
https://example.com/video-1
https://example.com/video-2

https://example.com/video-3
```

Empty lines are ignored.

The resulting list contains only non-empty URLs.

After selecting a TXT file, StreamFlow asks for the download group name, output
folder, filename prefix and suffix, naming template, optional indexing, media
type, format, and quality. The default template is `{title}`. When indexing is
enabled, `{index}` can be included in the template, for example
`{prefix}{index:02d} - {title}{suffix}`.

## YAML source

Choose **YAML File** and provide a UTF-8 YAML file using configuration version
1. Each item under `downloads` is downloaded with its own URLs, destination,
naming rules, and media settings:

```yaml
version: 1
downloads:
  - name: "YouTube videos"
    urls:
      - "https://www.youtube.com/watch?v=VIDEO_ID"
    output:
      folder: "E:/Videos/YouTube"
      prefix: "[YT] "
      suffix: ""
    naming:
      template: "{prefix}{index:02d} - {title}{suffix}"
      indexing:
        enabled: true
        start: 1
        padding: 2
    media:
      type: "video"
      format: "mkv"
      quality: "1080p"
```

`media.type` is `video` or `audio`. Video quality accepts `best`, `1440p`,
`1080p`, `720p`, `480p`, or one of StreamFlow's displayed quality labels.
Filename templates support `{title}`, `{prefix}`, `{suffix}`, and `{index}`.
For playlist URLs, the index counts the playlist items; for ordinary URLs, it
counts the URLs in that group. Each profile is processed sequentially.

## File validation

Before reading either file, StreamFlow checks:

1. whether the path exists;
2. whether the path points to a regular file;
3. whether the file can be opened;
4. whether the contents can be read as UTF-8.

## Sequential processing

URLs are processed sequentially.

For example:

```text
URL 1
 ↓
Download
 ↓
URL 2
 ↓
Download
 ↓
URL 3
 ↓
Download
```

The current implementation does not provide parallel downloads.

## Recommendations

For large collections of URLs, keep the TXT file simple:

```text
one URL per line
```

Avoid adding comments or additional metadata unless the source parser is extended to support them.

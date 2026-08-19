# Playlists and TXT files

StreamFlow supports both playlist URLs and text files containing multiple URLs.

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

## File validation

Before reading the file, StreamFlow checks:

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

# Download modes

StreamFlow supports several ways of specifying and processing download sources.

## Single URL

A single URL can be entered directly through the interactive interface.

For a single video, the user can optionally provide a custom filename.

If no custom filename is specified, StreamFlow uses the media title provided by `yt-dlp`.

## Playlist

A URL is treated as a playlist when the application detects a `list=` parameter.

For example:

```text
https://example.com/watch?v=123&list=456
```

StreamFlow then creates a playlist directory and downloads the playlist into that directory.

## TXT file

Multiple URLs can be loaded from a text file.

The file is read as UTF-8 and each non-empty line becomes a separate URL.

Example:

```text
https://example.com/video1
https://example.com/video2
https://example.com/video3
```

The URLs are processed sequentially.

## Video mode

Video mode downloads video together with its associated audio stream.

The selected quality determines the yt-dlp format selector.

The final media is merged into the selected container.

## Audio-only mode

Audio-only mode extracts audio instead of downloading a complete video.

The current implementation uses MP3 as the output format.

The configured audio quality is:

```text
192
```

## Custom filenames

Custom filenames are supported for single-video downloads.

Before being used, filenames are sanitized to remove characters that are invalid on common operating systems.

Invalid characters are replaced with:

```text
_
```

This prevents common filesystem errors.

## Output directories

Downloads are stored under the configured download directory.

Playlist downloads use an additional playlist-specific directory.

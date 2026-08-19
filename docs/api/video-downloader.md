# VideoDownloader

`VideoDownloader` is the central class of StreamFlow.

It coordinates source configuration, download settings, output paths and the interaction with yt-dlp.

## Responsibilities

The class is responsible for:

* configuring the download directory;
* accepting URLs;
* detecting playlists;
* selecting quality;
* selecting output formats;
* generating output paths;
* monitoring network availability;
* invoking yt-dlp;
* handling download errors.

## Download lifecycle

The typical lifecycle is:
```py
downloader = VideoDownloader()


downloader.prompt_user_options()


if downloader.confirm_options():
    downloader.download_video()
```
The application entry point uses this lifecycle internally.

## Quality configuration

The downloader uses a quality map to translate human-readable quality labels into yt-dlp format selectors.
For example:
```bash
High (720p)
```
maps to:
```bash
bestvideo[height<=720]+bestaudio/best[height<=720]
```

## Output handling

Single videos use the configured download directory.

Playlist downloads use a playlist-specific directory.

Output filenames are based on the media title unless a custom filename is provided.

## Class reference
### Video downloader
:::src.classes.video_downloader
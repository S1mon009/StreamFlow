# Download flow

A normal StreamFlow download consists of several stages.

## 1. Application startup

The application starts through:

```bash
python main.py
```

The `main()` function initializes the terminal and enters the download loop.

## 2. Downloader initialization

A new `VideoDownloader` object is created.

During initialization, StreamFlow loads environment configuration and determines the download directory.

The download directory is then verified.

## 3. Source configuration

The user provides the source.

The source can be:

* a single URL;
* a TXT file containing multiple URLs.

## 4. Playlist detection

For each URL, StreamFlow checks whether it contains:

```text
list=
```

If so, the URL is considered a playlist.

## 5. Download configuration

The user selects:

* video or audio-only mode;
* video quality;
* output format;
* playlist folder where required;
* custom filename where applicable.

## 6. Confirmation

StreamFlow displays a summary of the selected options.

The user can confirm or return to configuration.

## 7. Pre-download checks

The download operation is wrapped with decorators.

The decorators provide:

```text
FFmpeg check
     ↓
Network check
     ↓
Timer
     ↓
Download
```

## 8. yt-dlp

StreamFlow constructs the yt-dlp configuration and invokes the downloader.

For video downloads, it specifies:

* format selector;
* output template;
* merge output format;
* playlist behavior;
* progress hooks;
* post-processing.

## 9. Progress monitoring

The progress hook periodically receives status information from yt-dlp.

During an active download, StreamFlow checks network connectivity.

## 10. Error handling

The downloader handles several expected exceptions, including:

* missing output directory;
* insufficient permissions;
* keyboard interruption;
* general download errors.

The application prints an error instead of terminating the entire interactive session.

## 11. Next download

After the operation finishes, the user can choose whether to start another download.

The loop continues until the user selects **No**.

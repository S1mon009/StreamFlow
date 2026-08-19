# First download

After installing StreamFlow, the easiest way to start is to run the main application:

```bash
python main.py
```

StreamFlow uses an interactive configuration process.

## Step 1 — Select the source

The application first asks how the source should be provided.

You can select a single URL or a text file containing multiple URLs.

### Single URL

Enter the URL directly.

Example:

```text
https://example.com/video
```

### TXT file

A text file can contain multiple URLs:

```text
https://example.com/video-1
https://example.com/video-2
https://example.com/video-3
```

Empty lines are ignored.

## Step 2 — Select download mode

For video downloads, StreamFlow allows you to select the video mode.

Audio-only downloads are also available.

## Step 3 — Select video quality

Video mode provides predefined quality levels.

The available options are:

* The best;
* Medium (1440p);
* Above High (1080p);
* High (720p);
* Low (<=480p).

## Step 4 — Select output format

The current video output formats are:

* MP4;
* MKV.

## Step 5 — Configure additional options

Depending on the source, StreamFlow may ask for:

* a playlist folder;
* a custom filename;
* a download directory.

## Step 6 — Confirm

Before starting the download, StreamFlow displays a summary of the selected configuration.

The summary contains information such as:

```text
URL
Type
Quality
Output format
Download folder
```

The user can either confirm the configuration or return to the configuration screen.

## Step 7 — Download

After confirmation, StreamFlow starts the download process.

The application delegates media extraction and downloading to `yt-dlp`.

FFmpeg is used when multimedia processing or stream merging is required.

## Step 8 — Continue

After the operation finishes, StreamFlow asks whether another download should be started.

Selecting **No** terminates the application.

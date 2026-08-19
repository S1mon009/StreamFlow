# Frequently Asked Questions

## What is StreamFlow?

StreamFlow is a Python command-line application for downloading video and audio content using yt-dlp.

## Does StreamFlow support playlists?

Yes.

URLs containing a `list=` parameter are treated as playlists.

## Can I download multiple URLs?

Yes.

Select the TXT file source and provide a text file containing one URL per line.

## Can I download audio only?

Yes.

Audio-only mode extracts the best available audio and converts it to MP3.

## Which video formats are supported?

The current application provides:

* MP4;
* MKV.

## Which video quality levels are available?

The current quality menu contains:

* The best;
* Medium (1440p);
* Above High (1080p);
* High (720p);
* Low (<=480p).

## Is FFmpeg required?

Yes.

FFmpeg is required by the application's download pipeline and is checked before downloading.

## Where are downloaded files stored?

The default location is the user's Downloads directory.

The location can be customized through the input.

## Does StreamFlow handle network interruptions?

The application checks network availability before downloading and monitors connectivity during the yt-dlp download process.

## Can I specify a custom filename?

Yes.

Custom filenames are supported for single-video downloads.

Invalid filesystem characters are sanitized.

## Does StreamFlow use cookies?

Yes.

The current implementation passes:

```text
cookies.txt
```

to yt-dlp.

## Can I download several files at the same time?

No.

The current implementation processes configured URLs sequentially.

## Is StreamFlow a graphical application?

No.

StreamFlow is currently a command-line application with an interactive terminal interface.

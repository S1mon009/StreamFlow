# Troubleshooting

This page covers common problems that may occur while installing or running StreamFlow.

## FFmpeg is not available

If StreamFlow reports that FFmpeg is unavailable, verify the installation:

```bash
ffmpeg -version
```

If the command cannot be found, install FFmpeg and add it to `PATH`.

After changing `PATH`, restart the terminal.

## Python dependencies are missing

If Python reports an import error, activate the virtual environment and reinstall dependencies:

```bash
pip install -r requirements.txt
```

## Download folder does not exist

StreamFlow verifies the configured download directory and creates it when necessary.

If the directory cannot be created, verify:

* the path is correct;
* the user has write permissions;
* the drive is available.

## Permission denied

Verify that the configured download directory is writable.

On Windows, also check whether another application is locking the destination file.

On Linux/macOS, check directory permissions.

## Network connection unavailable

StreamFlow may wait while checking network connectivity.

The default connectivity test uses:

```text
8.8.8.8:53
```

Some corporate, VPN or restricted networks may block this connection.

If the internet works but StreamFlow continues waiting, check local firewall and network policies.

## Download fails

First verify that yt-dlp can access the supplied URL.

Possible causes include:

* invalid URL;
* unavailable media;
* authentication requirements;
* network problems;
* unsupported source behavior;
* expired cookies.

## Authentication problems

If authentication is required, verify that the expected `cookies.txt` file exists and contains valid cookies.

Do not share the cookie file.

## TXT file does not work

Check that:

* the path is correct;
* the file exists;
* the file is not a directory;
* the file is UTF-8 encoded;
* URLs are separated by new lines.

Example:

```text
https://example.com/video1
https://example.com/video2
```

## Custom filename causes an error

StreamFlow sanitizes invalid filename characters.

If problems remain, try a simple filename such as:

```text
my-video
```

## Documentation does not build

Install the documentation dependencies:

```bash
pip install -r requirements-docs.txt
```

Then run:

```bash
mkdocs build --strict
```

Pay attention to the first warning or error reported by MkDocs.

## Tests fail

Make sure:

* the virtual environment is active;
* dependencies are installed;
* the test command is being executed from the repository root.

Then run the project's configured test runner.

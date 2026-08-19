# Configuration

StreamFlow keeps application configuration separate from download-specific settings.

The configuration system is based on variables.

## Environment configuration

The main application setting is the download directory. The directory is stored in `src/config/app_config.py`.

## Download configuration

The download directory is handled separately from video settings.

This separation allows the application to keep:

* application configuration;
* video quality configuration;
* output format configuration

in their respective modules.

## Video settings

Video-related options are defined in `src/config/video_settings.py`.

These settings include:

* quality presets;
* yt-dlp format selectors;
* supported output formats.

The current implementation supports:

```text
MP4
MKV
```

## Configuration recommendations

Do not hard-code machine-specific paths in the source code.

A `.gitignore` should normally contain:

```gitignore
.env
.venv/
cookies.txt
site/
```

This prevents local configuration, authentication cookies and generated documentation from accidentally being committed.

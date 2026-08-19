# Architecture overview

StreamFlow follows a modular Python architecture.

The project separates application flow, downloading, configuration, cross-cutting concerns and utility functions.

## High-level architecture

```text
                    ┌───────────────┐
                    │    main.py    │
                    └───────┬───────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ VideoDownloader   │
                  └─────────┬─────────┘
                            │
          ┌─────────────────┼──────────────────┐
          │                 │                  │
          ▼                 ▼                  ▼
     Configuration      Decorators          yt-dlp
          │                 │                  │
          ▼                 ▼                  ▼
       .env /          Network /           Download
       settings         FFmpeg /           media
                        timing
                                                │
                                                ▼
                                             FFmpeg
```

## Application layer

`main.py` is responsible for the application lifecycle.

It:

1. initializes the terminal;
2. creates a downloader instance;
3. asks the user for configuration;
4. displays the confirmation;
5. starts the download;
6. asks whether another download should be started.

The entry point delegates actual download functionality to `VideoDownloader`.

## Download layer

`VideoDownloader` contains the main application logic.

It handles:

* source configuration;
* playlist detection;
* output paths;
* download options;
* yt-dlp execution;
* progress monitoring;
* error handling.

## Configuration layer

The `config` package contains settings that should not be mixed with download orchestration.

It provides application configuration and video-specific settings.

## Decorator layer

Decorators implement cross-cutting functionality.

Examples include:

* network checks;
* FFmpeg checks;
* execution-time measurement.

This allows these concerns to remain independent from the core download implementation.

## Utility layer

The `utils` package contains reusable helper functions.

The console utility provides terminal-related functionality used by the application.

## External dependencies

StreamFlow relies on:

* yt-dlp for media extraction and downloading;
* FFmpeg for multimedia processing;
* Python packages for configuration and terminal interaction.

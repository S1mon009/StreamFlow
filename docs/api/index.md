# API Reference

This section documents the Python API exposed by StreamFlow.

The API documentation is generated from the source code using `mkdocstrings`.

## Core API

The central component is:

```python
VideoDownloader
```

It provides the functionality required to configure and execute media downloads.

## Configuration API

Configuration is divided into:

* application configuration;
* video settings.

## Decorators

StreamFlow provides decorators for:

* network requirements;
* FFmpeg requirements;
* execution timing.

## Utilities

Utility functions provide reusable functionality such as terminal management.

## API organization

The reference is divided into the following pages:

* [VideoDownloader](video-downloader.md)
* [Configuration](configuration.md)
* [Decorators](decorators.md)
* [Utilities](utilities.md)
* [Main module](main.md)

## Generated documentation

The API pages use `mkdocstrings` directives.

For example:

```markdown
::: classes.video_downloader.VideoDownloader
```

This allows the documentation to be generated directly from Python classes and their docstrings.

As a result, developers should keep public classes and functions documented with clear Google-style docstrings.

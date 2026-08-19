# Configuration API

StreamFlow separates general application configuration from video-specific settings.

## AppConfig

`AppConfig` represents application-level configuration.

The primary configuration value is the download directory.

## Global application configuration

The module exposes a configured `app_config` instance.

## VideoSettings

`VideoSettings` contains video-specific configuration.

It defines:

* quality mappings;
* supported output formats.

## Configuration separation

The separation between `AppConfig` and `VideoSettings` prevents application paths and media settings from becoming tightly coupled.

This makes it easier to change one category without modifying the other.

## Class reference

### App config
:::src.config.app_config

### Video settings
:::src.config.video_settings
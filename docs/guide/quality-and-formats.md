# Quality and formats

StreamFlow provides predefined quality presets instead of requiring users to manually write yt-dlp format selectors.

## Video quality presets

| Preset     | Maximum resolution |
| ---------- | -----------------: |
| The best   |     Best available |
| Medium     |              1440p |
| Above High |              1080p |
| High       |               720p |
| Low        |               480p |

The selectors are defined in `config/video_settings.py`.

## The best

```text
bestvideo+bestaudio/best
```

This asks yt-dlp for the best available video and audio combination.

## 1440p

```text
bestvideo[height<=1440]+bestaudio/best[height<=1440]
```

The selected video stream cannot exceed 1440p.

## 1080p

```text
bestvideo[height<=1080]+bestaudio/best[height<=1080]
```

The selected video stream cannot exceed 1080p.

## 720p

```text
bestvideo[height<=720]+bestaudio/best[height<=720]
```

The selected video stream cannot exceed 720p.

## 480p

```text
bestvideo[height<=480]+bestaudio/best[height<=480]
```

The selected video stream cannot exceed 480p.

## Output formats

StreamFlow currently exposes:

```text
MP4
MKV
```

The selected format is passed to yt-dlp in lowercase.

For example:

```text
MP4 → mp4
MKV → mkv
```

## Audio output

Audio-only mode currently extracts:

```text
MP3
```

with an audio quality setting of:

```text
192
```

## Extending the quality map

Additional quality levels can be added to `VideoSettings`.

For example:

```python
quality_map = {
    "The best": "bestvideo+bestaudio/best",
    "2160p": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",
}
```

The corresponding label will then become available to the application if the settings object is used by the CLI.

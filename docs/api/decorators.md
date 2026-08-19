# Decorators API

StreamFlow uses decorators to implement functionality that surrounds the main download operation.

## Network connectivity

### `is_connected`

Checks whether a network connection can be established.

### `network_required`

Waits for a network connection before executing a function.

## FFmpeg
### `ffmpeg_required`

Ensures that FFmpeg is available before executing the decorated operation.

## Timing
### `timed`

Measures the execution time of the decorated function.

## Why decorators?

Decorators keep cross-cutting concerns outside the main download implementation.

Instead of writing network and FFmpeg checks directly inside `download_video()`, the checks can be composed around the function:

```py
@ffmpeg_required
@network_required
@timed
def download_video():
    ...
```
This keeps the method focused on the actual download operation.

## Class reference
### Connected
:::src.decorators.connected

### FFmpeg
:::src.decorators.ffmpeg

### Timed
:::src.decorators.timed
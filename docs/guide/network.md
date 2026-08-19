# Network handling

StreamFlow contains network checks designed to prevent downloads from starting while the machine is offline and to make downloads more tolerant of temporary connectivity loss.

## Connectivity check

The connectivity utility attempts to establish a TCP connection to:

```text
8.8.8.8:53
```

The default timeout is three seconds.

If the connection succeeds, the function returns:

```python
True
```

Otherwise:

```python
False
```

## `network_required`

The `network_required` decorator wraps functions that require network access.

When the network is unavailable, the decorator waits:

```text
5 seconds
```

and checks the connection again.

Conceptually:

```text
Start
  │
  ▼
Network available?
 ├── Yes ──► execute function
 │
 └── No
      │
      ▼
   wait 5 seconds
      │
      └────► check again
```

## Monitoring during downloads

`VideoDownloader` registers a progress hook with yt-dlp.

When yt-dlp reports:

```text
downloading
```

StreamFlow checks network connectivity.

If the connection disappears, the downloader waits until connectivity returns.

## Limitations

The network check does not verify that the target website is reachable.

It only verifies that the configured TCP endpoint can be reached.

Therefore, it is possible for:

* the general internet connection to work while the target service is unavailable;
* the target service to work while the connectivity test fails because of local firewall or network restrictions.

## Why this approach is used

Long-running downloads can be affected by temporary connectivity issues.

Waiting instead of immediately terminating the operation can make the application more resilient in unstable network environments.

# Cookies

StreamFlow can pass browser/session cookies to yt-dlp through a local `cookies.txt` file.

The downloader constructs the command with:

```text
--cookies cookies.txt
```

## Why cookies are useful

Some media resources require an authenticated session.

In those cases, cookies can provide yt-dlp with the authentication state required to access the resource.

## File location

The current implementation expects:

```text
cookies.txt
```

in the working directory from which the command is executed.

Example:

```text
StreamFlow/
├── cookies.txt
├── main.py
├── requirements.txt
└── ...
```

## Security

Cookie files can contain authentication information.

Treat them as sensitive data.

Never commit them to a public Git repository.

Add the file to `.gitignore`:

```gitignore
cookies.txt
```

Do not:

* upload cookies to GitHub;
* share them publicly;
* include them in documentation screenshots;
* send them to other users.

If a cookie file becomes exposed, invalidate the relevant browser session or authentication tokens.

## Responsible use

Cookies should only be used with accounts and content that you are authorized to access.

StreamFlow does not grant additional permissions to third-party resources.

It simply passes the supplied cookie data to yt-dlp.

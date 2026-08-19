# Contributing

Contributions to StreamFlow are welcome.

The project is organized into separate modules, so changes should preserve the existing separation of responsibilities.

## Before contributing

Before making a change:

1. clone the repository;
2. create a virtual environment;
3. install dependencies;
4. understand the relevant module;
5. review existing tests;
6. check the documentation.

## Making changes

Keep changes focused.

For example, a change to download quality should normally affect:

```text
config/video_settings.py
```

rather than placing quality logic directly into `main.py`.

Similarly, a new network-related behavior should be implemented in the network-related module or decorator.

## Tests

Add or update tests for behavior that can be tested automatically.

Run the available test suite before opening a pull request.

## Documentation

User-visible changes should be documented.

If a new feature changes:

* configuration;
* CLI behavior;
* download modes;
* output formats;
* API behavior;

the corresponding documentation should be updated.

## Code quality

Prefer:

* small functions;
* descriptive names;
* clear docstrings;
* single responsibility;
* minimal duplication.

Avoid unnecessary changes to unrelated parts of the project.

## Pull requests

A pull request should explain:

* what was changed;
* why it was changed;
* how it was tested;
* whether documentation was updated.

Keep the pull request focused on one feature, bug or improvement whenever possible.

## Sensitive files

Never commit:

```text
.env
cookies.txt
.venv/
site/
```

Authentication cookies and environment configuration may contain sensitive information.

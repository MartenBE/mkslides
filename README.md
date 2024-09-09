# MkSlides-Reveal

> Use `mkslides-reveal` to easily turn markdown files into beautiful slides using the power of [Reveal.js](https://revealjs.com/)!

[![PyPI](https://img.shields.io/pypi/v/mkslides-reveal)](https://pypi.org/project/mkslides-reveal/)

[MkSlides-Reveal](https://pypi.org/project/mkslides-reveal/) is a static site generator that's geared towards building slideshows. Slideshow source files are written in Markdown, and configured with a single YAML configuration file. The workflow and commands are heavily inspired by [MkDocs](https://pypi.org/project/mkdocs/) and [reveal-md](https://github.com/webpro/reveal-md).

## Features

- Build static HTML files from Markdown files.
    - Turn a single Markdown file into a HTML slideshow.
    - Turn a folder with Markdown files into a collection of HTML slideshows.
- Publish your slideshow(s) anywhere that static files can be served.
- Preview your site as you work, thanks to [python-livereload](https://pypi.org/project/livereload/).
- Use custom favicons, CSS themes, templates, ... if desired.
- And more!

## Installation

```bash
pip install mkslides-reveal
```

## Create static site

E.g. when your Markdown files are located in the `docs/` folder:

```bash
mkslides-reveal build docs/
```

E.g. when you have a single Markdown file called `test.md`:

```bash
mkslides-reveal build test.md
```

## Live preview

```bash
mkslides-reveal serve docs/
```

```bash
mkslides-reveal build test.md
```

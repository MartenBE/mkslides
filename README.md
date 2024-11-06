# MkSlides

> Use `mkslides` to easily turn markdown files into beautiful slides using the power of [Reveal.js](https://revealjs.com/)!

[![PyPI](https://img.shields.io/pypi/v/mkslides)](https://pypi.org/project/mkslides/)

[MkSlides](https://pypi.org/project/mkslides/) is a static site generator that's geared towards building slideshows. Slideshow source files are written in Markdown, and configured with a single YAML configuration file. The workflow and commands are heavily inspired by [MkDocs](https://pypi.org/project/mkdocs/) and [reveal-md](https://github.com/webpro/reveal-md).

## Features

-   Build static HTML slideshow files from Markdown files.
    -   Turn a single Markdown file into a HTML slideshow.
    -   Turn a folder with Markdown files into a collection of HTML slideshows.
-   Publish your slideshow(s) anywhere that static files can be served.
    -   Locally
    -   On a webserver
    -   Deploy through CI/CD with GitHub/GitLab (like this repo!)
-   Preview your site as you work, thanks to [python-livereload](https://pypi.org/project/livereload/).
-   Use custom favicons, CSS themes, templates, ... if desired.
-   Support for emojis :smile: :tada: :rocket: :sparkles: thanks to [emoji](https://github.com/carpedm20/emoji/)
-   Depends heavily on integration/unit tests to prevent regressions.
-   And more!

## Example

[demo.webm](https://github.com/user-attachments/assets/b594170e-a103-4643-88db-b32437426e77)

[Youtube link](https://youtu.be/RdyRe3JZC7Q) in case you want to look at 2x speed.

Want more examples? An example repo with [slides](https://hogenttin.github.io/hogent-markdown-slides/) demonstrating all possibilities ([Mermaid.js](https://mermaid.js.org/) and [PlantUML](https://plantuml.com/) support, multicolumn slides, image resizing, ...) using Reveal.js with the [HOGENT](https://hogent.be/) theme can be found at https://github.com/HoGentTIN/hogent-markdown-slides .

## Installation

```bash
pip install mkslides
```

## Create static site

E.g. when your Markdown files are located in the `docs/` folder:

```bash
mkslides build docs/
```

E.g. when you have a single Markdown file called `test.md`:

```bash
mkslides build test.md
```

## Live preview

```bash
mkslides serve docs/
```

```bash
mkslides serve test.md
```

## Configuration

Just create a `mkslides.yml`. All options are optional, you only have to add what you want to change to `mkslides.yml`.

Here's an example:

```yml
index:
    title: example-title
    favicon: ./example-index-favicon.ico
    theme: example-index-theme.css
slides:
    favicon: ./example-slides-favicon.ico
    theme: example-slides-theme.css
    highlight_theme: example-slides-highlight-theme.css
    separator: ^\s*---\s*$
    separator_vertical: ^\s*-v-\s*$
    separator_notes: "^Notes?:"
    separator_charset: utf-8
revealjs:
    height: 1080
    width: 1920
    transition: fade
plugins:
    - name: RevealMermaid
      extra_javascript:
          - https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin/plugin/mermaid/mermaid.min.js
    - extra_javascript:
          - https://cdn.jsdelivr.net/npm/reveal-plantuml/dist/reveal-plantuml.min.js
```

-   `favicon`and `theme`, can also be configured as an URL, e.g. `https://example.org/theme.css`.
-   `theme` can also be configured as a [Reveal.js built-in theme](https://revealjs.com/themes/), e.g. `black`, `white`, `league`, `solarized`, `dracula`, ... .
-   `highlight_theme` can also be configured as a [highlight.js built-in theme](https://highlightjs.org/examples), e.g. `monokai`, `obsidian`, `tokyo-night-dark`, `vs`, ... .
-   `revealjs` can contain all [Reveal.js options](https://revealjs.com/config/).

## Contributing

You can run the tests with `poetry` and `pytest`:

```bash
poetry run pytest
```

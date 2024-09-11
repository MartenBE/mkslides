# MkSlides-Reveal

> Use `mkslides-reveal` to easily turn markdown files into beautiful slides using the power of [Reveal.js](https://revealjs.com/)!

[![PyPI](https://img.shields.io/pypi/v/mkslides-reveal)](https://pypi.org/project/mkslides-reveal/)

[MkSlides-Reveal](https://pypi.org/project/mkslides-reveal/) is a static site generator that's geared towards building slideshows. Slideshow source files are written in Markdown, and configured with a single YAML configuration file. The workflow and commands are heavily inspired by [MkDocs](https://pypi.org/project/mkdocs/) and [reveal-md](https://github.com/webpro/reveal-md).

## Features

-   Build static HTML files from Markdown files.
    -   Turn a single Markdown file into a HTML slideshow.
    -   Turn a folder with Markdown files into a collection of HTML slideshows.
-   Publish your slideshow(s) anywhere that static files can be served.
    -   Locally
    -   On a webserver
    -   Deploy through CI/CD with GitHub/GitLab (like this repo!)
-   Preview your site as you work, thanks to [python-livereload](https://pypi.org/project/livereload/).
-   Use custom favicons, CSS themes, templates, ... if desired.
-   And more!

## Example

[build.webm](https://github.com/user-attachments/assets/85432467-46db-46ad-aa90-378c912b0098)

[Youtube link](https://www.youtube.com/watch?v=D9RSATHFf7U) in case you want to look at 2x speed.

The [repo](https://github.com/HoGentTIN/hogent-revealmd) in this example also has advanced usage examples and theming, so check it out to see more possibilities!

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
mkslides-reveal serve test.md
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
reveal.js:
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
-   `reveal.js` can contain all [Reveal.js options](https://revealjs.com/config/).

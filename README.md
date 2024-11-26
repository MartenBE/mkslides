# MkSlides

> Use `mkslides` to easily turn markdown files into beautiful slides using the power of [Reveal.js](https://revealjs.com/)!

[![PyPI](https://img.shields.io/pypi/v/mkslides)](https://pypi.org/project/mkslides/)

[MkSlides](https://pypi.org/project/mkslides/) is a static site generator that's geared towards building slideshows. Slideshow source files are written in Markdown, and configured with a single YAML configuration file. The workflow and commands are heavily inspired by [MkDocs](https://pypi.org/project/mkdocs/) and [reveal-md](https://github.com/webpro/reveal-md).

## Features

- Build static HTML slideshow files from Markdown files.
    - Turn a single Markdown file into a HTML slideshow.
    - Turn a folder with Markdown files into a collection of HTML slideshows.
- Publish your slideshow(s) anywhere that static files can be served.
    - Locally
    - On a webserver
    - Deploy through CI/CD with GitHub/GitLab (like this repo!)
- Preview your site as you work, thanks to [python-livereload](https://pypi.org/project/livereload/).
- Use custom favicons, CSS themes, templates, ... if desired.
- Support for emojis :smile: :tada: :rocket: :sparkles: thanks to [emoji](https://github.com/carpedm20/emoji/)
- Depends heavily on integration/unit tests to prevent regressions.
- And more!

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

# Need help or want to know more?

## Commands

```bash
mkslides build -h
mkslides serve -h
```

## Configuration

Just create a `mkslides.yml`. All options are optional, you only have to add what you want to change to `mkslides.yml`.

Here's an example showcasing all possible options in the config file:

```yml
# Configuration for the generated index page
index:
    # Title of the generated index page: string
    title: example-title
    # Favicon of the generated index page: file path or public url to favicon
    # file
    favicon: ./example-index-favicon.ico
    # Theme of the generated index page: file path or public url to CSS file
    theme: example-index-theme.css
# Configuration for the slides
slides:
    # Favicon of the slides: file path or public url to favicon file
    favicon: ./example-slides-favicon.ico
    # Theme of the slides: file path to CSS file, public url to CSS file, or one
    # of the reveal.js themes such as `black`, `white`, `league`, `solarized`,
    # `dracula`, ... (see https://revealjs.com/themes/)
    theme: example-slides-theme.css
    # Theme for syntax highlighting of code fragments on the slides: file path
    # to CSS file, public url to CSS file, or one of the highlight.js built-in
    # themes such as `monokai`, `obsidian`, `tokyo-night-dark`, `vs`, ...
    # (see https://highlightjs.org/examples)
    highlight_theme: example-slides-highlight-theme.css
    # Relative path to a python script containing a function
    # Callable[[str], str] named `preprocess`. For each Markdown file, the whole
    # file content is given to the function as a str. The returned string is
    # then further processed as the markdown to give to Reveal.js
    preprocess_script: tests/test_preprocessors/replace_ats.py
    # Separator to determine end current/begin new slide: regexp
    # (see https://revealjs.com/markdown/#external-markdown)
    separator: ^\s*---\s*$
    # Separator to determine end current/begin new vertical slide: regexp
    # (see https://revealjs.com/markdown/#external-markdown)
    separator_vertical: ^\s*-v-\s*$
    # Separator to determine notes of the slide: regexp
    # (see https://revealjs.com/markdown/#external-markdown)
    separator_notes: "^Notes?:"
    # Charset of the slides: string
    # (see https://revealjs.com/markdown/#external-markdown)
    separator_charset: utf-8
# Options to be passed to reveal.js: options in yaml format, they will be
# translated to JSON automatically (see https://revealjs.com/config/)
revealjs:
    height: 1080
    width: 1920
    transition: fade
# Plugins or additional CSS/JavaScript files for the slides. These are given as
# a list.
plugins:
    # Name of the plugin (optional, see plugin README): plugin id string
    # (see https://revealjs.com/creating-plugins/#registering-a-plugin)
    - name: RevealMermaid
      # List of JavaScript files of the plugin: file path or public url to
      # JavaScript file per entry
      extra_javascript:
          - https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin/plugin/mermaid/mermaid.min.js
    - extra_javascript:
          - https://cdn.jsdelivr.net/npm/reveal-plantuml/dist/reveal-plantuml.min.js
```

Default config (also used if no config file is present):

```yml
index:
    title: Index
slides:
    theme: black
    highlight_theme: monokai
revealjs:
    history: true
    slideNumber: c/t
```

It is also possible to override `slides`, `revealjs`, and `plugins` options on a per Markdown file base using it's frontmatter:

```md
---
title: frontmatter title
slides:
    theme: solarized
    highlight_theme: vs
    separator: <!--s-->
revealjs:
    height: 1080
    width: 1920
    transition: zoom
---

# Slides with frontmatter

<!--s-->

## Lorem ipsum

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

<!--s-->
```

Notes:

- `title` here is a frontmatter-only available option to set the title of this slideshow in the generated index page. This option is not available in `mkslides.yml`.
- The precedence is frontmatter > `mkslides.yml` > defaults.

## Contributing

You can run the tests with `poetry` and `pytest`:

```bash
poetry run pytest
```

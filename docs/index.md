---
title: "Would you like to know more?"
---

# MkSlides-Reveal

Created by [MartenBE](https://github.com/MartenBE)

Hosted on [GitHub](https://github.com/MartenBE/mkslides-reveal) and [Pypi](https://pypi.org/project/mkslides-reveal/)

---

## What does it do?

<img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Markdown-mark.svg" height="100px" style="margin-right: 50px; background: white; border-radius: 16px"/>
<img src="https://static.slid.es/reveal/logo-v1/reveal-white-text.svg" height="100px"/>

-   From Markdown to static HTML slides using [Reveal.js](https://revealjs.com/)
-   What [MkDocs](https://www.mkdocs.org/) does for documentation, [MkSlides-Reveal](https://pypi.org/project/mkslides-reveal/) does for slides
    -   MkSlides-Reveal lets you focus on Markdown, not on Reveal.js HTML boilerplate
    -   Very similar use pattern and CLI as MkDocs
-   Inspired by both MkDocs and [reveal-md](https://github.com/webpro/reveal-md)

---

## Installation

```console
$ pip install mkslides-reveal
```

---

## Usage

-   Input
    -   Markdown **file**
    -   or **directory** with multiple (nested) Markdown files
-   Output
    -   Folder with static HTML slides
        -   Includes an index.html page with links to each slideshow when the input was a directory
-   Can be used for
    -   Local slides
    -   Hosted slides on webserver
    -   Slides generated automatically by CI/CD using Markdown files in GitHub/GitLab repo
        -   That's exactly what is happening [here](https://github.com/MartenBE/mkslides-reveal/blob/main/.github/workflows/publish.yml)!

---

## Customizable

-   Configuration in `mkslides.yml`
-   You can customize:
    -   Index page:
        -   Theme (local file or by public URL)
        -   Favicon (local file or by public URL)
        -   Title
        -   Template for the output HTML page
    -   Slides
        -   Theme (local file, [Reveal.js theme](https://revealjs.com/themes/), or by public URL)
        -   Highlight.js Theme (local file, [highlight.js theme](https://highlightjs.org/examples), or by public URL)
        -   Favicon (local file or by public URL)
        -   Title
        -   Template for the output HTML page

---

## Build

-   Generate the static HTML files:

```console
$ mkslides-reveal build -h
Usage: mkslides-reveal build [OPTIONS] FILENAME|PATH

  Build the MkDocs documentation.

  FILENAME|PATH is the path to the Markdown file, or the directory containing Markdown files.

Options:
  -f, --config-file FILENAME  Provide a specific MkSlides-Reveal config file.
  -d, --site-dir PATH         The directory to output the result of the slides build.
  -h, --help                  Show this message and exit.
```

---

TODO: video

---

## Serve

-   Live preview:

```console
$ mkslides-reveal serve -h
Usage: mkslides-reveal serve [OPTIONS] FILENAME|PATH

  Run the builtin development server.

  FILENAME|PATH is the path to the Markdown file, or the directory containing Markdown files.

Options:
  -a, --dev-addr <IP:PORT>    IP address and port to serve slides locally.
  -o, --open                  Open the website in a Web browser after the initial build finishes.
  --watch-index-theme         Include the index theme in list of files to watch for live reloading.
  --watch-index-template      Include the index template in list of files to watch for live reloading.
  --watch-slides-theme        Include the slides theme in list of files to watch for live reloading.
  --watch-slides-template     Include the slides template in list of files to watch for live reloading.
  -f, --config-file FILENAME  Provide a specific MkSlides-Reveal config file.
  -h, --help                  Show this message and exit.
```

---

TODO: video

---

## Contributions

-   MkSlides-Reveal is and always will be open source
    -   [MIT license](https://github.com/MartenBE/mkslides-reveal/blob/main/LICENSE)
-   Contributions are very welcome!
    -   Open an issue and/or PR
    -   We only ask that you try real hard to include **tests**!
        -   Almost everything is [tested automatically](https://github.com/MartenBE/mkslides-reveal/tree/main/tests)

---

## Example

-   This slideshow
-   Showcase of all possibilities using Reveal.js with the [HOGENT](https://hogent.be/) theme.
    -   Also includes a lot of advanced examples such as [Mermaid.js](https://mermaid.js.org/) and [PlantUML](https://plantuml.com/) support, multicolumn slides, CI/CD, ... .
    -   [Slides](https://hogenttin.github.io/hogent-revealmd/)
    -   [Code](https://github.com/HoGentTIN/hogent-revealmd)
-   [Reveal.js](https://revealjs.com/?demo)

---

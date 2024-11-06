---
title: "Would you like to know more?"
---

# MkSlides

Created by [MartenBE](https://github.com/MartenBE)

Hosted on [GitHub](https://github.com/MartenBE/mkslides) and [PyPI](https://pypi.org/project/mkslides/)

Inspired by [MkDocs](https://pypi.org/project/mkdocs/) and [reveal-md](https://github.com/webpro/reveal-md)

---

## What does it do?

<img src="./img/markdown-logo.png" height="100px" style="margin-right: 50px;"/>
<img src="./img/reveal-js-logo.svg" height="100px"/>

-   Build static HTML slideshow files from Markdown files.
    -   Turn a single Markdown file into a HTML slideshow.
    -   Turn a folder with Markdown files into a collection of HTML slideshows.
-   Publish your slideshow(s) anywhere that static files can be served.
    -   Locally, on a webserver, deploy through CI/CD with GitHub/GitLab (like this repo!), ...

---

-   Preview your site as you work, thanks to [python-livereload](https://pypi.org/project/livereload/).
-   Use custom favicons, CSS themes, templates, ... if desired.
-   Support for emojis :smile: :tada: :rocket: :sparkles: thanks to [emoji](https://github.com/carpedm20/emoji/)
-   Depends heavily on integration/unit tests to prevent regressions.
-   And more!

---

## Installation

```console
$ pip install mkslides
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
        -   That's exactly what is happening [here](https://github.com/MartenBE/mkslides/blob/main/.github/workflows/publish.yml)!

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

## Example

<iframe width="1280" height="720" src="https://www.youtube.com/embed/RdyRe3JZC7Q?si=GQoCFem5ZKHoIaVA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

## Build

-   Generate the static HTML files:

```console
$ mkslides build -h
Usage: mkslides build [OPTIONS] FILENAME|PATH

  Build the MkDocs documentation.

  FILENAME|PATH is the path to the Markdown file, or the directory containing Markdown files.

Options:
  -f, --config-file FILENAME  Provide a specific MkSlides config file.
  -d, --site-dir PATH         The directory to output the result of the slides build.
  -h, --help                  Show this message and exit.
```

---

## Serve

-   Live preview:

```console
$ mkslides serve -h
Usage: mkslides serve [OPTIONS] FILENAME|PATH

  Run the builtin development server.

  FILENAME|PATH is the path to the Markdown file, or the directory containing Markdown files.

Options:
  -a, --dev-addr <IP:PORT>    IP address and port to serve slides locally.
  -o, --open                  Open the website in a Web browser after the initial build finishes.
  --watch-index-theme         Include the index theme in list of files to watch for live reloading.
  --watch-index-template      Include the index template in list of files to watch for live reloading.
  --watch-slides-theme        Include the slides theme in list of files to watch for live reloading.
  --watch-slides-template     Include the slides template in list of files to watch for live reloading.
  -f, --config-file FILENAME  Provide a specific MkSlides config file.
  -h, --help                  Show this message and exit.
```

---

## Contributions

-   MkSlides is and always will be open source
    -   [MIT license](https://github.com/MartenBE/mkslides/blob/main/LICENSE)
-   Contributions are very welcome!
    -   Open an issue and/or PR
    -   We only ask that you try real hard to include **tests**!
        -   Almost everything is [tested automatically](https://github.com/MartenBE/mkslides/tree/main/tests)

---

## Examples

-   The [MkSlides repo](https://github.com/MartenBE/mkslides/) itself generates the slideshow you are currently watching.
-   https://github.com/HoGentTIN/hogent-markdown-slides: an example repo demonstrating all possibilities using Reveal.js with the custom [HOGENT](https://hogent.be/) theme, including ...
    -   an example of the automatically generated index page
    -   a [slideshow](https://hogenttin.github.io/hogent-markdown-slides/) with a lot of advanced examples such as [Mermaid.js](https://mermaid.js.org/) and [PlantUML](https://plantuml.com/) support, multicolumn slides, ...
    -   an example of GitHub CI/CD pipelines

---

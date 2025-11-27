# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import datetime
import json
import logging
import re
import shutil
import time
from copy import deepcopy
from functools import partial
from importlib import resources
from pathlib import Path
from typing import Any

import frontmatter  # type: ignore[import-untyped]
import markdown
from bs4 import BeautifulSoup, Comment
from emoji import emojize
from jinja2 import Template
from omegaconf import DictConfig, OmegaConf

from mkslides.config import FRONTMATTER_ALLOWED_KEYS
from mkslides.mdfiletoprocess import MdFileToProcess
from mkslides.navtree import NavTree
from mkslides.preprocess import load_preprocessing_function
from mkslides.urltype import URLType
from mkslides.utils import get_url_type

from .constants import (
    DEFAULT_INDEX_TEMPLATE,
    DEFAULT_SLIDESHOW_TEMPLATE,
    HIGHLIGHTJS_THEMES_LIST,
    HIGHLIGHTJS_THEMES_RESOURCE,
    HTML_BACKGROUND_IMAGE_REGEX,
    HTML_RELATIVE_LINK_REGEX,
    LOCAL_JINJA2_ENVIRONMENT,
    MD_EXTENSION_REGEX,
    MD_RELATIVE_LINK_REGEX,
    OUTPUT_ASSETS_DIRNAME,
    REVEALJS_RESOURCE,
    REVEALJS_THEMES_LIST,
)

logger = logging.getLogger(__name__)


class MarkupGenerator:
    def __init__(
        self,
        global_config: DictConfig,
        md_root_path: Path,
        output_directory_path: Path,
        strict: bool,
    ) -> None:
        self.global_config = global_config
        self.md_root_path = md_root_path.resolve(strict=True)
        self.output_directory_path = output_directory_path.resolve(strict=False)
        logger.info(
            f"Output directory: '{self.output_directory_path.absolute()}'",
        )

        self.output_assets_path = self.output_directory_path / OUTPUT_ASSETS_DIRNAME
        self.output_revealjs_path = self.output_assets_path / "reveal-js"
        self.output_highlightjs_themes_path = (
            self.output_assets_path / "highlight-js-themes"
        )

        self.strict = strict

    def process_markdown(self) -> None:
        """Process the markdown files and generate HTML slideshows."""
        logger.debug("Processing markdown")
        start_time = time.perf_counter()

        self.__create_or_clear_output_directory()

        if self.md_root_path.is_file():
            assert self.md_root_path.suffix == ".md", (
                "md_root_path must be a markdown file"
            )
            self.__process_markdown_file()
        else:
            self.__process_markdown_directory()

        end_time = time.perf_counter()
        logger.info(
            f"Finished processing markdown in {end_time - start_time:.2f} seconds",
        )

    def __create_or_clear_output_directory(self) -> None:
        """Clear or create the output directory and copy reveal.js."""
        if self.output_directory_path.exists():
            shutil.rmtree(self.output_directory_path)
            logger.debug("Output directory already exists, deleted")

        self.output_directory_path.mkdir(parents=True, exist_ok=True)
        logger.debug("Output directory created")

        with resources.as_file(REVEALJS_RESOURCE) as revealjs_path:
            self.__copy(revealjs_path, self.output_revealjs_path)

        with resources.as_file(HIGHLIGHTJS_THEMES_RESOURCE) as highlightjs_themes_path:
            self.__copy(highlightjs_themes_path, self.output_highlightjs_themes_path)

    def scan_files(self) -> tuple[list[MdFileToProcess], list[Path]]:
        """Scan the markdown directory for markdown files and other files."""
        md_files: list[MdFileToProcess] = []
        non_md_files: list[Path] = []

        for file in self.md_root_path.rglob("*"):
            if file.is_file():
                resolved_file = file.resolve(strict=True)
                if resolved_file.suffix.lower() == ".md":
                    destination_path = (
                        self.output_directory_path
                        / resolved_file.relative_to(self.md_root_path).with_suffix(
                            ".html",
                        )
                    )

                    md_files.append(
                        self.__create_md_file_to_process(
                            resolved_file,
                            destination_path,
                        ),
                    )

                else:
                    non_md_files.append(resolved_file)

        return md_files, non_md_files

    def __create_md_file_to_process(
        self,
        source_path: Path,
        destination_path: Path,
    ) -> MdFileToProcess:
        """Create an MdFileToProcess instance from a markdown file."""
        content = source_path.read_text(encoding="utf-8-sig")
        frontmatter_metadata, markdown_content = frontmatter.parse(content)

        slide_config = self.__generate_slide_config(
            source_path,
            destination_path,
            frontmatter_metadata,
        )
        assert slide_config

        markdown_content = emojize(markdown_content, language="alias")

        if preprocess_script := slide_config.slides.preprocess_script:
            preprocess_function = load_preprocessing_function(preprocess_script)
            if not preprocess_function:
                msg = (
                    f"Preprocessing function '{preprocess_script}' could not be loaded"
                )
                raise ImportError(msg)
            markdown_content = preprocess_function(markdown_content)
            logger.debug(
                f"Applied preprocessing function '{preprocess_script}' to markdown content of '{source_path}'",
            )

        return MdFileToProcess(
            source_path=source_path,
            destination_path=destination_path,
            slide_config=slide_config,
            markdown_content=markdown_content,
        )

    def __process_markdown_file(self) -> None:
        """Process the detected markdown file."""
        absolute_input_path = self.md_root_path.absolute()
        logger.debug(f"Processing markdown file at '{absolute_input_path}'")
        logger.warning(
            f"When you use a single file like '{absolute_input_path}' as `PATH`, only default static assets will be copied to the output folder. If you want to include images or other files, create a folder instead and pass that as `PATH`. Using a file as `PATH` is more meant for a quick slideshow in a pinch using only text.",
        )

        destination_path = self.output_directory_path / "index.html"
        md_file_data = self.__create_md_file_to_process(
            self.md_root_path,
            destination_path,
        )

        self.__process_detected_markdown_files([md_file_data])

    def __process_markdown_directory(self) -> None:
        """Process the detected markdown files in a directory."""
        logger.debug(
            f"Processing markdown directory at '{self.md_root_path.absolute()}'",
        )

        md_files, non_md_files = self.scan_files()

        self.__process_detected_markdown_files(md_files, non_md_files)

    def __process_detected_markdown_files(
        self,
        md_files: list,
        non_md_files: list | None = None,
    ) -> None:
        """Process the detected markdown files and copy non-markdown files."""
        if non_md_files:
            for file in non_md_files:
                destination_path = self.output_directory_path / file.relative_to(
                    self.md_root_path,
                )
                self.__copy(file, destination_path)

        self.__handle_relative_links(md_files)

        templates = self.__load_templates(md_files)

        if len(md_files) == 1:
            md_files[0].destination_path = self.output_directory_path / "index.html"
        else:
            self.__generate_index(md_files)

        self.__render_slideshows(md_files, templates)

    def __render_slideshows(
        self,
        md_files: list[MdFileToProcess],
        templates: dict[str, Template],
    ) -> None:
        """Render all markdown files to HTML slideshows."""
        for md_file_data in md_files:
            slide_config = md_file_data.slide_config

            slideshow_template = None
            if template_config := slide_config.slides.template:
                slideshow_template = templates[template_config]
            else:
                slideshow_template = DEFAULT_SLIDESHOW_TEMPLATE

            revealjs_path = self.output_revealjs_path.relative_to(
                md_file_data.destination_path.parent,
                walk_up=True,
            )

            # https://revealjs.com/markdown/#external-markdown
            markdown_data_options = {
                key: value
                for key, value in {
                    "data-separator": slide_config.slides.separator,
                    "data-separator-vertical": slide_config.slides.separator_vertical,
                    "data-separator-notes": slide_config.slides.separator_notes,
                    "data-charset": slide_config.slides.charset,
                }.items()
                if value
            }

            markup = slideshow_template.render(
                favicon=slide_config.slides.favicon,
                theme=slide_config.slides.theme,
                highlight_theme=slide_config.slides.highlight_theme,
                revealjs_path=revealjs_path,
                markdown_data_options=markdown_data_options,
                markdown=md_file_data.markdown_content,
                revealjs_config=OmegaConf.to_container(slide_config.revealjs),
                plugins=slide_config.plugins,
            )

            self.__create_or_overwrite_file(
                md_file_data.destination_path,
                markup,
            )

    def __load_templates(
        self,
        md_files: list[MdFileToProcess],
    ) -> dict[str, Template]:
        """Load Jinja2 templates from the markdown files."""
        templates: dict[str, Template] = {}

        for md_file_data in md_files:
            template = md_file_data.slide_config.slides.template
            if template and template not in templates:
                templates[template] = LOCAL_JINJA2_ENVIRONMENT.get_template(template)
                logger.debug(f"Loaded custom template '{template}'")

        return templates

    def __generate_theme_url(
        self,
        destination_path: Path,
        slide_config: DictConfig,
        frontmatter_metadata: dict[str, object],
    ) -> str | None:
        """Generate the reveal.js theme URL."""
        theme = slide_config.slides.theme

        if theme is None:
            return None

        if theme in REVEALJS_THEMES_LIST:
            return str(
                (
                    self.output_revealjs_path / "dist" / "theme" / f"{theme}.css"
                ).relative_to(destination_path.parent, walk_up=True),
            )

        if get_url_type(theme) != URLType.RELATIVE or (
            "slides" in frontmatter_metadata
            and isinstance(frontmatter_metadata["slides"], dict)
            and frontmatter_metadata["slides"].get("theme")
        ):
            return theme

        return str(
            (self.output_directory_path / theme).relative_to(
                destination_path.parent,
                walk_up=True,
            ),
        )

    def __generate_highlight_theme_url(
        self,
        destination_path: Path,
        slide_config: DictConfig,
        frontmatter_metadata: dict[str, object],
    ) -> str | None:
        """Generate the highlight.js theme URL."""
        highlight_theme = slide_config.slides.highlight_theme

        if highlight_theme is None:
            return None

        if highlight_theme in HIGHLIGHTJS_THEMES_LIST:
            return str(
                (
                    self.output_highlightjs_themes_path / f"{highlight_theme}.css"
                ).relative_to(destination_path.parent, walk_up=True),
            )

        if get_url_type(highlight_theme) != URLType.RELATIVE or (
            "slides" in frontmatter_metadata
            and isinstance(frontmatter_metadata["slides"], dict)
            and frontmatter_metadata["slides"].get("highlight_theme")
        ):
            return highlight_theme

        return str(
            (self.output_directory_path / highlight_theme).relative_to(
                destination_path.parent,
                walk_up=True,
            ),
        )

    def __generate_favicon_url(
        self,
        destination_path: Path,
        slide_config: DictConfig,
        frontmatter_metadata: dict[str, object],
    ) -> str | None:
        favicon = slide_config.slides.favicon

        if favicon is None:
            return None

        if get_url_type(favicon) != URLType.RELATIVE or (
            "slides" in frontmatter_metadata
            and isinstance(frontmatter_metadata["slides"], dict)
            and frontmatter_metadata["slides"].get("favicon")
        ):
            return favicon

        return str(
            (self.output_directory_path / favicon).relative_to(
                destination_path.parent,
                walk_up=True,
            ),
        )

    def __generate_preprocess_script_absolute_path(
        self,
        source_path: Path,
        slide_config: DictConfig,
        frontmatter_metadata: dict[str, object],
    ) -> str | None:
        """Generate the absolute path for the preprocess script if it is a relative URL."""
        preprocess_script = slide_config.slides.preprocess_script

        if slide_config.slides.preprocess_script is None:
            return None

        if get_url_type(preprocess_script) != URLType.RELATIVE:
            return preprocess_script

        if (
            "slides" in frontmatter_metadata
            and isinstance(frontmatter_metadata["slides"], dict)
            and frontmatter_metadata["slides"].get("preprocess_script")
        ):
            return str(
                (source_path.parent / preprocess_script).resolve(strict=True),
            )

        return str(
            (
                self.global_config.internal.config_path.parent / preprocess_script
            ).resolve(strict=True),
        )

    def __generate_slide_config(
        self,
        source_path: Path,
        destination_path: Path,
        frontmatter_metadata: dict[str, object],
    ) -> DictConfig:
        """Generate the slide configuration by merging the metadata retrieved from the frontmatter of the markdown and the global configuration."""
        slide_config: DictConfig = deepcopy(self.global_config)

        if frontmatter_metadata:
            for key in FRONTMATTER_ALLOWED_KEYS:
                if key in frontmatter_metadata:
                    OmegaConf.update(slide_config, key, frontmatter_metadata[key])

        slide_config.slides.theme = self.__generate_theme_url(
            destination_path,
            slide_config,
            frontmatter_metadata,
        )

        slide_config.slides.highlight_theme = self.__generate_highlight_theme_url(
            destination_path,
            slide_config,
            frontmatter_metadata,
        )

        slide_config.slides.favicon = self.__generate_favicon_url(
            destination_path,
            slide_config,
            frontmatter_metadata,
        )

        slide_config.slides.preprocess_script = (
            self.__generate_preprocess_script_absolute_path(
                source_path,
                slide_config,
                frontmatter_metadata,
            )
        )

        return slide_config

    def __generate_index(self, md_files: list[MdFileToProcess]) -> None:
        """Generate an index.html file in the output directory."""
        logger.debug("Generating index")

        navtree = NavTree(self.md_root_path, self.output_directory_path)
        if self.global_config.index.nav:
            nav_from_config = OmegaConf.to_container(self.global_config.index.nav)
            assert isinstance(nav_from_config, list), "nav must be a list"
            logger.debug("Generating navigation tree from config")
            navtree.from_config_json(nav_from_config)
            navtree.validate_with_md_files(md_files, strict=self.strict)
        else:
            logger.debug("Generating navigation tree from markdown files")
            navtree.from_md_files(md_files)

        logger.debug(
            f"Generated navigation tree with input root path {navtree.input_root_path.absolute()} and output root path {navtree.output_root_path.absolute()}",
        )

        if logger.isEnabledFor(logging.DEBUG):
            navtree_json = json.dumps(json.loads(navtree.to_json()), indent=4)
            logger.debug(f"Navigation tree:\n\n{navtree_json}\n")

        # Refresh the templates here, so they have effect when live reloading
        index_template = None
        if template_config := self.global_config.index.template:
            index_template = LOCAL_JINJA2_ENVIRONMENT.get_template(template_config)
        else:
            index_template = DEFAULT_INDEX_TEMPLATE

        content = index_template.render(
            favicon=self.global_config.index.favicon,
            title=self.global_config.index.title,
            theme=self.global_config.index.theme,
            navtree=navtree,
            build_datetime=datetime.datetime.now(tz=datetime.UTC),
            enable_footer=self.global_config.index.enable_footer,
        )
        self.__create_or_overwrite_file(
            self.output_directory_path / "index.html",
            content,
        )

    def __create_or_overwrite_file(self, destination_path: Path, content: Any) -> None:
        """Create or overwrite a file with the given content."""
        is_overwrite = destination_path.exists()

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        destination_path.write_text(content, encoding="utf-8")

        action = "Overwritten" if is_overwrite else "Created"
        logger.debug(f"{action} file '{destination_path}'")

    def __copy(self, source_path: Path, destination_path: Path) -> None:
        """Copy a file or directory from the source path to the destination path."""
        is_overwrite = destination_path.exists()
        is_directory = source_path.is_dir()

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        if is_directory:
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
        else:
            shutil.copy(source_path, destination_path)

        action = "Overwritten" if is_overwrite else "Copied"
        file_or_directory = "directory" if is_directory else "file"
        logger.debug(
            f"{action} {file_or_directory} '{source_path.absolute()}' to '{destination_path.absolute()}'",
        )

    def __handle_relative_links(
        self,
        md_file_data: list[MdFileToProcess],
    ) -> None:
        """Check if all relative link targets are present and normalize .md links."""
        for md_file in md_file_data:
            content = md_file.markdown_content

            for link in self.__find_all_relative_links(content):
                link_path = md_file.source_path.parent / link
                relative_source_path = md_file.source_path.relative_to(
                    self.md_root_path,
                )

                if not link_path.exists():
                    msg = f"File '{relative_source_path}' contains a link '{link}', but the target is not found among slide files."
                    if self.strict:
                        raise FileNotFoundError(msg)
                    logger.warning(msg)
                elif link.lower().endswith(".md"):
                    content = self.__replace_md_link_target(content, link)

            md_file.markdown_content = content

    def __find_all_relative_links(self, markdown_content: str) -> set[str]:
        """Find all relative links in the given markdown content."""
        html_content = markdown.markdown(markdown_content, extensions=["extra"])
        soup = BeautifulSoup(html_content, "html.parser")

        found_links = set()

        for link in soup.find_all("a", href=True):
            if not link.find_parents(["code", "pre"]):
                found_links.add(link["href"])

        for link in soup.find_all("img", src=True):
            if not link.find_parents(["code", "pre"]):
                found_links.add(link["src"])

        for link in soup.find_all("source", src=True):
            if not link.find_parents(["code", "pre"]):
                found_links.add(link["src"])

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            if match := HTML_BACKGROUND_IMAGE_REGEX.search(comment):
                found_links.add(match.group("location"))

        relative_links = {
            link for link in found_links if get_url_type(link) == URLType.RELATIVE
        }

        return relative_links

    def __replace_md_link_target(self, content: str, link: str) -> str:
        """Replace a specific .md link target with .html in markdown and HTML links."""

        def _replacer(match: re.Match, *, link: str) -> str:
            matched_location = match.group("location")

            # Only touch matches that correspond exactly to this link
            if matched_location != link:
                return match.group(0)

            new_location = MD_EXTENSION_REGEX.sub(".html", matched_location)
            return match.group(0).replace(matched_location, new_location)

        for regex in (MD_RELATIVE_LINK_REGEX, HTML_RELATIVE_LINK_REGEX):
            bound_replacer = partial(_replacer, link=link)
            content = regex.sub(bound_replacer, content)

        return content

import datetime
import logging
import shutil
import time
from copy import deepcopy
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any

import frontmatter  # type: ignore[import-untyped]
import markdown
from bs4 import BeautifulSoup, Comment
from emoji import emojize
from natsort import natsorted
from omegaconf import DictConfig, OmegaConf

from mkslides.config import FRONTMATTER_ALLOWED_KEYS
from mkslides.preprocess import load_preprocessing_function
from mkslides.urltype import URLType
from mkslides.utils import get_url_type

from .constants import (
    DEFAULT_INDEX_TEMPLATE,
    DEFAULT_SLIDESHOW_TEMPLATE,
    HIGHLIGHTJS_THEMES_RESOURCE,
    HTML_BACKGROUND_IMAGE_REGEX,
    LOCAL_JINJA2_ENVIRONMENT,
    REVEALJS_RESOURCE,
    REVEALJS_THEMES_RESOURCE,
)

logger = logging.getLogger(__name__)


class MarkupGenerator:
    def __init__(
        self,
        global_config: DictConfig,
        output_directory_path: Path,
        strict: bool,
    ) -> None:
        self.global_config = global_config

        self.output_directory_path = output_directory_path.resolve(strict=False)
        logger.info(
            f"Output directory: '{self.output_directory_path.absolute()}'",
        )

        self.output_assets_path = self.output_directory_path / "assets"
        self.output_revealjs_path = self.output_assets_path / "reveal-js"

        self.strict = strict

        self.preprocess_script_func = (
            load_preprocessing_function(self.global_config.slides.preprocess_script)
            if self.global_config.slides.preprocess_script
            else None
        )

    def clear_output_directory(self) -> None:
        for item in self.output_directory_path.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        logger.debug("Output directory cleared")

    def create_or_clear_output_directory(self) -> None:
        if self.output_directory_path.exists():
            self.clear_output_directory()
        else:
            self.output_directory_path.mkdir(parents=True, exist_ok=True)
            logger.debug("Output directory created")

        with resources.as_file(REVEALJS_RESOURCE) as revealjs_path:
            self.__copy(revealjs_path, self.output_revealjs_path)

    def process_markdown(self, input_path: Path) -> None:
        logger.debug("Processing markdown")
        start_time = time.perf_counter()

        if input_path.is_dir():
            self.__process_markdown_directory(input_path)
        else:
            _, output_markup_path = self.__process_markdown_file(
                input_path,
                input_path.parent,
            )
            original_output_markup_path = output_markup_path

            if output_markup_path.stem != "index":
                output_markup_path.rename(output_markup_path.with_stem("index"))
                logger.debug(
                    f"Renamed '{original_output_markup_path.absolute()}' to '{output_markup_path.absolute()}' as it was the only Markdown file",
                )

        end_time = time.perf_counter()
        logger.info(
            f"Finished processing markdown in {end_time - start_time:.2f} seconds",
        )

    ################################################################################

    def __process_markdown_file(
        self,
        md_file: Path,
        md_root_path: Path,
    ) -> tuple[dict, Path]:
        md_file = md_file.resolve(strict=True)
        md_root_path = md_root_path.resolve(strict=True)

        logger.debug(f"Processing markdown file at '{md_file.absolute()}'")

        # Retrieve the frontmatter metadata and the markdown content

        content = md_file.read_text(encoding="utf-8-sig")
        metadata, markdown_content = frontmatter.parse(content)

        if self.preprocess_script_func:
            markdown_content = self.preprocess_script_func(markdown_content)
            logger.debug("Preprocessed markdown content with {preprocess_script_func}")

        slide_config = None
        if metadata:
            slide_config = deepcopy(self.global_config)
            for key in FRONTMATTER_ALLOWED_KEYS:
                if key in metadata:
                    OmegaConf.update(slide_config, key, metadata[key])
            logger.debug("Detected frontmatter, used config:")
            logger.debug(OmegaConf.to_yaml(slide_config, resolve=True))
        else:
            slide_config = self.global_config

        markdown_content = emojize(markdown_content, language="alias")

        # Get the relative path of reveal.js

        output_markup_path = self.output_directory_path / md_file.relative_to(
            md_root_path,
        )

        output_markup_path = output_markup_path.with_suffix(".html")
        relative_revealjs_path = self.output_revealjs_path.relative_to(
            output_markup_path.parent,
            walk_up=True,
        )

        revealjs_config = slide_config.revealjs

        # Copy the theme CSS

        relative_theme_path = None
        if theme := slide_config.slides.theme:
            relative_theme_path = self.__copy_theme(
                output_markup_path,
                theme,
                REVEALJS_THEMES_RESOURCE,
            )

        # Copy the highlight CSS

        relative_highlight_theme_path = None
        if theme := slide_config.slides.highlight_theme:
            relative_highlight_theme_path = self.__copy_theme(
                output_markup_path,
                theme,
                HIGHLIGHTJS_THEMES_RESOURCE,
            )

        # Copy the favicon

        relative_favicon_path = None
        if favicon := slide_config.slides.favicon:
            relative_favicon_path = self.__copy_favicon(output_markup_path, favicon)

        # Retrieve the 3rd party plugins

        plugins = slide_config.plugins

        # Generate the markup from markdown

        # Refresh the templates here, so they have effect when live reloading
        slideshow_template = None
        if template_config := slide_config.slides.template:
            slideshow_template = LOCAL_JINJA2_ENVIRONMENT.get_template(template_config)
        else:
            slideshow_template = DEFAULT_SLIDESHOW_TEMPLATE

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
            favicon=relative_favicon_path,
            theme=relative_theme_path,
            highlight_theme=relative_highlight_theme_path,
            revealjs_path=relative_revealjs_path,
            markdown_data_options=markdown_data_options,
            markdown=markdown_content,
            revealjs_config=revealjs_config,
            plugins=plugins,
        )
        self.__create_file(output_markup_path, markup)

        # Copy local files

        self.__copy_local_files(md_file, md_root_path, markdown_content)

        return metadata.get("title"), output_markup_path

    def __process_markdown_directory(self, md_root_path: Path) -> None:
        md_root_path = md_root_path.resolve(strict=True)
        logger.debug(f"Processing markdown directory at '{md_root_path.absolute()}'")
        slideshows = []
        for md_file in md_root_path.glob("**/*.md"):
            (title_for_index, output_markup_path) = self.__process_markdown_file(
                md_file,
                md_root_path,
            )

            slideshows.append(
                {
                    "title": title_for_index if title_for_index else md_file.stem,
                    "location": output_markup_path.relative_to(
                        self.output_directory_path,
                    ),
                },
            )

        slideshows = natsorted(slideshows, key=lambda x: str(x["location"]))

        logger.debug("Generating index")

        index_path = self.output_directory_path / "index.html"

        # Copy the theme

        relative_theme_path = None
        if theme := self.global_config.index.theme:
            relative_theme_path = self.__copy_theme(index_path, theme)

        # Copy the favicon

        relative_favicon_path = None
        if favicon := self.global_config.index.favicon:
            relative_favicon_path = self.__copy_favicon(index_path, favicon)

        # Refresh the templates here, so they have effect when live reloading
        index_template = None
        if template_config := self.global_config.index.template:
            index_template = LOCAL_JINJA2_ENVIRONMENT.get_template(template_config)
        else:
            index_template = DEFAULT_INDEX_TEMPLATE

        content = index_template.render(
            favicon=relative_favicon_path,
            title=self.global_config.index.title,
            theme=relative_theme_path,
            slideshows=slideshows,
            build_datetime=datetime.datetime.now(tz=datetime.timezone.utc),
        )
        self.__create_file(index_path, content)

    def __copy_local_files(
        self,
        md_file: Path,
        md_root_path: Path,
        markdown_content: str,
    ) -> None:
        links = self.__find_all_links(markdown_content)
        for link in links:
            if get_url_type(link) == URLType.RELATIVE:
                try:
                    local_file_path = Path(md_file.parent, link).resolve(strict=True)
                    self.__copy_to_output_relative_to_md_root(
                        local_file_path,
                        md_root_path,
                    )
                except FileNotFoundError as e:
                    message = f"Local file '{link}' mentioned in '{md_file}' not found."
                    if self.strict:
                        # https://docs.astral.sh/ruff/rules/raise-without-from-inside-except/
                        raise FileNotFoundError(message) from e
                    logger.warning(message)

    def __copy_theme(
        self,
        file_using_theme_path: Path,
        theme: str,
        default_theme_resource: Traversable | None = None,
    ) -> Path | str:
        if get_url_type(theme) == URLType.ABSOLUTE:
            logger.debug(
                f"Using theme '{theme}' from an absolute URL, no copy necessary",
            )
            return theme

        theme_path = None
        if not theme.endswith(".css"):
            assert default_theme_resource is not None
            with resources.as_file(
                default_theme_resource.joinpath(theme),
            ) as builtin_theme_path:
                theme_path = builtin_theme_path.with_suffix(".css").resolve(strict=True)
                logger.debug(
                    f"Using built-in theme '{theme}' from '{theme_path.absolute()}'",
                )
        else:
            theme_path = Path(theme).resolve(strict=True)
            logger.debug(f"Using theme '{theme_path.absolute()}'")

        theme_output_path = self.output_assets_path / theme_path.name
        self.__copy_to_output(theme_path, theme_output_path)

        relative_theme_path = theme_output_path.relative_to(
            file_using_theme_path.parent,
            walk_up=True,
        )

        return relative_theme_path

    def __copy_favicon(self, file_using_favicon_path: Path, favicon: str) -> Path | str:
        if get_url_type(favicon) == URLType.ABSOLUTE:
            logger.debug(
                f"Using favicon '{favicon}' from an absolute URL, no copy necessary",
            )
            return favicon

        favicon_path = Path(favicon).resolve(strict=True)
        logger.debug(f"Using favicon '{favicon_path.absolute()}'")

        favicon_output_path = self.output_assets_path / favicon_path.name
        self.__copy_to_output(favicon_path, favicon_output_path)

        relative_favicon_path = favicon_output_path.relative_to(
            file_using_favicon_path.parent,
            walk_up=True,
        )

        return relative_favicon_path

    ################################################################################

    def __create_file(self, destination_path: Path, content: Any) -> None:
        if destination_path.exists():
            destination_path.write_text(content)
            logger.debug(f"Overwritten: '{destination_path}'")
        else:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            destination_path.write_text(content)
            logger.debug(f"Created file '{destination_path}'")

    def __copy_to_output(self, source_path: Path, destination_path: Path) -> Path:
        self.__copy(source_path, destination_path)
        relative_path = destination_path.relative_to(self.output_directory_path)
        return relative_path

    def __copy_to_output_relative_to_md_root(
        self,
        source_path: Path,
        md_root_path: Path,
    ) -> Path | None:
        source_path = source_path.resolve(strict=True)
        if not source_path.is_relative_to(md_root_path):
            logger.warning(
                f"'{source_path.absolute()}' is outside the markdown root directory, skipped!",
            )
            return None

        relative_path = source_path.relative_to(md_root_path)
        destination_path = self.output_directory_path / relative_path

        self.__copy(source_path, destination_path)

        return relative_path

    def __copy(self, source_path: Path, destination_path: Path) -> None:
        if source_path.is_dir():
            self.__copy_tree(source_path, destination_path)
        else:
            self.__copy_file(source_path, destination_path)

    def __copy_tree(self, source_path: Path, destination_path: Path) -> None:
        overwrite = destination_path.exists()
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)

        action = "Overwritten" if overwrite else "Copied"
        logger.debug(
            f"{action} directory '{source_path.absolute()}' to '{destination_path.absolute()}'",
        )

    def __copy_file(self, source_path: Path, destination_path: Path) -> None:
        overwrite = destination_path.exists()
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_path, destination_path)

        action = "Overwritten" if overwrite else "Copied"
        logger.debug(
            f"{action} file '{source_path.absolute()}' to '{destination_path.absolute()}'",
        )

    def __find_all_links(self, markdown_content: str) -> set[str]:
        html_content = markdown.markdown(markdown_content, extensions=["extra"])
        soup = BeautifulSoup(html_content, "html.parser")

        found_links = set()

        for link in soup.find_all("a", href=True):
            if not link.find_parents(["code", "pre"]):
                found_links.add(link["href"])

        for link in soup.find_all("img", src=True):
            if not link.find_parents(["code", "pre"]):
                found_links.add(link["src"])

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            if match := HTML_BACKGROUND_IMAGE_REGEX.search(comment):
                found_links.add(match.group("location"))

        return found_links

import datetime
import logging
import shutil
import time
from copy import deepcopy
from dataclasses import dataclass
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any

import frontmatter  # type: ignore[import-untyped]
from jinja2 import Template
from emoji import emojize
from natsort import natsorted
from omegaconf import DictConfig, OmegaConf

from mkslides.config import Config, FRONTMATTER_ALLOWED_KEYS
from mkslides.preprocess import load_preprocessing_function
from mkslides.urltype import URLType
from mkslides.utils import get_url_type

from .constants import (
    DEFAULT_INDEX_TEMPLATE,
    DEFAULT_SLIDESHOW_TEMPLATE,
    HIGHLIGHTJS_THEMES_RESOURCE,
    LOCAL_JINJA2_ENVIRONMENT,
    OUTPUT_ASSETS_DIRNAME,
    REVEALJS_RESOURCE,
    REVEALJS_THEMES_RESOURCE,
)

logger = logging.getLogger(__name__)


@dataclass
class MdFileToProcess:
    source_path: Path
    destination_path: Path
    slide_config: Config
    markdown_content: str
    title: str | None = None


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
        self.output_themes_path = self.output_assets_path / "themes"
        self.output_favicons_path = self.output_assets_path / "favicons"

        self.strict = strict

        self.preprocess_script_func = (
            load_preprocessing_function(self.global_config.slides.preprocess_script)
            if self.global_config.slides.preprocess_script
            else None
        )

    def process_markdown(self) -> None:
        logger.debug("Processing markdown")
        start_time = time.perf_counter()
        self.__create_or_clear_output_directory()
        self.__process_markdown_directory()
        end_time = time.perf_counter()
        logger.info(
            f"Finished processing markdown in {end_time - start_time:.2f} seconds",
        )

    ################################################################################

    def __create_or_clear_output_directory(self) -> None:
        """
        Clears or creates the output directory and copies reveal.js.
        """
        if self.output_directory_path.exists():
            shutil.rmtree(self.output_directory_path)
            logger.debug("Output directory already exists, deleted")

        self.output_directory_path.mkdir(parents=True, exist_ok=True)
        logger.debug("Output directory created")

        with resources.as_file(REVEALJS_RESOURCE) as revealjs_path:
            self.__copy(revealjs_path, self.output_revealjs_path)

    def __process_markdown_directory(self) -> None:
        logger.debug(
            f"Processing markdown directory at '{self.md_root_path.absolute()}'"
        )

        md_files = []

        for file in self.md_root_path.rglob("*"):
            if file.is_file():
                file = file.resolve(strict=True)
                if file.suffix == ".md":
                    destination_path = self.output_directory_path / file.relative_to(
                        self.md_root_path
                    ).with_suffix(".html")

                    content = file.read_text(encoding="utf-8-sig")
                    metadata, markdown_content = frontmatter.parse(content)
                    if self.preprocess_script_func:
                        markdown_content = self.preprocess_script_func(markdown_content)
                    markdown_content = emojize(markdown_content, language="alias")

                    slide_config = self.__generate_slide_config(metadata)
                    logger.debug(metadata)
                    logger.debug(slide_config)

                    md_file_data = MdFileToProcess(
                        source_path=file,
                        destination_path=destination_path,
                        slide_config=slide_config,
                        markdown_content=markdown_content,
                        title=metadata.get("title", None),
                    )

                    md_files.append(md_file_data)
                else:
                    self.__copy(
                        file,
                        self.output_directory_path
                        / file.relative_to(self.md_root_path),
                    )

        templates, revealjs_themes, highlight_themes = self.__preprocess_slide_configs(
            md_files
        )

        for md_file_data in md_files:
            slide_config = md_file_data.slide_config

            slideshow_template = None
            if template_config := slide_config.slides.template:
                slideshow_template = templates[template_config]
            else:
                slideshow_template = DEFAULT_SLIDESHOW_TEMPLATE

            relative_theme_path = None
            if slide_config.slides.theme in revealjs_themes:
                relative_theme_path = revealjs_themes[
                    slide_config.slides.theme
                ].relative_to(
                    md_file_data.destination_path.parent,
                    walk_up=True,
                )
            else:
                relative_theme_path = slide_config.slides.theme

            relative_highlight_theme_path = None
            if slide_config.slides.highlight_theme in highlight_themes:
                relative_highlight_theme_path = highlight_themes[
                    slide_config.slides.highlight_theme
                ].relative_to(
                    md_file_data.destination_path.parent,
                    walk_up=True,
                )
            else:
                relative_highlight_theme_path = slide_config.slides.highlight_theme

            relative_revealjs_path = self.output_revealjs_path.relative_to(
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
                theme=relative_theme_path,
                highlight_theme=relative_highlight_theme_path,
                revealjs_path=relative_revealjs_path,
                markdown_data_options=markdown_data_options,
                markdown=md_file_data.markdown_content,
                revealjs_config=OmegaConf.to_container(slide_config.revealjs),
                plugins=slide_config.plugins,
            )

            self.__create_or_overwrite_file(md_file_data.destination_path, markup)

        self.__generate_index(md_files)

    def __preprocess_slide_configs(self, md_files: list[MdFileToProcess]) -> tuple[
        dict[str, Template],
        dict[str, Path],
        dict[str, Path],
    ]:
        templates = {}
        revealjs_themes = {}
        highlight_themes = {}
        for md_file_data in md_files:
            template = md_file_data.slide_config.slides.template
            if template and template not in templates:
                templates[template] = LOCAL_JINJA2_ENVIRONMENT.get_template(template)
                logger.debug(f"Loaded custom template '{template}'")

            theme = md_file_data.slide_config.slides.theme
            if (
                theme not in revealjs_themes
                and not get_url_type(theme) == URLType.ABSOLUTE
                and not theme.endswith(".css")
            ):
                with resources.as_file(
                    REVEALJS_THEMES_RESOURCE.joinpath(theme)
                ) as builtin_theme_path:
                    theme_path = builtin_theme_path.with_suffix(".css").resolve(
                        strict=True
                    )
                    theme_output_path = self.output_themes_path / theme_path.name
                    self.__copy(theme_path, theme_output_path)
                    revealjs_themes[theme] = theme_output_path

            highlight_theme = md_file_data.slide_config.slides.highlight_theme
            if (
                highlight_theme not in highlight_themes
                and not get_url_type(highlight_theme) == URLType.ABSOLUTE
                and not highlight_theme.endswith(".css")
            ):
                with resources.as_file(
                    HIGHLIGHTJS_THEMES_RESOURCE.joinpath(highlight_theme)
                ) as builtin_theme_path:
                    theme_path = builtin_theme_path.with_suffix(".css").resolve(
                        strict=True
                    )
                    theme_output_path = self.output_themes_path / theme_path.name
                    self.__copy(theme_path, theme_output_path)
                    highlight_themes[highlight_theme] = theme_output_path

        return templates, revealjs_themes, highlight_themes

    def __generate_slide_config(self, metadata) -> DictConfig:
        """
        Generate the slide configuration by merging the metadata retrieved from the frontmatter of the markdown and the global configuration.
        """
        slide_config: DictConfig = deepcopy(self.global_config)

        if metadata:
            for key in FRONTMATTER_ALLOWED_KEYS:
                if key in metadata:
                    OmegaConf.update(slide_config, key, metadata[key])

        return slide_config

    def __generate_index(self, md_files: list[MdFileToProcess]) -> None:
        logger.debug("Generating index")

        slideshows = []
        for md_file in natsorted(md_files, key=lambda x: str(x.destination_path)):
            title = md_file.title or md_file.destination_path.stem
            location = md_file.destination_path.relative_to(self.output_directory_path)
            slideshows.append(
                {
                    "title": title,
                    "location": location,
                }
            )

        index_path = self.output_directory_path / "index.html"

        # Copy the theme CSS

        relative_theme_path = None
        if theme := self.global_config.index.theme:
            if theme_output_path := self.__copy_theme(theme, REVEALJS_THEMES_RESOURCE):
                relative_theme_path = theme_output_path.relative_to(
                    index_path.parent,
                    walk_up=True,
                )

        # Refresh the templates here, so they have effect when live reloading
        index_template = None
        if template_config := self.global_config.index.template:
            index_template = LOCAL_JINJA2_ENVIRONMENT.get_template(template_config)
        else:
            index_template = DEFAULT_INDEX_TEMPLATE

        content = index_template.render(
            favicon=self.global_config.index.favicon,
            title=self.global_config.index.title,
            theme=relative_theme_path,
            slideshows=slideshows,
            build_datetime=datetime.datetime.now(tz=datetime.timezone.utc),
        )
        self.__create_or_overwrite_file(index_path, content)

    def __create_or_overwrite_file(self, destination_path: Path, content: Any) -> None:
        """
        Create or overwrite a file with the given content.
        """
        is_overwrite = destination_path.exists()

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        destination_path.write_text(content, encoding="utf-8")

        action = "Overwritten" if is_overwrite else "Created"
        logger.debug(f"{action} file '{destination_path}'")

    def __copy(self, source_path: Path, destination_path: Path) -> None:
        """
        Copy a file or directory from the source path to the destination path.
        """
        is_overwrite = destination_path.exists()
        is_directory = source_path.is_dir()

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        if is_directory:
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
        else:
            shutil.copy(source_path, destination_path)

        action = "Overwritten" if is_overwrite else "Copied"
        type = "directory" if is_directory else "file"
        logger.debug(
            f"{action} {type} '{source_path.absolute()}' to '{destination_path.absolute()}'",
        )

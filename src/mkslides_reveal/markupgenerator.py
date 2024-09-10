import datetime
from importlib.resources.abc import Traversable
import frontmatter
import logging
import shutil
import time

from importlib import resources
from pathlib import Path
from urllib.parse import urlparse

from .config import Config
from .constants import (
    HTML_BACKGROUND_IMAGE_REGEX,
    HTML_IMAGE_REGEX,
    MD_LINK_REGEX,
    REVEALJS_RESOURCE,
    REVEALJS_THEMES_RESOURCE,
    HIGHLIGHTJS_THEMES_RESOURCE,
    DEFAULT_INDEX_TEMPLATE,
    DEFAULT_SLIDESHOW_TEMPLATE,
    LOCAL_JINJA2_ENVIRONMENT,
)

logger = logging.getLogger(__name__)


class MarkupGenerator:
    def __init__(
        self,
        config: Config,
        output_directory_path: Path,
    ):

        # Config

        self.config = config

        # Paths

        self.output_directory_path = output_directory_path.resolve(strict=False)
        logger.info(
            f'Requested output directory: "{self.output_directory_path.absolute()}"'
        )

        self.output_assets_path = self.output_directory_path / "assets"
        self.output_revealjs_path = self.output_assets_path / "reveal-js"

    def clear_output_directory(self) -> None:
        for item in self.output_directory_path.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        logger.info("Output directory cleared")

    def create_output_directory(self) -> None:
        if self.output_directory_path.exists():
            self.clear_output_directory()
        else:
            self.output_directory_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Output directory created")

        with resources.as_file(REVEALJS_RESOURCE) as REVEALJS_PATH:
            self.__copy(REVEALJS_PATH, self.output_revealjs_path)

    def process_markdown(self, input_path: Path) -> None:
        logger.info(f"Processing markdown")
        start_time = time.perf_counter()

        if input_path.is_dir():
            self.__process_markdown_directory(input_path)
        else:
            _, output_markup_path = self.__process_markdown_file(input_path, input_path.parent)
            original_output_markup_path = output_markup_path

            if output_markup_path.stem != "index":
                output_markup_path.rename(output_markup_path.with_stem("index"))
                logger.info(f'Renamed "{original_output_markup_path.absolute()}" to "{output_markup_path.absolute()}" as it was the only Markdown file')

        end_time = time.perf_counter()
        logger.info(
            f"Finished processing markdown in {end_time - start_time:.2f} seconds"
        )

    ################################################################################

    def __process_markdown_file(
        self,
        md_file: Path,
        md_root_path: Path,
    ) -> tuple[dict, Path]:
        md_file = md_file.resolve(strict=True)
        md_root_path = md_root_path.resolve(strict=True)

        logger.info(f'Processing markdown file at "{md_file.absolute()}"')

        # Retrieve the frontmatter metadata and the markdown content

        content = md_file.read_text()
        metadata, markdown = frontmatter.parse(content)

        # Get the relative path of reveal.js

        output_markup_path = self.output_directory_path / md_file.relative_to(
            md_root_path
        )

        output_markup_path = output_markup_path.with_suffix(".html")
        relative_revealjs_path = self.output_revealjs_path.relative_to(
            output_markup_path.parent, walk_up=True
        )

        revealjs_config = self.config.get("reveal.js")

        # Copy the theme CSS

        relative_theme_path = None
        if theme := self.config.get("slides", "theme"):
            relative_theme_path = self.__copy_theme(
                output_markup_path, theme, REVEALJS_THEMES_RESOURCE
            )

        # Copy the highlight CSS

        relative_highlight_theme_path = None
        if theme := self.config.get("slides", "highlight_theme"):
            relative_highlight_theme_path = self.__copy_theme(
                output_markup_path, theme, HIGHLIGHTJS_THEMES_RESOURCE
            )

        # Copy the favicon

        relative_favicon_path = None
        if favicon := self.config.get("slides", "favicon"):
            relative_favicon_path = self.__copy_favicon(output_markup_path, favicon)

        # Retrieve the 3rd party plugins

        plugins = self.config.get("plugins")

        # Generate the markup from markdown

        # Refresh the templates here, so they have effect when live reloading
        slideshow_template = None
        if template_config := self.config.get("slides", "template"):
            slideshow_template = LOCAL_JINJA2_ENVIRONMENT.get_template(template_config)
        else:
            slideshow_template = DEFAULT_SLIDESHOW_TEMPLATE

        # https://revealjs.com/markdown/#external-markdown
        markdown_data_options = {}
        for option in [
            "separator",
            "separator_vertical",
            "separator_notes",
            "charset",
        ]:
            if value := self.config.get("slides", option):
                markdown_data_options[option.replace("_", "-")] = value

        markup = slideshow_template.render(
            favicon=relative_favicon_path,
            theme=relative_theme_path,
            highlight_theme=relative_highlight_theme_path,
            revealjs_path=relative_revealjs_path,
            markdown_data_options=markdown_data_options,
            markdown=markdown,
            revealjs_config=revealjs_config,
            plugins=plugins,
        )
        self.__create_file(output_markup_path, markup)

        # Copy local files

        self.__copy_local_files(md_file, md_root_path, markdown)

        return metadata, output_markup_path

    def __process_markdown_directory(self, md_root_path: Path) -> None:
        md_root_path = md_root_path.resolve(strict=True)
        logger.info(f"Processing markdown directory at {md_root_path.absolute()}")
        slideshows = []
        for md_file in md_root_path.glob("**/*.md"):
            (metadata, output_markup_path) = self.__process_markdown_file(md_file, md_root_path)

            slideshows.append(
                {
                    "title": metadata.get("title", md_file.stem),
                    "location": output_markup_path.relative_to(
                        self.output_directory_path
                    ),
                }
            )

        logger.info(f"Generating index")

        index_path = self.output_directory_path / "index.html"

        # Copy the theme

        relative_theme_path = None
        if theme := self.config.get("index", "theme"):
            relative_theme_path = self.__copy_theme(index_path, theme)

        # Copy the favicon

        relative_favicon_path = None
        if favicon := self.config.get("index", "favicon"):
            relative_favicon_path = self.__copy_favicon(index_path, favicon)

        # Refresh the templates here, so they have effect when live reloading
        index_template = None
        if template_config := self.config.get("index", "template"):
            index_template = LOCAL_JINJA2_ENVIRONMENT.get_template(template_config)
        else:
            index_template = DEFAULT_INDEX_TEMPLATE

        content = index_template.render(
            favicon=relative_favicon_path,
            title=self.config.get("index", "title"),
            theme=relative_theme_path,
            slideshows=slideshows,
            build_datetime=datetime.datetime.now(),
        )
        self.__create_file(index_path, content)

    def __copy_local_files(self, md_file: Path, md_root_path: Path, markdown: str) -> None:
        for regex in [MD_LINK_REGEX, HTML_IMAGE_REGEX, HTML_BACKGROUND_IMAGE_REGEX]:
            for m in regex.finditer(markdown):
                location = m.group("location")

                if not self.__is_absolute_url(location):
                    image = Path(md_file.parent, location).resolve(strict=True)
                    self.__copy_to_output_relative_to_md_root(image, md_root_path)

    def __copy_theme(
        self,
        file_using_theme_path: Path,
        theme: str,
        default_theme_resource: Traversable = None,
    ) -> Path | str:
        if self.__is_absolute_url(theme):
            logger.info(
                f'Using theme "{theme}" from an absolute URL, no copy necessary'
            )
            return theme

        theme_path = None
        if not theme.endswith(".css"):
            assert default_theme_resource is not None
            with resources.as_file(
                default_theme_resource.joinpath(theme)
            ) as theme_path:
                theme_path = theme_path.with_suffix(".css").resolve(strict=True)
                logger.info(
                    f'Using built-in theme "{theme}" from "{theme_path.absolute()}"'
                )
        else:
            theme_path = Path(theme).resolve(strict=True)
            logger.info(f'Using theme "{theme_path.absolute()}"')

        theme_output_path = self.output_assets_path / theme_path.name
        self.__copy_to_output(theme_path, theme_output_path)

        relative_theme_path = theme_output_path.relative_to(
            file_using_theme_path.parent, walk_up=True
        )

        return relative_theme_path

    def __copy_favicon(self, file_using_favicon_path: Path, favicon: str) -> Path | str:
        if self.__is_absolute_url(favicon):
            logger.info(
                f'Using favicon "{favicon}" from an absolute URL, no copy necessary'
            )
            return favicon

        favicon_path = Path(favicon).resolve(strict=True)
        logger.info(f'Using favicon "{favicon_path.absolute()}"')

        favicon_output_path = self.output_assets_path / favicon_path.name
        self.__copy_to_output(favicon_path, favicon_output_path)

        relative_favicon_path = favicon_output_path.relative_to(
            file_using_favicon_path.parent, walk_up=True
        )

        return relative_favicon_path

    ################################################################################

    def __create_file(self, destination_path: Path, content: any) -> None:
        if destination_path.exists():
            destination_path.write_text(content)
            logger.info(f'Overwritten: "{destination_path}"')
        else:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            destination_path.write_text(content)
            logger.info(f'Created file "{destination_path}"')

    def __copy_to_output(self, source_path: Path, destination_path: Path) -> Path:
        self.__copy(source_path, destination_path)
        relative_path = destination_path.relative_to(self.output_directory_path)
        return relative_path

    def __copy_to_output_relative_to_md_root(self, source_path: Path, md_root_path: Path) -> Path:
        source_path = source_path.resolve(strict=True)
        if not source_path.is_relative_to(md_root_path):
            logger.warning(
                f'"{source_path.absolute()}" is outside the markdown root directory, skipped!"'
            )
            return

        relative_path = source_path.relative_to(md_root_path)
        destination_path = self.output_directory_path / relative_path

        self.__copy(source_path, destination_path)

        return relative_path

    def __copy(self, source_path, destination_path) -> None:
        if source_path.is_dir():
            self.__copy_tree(source_path, destination_path)
        else:
            self.__copy_file(source_path, destination_path)

    def __copy_tree(self, source_path, destination_path) -> None:
        overwrite = destination_path.exists()
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)

        action = "Overwritten" if overwrite else "Copied"
        logger.info(
            f'{action} directory "{source_path.absolute()}" to "{destination_path.absolute()}"'
        )

    def __copy_file(self, source_path, destination_path) -> None:
        overwrite = destination_path.exists()
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_path, destination_path)

        action = "Overwritten" if overwrite else "Copied"
        logger.info(
            f'{action} file "{source_path.absolute()}" to "{destination_path.absolute()}"'
        )

    def __is_absolute_url(self, url: str) -> bool:
        return bool(urlparse(url).scheme)

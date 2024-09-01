import datetime
import frontmatter
import jinja2
import logging
import shutil

from pathlib import Path

from config import Config
from constants import HTML_BACKGROUND_IMAGE_REGEX, HTML_IMAGE_REGEX, MD_IMAGE_REGEX
from copier import Copier

logger = logging.getLogger(__name__)


class MarkupGenerator:
    def __init__(
        self,
        jinja2_environment: jinja2.Environment,
        config: Config,
        copier: Copier,
    ):
        self.slideshow_template = jinja2_environment.get_template(
            "slideshow.html.jinja"
        )
        self.index_template = jinja2_environment.get_template("index.html.jinja")
        self.config = config
        self.copier = copier

    def process_markdown_file(
        self,
        md_file: Path,
    ) -> tuple[dict, Path]:
        # Retrieve the frontmatter metadata and the markdown content

        content = md_file.read_text()
        metadata, markdown = frontmatter.parse(content)

        # Get the relative path of reveal.js

        output_markup_path = self.output_directory / md_file.relative_to(
            self.copier.md_root_directory
        )
        output_markup_path = output_markup_path.with_suffix(".html")
        relative_revealjs_path = self.output_revealjs_path.relative_to(
            output_markup_path.parent, walk_up=True
        )

        revealjs_config = self.config.get("reveal.js")
        logger.info(f'Using reveal.js config: "{revealjs_config}"')

        # Copy the theme CSS

        # TODO: What if it is an url?

        theme_path = Path(self.config.get("reveal-py", "slides", "theme")).resolve(
            strict=True
        )
        logger.info(f'Using theme "{theme_path}" for the slide')

        output_theme_path = self.output_assets_path / theme_path.name
        if not output_theme_path.exists():
            shutil.copy(theme_path, output_theme_path)
            logger.info(
                f'Copied "{theme_path.absolute()}" to "{output_theme_path.absolute()}"'
            )
        else:
            logger.warning(
                f'"{output_theme_path.absolute()}" already exists, skipped!"'
            )
        relative_theme_path = output_theme_path.relative_to(
            output_markup_path.parent, walk_up=True
        )

        # Generate the markup from markdown

        markup = self.slideshow_template.render(
            theme=relative_theme_path,
            revealjs_path=relative_revealjs_path,
            markdown=markdown,
            revealjs_config=revealjs_config,
        )

        output_markup_path.parent.mkdir(parents=True, exist_ok=True)
        output_markup_path.write_text(markup)
        logger.info(
            f'Transformed "{md_file.absolute()}" into "{output_markup_path.absolute()}"'
        )

        # Copy images

        for regex in [MD_IMAGE_REGEX, HTML_IMAGE_REGEX, HTML_BACKGROUND_IMAGE_REGEX]:
            for m in regex.finditer(markdown):
                image = Path(md_file.parent, m.group("location")).resolve(strict=True)

                if not image.is_relative_to(self.copier.md_root_directory):
                    logger.warning(
                        f'"{image.absolute()}" is outside the markdown directory, skipped!"'
                    )
                else:
                    output_image_path = self.output_directory / image.relative_to(
                        self.copier.md_root_directory
                    )
                    output_image_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(image, output_image_path)
                    logger.info(
                        f'Copied "{image.absolute()}" to "{output_image_path.absolute()}"'
                    )

        return metadata, output_markup_path

    def process_markdown_directory(self) -> None:
        slideshows = []
        for md_file in self.copier.md_root_path.glob("**/*.md"):
            (metadata, output_markup_path) = self.process_markdown_file(md_file)

            slideshows.append(
                {
                    "title": metadata.get("title", md_file.stem),
                    "location": output_markup_path.relative_to(self.output_directory),
                }
            )

        self.__generate_index(slideshows)

    def __generate_index(self, slideshows: dict[dict]) -> None:

        index_path = self.output_directory / "index.html"

        # Copy the index theme CSS

        theme_path = Path(self.config.get("reveal-py", "index", "theme")).resolve(
            strict=True
        )
        logger.info(f'Using theme "{theme_path}" for the index')

        output_theme_path = self.output_assets_path / theme_path.name

        shutil.copy(theme_path, output_theme_path)
        logger.info(
            f'Copied "{theme_path.absolute()}" to "{output_theme_path.absolute()}"'
        )
        relative_theme_path = output_theme_path.relative_to(
            index_path.parent, walk_up=True
        )

        # Generate the index

        index_path.write_text(
            self.index_template.render(
                title=self.config.get("reveal-py", "index", "title"),
                theme=relative_theme_path,
                slideshows=slideshows,
                build_datetime=datetime.datetime.now(),
            )
        )
        logger.info(f'Generated index: "{index_path.absolute()}"')

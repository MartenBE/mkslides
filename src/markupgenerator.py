import datetime
import frontmatter
import jinja2
import shutil

from pathlib import Path

from constants import HTML_BACKGROUND_IMAGE_REGEX, HTML_IMAGE_REGEX, MD_IMAGE_REGEX


class MarkupGenerator:
    def __init__(
        self,
        jinja2_environment: jinja2.Environment,
        input_path: Path,
        output_directory: Path,
        revealjs_path: Path,
    ):
        self.input_path = input_path
        self.output_directory = output_directory
        self.revealjs_path = revealjs_path
        self.slideshow_template = jinja2_environment.get_template(
            "slideshow.html.jinja"
        )
        self.index_template = jinja2_environment.get_template("index.html.jinja")

    def create_markup(self) -> None:
        if self.input_path.is_file():
            print("Processing a single file")
            md_file = self.input_path
            md_directory = self.input_path.parent
            self.__process_markdown_file(
                md_file, md_directory, self.output_directory, self.revealjs_path
            )
        else:
            print("Processing a directory")
            md_directory = self.input_path
            self.__process_markdown_directory(
                md_directory, self.output_directory, self.revealjs_path
            )

    def __process_markdown_file(
        self,
        md_file: Path,
        md_directory: Path,
        output_directory: Path,
        output_revealjs_path: Path,
    ) -> tuple[dict, Path]:
        # Retrieve the frontmatter metadata and the markdown content

        content = md_file.read_text()
        metadata, markdown = frontmatter.parse(content)

        # Generate the markup from markdown

        output_markup_path = output_directory / md_file.relative_to(md_directory)
        output_markup_path = output_markup_path.with_suffix(".html")
        revealjs_path = output_revealjs_path.relative_to(
            output_markup_path.parent, walk_up=True
        )

        markup = self.slideshow_template.render(
            revealjs_path=revealjs_path,
            markdown=markdown,
        )

        output_markup_path.parent.mkdir(parents=True, exist_ok=True)
        output_markup_path.write_text(markup)
        print(
            f'Transformed "{md_file.absolute()}" into "{output_markup_path.absolute()}"'
        )

        # Copy images

        for regex in [MD_IMAGE_REGEX, HTML_IMAGE_REGEX, HTML_BACKGROUND_IMAGE_REGEX]:
            for m in regex.finditer(markdown):
                image = Path(md_file.parent, m.group("location")).resolve(strict=True)

                if not image.is_relative_to(md_directory):
                    print(
                        f'\t\tWARNING: "{image.absolute()}" is outside the markdown directory, skipped!"'
                    )
                else:
                    output_image_path = output_directory / image.relative_to(
                        md_directory
                    )
                    output_image_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(image, output_image_path)
                    print(
                        f'\t\tCopied "{image.absolute()}" to "{output_image_path.absolute()}"'
                    )

        return metadata, output_markup_path

    def __process_markdown_directory(
        self, md_directory: Path, output_directory: Path, revealjs_path: Path
    ) -> None:
        slideshows = []
        for md_file in md_directory.glob("**/*.md"):
            (metadata, output_markup_path) = self.__process_markdown_file(
                md_file, md_directory, output_directory, revealjs_path
            )

            slideshows.append(
                {
                    "title": metadata.get("title", md_file.stem),
                    "location": output_markup_path.relative_to(output_directory),
                }
            )

        # Generate the index

        index_path = output_directory / "index.html"
        index_path.write_text(
            self.index_template.render(
                slideshows=slideshows, build_datetime=datetime.datetime.now()
            )
        )
        print(f'Generated index: "{index_path.absolute()}"')

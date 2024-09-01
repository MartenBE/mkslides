import logging
import shutil

from pathlib import Path

logger = logging.getLogger(__name__)


class Copier:
    """
    The Copier class is responsible for creating and copying files and directories into the output folder.

    It is also responsible for (recreating) the output directory and copying the reveal.js assets to the output directory.

    What comes from the markdown root directory is copied to the output directory using the same folder structure.
    Thus, the output directory will have the same structure as the markdown root directory.
    """

    def __init__(self, input_path: Path, output_directory_path: Path):
        input_path = input_path.resolve(strict=True)
        if input_path.is_dir():
            self.md_root_path = input_path
        else:
            self.md_root_path = input_path.parent
        logger.info(f'Markdown root directory: "{self.md_root_path.absolute()}"')

        self.output_directory_path = output_directory_path.resolve(strict=True)
        logger.info(
            f'Requested output directory: "{self.output_directory_path.absolute()}"'
        )

        self.assets_path = Path("assets").resolve(strict=True)
        self.revealjs_path = Path(self.assets_path / "reveal.js-master").resolve(
            strict=True
        )

        self.output_assets_path = self.output_directory_path / "assets"
        self.output_revealjs_path = self.output_assets_path / "reveal-js"

    def create_output_directory(self) -> None:
        if self.output_directory_path.exists():
            shutil.rmtree(self.output_directory_path)
            logger.info("Output directory already exists: deleted")

        self.output_directory_path.mkdir()
        logger.info(f"Output directory created")

        self.__copytree(self.revealjs_path, self.output_revealjs_path)

    def create_output_file(self, destination_path: Path, content: any) -> None:
        destination_path = destination_path.resolve(strict=True)
        pass

    def copy_from_anywhere(self, source_path: Path, destination_path: Path) -> None:
        source_path = source_path.resolve(strict=True)
        destination_path = destination_path.resolve(strict=True)
        pass

    def copy_relative_to_md_root(
        self, source_path: Path, destination_path: Path
    ) -> None:
        source_path = source_path.resolve(strict=True)
        destination_path = destination_path.resolve(strict=True)
        pass

    def __copytree(self, source_path, destination_path) -> None:
        shutil.copytree(source_path, destination_path)
        logger.info(
            f'Copied directory "{source_path.absolute()}" to "{destination_path.absolute()}"'
        )

    def __copyfile(self, source_path, destination_path) -> bool:
        if destination_path.exists():
            logger.warning(f'"{destination_path.absolute()}" already exists, skipped!"')
            return False

        shutil.copy(source_path, destination_path)
        logger.info(
            f'Copied file "{source_path.absolute()}" to "{destination_path.absolute()}"'
        )
        return True

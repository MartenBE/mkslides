import logging
from pathlib import Path

from omegaconf import DictConfig

from mkslides.markupgenerator import MarkupGenerator

logger = logging.getLogger(__name__)


def build(
    config: DictConfig,
    input_path: Path,
    output_path: Path,
    strict: bool,
) -> None:
    markup_generator = MarkupGenerator(config, output_path, strict)
    markup_generator.create_or_clear_output_directory()
    markup_generator.process_markdown(input_path)

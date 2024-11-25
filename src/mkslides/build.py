import logging
from pathlib import Path
from mkslides.config import get_config
from mkslides.markupgenerator import MarkupGenerator

logger = logging.getLogger(__name__)


def build(
    config_path: Path, input_path: Path, output_path: Path
) -> None:
    config = get_config(config_path)
    markup_generator = MarkupGenerator(config, output_path)
    markup_generator.create_or_clear_output_directory()
    markup_generator.process_markdown(input_path)

from pathlib import Path

import pytest

from mkslides.config import Config
from mkslides.markupgenerator import MarkupGenerator


@pytest.fixture
def setup_markup_generator() -> None:
    config = Config()
    output_path = Path("tests/site")
    markup_generator = MarkupGenerator(config, output_path)
    markup_generator.create_output_directory()
    return markup_generator, output_path

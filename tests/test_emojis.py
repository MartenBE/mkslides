from pathlib import Path
from typing import Any

from tests.utils import assert_html_contains


def test_emojize(setup_markup_generator: Any) -> None:
    markup_generator, output_path = setup_markup_generator
    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains(
        output_path / "someslides.html",
        [
            "⚠️",
            "👍",
        ],
    )

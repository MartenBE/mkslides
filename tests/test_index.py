from pathlib import Path
from typing import Any

from tests.utils import assert_html_contains


def test_index_title(setup_markup_generator: Any) -> None:
    markup_generator, output_path = setup_markup_generator
    markup_generator.config.merge_config_from_dict(
        {
            "index": {
                "title": "Lorem ipsum",
            },
        },
    )

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains(
        output_path / "index.html",
        [
            "<title>Lorem ipsum</title>",
            "<h1>Lorem ipsum</h1>",
        ],
    )

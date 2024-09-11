import re
from pathlib import Path
from typing import Any

from tests.utils import assert_html_contains_regexp


def test_revealjs_markdown_data_options(setup_markup_generator: Any) -> None:
    markup_generator, output_path = setup_markup_generator
    markup_generator.config.merge_config_from_dict(
        {
            "slides": {
                "charset": "utf-8",
                "separator": r"^\s*---\s*$",
                "separator_vertical": r"^\s*-v-\s*$",
                "separator_notes": r"^Notes?:",
            },
        },
    )

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains_regexp(
        output_path / "someslides.html",
        re.compile(
            r"""
            <section\s+data-markdown
                .*?
                data-separator="\^\\s\*---\\s\*\$"
                .*?
                data-separator-vertical="\^\\s\*-v-\\s\*\$"
                .*?
                data-separator-notes="\^Notes\?:"
                .*?
                data-charset="utf-8"
                .*?
            >
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )

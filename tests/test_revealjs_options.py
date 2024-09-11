import re
from pathlib import Path
from typing import Any

from tests.utils import assert_html_contains, assert_html_contains_regexp


# Necessary for livereload to work properly
def test_revealjs_default_options(setup_markup_generator: Any) -> None:
    markup_generator, output_path = setup_markup_generator

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains(
        output_path / "someslides.html",
        [
            "history: true,",
        ],
    )


def test_revealjs_integer_options(setup_markup_generator: Any) -> None:
    markup_generator, output_path = setup_markup_generator
    markup_generator.config.merge_config_from_dict(
        {
            "reveal.js": {
                "height": 1080,
                "width": 1920,
            },
        },
    )

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains_regexp(
        output_path / "someslides.html",
        re.compile(
            r"""
            Reveal\.initialize\({
                .*?
                height:\s+1080,
                .*?
                width:\s+1920,
                .*?
            }\);
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )


def test_revealjs_string_options(setup_markup_generator: Any) -> None:
    markup_generator, output_path = setup_markup_generator
    markup_generator.config.merge_config_from_dict(
        {
            "reveal.js": {
                "transition": "fade",
            },
        },
    )

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains_regexp(
        output_path / "someslides.html",
        re.compile(
            r"""
            Reveal\.initialize\({
                .*?
                transition:\s+"fade",
                .*?
            }\);
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )

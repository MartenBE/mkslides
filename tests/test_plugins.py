import re
from pathlib import Path
from typing import Any

from tests.utils import assert_html_contains, assert_html_contains_regexp


def test_plugins(setup_markup_generator: Any) -> None:
    markup_generator, output_path = setup_markup_generator
    markup_generator.config.merge_config_from_dict(
        {
            "plugins": [
                {
                    "name": "RevealMermaid",
                    "extra_javascript": [
                        "https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin/plugin/mermaid/mermaid.min.js",
                    ],
                },
                {
                    "extra_javascript": [
                        "https://cdn.jsdelivr.net/npm/reveal-plantuml/dist/reveal-plantuml.min.js",
                    ],
                },
            ],
        },
    )

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains(
        output_path / "someslides.html",
        [
            '<script src="https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin/plugin/mermaid/mermaid.min.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/reveal-plantuml/dist/reveal-plantuml.min.js"></script>',
        ],
    )

    assert_html_contains_regexp(
        output_path / "someslides.html",
        re.compile(
            r"""Reveal\.initialize\({
                .*?
                plugins:\s+\[
                    .*?
                    RevealMermaid,
                    .*?
                \]
                .*?
            }\);
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )

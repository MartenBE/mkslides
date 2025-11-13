import re
from typing import Any

from tests.utils import assert_html_contains_regexp, run_build_strict


def test_revealjs_markdown_data_options(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "markdown_data_options" / "slides"
    config_path = (
        cwd / "markdown_data_options" / "revealjs_markdown_data_options-config.yml"
    )
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains_regexp(
        output_path / "someslides-1.html",
        re.compile(
            r"""
            <section\s+data-markdown
                .*?
                \s+data-separator="\^\\s\*---\\s\*\$"\s+
                .*?
                \s+data-separator-vertical="\^\\s\*-v-\\s\*\$"\s+
                .*?
                \s+data-separator-notes="\^Notes\?:"\s+
                .*?
                \s+data-charset="utf-8"\s+
                .*?
            >
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )

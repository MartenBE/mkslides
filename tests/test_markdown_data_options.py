import re
from typing import Any

from tests.utils import assert_html_contains_regexp, run_build


def test_revealjs_markdown_data_options(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build(
        cwd,
        "test_files",
        output_path,
        "test_configs/test_revealjs_markdown_data_options.yml",
    )

    assert_html_contains_regexp(
        output_path / "someslides.html",
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

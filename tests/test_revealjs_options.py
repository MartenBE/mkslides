import re
from typing import Any

from tests.utils import (
    assert_html_contains,
    assert_html_contains_regexp,
    run_build,
    run_build_with_config,
)


# Necessary for livereload to work properly
def test_revealjs_default_options(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build(cwd, output_path)

    assert_html_contains(
        output_path / "someslides.html",
        [
            "history: true,",
        ],
    )


def test_revealjs_integer_options(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_revealjs_integer_options.yml")

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


def test_revealjs_string_options(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_revealjs_string_options.yml")

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

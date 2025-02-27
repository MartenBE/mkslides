import re
from typing import Any

from tests.utils import (
    assert_files_exist,
    assert_html_contains,
    assert_html_contains_regexp,
    run_build,
    run_build_with_config,
)


def test_frontmatter_overrides_default(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build(cwd, output_path)

    assert_html_contains(output_path / "index.html", "<td>frontmatter title</td>")

    assert_files_exist(output_path / "mkslides-assets/themes/solarized.css")
    assert_files_exist(output_path / "mkslides-assets/themes/vs.css")

    assert_html_contains(
        output_path / "frontmatter.html",
        '<link rel="stylesheet" href="mkslides-assets/themes/solarized.css" />',
    )
    assert_html_contains(
        output_path / "frontmatter.html",
        '<link rel="stylesheet" href="mkslides-assets/themes/vs.css" />',
    )

    assert_html_contains_regexp(
        output_path / "frontmatter.html",
        re.compile(
            r"""
            <section\s+data-markdown
                .*?
                \s+data-separator="<!--s-->"\s+
                .*?
            >
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )

    assert_html_contains_regexp(
        output_path / "frontmatter.html",
        re.compile(
            r"""
            Reveal\.initialize\({
                .*?
                height:\s+1080,
                .*?
                width:\s+1920,
                .*?
                transition:\s+"zoom",
                .*?
            }\);
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )


def test_frontmatter_overrides_options(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_frontmatter_overrides_options.yml")

    assert_html_contains(output_path / "index.html", "<td>frontmatter title</td>")

    assert_files_exist(output_path / "mkslides-assets/themes/solarized.css")
    assert_files_exist(output_path / "mkslides-assets/themes/vs.css")

    assert_html_contains(
        output_path / "frontmatter.html",
        '<link rel="stylesheet" href="mkslides-assets/themes/solarized.css" />',
    )
    assert_html_contains(
        output_path / "frontmatter.html",
        '<link rel="stylesheet" href="mkslides-assets/themes/vs.css" />',
    )

    assert_html_contains_regexp(
        output_path / "frontmatter.html",
        re.compile(
            r"""
            <section\s+data-markdown
                .*?
                \s+data-separator="<!--s-->"\s+
                .*?
            >
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )

    assert_html_contains_regexp(
        output_path / "frontmatter.html",
        re.compile(
            r"""
            Reveal\.initialize\({
                .*?
                height:\s+1080,
                .*?
                width:\s+1920,
                .*?
                transition:\s+"zoom",
                .*?
            }\);
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )

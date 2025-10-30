import re
from typing import Any

from tests.utils import (
    assert_files_exist,
    assert_html_contains,
    assert_html_contains_regexp,
    run_build_strict,
)


def test_frontmatter_overrides_default(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "frontmatter" / "docs"
    run_build_strict(cwd, input_path, output_path, None)

    assert_html_contains(
        output_path / "index.html",
        '<span class="node-title">frontmatter title</span>',
    )

    assert_files_exist(
        output_path / "mkslides-assets/reveal-js/dist/theme/solarized.css",
    )
    assert_files_exist(output_path / "mkslides-assets/highlight-js-themes/vs.css")

    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/theme/solarized.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/highlight-js-themes/vs.css" />',
    )

    assert_html_contains_regexp(
        output_path / "someslides-1.html",
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
        output_path / "someslides-1.html",
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
    input_path = cwd / "frontmatter" / "docs"
    config_path = cwd / "frontmatter" / "frontmatter_overrides_options-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "index.html",
        '<span class="node-title">frontmatter title</span>',
    )

    assert_files_exist(
        output_path / "mkslides-assets/reveal-js/dist/theme/solarized.css",
    )
    assert_files_exist(output_path / "mkslides-assets/highlight-js-themes/vs.css")

    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/theme/solarized.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/highlight-js-themes/vs.css" />',
    )

    assert_html_contains_regexp(
        output_path / "someslides-1.html",
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
        output_path / "someslides-1.html",
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


def test_frontmatter_paths_are_relative_to_mdfile(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "frontmatter" / "docs"
    run_build_strict(cwd, input_path, output_path, None)

    assert_html_contains(
        output_path / "someslides-2.html",
        '<link rel="icon" href="assets/favicon.ico">',
    )
    assert_html_contains(
        output_path / "someslides-2.html",
        '<link rel="stylesheet" href="assets/theme.css" />',
    )
    assert_html_contains(
        output_path / "someslides-2.html",
        '<link rel="stylesheet" href="assets/highlight-theme.css" />',
    )

    assert_html_contains(
        output_path / "somefolder" / "someslides-3.html",
        '<link rel="icon" href="../assets/favicon.ico">',
    )
    assert_html_contains(
        output_path / "somefolder" / "someslides-3.html",
        '<link rel="stylesheet" href="../assets/theme.css" />',
    )
    assert_html_contains(
        output_path / "somefolder" / "someslides-3.html",
        '<link rel="stylesheet" href="../assets/highlight-theme.css" />',
    )

    assert_html_contains(
        output_path / "somefolder" / "someslides-4.html",
        '<link rel="icon" href="favicon-2.ico">',
    )
    assert_html_contains(
        output_path / "somefolder" / "someslides-4.html",
        '<link rel="stylesheet" href="theme-2.css" />',
    )
    assert_html_contains(
        output_path / "somefolder" / "someslides-4.html",
        '<link rel="stylesheet" href="highlight-theme-2.css" />',
    )

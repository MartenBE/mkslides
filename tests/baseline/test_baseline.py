from typing import Any

from tests.utils import (
    assert_files_exist,
    assert_html_contains,
    run_build_strict,
)


def test_process_directory_without_config(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "baseline" / "docs"
    run_build_strict(cwd, input_path, output_path, None)

    assert_files_exist(output_path / "mkslides-assets/reveal-js/dist/reveal.css")
    assert_files_exist(output_path / "mkslides-assets/reveal-js/dist/reveal.js")
    assert_files_exist(
        output_path / "mkslides-assets/reveal-js/plugin/markdown/markdown.js",
    )
    assert_files_exist(
        output_path / "mkslides-assets/reveal-js/plugin/highlight/highlight.js",
    )
    assert_files_exist(output_path / "mkslides-assets/reveal-js/plugin/zoom/zoom.js")
    assert_files_exist(output_path / "mkslides-assets/reveal-js/dist/theme/black.css")
    assert_files_exist(output_path / "mkslides-assets/highlight-js-themes/monokai.css")

    assert_files_exist(output_path / "index.html")
    assert_files_exist(output_path / "someslides-1.html")
    assert_files_exist(output_path / "somefolder/someslides-2.html")

    assert_files_exist(output_path / "randomfile-1.txt")
    assert_files_exist(output_path / "somefolder/randomfile-2.txt")
    assert_files_exist(output_path / "extra/randomfile-3.txt")

    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/theme/black.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/highlight-js-themes/monokai.css" />',
    )

    assert_html_contains(
        output_path / "somefolder" / "someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder" / "someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/theme/black.css" />',
    )
    assert_html_contains(
        output_path / "somefolder" / "someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/highlight-js-themes/monokai.css" />',
    )

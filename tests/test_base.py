from typing import Any

from tests.utils import (
    assert_files_exist,
    assert_html_contains,
    run_build,
)


def test_process_directory_without_config(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build(cwd, "test_files", output_path, None)

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
    assert_files_exist(output_path / "someslides.html")
    assert_files_exist(output_path / "somefolder/someslides.html")
    assert_files_exist(output_path / "img/example-1.png")
    assert_files_exist(output_path / "img/example-2.png")
    assert_files_exist(output_path / "img/example-3.png")
    assert_files_exist(output_path / "img/example-4.png")
    assert_files_exist(output_path / "img/example-(7).png")
    assert_files_exist(output_path / "img/somefolder/example-5.png")
    assert_files_exist(output_path / "somefolder/example-6.png")
    assert_files_exist(output_path / "test-1.txt")
    assert_files_exist(output_path / "test-2.txt")
    assert_files_exist(output_path / "test-(3).txt")
    assert_files_exist(output_path / "video/demo.webm")

    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/theme/black.css" />',
    )
    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="mkslides-assets/highlight-js-themes/monokai.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/theme/black.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="../mkslides-assets/highlight-js-themes/monokai.css" />',
    )

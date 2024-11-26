from typing import Any

from tests.utils import (
    assert_files_exist,
    assert_html_contains,
    run_build,
    run_build_with_custom_input,
)


def test_process_directory_without_config(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build(cwd, output_path)

    assert_files_exist(
        output_path,
        [
            "assets/reveal-js/dist/reveal.css",
            "assets/reveal-js/dist/reveal.js",
            "assets/reveal-js/plugin/markdown/markdown.js",
            "assets/reveal-js/plugin/highlight/highlight.js",
            "assets/reveal-js/plugin/zoom/zoom.js",
            "assets/black.css",
            "assets/monokai.css",
            "index.html",
            "someslides.html",
            "somefolder/someslides.html",
            "img/example-1.png",
            "img/example-2.png",
            "img/example-3.png",
            "img/example-4.png",
            "img/example-(7).png",
            "img/somefolder/example-5.png",
            "somefolder/example-6.png",
            "test-1.txt",
            "test-2.txt",
            "test-(3).txt",
        ],
    )

    assert_html_contains(
        output_path / "someslides.html",
        [
            '<link rel="stylesheet" href="assets/reveal-js/dist/reveal.css" />',
            '<link rel="stylesheet" href="assets/black.css" />',
            '<link rel="stylesheet" href="assets/monokai.css" />',
        ],
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        [
            '<link rel="stylesheet" href="../assets/reveal-js/dist/reveal.css" />',
            '<link rel="stylesheet" href="../assets/black.css" />',
            '<link rel="stylesheet" href="../assets/monokai.css" />',
        ],
    )


def test_process_file_without_config(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_custom_input(cwd, output_path, "test_files/someslides.md")

    assert_files_exist(
        output_path,
        [
            "assets/reveal-js/dist/reveal.css",
            "assets/reveal-js/dist/reveal.js",
            "assets/reveal-js/plugin/markdown/markdown.js",
            "assets/reveal-js/plugin/highlight/highlight.js",
            "assets/reveal-js/plugin/zoom/zoom.js",
            "assets/black.css",
            "assets/monokai.css",
            "index.html",
            "img/example-1.png",
            "img/example-2.png",
            "img/example-3.png",
            "img/example-(7).png",
            "test-1.txt",
            "test-2.txt",
            "test-(3).txt",
        ],
    )

    assert not (
        output_path / "someslides.html"
    ).exists(), "someslides.html should not exist"

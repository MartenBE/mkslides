import subprocess
from typing import Any

from tests.utils import (
    assert_files_exist,
    assert_html_contains,
    run_build,
    run_build_with_custom_input,
)

# The output can be seen manually by running the following command:
#   poetry run mkslides build tests/test_files


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
            "frontmatter.html",
            "index.html",
            "indentation.html",
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
            "video/demo.webm",
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

    assert_html_contains(
        output_path / "indentation.html",
        [
"""<textarea data-template>
# Test

```text
                       : this line starts with 23 space characters
                        : this line starts with 24 space characters

```
""",
        ],
    )


def test_prevent_overwrite(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    file1_path = output_path / "test" / "test.md"
    file1_path.parent.mkdir(parents=True, exist_ok=True)
    file1_path.write_text("# Test 1")

    file2_path = output_path / "test" / "test2" / "test2.md"
    file2_path.parent.mkdir(parents=True, exist_ok=True)
    file2_path.write_text("# Test 2")

    result = subprocess.run(
        [
            "mkslides",
            "-v",
            "build",
            "-d",
            output_path,
            file1_path.parent,
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1

    result = subprocess.run(
        [
            "mkslides",
            "-v",
            "build",
            "-d",
            output_path,
            file2_path.parent,
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1

    assert_files_exist(
        output_path,
        [
            "test/test.md",
            "test/test2/test2.md",
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
            "video/demo.webm",
        ],
    )

    assert not (
        output_path / "someslides.html"
    ).exists(), "someslides.html should not exist"

from typing import Any

from tests.utils import (
    assert_html_contains,
    run_build_strict,
)


def test_process_directory_without_config(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "relative_slideshow_links" / "slides"
    run_build_strict(cwd, input_path, output_path, None)

    assert_html_contains(output_path / "someslides-1.html", "[](someslides-2.html)")
    assert_html_contains(output_path / "someslides-1.html", "[](./someslides-2.html)")
    assert_html_contains(output_path / "someslides-1.html", "[test](someslides-2.html)")
    assert_html_contains(
        output_path / "someslides-1.html",
        "[test](./someslides-2.html)",
    )

    assert_html_contains(
        output_path / "someslides-1.html",
        '<a href="someslides-2.html">test</a>',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<a href="./someslides-2.html">test</a>',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<a target="_blank" href="someslides-2.html" class="dummy">test</a>',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<a target="_blank" href="./someslides-2.html" class="dummy">test</a>',
    )

    assert_html_contains(
        output_path / "someslides-1.html",
        "[](category-1/someslides-3.html)",
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        "[](./category-1/someslides-3.html)",
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        "[test](category-1/someslides-3.html)",
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        "[test](./category-1/someslides-3.html)",
    )

    assert_html_contains(
        output_path / "someslides-1.html",
        '<a href="category-1/someslides-3.html">test</a>',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<a href="./category-1/someslides-3.html">test</a>',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<a target="_blank" href="category-1/someslides-3.html" class="dummy">test</a>',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<a target="_blank" href="./category-1/someslides-3.html" class="dummy">test</a>',
    )

    assert_html_contains(
        output_path / "someslides-1.html",
        "[](https://example.com/test.md)",
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        "[test](https://example.com/test.md)",
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<a href="https://example.com/test.md">test</a>',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<a target="_blank" href="https://example.com/test.md" class="dummy">test</a>',
    )

    assert_html_contains(
        output_path / "someslides-1.html",
        "[](/folder/test.md)",
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        "[test](/folder/test.md)",
    )

    assert_html_contains(
        output_path / "someslides-1.html",
        '<a href="/folder/test.md">test</a>',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<a target="_blank" href="/folder/test.md" class="dummy">test</a>',
    )


# import subprocess
# from typing import Any


# def test_process_file_without_config(setup_paths: Any) -> None:
#     cwd, output_path = setup_paths
#     input_path = cwd / "strict" / "slides"

#     result = subprocess.run(
#         [
#             "mkslides",
#             "-v",
#             "build",
#             "-s",
#             "-d",
#             output_path,
#             input_path,
#         ],
#         cwd=cwd,
#         capture_output=True,
#         text=True,
#         check=False,
#     )

#     print(result.stdout)

#     assert result.returncode == 1

#     assert (
#         "Local file './some-random-md-link' mentioned in '/home/martijn/git/mkslides/tests/test_files_crash/strict.md' not found."
#         in result.stderr
#     )

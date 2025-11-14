import re
import subprocess
from typing import Any

from tests.utils import (
    assert_html_contains,
    run_build_strict,
)


def test_relative_slideshow_links(setup_paths: Any) -> None:
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


def test_relative_slideshow_links_without_strict(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    expected_returncode = 0

    input_path = cwd / "relative_slideshow_links" / "slides-fail-1"
    result = subprocess.run(
        [
            "mkslides",
            "-v",
            "build",
            "-d",
            output_path,
            input_path,
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == expected_returncode
    assert re.search(
        r"WARNING\s*Relative\s*slideshow\s*link\s*'non-existing-file\.md'\s*in\s*file\s*'.*/someslides-1.md'\s*does\s*not\s*exist",
        result.stdout,
        flags=re.DOTALL,
    )

    input_path = cwd / "relative_slideshow_links" / "slides-fail-2"
    result = subprocess.run(
        [
            "mkslides",
            "-v",
            "build",
            "-d",
            output_path,
            input_path,
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == expected_returncode
    assert re.search(
        r"WARNING\s+Relative\s+slideshow\s+link\s+'non-existing-file\.md'\s+in\s+file\s+'.*/someslides-1.md'\s+does\s+not\s+exist",
        result.stdout,
        flags=re.DOTALL,
    )


def test_relative_slideshow_links_with_strict(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    expected_returncode = 1

    input_path = cwd / "relative_slideshow_links" / "slides-fail-1"
    result = subprocess.run(
        [
            "mkslides",
            "-v",
            "build",
            "-s",
            "-d",
            output_path,
            input_path,
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == expected_returncode
    assert re.search(
        r"FileNotFoundError:\s+Relative\s+slideshow\s+link\s+'non-existing-file\.md'\s+in\s+file\s+'.*/someslides-1\.md'\s+does\s+not\s+exist",
        result.stderr,
    )

    input_path = cwd / "relative_slideshow_links" / "slides-fail-2"
    result = subprocess.run(
        [
            "mkslides",
            "-v",
            "build",
            "-s",
            "-d",
            output_path,
            input_path,
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == expected_returncode
    assert re.search(
        r"FileNotFoundError:\s+Relative\s+slideshow\s+link\s+'non-existing-file\.md'\s+in\s+file\s+'.*/someslides-1\.md'\s+does\s+not\s+exist",
        result.stderr,
    )

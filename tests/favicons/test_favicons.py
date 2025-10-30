from typing import Any

from tests.utils import assert_html_contains, run_build_strict


def test_absolute_url_index_favicon_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "favicons" / "docs"
    config_path = cwd / "favicons" / "absolute_url_index_favicon_path-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "index.html",
        '<link rel="icon" href="https://hogenttin.github.io/cdn/favicon/favicon.ico">',
    )


def test_absolute_url_slideshow_favicon_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "favicons" / "docs"
    config_path = cwd / "favicons" / "absolute_url_slideshow_favicon_path-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="icon" href="https://hogenttin.github.io/cdn/favicon/favicon.ico">',
    )

    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="icon" href="https://hogenttin.github.io/cdn/favicon/favicon.ico">',
    )


def test_local_index_favicon_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "favicons" / "docs"
    config_path = cwd / "favicons" / "local_index_favicon_path-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "index.html",
        '<link rel="icon" href="assets/favicon.ico">',
    )


def test_local_slideshow_favicon_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "favicons" / "docs"
    config_path = cwd / "favicons" / "local_slideshow_favicon_path-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="icon" href="assets/favicon.ico">',
    )

    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="icon" href="../assets/favicon.ico">',
    )

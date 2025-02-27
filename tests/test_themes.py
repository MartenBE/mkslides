from typing import Any

from tests.utils import assert_files_exist, assert_html_contains, run_build_with_config


def test_local_slideshow_theme_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_local_slideshow_theme_path.yml")

    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="mkslides-assets/themes/theme.css" />',
    )
    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="mkslides-assets/themes/highlight-theme.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="../mkslides-assets/themes/theme.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="../mkslides-assets/themes/highlight-theme.css" />',
    )


def test_absolute_url_slideshow_theme_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(
        cwd,
        output_path,
        "test_absolute_url_slideshow_theme_path.yml",
    )

    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="https://example.org/theme.css" />',
    )
    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="https://example.org/highlight-theme.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="https://example.org/theme.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="https://example.org/highlight-theme.css" />',
    )


def test_builtin_slideshow_theme_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_builtin_slideshow_theme_path.yml")

    assert_files_exist(output_path / "mkslides-assets/themes/simple.css")

    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="mkslides-assets/themes/simple.css" />',
    )
    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="stylesheet" href="mkslides-assets/themes/vs.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="../mkslides-assets/themes/simple.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="stylesheet" href="../mkslides-assets/themes/vs.css" />',
    )


def test_local_index_theme_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_local_index_theme_path.yml")

    assert_html_contains(
        output_path / "index.html",
        '<link rel="stylesheet" href="mkslides-assets/themes/theme.css" />',
    )


def test_absolute_url_index_theme_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_absolute_url_index_theme_path.yml")

    assert_html_contains(
        output_path / "index.html",
        '<link rel="stylesheet" href="https://example.org/theme.css" />',
    )


def test_absolute_url_index_favicon_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_absolute_url_index_favicon_path.yml")

    assert_html_contains(
        output_path / "index.html",
        '<link rel="icon" href="https://hogenttin.github.io/cdn/favicon/favicon.ico">',
    )


def test_absolute_url_slideshow_favicon_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(
        cwd,
        output_path,
        "test_absolute_url_slideshow_favicon_path.yml",
    )

    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="icon" href="https://hogenttin.github.io/cdn/favicon/favicon.ico">',
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="icon" href="https://hogenttin.github.io/cdn/favicon/favicon.ico">',
    )


def test_local_index_favicon_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_local_index_favicon_path.yml")

    assert_html_contains(
        output_path / "index.html",
        '<link rel="icon" href="mkslides-assets/favicon.ico">',
    )


def test_local_slideshow_favicon_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_local_slideshow_favicon_path.yml")

    assert_html_contains(
        output_path / "someslides.html",
        '<link rel="icon" href="mkslides-assets/favicon.ico">',
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        '<link rel="icon" href="../mkslides-assets/favicon.ico">',
    )

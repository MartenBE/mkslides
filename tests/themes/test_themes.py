from typing import Any

from tests.utils import assert_files_exist, assert_html_contains, run_build_strict


def test_local_slideshow_theme_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "themes" / "slides"
    config_path = cwd / "themes" / "local_slideshow_theme_path-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="assets/theme.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="assets/highlight-theme.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="stylesheet" href="../assets/theme.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="stylesheet" href="../assets/highlight-theme.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides-3.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides-3.html",
        '<link rel="stylesheet" href="theme-3.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides-3.html",
        '<link rel="stylesheet" href="highlight-theme-3.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides-4.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides-4.html",
        '<link rel="stylesheet" href="../assets-2/theme-2.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides-4.html",
        '<link rel="stylesheet" href="../assets-2/highlight-theme-2.css" />',
    )


def test_absolute_url_slideshow_theme_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "themes" / "slides"
    config_path = cwd / "themes" / "absolute_url_slideshow_theme_path-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="https://example.org/theme.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="https://example.org/highlight-theme.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="stylesheet" href="https://example.org/theme.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="stylesheet" href="https://example.org/highlight-theme.css" />',
    )


def test_builtin_slideshow_theme_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "themes" / "slides"
    config_path = cwd / "themes" / "builtin_slideshow_theme_path-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_files_exist(output_path / "mkslides-assets/reveal-js/dist/theme/simple.css")

    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/theme/simple.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/highlight-js-themes/vs.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/theme/simple.css" />',
    )

    assert_html_contains(
        output_path / "somefolder/someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/highlight-js-themes/vs.css" />',
    )


def test_local_index_theme_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "themes" / "slides"
    config_path = cwd / "themes" / "local_index_theme_path-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "index.html",
        '<link rel="stylesheet" href="assets/theme.css" />',
    )


def test_absolute_url_index_theme_path(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "themes" / "slides"
    config_path = cwd / "themes" / "absolute_url_index_theme_path-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "index.html",
        '<link rel="stylesheet" href="https://example.org/theme.css" />',
    )

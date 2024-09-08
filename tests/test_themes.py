from pathlib import Path

from tests.utils import assert_files_exist, assert_html_contains


def test_local_slideshow_theme_path(setup_markup_generator):
    markup_generator, output_path = setup_markup_generator
    markup_generator.config.merge_config_from_dict(
        {
            "slides": {
                "theme": "tests/test_styles/theme.css",
                "highlight_theme": "tests/test_styles/highlight-theme.css",
            }
        }
    )

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains(
        output_path / "someslides.html",
        [
            '<link rel="stylesheet" href="assets/reveal-js/dist/reveal.css" />',
            '<link rel="stylesheet" href="assets/theme.css" />',
            '<link rel="stylesheet" href="assets/highlight-theme.css" />',
        ],
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        [
            '<link rel="stylesheet" href="../assets/reveal-js/dist/reveal.css" />',
            '<link rel="stylesheet" href="../assets/theme.css" />',
            '<link rel="stylesheet" href="../assets/highlight-theme.css" />',
        ],
    )


def test_absolute_url_slideshow_theme_path(setup_markup_generator):
    markup_generator, output_path = setup_markup_generator
    markup_generator.config.merge_config_from_dict(
        {
            "slides": {
                "theme": "https://example.org/theme.css",
                "highlight_theme": "https://example.org/highlight-theme.css",
            }
        }
    )

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains(
        output_path / "someslides.html",
        [
            '<link rel="stylesheet" href="assets/reveal-js/dist/reveal.css" />',
            '<link rel="stylesheet" href="https://example.org/theme.css" />',
            '<link rel="stylesheet" href="https://example.org/highlight-theme.css" />',
        ],
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        [
            '<link rel="stylesheet" href="../assets/reveal-js/dist/reveal.css" />',
            '<link rel="stylesheet" href="https://example.org/theme.css" />',
            '<link rel="stylesheet" href="https://example.org/highlight-theme.css" />',
        ],
    )


def test_builtin_slideshow_theme_path(setup_markup_generator):
    markup_generator, output_path = setup_markup_generator
    markup_generator.config.merge_config_from_dict(
        {
            "slides": {
                "theme": "simple",
                "highlight_theme": "vs",
            }
        }
    )

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_files_exist(
        output_path,
        [
            "assets/simple.css",
        ],
    )

    assert_html_contains(
        output_path / "someslides.html",
        [
            '<link rel="stylesheet" href="assets/reveal-js/dist/reveal.css" />',
            '<link rel="stylesheet" href="assets/simple.css" />',
            '<link rel="stylesheet" href="assets/vs.css" />',
        ],
    )

    assert_html_contains(
        output_path / "somefolder/someslides.html",
        [
            '<link rel="stylesheet" href="../assets/reveal-js/dist/reveal.css" />',
            '<link rel="stylesheet" href="../assets/simple.css" />',
            '<link rel="stylesheet" href="../assets/vs.css" />',
        ],
    )


def test_local_index_theme_path(setup_markup_generator):
    markup_generator, output_path = setup_markup_generator
    markup_generator.config.merge_config_from_dict(
        {
            "index": {
                "theme": "tests/test_styles/theme.css",
            }
        }
    )

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains(
        output_path / "index.html",
        [
            '<link rel="stylesheet" href="assets/theme.css" />',
        ],
    )


def test_absolute_url_index_theme_path(setup_markup_generator):
    markup_generator, output_path = setup_markup_generator
    markup_generator.config.merge_config_from_dict(
        {
            "index": {
                "theme": "https://example.org/theme.css",
            }
        }
    )

    test_files_path = Path("tests/test_files")
    markup_generator.process_markdown(test_files_path)

    assert_html_contains(
        output_path / "index.html",
        [
            '<link rel="stylesheet" href="https://example.org/theme.css" />',
        ],
    )

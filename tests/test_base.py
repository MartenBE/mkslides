from pathlib import Path

from mkslides_reveal.config import Config
from mkslides_reveal.markupgenerator import MarkupGenerator


def test_process_directory_without_config():
    config = Config()
    test_files_path = Path("tests/test_files")
    output_path = Path("tests/site")
    markup_generator = MarkupGenerator(config, output_path)
    markup_generator.create_output_directory()
    markup_generator.process_markdown(test_files_path)

    assert (output_path / "assets/reveal-js/dist/reveal.css").exists()
    assert (output_path / "assets/reveal-js/dist/reveal.js").exists()
    assert (output_path / "assets/reveal-js/plugin/markdown/markdown.js").exists()
    assert (output_path / "assets/reveal-js/plugin/highlight/highlight.js").exists()
    assert (output_path / "assets/reveal-js/plugin/zoom/zoom.js").exists()

    assert (output_path / "assets/black.css").exists()
    assert (output_path / "assets/monokai.css").exists()

    assert (output_path / "index.html").exists()
    assert (output_path / "someslides.html").exists()
    assert (output_path / "somefolder/someslides.html").exists()
    assert (output_path / "img/example-1.png").exists()
    assert (output_path / "img/example-2.png").exists()
    assert (output_path / "img/example-3.png").exists()
    assert (output_path / "img/example-4.png").exists()
    assert (output_path / "img/somefolder/example-5.png").exists()
    assert (output_path / "somefolder/example-6.png").exists()

    with open(output_path / "someslides.html", "r") as file:
        content = file.read()
        assert (
            '<link rel="stylesheet" href="assets/reveal-js/dist/reveal.css" />'
            in content
        )
        assert '<link rel="stylesheet" href="assets/black.css" />' in content
        assert '<link rel="stylesheet" href="assets/monokai.css" />' in content

    with open(output_path / "somefolder/someslides.html", "r") as file:
        content = file.read()
        assert (
            '<link rel="stylesheet" href="../assets/reveal-js/dist/reveal.css" />'
            in content
        )
        assert '<link rel="stylesheet" href="../assets/black.css" />' in content
        assert '<link rel="stylesheet" href="../assets/monokai.css" />' in content


def test_process_file_without_config():
    config = Config()
    test_file_path = Path("tests/test_files/someslides.md")
    output_path = Path("tests/site")
    markup_generator = MarkupGenerator(config, output_path)
    markup_generator.create_output_directory()
    markup_generator.process_markdown(test_file_path)

    assert (output_path / "assets/reveal-js/dist/reveal.css").exists()
    assert (output_path / "assets/reveal-js/dist/reveal.js").exists()
    assert (output_path / "assets/reveal-js/plugin/markdown/markdown.js").exists()
    assert (output_path / "assets/reveal-js/plugin/highlight/highlight.js").exists()
    assert (output_path / "assets/reveal-js/plugin/zoom/zoom.js").exists()

    assert (output_path / "assets/black.css").exists()
    assert (output_path / "assets/monokai.css").exists()

    assert not (output_path / "index.html").exists()
    assert (output_path / "someslides.html").exists()
    assert (output_path / "img/example-1.png").exists()
    assert (output_path / "img/example-2.png").exists()
    assert (output_path / "img/example-3.png").exists()

from typing import Any

from tests.utils import assert_html_contains, run_build_strict


def test_index_title(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "index" / "docs"
    config_path = cwd / "index" / "index_title-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(output_path / "index.html", "<title>Lorem ipsum</title>")
    assert_html_contains(
        output_path / "index.html",
        "<h1>Lorem ipsum</h1>",
    )

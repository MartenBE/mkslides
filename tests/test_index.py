from typing import Any

from tests.utils import assert_html_contains, run_build


def test_index_title(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build(cwd, "test_files", output_path, "test_configs/test_index_title.yml")

    assert_html_contains(output_path / "index.html", "<title>Lorem ipsum</title>")
    assert_html_contains(
        output_path / "index.html",
        "<h1>Lorem ipsum</h1>",
    )

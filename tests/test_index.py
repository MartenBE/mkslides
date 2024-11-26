from typing import Any

from tests.utils import assert_html_contains, run_build_with_config


def test_index_title(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_index_title.yml")

    assert_html_contains(
        output_path / "index.html",
        [
            "<title>Lorem ipsum</title>",
            "<h1>Lorem ipsum</h1>",
        ],
    )

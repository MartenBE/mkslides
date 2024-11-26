from typing import Any

from tests.utils import assert_html_contains, run_build


def test_emojize(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build(cwd, output_path)

    assert_html_contains(
        output_path / "someslides.html",
        [
            "⚠️",
            "👍",
        ],
    )

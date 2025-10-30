import re
from typing import Any

from tests.utils import assert_html_contains_regexp, run_build_strict


def test_preprocessing(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "preprocessing" / "docs"
    config_path = cwd / "preprocessing" / "preprocessing-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains_regexp(
        output_path / "someslides-1.html",
        re.compile(
            r"""
                atbegin@@@@@atend-atbegin@@@@atend
                .*?
                atbegin@@@atend-atbegin@@atend
                .*?
                atbegin@atend
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )

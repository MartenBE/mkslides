import re
from typing import Any

from tests.utils import assert_html_contains_regexp, run_build


def test_preprocess(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build(cwd, "test_files", output_path, "test_configs/test_preprocess.yml")

    assert_html_contains_regexp(
        output_path / "someslides.html",
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

from typing import Any

from tests.utils import (
    assert_file_exist,
    run_build_strict,
)


def test_process_directory_without_config(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "images" / "slides"
    run_build_strict(cwd, input_path, output_path, None)

    assert_file_exist(output_path / "img/example-1.png")
    assert_file_exist(output_path / "somefolder/example-2.png")
    assert_file_exist(output_path / "img/somefolder/example-3.png")
    assert_file_exist(output_path / "example-4.png")

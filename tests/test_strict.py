import subprocess
from typing import Any


def test_process_file_without_config(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    result = subprocess.run(
        [
            "mkslides",
            "-v",
            "build",
            "-s",
            "-d",
            output_path,
            "test_files_crash/strict.md",
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert (
        "Local file './some-random-md-link' mentioned in '/home/martijn/git/mkslides/tests/test_files_crash/strict.md' not found."
        in result.stderr
    )

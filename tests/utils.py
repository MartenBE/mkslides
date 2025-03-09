import subprocess
from pathlib import Path
from re import Pattern


def run_build(
    cwd: Path,
    input_filename: str,
    output_path: Path,
    config_filename: str | None,
) -> subprocess.CompletedProcess[str]:
    input_path = (cwd / input_filename).resolve(strict=True)

    if config_filename:
        config_path = (cwd / config_filename).resolve(strict=True)
        command = [
            "mkslides",
            "-v",
            "build",
            "-s",
            "-d",
            str(output_path),
            "-f",
            str(config_path),
            str(input_path),
        ]
    else:
        command = [
            "mkslides",
            "-v",
            "build",
            "-s",
            "-d",
            str(output_path),
            str(input_path),
        ]

    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr

    return result


def assert_files_exist(file: Path) -> None:
    absolute_file = file.absolute()
    assert absolute_file.exists(), f"{absolute_file} does not exist"


def assert_html_contains(file_path: Path, expected_content: str) -> None:
    with file_path.open() as file:
        content = file.read()
        assert (
            expected_content in content
        ), f"{expected_content} not found in {file_path}"


def assert_html_contains_regexp(file_path: Path, regexp: Pattern[str]) -> None:
    with file_path.open() as file:
        content = file.read()
        assert regexp.search(content), f"{regexp} not found in {file_path}"

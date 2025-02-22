import subprocess
from pathlib import Path
from re import Pattern


def run_build_with_custom_input(
    cwd: Path,
    output_path: Path,
    input_filename: str,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["mkslides", "-v", "build", "-s", "-d", output_path, input_filename],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result


def run_build(cwd: Path, output_path: Path) -> subprocess.CompletedProcess[str]:
    return run_build_with_custom_input(cwd, output_path, "test_files")


def run_build_with_config(
    cwd: Path,
    output_path: Path,
    config_filename: str,
    input_filename: str = "test_files",
) -> subprocess.CompletedProcess[str]:
    config_path = (cwd / "test_configs" / config_filename).resolve(strict=True)
    result = subprocess.run(
        [
            "mkslides",
            "-v",
            "build",
            "-s",
            "-d",
            output_path,
            "-f",
            config_path,
            input_filename,
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result


def assert_files_exist(output_path: Path, files: list[str]) -> None:
    for file in files:
        file_path = (output_path / file).absolute()
        assert file_path.exists(), f"{file_path} does not exist"


def assert_html_contains(file_path: Path, expected_content: list[str]) -> None:
    with file_path.open() as file:
        content = file.read()
        for substring in expected_content:
            assert substring in content, f"{substring} not found in {file_path}"


def assert_html_contains_regexp(file_path: Path, regexp: Pattern[str]) -> None:
    with file_path.open() as file:
        content = file.read()
        assert regexp.search(content), f"{regexp} not found in {file_path}"

from pathlib import Path


def assert_files_exist(output_path: Path, files: list[str]) -> None:
    for file in files:
        assert (output_path / file).exists(), f"{file} does not exist"


def assert_html_contains(file_path: Path, expected_content: str) -> None:
    with file_path.open() as file:
        content = file.read()
        for substring in expected_content:
            assert substring in content, f"{substring} not found in {file_path}"

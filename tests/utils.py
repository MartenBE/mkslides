# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import subprocess
from pathlib import Path
from re import Pattern


def __run_build_generic(
    cwd: Path,
    input_path: Path,
    output_path: Path,
    config_path: Path | None,
    *,
    strict: bool = False,
) -> subprocess.CompletedProcess[str]:
    command = [
        "mkslides",
        "-v",
        "build",
        "-d",
        str(output_path),
    ]

    if strict:
        command.insert(3, "-s")  # Insert -s after "build"

    if config_path:
        command.extend(["-f", str(config_path)])

    command.append(str(input_path))

    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result


def run_build_strict(
    cwd: Path,
    input_path: Path,
    output_path: Path,
    config_path: Path | None,
) -> subprocess.CompletedProcess[str]:
    return __run_build_generic(cwd, input_path, output_path, config_path, strict=True)


def run_build(
    cwd: Path,
    input_path: Path,
    output_path: Path,
    config_path: Path | None,
) -> subprocess.CompletedProcess[str]:
    return __run_build_generic(cwd, input_path, output_path, config_path, strict=False)


def assert_file_exist(file: Path) -> None:
    absolute_file = file.absolute()
    assert absolute_file.exists(), f"{absolute_file} does not exist"


def assert_file_does_not_exist(file: Path) -> None:
    absolute_file = file.absolute()
    assert not absolute_file.exists(), f"{absolute_file} exists but should not"


def assert_html_contains(file_path: Path, expected_content: str) -> None:
    with file_path.open() as file:
        content = file.read()
        assert expected_content in content, (
            f"{expected_content} not found in {file_path}"
        )


def assert_html_does_not_contain(file_path: Path, expected_content: str) -> None:
    with file_path.open() as file:
        content = file.read()
        assert expected_content not in content, (
            f"{expected_content} found in {file_path} but should not be"
        )


def assert_html_contains_regexp(file_path: Path, regexp: Pattern[str]) -> None:
    with file_path.open() as file:
        content = file.read()
        assert regexp.search(content), f"{regexp} not found in {file_path}"

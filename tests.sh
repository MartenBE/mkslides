#!/usr/bin/env bash

# SPDX-FileCopyrightText: Copyright (C) 2026 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

set -o errexit
set -o nounset
set -o pipefail

assert_is_installed () {
  if ! command -v "${1}" &> /dev/null
  then
    echo "${1} is not installed. Please install it to run the tests."
    exit 1
  fi
}

if [[ "$#" -ne 1 ]]
then
    echo "Usage: ${0} <git_repo_root>"
    exit 1
fi

git_repo_root="$(realpath "${1}")"
cd "${git_repo_root}"
echo "Running tests in ${git_repo_root} ..."
echo

assert_is_installed "prettier"

echo "Linting with prettier ..."
prettier --check .
echo "OK."
echo

assert_is_installed "uv"

uv sync

echo "Checking licenses ..."
uv run reuse lint
echo "OK."
echo

echo "Linting python code ..."
uv run ruff format --check
echo "OK."
echo

echo "Checking python code ..."
uv run ruff check
echo "OK."
echo

echo "Checking python types ..."
uv run mypy src/ tests/
echo "OK."
echo

echo "Running python tests ..."
uv run pytest
echo "OK."
echo

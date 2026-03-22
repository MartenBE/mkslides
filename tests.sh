#!/usr/bin/env sh

# SPDX-FileCopyrightText: Copyright (C) 2026 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

set -o errexit
set -o nounset

assert_is_installed () {
  if ! command -v "${1}"  1>/dev/null 2>&1
  then
    echo "${1} is not installed. Please install it to run the tests."
    exit 1
  fi
}

if [ -n "${1:-}" ]
then
    BASE_DIR="${1}"
else
    BASE_DIR="."
fi

BASE_DIR="$(realpath "${BASE_DIR}")"
echo "Starting linting checks using base directory: ${BASE_DIR}"
cd "${BASE_DIR}" || exit 1
echo

echo "Checking licenses ..."
uv run reuse lint
echo "OK."
echo

echo "Checking shell scripts."
git ls-files -z '*.sh' | xargs -0 shellcheck
echo "OK."
echo

echo "Checking yaml files."
git ls-files -z '*.yml' '*.yaml' | xargs -0 uv run yamllint --strict
echo "OK."
echo

echo "Checking json and markdown files."
git ls-files -z '*.json' '*.md' | xargs -0 npx prettier --check
echo "OK."
echo

uv sync

echo "Checking python scripts."
git ls-files -z '*.py' | xargs -0 uv run ruff check
git ls-files -z '*.py' | xargs -0 uv run ruff format --check
uv run mypy src/ tests/
uv run pytest
echo "OK."
echo

echo "OK: All checks passed."

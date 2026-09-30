#!/usr/bin/env sh

# SPDX-FileCopyrightText: Copyright (C) 2026 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

uv lock
uv sync
./tests.sh
echo
python ./cli-help-output-to-docs.py

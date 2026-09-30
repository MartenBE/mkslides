#!/usr/bin/env sh

# SPDX-FileCopyrightText: Copyright (C) 2026 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

rm -rf dist/
uv build
# uv publish

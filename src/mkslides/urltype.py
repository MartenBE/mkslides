# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

from enum import Enum


class URLType(Enum):
    ANCHOR = "anchor"
    ABSOLUTE = "absolute"
    RELATIVE = "relative"

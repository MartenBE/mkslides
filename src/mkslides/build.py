# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import logging
from pathlib import Path

from omegaconf import DictConfig

from mkslides.markupgenerator import MarkupGenerator

logger = logging.getLogger(__name__)


def build(
    config: DictConfig,
    input_path: Path,
    output_path: Path,
    strict: bool,
) -> None:
    markup_generator = MarkupGenerator(config, input_path, output_path, strict)
    markup_generator.process_markdown()

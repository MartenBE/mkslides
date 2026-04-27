# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from omegaconf import MISSING, DictConfig, OmegaConf

from mkslides.constants import (
    DEFAULT_CONFIG_LOCATION,
)

logger = logging.getLogger(__name__)

FRONTMATTER_ALLOWED_KEYS = ["slides", "revealjs", "plugins"]


@dataclass
class Index:
    favicon: str | None = None
    template: str | None = None
    theme: str | None = None
    title: str = "Index"
    nav: list[Any] | None = None
    enable_footer: bool = True


@dataclass
class Slides:
    charset: str | None = None
    favicon: str | None = None
    highlight_theme: str = "monokai"
    preprocess_script: str | None = None
    separator_notes: str | None = None
    separator_vertical: str | None = None
    separator: str | None = None
    template: str | None = None
    theme: str = "black"
    title: str | None = None


@dataclass
class Plugin:
    name: str | None = None
    extra_css: list[str] | None = None
    extra_javascript: list[str] | None = None


# For internal use only
@dataclass
class Internal:
    config_path: Path | None = MISSING


@dataclass
class Config:
    index: Index = field(default_factory=Index)
    slides: Slides = field(default_factory=Slides)
    revealjs: dict[str, Any] = field(
        default_factory=lambda: {
            "history": True,  # Necessary for back/forward buttons and livereload
            "slideNumber": "c/t",
        },
    )
    plugins: list[Plugin] = field(default_factory=list)
    internal: Internal = field(default_factory=Internal)


def get_config(config_file: Path | None = None) -> DictConfig:
    config = OmegaConf.structured(Config)

    if not config_file and DEFAULT_CONFIG_LOCATION.exists():
        config_file = DEFAULT_CONFIG_LOCATION.resolve(strict=True).absolute()

    config.internal.config_path = config_file
    if config_file:
        try:
            loaded_config = OmegaConf.load(config_file)
            config = OmegaConf.merge(config, loaded_config)

            logger.info(f"Loaded config from '{config_file}'")
        except Exception:
            logger.exception(f"Failed to load config from {config_file}")
            raise

    assert OmegaConf.is_dict(config)

    logger.debug(f"Used config:\n\n{OmegaConf.to_yaml(config, resolve=True)}")

    return config

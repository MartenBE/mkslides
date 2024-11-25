from dataclasses import dataclass, field
import logging
from pathlib import Path
import sys
from typing import Any, Dict, Optional

from mkslides.constants import (
    DEFAULT_CONFIG_LOCATION,
    HIGHLIGHTJS_THEMES_LIST,
    REVEALJS_THEMES_LIST,
)
from mkslides.urltype import URLType
from mkslides.utils import get_url_type
from omegaconf import MISSING, DictConfig, OmegaConf

logger = logging.getLogger(__name__)


@dataclass
class Index:
    favicon: Optional[str] = None
    template: Optional[str] = None
    theme: Optional[str] = None
    title: str = "Index"


@dataclass
class Slides:
    charset: Optional[str] = None
    favicon: Optional[str] = None
    highlight_theme: str = "monokai"
    separator_notes: Optional[str] = None
    separator_vertical: Optional[str] = None
    separator: Optional[str] = None
    template: Optional[str] = None
    theme: str = "black"


@dataclass
class Plugin:
    name: Optional[str] = None
    extra_javascript: Optional[str] = MISSING


@dataclass
class Config:
    index: Index = field(default_factory=Index)
    slides: Slides = field(default_factory=Slides)
    revealjs: Dict[str, Any] = field(
        default_factory=lambda: {
            "history": True,  # Necessary for back/forward buttons and livereload
            "slideNumber": "c/t",
        }
    )
    plugins: list[Plugin] = field(default_factory=list)


def validate(config) -> None:
    if config.index.favicon and get_url_type(config.index.favicon) == URLType.RELATIVE:
        Path(config.index.favicon).resolve(strict=True)

    if (
        config.index.template
        and get_url_type(config.index.template) == URLType.RELATIVE
    ):
        Path(config.index.template).resolve(strict=True)

    if (
        config.index.theme
        and get_url_type(config.index.theme) == URLType.RELATIVE
        and not config.index.theme in REVEALJS_THEMES_LIST
    ):
        Path(config.index.theme).resolve(strict=True)

    if (
        config.slides.favicon
        and get_url_type(config.slides.favicon) == URLType.RELATIVE
    ):
        Path(config.slides.favicon).resolve(strict=True)

    if (
        config.slides.highlight_theme
        and get_url_type(config.slides.highlight_theme) == URLType.RELATIVE
        and not config.slides.highlight_theme in HIGHLIGHTJS_THEMES_LIST
    ):
        Path(config.slides.highlight_theme).resolve(strict=True)

    if (
        config.slides.template
        and get_url_type(config.slides.template) == URLType.RELATIVE
    ):
        Path(config.slides.template).resolve(strict=True)

    if config.slides.theme:
        if get_url_type(config.slides.theme) == URLType.RELATIVE:
            if config.slides.theme in REVEALJS_THEMES_LIST:
                pass
            else:
                Path(config.slides.theme).resolve(strict=True)


def get_config(config_file: Path | None = None) -> DictConfig:
    config = OmegaConf.structured(Config)

    if not config_file and DEFAULT_CONFIG_LOCATION.exists():
        config_file = DEFAULT_CONFIG_LOCATION

    if config_file:
        try:
            loaded_config = OmegaConf.load(config_file)
            config = OmegaConf.merge(config, loaded_config)
            logger.info(f'Loaded config from "{config_file}"')
        except Exception as e:
            logger.error(f"Failed to load config from {config_file}: {e}")
            raise

    assert OmegaConf.is_dict(config)

    logger.debug("Used config:")
    logger.debug(OmegaConf.to_yaml(config, resolve=True))

    return config

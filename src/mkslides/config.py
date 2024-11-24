from dataclasses import dataclass, field
import logging
from pathlib import Path
import sys
from typing import Any, Dict, Optional

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


def validate_config(config: Config) -> None:
    # index.favicon
    # index.theme
    # index.template
    # slides.favicon
    # slides.highlight_theme
    # slides.theme
    # slides.template

    return True


def load_config_file(config_file: Path) -> DictConfig:
    config = OmegaConf.structured(Config)

    # config = OmegaConf.merge(
    #     config,
    #     OmegaConf.load(config_file),
    # )
    # logger.info(f"Loaded config from {config_file}")

    assert OmegaConf.is_dict(config)

    if not validate_config(config):
        raise ValueError("Invalid config")

    OmegaConf.set_readonly(conf=config, value=True)
    logger.debug(f"Used config: {config}")

    return config

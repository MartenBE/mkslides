import logging
from pathlib import Path
from typing import Any

import yaml

from .constants import DEFAULT_CONFIG_RESOURCE

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        with DEFAULT_CONFIG_RESOURCE.open() as f:
            self.__config = yaml.safe_load(f)

        logger.info(f'Default config loaded from "{DEFAULT_CONFIG_RESOURCE}"')
        logger.info(f"Default config: {self.__config}")

    def get_index_title(self) -> str | None:
        value = self.__get("index", "title")
        assert isinstance(value, str) or value is None
        return value

    def get_index_favicon(self) -> str | None:
        value = self.__get("index", "favicon")
        assert isinstance(value, str) or value is None
        return value

    def get_index_theme(self) -> str | None:
        value = self.__get("index", "theme")
        assert isinstance(value, str) or value is None
        return value

    def get_index_template(self) -> str | None:
        value = self.__get("index", "template")
        assert isinstance(value, str) or value is None
        return value

    def get_slides_favicon(self) -> str | None:
        value = self.__get("slides", "favicon")
        assert isinstance(value, str) or value is None
        return value

    def get_slides_theme(self) -> str | None:
        value = self.__get("slides", "theme")
        assert isinstance(value, str) or value is None
        return value

    def get_slides_highlight_theme(self) -> str | None:
        value = self.__get("slides", "highlight_theme")
        assert isinstance(value, str) or value is None
        return value

    def get_slides_template(self) -> str | None:
        value = self.__get("slides", "template")
        assert isinstance(value, str) or value is None
        return value

    def get_slides_separator(self) -> str | None:
        value = self.__get("slides", "separator")
        assert isinstance(value, str) or value is None
        return value

    def get_slides_separator_vertical(self) -> str | None:
        value = self.__get("slides", "separator_vertical")
        assert isinstance(value, str) or value is None
        return value

    def get_slides_separator_notes(self) -> str | None:
        value = self.__get("slides", "separator_notes")
        assert isinstance(value, str) or value is None
        return value

    def get_slides_charset(self) -> str | None:
        value = self.__get("slides", "charset")
        assert isinstance(value, str) or value is None
        return value

    def get_revealjs_options(self) -> dict | None:
        value = self.__get("revealjs")
        assert isinstance(value, dict) or value is None
        return value

    def get_plugins(self) -> list | None:
        value = self.__get("plugins")
        assert isinstance(value, list) or value is None
        return value

    def merge_config_from_file(self, config_path: Path) -> None:
        with config_path.open(encoding="utf-8-sig") as f:
            new_config = yaml.safe_load(f)

            self.__config = self.__recursive_merge(self.__config, new_config)

            logger.info(f'Config merged from "{config_path}"')
            logger.info(f"Config: {self.__config}")

    def merge_config_from_dict(self, new_config: dict) -> None:
        self.__config = self.__recursive_merge(self.__config, new_config)

        logger.info("Config merged from dict")
        logger.info(f"Config: {self.__config}")

    def __get(self, *keys: str) -> str | dict | list | None:
        current_value = self.__config
        for key in keys:
            if isinstance(current_value, dict) and key in current_value:
                current_value = current_value[key]
            else:
                return None
        return current_value

    def __recursive_merge(self, current: Any, new: dict) -> dict:
        if new:
            for key, value in new.items():
                if isinstance(value, dict):
                    current[key] = self.__recursive_merge(current.get(key, {}), value)
                else:
                    current[key] = value

        return current

import logging
from pathlib import Path

import yaml

from .constants import DEFAULT_CONFIG_RESOURCE

logger = logging.getLogger(__name__)


class Config:
    schema = {
        "type": "object",
        "properties": {
            "price": {"type": "number"},
            "name": {"type": "string"},
        },
    }

    def __init__(self) -> None:
        with DEFAULT_CONFIG_RESOURCE.open() as f:
            self.__config = yaml.safe_load(f)

        logger.info(f'Default config loaded from "{DEFAULT_CONFIG_RESOURCE}"')
        logger.info(f"Default config: {self.__config}")

    def get_index_title(self) -> str | None:
        return self.__get("index", "title")

    def get_index_favicon(self) -> str | None:
        return self.__get("index", "favicon")

    def get_index_theme(self) -> str | None:
        return self.__get("index", "theme")

    def get_index_template(self) -> str | None:
        return self.__get("index", "template")

    def get_slides_favicon(self) -> str | None:
        return self.__get("slides", "favicon")

    def get_slides_theme(self) -> str | None:
        return self.__get("slides", "theme")

    def get_slides_highlight_theme(self) -> str | None:
        return self.__get("slides", "highlight_theme")

    def get_slides_template(self) -> str | None:
        return self.__get("slides", "template")

    def get_slides_separator(self) -> str | None:
        return self.__get("slides", "separator")

    def get_slides_separator_vertical(self) -> str | None:
        return self.__get("slides", "separator_vertical")

    def get_slides_separator_notes(self) -> str | None:
        return self.__get("slides", "separator_notes")

    def get_slides_charset(self) -> str | None:
        return self.__get("slides", "charset")

    def get_revealjs_options(self) -> dict | None:
        return self.__get("revealjs")

    def get_plugins(self) -> list | None:
        return self.__get("plugins")

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

    def __get(self, *keys) -> str | dict | list | None:
        current_value = self.__config
        for key in keys:
            if isinstance(current_value, dict) and key in current_value:
                current_value = current_value[key]
            else:
                return None
        return current_value

    def __recursive_merge(self, current, new) -> dict:
        if new:
            for key, value in new.items():
                if isinstance(value, dict):
                    current[key] = self.__recursive_merge(current.get(key, {}), value)
                else:
                    current[key] = value

        return current

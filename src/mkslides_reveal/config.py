import importlib
import logging
import yaml

from pathlib import Path

from .constants import DEFAULT_CONFIG_RESOURCE


logger = logging.getLogger(__name__)


class Config:
    def __init__(self):
        with DEFAULT_CONFIG_RESOURCE.open() as f:
            self.config = yaml.safe_load(f)

        logger.info(f'Default config loaded from "{DEFAULT_CONFIG_RESOURCE}"')
        logger.info(f"Default config: {self.config}")

    def merge_config_from_file(self, config_path: Path):
        with config_path.open() as f:
            new_config = yaml.safe_load(f)

            self.config = self.__recursive_merge(self.config, new_config)

            logger.info(f'Config merged from "{config_path}"')
            logger.info(f"Config: {self.config}")

    def merge_config_from_dict(self, new_config: dict):
        self.config = self.__recursive_merge(self.config, new_config)

        logger.info(f"Config merged from dict")
        logger.info(f"Config: {self.config}")

    def get(self, *keys):
        current_value = self.config
        for key in keys:
            if isinstance(current_value, dict) and key in current_value:
                current_value = current_value[key]
            else:
                return None
        return current_value

    def __recursive_merge(self, current, new):
        if new:
            for key, value in new.items():
                if isinstance(value, dict):
                    current[key] = self.__recursive_merge(current.get(key, {}), value)
                else:
                    current[key] = value

        return current

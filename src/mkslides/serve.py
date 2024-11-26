import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import livereload  # type: ignore[import-untyped]
from livereload.handlers import LiveReloadHandler  # type: ignore[import-untyped]
from omegaconf import DictConfig

from mkslides.build import build
from mkslides.config import get_config
from mkslides.constants import REVEALJS_THEMES_LIST
from mkslides.urltype import URLType
from mkslides.utils import get_url_type

logger = logging.getLogger(__name__)

LiveReloadHandler.DEFAULT_RELOAD_TIME = (
    0  # https://github.com/lepture/python-livereload/pull/244
)


@dataclass
class ServeConfig:
    dev_ip: Optional[str] = None
    dev_port: Optional[str] = None
    open_in_browser: bool = False


def determine_paths_to_watch(input_path: Path, config: DictConfig) -> list[Path]:
    def should_watch(
        path: Optional[str],
        unwatchable_values: Optional[list[str]] = None,
    ) -> Optional[Path]:
        # https://docs.astral.sh/ruff/rules/mutable-argument-default/
        if unwatchable_values is None:
            unwatchable_values = []

        return (
            Path(path).resolve(strict=True).absolute()
            if path
            and get_url_type(path) == URLType.RELATIVE
            and path not in unwatchable_values
            else None
        )

    paths_to_watch = [
        input_path,
        config.internal.config_path,
        should_watch(config.index.theme),
        should_watch(config.index.template),
        should_watch(config.slides.theme, REVEALJS_THEMES_LIST),
        should_watch(config.slides.template),
    ]

    return [path for path in paths_to_watch if path]


def serve(
    config: DictConfig,
    input_path: Path,
    output_path: Path,
    serve_config: DictConfig,
) -> None:
    config_path = config.internal.config_path

    def reload() -> None:
        logger.info("Reloading...")
        new_config = get_config(config_path)
        build(new_config, input_path, output_path, serve_config.strict)

        new_paths_to_watch = determine_paths_to_watch(input_path, new_config)
        diff_paths_to_watch = set(new_paths_to_watch) - set(paths_to_watch)
        for path in diff_paths_to_watch:
            logger.debug(f'Adding new watched path: "{path}"')
            server.watch(filepath=path.as_posix(), func=reload, delay=1)

    build(config, input_path, output_path, serve_config.strict)
    paths_to_watch = determine_paths_to_watch(input_path, config)

    try:
        server = livereload.Server()

        # https://github.com/lepture/python-livereload/issues/232
        server._setup_logging = lambda: None  # noqa: SLF001

        for path in paths_to_watch:
            logger.debug(f'Watching: "{path}"')
            server.watch(filepath=path.as_posix(), func=reload, delay=1)

        server.serve(
            host=serve_config.dev_ip,
            port=serve_config.dev_port,
            root=output_path,
            open_url_delay=0 if serve_config.open_in_browser else None,
        )

    finally:
        if output_path.exists():
            shutil.rmtree(output_path)
            logger.debug(f'Removed "{output_path}"')

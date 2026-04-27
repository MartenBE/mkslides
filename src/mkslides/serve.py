# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import logging
import shutil
import threading
from pathlib import Path

import livereload  # type: ignore[import-untyped]
from livereload.handlers import LiveReloadHandler  # type: ignore[import-untyped]
from omegaconf import DictConfig

from mkslides.build import build
from mkslides.config import get_config

logger = logging.getLogger(__name__)

LiveReloadHandler.DEFAULT_RELOAD_TIME = (
    0  # https://github.com/lepture/python-livereload/pull/244
)


def serve(
    config: DictConfig,
    input_path: Path,
    output_path: Path,
    serve_config: DictConfig,
) -> None:
    build(
        config,
        input_path,
        output_path,
        serve_config.strict,
    )

    paths_to_watch: list[Path] = [
        input_path,
        config.internal.config_path,
    ]

    def reload() -> None:
        logger.info("Reloading...")
        new_config = get_config(config.internal.config_path)
        build(new_config, input_path, output_path, serve_config.strict)

    debounce_timer: threading.Timer | None = None

    def debounced_reload() -> None:
        nonlocal debounce_timer

        if debounce_timer is not None:
            logger.info(
                f"New change detected, resetting debounce timer ({serve_config.debounce_interval}s) ...",
            )
            debounce_timer.cancel()

        debounce_timer = threading.Timer(serve_config.debounce_interval, reload)
        debounce_timer.daemon = True
        debounce_timer.start()

    try:
        server = livereload.Server()

        # https://github.com/lepture/python-livereload/issues/232
        server._setup_logging = lambda: None  # noqa: SLF001

        for path in paths_to_watch:
            logger.info(f"Watching: '{path}'")
            server.watch(filepath=path.as_posix(), func=debounced_reload)

        server.serve(
            host=serve_config.dev_ip,
            port=serve_config.dev_port,
            root=output_path,
            open_url_delay=0 if serve_config.open_in_browser else None,
        )

    finally:
        if output_path.exists():
            shutil.rmtree(output_path)
            logger.info(f"Removed '{output_path}'")

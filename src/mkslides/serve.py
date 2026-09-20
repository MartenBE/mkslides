# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import asyncio
import logging
import shutil
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

    async def reload() -> None:
        await asyncio.sleep(serve_config.debounce_interval)

        logger.info("Reloading...")
        new_config = get_config(config.internal.config_path)

        await asyncio.get_running_loop().run_in_executor(
            None,
            build,
            new_config,
            input_path,
            output_path,
            serve_config.strict,
        )

        LiveReloadHandler.reload_waiters()

    pending_reload: asyncio.Task[None] | None = None

    def debounced_reload() -> None:
        nonlocal pending_reload

        if pending_reload is not None and not pending_reload.done():
            logger.info(
                f"New change detected, resetting debounce timer ({serve_config.debounce_interval}s) ...",
            )
            pending_reload.cancel()

        pending_reload = asyncio.get_running_loop().create_task(reload())

    try:
        server = livereload.Server()

        # https://github.com/lepture/python-livereload/issues/232
        server._setup_logging = lambda: None  # noqa: SLF001

        for path in paths_to_watch:
            # E.g. if there is no config file present.
            if path is not None:
                logger.info(f"Watching: '{path}'")
                # "forever" means livereload never sends a reload itself.
                server.watch(
                    filepath=path.as_posix(),
                    func=debounced_reload,
                    delay="forever",
                )

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

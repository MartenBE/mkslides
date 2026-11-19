# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import asyncio
import logging
import shutil
from pathlib import Path

import livereload  # type: ignore[import-untyped]
from livereload.handlers import LiveReloadHandler  # type: ignore[import-untyped]
from livereload.watcher import get_watcher_class  # type: ignore[import-untyped]
from omegaconf import DictConfig

from mkslides.build import build
from mkslides.config import get_config

logger = logging.getLogger(__name__)

LiveReloadHandler.DEFAULT_RELOAD_TIME = (
    0  # https://github.com/lepture/python-livereload/pull/244
)


# Watcher that runs the watch tasks, but never lets livereload reload the browser.
#
# Livereload reloads the browser right after the watch task returns. Our task only
# starts a debounce task, so that reload would happen before the rebuild and show
# stale content. Instead, `reload()` in `serve()` reloads the browser itself once
# the build has finished. (`delay="forever"` would be the documented way to do
# this, but livereload drops non-float delays in `Watcher.examine()`.)
#
# TODO: https://github.com/lepture/python-livereload/pull/289
#
class _BuildThenReloadWatcher(get_watcher_class()):  # type: ignore[misc]
    def examine(self) -> tuple[None, None]:
        super().examine()
        return None, None


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

    async def rebuild() -> None:
        await asyncio.sleep(serve_config.debounce_interval)

        logger.info("Reloading...")
        try:
            new_config = get_config(config.internal.config_path)
            build(new_config, input_path, output_path, serve_config.strict)
        except Exception:
            logger.exception("Build failed, browser not reloaded")
            return

        LiveReloadHandler.reload_waiters()

    pending_reload: asyncio.Task[None] | None = None

    def debounced_rebuild() -> None:
        nonlocal pending_reload

        if pending_reload is not None and not pending_reload.done():
            logger.info(
                f"New change detected, resetting debounce timer ({serve_config.debounce_interval}s) ...",
            )
            pending_reload.cancel()

        pending_reload = asyncio.create_task(rebuild())

    try:
        server = livereload.Server(watcher=_BuildThenReloadWatcher())

        # https://github.com/lepture/python-livereload/issues/232
        server._setup_logging = lambda: None  # noqa: SLF001

        for path in paths_to_watch:
            # E.g. if there is no config file present.
            if path is not None:
                logger.info(f"Watching: '{path}'")
                server.watch(
                    filepath=path.as_posix(),
                    func=debounced_rebuild,
                    # delay="forever",  # TODO: https://github.com/lepture/python-livereload/pull/289
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

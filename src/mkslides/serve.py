import logging
from pathlib import Path
import shutil

import livereload  # type: ignore[import-untyped]
from livereload.handlers import LiveReloadHandler  # type: ignore[import-untyped]

from mkslides.build import execute_build_command
from mkslides.config import get_config
from mkslides.markupgenerator import MarkupGenerator
from mkslides.utils import parse_ip_port

logger = logging.getLogger(__name__)

LiveReloadHandler.DEFAULT_RELOAD_TIME = (
    0  # https://github.com/lepture/python-livereload/pull/244
)


class LiveReloadHandler:
    def __init__(
        self,  # noqa: C901
        config_path: Path | None,
        input_path: Path,
        output_path: Path,
        dev_addr: str,
        open_in_browser: bool,
        watch_index_theme: bool,
        watch_index_template: bool,
        watch_slides_theme: bool,
        watch_slides_template: bool,
    ):
        self.config_path = config_path
        self.input_path = input_path
        self.output_path = output_path
        self.dev_addr = dev_addr
        self.open_in_browser = open_in_browser
        self.watch_index_theme = watch_index_theme
        self.watch_index_template = watch_index_template
        self.watch_slides_theme = watch_slides_theme
        self.watch_slides_template = watch_slides_template

    def determine_watched_paths(self, config):
        watched_paths = [
            self.input_path,
            self.config_path,
            config.index.theme if self.watch_index_theme else None,
            config.index.template if self.watch_index_template else None,
            config.slides.theme if self.watch_slides_theme else None,
            config.slides.template if self.watch_slides_template else None,
        ]

        for path in watched_paths:
            if path:
                resolved_path = Path(path).resolve(strict=True).absolute()
                logger.debug(f'Watching: "{resolved_path}"')
                server.watch(filepath=resolved_path.as_posix(), func=reload, delay=1)

    def generate_slides(self):
        self.config = get_config(config_path)
        markup_generator = MarkupGenerator(config, output_path)
        markup_generator.create_or_clear_output_directory()
        markup_generator.process_markdown(input_path)

    def serve():
        try:
            server = livereload.Server()

            # https://github.com/lepture/python-livereload/issues/232
            server._setup_logging = lambda: None  # noqa: SLF001

            watched_paths = [
                input_path,
                config_path if config_path.exists() else None,
                # config.index.theme if watch_index_theme else None,
                # config.index.template if watch_index_template else None,
                # config.slides.theme if watch_slides_theme else None,
                # config.slides.template if watch_slides_template else None,
            ]

            for path in watched_paths:
                if path:
                    resolved_path = Path(path).resolve(strict=True).absolute()
                    logger.debug(f'Watching: "{resolved_path}"')
                    server.watch(
                        filepath=resolved_path.as_posix(), func=reload, delay=1
                    )

            ip, port = parse_ip_port(dev_addr)

            server.serve(
                host=ip,
                port=port,
                root=output_path,
                open_url_delay=0 if open_in_browser else None,
            )

        finally:
            if output_path.exists():
                shutil.rmtree(output_path)
                logger.debug(f'Removed "{output_path}"')


# def execute_serve_command(  # noqa: C901
#     config_path: Path,
#     input_path: Path,
#     output_path: Path,
#     dev_addr: str,
#     open_in_browser: bool,
#     watch_index_theme: bool,
#     watch_index_template: bool,
#     watch_slides_theme: bool,
#     watch_slides_template: bool,
# ) -> None:

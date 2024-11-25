# import logging
# from pathlib import Path
# import shutil

# import livereload  # type: ignore[import-untyped]
# from livereload.handlers import LiveReloadHandler
# from omegaconf import DictConfig  # type: ignore[import-untyped]

# from mkslides.build import execute_build_command
# from mkslides.config import get_config
# from mkslides.markupgenerator import MarkupGenerator
# from mkslides.utils import parse_ip_port

# logger = logging.getLogger(__name__)

# LiveReloadHandler.DEFAULT_RELOAD_TIME = (
#     0  # https://github.com/lepture/python-livereload/pull/244
# )


# # def determine_watched_paths(self, config):
# #     watched_paths = [
# #         self.input_path,
# #         self.config_path,
# #         config.index.theme if self.watch_index_theme else None,
# #         config.index.template if self.watch_index_template else None,
# #         config.slides.theme if self.watch_slides_theme else None,
# #         config.slides.template if self.watch_slides_template else None,
# #     ]

# #     for path in watched_paths:
# #         if path:
# #             resolved_path = Path(path).resolve(strict=True).absolute()
# #             logger.debug(f'Watching: "{resolved_path}"')
# #             server.watch(filepath=resolved_path.as_posix(), func=reload, delay=1)


# def serve(
#     config: DictConfig, input_path: Path, output_path: Path
# ) -> None:
#     try:
#         server = livereload.Server()

#         # https://github.com/lepture/python-livereload/issues/232
#         server._setup_logging = lambda: None  # noqa: SLF001

#         watched_paths = [
#             input_path,
#             config.serve.config_path if config.serve.exists() else None,
#             # config.index.theme if config.serve.watch_index_theme else None,
#             # config.index.template if config.serve.watch_index_template else None,
#             # config.slides.theme if config.serve.watch_slides_theme else None,
#             # config.slides.template if config.serve.watch_slides_template else None,
#         ]

#         for path in watched_paths:
#             if path:
#                 resolved_path = Path(path).resolve(strict=True).absolute()
#                 logger.debug(f'Watching: "{resolved_path}"')
#                 server.watch(filepath=resolved_path.as_posix(), func=reload, delay=1)

#         ip, port = parse_ip_port(config.serve.dev_addr)

#         server.serve(
#             host=ip,
#             port=port,
#             root=output_path,
#             open_url_delay=0 if config.serve.open_in_browser else None,
#         )

#     finally:
#         if output_path.exists():
#             shutil.rmtree(output_path)
#             logger.debug(f'Removed "{output_path}"')

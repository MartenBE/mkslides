import json
from typing import Any

from click import Path
from omegaconf import DictConfig, ListConfig, OmegaConf

from mkslides.config import Config
from mkslides.mdfiletoprocess import MdFileToProcess
from mkslides.navtree import NavTree

# TODO
expected_tree_json = json.loads(
    """
    """,
)


def test_navtree_from_config(setup_paths: Any) -> None:
    _, output_path = setup_paths

    # TODO


def test_navtree_from_md_files(setup_paths: Any) -> None:
    _, output_path = setup_paths

    # TODO


# TODO: simulate following warnings:
#
# INFO    -  Cleaning site directory
# INFO    -  Building documentation to directory: /tmp/test/site
# INFO    -  The following pages exist in the docs directory, but are not included in the "nav" configuration:
#              - 1.md
#              - 2.md
#              - 3.md
#              - some/4.md
#              - some/5.md
# WARNING -  A reference to 'index.md' is included in the 'nav' configuration, which is not found in the documentation files.
# WARNING -  A reference to 'about.md' is included in the 'nav' configuration, which is not found in the documentation files.
# INFO    -  Documentation built in 0.06 seconds

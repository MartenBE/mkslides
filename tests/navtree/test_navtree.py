import json
from typing import Any

from deepdiff import DeepDiff

# from mkslides.mdfiletoprocess import MdFileToProcess
from omegaconf import OmegaConf

from mkslides.config import get_config
from mkslides.markupgenerator import MarkupGenerator
from mkslides.navtree import NavTree


def test_navtree_from_md_files(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = (cwd / "navtree" / "docs").resolve(strict=True)
    config = get_config(None)

    expected_tree_json = json.dumps(
        {
            "root": {
                "children": [
                    {
                        "category-1": {
                            "children": [
                                {
                                    "category-1/someslides-3.html": {
                                        "data": "someslides-3",
                                    },
                                },
                                {
                                    "category-1/someslides-4.html": {
                                        "data": "someslides-4",
                                    },
                                },
                            ],
                            "data": "category-1",
                        },
                    },
                    {
                        "category-2": {
                            "children": [
                                {
                                    "category-2/category-3": {
                                        "children": [
                                            {
                                                "category-2/category-3/someslides-7.html": {
                                                    "data": "someslides-7",
                                                },
                                            },
                                            {
                                                "category-2/category-3/someslides-8.html": {
                                                    "data": "someslides-8",
                                                },
                                            },
                                        ],
                                        "data": "category-3",
                                    },
                                },
                                {
                                    "category-2/someslides-5.html": {
                                        "data": "someslides-5",
                                    },
                                },
                                {
                                    "category-2/someslides-6.html": {
                                        "data": "someslides-6",
                                    },
                                },
                            ],
                            "data": "category-2",
                        },
                    },
                    {"someslides-1.html": {"data": "someslides-1"}},
                    {"someslides-2.html": {"data": "someslides-2"}},
                ],
                "data": None,
            },
        },
    )

    markup_generator = MarkupGenerator(config, input_path, output_path, strict=True)
    md_files, _ = markup_generator.scan_files()
    navtree = NavTree(input_path, output_path)
    navtree.from_md_files(md_files)

    assert DeepDiff(navtree.to_json(), expected_tree_json, ignore_order=True) == {}


def test_navtree_from_config(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = (cwd / "navtree" / "docs").resolve(strict=True)
    config_path = (cwd / "navtree" / "navtree-config.yml").resolve(strict=True)
    config = get_config(config_path)

    expected_tree_json = json.dumps(
        {
            "root": {
                "children": [
                    {
                        "category-1": {
                            "children": [
                                {
                                    "category-1/someslides-3.html": {
                                        "data": "someslides-3",
                                    },
                                },
                                {
                                    "category-1/someslides-4.html": {
                                        "data": "someslides-4",
                                    },
                                },
                            ],
                            "data": "category-1",
                        },
                    },
                    {
                        "category-2": {
                            "children": [
                                {
                                    "category-2/category-3": {
                                        "children": [
                                            {
                                                "category-2/category-3/someslides-7.html": {
                                                    "data": "someslides-7",
                                                },
                                            },
                                            {
                                                "category-2/category-3/someslides-8.html": {
                                                    "data": "custom-file-name-3",
                                                },
                                            },
                                        ],
                                        "data": "category-3",
                                    },
                                },
                                {
                                    "category-2/someslides-5.html": {
                                        "data": "someslides-5",
                                    },
                                },
                                {
                                    "category-2/someslides-6.html": {
                                        "data": "custom-file-name-2",
                                    },
                                },
                            ],
                            "data": "category-2",
                        },
                    },
                    {"someslides-1.html": {"data": "someslides-1"}},
                    {"someslides-2.html": {"data": "custom-file-name-1"}},
                ],
                "data": None,
            },
        },
    )

    navtree = NavTree(input_path, output_path)
    assert config.index.nav
    nav_from_config = OmegaConf.to_container(config.index.nav)
    assert isinstance(nav_from_config, list), "nav must be a list"
    navtree.from_config_json(nav_from_config)

    assert DeepDiff(navtree.to_json(), expected_tree_json, ignore_order=True) == {}


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

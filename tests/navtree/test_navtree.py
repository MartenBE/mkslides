from typing import Any

expected_tree_json = {
    "root": {
        "children": [
            {
                "category-1": {
                    "children": [
                        {"category-1/someslides-3.html": {"data": "someslides-3"}},
                        {"category-1/someslides-4.html": {"data": "someslides-4"}},
                    ],
                    "data": None,
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
                                "data": None,
                            },
                        },
                        {"category-2/someslides-5.html": {"data": "someslides-5"}},
                        {
                            "category-2/someslides-6.html": {
                                "data": "custom-file-name-2",
                            },
                        },
                    ],
                    "data": None,
                },
            },
            {"someslides-1.html": {"data": "someslides-1"}},
            {"someslides-2.html": {"data": "custom-file-name-1"}},
        ],
        "data": None,
    },
}


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

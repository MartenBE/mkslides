import json
from typing import Any

from omegaconf import DictConfig, ListConfig, OmegaConf

from mkslides.config import Config
from mkslides.mdfiletoprocess import MdFileToProcess
from mkslides.navtree import NavTree

# ruff: noqa: PLR0915, PLR2004


def test_navtree_from_json(setup_paths: Any) -> None:
    _, output_path = setup_paths

    json_data = json.loads(
        """
    [
        {
            "Home": "index.md"
        },
        {
            "User Guide": [
                {
                    "Writing your docs": "writing-your-docs.md"
                },
                {
                    "Styling your docs": "styling-your-docs.md"
                }
            ]
        },
        {
            "About": [
                {
                    "License": "dev/license.md"
                },
                {
                    "Release Notes": "./dev/notes/release-notes.md"
                }
            ]
        },
        "disclaimer.md",
        "./extras/info.md"
    ]
    """,
    )

    tree = NavTree(output_path)
    tree.from_json(json_data)

    assert len(tree.root_nodes) == 5

    home_node = tree.root_nodes[0]
    assert home_node.title == "Home"
    assert home_node.represents_file()
    assert not home_node.represents_folder()
    assert home_node.url == output_path / "index.html"
    assert len(home_node.children) == 0

    user_guide_node = tree.root_nodes[1]
    assert user_guide_node.title == "User Guide"
    assert not user_guide_node.represents_file()
    assert user_guide_node.represents_folder()
    assert len(user_guide_node.children) == 2

    writing_docs_node = user_guide_node.children[0]
    assert writing_docs_node.title == "Writing your docs"
    assert writing_docs_node.represents_file()
    assert not writing_docs_node.represents_folder()
    assert writing_docs_node.url == output_path / "writing-your-docs.html"
    assert len(writing_docs_node.children) == 0

    styling_docs_node = user_guide_node.children[1]
    assert styling_docs_node.title == "Styling your docs"
    assert styling_docs_node.represents_file()
    assert not styling_docs_node.represents_folder()
    assert styling_docs_node.url == output_path / "styling-your-docs.html"
    assert len(styling_docs_node.children) == 0

    about_node = tree.root_nodes[2]
    assert about_node.title == "About"
    assert not about_node.represents_file()
    assert about_node.represents_folder()
    assert len(about_node.children) == 2

    license_node = about_node.children[0]
    assert license_node.title == "License"
    assert license_node.represents_file()
    assert not license_node.represents_folder()
    assert license_node.url == output_path / "dev" / "license.html"
    assert len(license_node.children) == 0

    release_notes_node = about_node.children[1]
    assert release_notes_node.title == "Release Notes"
    assert release_notes_node.represents_file()
    assert not release_notes_node.represents_folder()
    assert (
        release_notes_node.url == output_path / "dev" / "notes" / "release-notes.html"
    )
    assert len(release_notes_node.children) == 0

    disclaimer_node = tree.root_nodes[3]
    assert disclaimer_node.title == "disclaimer"
    assert disclaimer_node.represents_file()
    assert not disclaimer_node.represents_folder()
    assert disclaimer_node.url == output_path / "disclaimer.html"
    assert len(disclaimer_node.children) == 0

    info_node = tree.root_nodes[4]
    assert info_node.title == "info"
    assert info_node.represents_file()
    assert not info_node.represents_folder()
    assert info_node.url == output_path / "extras" / "info.html"
    assert len(info_node.children) == 0


def test_navtree_from_md_files(setup_paths: Any) -> None:
    cwd, output_path = setup_paths

    config = OmegaConf.structured(Config)
    md_files = [
        MdFileToProcess(
            source_path=cwd / "index.md",
            destination_path=output_path / "index.html",
            slide_config=type_safe_config(
                OmegaConf.merge(
                    config,
                    OmegaConf.create(
                        """
                        slides:
                            title: "Home"
                        """,
                    ),
                ),
            ),
            markdown_content="",
        ),
        MdFileToProcess(
            source_path=cwd / "writing-your-docs.md",
            destination_path=output_path / "writing-your-docs.html",
            slide_config=type_safe_config(
                OmegaConf.merge(
                    config,
                    OmegaConf.create(
                        """
                    slides:
                        title: "Writing your docs"
                    """,
                    ),
                ),
            ),
            markdown_content="",
        ),
        MdFileToProcess(
            source_path=cwd / "styling-your-docs.md",
            destination_path=output_path / "styling-your-docs.html",
            slide_config=type_safe_config(
                OmegaConf.merge(
                    config,
                    OmegaConf.create(
                        """
                    slides:
                        title: "Styling your docs"
                    """,
                    ),
                ),
            ),
            markdown_content="",
        ),
        MdFileToProcess(
            source_path=cwd / "dev" / "license.md",
            destination_path=output_path / "dev" / "license.html",
            slide_config=type_safe_config(
                OmegaConf.merge(
                    config,
                    OmegaConf.create(
                        """
                    slides:
                        title: "License"
                    """,
                    ),
                ),
            ),
            markdown_content="",
        ),
        MdFileToProcess(
            source_path=cwd / "dev" / "notes" / "release-notes.md",
            destination_path=output_path / "dev" / "notes" / "release-notes.html",
            slide_config=type_safe_config(
                OmegaConf.merge(
                    config,
                    OmegaConf.create(
                        """
                    slides:
                        title: "Release Notes"
                    """,
                    ),
                ),
            ),
            markdown_content="",
        ),
        MdFileToProcess(
            source_path=cwd / "disclaimer.md",
            destination_path=output_path / "disclaimer.md",
            slide_config=type_safe_config(
                OmegaConf.merge(
                    config,
                    OmegaConf.create(),
                ),
            ),
            markdown_content="",
        ),
        MdFileToProcess(
            source_path=cwd / "extras" / "info.md",
            destination_path=output_path / "extras" / "info.md",
            slide_config=type_safe_config(
                OmegaConf.merge(
                    config,
                    OmegaConf.create(),
                ),
            ),
            markdown_content="",
        ),
    ]

    tree = NavTree(output_path)
    tree.from_md_files(md_files)

    assert len(tree.root_nodes) == 6

    home_node = tree.root_nodes[0]
    assert home_node.title == "Home"
    assert home_node.represents_file()
    assert not home_node.represents_folder()
    assert home_node.url == output_path / "index.html"
    assert len(home_node.children) == 0

    writing_docs_node = tree.root_nodes[1]
    assert writing_docs_node.title == "Writing your docs"
    assert writing_docs_node.represents_file()
    assert not writing_docs_node.represents_folder()
    assert writing_docs_node.url == output_path / "writing-your-docs.html"
    assert len(writing_docs_node.children) == 0

    styling_docs_node = tree.root_nodes[2]
    assert styling_docs_node.title == "Styling your docs"
    assert styling_docs_node.represents_file()
    assert not styling_docs_node.represents_folder()
    assert styling_docs_node.url == output_path / "styling-your-docs.html"
    assert len(styling_docs_node.children) == 0

    dev_node = tree.root_nodes[3]
    assert dev_node.title == "dev"
    assert not dev_node.represents_file()
    assert dev_node.represents_folder()
    assert len(dev_node.children) == 2

    license_node = dev_node.children[0]
    assert license_node.title == "License"
    assert license_node.represents_file()
    assert not license_node.represents_folder()
    assert license_node.url == output_path / "dev" / "license.html"
    assert len(license_node.children) == 0

    notes_node = dev_node.children[1]
    assert notes_node.title == "notes"
    assert not notes_node.represents_file()
    assert notes_node.represents_folder()
    assert len(notes_node.children) == 1

    release_notes_node = notes_node.children[0]
    assert release_notes_node.title == "Release Notes"
    assert release_notes_node.represents_file()
    assert not release_notes_node.represents_folder()
    assert (
        release_notes_node.url == output_path / "dev" / "notes" / "release-notes.html"
    )
    assert len(release_notes_node.children) == 0

    disclaimer_node = tree.root_nodes[4]
    assert disclaimer_node.title == "disclaimer"
    assert disclaimer_node.represents_file()
    assert not disclaimer_node.represents_folder()
    assert disclaimer_node.url == output_path / "disclaimer.html"
    assert len(disclaimer_node.children) == 0

    extras_node = tree.root_nodes[5]
    assert extras_node.title == "extras"
    assert not extras_node.represents_file()
    assert extras_node.represents_folder()
    assert len(extras_node.children) == 1

    info_node = extras_node.children[0]
    assert info_node.title == "info"
    assert info_node.represents_file()
    assert not info_node.represents_folder()
    assert info_node.url == output_path / "extras" / "info.html"
    assert len(info_node.children) == 0


def type_safe_config(config: ListConfig | DictConfig) -> DictConfig:
    if not isinstance(config, DictConfig):
        msg = f"Expected DictConfig, got {type(config)}"
        raise TypeError(msg)

    return config

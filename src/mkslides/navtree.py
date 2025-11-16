# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import logging
from pathlib import Path

from treelib import Tree

from mkslides.mdfiletoprocess import MdFileToProcess

logger = logging.getLogger(__name__)


class NavTree:
    def __init__(self, input_root_path: Path, output_root_path: Path) -> None:
        self.input_root_path = input_root_path
        self.output_root_path = output_root_path

        # Relative path as str is the index, title as str the data.
        self.tree = Tree()
        self.tree.create_node(identifier="root")

    def from_md_files(self, md_files: list[MdFileToProcess]) -> None:
        for md_file in md_files:
            relative_source_path = md_file.source_path.relative_to(
                self.input_root_path,
            )
            parts = relative_source_path.parts

            current_relative_source_path = Path()
            parent_node_id = str(self.tree.root)
            for part in parts:
                current_relative_source_path /= part

                node_id = None
                if (self.input_root_path / current_relative_source_path).is_dir():
                    node_id = str(current_relative_source_path)
                else:
                    node_id = str(current_relative_source_path.with_suffix(".html"))

                node_data = None
                if md_file.slide_config.slides.title:
                    node_data = md_file.slide_config.slides.title
                else:
                    node_data = current_relative_source_path.stem

                if node_id not in self.tree:
                    self.tree.create_node(
                        identifier=node_id,
                        parent=parent_node_id,
                        data=node_data,
                    )

                parent_node_id = node_id

    def from_config_json(self, json_data: list) -> None:
        assert isinstance(json_data, list), "json data must be a list"

        for item in json_data:
            self.__node_from_config_json(
                item,
                self.output_root_path,
                str(self.tree.root),
            )

    def __node_from_config_json(
        self,
        json_data: dict | str,
        current_path: Path,
        parent_node_id: str,
    ) -> None:
        # leaf node
        #
        # - filename.md
        #
        if isinstance(json_data, str):
            destination_path = (current_path / json_data).with_suffix(".html")
            node_id = str(destination_path.relative_to(self.output_root_path))
            node_data = destination_path.stem

            self.tree.create_node(
                identifier=node_id,
                parent=parent_node_id,
                data=node_data,
            )

        # category or leaf node with custom file name
        elif isinstance(json_data, dict):
            assert len(json_data.keys()) == 1, "json dict must have one key"

            title, content = next(iter(json_data.items()))

            # leaf node with custom name
            #
            # - custom-file-name: filename.md
            #
            if isinstance(content, str):
                destination_path = (current_path / content).with_suffix(".html")
                node_id = str(destination_path.relative_to(self.output_root_path))
                node_data = title

                self.tree.create_node(
                    identifier=node_id,
                    parent=parent_node_id,
                    data=node_data,
                )

            # category node
            #
            # - category:
            #   - ...
            #
            elif isinstance(content, list):
                destination_path = current_path / title
                node_id = str(f"{destination_path.relative_to(self.output_root_path)}")
                node_data = title

                self.tree.create_node(
                    identifier=node_id,
                    parent=parent_node_id,
                    data=node_data,
                )

                for item in content:
                    self.__node_from_config_json(item, destination_path, node_id)

            else:
                msg = f"json dict must have a string or list as value, but value is of {type(content)}"
                raise TypeError(msg)

        else:
            msg = (
                f"json data must be a string or dict, but is of type {type(json_data)}"
            )

            raise TypeError(msg)

    def is_node_leaf(self, node_id: str) -> bool:
        return self.tree[node_id].is_leaf(self.tree.identifier)

    def get_node_children(self, node_id: str) -> list:
        return sorted(self.tree.children(node_id), key=lambda n: n.identifier)

    def to_json(self) -> str:
        if not self.tree:
            return "{}"

        return self.tree.to_json(with_data=True)

    def validate_with_md_files(
        self,
        md_files: list[MdFileToProcess],
        strict: bool,
    ) -> None:
        md_file_relative_destination_paths = [
            str(md_file.destination_path.relative_to(self.output_root_path))
            for md_file in md_files
        ]

        files_not_in_navtree = []
        for md_file_relative_destination_path in md_file_relative_destination_paths:
            if md_file_relative_destination_path not in self.tree:
                source_file_name = str(
                    Path(md_file_relative_destination_path).with_suffix(".md"),
                )
                files_not_in_navtree.append(source_file_name)

        if files_not_in_navtree:
            logger.info(
                "The following pages exist in the slides directory, but are not included in the 'nav' configuration:",
            )

            for file_name in files_not_in_navtree:
                logger.info(f"\t- {file_name}")

        for node_id in self.tree.expand_tree():
            node = self.tree.get_node(node_id)
            assert node
            if (
                node.is_leaf(self.tree.identifier)
                and node.identifier not in md_file_relative_destination_paths
            ):
                source_file_name = Path(node.identifier).with_suffix(".md").name
                msg = f"A reference to '{source_file_name}' is included in the 'nav' configuration, which is not found in the slideshow files."
                if strict:
                    raise FileNotFoundError(msg)
                logger.warning(msg)

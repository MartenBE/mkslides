import logging
from pathlib import Path
from treelib import Tree

from mkslides.mdfiletoprocess import MdFileToProcess

logger = logging.getLogger(__name__)


class NavTree:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path

        # Relative path as str is the index, title as str the data.
        self.tree = Tree()
        self.tree.create_node(identifier="root", data="Root")

    def from_md_files(self, md_files: list[MdFileToProcess]) -> None:
        for md_file in md_files:
            relative_destination_path = md_file.relative_destination_path.relative_to(
                self.root_path
            )
            parts = relative_destination_path.parts

            path_relative_destination_path = Path()
            parent_node_id = self.tree.root
            for part in parts:
                path_relative_destination_path /= part
                node_id = str(path_relative_destination_path)
                node_data = md_file.source_path.stem

                if not node_id in self.tree:
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
                self.root_path,
                self.root_path,
                self.tree.root,
            )

    def __node_from_config_json(
        self,
        json_data: dict | str,
        current_actual_path: Path,
        current_virtual_path: Path,
        parent_node_id: str,
    ) -> None:

        # leaf node
        #
        # - filename.md
        #
        if isinstance(json_data, str):
            destination_path = (current_actual_path / json_data).with_suffix(".html")
            node_id = str(destination_path.relative_to(self.root_path))
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
                destination_path = (current_actual_path / content).with_suffix(".html")
                node_id = str(destination_path.relative_to(self.root_path))
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
                node_id = str(
                    f"{(current_virtual_path / title).relative_to(self.root_path)} (virtual node)"
                )
                node_data = title

                self.tree.create_node(
                    identifier=node_id,
                    parent=parent_node_id,
                )

                for item in content:
                    self.__node_from_config_json(
                        item,
                        current_actual_path,
                        current_virtual_path,
                        node_id,
                    )

            else:
                msg = f"json dict must have a string or list as value, but value is of {type(content)}"
                raise ValueError(msg)

        else:
            msg = (
                f"json data must be a string or dict, but is of type {type(json_data)}"
            )

            raise ValueError(msg)

    def to_json(self) -> dict:
        if not self.tree:
            return {}

        return self.tree.to_json(with_data=True)

from pathlib import Path

from omegaconf import OmegaConf

from mkslides.mdfiletoprocess import MdFileToProcess


class Node:
    def __init__(self, title: str) -> None:
        self.title: str = title
        self.__url: Path | None = None
        self.children: list["Node"] = []

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        if value:
            self.__url = value.with_suffix(".html")

    def represents_file(self) -> bool:
        self.__check_representation()
        return self.url != None

    def represents_folder(self) -> bool:
        self.__check_representation()
        return len(self.children) > 0

    def __check_representation(self) -> None:
        if self.url and len(self.children) != 0:
            raise ValueError("Node cannot represent both a file and a folder")

        if not self.url and len(self.children) == 0:
            raise ValueError("Node must represent either a file or a folder")


class NavTree:
    def __init__(self, root_path: Path) -> None:
        self.root_nodes: list[Node] = []
        self.root_path = root_path

    def from_json(self, json_data) -> None:
        assert isinstance(json_data, list), "json data must be a list"

        for item in json_data:
            node = self.__node_from_json_dict(item)
            self.root_nodes.append(node)

    def __node_from_json_dict(self, json_data: dict | str) -> Node:
        if isinstance(json_data, str):
            title = Path(json_data).stem
            node = Node(title)
            node.url = self.root_path / json_data
            return node
        elif isinstance(json_data, dict):
            assert len(json_data.keys()) == 1, "json dict must have one key"

            title, content = list(json_data.items())[0]
            if isinstance(content, str):
                node = Node(title)
                node.url = self.root_path / content
                return node
            elif isinstance(content, list):
                node = Node(title)
                for item in content:
                    child_node = self.__node_from_json_dict(item)
                    node.children.append(child_node)
                return node
            else:
                raise ValueError("json dict must have a string or list as value")
        else:
            raise ValueError("json data must be a string or dict")

    def from_md_files(self, md_files: list[MdFileToProcess]) -> None:
        for md_file in md_files:
            relative_destination_path = md_file.destination_path.relative_to(
                self.root_path
            )
            parts = relative_destination_path.parts

            node_list = self.root_nodes
            node = None
            for part in parts:
                node = next((n for n in node_list if n.title == part), None)
                if node is None:
                    node = Node(part)
                    node_list.append(node)
                node_list = node.children

            assert node

            node.title = md_file.slide_config.slides.title or md_file.source_path.stem
            print(md_file.slide_config)
            node.url = md_file.destination_path


# TODO simulate following warnings:
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
#

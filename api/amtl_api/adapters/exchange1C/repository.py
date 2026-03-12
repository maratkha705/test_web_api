"""
Репозиторий для обмена с 1C
на основе xml.etree.ElementTree
Альтернатива lxml
проход по элементам, очистка!!!!
"""

from typing import Any
import xml.etree.ElementTree as ElementTree


class Parse1cXML:
    """ парсер XML """
    def __init__(self, xml_file: str, flag: bool = False):
        self.xml_file = xml_file

    def __prepare_node__(self, node: ElementTree.ElementTree, matches: dict) -> dict: ...

    def get_root_nodes(self) -> ElementTree.ElementTree:

        tree: ElementTree.ElementTree = ElementTree.parse(self.xml_file)

        return tree.getroot()

    def _get_node(self, nodes: ElementTree.ElementTree) -> ElementTree.Element: ...

    def _add_node(self, nodes: ElementTree.ElementTree) -> ElementTree.Element: ...

    def _check_node(self, nodes: ElementTree.ElementTree) -> dict[str, Any]: ...

    def _find_parameters(self, nodes: ElementTree.Element) -> dict[str, Any]: ...

    def _check_price_type(self, nodes: ElementTree.Element) -> dict[str, Any]: ...

    def _find_price(self, nodes: ElementTree.Element) -> dict[str, Any]: ...

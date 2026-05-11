from __future__ import annotations
from typing import List


class HTMLNode:
    def __init__(self, 
                 tag: str | None = None,
                 value: str | None = None,
                 children: List[HTMLNode] | None = None,
                 props: dict[str, str] | None = None
                 ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        prop_str_list: list[str] = []
        for prop, val in self.props.items():
            prop_str_list.append(f" {prop}=\"{val}\"")
        return "".join(prop_str_list)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"


class LeafNode(HTMLNode):
    def __init__(self,
                 tag: str | None,
                 value: str | None,
                 props: dict[str, str] | None = None
                 ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props_to_html()})"

class ParentNode(HTMLNode):
    def __init__(self,
                 tag: str | None,
                 children: List[HTMLNode] | None,
                 props: dict[str, str] | None = None
                 ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError

        if self.children is None:
            raise ValueError("children is missing in parent node")

        children_html = []
        for child in self.children:
            children_html.append(child.to_html())

        return f"<{self.tag}{self.props_to_html()}>{"".join(children_html)}</{self.tag}>"

from typing import TypeVar, Optional, List

NodeT = TypeVar("NodeT", bound="HTMLNode")

class HTMLNode:
    def __init__(self, 
                 tag: Optional[str] = None,
                 value: Optional[str] = None,
                 children: Optional[List[NodeT]] = None,
                 props: Optional[dict[str, str]] = None
                 ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
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
                 tag: Optional[str],
                 value: Optional[str],
                 props: Optional[dict[str, str]] = None
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
                 tag: Optional[str],
                 children: Optional[List[HTMLNode]],
                 props: Optional[dict[str, str]] = None
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

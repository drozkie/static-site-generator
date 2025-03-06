from enum import Enum

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props.copy() if props is not None else {}

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return (self.tag == other.tag and
                    self.value == other.value and
                    self.children == other.children and
                    self.props == other.props)
        return False

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None or self.tag == "":
            return f"{self.value}"
        if self.props is None or self.props == {}:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        if self.tag == "img":
            return f"<{self.tag} " + self.props_to_html() + f">"
        return f"<{self.tag} " + self.props_to_html() + f">{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag, "", children, props={})

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("Tag is required.")
        if self.children is None or self.children == []:
            raise ValueError("Children required.")
        working_list = self.children

        def to_html_leafs(working_list):
            if len(working_list) == 0:
                return ""
            return working_list[0].to_html() + to_html_leafs(working_list[1:])

        return f"<{self.tag}>" + to_html_leafs(working_list) + f"</{self.tag}>"
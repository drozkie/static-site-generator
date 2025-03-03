from enum import Enum

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props.copy()

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
    def __init__(self, tag, value):
        super().__init__(tag, value, [], {})

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return f"{self.value}"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
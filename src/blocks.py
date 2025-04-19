from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):

    HEADING_RE = re.compile(r"^(\#{1,6}\s)")
    CODE_BLOCK_RE = re.compile(r"^(\`\`\`)\n(.*?)\n(\`\`\`)")
    QUOTE_RE = re.compile(r"^(\>\s)")
    UNORDERED_LIST_RE = re.compile(r"^(\-\s)")
    ORDERED_LIST_RE = re.compile(r"^(\d\.\s)")

    match block:
        case text if HEADING_RE.match(text):
            return BlockType.HEADING
        case text if CODE_BLOCK_RE.match(text):
            return BlockType.CODE
        case text if QUOTE_RE.match(text):
            return BlockType.QUOTE
        case text if UNORDERED_LIST_RE.match(text):
            return BlockType.UNORDERED_LIST
        case text if ORDERED_LIST_RE.match(text):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH
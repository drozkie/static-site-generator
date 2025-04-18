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

    match block:
        case text if HEADING_RE.match(text):
            return BlockType.HEADING
        case text if CODE_BLOCK_RE.match(text):
            return BlockType.CODE
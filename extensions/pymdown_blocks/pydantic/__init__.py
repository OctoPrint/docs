from pymdownx.blocks import BlocksExtension
from pymdownx.blocks.block import (
    Block,
    type_string_in,
    type_string,
    type_string_insensitive,
)
import xml.etree.ElementTree as etree


class PydanticBlock(Block):
    NAME = "pydantic"
    ARGUMENT = True
    OPTIONS = {
        "mode": [
            "full",
            type_string_in(["full", "table", "example"], type_string_insensitive),
        ],
        "key": ["", type_string],
    }

    def on_create(self, parent):
        return etree.SubElement(parent, "div")

    def on_add(self, block):
        return "Just **a test** with *markdown*."


class PydanticBlocksExtension(BlocksExtension):
    def extendMarkdownBlocks(self, md, block_mgr):
        block_mgr.register(PydanticBlock, self.getConfigs())


def makeExtension(*args, **kwargs):
    return PydanticBlocksExtension(*args, **kwargs)

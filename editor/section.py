#!/usr/bin/python
##-------------------------------##
## Pokemon Save Editor           ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Section                       ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import BinaryIO

## Constants
__all__: tuple[str] = ("Section",)
DATA_SIZE: int = 0x0F80
FOOTER_SIZE: int = 0x80
SECTION_SIZE: int = DATA_SIZE + FOOTER_SIZE
SECTION_SIGNATURE: int = 0x08012025
SECTION_NAMES: tuple[str, ...] = (
    "Trainer Info",
    "Team/Bag Info",
    "Game State",
    "Misc Data",
    "Rival Info",
    "PC Info {}"
)
# -[FOOTER]
ID_SIZE: int = 2
CHECKSUM_SIZE: int = 2
SIGNATURE_SIZE: int = 4
INDEX_SIZE: int = 4
ID_OFFSET: int = 0 - ID_SIZE - CHECKSUM_SIZE - SIGNATURE_SIZE - INDEX_SIZE
CHECKSUM_OFFSET: int = ID_OFFSET + ID_SIZE
SIGNATURE_OFFSET: int = CHECKSUM_OFFSET + CHECKSUM_SIZE
INDEX_OFFSET: int = SIGNATURE_OFFSET + SIGNATURE_SIZE


## Classes
class Section:
    """
    A single marke section of a save block
    """

    # -Constructor
    def __init__(self, _id: int, index: int, data: bytes) -> None:
        self.id: int = _id
        self.index: int = index
        self.data: bytes = data

    # -Class Methods
    @classmethod
    def from_file_pointer(cls, fp: BinaryIO) -> Section:
        '''Load a given section from a file pointer and return its id and data'''
        data: bytes = fp.read(DATA_SIZE)
        footer: bytes = fp.read(FOOTER_SIZE)
        signature_bytes: bytes = footer[SIGNATURE_OFFSET : SIGNATURE_OFFSET + SIGNATURE_SIZE]
        signature: int = int.from_bytes(signature_bytes, 'little', signed=False)
        if signature != SECTION_SIGNATURE:
            raise ValueError(f"Unexpected signature {hex(signature)} - does not match expected value.")
        id_bytes: bytes = footer[ID_OFFSET : ID_OFFSET + ID_SIZE]
        _id: int = int.from_bytes(id_bytes, 'little', signed=False)
        index_bytes: bytes = footer[INDEX_OFFSET : INDEX_OFFSET + INDEX_SIZE]
        index: int = int.from_bytes(index_bytes, 'little', signed=False)
        return cls(_id, index, data)

    # -Properties
    @property
    def name(self) -> str:
        name_count: int = len(SECTION_NAMES)
        name: str = SECTION_NAMES[min(self.id, name_count - 1)]
        if self.id >= name_count - 1:
            name = name.format(self.id - name_count + 1)
        return name

#!/usr/bin/python
##-------------------------------##
## Pokemon Save Editor           ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from pathlib import Path

from text import decode_string, encode_string

## Constants
FILE: Path = Path("./saves/lg02.sav")
SAVE_BLOCK_COUNT: int = 2
SECTION_BLOCK_COUNT: int = 14
SECTION_TITLES: tuple[str, ...] = (
    "Trainer Info",
    "Team/Bag Info",
    "Game State",
    "Misc Data",
    "Rival Info",
    "PC Info {}"
)
SECTION_SIGNATURE: int = 0x08012025
# -SECTION: TRAINER INFO
NAME_SIZE = 0x07
NAME_LENGTH = NAME_SIZE + 1
GENDER_OFFSET = 0x08
# -SUBSECTION: Text
TEXT_OFFSET = 0x14
TEXT_SPEED_MASK = 0x07
TEXT_FRAME_MASK = 0xF8
TEXT_FRAME_SHIFT = 0x03
# -SUBSECTION: Bitflags
BITFLAGS_OFFSET = 0x15
BITFLAGS_AUDIO_MASK = 0x1
BITFLAGS_STYLE_MASK = 0x2
BITFLAGS_SCENE_MASK = 0x4


## Functions
def parse_file(file: Path) -> None:
    """
    """
    fp = file.open('rb')
    for block in range(SAVE_BLOCK_COUNT):
        for section in range(SECTION_BLOCK_COUNT):
            data = fp.read(0x1000)
            _id: int = int.from_bytes(data[-12:-10], byteorder='little', signed=False)
            signature: int = int.from_bytes(data[-8:-4], byteorder='little', signed=False)
            assert signature == SECTION_SIGNATURE, f"Signature '{hex(signature)}' incorrect"
            title: str = SECTION_TITLES[min(_id, len(SECTION_TITLES) - 1)]
            if _id >= len(SECTION_TITLES) - 1:
                title = title.format(_id - len(SECTION_TITLES) + 1)
            print(f"[Position: {hex(fp.tell() - 0x1000)} ; Block:{block} ; Section:{section:2} ; Id:{_id:2}]{title}")
            match _id:
                # -Trainer Info
                case 0:
                    _parse_trainer_info(data)
    fp.close()


def _parse_trainer_info(data: bytes) -> None:
    """"""
    # -[NAME|GENDER]
    name = decode_string(data[0:NAME_LENGTH])
    gender = data[GENDER_OFFSET] == 0
    print(f"Name: {name} | Gender: {'Male' if gender else 'Female'}")
    # -Gender
    # -Options[TEXT]
    text_options = data[TEXT_OFFSET]
    speed = ("Slow", "Medium", "Fast")[text_options & TEXT_SPEED_MASK]
    frame = (text_options & TEXT_FRAME_MASK) >> TEXT_FRAME_SHIFT
    print(f"Frame: {frame + 1} | Speed: {speed}")
    # -Options[BITFLAGS]
    op = data[BITFLAGS_OFFSET]
    audio = "Stereo" if (op & BITFLAGS_AUDIO_MASK) >> 0 == 1 else "Mono"
    style = "Set" if (op & BITFLAGS_STYLE_MASK) >> 1 == 1 else "Switch"
    scene = (op & BITFLAGS_SCENE_MASK) >> 2 == 0
    print(f"Audio: {audio} ; Battle: {style} ; Visuals: {scene}")


## Body
parse_file(FILE)

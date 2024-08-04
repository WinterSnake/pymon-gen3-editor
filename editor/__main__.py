#!/usr/bin/python
##-------------------------------##
## Pokemon Save Editor           ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from pathlib import Path

## Constants
FILE: Path = Path("./saves/lg01.sav")
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
# -SUBSECTION: Text
TEXT_OFFSET = 0x14
TEXT_SPEED_MASK = 0x07
TEXT_FRAME_MASK = 0xF8
TEXT_FRAME_SHIFT = 0x03
# -SUBSECTION: Bitflags
BITFLAGS_OFFSET = 0x15
BITFLAGS_AUDIO_MASK = 0x1
BITFLAGS_STYLE_MASK = 0x2
BITFLAGS_SCENE_MASK = 0x3


## Classes


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
            assert signature == SECTION_SIGNATURE, f"Signature '{hex(sig)}' incorrect"
            if _id != 0:
                continue
            # -Trainer Info
            print(hex(fp.tell() - 0x1000))
            title: str = SECTION_TITLES[min(_id, len(SECTION_TITLES) - 1)]
            if _id >= len(SECTION_TITLES) - 1:
                title = title.format(_id - len(SECTION_TITLES) + 1)
            print(f"[Block:{block} ; Section:{section:2} ; Id:{_id:2}]{title}")
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
    fp.close()


## Body
parse_file(FILE)

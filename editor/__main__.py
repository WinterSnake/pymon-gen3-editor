#!/usr/bin/python
##-------------------------------##
## Pokemon Save Editor           ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from pathlib import Path

from pokemon import POKEMON_SIZE, PARTY_POKEMON_SIZE, Pokemon, PartyPokemon
from section import Section
from text import decode_string, encode_string

## Constants
FILE: Path = Path("./saves/lg02.sav")
SAVE_BLOCK_COUNT: int = 2
SECTION_BLOCK_COUNT: int = 14
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
            segment: Section = Section.from_file_pointer(fp)
            match segment.id:
                # -Trainer Info
                case 0:
                    pass
                    #_parse_trainer_info(segment.data)
                case 1:
                    print(segment.name)
                    _parse_team_info(segment.data)
    fp.close()


def _parse_team_info(data: bytes) -> None:
    """"""
    party_size: int = data[0x34]
    party_pokemon: list[PartyPokemon | None] = []
    for i in range(party_size):
        position = 0x38 + PARTY_POKEMON_SIZE * i
        length: int = position + PARTY_POKEMON_SIZE
        pokemon_bytes: bytes = data[position : length]
        pokemon = PartyPokemon.from_bytes(pokemon_bytes)


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

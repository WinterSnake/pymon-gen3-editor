#!/usr/bin/python
##-------------------------------##
## Pokemon Save Editor           ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Pokemon                       ##
##-------------------------------##

## Imports
from __future__ import annotations

## Constants
__all__: tuple[str] = ("POKEMON_SIZE", "PARTY_POKEMON_SIZE", "Pokemon", "PartyPokemon")
POKEMON_SIZE: int = 0x50
PARTY_POKEMON_SIZE: int = 0x64


## Classes
class Pokemon:
    """
    """

    # -Constructor
    def __init__(self) -> None:
        pass

    # -Class Methods
    @classmethod
    def from_bytes(cls, data: bytes) -> Pokemon:
        ''''''
        assert len(data) == POKEMON_SIZE
        personality = int.from_bytes(data[:4], 'little', signed=False)


class PartyPokemon:
    """
    """

    # -Constructor
    def __init__(self) -> None:
        pass

    # -Class Methods
    @classmethod
    def from_bytes(cls, data: bytes) -> PartyPokemon:
        ''''''
        assert len(data) == PARTY_POKEMON_SIZE
        pokemon = Pokemon.from_bytes(data[:POKEMON_SIZE])

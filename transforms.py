from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class PuzzleTransform(ABC):
    """Base class for a transformation in the initial scramble plan."""

    @abstractmethod
    def apply(self, board: "PuzzleBoard") -> None:
        """Apply this transformation to the supplied board."""
        raise NotImplementedError


@dataclass(frozen=True)
class SwapTransform(PuzzleTransform):
    first_tile_id: int
    second_tile_id: int

    def apply(self, board: "PuzzleBoard") -> None:
        board.swap_tiles_by_id(self.first_tile_id, self.second_tile_id)


@dataclass(frozen=True)
class RotateTransform(PuzzleTransform):
    tile_id: int
    quarter_turns: int

    def apply(self, board: "PuzzleBoard") -> None:
        board.tile_by_id(self.tile_id).rotate_clockwise(self.quarter_turns)


@dataclass(frozen=True)
class FlipTransform(PuzzleTransform):
    tile_id: int
    horizontal: bool

    def apply(self, board: "PuzzleBoard") -> None:
        tile = board.tile_by_id(self.tile_id)
        if self.horizontal:
            tile.flip_horizontal()
        else:
            tile.flip_vertical()


# Imported only for type checking, avoiding a runtime circular import.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from puzzle_board import PuzzleBoard

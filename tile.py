from __future__ import annotations

import cv2
import numpy as np


class Tile:
    """Represents one puzzle tile and its current orientation."""

    _IDENTITY = np.array([[1, 0], [0, 1]], dtype=np.int8)
    _ROTATE_CW = np.array([[0, 1], [-1, 0]], dtype=np.int8)
    _FLIP_HORIZONTAL = np.array([[-1, 0], [0, 1]], dtype=np.int8)
    _FLIP_VERTICAL = np.array([[1, 0], [0, -1]], dtype=np.int8)

    def __init__(self, tile_id: int, original_image: np.ndarray) -> None:
        self._tile_id = tile_id
        self._original_image = original_image.copy()
        self._image = original_image.copy()
        self._orientation = self._IDENTITY.copy()

    @property
    def tile_id(self) -> int:
        return self._tile_id

    @property
    def image(self) -> np.ndarray:
        return self._image

    def rotate_clockwise(self, quarter_turns: int = 1) -> None:
        """Rotate the tile clockwise by 90 degrees per quarter turn."""
        turns = quarter_turns % 4
        for _ in range(turns):
            self._image = cv2.rotate(self._image, cv2.ROTATE_90_CLOCKWISE)
            self._orientation = self._ROTATE_CW @ self._orientation

    def flip_horizontal(self) -> None:
        """Flip the tile from left to right."""
        self._image = cv2.flip(self._image, 1)
        self._orientation = self._FLIP_HORIZONTAL @ self._orientation

    def flip_vertical(self) -> None:
        """Flip the tile from top to bottom."""
        self._image = cv2.flip(self._image, 0)
        self._orientation = self._FLIP_VERTICAL @ self._orientation

    def reset_orientation(self) -> None:
        self._image = self._original_image.copy()
        self._orientation = self._IDENTITY.copy()

    def is_orientation_correct(self) -> bool:
        return bool(np.array_equal(self._orientation, self._IDENTITY))

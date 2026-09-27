from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from tile import Tile


class ImageProcessor:
    """Loads, prepares, divides and reassembles puzzle images."""

    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

    def __init__(self, target_size: int = 420) -> None:
        self.target_size = target_size

    def load_and_prepare(self, path: str, grid_size: int) -> np.ndarray:
        """
        Load an image, preserve its aspect ratio, and pad it to a square canvas.
        The resulting canvas is divisible evenly by the selected grid size.
        """
        extension = Path(path).suffix.lower()
        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError("Please select a JPG, JPEG, PNG or BMP image.")

        image = self._read_image(path)
        if image is None or image.size == 0:
            raise ValueError("The selected file could not be read as an image.")

        height, width = image.shape[:2]
        if height <= 0 or width <= 0:
            raise ValueError("The selected image has invalid dimensions.")

        usable_size = self.target_size - (self.target_size % grid_size)
        scale = min(usable_size / width, usable_size / height)

        new_width = max(1, int(round(width * scale)))
        new_height = max(1, int(round(height * scale)))

        interpolation = cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC
        resized = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=interpolation,
        )

        canvas = np.zeros((usable_size, usable_size, 3), dtype=np.uint8)
        y_offset = (usable_size - new_height) // 2
        x_offset = (usable_size - new_width) // 2

        canvas[
            y_offset:y_offset + new_height,
            x_offset:x_offset + new_width,
        ] = resized

        return canvas

    def split_into_tiles(self, image: np.ndarray, grid_size: int) -> list[Tile]:
        height, width = image.shape[:2]
        tile_height = height // grid_size
        tile_width = width // grid_size

        tiles: list[Tile] = []
        tile_id = 0

        for row in range(grid_size):
            for column in range(grid_size):
                y1 = row * tile_height
                y2 = y1 + tile_height
                x1 = column * tile_width
                x2 = x1 + tile_width

                tile_image = image[y1:y2, x1:x2].copy()
                tiles.append(Tile(tile_id, tile_image))
                tile_id += 1

        return tiles

    def reassemble(self, tiles: list[Tile], grid_size: int) -> np.ndarray:
        if not tiles:
            raise ValueError("There are no tiles to reassemble.")

        tile_height, tile_width = tiles[0].image.shape[:2]
        result = np.zeros(
            (tile_height * grid_size, tile_width * grid_size, 3),
            dtype=np.uint8,
        )

        for position, tile in enumerate(tiles):
            row, column = divmod(position, grid_size)
            y1 = row * tile_height
            y2 = y1 + tile_height
            x1 = column * tile_width
            x2 = x1 + tile_width
            result[y1:y2, x1:x2] = tile.image

        return result

    @staticmethod
    def _read_image(path: str) -> np.ndarray | None:
        """
        Read image bytes first, then decode with OpenCV.
        This is more reliable for Unicode file paths on Windows.
        """
        try:
            data = np.fromfile(path, dtype=np.uint8)
            return cv2.imdecode(data, cv2.IMREAD_COLOR)
        except (OSError, ValueError):
            return None

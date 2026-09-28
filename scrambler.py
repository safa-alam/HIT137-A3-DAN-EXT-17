from __future__ import annotations

import random

from transforms import FlipTransform, PuzzleTransform, RotateTransform, SwapTransform


class Scrambler:
    """
    Builds the complete transformation plan before applying it.

    The required operation counts are:
        3x3 -> 6 transformations
        4x4 -> 12 transformations
        5x5 -> 20 transformations

    Two swap transformations are included in every plan. All remaining
    operations are rotations or flips. Every tile ID is targeted at most once
    across the complete initial plan, including both sides of each swap.
    """

    TRANSFORMATION_COUNTS = {
        3: 6,
        4: 12,
        5: 20,
    }

    def build_plan(self, grid_size: int, tile_count: int) -> list[PuzzleTransform]:
        if grid_size not in self.TRANSFORMATION_COUNTS:
            raise ValueError("Grid size must be 3, 4 or 5.")

        operation_count = self.TRANSFORMATION_COUNTS[grid_size]
        swap_count = 2

        # Each swap uses two unique tile IDs instead of one.
        required_unique_tiles = operation_count + swap_count
        if required_unique_tiles > tile_count:
            raise ValueError("Not enough tiles to build a unique scramble plan.")

        chosen_ids = random.sample(range(tile_count), required_unique_tiles)
        id_cursor = 0

        operation_types = ["swap"] * swap_count

        # Guarantee at least one rotation and at least one flip.
        remaining_count = operation_count - swap_count
        operation_types.extend(["rotate", "flip"])
        operation_types.extend(
            random.choice(["rotate", "flip"])
            for _ in range(remaining_count - 2)
        )
        random.shuffle(operation_types)

        plan: list[PuzzleTransform] = []

        for operation_type in operation_types:
            if operation_type == "swap":
                first = chosen_ids[id_cursor]
                second = chosen_ids[id_cursor + 1]
                id_cursor += 2
                plan.append(SwapTransform(first, second))

            elif operation_type == "rotate":
                tile_id = chosen_ids[id_cursor]
                id_cursor += 1
                turns = random.choice([1, 2, 3])
                plan.append(RotateTransform(tile_id, turns))

            else:
                tile_id = chosen_ids[id_cursor]
                id_cursor += 1
                horizontal = random.choice([True, False])
                plan.append(FlipTransform(tile_id, horizontal))

        return plan

    @staticmethod
    def apply_plan(board: "PuzzleBoard", plan: list[PuzzleTransform]) -> None:
        for transformation in plan:
            transformation.apply(board)


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from puzzle_board import PuzzleBoard

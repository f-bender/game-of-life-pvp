import itertools
from typing import Literal, Self

import numpy as np
from PIL import ImageGrab


class Board:
    # "emoji" works correctly in VS Code console, but not in Windows Terminal,
    # but even in VS Code it breaks down at a width of ~100

    # "unicode" works reliably in VS Code console, but not in Windows Terminal, and if it works in Windows Terminal,
    # it's very inefficient

    # "ASCII" works flawlessly everywhere
    SYMBOLS = {
        "red": {
            "ASCII": "@",
            "unicode": "█",
            "emoji": "🟥",
        },
        "blue": {
            "ASCII": "=",
            "unicode": "▒",
            "emoji": "🟦",
        },
        "empty": {
            "ASCII": ".",
            "unicode": "░",
            "emoji": "⬛",
        },
    }

    def __init__(
        self,
        size: tuple[int, int] = (25, 25),  # height, width
        symbol_set: Literal["ASCII", "unicode", "emoji"] = "emoji",
    ) -> None:
        self.grid = np.zeros(size, dtype=np.uint8)  # upper 4 bits: blue, lower 4 bits: red

        self.red_symbol = self.SYMBOLS["red"][symbol_set]
        self.blue_symbol = self.SYMBOLS["blue"][symbol_set]
        self.empty_symbol = self.SYMBOLS["empty"][symbol_set]

        self.generation = 0

    def get_cell_counts(self) -> tuple[int, int]:
        """Returns number of red cells, and number of blue cells."""
        return int(np.sum(self.grid % 0x10)), int(np.sum(self.grid // 0x10))

    @classmethod
    def from_string_representation(
        cls, string_repr: str, symbol_set: Literal["ASCII", "unicode", "emoji"] = "emoji"
    ) -> Self:
        rows = [row.strip() for row in string_repr.strip().replace(" ", "").split("\n")]
        board = cls(size=(len(rows), len(rows[0])), symbol_set=symbol_set)

        for y, row in enumerate(rows):
            for x, cell in enumerate(row):
                board.grid[y, x] = (
                    0
                    if cell in itertools.chain(cls.SYMBOLS["empty"].values(), "se")
                    else (0x01 if cell in itertools.chain(cls.SYMBOLS["red"].values(), "ra") else 0x10)
                )

        return board

    @classmethod
    def from_screengrab(
        cls, grid_size: tuple[int, int] = (25, 25), symbol_set: Literal["ASCII", "unicode", "emoji"] = "emoji"
    ) -> Self:
        image_array = np.asarray(ImageGrab.grabclipboard())

        grid_height, grid_width = grid_size
        image_height, image_width = image_array.shape[:2]

        cell_width = image_width / grid_width
        cell_height = image_height / grid_height

        board = cls(size=grid_size, symbol_set=symbol_set)

        for grid_y, pixel_y in enumerate(np.arange(cell_height / 2, image_height, cell_height)):
            for grid_x, pixel_x in enumerate(np.arange(cell_width / 2, image_width, cell_width)):
                pixel = image_array[int(pixel_y), int(pixel_x)][:3]  # ignore alpha channel
                board.grid[grid_y, grid_x] = 0 if np.max(pixel) < 128 else (0x01 if np.argmax(pixel) == 0 else 0x10)

        return board

    def tick(self) -> None:
        neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        nums_neighbors = sum(np.roll(self.grid, offset, axis=(0, 1)) for offset in neighbor_offsets)

        red_neighbors = nums_neighbors % 0x10
        blue_neighbors = nums_neighbors // 0x10

        red = np.logical_and(
            red_neighbors > blue_neighbors,
            np.logical_or(
                red_neighbors == 3,
                np.logical_and(
                    self.grid,
                    red_neighbors == 2,
                ),
            ),
        ).astype(np.uint8)

        blue = np.logical_and(
            blue_neighbors > red_neighbors,
            np.logical_or(
                blue_neighbors == 3,
                np.logical_and(
                    self.grid,
                    blue_neighbors == 2,
                ),
            ),
        ).astype(np.uint8)

        unchanged_indices = np.logical_and(red_neighbors == blue_neighbors, red_neighbors > 0)
        prev_cells = self.grid[unchanged_indices]

        self.grid = blue * 0x10 + red
        self.grid[unchanged_indices] = prev_cells

        self.generation += 1

    def pretty_print(self) -> None:
        red_count, blue_count = self.get_cell_counts()
        print(f"Red: {red_count}, Blue: {blue_count}, Generation {self.generation}")
        for row in np.where(
            self.grid == 0, self.empty_symbol, np.where(self.grid == 1, self.red_symbol, self.blue_symbol)
        ):
            print("".join(row))

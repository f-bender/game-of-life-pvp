import time
from typing import Self
import numpy as np

class Board:
    def __init__(self, size: tuple[int, int] = (25, 25)) -> None:
        self.grid = np.zeros(size, dtype=bool)
        self.grid[2, 0] = True
        self.grid[2, 1] = True
        self.grid[2, 2] = True
        self.grid[1, 2] = True
        self.grid[0, 1] = True

    @classmethod
    def from_string_representation(cls, string_repr: str) -> Self:
        """TODO!"""

    def tick(self) -> None:
        neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        nums_neighbors = sum(np.roll(self.grid, offset, axis=(0, 1)) for offset in neighbor_offsets)

        self.grid = np.logical_or(nums_neighbors == 3, np.logical_and(self.grid, nums_neighbors == 2))

    def pretty_print(self) -> None:
        print()
        for row in np.where(self.grid, "🟥", "⬜"):
            print("".join(row))


if __name__ == "__main__":
    b = Board()
    for _ in range(1000):
        time.sleep(0.1)
        b.pretty_print() # ~3 ms
        b.tick() # ~150 us

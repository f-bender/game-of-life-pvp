import hashlib
import time

from board import Board


def main() -> None:
    board = Board.from_screengrab(grid_size=(25, 25))
    board.pretty_print()

    board_states = {hashlib.md5(board.grid).digest()}  # type: ignore[arg-type]

    while True:
        time.sleep(0.1)

        board.tick()  # ~150 us

        grid_hash = hashlib.md5(board.grid).digest()  # type: ignore[arg-type]
        # NOTE: in case everybody eventually dying is treated as a tie, remove "or 0 in board.get_cell_counts()"
        if grid_hash in board_states or 0 in board.get_cell_counts():  # get_cell_counts(): ~30 us
            break
        board_states.add(grid_hash)

        board.pretty_print()  # ~3 ms

    board.pretty_print()
    red, blue = board.get_cell_counts()

    if red > blue:
        print("RED WINS!")
    elif blue > red:
        print("BLUE WINS!")
    else:
        print("TIE!")


if __name__ == "__main__":
    main()

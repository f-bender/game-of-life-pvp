# Game of Life PVP

A light-weight, efficient implementation of [DougDoug](https://www.dougdoug.com/)'s interpretation of Conway's Game of Life as PvP (see [this VoD](https://www.twitch.tv/videos/1937525858)).

## Setup

> [!NOTE]  
> If you are familiar with [`poetry`](https://python-poetry.org/), you can use it do directly get started. Otherwise, you can safely ignore this hint.

1. Install [Python](https://www.python.org/downloads/) (the code was developed on Python 3.11, but *should* work with anything >=3.6). Make sure to include `pip` in the installation.
1. Install the dependencies: `pip install -r requirements.txt`

## Usage

### In Code

Import the board class

```python
from board import Board
```

Create a board from a string

```python
board = Board.from_string_representation("""
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦⬛🟦⬛⬛🟦⬛⬛🟦⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦⬛⬛🟦🟦⬛⬛⬛🟦⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦🟦🟦⬛⬛⬛⬛🟦⬛🟦⬛🟦🟦
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦⬛🟦⬛🟦🟦⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦⬛⬛🟦⬛⬛⬛🟦🟦🟦⬛🟦⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦⬛⬛⬛🟦⬛⬛🟦⬛⬛🟦
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦⬛🟦⬛🟦⬛🟦⬛⬛⬛🟦🟦⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦⬛⬛⬛⬛🟦🟦⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦🟦⬛⬛⬛⬛🟦⬛🟦
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦⬛⬛🟦⬛⬛⬛🟦⬛🟦⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛🟥⬛⬛🟥⬛🟥⬛⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛🟥🟥⬛🟥⬛⬛⬛🟥🟥🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛🟥⬛🟥⬛🟥🟥🟥⬛🟥⬛⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛🟥⬛🟥🟥🟥🟥🟥⬛🟥⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛🟥⬛🟥⬛🟥⬛🟥⬛⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛🟥⬛⬛⬛🟥🟥🟥⬛⬛🟥⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛🟥⬛⬛🟥⬛🟥⬛⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛🟥⬛🟥⬛🟥⬛⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛🟥⬛⬛⬛⬛🟥⬛⬛🟥🟥⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛🟥⬛⬛🟥⬛⬛🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
    """,
    symbol_set="emoji",
)
```

The `symbol_set` argument specifies how the board will be (pretty-)printed.  
`"emoji"` looks the nicest but might not work correctly on all consoles.
`"unicode"` looks still quite nice and should work on most consoles.
`"ASCII"` looks the worst but should work on all consoles.

For empty, blue, and red cells, you can use the characters

- `e` `b` `r` (starting letters, easy to remember)
- `s` `d` `a` (easy to type with left hand)
- ⬛ 🟦 🟥 (emoji representation)
- ░ ▒ █ (unicode representation)
- `.` `=` `@` (ASCII representation)

Spaces and newlines at the start or end of the string are ignored. These are for example all equivalent representations:

```python
[
    """ sssss
        aasdd
        ddsaa
    """,
    """
        e eeee
        rr  e  bb
        bb err
    """,
    """
. . . . .
@ @ . = =
= = . @ @
    """,
    """
        ⬛⬛⬛⬛⬛
        🟥🟥⬛🟦🟦
        🟦🟦⬛🟥🟥""",
]
```

Alternatively, a board can be created from a screengrab saved in the clipboard (e.g. using `Windows + Shift + S` if you're on Windows). The size of the grid still needs to provided manually. Note that the screengrab should be quite accurate and contain only the board itself, without any unrelated border around it.

```python
board = Board.from_screengrab(grid_size=(25, 25))
```

Running the simulation

```python
from time import sleep
while True:
    board.tick()
    board.pretty_print()
    sleep(0.5)
```

This is a simple endless loop which runs the simulation idefinitely, and prints the board to the console in every iteration.

[`main.py`](src/main.py) includes a more complex example which also checks for the winner.

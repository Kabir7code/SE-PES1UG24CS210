# Lab 4 – Changes to Dots and Boxes

## Task 1 – Bug fix (board display)
- `board.py`: the grid printed only the inner dots, so rows like `---.---` had no
  outer corners and the `|` walls did not line up. Each row now starts and ends with
  a dot (`.---.---.`) and every line has the same width.
- `board.py` / `game.py`: the final board still printed `Turn: P#` after the game had
  ended. `Board.display()` now takes `current=None` and skips the turn when it is
  `None`; `game.py` passes nothing on the final board.

## Task 2 – Feature: box ownership
- Completed boxes previously showed only `X`, so you could not tell who won which box.
- `board.py`: `Board` keeps an `owners` dict mapping `(row, col) -> player`.
  `add_line()` takes the moving player and records the owner of any box it completes.
  A box's owner is never overwritten once set.
- `game.py`: passes the current player to `add_line()`; the board now shows `1` or `2`
  in each completed box. Score and extra-turn rules are unchanged.

## Task 3 – Validation and robustness
- `H ² 0` crashed with a `ValueError` because `str.isdigit()` accepts Unicode digits
  like `²` that `int()` rejects. Rows/columns must now be ASCII digits.
- Orientation other than `H`/`V` gets its own clear message.
- Ctrl+D / Ctrl+C (`EOFError` / `KeyboardInterrupt`) at the prompt now exits cleanly
  instead of crashing.
- Invalid, out-of-range and repeated moves are rejected before the board is touched, so
  they can never change the board, score or turn. The game loop stops as soon as the
  board is complete, so no move can be made after the game ends.

## Task 4 – Tests
- `test_game.py` (standard-library `unittest`, no dependencies). Run with
  `python3 -m unittest -v`.
- Covers: valid horizontal move, valid vertical move, invalid/repeated move, box
  completion (score + extra turn), end-of-game condition, grid alignment, hidden final
  turn, box ownership, malformed input, out-of-range coordinates, `²` input, and EOF.

## Design decisions
- Kept the existing modular split: display/state in `board.py`, rules in `rules.py`,
  game flow and input in `game.py`; `main.py` is unchanged.
- Ownership is stored on the board (it is board state), while the game decides who the
  current player is.
- `player` defaults to `None` in `add_line()` so existing callers keep working.

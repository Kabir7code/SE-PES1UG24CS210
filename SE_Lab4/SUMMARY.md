# Lab 4 (VibeCoding) – Summary of Changes

**Student:** Kabir Raju G (PES1UG24CS210)
**Assigned repo:** [SETAPESU26/23_dots_and_boxes](https://github.com/SETAPESU26/23_dots_and_boxes) – terminal Dots and Boxes in Python
**AI tool used:** Claude

## Problems found in the original code

| # | Problem | Where it came from |
|---|---------|--------------------|
| 1 | Grid was misaligned and the outer dots were missing (`---.---` instead of `.---.---.`) | `Board.display()` joined cells with `.` only *between* them |
| 2 | Completed boxes showed only `X`, so you couldn't tell which player won them | The board stored *which* boxes were complete, not *who* completed them |
| 3 | The final board still printed `Turn: P#` after "Game over!" | `game.py` passed the current player to the final `display()` call |
| 4 | Typing `H ² 0` crashed with `ValueError` | `str.isdigit()` accepts Unicode digits like `²`, but `int()` rejects them |
| 5 | Pressing Ctrl+D at the prompt crashed with `EOFError` | `input()` was not wrapped in any error handling |

## Commits (one per task)

| Commit | Task | Change | Files |
|--------|------|--------|-------|
| `16c12ce` | Baseline | Original starter code added unchanged, so each task's diff is visible | all |
| `5062575` | Task 1 – Bug fix | Fixed grid alignment and removed `Turn` from the final board (bugs 1, 3) | `board.py`, `game.py` |
| `9658ce7` | Task 2 – Feature | Box ownership: completed boxes show `1` or `2` (bug 2) | `board.py`, `game.py` |
| `d002a61` | Task 3 – Validation | Safe input handling for `²`, bad orientation, Ctrl+D / Ctrl+C (bugs 4, 5) | `game.py` |
| `86a36b6` | Task 4 – Tests | 17 unit tests and `CHANGES.md` | `test_game.py`, `CHANGES.md` |
| `bb134d8` | Deliverables | Before and after videos | `before.mov`, `after.mov` |

## Details

### Task 1 – Bug fix
- `Board.display()` now starts and ends every row with a dot, so a 2×2 board prints a full 3×3 grid of dots and every line is the same width.
- `display()` takes `current=None`; when it is `None` the `Turn` part is skipped. The game calls it this way once the board is complete.

### Task 2 – Feature: box ownership
- `Board` has a new `owners` dictionary mapping `(row, col)` to the player who completed that box.
- `add_line()` takes the moving player and records the owner of any box it completes. An owner is never overwritten.
- `game.py` passes the current player into `add_line()`. Scoring and the "complete a box, play again" rule are unchanged.
- This change spans two modules (`board.py` and `game.py`) and works with the existing turn and score system, as the README requires.

### Task 3 – Validation and robustness
- Row and column must be ASCII digits, so `²` gets a clear message instead of crashing.
- An orientation other than `H` or `V` gets its own error message.
- `EOFError` (Ctrl+D) and `KeyboardInterrupt` (Ctrl+C) exit cleanly with a goodbye message.
- Malformed, out-of-range and repeated moves are rejected before the board is changed, so they cannot alter the board, score or turn. The game loop ends as soon as the board is full, so no move can be made after the game is over.

### Task 4 – Tests
`test_game.py` uses only the standard-library `unittest`. Run it with:

```bash
python3 -m unittest -v
```

All 17 tests pass. They cover the README's required cases (valid horizontal move, valid vertical move, invalid/repeated move, box completion, end of game) plus the grid layout, the hidden final turn, box ownership, malformed input, out-of-range coordinates, `²` input and EOF.

## Before vs after

| Behaviour | Before | After |
|-----------|--------|-------|
| Empty grid | `   .   ` (one dot per row) | `.   .   .` |
| Completed box | `\| X \|` | `\| 1 \|` or `\| 2 \|` |
| Final board | `Scores: P1=2  P2=2 \| Turn: P1` | `Scores: P1=2  P2=2` |
| `H ² 0` | `ValueError` traceback | "Row and column must be whole numbers (0-9)." |
| Ctrl+D | `EOFError` traceback | "Input closed. Exiting game. Goodbye!" |

## Design decisions
- Kept the original modular structure: board state and display in `board.py`, rules in `rules.py`, game flow and input in `game.py`. `main.py` is unchanged.
- Ownership is stored on the board because it is board state; the game decides who the current player is.
- `player` defaults to `None` in `add_line()`, so any existing callers still work.
- No third-party dependencies were added.

## How to run

```bash
cd SE_Lab4
python3 main.py
```

Enter moves as `H row col` or `V row col` (rows and columns start at 0).

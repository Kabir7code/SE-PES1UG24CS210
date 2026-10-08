# Scenario 23 - Dots and Boxes

## Overview

Dots and Boxes is a turn-based grid game. Players draw one line at a time between adjacent dots. Completing the fourth side of a box claims that box, earns a point, and gives the same player another turn.

The starter project is deliberately split into separate modules for game flow, board state, and rule validation. Read the existing implementation carefully before changing it.

## How to run

From this folder:

```text
python main.py
```

Enter moves in the form:

```text
H row column
```

or

```text
V row column
```

Rows and columns start at zero.

## Task 1 — Reproduce and investigate the bug

Run several games and deliberately create situations where a move completes one or more boxes.

Compare the score and turn behaviour before and after box completion. Identify the incorrect behaviour, trace it through the board and game-state logic, and fix it without replacing the modular structure.

Your before-change video should capture the broken behaviour clearly.

## Task 2 — Add a meaningful feature

Add a substantial gameplay feature that requires changes across more than one module.

The feature should make the game more complete rather than simply changing text or appearance. It should interact correctly with the existing board state and turn/score system.

## Task 3 — Validation and robustness

Strengthen input and game-state handling.

The program should safely handle malformed commands, invalid coordinates, repeated lines, and moves made after the board is already complete. Invalid input must not corrupt the board or score.

## Task 4 — Testing and quality

Create or expand automated tests covering the important game rules.

Include tests for at least:
- a valid horizontal move
- a valid vertical move
- an invalid/repeated move
- completion of a box
- the end-of-game condition

Document the changes you made and any design decisions that were important to the solution.

## Constraints

- Keep the project modular.
- Do not replace the game with an unrelated implementation.
- Preserve the existing gameplay.
- Avoid putting all new logic into `main.py`.
- Keep third-party dependencies out unless there is a clear need for them.

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history

# Lab 5: Reflection

## 1. Which issues were the easiest and hardest to fix?

The easiest were the mechanical ones: removing the unused `summary` variable and its trailing whitespace, changing `== None` to `is None`, renaming the functions to snake_case and adding docstrings. The tools point at the exact line and the fix is obvious.

The hardest was `rentBike`'s inconsistent return (Pylint R1710). Returning `False` on failure was simple, but `main` used `rentBike(9) is None` to detect a failed rental, so the fix had to be made together with a change in the caller (`not rent_bike(9)`). Deciding what `reset_station` should do instead of `pass` also needed a choice (log the error rather than hide it).

## 2. Did the tools report anything you disagreed with, or report the same thing twice?

I did not find a real false positive, but I do think some findings were rated generously. Bandit's B311 on `random.randint` is only Low severity, but in this program the number is a PIN that unlocks a bike, so a predictable generator is a genuine weakness and `secrets` is the right choice.

The tools also disagree with each other on style. Pylint accepts lines up to 100 characters while Flake8 enforces 79, so Pylint reached 10/10 while Flake8 still reported five long lines. Several issues were also reported twice: the unused variable (Pylint W0612 and Flake8 F841), `== None` (Pylint C0121 and Flake8 E711), trailing whitespace (C0303 and W291), and the swallowed exception (Pylint W0718 and Bandit B110).

## 3. How did the three tools complement each other?

Each tool found things the others cannot. Bandit alone found the SQL injection and the weak random generator. Pylint alone found the mutable default argument, the inconsistent returns, the naming and docstring problems. Flake8 alone enforced the 79-character PEP 8 line limit. Running all three gave a much fuller picture than any one of them, and fixing in the order security, then quality, then style kept each commit focused on one kind of problem.

## 4. How would you use static analysis in a real project, and what are its limits?

I would run all three tools automatically, for example as a pre-commit hook and in CI, so problems are caught before they are merged and the Pylint score cannot quietly drop. The 3.89 to 10.00 jump shows how much unreviewed code can hide.

Static analysis has limits, though. It only reads the source, so it cannot confirm that the program behaves correctly. A clean report does not mean the code is right: for example, `has_bikes` would have crashed on a station that does not exist, which only came up while reading the code around the `== None` warning, and `main()` running on import was not flagged by any tool. Static analysis needs to be paired with code review and tests.

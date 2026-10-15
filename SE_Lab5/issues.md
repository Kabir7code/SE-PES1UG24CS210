# Lab 5: Static Code Analysis - Issues Found and Fixed

Script analysed: `bike_share_stations.py` (bike-share station manager).
Line numbers refer to the **original** script (see the `*_before.txt` reports).

## Issue table

Ordered by severity, security issues first.

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| SQL injection via string-built query (Bandit B608, Medium) | Security | 9 | `addStation` builds the INSERT by concatenating `name` into the SQL string, so quote characters in `name` become part of the SQL itself and crafted input can break or change the statement (sqlite3 blocks stacked statements, but the query can still be manipulated) | Use a parameterized query: `VALUES (?, ?, ?)` with `(name, capacity, bikes)` passed separately |
| Weak random generator for unlock PIN (Bandit B311, Low) | Security | 22 | `random.randint` is a predictable pseudo-random generator, not suitable for a PIN that unlocks a bike | Use the `secrets` module: `secrets.randbelow(9000) + 1000` (still 1000-9999) |
| `try/except/pass` swallows errors (Bandit B110, Low) | Security / Bug | 32-35 | `resetStation` ignores every failure silently, so a failed reset looks like a success | Catch only `sqlite3.Error` and log it with `logging.error` instead of `pass` |
| Overly broad exception (Pylint W0718) | Bug | 34 | `except Exception` also hides unrelated programming errors | Catch the specific `sqlite3.Error` |
| Mutable default argument (Pylint W0102) | Bug | 8 | `log=[]` is created once and shared across every call to `addStation` | Default to `None` and create a new list inside the function |
| Inconsistent return statements (Pylint R1710) | Bug | 14-18 | `rentBike` returns `True` on success but falls off the end (returns `None`) on failure | Return `False` explicitly on failure; `main` now prints `not rent_bike(9)` so the demo output is unchanged |
| Comparison to `None` with `==` (Pylint C0121, Flake8 E711) | Bug / Style | 40 | `row[0] == None` should use identity; the function also crashes with `TypeError` when the station does not exist (`row` is `None`) | `if row is None or row[0] is None: return False` |
| Unused variable `summary` (Pylint W0612, Flake8 F841) | Code quality | 27 | `summary = len(stations)` is assigned but never used | Remove the line |
| Trailing whitespace (Pylint C0303, Flake8 W291) | Style | 27 | Stray spaces after the unused assignment | Removed along with the line above |
| Function names not snake_case (Pylint C0103) | Style | 8, 14, 21, 25, 31, 38 | `addStation`, `rentBike`, `unlockPin`, `fullStations`, `resetStation`, `hasBikes` break PEP 8 naming | Renamed to `add_station`, `rent_bike`, `unlock_pin`, `full_stations`, `reset_station`, `has_bikes` |
| Missing docstrings (Pylint C0114, C0116) | Documentation | 1, 8, 14, 21, 25, 31, 38, 45 | The module and every function lack a docstring | Added a one-line docstring to the module and each function |
| Lines too long (Pylint C0301, Flake8 E501) | Style | 5, 9 (Pylint, over 100); 5, 9, 15, 17, 26, 33, 39 (Flake8, over 79) | SQL strings and calls run past the line-length limits | Split long calls and SQL strings across lines |
| `main()` runs on import (not flagged by any tool) | Design | 53 | Importing the module would immediately execute the demo | Wrapped in `if __name__ == "__main__":` |

## Results before and after

| Tool | Before | After |
| ---- | ------ | ----- |
| Bandit | 3 issues (1 Medium, 2 Low) | 0 issues |
| Pylint | 3.89 / 10 | 10.00 / 10 |
| Flake8 | 10 warnings | 0 warnings |

## How the fixes map to commits

1. **Fix Bandit security issues** - SQL injection, `secrets` for the PIN, no more `try/except/pass`
2. **Fix Pylint issues** - naming, docstrings, mutable default, consistent returns, unused variable, `is None`, score 3.89 to 10.00
3. **Fix Flake8 formatting issues** - wrapped the remaining lines over 79 characters and refreshed all three after-reports

Reports: `pylint_report_before.txt`, `bandit_report_before.txt`, `flake8_report_before.txt` and the matching `*_after.txt` files.

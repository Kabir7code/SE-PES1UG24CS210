class Board:
    def __init__(self, rows=2, cols=2):
        self.rows = rows
        self.cols = cols
        self.horizontal = [[False] * cols for _ in range(rows + 1)]
        self.vertical = [[False] * (cols + 1) for _ in range(rows)]
        self.completed = set()

    def add_line(self, orientation, row, col):
        if orientation == "H":
            self.horizontal[row][col] = True
        else:
            self.vertical[row][col] = True
        self._update_completed()

    def _update_completed(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (
                    self.horizontal[r][c]
                    and self.horizontal[r + 1][c]
                    and self.vertical[r][c]
                    and self.vertical[r][c + 1]
                ):
                    self.completed.add((r, c))

    def is_complete(self):
        total = self.rows * (self.cols + 1) + self.cols * (self.rows + 1)
        used = sum(map(sum, self.horizontal)) + sum(map(sum, self.vertical))
        return used == total

    def display(self, scores, current=None):
        print()
        status = f"Scores: P1={scores[0]}  P2={scores[1]}"
        if current is not None:
            status += f" | Turn: P{current + 1}"
        print(status)

        for r in range(self.rows + 1):
            line = "."
            for c in range(self.cols):
                line += ("---" if self.horizontal[r][c] else "   ") + "."
            print(line)

            if r < self.rows:
                line = ""
                for c in range(self.cols + 1):
                    line += "|" if self.vertical[r][c] else " "
                    if c < self.cols:
                        line += " X " if (r, c) in self.completed else "   "
                print(line)
        print()

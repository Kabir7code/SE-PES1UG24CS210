import builtins
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from board import Board
from game import DotsAndBoxes
from rules import valid_move


FULL_GAME = ["H 0 0", "H 1 0", "V 0 0", "V 0 1", "H 0 1", "H 1 1",
             "V 0 2", "H 2 0", "H 2 1", "V 1 0", "V 1 1", "V 1 2"]


def play(inputs):
    """Run a game with scripted inputs; raise EOFError when they run out."""
    feed = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(feed)
        except StopIteration:
            raise EOFError

    out = io.StringIO()
    with patch.object(builtins, "input", fake_input), redirect_stdout(out):
        game = DotsAndBoxes()
        game.run()
    return game, out.getvalue()


class TestBoardDisplay(unittest.TestCase):
    def render(self, board, current=None):
        out = io.StringIO()
        with redirect_stdout(out):
            board.display([0, 0], current)
        return out.getvalue()

    def test_empty_grid_has_all_dots(self):
        text = self.render(Board())
        self.assertEqual(text.count("."), 9)  # 3 x 3 dots on a 2x2 board

    def test_rows_are_aligned(self):
        board = Board()
        board.add_line("H", 0, 0)
        board.add_line("V", 0, 0)
        lines = [l for l in self.render(board).splitlines()[2:] if l]
        self.assertEqual(lines[0], ".---.   .")
        self.assertEqual(lines[1][0], "|")
        self.assertEqual({len(l) for l in lines}, {9})

    def test_turn_hidden_when_current_is_none(self):
        self.assertNotIn("Turn", self.render(Board()))
        self.assertIn("Turn: P2", self.render(Board(), current=1))


class TestOwnership(unittest.TestCase):
    def test_completed_box_records_owner(self):
        board = Board()
        for move in [("H", 0, 0), ("H", 1, 0), ("V", 0, 0)]:
            board.add_line(*move, player=1)
        board.add_line("V", 0, 1, player=2)
        self.assertEqual(board.owners[(0, 0)], 2)

    def test_owner_not_overwritten(self):
        board = Board()
        for move in [("H", 0, 0), ("H", 1, 0), ("V", 0, 0), ("V", 0, 1)]:
            board.add_line(*move, player=1)
        board.add_line("H", 0, 1, player=2)
        self.assertEqual(board.owners[(0, 0)], 1)


class TestRules(unittest.TestCase):
    def test_valid_horizontal_move(self):
        board = Board()
        self.assertTrue(valid_move(board, "H", 0, 0))
        board.add_line("H", 0, 0, player=1)
        self.assertTrue(board.horizontal[0][0])

    def test_valid_vertical_move(self):
        board = Board()
        self.assertTrue(valid_move(board, "V", 1, 2))
        board.add_line("V", 1, 2, player=1)
        self.assertTrue(board.vertical[1][2])

    def test_repeated_move_is_invalid(self):
        board = Board()
        board.add_line("H", 1, 1, player=1)
        self.assertFalse(valid_move(board, "H", 1, 1))

    def test_repeated_move_does_not_change_score_or_turn(self):
        game, out = play(["H 0 0", "H 0 0"])
        self.assertIn("Invalid or already-used move.", out)
        self.assertEqual(game.scores, [0, 0])
        self.assertEqual(game.current, 1)

    def test_box_completion_scores_and_keeps_turn(self):
        game, out = play(["H 0 0", "H 1 0", "V 0 0", "V 0 1"])
        self.assertEqual(game.scores, [0, 1])
        self.assertEqual(game.current, 1)
        self.assertIn("Player 2 completed 1 box(es)", out)

    def test_end_of_game_condition(self):
        board = Board()
        self.assertFalse(board.is_complete())
        for move in FULL_GAME:
            o, r, c = move.split()
            board.add_line(o, int(r), int(c), player=1)
        self.assertTrue(board.is_complete())
        self.assertEqual(len(board.completed), 4)


class TestValidation(unittest.TestCase):
    def test_valid_move_bounds(self):
        board = Board()
        self.assertTrue(valid_move(board, "H", 2, 1))
        self.assertFalse(valid_move(board, "H", 3, 0))
        self.assertFalse(valid_move(board, "V", 0, 3))
        self.assertFalse(valid_move(board, "X", 0, 0))

    def test_superscript_digit_rejected_without_crash(self):
        _, out = play(["H ² 0"])
        self.assertIn("whole numbers", out)

    def test_bad_format_rejected(self):
        _, out = play(["H 0"])
        self.assertIn("Invalid format", out)

    def test_out_of_range_coordinates_rejected(self):
        game, out = play(["H 9 9", "V 0 3"])
        self.assertEqual(out.count("Invalid or already-used move."), 2)
        self.assertEqual(game.scores, [0, 0])

    def test_eof_exits_cleanly(self):
        _, out = play([])
        self.assertIn("Goodbye", out)


class TestFullGame(unittest.TestCase):
    def test_full_game_draw_and_no_turn_on_final_board(self):
        game, out = play(FULL_GAME)
        self.assertEqual(game.scores, [2, 2])
        self.assertIn("The game is a draw.", out)
        final_board = out.split("Game over!")[0].rsplit("Scores:", 1)[1]
        self.assertNotIn("Turn", final_board)


if __name__ == "__main__":
    unittest.main()

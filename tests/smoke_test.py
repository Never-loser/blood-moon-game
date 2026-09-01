"""Headless-ish smoke test: builds every screen and minigame, pumps the
event loop briefly, then quits. Run from the project root:

    python tests/smoke_test.py
"""
from __future__ import annotations

import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.app import BloodMoonApp


def pump(root, ms=150):
    """Pump the Tk event loop for ~ms milliseconds of *real* time."""
    import time

    deadline = time.time() + ms / 1000.0
    while time.time() < deadline:
        try:
            root.update()
        except tk.TclError:
            return
        time.sleep(0.01)


def main() -> int:
    app = BloodMoonApp(windowed=True)
    root = app.root
    root.withdraw()
    root.deiconify()

    from game.screens import (MenuScreen, SettingsScreen, DifficultyScreen,
                              Level1Screen, Level2Screen, Level3Screen, EndScreen)
    from game.minigames import (ColorGame, ChessPuzzle, RiddleGame, QuizSheet,
                                MathSprint, MazeGame, SnakeGame)

    # ---- full screens ----
    for cls in (MenuScreen, SettingsScreen, DifficultyScreen,
                Level1Screen, Level2Screen, Level3Screen, EndScreen):
        app.state.remaining_seconds = None
        app.show_screen(cls)
        pump(root, 200)
        assert app.screen_name == cls.__name__, f"{cls.__name__} not active"
        print(f"screen {cls.__name__:18s} OK")
    app.audio.stop()

    # ---- minigames ----
    app.show_screen(Level3Screen)  # parent context for modality
    for factory in (
        lambda: ColorGame(app),
        lambda: ChessPuzzle(app),
        lambda: RiddleGame(app),
        lambda: QuizSheet(app, "math"),
        lambda: QuizSheet(app, "biology"),
        lambda: QuizSheet(app, "chemistry"),
        lambda: MathSprint(app),
        lambda: MazeGame(app),
        lambda: SnakeGame(app),
    ):
        win = factory()
        pump(root, 250)
        win.close()
        pump(root, 60)
    print("minigames               OK")

    # ---- chess engine ----
    from game.minigames.chess_engine import (BLACK, WHITE, Board, describe,
                                             mate_in_two_keys, mates_in_one)

    back_rank = Board.from_placement(
        {"a1": "wR", "e1": "wK", "h8": "bK",
         "f7": "bP", "g7": "bP", "h7": "bP"}, WHITE)
    assert "Ra1-a8" in [describe(back_rank, m)
                        for m in mates_in_one(back_rank, WHITE)]

    # Queen defended by a rook mates; the same queen alone is only check.
    mated = Board.from_placement(
        {"a8": "bK", "b7": "wQ", "b1": "wR", "h1": "wK"}, BLACK)
    assert mated.is_checkmate(BLACK)
    lone = Board.from_placement({"a8": "bK", "b7": "wQ", "h1": "wK"}, BLACK)
    assert lone.in_check(BLACK) and not lone.is_checkmate(BLACK)

    assert Board.from_placement(
        {"a8": "bK", "c7": "wQ", "h1": "wK"}, BLACK).is_stalemate(BLACK)

    # A pinned rook may only move along the pinning line.
    pin = Board.from_placement(
        {"e1": "wK", "e2": "wR", "e8": "bR", "a1": "bK"}, WHITE)
    # e-file is index 4; a pinned rook must stay on it.
    assert all(m[3] == 4 for m in pin.legal_moves(WHITE)
               if (m[0], m[1]) == (6, 4))
    print("chess engine            OK")

    # ---- chess puzzle integrity ----
    from game.minigames.chess_puzzle import (CELL, MARGIN, PLAYER_COLOR,
                                             PUZZLE_PLACEMENT)

    position = Board.from_placement(PUZZLE_PLACEMENT, PLAYER_COLOR)
    assert not mates_in_one(position, WHITE), "puzzle has a mate in one"
    keys = mate_in_two_keys(position, WHITE)
    assert len(keys) == 1, f"key must be unique, got {len(keys)}"
    after_key = position.apply(keys[0])
    black_replies = after_key.legal_moves(BLACK)
    assert black_replies, "black must have a reply"
    for reply in black_replies:
        assert mates_in_one(after_key.apply(reply), WHITE), \
            f"no mate after {describe(after_key, reply)}"
    print("chess puzzle unique     OK")

    # ---- chess solution walk-through (through the real UI) ----
    class E:  # fake tkinter event
        pass

    def click(widget, rank, file):
        E.x = MARGIN + file * CELL + CELL // 2
        E.y = MARGIN + rank * CELL + CELL // 2
        widget.on_click(E)
        pump(root, 30)

    def play(widget, move):
        click(widget, move[0], move[1])
        click(widget, move[2], move[3])
        if widget._pending_promotion:  # choose the promotion piece
            index = [m[4] for m in widget._pending_promotion].index(move[4])
            E.x = (MARGIN + max(0, min(move[3], 4)) * CELL
                   + index * CELL + CELL // 2)
            E.y = MARGIN + move[2] * CELL + CELL // 2
            widget.on_click(E)
            pump(root, 30)

    puzzle = ChessPuzzle(app)
    pump(root, 120)

    # A wrong first move must be refused, not accepted.
    wrong = next(m for m in puzzle.board.legal_moves(WHITE) if m != keys[0])
    play(puzzle, wrong)
    assert puzzle.phase == 0, "a non-key move advanced the puzzle"
    pump(root, 1400)  # the board takes the wrong move back
    assert puzzle.board.piece_at(*keys[0][:2]), "board did not revert"

    play(puzzle, keys[0])
    assert puzzle.phase == 1, "the key move was rejected"
    pump(root, 800)  # black answers 650 ms later

    mate = mates_in_one(puzzle.board, WHITE)[0]
    play(puzzle, mate)
    assert puzzle.solved, "mating move was not accepted"
    pump(root, 1600)  # finish() fires 1400 ms after mate
    assert puzzle.result is True, "chess did not finish"
    print("chess walkthrough       OK")

    # ---- riddle answer normalization ----
    riddle = RiddleGame(app)
    pump(root, 80)
    riddle.rows[0]["entry"].insert(0, "  MATCH ")
    riddle.check(0)
    assert riddle.solved[0], "normalized answer failed"
    riddle.close()
    print("riddle matching         OK")

    # ---- snake reversal guard ----
    snake_win = SnakeGame(app)
    pump(root, 100)

    class KE:
        def __init__(self, keysym):
            self.keysym = keysym

    snake_win.change_direction(KE("Down"))  # moving Down → must be ignored
    assert snake_win.direction == "Down"
    snake_win.change_direction(KE("Right"))  # perpendicular turn allowed
    assert snake_win.direction == "Right"
    snake_win.close()
    print("snake direction guard   OK")

    # ---- level progression routing ----
    # Regression guard: finishing a room must open the *next* room and,
    # after room 3, the ending. A missing key here used to raise KeyError
    # and made the game impossible to finish past level 2.
    from game.screens.game_over import route_after_level, GameOverScreen

    expected = {1: "Level2Screen", 2: "Level3Screen", 3: "EndScreen"}
    for finished, next_screen in expected.items():
        app.state.remaining_seconds = None
        route_after_level(app, finished)
        pump(root, 60)
        assert app.screen_name == next_screen, (
            f"finishing level {finished} opened {app.screen_name}, "
            f"expected {next_screen}")
    print("level progression       OK")

    # ---- game over screen ----
    app.show_screen(GameOverScreen)
    pump(root, 80)
    assert app.screen_name == "GameOverScreen"
    app.state.current_level = 1
    print("game over screen        OK")

    # ---- save/load round trip ----
    app.state.theme_id = 2
    app.state.language = "fa"
    app.state.difficulty = "hard"
    app.state.current_level = 3
    app.state.complete_task(1, "color")
    app.state.save()
    from game.state import GameState

    reloaded = GameState.load()
    assert reloaded.theme_id == 2 and reloaded.language == "fa"
    assert reloaded.difficulty == "hard" and reloaded.current_level == 3
    print("save/load round trip    OK")

    os.remove(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "save.json"))  # keep repo clean

    app.quit()
    print("\nALL SMOKE TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""The level-1 chess puzzle: a real board, real rules, mate in two.

The previous version was not chess. It showed five screenshots of a chess
program and asked the player to click seven hard-coded rectangles in a
fixed order; there were no pieces, no legality, and no way to lose except
by clicking the wrong pixel. This version draws the board itself, moves
pieces under real rules, and answers back: Black picks its most stubborn
defence and the player has to find the mate against it.

The position is verified at import time by :mod:`chess_engine` - the key
is unique, no mate in one exists, and every Black reply is still mated.
"""
from __future__ import annotations

import random
import tkinter as tk

from ..i18n import tr
from ..themes import SPACE
from .base import Minigame
from .chess_engine import (BLACK, WHITE, Board, assert_no_special_moves,
                           describe, mates_in_one, square_name)

# --------------------------------------------------------------------------
# The puzzle. White to play and mate in two.
#
#   White: Qe5, Kh5, Nc3, Na1, pawns d7 and f7
#   Black: Ka3, Nc4, pawn a5
#
# Key: Qe5-b5!  - quiet, neither a check nor a capture, which is exactly
# what makes a two-mover hard. All 45 other first moves fail. Black has
# seven defences and five distinct mates answer them, including the
# underpromotion f7-f8=B.
# --------------------------------------------------------------------------
PUZZLE_PLACEMENT = {
    "d7": "wP", "f7": "wP",
    "a5": "bP", "e5": "wQ", "h5": "wK",
    "c4": "bN", "a3": "bK", "c3": "wN",
    "a1": "wN",
}
PLAYER_COLOR = WHITE

# Solid glyphs for both colours, tinted by side - the outline glyphs
# (U+2654..) render inconsistently across Windows fonts.
GLYPHS = {"K": "♚", "Q": "♛", "R": "♜",
          "B": "♝", "N": "♞", "P": "♟"}
GLYPH_FONTS = ("Segoe UI Symbol", "Arial Unicode MS", "DejaVu Sans")

CELL = 62
MARGIN = 22
BOARD_PIXELS = CELL * 8

PHASE_KEY, PHASE_MATE, PHASE_DONE = 0, 1, 2


def _board_colors(theme):
    """Light/dark squares tuned to the active mood."""
    if theme.id == 1:
        return "#c3ab92", "#6d4a41"
    return "#a9bed2", "#3c5068"


class ChessPuzzle(Minigame):
    def __init__(self, app):
        super().__init__(app, size=(BOARD_PIXELS + 2 * MARGIN + 40,
                                    BOARD_PIXELS + 2 * MARGIN + 190))
        self.title(tr("chess.title"))

        self.start_board = Board.from_placement(PUZZLE_PLACEMENT, PLAYER_COLOR)
        assert_no_special_moves(self.start_board)
        self.keys = _solve_keys(self.start_board)

        self.board = self.start_board
        self.phase = PHASE_KEY
        self.selected: tuple[int, int] | None = None
        self.last_move = None
        self.solved = False
        self._pending_promotion: list | None = None
        self._revert_job = None

        theme = self.theme
        self.light, self.dark = _board_colors(theme)
        self.glyph_font = _pick_glyph_font()

        tk.Label(self, text=tr("chess.mate_in_two"), bg=theme.bg,
                 fg=theme.accent, font=theme.ui_font(13, "bold")).pack(
            pady=(SPACE["md"], 2))
        self.hint = tk.Label(self, text=tr("chess.find_key"), bg=theme.bg,
                             fg=theme.fg_dim, font=theme.body_font(11))
        self.hint.pack()

        self.canvas = tk.Canvas(
            self, width=BOARD_PIXELS + 2 * MARGIN,
            height=BOARD_PIXELS + 2 * MARGIN, bg=theme.surface,
            highlightthickness=0, bd=0)
        self.canvas.pack(pady=SPACE["md"])
        self.canvas.bind("<Button-1>", self.on_click)

        self.feedback = tk.Label(self, text="", bg=theme.bg, fg=theme.muted,
                                 font=theme.ui_font(11), wraplength=BOARD_PIXELS)
        self.feedback.pack()

        self.reset_btn = tk.Button(self, text=tr("chess.reset"),
                                   command=self.reset)
        self.reset_btn.pack(pady=(SPACE["sm"], SPACE["md"]))

        self.draw()

    # ==================================================================== draw
    def draw(self) -> None:
        self.canvas.delete("all")
        theme = self.theme
        legal_targets = self._targets_for_selection()

        for rank in range(8):
            for file in range(8):
                x0 = MARGIN + file * CELL
                y0 = MARGIN + rank * CELL
                light = (rank + file) % 2 == 0
                fill = self.light if light else self.dark

                if self.last_move and (rank, file) in (
                        (self.last_move[0], self.last_move[1]),
                        (self.last_move[2], self.last_move[3])):
                    fill = _blend(fill, theme.accent, 0.35)
                if self.selected == (rank, file):
                    fill = _blend(fill, theme.accent_bright, 0.55)

                self.canvas.create_rectangle(x0, y0, x0 + CELL, y0 + CELL,
                                             fill=fill, outline="")

                if (rank, file) in legal_targets:
                    occupied = self.board.piece_at(rank, file) is not None
                    center = (x0 + CELL / 2, y0 + CELL / 2)
                    if occupied:
                        # Ring around a capturable piece.
                        self.canvas.create_oval(
                            x0 + 4, y0 + 4, x0 + CELL - 4, y0 + CELL - 4,
                            outline=theme.accent_bright, width=3)
                    else:
                        self.canvas.create_oval(
                            center[0] - 8, center[1] - 8,
                            center[0] + 8, center[1] + 8,
                            fill=theme.accent_bright, outline="")

        self._draw_check_marker()
        self._draw_pieces()
        self._draw_coordinates()
        if self._pending_promotion:
            self._draw_promotion_picker()

    def _draw_pieces(self) -> None:
        for rank in range(8):
            for file in range(8):
                piece = self.board.piece_at(rank, file)
                if not piece:
                    continue
                x = MARGIN + file * CELL + CELL / 2
                y = MARGIN + rank * CELL + CELL / 2
                glyph = GLYPHS[piece[1]]
                white = piece[0] == WHITE
                fill = "#f6f1e7" if white else "#17110f"
                edge = "#241a16" if white else "#c9bfae"
                # Larger glyph behind = a cheap outline, so white pieces
                # stay visible on light squares and vice versa.
                self.canvas.create_text(x, y, text=glyph, fill=edge,
                                        font=(self.glyph_font,
                                              int(CELL * 0.80)))
                self.canvas.create_text(x, y, text=glyph, fill=fill,
                                        font=(self.glyph_font,
                                              int(CELL * 0.72)))

    def _draw_check_marker(self) -> None:
        for color in (WHITE, BLACK):
            if not self.board.in_check(color):
                continue
            king = self.board.find_king(color)
            if not king:
                continue
            rank, file = king
            x0 = MARGIN + file * CELL
            y0 = MARGIN + rank * CELL
            self.canvas.create_rectangle(x0, y0, x0 + CELL, y0 + CELL,
                                         outline=self.theme.danger, width=4)

    def _draw_coordinates(self) -> None:
        theme = self.theme
        font = theme.ui_font(9, "bold")
        for file in range(8):
            x = MARGIN + file * CELL + CELL / 2
            self.canvas.create_text(x, MARGIN + BOARD_PIXELS + 10,
                                    text="abcdefgh"[file], fill=theme.muted,
                                    font=font)
        for rank in range(8):
            y = MARGIN + rank * CELL + CELL / 2
            self.canvas.create_text(MARGIN - 11, y, text=str(8 - rank),
                                    fill=theme.muted, font=font)

    # =============================================================== promotion
    def _draw_promotion_picker(self) -> None:
        theme = self.theme
        moves = self._pending_promotion
        _, _, to_rank, to_file, _ = moves[0]
        x0 = MARGIN + max(0, min(to_file, 4)) * CELL
        y0 = MARGIN + to_rank * CELL
        self.canvas.create_rectangle(x0 - 2, y0 - 2, x0 + 4 * CELL + 2,
                                     y0 + CELL + 2, fill=theme.surface,
                                     outline=theme.accent, width=2,
                                     tags="promo")
        for index, move in enumerate(moves):
            cx = x0 + index * CELL + CELL / 2
            cy = y0 + CELL / 2
            self.canvas.create_text(cx, cy, text=GLYPHS[move[4]],
                                    fill="#f6f1e7",
                                    font=(self.glyph_font, int(CELL * 0.66)),
                                    tags=("promo", f"promo{index}"))

    def _promotion_click(self, x: int, y: int) -> bool:
        moves = self._pending_promotion
        if not moves:
            return False
        _, _, to_rank, to_file, _ = moves[0]
        x0 = MARGIN + max(0, min(to_file, 4)) * CELL
        y0 = MARGIN + to_rank * CELL
        if not (x0 <= x <= x0 + 4 * CELL and y0 <= y <= y0 + CELL):
            self._pending_promotion = None  # clicking away cancels
            self.draw()
            return True
        index = int((x - x0) // CELL)
        if 0 <= index < len(moves):
            move = moves[index]
            self._pending_promotion = None
            self.play(move)
        return True

    # =================================================================== input
    def on_click(self, event: tk.Event) -> None:
        if self.phase == PHASE_DONE or self._revert_job:
            return
        if self._promotion_click(event.x, event.y):
            return

        file = (event.x - MARGIN) // CELL
        rank = (event.y - MARGIN) // CELL
        if not (0 <= rank < 8 and 0 <= file < 8):
            return
        rank, file = int(rank), int(file)

        if self.selected:
            candidates = [m for m in self.board.legal_moves(PLAYER_COLOR)
                          if (m[0], m[1]) == self.selected
                          and (m[2], m[3]) == (rank, file)]
            if len(candidates) > 1:  # promotion: ask which piece
                self._pending_promotion = candidates
                self.selected = None
                self.draw()
                return
            if candidates:
                self.selected = None
                self.play(candidates[0])
                return

        if self.board.color_at(rank, file) == PLAYER_COLOR:
            self.selected = (rank, file)
        else:
            self.selected = None
            if self.board.piece_at(rank, file) is not None:
                self.set_feedback(tr("chess.not_yours"), self.theme.muted)
        self.draw()

    def _targets_for_selection(self) -> set[tuple[int, int]]:
        if not self.selected:
            return set()
        return {(m[2], m[3]) for m in self.board.legal_moves(PLAYER_COLOR)
                if (m[0], m[1]) == self.selected}

    # ==================================================================== play
    def play(self, move) -> None:
        text = describe(self.board, move)
        if self.phase == PHASE_KEY:
            if move not in self.keys:
                self._show_and_revert(move, tr("chess.not_forcing", move=text))
                return
            self.board = self.board.apply(move)
            self.last_move = move
            self.phase = PHASE_MATE
            self.draw()
            self.set_feedback(tr("chess.key_found", move=text), self.theme.ok)
            self.after(650, self._black_replies)
            return

        # PHASE_MATE - the move has to be mate.
        after = self.board.apply(move)
        if after.is_checkmate(BLACK):
            self.board = after
            self.last_move = move
            self.phase = PHASE_DONE
            self.solved = True
            self.selected = None
            self.draw()
            self.set_feedback(tr("chess.solved"), self.theme.ok)
            self.hint.config(text=tr("chess.mate_delivered", move=text))
            self.after(1400, self.finish)
        else:
            self._show_and_revert(move, tr("chess.not_mate", move=text))

    def _black_replies(self) -> None:
        replies = self.board.legal_moves(BLACK)
        if not replies:
            return
        reply = _most_stubborn(self.board, replies)
        text = describe(self.board, reply)
        self.board = self.board.apply(reply)
        self.last_move = reply
        self.draw()
        self.hint.config(text=tr("chess.now_mate"))
        self.set_feedback(tr("chess.black_played", move=text), self.theme.fg_dim)

    def _show_and_revert(self, move, message: str) -> None:
        """Play the wrong move so the player sees it, then take it back."""
        before = self.board
        self.board = self.board.apply(move)
        self.last_move = move
        self.selected = None
        self.draw()
        self.set_feedback(message, self.theme.danger)

        def undo():
            self._revert_job = None
            self.board = before
            self.last_move = None
            self.draw()

        self._revert_job = self.after(1300, undo)

    # =================================================================== misc
    def set_feedback(self, text: str, color: str | None = None) -> None:
        self.feedback.config(text=text, fg=color or self.theme.muted)

    def reset(self) -> None:
        if self._revert_job:
            try:
                self.after_cancel(self._revert_job)
            except Exception:
                pass
            self._revert_job = None
        self.board = self.start_board
        self.phase = PHASE_KEY
        self.selected = None
        self.last_move = None
        self._pending_promotion = None
        self.hint.config(text=tr("chess.find_key"))
        self.set_feedback("")
        self.draw()

    def on_close(self) -> None:
        if self._revert_job:
            try:
                self.after_cancel(self._revert_job)
            except Exception:
                pass
            self._revert_job = None


# ==========================================================================
# Helpers
# ==========================================================================
def _solve_keys(board: Board) -> list:
    from .chess_engine import mate_in_two_keys

    keys = mate_in_two_keys(board, PLAYER_COLOR)
    if not keys:
        raise AssertionError("puzzle position has no mate in two")
    return keys


def _most_stubborn(board: Board, replies: list) -> list:
    """Black's most testing defence: the one with the fewest mating answers."""
    scored = [(len(mates_in_one(board.apply(reply), PLAYER_COLOR)), reply)
              for reply in replies]
    fewest = min(count for count, _ in scored)
    return random.choice([reply for count, reply in scored if count == fewest])


def _pick_glyph_font() -> str:
    import tkinter.font as tkfont

    try:
        available = {f.lower() for f in tkfont.families()}
    except Exception:
        return GLYPH_FONTS[-1]
    for name in GLYPH_FONTS:
        if name.lower() in available:
            return name
    return GLYPH_FONTS[-1]


def _blend(base: str, tint: str, amount: float) -> str:
    """Mix two #rrggbb colors - used for square highlights."""
    def parts(value: str) -> tuple[int, int, int]:
        value = value.lstrip("#")
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore

    a, b = parts(base), parts(tint)
    mixed = tuple(int(x + (y - x) * amount) for x, y in zip(a, b))
    return "#%02x%02x%02x" % mixed


# Re-exported for the smoke test.
__all__ = ["ChessPuzzle", "PUZZLE_PLACEMENT", "square_name"]

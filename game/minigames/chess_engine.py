"""A small, self-contained chess move generator.

Only what the level-1 puzzle needs: legal move generation, check and
checkmate detection, and a mate-in-two solver used to validate the
position and to judge the player's attempts.

Deliberately *not* implemented: castling and en passant. The puzzle
position has neither available, and leaving them out keeps this file
short enough to audit. :func:`assert_no_special_moves` guards that
assumption so a future position change cannot silently rely on them.

Board layout
------------
``board[rank][file]`` with ``rank`` 0 = rank 8 (Black's back rank) and
``file`` 0 = the a-file, i.e. index (0, 0) is a8 and (7, 7) is h1.
Pieces are two-character strings: colour (``w``/``b``) + type
(``KQRBNP``). Empty squares are ``None``.
"""
from __future__ import annotations

from typing import Iterator

WHITE, BLACK = "w", "b"
Square = tuple[int, int]
# (from_rank, from_file, to_rank, to_file, promotion_piece_or_None)
Move = tuple[int, int, int, int, str | None]

KNIGHT_STEPS = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1))
KING_STEPS = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), (1, 0), (1, 1))
BISHOP_DIRS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
ROOK_DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))

PROMOTION_PIECES = ("Q", "R", "B", "N")


def opposite(color: str) -> str:
    return BLACK if color == WHITE else WHITE


def on_board(rank: int, file: int) -> bool:
    return 0 <= rank < 8 and 0 <= file < 8


def square_name(rank: int, file: int) -> str:
    """(0, 0) -> 'a8', (7, 7) -> 'h1'."""
    return "abcdefgh"[file] + str(8 - rank)


def parse_square(name: str) -> Square:
    return 8 - int(name[1]), "abcdefgh".index(name[0])


class Board:
    """An immutable-by-convention position. :meth:`apply` returns a copy."""

    __slots__ = ("squares", "turn")

    def __init__(self, squares: list[list[str | None]], turn: str = WHITE):
        self.squares = squares
        self.turn = turn

    # ------------------------------------------------------------- setup
    @classmethod
    def empty(cls, turn: str = WHITE) -> "Board":
        return cls([[None] * 8 for _ in range(8)], turn)

    @classmethod
    def from_placement(cls, placement: dict[str, str],
                       turn: str = WHITE) -> "Board":
        """Build from ``{"e1": "wK", "a8": "bR", ...}``."""
        board = cls.empty(turn)
        for name, piece in placement.items():
            rank, file = parse_square(name)
            board.squares[rank][file] = piece
        return board

    def copy(self) -> "Board":
        return Board([row[:] for row in self.squares], self.turn)

    # ------------------------------------------------------------ access
    def piece_at(self, rank: int, file: int) -> str | None:
        return self.squares[rank][file]

    def color_at(self, rank: int, file: int) -> str | None:
        piece = self.squares[rank][file]
        return piece[0] if piece else None

    def find_king(self, color: str) -> Square | None:
        target = color + "K"
        for rank in range(8):
            for file in range(8):
                if self.squares[rank][file] == target:
                    return rank, file
        return None

    def pieces_of(self, color: str) -> Iterator[tuple[int, int, str]]:
        for rank in range(8):
            for file in range(8):
                piece = self.squares[rank][file]
                if piece and piece[0] == color:
                    yield rank, file, piece

    # ------------------------------------------------------------- moves
    def pseudo_moves(self, color: str) -> list[Move]:
        """Moves ignoring whether they leave one's own king in check."""
        moves: list[Move] = []
        for rank, file, piece in self.pieces_of(color):
            kind = piece[1]
            if kind == "P":
                moves.extend(self._pawn_moves(rank, file, color))
            elif kind == "N":
                moves.extend(self._step_moves(rank, file, color, KNIGHT_STEPS))
            elif kind == "K":
                moves.extend(self._step_moves(rank, file, color, KING_STEPS))
            elif kind == "B":
                moves.extend(self._slide_moves(rank, file, color, BISHOP_DIRS))
            elif kind == "R":
                moves.extend(self._slide_moves(rank, file, color, ROOK_DIRS))
            elif kind == "Q":
                moves.extend(self._slide_moves(rank, file, color,
                                               BISHOP_DIRS + ROOK_DIRS))
        return moves

    def _step_moves(self, rank: int, file: int, color: str,
                    steps) -> list[Move]:
        moves = []
        for d_rank, d_file in steps:
            to_rank, to_file = rank + d_rank, file + d_file
            if on_board(to_rank, to_file) and \
                    self.color_at(to_rank, to_file) != color:
                moves.append((rank, file, to_rank, to_file, None))
        return moves

    def _slide_moves(self, rank: int, file: int, color: str,
                     dirs) -> list[Move]:
        moves = []
        for d_rank, d_file in dirs:
            to_rank, to_file = rank + d_rank, file + d_file
            while on_board(to_rank, to_file):
                target = self.color_at(to_rank, to_file)
                if target == color:
                    break
                moves.append((rank, file, to_rank, to_file, None))
                if target is not None:
                    break  # captured, cannot slide further
                to_rank += d_rank
                to_file += d_file
        return moves

    def _pawn_moves(self, rank: int, file: int, color: str) -> list[Move]:
        moves: list[Move] = []
        forward = -1 if color == WHITE else 1
        start_rank = 6 if color == WHITE else 1
        last_rank = 0 if color == WHITE else 7

        one = rank + forward
        if on_board(one, file) and self.piece_at(one, file) is None:
            self._add_pawn_move(moves, rank, file, one, file, last_rank)
            two = rank + 2 * forward
            if rank == start_rank and self.piece_at(two, file) is None:
                moves.append((rank, file, two, file, None))

        for d_file in (-1, 1):
            to_file = file + d_file
            if not on_board(one, to_file):
                continue
            target = self.color_at(one, to_file)
            if target is not None and target != color:
                self._add_pawn_move(moves, rank, file, one, to_file, last_rank)
        return moves

    @staticmethod
    def _add_pawn_move(moves: list[Move], rank: int, file: int,
                       to_rank: int, to_file: int, last_rank: int) -> None:
        if to_rank == last_rank:
            for promo in PROMOTION_PIECES:
                moves.append((rank, file, to_rank, to_file, promo))
        else:
            moves.append((rank, file, to_rank, to_file, None))

    # ------------------------------------------------------------- checks
    def attacks_square(self, color: str, rank: int, file: int) -> bool:
        """Is (rank, file) attacked by any `color` piece?

        Computed directly rather than by scanning move lists, so it stays
        correct for pawns (whose captures differ from their pushes).
        """
        forward = -1 if color == WHITE else 1
        # A pawn on (rank - forward, file +- 1) attacks this square.
        for d_file in (-1, 1):
            from_rank, from_file = rank - forward, file + d_file
            if on_board(from_rank, from_file) and \
                    self.squares[from_rank][from_file] == color + "P":
                return True

        for d_rank, d_file in KNIGHT_STEPS:
            from_rank, from_file = rank + d_rank, file + d_file
            if on_board(from_rank, from_file) and \
                    self.squares[from_rank][from_file] == color + "N":
                return True

        for d_rank, d_file in KING_STEPS:
            from_rank, from_file = rank + d_rank, file + d_file
            if on_board(from_rank, from_file) and \
                    self.squares[from_rank][from_file] == color + "K":
                return True

        for dirs, kinds in ((BISHOP_DIRS, ("B", "Q")), (ROOK_DIRS, ("R", "Q"))):
            for d_rank, d_file in dirs:
                from_rank, from_file = rank + d_rank, file + d_file
                while on_board(from_rank, from_file):
                    piece = self.squares[from_rank][from_file]
                    if piece is not None:
                        if piece[0] == color and piece[1] in kinds:
                            return True
                        break
                    from_rank += d_rank
                    from_file += d_file
        return False

    def in_check(self, color: str) -> bool:
        king = self.find_king(color)
        if king is None:
            return False
        return self.attacks_square(opposite(color), *king)

    # -------------------------------------------------------------- play
    def apply(self, move: Move) -> "Board":
        from_rank, from_file, to_rank, to_file, promo = move
        new = self.copy()
        piece = new.squares[from_rank][from_file]
        new.squares[from_rank][from_file] = None
        if promo and piece:
            piece = piece[0] + promo
        new.squares[to_rank][to_file] = piece
        new.turn = opposite(self.turn)
        return new

    def legal_moves(self, color: str | None = None) -> list[Move]:
        color = color or self.turn
        legal = []
        for move in self.pseudo_moves(color):
            if not self.apply(move).in_check(color):
                legal.append(move)
        return legal

    def has_legal_move(self, color: str | None = None) -> bool:
        """Like ``legal_moves`` but stops at the first one it finds.

        Checkmate detection asks this question thousands of times when the
        mate solver runs, and building the whole list each time dominated
        the cost.
        """
        color = color or self.turn
        for move in self.pseudo_moves(color):
            if not self.apply(move).in_check(color):
                return True
        return False

    def is_checkmate(self, color: str | None = None) -> bool:
        color = color or self.turn
        return self.in_check(color) and not self.has_legal_move(color)

    def is_stalemate(self, color: str | None = None) -> bool:
        color = color or self.turn
        return not self.in_check(color) and not self.has_legal_move(color)


# ==========================================================================
# Puzzle analysis
# ==========================================================================
def mates_in_one(board: Board, color: str) -> list[Move]:
    return [m for m in board.legal_moves(color)
            if board.apply(m).is_checkmate(opposite(color))]


def has_mate_in_one(board: Board, color: str) -> bool:
    """Early-exit form of :func:`mates_in_one`."""
    defender = opposite(color)
    for move in board.legal_moves(color):
        if board.apply(move).is_checkmate(defender):
            return True
    return False


def mate_in_two_keys(board: Board, color: str = WHITE) -> list[Move]:
    """Every first move that forces mate on the second move.

    A key must *not* already be mate (that would be a one-mover), and
    every black reply must still allow a mate in one.
    """
    defender = opposite(color)
    keys: list[Move] = []
    for move in board.legal_moves(color):
        after_key = board.apply(move)
        if after_key.is_checkmate(defender):
            continue  # mate in one, not a two-mover key
        replies = after_key.legal_moves(defender)
        if not replies:
            continue  # stalemate: black is not mated
        if all(has_mate_in_one(after_key.apply(reply), color)
               for reply in replies):
            keys.append(move)
    return keys


def assert_no_special_moves(board: Board) -> None:
    """Fail loudly if a position would need castling or en passant.

    Castling needs a king and rook on their original squares; en passant
    needs a pawn that has just made a double push, which cannot happen in
    a puzzle that starts at move one.
    """
    for color, king_square, rook_squares in (
            (WHITE, "e1", ("a1", "h1")), (BLACK, "e8", ("a8", "h8"))):
        king_rank, king_file = parse_square(king_square)
        if board.squares[king_rank][king_file] != color + "K":
            continue
        for rook in rook_squares:
            rank, file = parse_square(rook)
            if board.squares[rank][file] == color + "R":
                raise AssertionError(
                    f"{color} could castle from {king_square}/{rook}; "
                    "this engine does not implement castling")


def describe(board: Board, move: Move) -> str:
    """Short algebraic-ish description, e.g. 'Qd1-h5' or 'b7-b8=Q'."""
    from_rank, from_file, to_rank, to_file, promo = move
    piece = board.piece_at(from_rank, from_file)
    kind = piece[1] if piece else "?"
    prefix = "" if kind == "P" else kind
    capture = "x" if board.piece_at(to_rank, to_file) else "-"
    text = (f"{prefix}{square_name(from_rank, from_file)}{capture}"
            f"{square_name(to_rank, to_file)}")
    return text + (f"={promo}" if promo else "")

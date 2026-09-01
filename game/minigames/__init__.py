"""Modal minigame windows."""
from .base import Minigame
from .color_game import ColorGame
from .chess_puzzle import ChessPuzzle
from .riddle_game import RiddleGame
from .quiz_sheet import QuizSheet
from .math_sprint import MathSprint
from .maze_game import MazeGame
from .snake_game import SnakeGame

__all__ = [
    "Minigame", "ColorGame", "ChessPuzzle", "RiddleGame",
    "QuizSheet", "MathSprint", "MazeGame", "SnakeGame",
]

# Blood-Moon-Ritual-Game

## 🚀 Overview

**A mind-bending puzzle adventure** with multiple challenge levels, combining logic, strategy, and fast-paced action. Navigate through mysterious rooms, solve riddles, and escape before time runs out!

Key Features:  
✔️ 3 Unique Levels (Color Puzzles, Chess Challenges, Math Mazes)  
✔️ Dual-Language Support (English/Persian)  
✔️ Two Color Themes (Blood Red / Moonlight Blue)  
✔️ Dynamic Difficulty System (15 / 10 / 5 minutes per level)  
✔️ Original Soundtrack & Voice Guidance  
✔️ Progress is saved automatically (save.json)

## 🕹️ Controls

| Input | Action |
|---|---|
| Mouse | Click the glowing spots in each room to open its challenge |
| `ESC` | Pause menu (resume / save & quit) |
| `F11` | Toggle fullscreen |
| Arrow keys / `WASD` | Move in the maze |
| Arrow keys | Steer the snake |
| Number keys + `Enter` | Answer riddles, quizzes and the math sprint |

## 🆕 What changed in v2.0 (deep refactor)

- **One window, one event loop.** The old build opened 17 separate fullscreen windows with 23 nested `mainloop()` calls; everything now runs inside a single root with proper screen navigation.
- **~47 % code duplication removed.** Every screen used to be built 4× (theme × language). Themes and languages are now data-driven (`game/strings.py`, `game/themes.py`).
- **Several progression bugs fixed**, including the chess puzzle that could never be completed, the always-true riddle checks, the blue-theme snake crash, and maze out-of-bounds crashes. One was missed and is fixed in v2.1 below.
- **Real saving.** Settings (volume/theme/language), difficulty, current level and even the paused countdown persist in `save.json` (old `saving.txt` files are migrated automatically).
- **Resolution independent.** Layout uses relative positioning; hotspot areas scale with the window instead of assuming 1920×1080.
- **Safe I/O.** Missing pictures/sounds/save files no longer crash the game; the intro video is decoded with a cheaper scaler and released on exit.
- **Animated maze hazards**, snake self-collision + reversal guards, per-question feedback in quizzes, and a proper objectives checklist per room.

## 🆕 What changed in v2.1

**Fixes**

- **The game can be finished again.** Clearing room 2 raised `KeyError: 3`
  instead of opening room 3, so room 3 and the ending were unreachable. The
  v2.0 refactor shipped with this: the smoke test never walked the
  room-to-room path, so nothing caught it. `tests/smoke_test.py` now asserts
  every room transition, and fails if that regression comes back.
- `TASK_NAMES` was used in `screens/level_base.py` without being imported —
  a latent `NameError` in the base implementation of `objective_status()`.
- `tests/smoke_test.py` caught `tk.TclError` without importing `tkinter`, so
  the test harness would itself crash while reporting a failure.
- Unused imports and dead locals removed across the package.

**The chess puzzle is now chess**

- The old "chess puzzle" contained no chess. It displayed five screenshots
  of a chess program and asked the player to click seven hard-coded
  rectangles in a fixed order — no pieces, no rules, no way to lose except
  by missing a pixel. Those five screenshots have been deleted.
- `minigames/chess_engine.py` is a small, self-contained move generator:
  legal moves for every piece, pin-aware filtering, check, checkmate and
  stalemate detection, plus a mate-in-two solver. Castling and en passant
  are deliberately not implemented and `assert_no_special_moves()` fails
  loudly if a future position would need them.
- `minigames/chess_puzzle.py` draws the board itself — themed squares,
  Unicode pieces, coordinates, selected-square and last-move highlights,
  legal-move dots, a check marker and a promotion picker.
- The puzzle is a **mate in two**: White Qe5, Kh5, Nc3, Na1, pawns d7/f7
  against Black Ka3, Nc4, pawn a5. The key is `Qe5-b5` — a quiet move,
  neither a check nor a capture, which is what makes a two-mover hard. All
  45 other first moves are refuted, Black has seven defences, and five
  distinct mates answer them (including the underpromotion `f7-f8=B`).
- Black is not a script: it plays its most stubborn defence, the reply with
  the fewest mating answers, so the second move genuinely has to be found.
  A wrong move is played on the board, refuted, and taken back.
- The solution is verified in `tests/smoke_test.py` rather than trusted:
  the suite asserts there is no mate in one, that the key is unique, that
  every Black reply is still mated, and then plays the whole line through
  the real click handler — including refusing a wrong first move.

**Interface**

- **The HUD no longer covers the room.** The objectives panel and the three
  action buttons used to be placed on top of a canvas that already spanned
  95% of the window. Rooms are now a two-column grid: artwork on the left,
  a dedicated 292px rail on the right. Nothing overlaps at any window size.
- **Interactive spots are visible.** Every hotspot is drawn as a pulsing
  sigil that names itself on hover and turns into a green tick once solved.
  Previously the only hint that a hotspot existed was the mouse cursor.
- **Room art is no longer distorted.** Backgrounds are cover-scaled to the
  window instead of stretched (the 1:1 room images were being squashed into
  a 16:9 box), and graded with a vignette so light text stays readable.
- **One design system.** `game/themes.py` now holds the full token set —
  colour roles, a spacing scale, and font stacks resolved against the fonts
  actually installed. `game/widgets.py` provides the shared button, card,
  progress bar and toast that every screen is built from.
- The countdown uses tabular figures and shifts amber below 30% and red
  below 10%; both progress bars (time and objectives) are live.
- Menu, difficulty, settings, pause, game over and the ending were rebuilt
  on those components. The blood moon on the game-over screen is generated
  procedurally, so it costs the repository nothing and follows the theme.
- Volume applies live as you drag instead of needing a separate apply
  button.
- Minigames share the chrome: one restyling pass in `minigames/base.py`
  themes every button and entry, so no minigame repeats it.
- **Exam sheet layout fixed.** `q3.png` ships at 772px wide and was drawn at
  native size, which blew out its grid column and squeezed the other two
  questions into unreadable slivers. Question images are now capped to the
  column width and all three columns are uniform.
- Persian is laid out right-to-left throughout — objectives, settings rows
  and the HUD rail all mirror.

## 📁 Project structure

```
main.py              # entry point
game/
  config.py          # paths, tuning constants
  strings.py         # every UI text (EN/FA) + riddle data
  i18n.py            # translation helper
  state.py           # game state + JSON persistence
  audio.py           # pygame mixer wrapper
  widgets.py         # shared widgets (hover buttons, backgrounds)
  app.py             # single-window app shell & navigation
  themes.py          # design tokens: colors, fonts, spacing
  quiz_data.py       # level-2 exam sheets + maze map
  screens/           # menu, settings, difficulty, levels, game over
  minigames/         # color game, riddles, quizzes,
                     # math sprint, maze, snake
    chess_engine.py  # legal moves, checkmate, mate-in-two solver
    chess_puzzle.py  # the board and the two-mover
tests/smoke_test.py  # automated sanity checks
```

## HOW TO USE

Download the Entire Repository (as ZIP): go to the repository page, click the green **Code** button and select **Download ZIP**.

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- `pip install -r requirements.txt`  (pygame, Pillow, opencv-python)

### Run

```bash
python main.py
# debug window instead of fullscreen:
python main.py --windowed
```

### Tests

```bash
python tests/smoke_test.py
```

## Copyright Notice and Usage Terms

© 2025 MaatinFallah, Never-loser All Rights Reserved.

This software is provided for **personal use and viewing only**.

**You are NOT permitted to:**

- Modify this code.
- Copy or redistribute this code in any form (including forks outside of GitHub's viewing mechanism).
- Use this code for commercial purposes.

If you wish to use or build upon any part of this project, please contact us directly at [maatinfallah@gmail.com](mailto:maatinfallah@gmail.com) and [ilia95081@gmail.com](mailto:ilia95081@gmail.com)

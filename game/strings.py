"""All user-facing strings in English and Persian.

Every entry maps a key to {"en": ..., "fa": ...}. Use `tr(key)` from
game.i18n to resolve the current language.
"""
from __future__ import annotations

STRINGS = {
    # ---------- Main menu ----------
    "menu.title": {"en": "the blood moon", "fa": "   ماه خونین   "},
    "menu.start": {"en": "Start Game", "fa": "شروع بازی"},
    "menu.settings": {"en": "Settings", "fa": "تنظیمات"},
    "menu.exit": {"en": "Exit Game", "fa": "خروج از بازی"},
    "exit.title": {"en": "Exit Confirmation", "fa": "تایید خروج"},
    "exit.question": {
        "en": "Are you sure you want to leave?",
        "fa": "آیا مطمئنی که می‌خواهی خارج شوی؟",
    },
    "common.yes": {"en": "Yes", "fa": "بله"},
    "common.no": {"en": "No", "fa": "خیر"},
    "common.back": {"en": "Back", "fa": "بازگشت"},
    "common.main_menu": {"en": "Main Menu", "fa": "منوی اصلی"},

    # ---------- Settings ----------
    "settings.title": {"en": "Settings", "fa": "تنظیمات"},
    "settings.audio": {"en": "Audio", "fa": "موسیقی"},
    "settings.volume": {"en": "Volume", "fa": "صدا"},
    "settings.change_volume": {"en": "Apply Volume", "fa": "اعمال صدا"},
    "settings.change_audio": {"en": "Change Audio", "fa": "تغییر موسیقی"},
    "settings.language": {"en": "Language", "fa": "زبان"},
    "settings.persian": {"en": "Persian", "fa": "فارسی"},
    "settings.english": {"en": "English", "fa": "انگلیسی"},
    "settings.theme": {"en": "Theme", "fa": "تم"},
    "settings.theme1": {"en": "Theme 1", "fa": "تم ۱"},
    "settings.theme2": {"en": "Theme 2", "fa": "تم ۲"},

    # ---------- Difficulty ----------
    "difficulty.title": {"en": "Choose Difficulty", "fa": "سختی را انتخاب کن"},
    "difficulty.easy": {"en": "Easy", "fa": "آسان"},
    "difficulty.medium": {"en": "Medium", "fa": "متوسط"},
    "difficulty.hard": {"en": "Hard", "fa": "سخت"},
    "difficulty.time_per_level": {
        "en": "Time per level: {minutes} min",
        "fa": "زمان هر مرحله: {minutes} دقیقه",
    },

    # ---------- Level chrome ----------
    "level.room": {"en": "room {n}", "fa": "اتاق {n}"},
    "level.position": {"en": "your position: {percent}%", "fa": "موقعیت شما: %{percent}"},
    "level.next_room": {"en": "Next Room", "fa": "اتاق بعدی"},
    "level.option": {"en": "Pause", "fa": "توقف بازی"},
    "level.story_voice": {"en": "Story Voice", "fa": "صوت داستان"},
    "level.play_music": {"en": "Play Music", "fa": "پخش موسیقی"},
    "level.items_title": {"en": "Objectives", "fa": "اهداف"},

    # Objectives panel (list of lines per language)
    "level1.items": {
        "en": ["score 10 in the color game", "answer the riddles with one word", "solve the chess puzzle"],
        "fa": ["۱۰ امتیاز در بازی رنگ‌ها به دست بیاور", "جواب معماها را در یک کلمه بده", "پازل شطرنج را حل کن"],
    },
    "level2.items": {
        "en": ["choose the right answer in every exam sheet"],
        "fa": ["در هر برگ امتحانی جواب درست را انتخاب کن"],
    },
    "level3.items": {
        "en": ["score 10 in math sprint", "score 70 in snake", "reach the red square in the maze"],
        "fa": ["۱۰ امتیاز در بازی ریاضی به دست بیاور", "۷۰ امتیاز در بازی مار به دست بیاور", "در ماز به مربع قرمز برس"],
    },

    # ---------- Pause ----------
    "pause.title": {"en": "GAME PAUSED", "fa": "بازی متوقف شد"},
    "pause.back_to_game": {"en": "Back To Game", "fa": "بازگشت به بازی"},
    "pause.save_quit": {"en": "Save And Quit", "fa": "ذخیره و خروج"},

    # ---------- Game over / win ----------
    "gameover.title": {"en": "Game Over", "fa": "بازی تمام شد"},
    "level.win_room": {"en": "You cleared this room!", "fa": "این اتاق را تمام کردی!"},
    "level.incomplete": {
        "en": "Not everything in this room is finished yet!",
        "fa": "همه کارهای این اتاق تمام نشده است!",
    },
    "end.text": {"en": "you finished this game but...", "fa": "بازی را تمام کردی اما..."},

    # ---------- HUD rail ----------
    "hud.time_left": {"en": "Time Left", "fa": "زمان باقی‌مانده"},
    "hud.progress": {"en": "Progress", "fa": "پیشرفت"},
    "hud.actions": {"en": "Actions", "fa": "کنترل‌ها"},
    "hud.count": {"en": "{done} of {total}", "fa": "{done} از {total}"},
    "hud.hint": {
        "en": "Click a glowing sigil to open its challenge",
        "fa": "روی نشانه‌های درخشان کلیک کن تا چالشش باز شود",
    },
    "hud.cleared": {"en": "Room cleared", "fa": "اتاق تمام شد"},

    # ---------- Hotspot names (shown on hover) ----------
    "spot.color": {"en": "The Color Game", "fa": "بازی رنگ‌ها"},
    "spot.riddles": {"en": "The Riddles", "fa": "معماها"},
    "spot.chess": {"en": "The Chess Puzzle", "fa": "پازل شطرنج"},
    "spot.biology": {"en": "Biology Sheet", "fa": "برگ زیست‌شناسی"},
    "spot.math": {"en": "Physics Sheet", "fa": "برگ فیزیک"},
    "spot.chemistry": {"en": "Chemistry Sheet", "fa": "برگ شیمی"},
    "spot.math_sprint": {"en": "Math Sprint", "fa": "سرعت ریاضی"},
    "spot.maze": {"en": "The Maze", "fa": "هزارتو"},
    "spot.snake": {"en": "The Snake", "fa": "بازی مار"},

    # ---------- Menu / endings ----------
    "menu.subtitle": {
        "en": "Three rooms. One night. The moon is already red.",
        "fa": "سه اتاق. یک شب. ماه همین حالا هم سرخ است.",
    },
    "menu.continue_hint": {
        "en": "Continuing from room {n}",
        "fa": "ادامه از اتاق {n}",
    },
    "difficulty.subtitle": {
        "en": "How long do you get in each room?",
        "fa": "در هر اتاق چقدر وقت داری؟",
    },
    "quiz.hand_in": {"en": "Hand In Sheet", "fa": "تحویل برگه"},
    "settings.appearance": {"en": "Appearance", "fa": "ظاهر"},
    "difficulty.minutes_caption": {
        "en": "minutes per room",
        "fa": "دقیقه برای هر اتاق",
    },
    "difficulty.selected": {"en": "Selected", "fa": "انتخاب شده"},
    "settings.current": {"en": "Now playing: {name}", "fa": "در حال پخش: {name}"},
    "pause.subtitle": {
        "en": "The countdown is frozen while this is open.",
        "fa": "تا وقتی این باز است، شمارش معکوس متوقف می‌ماند.",
    },
    "gameover.subtitle": {
        "en": "The room kept you. The ritual goes on without you.",
        "fa": "اتاق تو را نگه داشت. آیین بدون تو ادامه پیدا می‌کند.",
    },
    "gameover.returning": {
        "en": "Returning to the menu...",
        "fa": "بازگشت به منو...",
    },
    "gameover.retry": {"en": "Back to Menu", "fa": "بازگشت به منو"},
    "end.title": {"en": "The End", "fa": "پایان"},
    "end.replay": {"en": "Play Again", "fa": "بازی دوباره"},

    # ---------- Color game ----------
    "color.title": {"en": "Color Game", "fa": "بازی رنگ‌ها"},
    "color.prompt": {
        "en": "Type the COLOR of the word (not what it says):",
        "fa": "رنگِ کلمه را بنویس (نه خود کلمه را):",
    },
    "color.enter": {"en": "enter", "fa": "ثبت"},
    "color.start": {"en": "start", "fa": "شروع"},
    "color.score": {"en": "score: {n}", "fa": "امتیاز: {n}"},
    "color.won": {"en": "you won!", "fa": "بردی!"},
    "color.lost": {"en": "game over", "fa": "بازی تمام شد"},

    # ---------- Chess puzzle ----------
    "chess.title": {"en": "Chess Puzzle", "fa": "پازل شطرنج"},

    "chess.mate_in_two": {
        "en": "White to play — mate in two",
        "fa": "نوبت سفید — مات در دو حرکت",
    },
    "chess.find_key": {
        "en": "Find the one move that forces mate, whatever Black answers.",
        "fa": "حرکتی را پیدا کن که هر جوابی سیاه بدهد، مات را اجباری کند.",
    },
    "chess.now_mate": {
        "en": "Black has answered. Now deliver mate.",
        "fa": "سیاه جواب داد. حالا مات کن.",
    },
    "chess.key_found": {
        "en": "{move} — that's the key.",
        "fa": "{move} — کلید همین است.",
    },
    "chess.black_played": {"en": "Black played {move}", "fa": "سیاه {move} را بازی کرد"},
    "chess.not_forcing": {
        "en": "{move} doesn't force mate — Black escapes.",
        "fa": "{move} مات را اجباری نمی‌کند — سیاه فرار می‌کند.",
    },
    "chess.not_mate": {
        "en": "{move} isn't mate. Try another square.",
        "fa": "{move} مات نیست. خانه‌ی دیگری را امتحان کن.",
    },
    "chess.mate_delivered": {"en": "{move} — checkmate.", "fa": "{move} — کیش و مات."},
    "chess.solved": {"en": "Puzzle solved!", "fa": "پازل حل شد!"},
    "chess.reset": {"en": "Reset Position", "fa": "چیدمان اولیه"},
    "chess.not_yours": {
        "en": "That's a Black piece — you are playing White.",
        "fa": "آن مهره سیاه است — تو سفید بازی می‌کنی.",
    },

    # ---------- Riddles ----------
    "riddle.title_1": {"en": "first riddle", "fa": "معمای اول"},
    "riddle.title_2": {"en": "second riddle", "fa": "معمای دوم"},
    "riddle.title_3": {"en": "third riddle", "fa": "معمای سوم"},
    "riddle.answer": {"en": "answer:", "fa": "جواب:"},
    "riddle.submit": {"en": "submit", "fa": "ثبت"},
    "riddle.correct": {"en": "correct!", "fa": "درست است!"},
    "riddle.wrong": {"en": "not yet...", "fa": "هنوز نه..."},
    "riddle.all_done": {"en": "All riddles solved!", "fa": "همه معماها حل شد!"},
}


def build_riddles() -> list[dict]:
    """The three level-1 riddles with their accepted answers."""
    return [
        {
            "key": "riddle.title_1",
            "text": {
                "en": ("In a dark room, there is a candle, a heater,\n"
                       "and a lantern. You only have one match.\n"
                       "Which one do you light first?"),
                "fa": ("در اتاقی تاریک یک شمع، یک بخاری و یک فانوس داری.\n"
                       "فقط یک کبریت داری.\nاول کدام را روشن می‌کنی؟"),
            },
            "answers": ["match", "کبریت"],
        },
        {
            "key": "riddle.title_2",
            "text": {
                "en": ("John enters a bar and asks for a glass of water.\n"
                       "The bartender suddenly shoots the ceiling with a gun.\n"
                       "John says thank you and leaves. Why did John want water?"),
                "fa": ("جان وارد بار می‌شود و لیوان آب می‌خواهد.\n"
                       "متصدی ناگهان با اسلحه به سقف شلیک می‌کند.\n"
                       "جان تشکر می‌کند و می‌رود. چرا جان آب خواست؟"),
            },
            "answers": ["hiccup", "hiccough", "سکسکه"],
        },
        {
            "key": "riddle.title_3",
            "text": {
                "en": ("I'm light as a feather, yet the strongest person\n"
                       "can't hold me for long. What am I?"),
                "fa": ("سبک‌تر از پر هستم، اما قوی‌ترین آدم هم\n"
                       "نمی‌تواند مدت زیادی مرا نگه دارد. من چه هستم؟"),
            },
            "answers": ["breath", "نفس"],
        },
    ]

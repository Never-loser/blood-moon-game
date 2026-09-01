"""Room 2: the three exam sheets (physics, biology, chemistry)."""
from __future__ import annotations

from ..i18n import tr
from ..minigames import QuizSheet
from .level_base import LevelScreen

SUBJECT_TASKS = {
    "math": ["math1", "math2", "math3"],
    "biology": ["bio1", "bio2", "bio3"],
    "chemistry": ["chem1", "chem2", "chem3"],
}


class Level2Screen(LevelScreen):
    level_number = 2

    def subject_done(self, subject: str) -> bool:
        return all(self.state.task(2, name) for name in SUBJECT_TASKS[subject])

    def objective_status(self) -> list[bool]:
        return [all(self.subject_done(subject) for subject in SUBJECT_TASKS)]

    def hotspots(self) -> list[dict]:
        spots = [
            ("biology", (480, 436, 714, 457)),
            ("math", (825, 422, 1113, 457)),
            ("chemistry", (85, 432, 367, 457)),
        ]
        return [
            {"fraction": self.fraction(rect),
             "callback": (lambda s=subject: self.launch(s)),
             "label": tr("spot." + subject),
             "done": self.subject_done(subject)}
            for subject, rect in spots
        ]

    def launch(self, subject: str) -> None:
        if self.paused:
            return
        window = QuizSheet(self.app, subject)
        self.wait_window(window)
        # Exam sheets always record whatever was answered correctly.
        tasks = SUBJECT_TASKS[subject]
        for index, correct in enumerate(window.correct_flags):
            if correct and index < len(tasks):
                self.state.complete_task(2, tasks[index])
        self.refresh_objectives()

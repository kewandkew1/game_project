import random
import copy
import time
from resident import Resident, Doppelganger
from stats_tracker import StatsTracker


class GameManager:
    def __init__(self, starting_difficulty=1):
        self.lives = 3
        self.score = 0
        self.round_num = 0
        self.difficulty = starting_difficulty
        self.running = True
        self.current_visitor = None
        self.round_start_time = None
        self.residents = self._load_residents()
        self.stats = StatsTracker()

    def _load_residents(self):
        return [
            Resident("John Smith",   "201", "STU145", "stu001.png"),
            Resident("Maria Garcia", "305", "STU654", "stu002.png"),
            Resident("James Lee",    "412", "STU067", "stu003.png"),
            Resident("Sara Johnson", "118", "STU896", "stu004.png"),
            Resident("David Kim",    "220", "STU557", "stu005.png"),
        ]

    def next_round(self):
        self.round_num += 1
        r = random.choice(self.residents)

        if random.random() < 0.5:
            self.current_visitor = copy.deepcopy(r)
        else:
            error = self._pick_error_type()
            self.current_visitor = Doppelganger(r, error)

        self.round_start_time = time.time()
        return self.current_visitor

    def _pick_error_type(self):
        if self.difficulty == 1:
            return random.choice(["name_error", "photo_swap"])
        elif self.difficulty == 2:
            return random.choice(["room_mismatch", "wrong_id"])
        else:
            return random.choice(["room_mismatch", "name_typo"])

    def check_decision(self, player_choice):
        is_real = self.current_visitor.get_result()
        correct = (player_choice == "ALLOW") == is_real

        if correct:
            self.score += 10
        else:
            self.lives -= 1

        elapsed = time.time() - self.round_start_time if self.round_start_time else 0.0

        self.stats.record_decision(
            round_num=self.round_num,
            decision_time=elapsed,
            is_correct=int(correct),
            error_type=getattr(self.current_visitor, "error_type", "real"),
            score=self.score,
        )
        return correct

    def update_difficulty(self):
        if self.round_num % 5 == 0:
            self.difficulty = min(self.difficulty + 1, 3)

    def is_game_over(self):
        return self.lives <= 0

    def game_over(self):
        self.running = False
        self.stats.save_to_csv()
        return {
            "score":  self.score,
            "rounds": self.round_num,
        }

import csv
import os


class StatsTracker:
    def __init__(self, filename="gameplay_stats.csv"):
        self.filename = filename
        self.session_data = []

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "session_id", "round_number", "decision_time",
                    "is_correct", "error_type", "score_at_decision"
                ])

        self.session_id = self._generate_session_id()

    def _generate_session_id(self):
        try:
            with open(self.filename, "r", newline="") as f:
                reader = csv.DictReader(f)
                sessions = {row["session_id"]
                            for row in reader if row.get("session_id")}
            return f"S{len(sessions) + 1:03d}"
        except Exception:
            return "S001"

    def record_decision(self, round_num, decision_time, is_correct, error_type, score):
        row = {
            "session_id":        self.session_id,
            "round_number":      round_num,
            "decision_time":     round(decision_time, 3),
            "is_correct":        is_correct,
            "error_type":        error_type,
            "score_at_decision": score,
        }
        self.session_data.append(row)

    def save_to_csv(self):
        with open(self.filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "session_id", "round_number", "decision_time",
                "is_correct", "error_type", "score_at_decision"
            ])
            writer.writerows(self.session_data)
        print(
            f"[StatsTracker] save {len(self.session_data)} rows → {self.filename}  (session: {self.session_id})")

    def summarize(self):
        if not self.session_data:
            return {}
        times = [r["decision_time"] for r in self.session_data]
        correct = [r["is_correct"] for r in self.session_data]
        return {
            "total_decisions": len(self.session_data),
            "accuracy":        round(sum(correct) / len(correct) * 100, 1),
            "avg_time":        round(sum(times) / len(times),  2),
        }

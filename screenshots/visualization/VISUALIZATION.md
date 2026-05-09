# Data Visualization — Who is Your Neighbor?

Every player decision is recorded as a row in a CSV file during gameplay. A typical session of 10–15 rounds produces roughly 10–15 rows; across multiple sessions the data grows quickly — the current dataset logs **159 decisions over 18 sessions**. This raw data is the foundation for 4 graphs and 1 summary table, all accessible in-game after a session ends via the **"View Stats"** button on the Game Over screen (or by pressing `S`). Players can also launch `generate_graphs.py` at any time to open a standalone Tkinter window and analyse data from any previously saved `gameplay_stats.csv`.

---

## Component 1 — Decision Time Distribution (Histogram)

![Decision_Time_Distribution](Decision_Time_Distribution.png)

This histogram plots how long the player took to make each ALLOW/DENY decision, measured in seconds from the moment a visitor appears to the moment the player clicks. The x-axis represents time in seconds and the y-axis counts the number of decisions that fell within each bin. The red dashed line marks the mean decision time of **5.23 seconds**. The distribution is right-skewed, meaning most decisions are made quickly (under 5 seconds), while a long tail extends towards slower deliberations reaching up to ~15 seconds. This pattern suggests players generally develop a fast intuition for obvious cases, but slow down considerably when facing subtle doppelganger errors such as `name_typo` or `wrong_id`.

---

## Component 2 — Error Type Distribution (Pie Chart)

![Error_Type_Distribution](Error_Type_Distribution.png)

This pie chart shows the proportion of each visitor type encountered across all 18 recorded sessions. The largest slice is **real** residents (49.1%), confirming that the game does not over-generate doppelgangers and keeps the player uncertain. Among doppelganger error types, `name_typo` (13.8%) and `wrong_id` (13.2%) appear most frequently, which aligns with the difficulty-3 weighting in `_pick_error_type()` that favours subtle errors. `room_mismatch` (7.5%) and `name_error` (6.3%) are less common because they are assigned primarily in lower difficulty brackets, while `photo_swap` (10.1%) remains a mid-frequency challenge across all levels. This distribution reflects the adaptive difficulty scaling that increases every 5 rounds.

---

## Component 3 — Accuracy & Decision Time per Round (Dual-Axis Line Chart)

![accuracy_decision_time](accuracy_decision_time.png)

This dual-axis line chart overlays two metrics across round numbers: **accuracy percentage** (green, left axis) and **average decision time in seconds** (red dashed, right axis). Each data point represents the mean value of all decisions made in that round number, pooled across all sessions. The green line shows that accuracy is generally high in early rounds but becomes more volatile in later rounds (9–15), corresponding to the point where difficulty has scaled up to level 2 and 3. The red line reveals that decision times are not strictly correlated with accuracy — players sometimes take longer but still make correct calls, particularly in rounds where `name_typo` errors dominate. The horizontal grey dotted line at 50% accuracy marks the random-chance baseline.

---

## Component 4 — Score Progression per Session (Area Line Chart)

![Score_per_session](Score_per_session.png)

This chart traces the cumulative score for each of the 18 recorded sessions (S001–S018) over the sequence of decisions made within that session. Each coloured line represents one play session; the shaded fill beneath each line emphasises the area under the score curve, making it easy to compare overall performance volume between sessions. Steeper lines indicate sustained correct decisions (+10 per correct), while flat or stagnant segments indicate a string of incorrect decisions where no points were earned. The highest score reached is **120 points**. Sessions vary significantly in length (some ending after only 5–6 decisions due to losing all 3 lives quickly), while others extend to 15+ decisions, showing the range of player skill and game variability between runs.

---

## Component 5 — Summary Statistics (Table)

![Summary_table](Summary_table.png)

This table consolidates the key aggregate statistics from the entire `gameplay_stats.csv` dataset into a single readable reference. It reports total decisions recorded (159), number of sessions (18), overall accuracy (72.3%), average decision time (5.23 s), the fastest and slowest recorded decisions (0.03 s and 14.92 s respectively), and the maximum score ever reached (120). The lower section breaks down decisions by `error_type`, showing exactly how many times each type appeared. This table is rendered both inside the in-game Pygame statistics screen under the "Summary" tab and in the standalone Tkinter viewer's "Summary Stats" popup window. It provides a quick sanity check on data volume and confirms that the 100-record minimum requirement has been met.

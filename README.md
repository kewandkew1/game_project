# Who is Your Neighbor?

## Project Description
- Project by: Chayapol Kaewsakul
- Game Genre: Casual, Puzzle / Decision-Making

"Who is Your Neighbor?" is a single-screen doppelganger detection game inspired by *That's Not My Neighbor*. The player acts as a university dormitory security guard stationed at the entrance. Each round, a visitor approaches and presents an ID card. The player must compare the visitor's face and card details against the resident list to decide whether to **ALLOW** or **DENY** entry. Correct decisions earn points; wrong decisions cost a life. The game ends when all 3 lives are lost.

Key features include multiple doppelganger error types (wrong room, name typo, photo swap, and more), adaptive difficulty that scales every 5 rounds, and a live statistics tracker that records every decision to a CSV file for post-game analysis with graphs.

---

## Installation

To clone this project:
```sh
git clone https://github.com/kewandkew1/game_project
cd who-is-your-neighbor
```

To create and run a Python environment for this project:

**Windows:**
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Mac:**
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Requirements:** Python 3.10+, pygame 2.6.1, pandas, matplotlib

---

## Running Guide

After activating the Python environment, run the game with:

**Windows:**
```bat
python main.py
```

**Mac:**
```sh
python3 main.py
```

---

## Tutorial / Usage

1. **Title Screen** — Press `ENTER` or `SPACE` to start, or `Q` to quit.
2. **Difficulty Screen** — Use `←` / `→` arrow keys to select Easy, Normal, or Hard, then press `ENTER` to confirm. You can also click a button directly.
3. **Gameplay** — Each round, a visitor appears on screen.
   - Click the **ID card area** (bottom-center of the screen) to open the visitor's ID card. The card is draggable — click and drag to move it anywhere on screen.
   - Click the **DATA folder** (right side of the desk) to toggle the resident list panel.
   - Compare the visitor's face on-screen with the photo on the ID card, and cross-check the card details against the resident list.
   - Press **`A`** or click **ALLOW** to let the visitor in.
   - Press **`D`** or click **DENY** to turn the visitor away.
4. **Scoring** — Correct decision: +10 points. Wrong decision: −1 life. You start with 3 lives.
5. **Game Over** — When all lives are lost, you see your final score and can choose to Restart, View Stats, or Quit.
6. **Statistics Viewer** — Click **View Stats** or press `S` on the Game Over screen to open the built-in stats viewer. Use `←` / `→` or the sidebar buttons to switch between charts. Press `S` to save all graphs to the `graphs/` folder, and `ESC` or **Back** to return.

---

## Game Features

- **Doppelganger Detection** — Visitors are either real residents or doppelgangers disguised with one of five error types:
  - `room_mismatch` — room number is off by ±1
  - `name_error` — name is replaced with a similar-sounding fake
  - `name_typo` — a single character in the name is changed
  - `wrong_id` — last digit of the student ID is altered
  - `photo_swap` — ID card photo belongs to a different resident
- **Draggable ID Card** — The ID card popup can be dragged around the screen and resets to center each time it is reopened.
- **Resident List Panel** — A toggleable panel showing all 5 residents with grayscale portraits, room numbers, and student IDs.
- **Difficulty Scaling** — Three selectable difficulty levels (Easy / Normal / Hard). Difficulty also increases automatically every 5 rounds within a session.
- **Statistics Tracking** — Every ALLOW/DENY decision is recorded in real time to `gameplay_stats.csv`, including decision time, correctness, error type, round number, and score.
- **Built-in Statistics Viewer** — Accessible from the Game Over screen directly inside the game (no separate window needed). Displays four charts rendered inside pygame:
  - Decision time histogram
  - Error type pie chart
  - Accuracy & average decision time per round (dual-axis line chart)
  - Score progression per session (area chart)
  - Summary statistics panel
  - "Save All" export to the `graphs/` folder

---

## Known Bugs

- None currently identified.

---

## Unfinished Works

- All core planned features have been implemented.
- Potential future additions: sound effects, animated sprite transitions, leaderboard across sessions, and expanded resident roster beyond 5 characters.

---

## External Sources

Acknowledge to:
1. *That's Not My Neighbor* by Nacho Sama — core gameplay inspiration [game concept]
2. Pygame documentation, https://www.pygame.org/docs/ [library reference]
3. Piskel, https://www.piskelapp.com/ — used to draw all character face sprites [art tool]
4. Matplotlib documentation, https://matplotlib.org/stable/index.html [library reference]

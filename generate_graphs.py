import os
import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CSV_FILE   = "gameplay_stats.csv"
OUTPUT_DIR = "graphs"


# ── data ──────────────────────────────────────────────────────────────────────

def load_data():
    if not os.path.exists(CSV_FILE):
        return None, f"'{CSV_FILE}' not found. Play the game first to generate data."
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        return None, "CSV file is empty."
    return df, None


# ── graph builders (return Figure) ────────────────────────────────────────────

def graph_decision_time_histogram(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["decision_time"], bins=20, color="#4A90D9", edgecolor="white", linewidth=0.8)
    ax.axvline(df["decision_time"].mean(), color="#E74C3C", linestyle="--", linewidth=1.8,
               label=f"Mean: {df['decision_time'].mean():.2f}s")
    ax.set_title("Decision Time Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Number of Decisions")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig


def graph_error_type_pie(df):
    counts  = df["error_type"].value_counts()
    colors  = ["#E74C3C", "#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C"]
    explode = [0.04] * len(counts)

    fig, ax = plt.subplots(figsize=(7, 7))
    _, _, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=colors[:len(counts)],
        explode=explode,
        startangle=140,
        textprops={"fontsize": 11},
    )
    for at in autotexts:
        at.set_fontweight("bold")
    ax.set_title("Error Type Distribution", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig


def graph_accuracy_and_time_per_round(df):
    grouped = df.groupby("round_number").agg(
        accuracy=("is_correct",    "mean"),
        avg_time=("decision_time", "mean"),
    ).reset_index()
    grouped["accuracy"] *= 100

    fig, ax1 = plt.subplots(figsize=(10, 5))
    color_acc  = "#2ECC71"
    color_time = "#E74C3C"

    ax1.plot(grouped["round_number"], grouped["accuracy"],
             color=color_acc, marker="o", linewidth=2, label="Accuracy (%)")
    ax1.set_xlabel("Round Number")
    ax1.set_ylabel("Accuracy (%)", color=color_acc)
    ax1.tick_params(axis="y", labelcolor=color_acc)
    ax1.set_ylim(0, 110)
    ax1.axhline(50, color="gray", linestyle=":", linewidth=0.8)

    ax2 = ax1.twinx()
    ax2.plot(grouped["round_number"], grouped["avg_time"],
             color=color_time, marker="s", linewidth=2, linestyle="--", label="Avg Time (s)")
    ax2.set_ylabel("Avg Decision Time (s)", color=color_time)
    ax2.tick_params(axis="y", labelcolor=color_time)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    ax1.set_title("Accuracy & Decision Time per Round", fontsize=14, fontweight="bold")
    ax1.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    return fig


def graph_score_progression(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    sessions = df["session_id"].unique()
    palette  = plt.cm.tab10.colors
    for i, sid in enumerate(sessions):
        sdf   = df[df["session_id"] == sid].reset_index(drop=True)
        x     = range(1, len(sdf) + 1)
        color = palette[i % len(palette)]
        ax.plot(x, sdf["score_at_decision"], color=color, linewidth=2, label=sid)
        ax.fill_between(x, sdf["score_at_decision"], alpha=0.15, color=color)
    ax.set_title("Score Progression per Session", fontsize=14, fontweight="bold")
    ax.set_xlabel("Decision Number (within session)")
    ax.set_ylabel("Cumulative Score")
    ax.legend(title="Session", fontsize=9, title_fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def build_summary_text(df):
    lines = [
        f"Total decisions : {len(df)}",
        f"Sessions        : {df['session_id'].nunique()}",
        f"Overall accuracy: {df['is_correct'].mean()*100:.1f}%",
        f"Avg decision time: {df['decision_time'].mean():.2f}s",
        "",
        "Error type breakdown:",
    ]
    for et, cnt in df["error_type"].value_counts().items():
        lines.append(f"  {et:<22}{cnt}")
    return "\n".join(lines)


# ── save helpers (kept for CLI / export button) ────────────────────────────────

def save_all(df):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fns = {
        "graph1_decision_time_histogram.png": graph_decision_time_histogram,
        "graph2_error_type_pie.png":          graph_error_type_pie,
        "graph3_accuracy_and_time_line.png":  graph_accuracy_and_time_per_round,
        "graph4_score_progression_area.png":  graph_score_progression,
    }
    for fname, fn in fns.items():
        fig = fn(df)
        fig.savefig(os.path.join(OUTPUT_DIR, fname), dpi=150)
        plt.close(fig)
    return OUTPUT_DIR


# ── tkinter app ───────────────────────────────────────────────────────────────

GRAPHS = [
    ("Decision Time Histogram",       graph_decision_time_histogram),
    ("Error Type Pie Chart",          graph_error_type_pie),
    ("Accuracy & Time per Round",     graph_accuracy_and_time_per_round),
    ("Score Progression per Session", graph_score_progression),
]

BG        = "#1E1E2E"
SIDEBAR   = "#2A2A3E"
ACCENT    = "#4A90D9"
BTN_FG    = "#FFFFFF"
BTN_ACTIVE = "#5BA3F5"
TEXT_FG   = "#CDD6F4"


class GraphViewer(tk.Tk):
    def __init__(self, df):
        super().__init__()
        self.df           = df
        self.current_fig  = None
        self.canvas_widget = None

        self.title("Gameplay Statistics Viewer")
        self.configure(bg=BG)
        self.geometry("1050x680")
        self.minsize(800, 550)

        self._build_ui()
        self._show_graph(0)

    # ── layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # sidebar
        sidebar = tk.Frame(self, bg=SIDEBAR, width=210)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="GRAPHS", bg=SIDEBAR, fg=ACCENT,
                 font=("Segoe UI", 11, "bold"), pady=16).pack(fill=tk.X)

        ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X, padx=12)

        self.btn_vars = []
        self.buttons  = []
        for idx, (label, _) in enumerate(GRAPHS):
            btn = tk.Button(
                sidebar, text=label, wraplength=180,
                bg=SIDEBAR, fg=TEXT_FG,
                activebackground=ACCENT, activeforeground=BTN_FG,
                relief=tk.FLAT, padx=10, pady=10,
                font=("Segoe UI", 9), cursor="hand2",
                command=lambda i=idx: self._show_graph(i),
            )
            btn.pack(fill=tk.X, padx=6, pady=3)
            self.buttons.append(btn)

        ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X, padx=12, pady=8)

        tk.Button(
            sidebar, text="Summary Stats",
            bg="#3A3A5E", fg=TEXT_FG,
            activebackground=ACCENT, activeforeground=BTN_FG,
            relief=tk.FLAT, padx=10, pady=10,
            font=("Segoe UI", 9), cursor="hand2",
            command=self._show_summary,
        ).pack(fill=tk.X, padx=6, pady=3)

        tk.Button(
            sidebar, text="Save All Graphs",
            bg="#3A3A5E", fg=TEXT_FG,
            activebackground="#2ECC71", activeforeground=BTN_FG,
            relief=tk.FLAT, padx=10, pady=10,
            font=("Segoe UI", 9), cursor="hand2",
            command=self._save_all,
        ).pack(fill=tk.X, padx=6, pady=3)

        # main canvas area
        self.canvas_frame = tk.Frame(self, bg=BG)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(
            self.canvas_frame, text="", bg=BG, fg=TEXT_FG,
            font=("Segoe UI", 13, "bold"), pady=8,
        )
        self.title_label.pack(fill=tk.X)

        self.plot_frame = tk.Frame(self.canvas_frame, bg=BG)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    # ── actions ───────────────────────────────────────────────────────────────

    def _show_graph(self, idx):
        label, builder = GRAPHS[idx]
        self.title_label.config(text=label)

        # highlight selected button
        for i, btn in enumerate(self.buttons):
            btn.config(bg=ACCENT if i == idx else SIDEBAR,
                       fg=BTN_FG if i == idx else TEXT_FG)

        fig = builder(self.df)
        self._embed_figure(fig)

    def _embed_figure(self, fig):
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
        if self.current_fig:
            plt.close(self.current_fig)

        self.current_fig   = fig
        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _show_summary(self):
        win = tk.Toplevel(self)
        win.title("Summary Statistics")
        win.configure(bg=BG)
        win.geometry("400x300")

        text = tk.Text(win, bg=SIDEBAR, fg=TEXT_FG,
                       font=("Consolas", 10), relief=tk.FLAT,
                       padx=12, pady=12)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(tk.END, build_summary_text(self.df))
        text.config(state=tk.DISABLED)

    def _save_all(self):
        out = save_all(self.df)
        messagebox.showinfo("Saved", f"All 4 graphs saved to '{out}/' folder.")

    def destroy(self):
        if self.current_fig:
            plt.close(self.current_fig)
        super().destroy()


# ── entry point ───────────────────────────────────────────────────────────────

def open_stats_viewer():
    df, err = load_data()
    if err:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", err)
        root.destroy()
    else:
        app = GraphViewer(df)
        app.mainloop()


if __name__ == "__main__":
    open_stats_viewer()

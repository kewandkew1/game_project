import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

CSV_FILE   = "gameplay_stats.csv"
OUTPUT_DIR = "graphs"


def load_data():
    if not os.path.exists(CSV_FILE):
        print(f"[ERROR] '{CSV_FILE}' not found. Play the game first to generate data.")
        return None
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print("[ERROR] CSV file is empty.")
        return None
    print(f"[INFO] Loaded {len(df)} rows from {CSV_FILE}")
    return df


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
    path = os.path.join(OUTPUT_DIR, "graph1_decision_time_histogram.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {path}")


def graph_error_type_pie(df):
    counts = df["error_type"].value_counts()

    colors = ["#E74C3C", "#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C"]
    explode = [0.04] * len(counts)

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
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

    path = os.path.join(OUTPUT_DIR, "graph2_error_type_pie.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {path}")


def graph_accuracy_and_time_per_round(df):
    grouped = df.groupby("round_number").agg(
        accuracy     = ("is_correct",    "mean"),
        avg_time     = ("decision_time", "mean"),
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

    path = os.path.join(OUTPUT_DIR, "graph3_accuracy_and_time_line.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {path}")


def graph_score_progression(df):
    fig, ax = plt.subplots(figsize=(10, 5))

    # One line per session
    sessions = df["session_id"].unique()
    palette  = plt.cm.tab10.colors
    for i, sid in enumerate(sessions):
        sdf  = df[df["session_id"] == sid].reset_index(drop=True)
        x    = range(1, len(sdf) + 1)
        color = palette[i % len(palette)]
        ax.plot(x, sdf["score_at_decision"], color=color, linewidth=2, label=sid)
        ax.fill_between(x, sdf["score_at_decision"], alpha=0.15, color=color)

    ax.set_title("Score Progression per Session", fontsize=14, fontweight="bold")
    ax.set_xlabel("Decision Number (within session)")
    ax.set_ylabel("Cumulative Score")
    ax.legend(title="Session", fontsize=9, title_fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()

    path = os.path.join(OUTPUT_DIR, "graph4_score_progression_area.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {path}")


def print_summary(df):
    print("\n── Summary Statistics ──────────────────────────────")
    print(f"  Total decisions : {len(df)}")
    print(f"  Sessions        : {df['session_id'].nunique()}")
    print(f"  Overall accuracy: {df['is_correct'].mean()*100:.1f}%")
    print(f"  Avg decision time: {df['decision_time'].mean():.2f}s")
    print(f"  Error type breakdown:")
    for et, cnt in df["error_type"].value_counts().items():
        print(f"    {et:20s} {cnt}")
    print("────────────────────────────────────────────────────\n")


if __name__ == "__main__":
    df = load_data()
    if df is None:
        raise SystemExit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print_summary(df)
    graph_decision_time_histogram(df)
    graph_error_type_pie(df)
    graph_accuracy_and_time_per_round(df)
    graph_score_progression(df)

    print(f"\n✅  All 4 graphs saved to '{OUTPUT_DIR}/' folder.")

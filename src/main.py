"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

from recommender import load_songs, recommend_songs

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

REASON_WRAP_WIDTH = 50


def print_recommendations(recommendations) -> None:
    """Render (song, score, explanation) tuples as a terminal table."""
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = textwrap.fill(explanation, width=REASON_WRAP_WIDTH)
        rows.append([rank, song["title"], f"{score:.2f}", reasons])

    headers = ["#", "Title", "Score", "Reasons"]

    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="grid", disable_numparse=True))
        return

    # Fallback: simple ASCII table if tabulate isn't installed.
    # Width is the longest individual line, since cells may wrap to multiple lines.
    col_widths = [
        max(
            len(line)
            for row in ([headers] + rows)
            for line in str(row[i]).split("\n")
        )
        for i in range(len(headers))
    ]

    def format_row(row):
        cells = []
        for i, value in enumerate(row):
            lines = str(value).split("\n")
            cells.append(lines)
        max_lines = max(len(c) for c in cells)
        out_lines = []
        for line_idx in range(max_lines):
            parts = []
            for i, lines in enumerate(cells):
                text = lines[line_idx] if line_idx < len(lines) else ""
                parts.append(text.ljust(col_widths[i]))
            out_lines.append("| " + " | ".join(parts) + " |")
        return "\n".join(out_lines)

    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    print(separator)
    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))
        print(separator)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    print_recommendations(recommendations)


if __name__ == "__main__":
    main()

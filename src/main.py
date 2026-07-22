"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs

# Project root is the parent of this file's directory (src/).
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SONGS_CSV = PROJECT_ROOT / "data" / "songs.csv"


def main() -> None:
    songs = load_songs(str(SONGS_CSV))
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(recommendations, user_prefs)


def print_recommendations(recommendations, user_prefs) -> None:
    """Print recommendations in a clean, readable terminal layout."""
    prefs = (
        f"genre={user_prefs.get('genre')}, "
        f"mood={user_prefs.get('mood')}, "
        f"energy={user_prefs.get('energy')}"
    )

    width = 60
    print()
    print("=" * width)
    print("  TOP RECOMMENDATIONS")
    print(f"  for: {prefs}")
    print("=" * width)

    if not recommendations:
        print("\n  No songs matched your preferences.\n")
        return

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        title = f"{rank}. {song['title']}"
        by = f"by {song.get('artist', 'Unknown artist')}"
        print(f"\n{title}  ({by})")
        print(f"   Score: {score:.2f}")
        if reasons:
            print("   Reasons:")
            for reason in reasons:
                print(f"     - {reason}")
        else:
            print("   Reasons: no strong matches with your preferences")

    print("\n" + "=" * width + "\n")


if __name__ == "__main__":
    main()

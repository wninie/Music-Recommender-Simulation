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


# Adversarial / edge-case profiles designed to probe the scoring logic.
# Each is named so its intent is obvious when the output prints below.
ADVERSARIAL_PROFILES = {
    # Wants high energy but a *low*-energy mood. Genre(+3)+mood(+2) swamp
    # energy(max +2), so a calm classical track can beat an EDM banger.
    "conflicting_energy_vs_mood": {"genre": "classical", "mood": "melancholy", "energy": 0.9},
    # Genre/mood that exist in no song: both silently score 0, leaving an
    # energy-only ranking with no warning that the input was unrecognized.
    "nonexistent_genre": {"genre": "polka", "mood": "sad", "energy": 0.5},
    # Boundary energy: rewards the lowest-energy songs in the catalog.
    "boundary_energy_min": {"genre": "none", "mood": "none", "energy": 0.0},
    # Boundary energy: rewards the highest-energy songs in the catalog.
    "boundary_energy_max": {"genre": "none", "mood": "none", "energy": 1.0},
    # Correct taste but wrong capitalization: exact-match scoring drops all
    # 5 categorical points despite the "obvious" intent.
    "case_mismatch": {"genre": "Pop", "mood": "Happy", "energy": 0.82},
    # Wants high energy AND acoustic — but every acoustic song is low energy,
    # so the acoustic bonus fights the energy target.
    "acoustic_vs_energy": {"genre": "none", "mood": "none", "energy": 0.95, "likes_acoustic": True},
}


def main() -> None:
    songs = load_songs(str(SONGS_CSV))
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(recommendations, user_prefs)

    # Run each adversarial profile through the same pipeline to see how the
    # scoring logic behaves under tricky / conflicting inputs.
    for name, prefs in ADVERSARIAL_PROFILES.items():
        print(f"\n>>> Adversarial profile: {name}")
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(recommendations, prefs)


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

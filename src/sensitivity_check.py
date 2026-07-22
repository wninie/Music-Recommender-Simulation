"""
Sensitivity check for the point-weighting scheme.

Runs several different user profiles against the full song catalog so you can
see how the weights behave before locking them in. Run from the project root:

    python src/sensitivity_check.py
"""

from recommender import load_songs, recommend_songs

# A few contrasting profiles to stress-test the weights.
PROFILES = {
    "Pop + happy + high energy": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Lofi + chill + low energy":  {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Metal + aggressive + max energy": {"genre": "metal", "mood": "aggressive", "energy": 0.95},
    "Chill acoustic lover":       {"genre": "jazz", "mood": "relaxed", "energy": 0.4, "likes_acoustic": True},
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, prefs in PROFILES.items():
        print(f"\n=== {label} ===")
        print(f"    prefs: {prefs}")
        recs = recommend_songs(prefs, songs, k=5)
        for song, score, _ in recs:
            print(f"    {score:5.2f}  {song['title']:<22} "
                  f"[{song['genre']}/{song['mood']}, energy {song['energy']:.2f}]")


if __name__ == "__main__":
    main()

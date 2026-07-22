import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# --- Point-weighting configuration ---------------------------------------
# Genre is the strongest taste signal, so it wins ties over mood.
# Energy is scored on a sliding scale (closer to target = more points).
GENRE_POINTS = 3.0
MOOD_POINTS = 2.0
ENERGY_MAX_POINTS = 2.0
ACOUSTIC_POINTS = 1.0
ACOUSTIC_THRESHOLD = 0.6  # a song counts as "acoustic" above this

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _energy_points(song_energy: float, target_energy: float) -> float:
    """Sliding score: 2.0 for a perfect match, fading to 0.0 as the gap grows."""
    gap = abs(song_energy - target_energy)
    return max(0.0, ENERGY_MAX_POINTS * (1 - gap))


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Returns a song's total match score and the reasons behind it for a given user."""
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += GENRE_POINTS
            reasons.append(f"matches your favorite genre ({song.genre})")

        if song.mood == user.favorite_mood:
            score += MOOD_POINTS
            reasons.append(f"matches your mood ({song.mood})")

        energy_pts = _energy_points(song.energy, user.target_energy)
        score += energy_pts
        gap = abs(song.energy - user.target_energy)
        if gap <= 0.1:
            reasons.append("energy level is a great fit")
        elif gap <= 0.3:
            reasons.append("energy level is close to what you want")

        if user.likes_acoustic and song.acousticness >= ACOUSTIC_THRESHOLD:
            score += ACOUSTIC_POINTS
            reasons.append("has the acoustic sound you like")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs ranked by how well they match the user's taste."""
        # Sort by score descending; ties keep original order (stable sort).
        ranked = sorted(
            self.songs,
            key=lambda song: self._score(user, song)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable sentence explaining why a song was recommended to the user."""
        score, reasons = self._score(user, song)
        if not reasons:
            return f"'{song.title}' scored {score:.1f} but didn't match your preferences closely."
        return f"'{song.title}' (score {score:.1f}) because it " + ", and ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file, converting numeric columns to numbers.
    Required by src/main.py
    """
    numeric_floats = {"energy", "valence", "danceability", "acousticness"}
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            for field in numeric_floats:
                row[field] = float(row[field])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    user_prefs keys: "genre", "mood", "energy" (optionally "likes_acoustic").
    Returns (score, reasons).
    """
    score = 0.0
    reasons: List[str] = []

    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_POINTS
        reasons.append(f"matches your favorite genre ({song['genre']}) (+{GENRE_POINTS:.1f})")

    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_POINTS
        reasons.append(f"matches your mood ({song['mood']}) (+{MOOD_POINTS:.1f})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_pts = _energy_points(song["energy"], target_energy)
        score += energy_pts
        gap = abs(song["energy"] - target_energy)
        if gap <= 0.1:
            reasons.append(f"energy level is a great fit (+{energy_pts:.1f})")
        elif gap <= 0.3:
            reasons.append(f"energy level is close to what you want (+{energy_pts:.1f})")

    if user_prefs.get("likes_acoustic") and song["acousticness"] >= ACOUSTIC_THRESHOLD:
        score += ACOUSTIC_POINTS
        reasons.append(f"has the acoustic sound you like (+{ACOUSTIC_POINTS:.1f})")

    return score, reasons


def _explanation(reasons: List[str]) -> str:
    """Turns a list of reasons into a human-readable sentence."""
    if not reasons:
        return "it didn't match your preferences closely."
    return "it " + ", and ".join(reasons) + "."


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Scores every song, ranks by score, and returns the top k.
    Each item: (song_dict, score, reasons) where reasons is the list of
    scoring explanations produced by score_song.
    Required by src/main.py
    """
    # Judge every song once with score_song, packaging each as (song, score, reasons).
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))
    # sorted() returns a NEW list ranked high-to-low; the input `songs` is untouched.
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]

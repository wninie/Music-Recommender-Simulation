from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    score_song,
    GENRE_POINTS,
    MOOD_POINTS,
    ENERGY_MAX_POINTS,
    ACOUSTIC_POINTS,
)


POP_SONG = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.8,
    "acousticness": 0.2,
}
ACOUSTIC_SONG = {
    "genre": "folk",
    "mood": "wistful",
    "energy": 0.4,
    "acousticness": 0.9,
}

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- score_song (dict-based scoring) -------------------------------------

def test_score_song_returns_score_and_reasons():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, reasons = score_song(prefs, POP_SONG)
    assert isinstance(score, float)
    assert isinstance(reasons, list)


def test_genre_match_awards_genre_points():
    prefs = {"genre": "pop"}
    score, reasons = score_song(prefs, POP_SONG)
    assert score == GENRE_POINTS
    assert any("genre" in r for r in reasons)


def test_mood_match_awards_mood_points():
    prefs = {"mood": "happy"}
    score, reasons = score_song(prefs, POP_SONG)
    assert score == MOOD_POINTS
    assert any("mood" in r for r in reasons)


def test_perfect_energy_match_awards_full_points():
    prefs = {"energy": 0.8}  # exactly equal to the song's energy
    score, reasons = score_song(prefs, POP_SONG)
    assert score == ENERGY_MAX_POINTS
    assert any("energy" in r for r in reasons)


def test_energy_slides_down_as_gap_grows():
    close = score_song({"energy": 0.7}, POP_SONG)[0]   # gap 0.1
    far = score_song({"energy": 0.3}, POP_SONG)[0]     # gap 0.5
    assert ENERGY_MAX_POINTS > close > far


def test_acoustic_bonus_only_when_user_likes_acoustic():
    with_bonus = score_song({"likes_acoustic": True}, ACOUSTIC_SONG)[0]
    without_bonus = score_song({"likes_acoustic": False}, ACOUSTIC_SONG)[0]
    assert with_bonus - without_bonus == ACOUSTIC_POINTS


def test_reasons_include_point_annotations():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    _, reasons = score_song(prefs, POP_SONG)
    # Rubric: each reason should show the points it contributed, e.g. "(+3.0)"
    assert all("(+" in r for r in reasons)


def test_no_match_scores_zero_with_no_reasons():
    prefs = {"genre": "metal", "mood": "aggressive"}  # no energy pref, no matches
    score, reasons = score_song(prefs, POP_SONG)
    assert score == 0.0
    assert reasons == []

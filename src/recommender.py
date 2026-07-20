import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

DEFAULT_MODE = "balanced"

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
    mode: str = DEFAULT_MODE

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs recommended for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a given song was recommended to the user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)
    return songs

# Mood -> implied (valence_target, danceability_target).
# Lets score_song reason about valence/danceability even though UserProfile /
# user_prefs only carry a favorite_mood, not those raw feature values.
MOOD_TARGETS: Dict[str, Tuple[float, float]] = {
    "happy": (0.80, 0.80),
    "chill": (0.55, 0.55),
    "intense": (0.60, 0.85),
    "relaxed": (0.65, 0.55),
    "moody": (0.50, 0.70),
    "focused": (0.55, 0.55),
    "energetic": (0.65, 0.85),
    "peaceful": (0.55, 0.20),
    "nostalgic": (0.55, 0.40),
    "angry": (0.30, 0.50),
    "romantic": (0.70, 0.65),
    "euphoric": (0.80, 0.90),
    "warm": (0.70, 0.55),
    "laid-back": (0.75, 0.70),
    "melancholic": (0.30, 0.40),
    "rebellious": (0.55, 0.60),
}
DEFAULT_MOOD_TARGET: Tuple[float, float] = (0.60, 0.60)

# Algorithm Recipe v2 weight presets, one per scoring mode (each must sum to 1.0)
WEIGHT_PRESETS = {
    "balanced": {
        "genre": 0.25,
        "mood": 0.20,
        "energy": 0.20,
        "valence": 0.15,
        "danceability": 0.10,
        "acousticness": 0.10,
    },
    "genre_first": {
        "genre": 0.45,
        "mood": 0.15,
        "energy": 0.15,
        "valence": 0.10,
        "danceability": 0.075,
        "acousticness": 0.075,
    },
    "mood_first": {
        "genre": 0.15,
        "mood": 0.40,
        "energy": 0.10,
        "valence": 0.20,
        "danceability": 0.10,
        "acousticness": 0.05,
    },
    "energy_focused": {
        "genre": 0.10,
        "mood": 0.10,
        "energy": 0.40,
        "valence": 0.15,
        "danceability": 0.20,
        "acousticness": 0.05,
    },
}

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm Recipe v2 (weighted feature distance):
      - genre / mood: exact match (1.0 or 0.0)
      - energy: 1 - abs(song.energy - target_energy)
      - valence / danceability: 1 - abs(song.value - implied target from favorite mood)
      - acousticness: acousticness if likes_acoustic else (1 - acousticness)
      score = 100 * sum(weight_i * match_i)

    user_prefs["mode"] selects which entry of WEIGHT_PRESETS to weight the
    features by (e.g. "genre_first", "mood_first", "energy_focused");
    defaults to DEFAULT_MODE ("balanced") when absent.
    """
    mode = user_prefs.get("mode", DEFAULT_MODE)
    if mode not in WEIGHT_PRESETS:
        valid = ", ".join(sorted(WEIGHT_PRESETS))
        raise ValueError(f"Unknown scoring mode '{mode}'. Valid modes: {valid}")
    weights = WEIGHT_PRESETS[mode]

    favorite_genre = user_prefs.get("genre")
    favorite_mood = user_prefs.get("mood")
    target_energy = user_prefs.get("energy", 0.5)
    likes_acoustic = user_prefs.get("likes_acoustic", False)

    valence_target, danceability_target = MOOD_TARGETS.get(favorite_mood, DEFAULT_MOOD_TARGET)

    genre_match = 1.0 if song.get("genre") == favorite_genre else 0.0
    mood_match = 1.0 if song.get("mood") == favorite_mood else 0.0
    energy_match = 1.0 - abs(song.get("energy", 0.0) - target_energy)
    valence_match = 1.0 - abs(song.get("valence", 0.0) - valence_target)
    danceability_match = 1.0 - abs(song.get("danceability", 0.0) - danceability_target)

    acousticness = song.get("acousticness", 0.0)
    acousticness_match = acousticness if likes_acoustic else (1.0 - acousticness)

    matches = {
        "genre": genre_match,
        "mood": mood_match,
        "energy": energy_match,
        "valence": valence_match,
        "danceability": danceability_match,
        "acousticness": acousticness_match,
    }

    contributions = {feature: weights[feature] * match for feature, match in matches.items()}
    score = round(sum(contributions.values()) * 100, 2)

    reason_templates = {
        "genre": lambda: f"genre '{song.get('genre')}' matches your favorite genre",
        "mood": lambda: f"mood '{song.get('mood')}' matches your favorite mood",
        "energy": lambda: f"energy {song.get('energy'):.2f} is close to your target {target_energy:.2f}",
        "valence": lambda: f"valence {song.get('valence'):.2f} fits the '{favorite_mood}' mood profile",
        "danceability": lambda: f"danceability {song.get('danceability'):.2f} fits the '{favorite_mood}' mood profile",
        "acousticness": lambda: (
            f"acousticness {acousticness:.2f} matches your preference for acoustic tracks"
            if likes_acoustic
            else f"acousticness {acousticness:.2f} matches your preference for non-acoustic tracks"
        ),
    }

    top_features = sorted(contributions, key=contributions.get, reverse=True)[:3]
    reasons = [reason_templates[feature]() for feature in top_features if matches[feature] > 0]

    return score, reasons

MAX_SONGS_PER_ARTIST = 2

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Scores every song, ranks highest-to-lowest, then applies a diversity cap
    so no artist appears more than MAX_SONGS_PER_ARTIST times in the top k.

    user_prefs["mode"] (see score_song) selects the scoring weight preset.
    """
    scored = sorted(
        ((song, *score_song(user_prefs, song)) for song in songs),
        key=lambda scored_song: scored_song[1],
        reverse=True,
    )

    artist_counts: Dict[str, int] = {}
    recommendations: List[Tuple[Dict, float, str]] = []

    for song, score, reasons in scored:
        if len(recommendations) == k:
            break

        artist = song.get("artist")
        if artist_counts.get(artist, 0) >= MAX_SONGS_PER_ARTIST:
            continue

        explanation = ", ".join(reasons) if reasons else "No strong matches on your preferences"
        recommendations.append((song, score, explanation))
        artist_counts[artist] = artist_counts.get(artist, 0) + 1

    return recommendations

# 🎵 Music Recommender Simulation

## Project Summary

A small content-based music recommender. It scores a catalog of songs against a listener's stated taste (genre, mood, energy, acoustic preference), ranks them, and returns the top matches with a plain-language explanation for each pick. An artist cap (max 2 songs per artist) keeps results varied.

---

## How The System Works

Real-world recommenders combine collaborative filtering (recommends based on similar users) and content-based filtering (recommends based on item features compared to what a user already likes). This project uses **content-based filtering**, since it works entirely from song features.

### Song features (10 attributes)

- `id`, `title`, `artist` — metadata only, not used in scoring
- `genre`, `mood` — categorical
- `energy`, `valence`, `danceability`, `acousticness` — floats, 0 to 1
- `tempo_bpm` — loaded but not used in scoring

### UserProfile fields

- `favorite_genre` / `favorite_mood` — matched exactly; mood also looks up a target `valence`/`danceability` pair
- `target_energy` — desired energy level (0 to 1)
- `likes_acoustic` — flips whether high or low acousticness scores better
- `mode` — weight preset: `balanced`, `genre_first`, `mood_first`, or `energy_focused`

### Scoring

For each song, five match values are computed and combined using weights from the selected mode (weights sum to 1.0), then scaled to 0–100:

- `genre_match` / `mood_match` — 1.0 exact match, else 0.0
- `energy_match` — `1 - abs(song.energy - target_energy)`
- `valence_match` / `danceability_match` — `1 - abs(song.value - mood-implied target)`
- `acousticness_match` — acousticness if user likes acoustic, else `1 - acousticness`

Songs are sorted by score, then the top `k` are selected, skipping any song that would push an artist past 2 appearances. Each recommendation includes an explanation built from its top 3 contributing features.

**Known bias:** genre and mood require exact matches, so close-but-different tastes (e.g. "chill" vs. "relaxed") are never surfaced — this narrows discovery rather than encouraging it.

---

## Getting Started

### Setup

1. Create a virtual environment (optional):
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

Add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loaded songs: 20

Top recommendations:

+-----+----------------+---------+----------------------------------------------------+
| #   | Title          | Score   | Reasons                                            |
+=====+================+=========+====================================================+
| 1   | Sunrise City   | 97.10   | genre 'pop' matches your favorite genre, mood      |
|     |                |         | 'happy' matches your favorite mood, energy 0.82 is |
|     |                |         | close to your target 0.80                          |
+-----+----------------+---------+----------------------------------------------------+
| 2   | Gym Hero       | 75.65   | genre 'pop' matches your favorite genre, energy    |
|     |                |         | 0.93 is close to your target 0.80, valence 0.77    |
|     |                |         | fits the 'happy' mood profile                      |
+-----+----------------+---------+----------------------------------------------------+
| 3   | Rooftop Lights | 70.35   | mood 'happy' matches your favorite mood, energy    |
|     |                |         | 0.76 is close to your target 0.80, valence 0.81    |
|     |                |         | fits the 'happy' mood profile                      |
+-----+----------------+---------+----------------------------------------------------+
| 4   | Neon Horizon   | 51.90   | energy 0.88 is close to your target 0.80, valence  |
|     |                |         | 0.80 fits the 'happy' mood profile, acousticness   |
|     |                |         | 0.05 matches your preference for non-acoustic      |
|     |                |         | tracks                                             |
+-----+----------------+---------+----------------------------------------------------+
| 5   | Concrete Kings | 50.15   | energy 0.85 is close to your target 0.80, valence  |
|     |                |         | 0.65 fits the 'happy' mood profile, danceability   |
|     |                |         | 0.88 fits the 'happy' mood profile                 |
+-----+----------------+---------+----------------------------------------------------+
```

---

## Experiments You Tried

`src/main.py` defines `USER_PROFILES` — three normal taste profiles and five adversarial/edge-case profiles — all run through `recommend_songs` against the sample catalog.

### Normal profiles

- **High-Energy Pop** (`genre_first`, target energy 0.9): correctly ranked both `pop` songs first, since the boosted genre weight (0.45) dominated.

```
=== High-Energy Pop ===
user_prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'likes_acoustic': False, 'mode': 'genre_first'}
+-----+----------------+---------+----------------------------------------------------+
| #   | Title          | Score   | Reasons                                            |
+=====+================+=========+====================================================+
| 1   | Sunrise City   | 96.97   | genre 'pop' matches your favorite genre, mood      |
|     |                |         | 'happy' matches your favorite mood, energy 0.82 is |
|     |                |         | close to your target 0.90                          |
+-----+----------------+---------+----------------------------------------------------+
| 2   | Gym Hero       | 83.28   | genre 'pop' matches your favorite genre, energy    |
|     |                |         | 0.93 is close to your target 0.90, valence 0.77    |
|     |                |         | fits the 'happy' mood profile                      |
+-----+----------------+---------+----------------------------------------------------+
| 3   | Rooftop Lights | 50.02   | mood 'happy' matches your favorite mood, energy    |
|     |                |         | 0.76 is close to your target 0.90, valence 0.81    |
|     |                |         | fits the 'happy' mood profile                      |
+-----+----------------+---------+----------------------------------------------------+
| 4   | Neon Horizon   | 38.57   | energy 0.88 is close to your target 0.90, valence  |
|     |                |         | 0.80 fits the 'happy' mood profile, acousticness   |
|     |                |         | 0.05 matches your preference for non-acoustic      |
|     |                |         | tracks                                             |
+-----+----------------+---------+----------------------------------------------------+
| 5   | Concrete Kings | 36.55   | energy 0.85 is close to your target 0.90, valence  |
|     |                |         | 0.65 fits the 'happy' mood profile, danceability   |
|     |                |         | 0.88 fits the 'happy' mood profile                 |
+-----+----------------+---------+----------------------------------------------------+
```

- **Chill Lofi** (`mood_first`, likes acoustic, target energy 0.35): both `lofi` tracks ranked highest; mood/valence weighting pulled a thematically-similar ambient track above unrelated genres.

```
=== Chill Lofi ===
user_prefs = {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True, 'mode': 'mood_first'}
+-----+--------------------+---------+----------------------------------------------------+
| #   | Title              | Score   | Reasons                                            |
+=====+====================+=========+====================================================+
| 1   | Library Rain       | 98.00   | mood 'chill' matches your favorite mood, valence   |
|     |                    |         | 0.60 fits the 'chill' mood profile, genre 'lofi'   |
|     |                    |         | matches your favorite genre                        |
+-----+--------------------+---------+----------------------------------------------------+
| 2   | Midnight Coding    | 96.95   | mood 'chill' matches your favorite mood, valence   |
|     |                    |         | 0.56 fits the 'chill' mood profile, genre 'lofi'   |
|     |                    |         | matches your favorite genre                        |
+-----+--------------------+---------+----------------------------------------------------+
| 3   | Spacewalk Thoughts | 80.50   | mood 'chill' matches your favorite mood, valence   |
|     |                    |         | 0.65 fits the 'chill' mood profile, energy 0.28 is |
|     |                    |         | close to your target 0.35                          |
+-----+--------------------+---------+----------------------------------------------------+
| 4   | Focus Flow         | 57.10   | valence 0.59 fits the 'chill' mood profile, genre  |
|     |                    |         | 'lofi' matches your favorite genre, danceability   |
|     |                    |         | 0.60 fits the 'chill' mood profile                 |
+-----+--------------------+---------+----------------------------------------------------+
| 5   | Old Porch Stories  | 41.30   | valence 0.58 fits the 'chill' mood profile, energy |
|     |                    |         | 0.33 is close to your target 0.35, danceability    |
|     |                    |         | 0.35 fits the 'chill' mood profile                 |
+-----+--------------------+---------+----------------------------------------------------+
```

- **Deep Intense Rock** (`energy_focused`, target energy 0.9): the one true `rock`+`intense` song ranked first, but de-emphasized genre/mood let several unrelated high-energy tracks crowd the top 5.

```
=== Deep Intense Rock ===
user_prefs = {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False, 'mode': 'energy_focused'}
+-----+----------------+---------+----------------------------------------------------+
| #   | Title          | Score   | Reasons                                            |
+=====+================+=========+====================================================+
| 1   | Storm Runner   | 93.50   | energy 0.91 is close to your target 0.90,          |
|     |                |         | danceability 0.66 fits the 'intense' mood profile, |
|     |                |         | valence 0.48 fits the 'intense' mood profile       |
+-----+----------------+---------+----------------------------------------------------+
| 2   | Gym Hero       | 85.40   | energy 0.93 is close to your target 0.90,          |
|     |                |         | danceability 0.88 fits the 'intense' mood profile, |
|     |                |         | valence 0.77 fits the 'intense' mood profile       |
+-----+----------------+---------+----------------------------------------------------+
| 3   | Concrete Kings | 76.25   | energy 0.85 is close to your target 0.90,          |
|     |                |         | danceability 0.88 fits the 'intense' mood profile, |
|     |                |         | valence 0.65 fits the 'intense' mood profile       |
+-----+----------------+---------+----------------------------------------------------+
| 4   | Neon Horizon   | 74.95   | energy 0.88 is close to your target 0.90,          |
|     |                |         | danceability 0.90 fits the 'intense' mood profile, |
|     |                |         | valence 0.80 fits the 'intense' mood profile       |
+-----+----------------+---------+----------------------------------------------------+
| 5   | Broken Curfew  | 72.00   | energy 0.95 is close to your target 0.90,          |
|     |                |         | danceability 0.60 fits the 'intense' mood profile, |
|     |                |         | valence 0.55 fits the 'intense' mood profile       |
+-----+----------------+---------+----------------------------------------------------+
```

### Adversarial / edge-case profiles

- **Empty Preferences** (`{}`): didn't crash — every field fell back to a default, producing a generic "middle of the road" playlist with no warning that no real preferences were given. The explanation text even leaked `'None' mood profile` to the user.

```
=== Empty Preferences ===
user_prefs = {}
+-----+-----------------+---------+---------------------------------------------------+
| #   | Title           | Score   | Reasons                                           |
+=====+=================+=========+===================================================+
| 1   | Velvet Whisper  | 48.70   | energy 0.55 is close to your target 0.50, valence |
|     |                 |         | 0.70 fits the 'None' mood profile, danceability   |
|     |                 |         | 0.68 fits the 'None' mood profile                 |
+-----+-----------------+---------+---------------------------------------------------+
| 2   | Island Sway     | 46.75   | energy 0.45 is close to your target 0.50, valence |
|     |                 |         | 0.75 fits the 'None' mood profile, danceability   |
|     |                 |         | 0.70 fits the 'None' mood profile                 |
+-----+-----------------+---------+---------------------------------------------------+
| 3   | Backroad Sunset | 46.70   | energy 0.50 is close to your target 0.50, valence |
|     |                 |         | 0.72 fits the 'None' mood profile, danceability   |
|     |                 |         | 0.55 fits the 'None' mood profile                 |
+-----+-----------------+---------+---------------------------------------------------+
| 4   | Midnight Coding | 45.50   | energy 0.42 is close to your target 0.50, valence |
|     |                 |         | 0.56 fits the 'None' mood profile, danceability   |
|     |                 |         | 0.62 fits the 'None' mood profile                 |
+-----+-----------------+---------+---------------------------------------------------+
| 5   | Focus Flow      | 45.05   | energy 0.40 is close to your target 0.50, valence |
|     |                 |         | 0.59 fits the 'None' mood profile, danceability   |
|     |                 |         | 0.60 fits the 'None' mood profile                 |
+-----+-----------------+---------+---------------------------------------------------+
```

- **Nonexistent Genre/Mood** (made-up strings): behaved almost identically to the empty-preferences case, since unrecognized moods silently fall back to a default and unmatched genres just score 0 — but the explanation text confidently echoed the made-up mood back, implying false understanding.

```
=== Nonexistent Genre and Mood ===
user_prefs = {'genre': 'vaporwave-death-polka', 'mood': 'ecstatic-dread', 'energy': 0.5, 'likes_acoustic': False}
+-----+-----------------+---------+---------------------------------------------------+
| #   | Title           | Score   | Reasons                                           |
+=====+=================+=========+===================================================+
| 1   | Velvet Whisper  | 48.70   | energy 0.55 is close to your target 0.50, valence |
|     |                 |         | 0.70 fits the 'ecstatic-dread' mood profile,      |
|     |                 |         | danceability 0.68 fits the 'ecstatic-dread' mood  |
|     |                 |         | profile                                           |
+-----+-----------------+---------+---------------------------------------------------+
| 2   | Island Sway     | 46.75   | energy 0.45 is close to your target 0.50, valence |
|     |                 |         | 0.75 fits the 'ecstatic-dread' mood profile,      |
|     |                 |         | danceability 0.70 fits the 'ecstatic-dread' mood  |
|     |                 |         | profile                                           |
+-----+-----------------+---------+---------------------------------------------------+
| 3   | Backroad Sunset | 46.70   | energy 0.50 is close to your target 0.50, valence |
|     |                 |         | 0.72 fits the 'ecstatic-dread' mood profile,      |
|     |                 |         | danceability 0.55 fits the 'ecstatic-dread' mood  |
|     |                 |         | profile                                           |
+-----+-----------------+---------+---------------------------------------------------+
| 4   | Midnight Coding | 45.50   | energy 0.42 is close to your target 0.50, valence |
|     |                 |         | 0.56 fits the 'ecstatic-dread' mood profile,      |
|     |                 |         | danceability 0.62 fits the 'ecstatic-dread' mood  |
|     |                 |         | profile                                           |
+-----+-----------------+---------+---------------------------------------------------+
| 5   | Focus Flow      | 45.05   | energy 0.40 is close to your target 0.50, valence |
|     |                 |         | 0.59 fits the 'ecstatic-dread' mood profile,      |
|     |                 |         | danceability 0.60 fits the 'ecstatic-dread' mood  |
|     |                 |         | profile                                           |
+-----+-----------------+---------+---------------------------------------------------+
```

- **Out-of-Range Energy** (`energy = 5.0`): broke the scoring math instead of erroring — scores went negative for every song, since nothing clamps `target_energy` to `[0, 1]`.

```
=== Out-of-Range Energy ===
user_prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 5.0, 'likes_acoustic': False}
+-----+----------------+---------+----------------------------------------------------+
| #   | Title          | Score   | Reasons                                            |
+=====+================+=========+====================================================+
| 1   | Sunrise City   | 13.90   | genre 'pop' matches your favorite genre, mood      |
|     |                |         | 'happy' matches your favorite mood, valence 0.84   |
|     |                |         | fits the 'happy' mood profile                      |
+-----+----------------+---------+----------------------------------------------------+
| 2   | Gym Hero       | -3.15   | genre 'pop' matches your favorite genre, valence   |
|     |                |         | 0.77 fits the 'happy' mood profile, acousticness   |
|     |                |         | 0.05 matches your preference for non-acoustic      |
|     |                |         | tracks                                             |
+-----+----------------+---------+----------------------------------------------------+
| 3   | Rooftop Lights | -13.65  | mood 'happy' matches your favorite mood, valence   |
|     |                |         | 0.81 fits the 'happy' mood profile, danceability   |
|     |                |         | 0.82 fits the 'happy' mood profile                 |
+-----+----------------+---------+----------------------------------------------------+
| 4   | Neon Horizon   | -28.90  | valence 0.80 fits the 'happy' mood profile,        |
|     |                |         | acousticness 0.05 matches your preference for non- |
|     |                |         | acoustic tracks, danceability 0.90 fits the        |
|     |                |         | 'happy' mood profile                               |
+-----+----------------+---------+----------------------------------------------------+
| 5   | Concrete Kings | -31.85  | valence 0.65 fits the 'happy' mood profile,        |
|     |                |         | danceability 0.88 fits the 'happy' mood profile,   |
|     |                |         | acousticness 0.08 matches your preference for non- |
|     |                |         | acoustic tracks                                    |
+-----+----------------+---------+----------------------------------------------------+
```

- **Negative Energy** (`energy = -2.0`): same unvalidated-range problem; combined with a conflicting acoustic preference, all scores landed near 0 with no visual signal that the input was invalid.

```
=== Negative Energy ===
user_prefs = {'genre': 'metal', 'mood': 'angry', 'energy': -2.0, 'likes_acoustic': True}
+-----+-----------------------+---------+--------------------------------------------------+
| #   | Title                 | Score   | Reasons                                          |
+=====+=======================+=========+==================================================+
| 1   | Iron Revolt           | 29.65   | genre 'metal' matches your favorite genre, mood  |
|     |                       |         | 'angry' matches your favorite mood, valence 0.25 |
|     |                       |         | fits the 'angry' mood profile                    |
+-----+-----------------------+---------+--------------------------------------------------+
| 2   | Moonlit Sonata Dreams | 3.25    | valence 0.55 fits the 'angry' mood profile,      |
|     |                       |         | acousticness 0.95 matches your preference for    |
|     |                       |         | acoustic tracks, danceability 0.15 fits the      |
|     |                       |         | 'angry' mood profile                             |
+-----+-----------------------+---------+--------------------------------------------------+
| 3   | Spacewalk Thoughts    | 2.45    | valence 0.65 fits the 'angry' mood profile,      |
|     |                       |         | acousticness 0.92 matches your preference for    |
|     |                       |         | acoustic tracks, danceability 0.41 fits the      |
|     |                       |         | 'angry' mood profile                             |
+-----+-----------------------+---------+--------------------------------------------------+
| 4   | Rainy Window Blues    | 1.90    | valence 0.30 fits the 'angry' mood profile,      |
|     |                       |         | danceability 0.40 fits the 'angry' mood profile, |
|     |                       |         | acousticness 0.55 matches your preference for    |
|     |                       |         | acoustic tracks                                  |
+-----+-----------------------+---------+--------------------------------------------------+
| 5   | Library Rain          | 1.30    | valence 0.60 fits the 'angry' mood profile,      |
|     |                       |         | danceability 0.58 fits the 'angry' mood profile, |
|     |                       |         | acousticness 0.86 matches your preference for    |
|     |                       |         | acoustic tracks                                  |
+-----+-----------------------+---------+--------------------------------------------------+
```

- **Contradictory Acoustic Metal** (metal/angry + likes_acoustic): a valid but hard-to-satisfy profile — the top song still won comfortably on genre/mood/energy alone, with the acoustic term simply outweighed rather than breaking anything.

```
=== Contradictory Acoustic Metal ===
user_prefs = {'genre': 'metal', 'mood': 'angry', 'energy': 0.95, 'likes_acoustic': True}
+-----+--------------------+---------+----------------------------------------------------+
| #   | Title              | Score   | Reasons                                            |
+=====+====================+=========+====================================================+
| 1   | Iron Revolt        | 88.65   | genre 'metal' matches your favorite genre, mood    |
|     |                    |         | 'angry' matches your favorite mood, energy 0.97 is |
|     |                    |         | close to your target 0.95                          |
+-----+--------------------+---------+----------------------------------------------------+
| 2   | Storm Runner       | 40.90   | energy 0.91 is close to your target 0.95, valence  |
|     |                    |         | 0.48 fits the 'angry' mood profile, danceability   |
|     |                    |         | 0.66 fits the 'angry' mood profile                 |
+-----+--------------------+---------+----------------------------------------------------+
| 3   | Broken Curfew      | 40.75   | energy 0.95 is close to your target 0.95, valence  |
|     |                    |         | 0.55 fits the 'angry' mood profile, danceability   |
|     |                    |         | 0.60 fits the 'angry' mood profile                 |
+-----+--------------------+---------+----------------------------------------------------+
| 4   | Rainy Window Blues | 38.10   | valence 0.30 fits the 'angry' mood profile,        |
|     |                    |         | danceability 0.40 fits the 'angry' mood profile,   |
|     |                    |         | energy 0.38 is close to your target 0.95            |
+-----+--------------------+---------+----------------------------------------------------+
| 5   | Night Drive Loop   | 38.05   | energy 0.75 is close to your target 0.95, valence  |
|     |                    |         | 0.49 fits the 'angry' mood profile, danceability   |
|     |                    |         | 0.66 fits the 'angry' mood profile                 |
+-----+--------------------+---------+----------------------------------------------------+
```

- **Invalid Scoring Mode** (`mode = "vibes_based"`): the only input actually rejected — raises a clear `ValueError` listing valid modes.

```
=== Invalid Scoring Mode ===
user_prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'mode': 'vibes_based'}
ERROR: ValueError: Unknown scoring mode 'vibes_based'. Valid modes: balanced, energy_focused, genre_first, mood_first
```

**Takeaway:** the system only validates `mode`. Every other bad input (unknown genre/mood, out-of-range energy) is silently absorbed and still rendered in the same polished, confident table as a legitimate result — this is the main risk area.

---

## Limitations and Risks

- Only validates `mode`; all other invalid input (unknown genre/mood, out-of-range energy) fails silently rather than erroring or warning
- Exact-match genre/mood scoring narrows discovery and can reinforce a user's existing habits
- Small, static catalog — no real-world scale or freshness
- No understanding of lyrics, audio content, or language — purely metadata-driven
- No handling for conflicting preferences beyond weighted averaging

See [model_card.md](model_card.md) for a deeper look at bias and fairness.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Building this system showed me that a recommender turns data into predictions by comparing labeled item features against stated user preferences, then combining the differences into a single weighted score — no real "understanding" required, just feature engineering and tunable weights. The clearest bias I found came from the data, not the algorithm: because pop was the only genre with two songs in the catalog, a pop fan got a fully on-genre list while every other fan's results were padded with mismatched songs. This showed me that unfairness can stem entirely from an unbalanced dataset, and that the system's silent fallbacks on bad input (blank preferences, made-up genres, out-of-range values) make that bias harder to notice rather than surfacing it.

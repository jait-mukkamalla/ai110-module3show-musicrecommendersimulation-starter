# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version scores a small catalog of songs against a listener's stated taste (genre, mood, energy, and acoustic preference), ranks them, and returns the top matches with a plain-language explanation for each pick. It also caps how many songs from one artist can appear, so the results stay a bit more varied.

---

## How The System Works

Real world recommendation systems are a combination of collaborative filtering, content-based filtering, and as of more recently machine learning and AI.
Collaborative filtering generates recommendations for a user by using the viewing habits of similar user profiles, hence a 'collaboration' between users.
Content-based filtering uses the features of the content getting evaluated and compares that information to content that you've previously liked.
Collaborative filtering is used to 'taste-match' for an individual using other user's profiles while content-based filtering is generally used on newer content.
Because of the feature-based implementation of this project, this recommender whill be built using content-based filtering.

**What features does each `Song` use in your system?**

Each `Song` carries 10 attributes:

- `id`, `title`, `artist` — identifying metadata (used for display and artist deduplication, not scoring)
- `genre` — categorical (e.g. "pop", "rock")
- `mood` — categorical (e.g. "happy", "chill")
- `energy` — float, 0 to 1
- `tempo_bpm` — float (loaded but not currently used in scoring)
- `valence` — float, 0 to 1 (musical positivity/happiness)
- `danceability` — float, 0 to 1
- `acousticness` — float, 0 to 1

**What information does your `UserProfile` store?**

- `favorite_genre` — preferred genre, matched exactly against a song's genre
- `favorite_mood` — preferred mood, matched exactly, and also used to look up an implied target `valence`/`danceability` pair via a mood-to-target table
- `target_energy` — the energy level (0 to 1) the user wants songs to be close to
- `likes_acoustic` — boolean; flips whether high or low `acousticness` scores well
- `mode` — selects a weight preset (`balanced`, `genre_first`, `mood_first`, or `energy_focused`) that changes how much each feature counts toward the score

**How does your `Recommender` compute a score for each song?**

For each song, five match values are computed against the user's profile:

- `genre_match` / `mood_match` — 1.0 for an exact match, 0.0 otherwise
- `energy_match` — `1 - abs(song.energy - target_energy)`
- `valence_match` / `danceability_match` — `1 - abs(song.value - implied_target)`, where the implied target comes from the user's favorite mood
- `acousticness_match` — the song's acousticness if the user likes acoustic tracks, otherwise `1 - acousticness`

Each match is multiplied by its weight from the selected mode's preset (weights sum to 1.0), summed, and scaled to a 0–100 score. The top three contributing features are turned into a plain-language explanation string.

**How do you choose which songs to recommend?**

All songs are scored and sorted highest to lowest. The system then walks down that ranked list and takes the top `k`, but skips any song that would put an artist over a cap of 2 songs in the results — this keeps one artist from dominating the recommendation list even if they have several high-scoring tracks.

### Algorithm Recipe (Final)

- Look up the weight preset for `user_prefs["mode"]` (defaults to `"balanced"` if not set)
- For each song, compute five match values:
  - `genre_match` = 1.0 if song genre equals favorite genre, else 0.0
  - `mood_match` = 1.0 if song mood equals favorite mood, else 0.0
  - `energy_match` = 1 - |song energy - target energy|
  - `valence_match` = 1 - |song valence - mood-implied valence target|
  - `danceability_match` = 1 - |song danceability - mood-implied danceability target|
  - `acousticness_match` = song acousticness if user likes acoustic, else 1 - acousticness
- Multiply each match by its weight from the preset and sum them
- Scale the sum by 100 to get a final score (0–100)
- Sort all songs by score, highest to lowest
- Walk down the sorted list and keep the top `k`, skipping any song that would push an artist past 2 appearances
- Build an explanation string from the top 3 highest-contributing features for each recommended song

**Potential biases:** since genre and mood are scored as strict exact-matches, the system will likely under-recommend songs that are close but not identical to a user's stated preferences (e.g. a "chill" fan may never see "relaxed" songs), reinforcing narrow listening habits rather than encouraging discovery.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I defined a set of `USER_PROFILES` in [src/main.py](src/main.py) — three distinct "normal" taste profiles plus five adversarial/edge-case profiles — and ran every one of them through `recommend_songs` against the sample catalog.

### Normal taste profiles

**High-Energy Pop** (`genre_first` mode, target energy 0.9) correctly surfaced the two `pop` songs first, with `Sunrise City` and `Gym Hero` far outscoring everything else thanks to the genre weight being boosted to 0.45.

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

**Chill Lofi** (`mood_first` mode, likes acoustic, target energy 0.35) put both `lofi` tracks at the top, with the mood/valence weighting from `mood_first` pulling `Spacewalk Thoughts` (ambient, but very "chill"-coded) above unrelated genres.

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

**Deep Intense Rock** (`energy_focused` mode, target energy 0.9) ranked `Storm Runner` (the catalog's only `rock` + `intense` song) first, but because `energy_focused` de-emphasizes genre/mood, several unrelated high-energy tracks (`Gym Hero`, `Concrete Kings`, `Neon Horizon`) crowded into the top 5 purely on energy/danceability similarity.

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

**Empty Preferences** (`{}` — no genre, mood, energy, or mode at all) didn't crash. Every field fell back to its default (`target_energy=0.5`, `genre=None`, `mood=None` → the `DEFAULT_MOOD_TARGET` of `(0.60, 0.60)`), so the system quietly recommended a generic "middle of the road" playlist instead of refusing or flagging that it had nothing to go on. The explanation text even prints the literal string `'None' mood profile`, leaking an internal implementation detail to the user.

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

**Nonexistent Genre and Mood** (made-up strings `"vaporwave-death-polka"` / `"ecstatic-dread"`) produced an almost *identical* ranking to the empty-preferences run, because any mood not in `MOOD_TARGETS` silently falls back to `DEFAULT_MOOD_TARGET` and any genre not in the catalog can never match. The system never tells the user their genre/mood was unrecognized — it just quietly ignores it and still confidently prints an explanation string that repeats their made-up mood back to them (`fits the 'ecstatic-dread' mood profile`), which reads as a false signal that the system "understood" the input.

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

**Out-of-Range Energy** (`energy = 5.0`, way outside the documented 0–1 range) broke the scoring math instead of erroring: `energy_match = 1 - abs(song.energy - 5.0)` goes deeply negative for every song, which drags overall scores negative too (`-3.15`, `-13.65`, `-28.90`, `-31.85`). There is no input validation clamping `target_energy` to `[0, 1]`, so a single out-of-range field can flip the sign of the whole score and make "matches" look like penalties.

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

**Negative Energy** (`energy = -2.0`) triggers the same unvalidated-range problem from the other direction, and combines badly with `likes_acoustic=True`: the top result `Iron Revolt` only scores 29.65 (it's metal/angry, a "correct" match, but its very low acousticness tanks the acoustic-preference term), while everything else scores close to zero. A confidently-rendered table with all scores near 0–30 gives no visual signal to the user that the input itself was nonsensical.

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

**Contradictory Acoustic Metal** (`genre="metal"`, `mood="angry"`, `likes_acoustic=True` — metal/angry songs in this catalog are almost by definition low-acousticness) is a "can the profile even be satisfied" test rather than a bad-input test. `Iron Revolt` still wins comfortably (88.65) on genre + mood + energy alone, showing the system tolerates an internally-inconsistent-but-valid profile gracefully — the acoustic preference just quietly loses out to the other four weighted terms instead of causing an error or a nonsensical top pick.

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

**Invalid Scoring Mode** (`mode = "vibes_based"`, a mode that doesn't exist in `WEIGHT_PRESETS`) is the one input that the system actually rejects — `score_song` raises a `ValueError` naming the invalid mode and listing the valid options. This is the correct behavior for a fully-invalid categorical input, and it stands in contrast to the silent, no-error fallback behavior for unrecognized genres/moods and out-of-range numeric fields above — the system validates the `mode` string but nothing else.

```
=== Invalid Scoring Mode ===
user_prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'mode': 'vibes_based'}
ERROR: ValueError: Unknown scoring mode 'vibes_based'. Valid modes: balanced, energy_focused, genre_first, mood_first
```

**Takeaway:** the recommender only validates one input (`mode`) and silently no-ops or produces nonsensical/negative scores for everything else (unknown genre, unknown mood, out-of-range or negative energy). None of these adversarial profiles crashed the recommendation pipeline itself (aside from the intentionally-invalid mode), but several produced misleading confidence — a fully-generic fallback playlist and negative scores presented in the exact same polished table as a legitimate result, with no warning that the input was out of bounds or unrecognized.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this




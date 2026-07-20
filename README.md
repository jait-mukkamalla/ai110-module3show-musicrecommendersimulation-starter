# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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




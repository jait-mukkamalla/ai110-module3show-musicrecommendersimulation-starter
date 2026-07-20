# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

Strategy pattern, applied to the song-scoring weights in `score_song`.

**How did AI help you brainstorm or implement it?**

I wanted `score_song` to support multiple scoring modes (genre-first, mood-first,
energy-focused) instead of one fixed set of weights, and asked Claude to plan the
approach before writing code. It suggested replacing the single `WEIGHTS` dict with
a `WEIGHT_PRESETS` dict keyed by mode name (each preset still summing to 1.0), and
initially had `score_song`/`recommend_songs` take a `mode` parameter to select the
preset. When I said the user profile should decide the mode rather than passing it
around separately, it moved `mode` onto `user_prefs`/`UserProfile` itself (defaulting
to `"balanced"`), so `score_song` just reads `user_prefs.get("mode", DEFAULT_MODE)`
and looks up the matching weight preset — no extra parameter to thread through.

**How does the pattern appear in your final code?**

`WEIGHT_PRESETS` in `src/recommender.py` holds the interchangeable "strategies"
(`balanced`, `genre_first`, `mood_first`, `energy_focused`), and `score_song`
(`src/recommender.py`) selects one at runtime based on `user_prefs["mode"]` /
`UserProfile.mode` to weight the same match calculations differently.

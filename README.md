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

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

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




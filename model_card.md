# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**BeatsBlender 1.0**  

---

## 2. Intended Use  

This recommender suggests songs from a small sample catalog based on a listener's stated taste — favorite genre, favorite mood, desired energy level, and whether they like acoustic songs. It assumes the listener can describe their taste in these simple terms, and that their taste stays fairly consistent (it does not learn or adapt over time). This is a classroom exploration project, not a system built for real users or a real music catalog.

---

## 3. How the Model Works  

Every song has a genre, a mood, an energy level, and a few other traits like how "danceable" or "acoustic" it sounds. The listener tells the system their favorite genre, favorite mood, how much energy they want, and whether they like acoustic songs. The system compares each song to those preferences: exact matches on genre and mood score well, and energy/mood-related traits score well when they're numerically close to what the listener asked for. All of that gets combined into a single score out of 100, and the songs are sorted from best match to worst. I added a setting that lets the listener say which of those traits matters most to them (for example, someone can say genre matters most, or energy matters most), and I added a rule that stops any one artist from taking over the list, so the results feel a bit more varied.

---

## 4. Data  

The catalog is a small, made-up list of 20 songs covering genres like pop, lofi, rock, metal, and a few others, each tagged with a mood (like happy, chill, or angry) and numeric traits for energy, valence, danceability, and acousticness. I used the starter dataset as-is without adding or removing songs. Most genres only have one song each — pop is the only genre with two — so the catalog can't really represent the full range of any genre's variety, and things like lyrics, vocal style, or instrumentation aren't captured at all.

---

## 5. Strengths  

The system works well for listeners with a clear, well-represented taste, like a high-energy pop fan or a chill lofi fan — their top picks are genuinely a good match, and the reasons given for each pick make sense. It also correctly tells apart listeners who want similar energy levels but different moods, for example separating a "happy" high-energy fan from an "intense" high-energy fan even though both want loud, energetic songs. The artist cap also does its job: no single artist crowds out the results, even when they have several high-scoring songs.

---

## 6. Limitations and Bias 

The system does not consider lyrics, vocals, tempo, or anything about the actual sound of a song — only its labeled genre, mood, and a handful of numeric traits. Genre and mood require an exact match, so listeners with tastes close to but not exactly matching a label (e.g. "chill" instead of "relaxed") are never matched well. It also does not validate most inputs, so out-of-range values (like an energy above 1) produce broken, misleading scores instead of an error.

**Finding from experiments:** the system quietly favors pop fans, because pop is the only genre with two songs in our small catalog, while every other genre only has one. That means a pop fan is the only person who can get a results list full of songs that truly match their taste, while a fan of any other genre gets one real match at most, and the rest of their list is filled in with songs from completely different genres that just happen to have a similar mood or energy level. When I tested this by making genre matter a lot more for a rock fan, it only kept that one rock song reliably at the top, and everything after it was a random-feeling mix of other genres rather than music an actual rock fan would want. This is a small example of a filter bubble caused by an unbalanced music collection rather than anything about the listener, and it would be worth fixing by having the system recognize similar genres instead of only rewarding an exact match, so that genres with few songs aren't unfairly overlooked.

---

## 7. Evaluation  

I tested nine made-up listeners: three normal ones meant to represent real people (a high-energy pop fan, a chill lofi fan, and a deep intense rock fan) and six "break it if you can" listeners meant to poke at the edges of the system (a completely blank listener with no preferences at all, a listener who typed in a made-up genre and mood, a listener who asked for an energy level way above what's possible, a listener who asked for a negative energy level, a listener who asked for angry metal but also said they like acoustic songs, and a listener who typed in a scoring mode that doesn't exist). For each one I looked at whether the top few picks actually made sense for that kind of listener, and whether the reasons given for each pick lined up with what I'd expect a real person to hear in that song.

The pop fan's list was upbeat and high-energy; the lofi fan's was slow and mellow — the two asked for opposite energy and mood, and the system told them apart correctly. The pop fan and rock fan both wanted high energy and shared a couple of loud songs, but the rock fan's top pick was moody and aggressive while the pop fan's was bright and cheerful, so the system is also picking up on "happy" versus "intense," not just loudness.

The biggest surprise: the blank listener and the listener with a made-up genre and mood got almost identical lists. I expected "said nothing" and "said something unrecognized" to behave differently, but both silently fall back to the same generic playlist with no warning that the request wasn't understood. The two out-of-bounds energy listeners (too high, negative) both produced negative-looking scores instead of an error — flipping the direction only changed which songs filled out the bottom of the list, not the underlying problem, so there's no real sanity check on numbers outside the expected 0-to-1 range.

The rock fan and the "contradictory acoustic metal" listener (same angry/intense style, but also wants acoustic songs, which barely exist in that style) landed on the same top pick — genre, mood, and energy outweighed the acoustic request, so the contradiction just quietly lost out instead of causing confusion. By contrast, the listener who typed a scoring mode that doesn't exist was the only one the system actually stopped for with an error, rather than guessing or falling back to a default like it does for every other bad input — the system is inconsistent about which mistakes it catches.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

- Implement a RAG system that could pull songs off of the interent or a some other data source to diversify and increase song data
- Build more validations checks for user profile input
- Connect the model to Streamlit to create a interactive user application similar to spotify (data validation would be needed for sure here)

---

## 9. Personal Reflection  

I learnt a lot from the research portion at the beginning of this project about how real recommendation systems function.

All though this simple model only used weights and normalized vaues for song features to generate recommendations, it still felt like it was a small scale recommendation engine due to its ability to provide scores and reasoning behind the rankings of songs.

As I went through this project, I realized that these systems are heavily subjected the discretion of the creator due to the constant decision of features vs tradeoffs. This was definitely a fun project, and I see how ML/AI systems are useful in creating recommendation systems as tech evolves.

Throughout the building process, I used AI to implement code, visual the flow of data across functions and files, and draft various versions of new model functions.
I felt that I mostly did architectural work and creative design. The AI agent did sometimes need corrections to make the code more 'Pythonic" (modular / concise).

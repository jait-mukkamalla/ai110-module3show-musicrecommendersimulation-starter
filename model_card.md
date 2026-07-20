# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Finding from experiments:** the system quietly favors pop fans, because pop is the only genre with two songs in our small catalog, while every other genre only has one. That means a pop fan is the only person who can get a results list full of songs that truly match their taste, while a fan of any other genre gets one real match at most, and the rest of their list is filled in with songs from completely different genres that just happen to have a similar mood or energy level. When I tested this by making genre matter a lot more for a rock fan, it only kept that one rock song reliably at the top, and everything after it was a random-feeling mix of other genres rather than music an actual rock fan would want. This is a small example of a filter bubble caused by an unbalanced music collection rather than anything about the listener, and it would be worth fixing by having the system recognize similar genres instead of only rewarding an exact match, so that genres with few songs aren't unfairly overlooked.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested nine made-up listeners: three normal ones meant to represent real people (a high-energy pop fan, a chill lofi fan, and a deep intense rock fan) and six "break it if you can" listeners meant to poke at the edges of the system (a completely blank listener with no preferences at all, a listener who typed in a made-up genre and mood, a listener who asked for an energy level way above what's possible, a listener who asked for a negative energy level, a listener who asked for angry metal but also said they like acoustic songs, and a listener who typed in a scoring mode that doesn't exist). For each one I looked at whether the top few picks actually made sense for that kind of listener, and whether the reasons given for each pick lined up with what I'd expect a real person to hear in that song.

The pop fan's list was upbeat and high-energy; the lofi fan's was slow and mellow — the two asked for opposite energy and mood, and the system told them apart correctly. The pop fan and rock fan both wanted high energy and shared a couple of loud songs, but the rock fan's top pick was moody and aggressive while the pop fan's was bright and cheerful, so the system is also picking up on "happy" versus "intense," not just loudness.

The biggest surprise: the blank listener and the listener with a made-up genre and mood got almost identical lists. I expected "said nothing" and "said something unrecognized" to behave differently, but both silently fall back to the same generic playlist with no warning that the request wasn't understood. The two out-of-bounds energy listeners (too high, negative) both produced negative-looking scores instead of an error — flipping the direction only changed which songs filled out the bottom of the list, not the underlying problem, so there's no real sanity check on numbers outside the expected 0-to-1 range.

The rock fan and the "contradictory acoustic metal" listener (same angry/intense style, but also wants acoustic songs, which barely exist in that style) landed on the same top pick — genre, mood, and energy outweighed the acoustic request, so the contradiction just quietly lost out instead of causing confusion. By contrast, the listener who typed a scoring mode that doesn't exist was the only one the system actually stopped for with an error, rather than guessing or falling back to a default like it does for every other bad input — the system is inconsistent about which mistakes it catches.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

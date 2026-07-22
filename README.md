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
real world music recommenders work by translating a listener started and implied preferences into compared numeric scores, then they rank condidates byy how well they match. So they score and then sort . My version would prioritize genre and mood as the strongest signals, since they capture kind of music and what situation someone wants. Features like energy, acousticness, valencfe, and danceability are scored b closeness to a targe rathe than the magnituede since more enegric does not rly mean better, only closer to what the use asked for. 

I would have like an id, title, artist, genre, mood, energy, calence, danceability, acoustiness,tempo bpm. The user profile features would be like fav genre, fav mood, fav energy, target tempo, and target energy

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Finalized algo recipe.
Step 1 - Have a taste profile. So i will have a dictonary of target values on the same scare as the song features.
Step 2 - we will rankfeatures by how cosly a miss is basically weights. 
Step 3 - Scoring - so bascially there will be a categorical match and then we wills core by that and closeness, then boolean preference, and sum of the weight and contribution. It will return a score and the reasons.
Step 4 - Then you will score every song with step 3 and it wll sort by score. Then we wills lice to the top 5 with a tie breaker being id, so the results aer repoducable.
Step 5 - turn reasons list into a sentence for explaining

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
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
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




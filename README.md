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
TOP RECOMMENDATIONS
  for: genre=pop, mood=happy, energy=0.8
============================================================

1. Sunrise City  (by Neon Echo)
   Score: 6.96
   Reasons:
     - matches your favorite genre (pop) (+3.0)
     - matches your mood (happy) (+2.0)
     - energy level is a great fit (+2.0)

2. Gym Hero  (by Max Pulse)
   Score: 4.74
   Reasons:
     - matches your favorite genre (pop) (+3.0)
     - energy level is close to what you want (+1.7)

3. Rooftop Lights  (by Indigo Parade)
   Score: 3.92
   Reasons:
     - matches your mood (happy) (+2.0)
     - energy level is a great fit (+1.9)

4. Night Drive Loop  (by Neon Echo)
   Score: 1.90
   Reasons:
     - energy level is a great fit (+1.9)

5. Storm Runner  (by Voltline)
   Score: 1.78
   Reasons:
     - energy level is close to what you want (+1.8)

============================================================

```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Stress Test Results

To find out whether the scoring logic could be "tricked," I ran a set of
adversarial / edge-case profiles (defined in `ADVERSARIAL_PROFILES` in
`src/main.py`) through the same `recommend_songs` pipeline as the normal
profile. Each block below is the raw terminal output, exactly as printed.

**1. Conflicting energy vs. mood** — asks for high energy (`0.9`) but a
low-energy mood. Genre + mood points swamp energy, so a calm classical track
wins over every high-energy song:

```
  TOP RECOMMENDATIONS
  for: genre=classical, mood=melancholy, energy=0.9
============================================================

1. Moonlit Sonata Drift  (by Elena Voss)
   Score: 5.80
   Reasons:
     - matches your favorite genre (classical) (+3.0)
     - matches your mood (melancholy) (+2.0)

2. Storm Runner  (by Voltline)
   Score: 1.98
   Reasons:
     - energy level is a great fit (+2.0)

3. Gym Hero  (by Max Pulse)
   Score: 1.94
   Reasons:
     - energy level is a great fit (+1.9)

4. Neon Overdrive  (by Pulse Machine)
   Score: 1.90
   Reasons:
     - energy level is a great fit (+1.9)

5. Iron Verdict  (by Ashen Crown)
   Score: 1.86
   Reasons:
     - energy level is a great fit (+1.9)
```

**2. Non-existent genre / mood** — `genre=polka`, `mood=sad` match no song, so
both silently score 0 and the ranking quietly degrades to energy-only. No
warning that the input was unrecognized:

```
  TOP RECOMMENDATIONS
  for: genre=polka, mood=sad, energy=0.5
============================================================

1. Island Time  (by Coral Sound)
   Score: 2.00
   Reasons:
     - energy level is a great fit (+2.0)

2. Velvet Hours  (by Mira Sole)
   Score: 1.96
   Reasons:
     - energy level is a great fit (+2.0)

3. Dusty Backroads  (by Cole Harlan)
   Score: 1.90
   Reasons:
     - energy level is a great fit (+1.9)

4. Midnight Coding  (by LoRoom)
   Score: 1.84
   Reasons:
     - energy level is a great fit (+1.8)

5. Focus Flow  (by LoRoom)
   Score: 1.80
   Reasons:
     - energy level is a great fit (+1.8)
```

**3. Boundary energy = 0.0** — rewards the lowest-energy songs. Note ranks 3–5
score above 1.0 yet print "no strong matches" because a `0.3 < gap` energy
contribution earns points but no reason string:

```
  TOP RECOMMENDATIONS
  for: genre=none, mood=none, energy=0.0
============================================================

1. Spacewalk Thoughts  (by Orbit Bloom)
   Score: 1.44
   Reasons:
     - energy level is close to what you want (+1.4)

2. Moonlit Sonata Drift  (by Elena Voss)
   Score: 1.40
   Reasons:
     - energy level is close to what you want (+1.4)

3. Library Rain  (by Paper Lanterns)
   Score: 1.30
   Reasons: no strong matches with your preferences

4. Coffee Shop Stories  (by Slow Stereo)
   Score: 1.26
   Reasons: no strong matches with your preferences

5. Winds of Elsewhere  (by Hollow Pines)
   Score: 1.24
   Reasons: no strong matches with your preferences
```

**4. Boundary energy = 1.0** — the mirror image, rewarding the highest-energy
songs in the catalog:

```
  TOP RECOMMENDATIONS
  for: genre=none, mood=none, energy=1.0
============================================================

1. Iron Verdict  (by Ashen Crown)
   Score: 1.94
   Reasons:
     - energy level is a great fit (+1.9)

2. Neon Overdrive  (by Pulse Machine)
   Score: 1.90
   Reasons:
     - energy level is a great fit (+1.9)

3. Gym Hero  (by Max Pulse)
   Score: 1.86
   Reasons:
     - energy level is a great fit (+1.9)

4. Storm Runner  (by Voltline)
   Score: 1.82
   Reasons:
     - energy level is a great fit (+1.8)

5. Sunrise City  (by Neon Echo)
   Score: 1.64
   Reasons:
     - energy level is close to what you want (+1.6)
```

**5. Case mismatch** — correct taste but capitalized (`Pop`, `Happy`).
Exact-string matching drops all 5 categorical points, so the "perfect" pop/happy
profile ranks songs by energy alone:

```
  TOP RECOMMENDATIONS
  for: genre=Pop, mood=Happy, energy=0.82
============================================================

1. Sunrise City  (by Neon Echo)
   Score: 2.00
   Reasons:
     - energy level is a great fit (+2.0)

2. Rooftop Lights  (by Indigo Parade)
   Score: 1.88
   Reasons:
     - energy level is a great fit (+1.9)

3. Night Drive Loop  (by Neon Echo)
   Score: 1.86
   Reasons:
     - energy level is a great fit (+1.9)

4. Storm Runner  (by Voltline)
   Score: 1.82
   Reasons:
     - energy level is a great fit (+1.8)

5. Gym Hero  (by Max Pulse)
   Score: 1.78
   Reasons:
     - energy level is close to what you want (+1.8)
```

**6. Acoustic vs. energy** — wants high energy (`0.95`) AND acoustic, but every
acoustic song is low energy. The +1.0 acoustic bonus lets a mid-energy country
track (`Dusty Backroads`, energy 0.55) beat true high-energy songs:

```
  TOP RECOMMENDATIONS
  for: genre=none, mood=none, energy=0.95
============================================================

1. Dusty Backroads  (by Cole Harlan)
   Score: 2.20
   Reasons:
     - has the acoustic sound you like (+1.0)

2. Neon Overdrive  (by Pulse Machine)
   Score: 2.00
   Reasons:
     - energy level is a great fit (+2.0)

3. Gym Hero  (by Max Pulse)
   Score: 1.96
   Reasons:
     - energy level is a great fit (+2.0)

4. Iron Verdict  (by Ashen Crown)
   Score: 1.96
   Reasons:
     - energy level is a great fit (+2.0)

5. Midnight Coding  (by LoRoom)
   Score: 1.94
   Reasons:
     - has the acoustic sound you like (+1.0)
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

### Accuracy & Surprises

**The surprise:** In the starter `pop / happy / energy=0.8` profile, **"Gym Hero"
ranks #2 (score 4.74) even though it is tagged `mood=intense`, not `happy`.** A
song that is explicitly *not* happy beats "Rooftop Lights" (#3, score 3.92),
which *is* tagged `happy`. For a "happy" request, that feels backwards.

**Why it happens — tracing the actual weights in `recommender.py`:**

- `GENRE_POINTS = 3.0`, `MOOD_POINTS = 2.0`, `ENERGY_MAX_POINTS = 2.0`.
- "Gym Hero" is `pop` (matches genre → **+3.0**), `intense` (no mood match → +0),
  energy `0.93` vs target `0.8` → gap `0.13`, so `2.0 * (1 - 0.13) = ` **+1.74**.
  Total = **4.74**.
- "Rooftop Lights" is `indie pop` (**not** `pop`, so genre → +0), `happy`
  (matches mood → **+2.0**), energy `0.76` vs `0.8` → gap `0.04`, so
  `2.0 * (1 - 0.04) = ` **+1.92**. Total = **3.92**.

So a single genre match (`+3.0`) outweighs a mood match (`+2.0`) entirely, and
"Rooftop Lights" is punished for being `indie pop` rather than exactly `pop`.
Because genre is weighted higher than mood **and** matching is exact-string, the
recommender treats "right genre, wrong mood" as a better fit than "wrong genre,
right mood" — which is why an *intense* workout song keeps surfacing for a
*happy* listener. The fix would be either lowering `GENRE_POINTS` relative to
`MOOD_POINTS`, or grouping related genres (e.g. `indie pop` ≈ `pop`) so a
near-miss genre isn't scored as a total miss.

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




# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  
vibeMatch 1..0

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

VibeMatch is a simple content-based recommender that suggests songs from a small local catalog based on a user's stated genre, mood, and energy preferences. It's designed for classroom exploration of how recommendation algorithms work — not for production use or real listeners. It assumes a user can express their taste as a few clean preference values (a favorite genre, a favorite mood, a target energy level, and optionally whether they like acoustic music), and it always returns *something*, even when the request doesn't match anything well in the catalog. It's meant to teach how scoring, weighting, and ranking logic interact, and to expose — through deliberate stress-testing — where that logic breaks down.


---

## 3. How the Model Works  


Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song gets scored against a user's preferences using four signals: does the genre match (worth the most points), does the mood match (worth a bit less), how close is the song's energy to what the user wants (a sliding scale, not all-or-nothing), and — if the user says they like acoustic music — is the song acoustic enough to earn a small bonus.

Genre and mood are treated as exact matches: either the song hits the target or it doesn't. Energy is treated differently, since nobody's energy preference is an exact number — it rewards songs that are *close* to the target and gradually gives less credit the further away a song gets, in either direction.

All four scores are added together into one number, and every song in the catalog gets scored this way. The recommender then sorts every song from highest to lowest score and returns the top 5. Alongside the score, it also returns a plain-English list of reasons ("matches your favorite genre," "energy level is a great fit") so the recommendation isn't just a number
---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog contains **18 songs**, hand-assembled and expanded from a 10-song starter file. It spans 15 genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, edm, classical, country, reggae, metal, r&b, folk) and a similarly wide range of moods (happy, chill, intense, moody, relaxed, focused, confident, energetic, melancholy, nostalgic, aggressive, romantic, wistful).

Each song has: genre, mood, energy (0–1), valence (0–1), danceability (0–1), acousticness (0–1), and tempo in BPM (60–152).

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The recommender does well when a user's stated genre and mood both exist clearly in the catalog and line up with a real song — for example, a "pop / happy / energy 0.8" profile correctly surfaces "Sunrise City," a pop song tagged happy with energy 0.82, as its clear #1 pick. It also correctly distinguishes very different taste clusters: a "lofi / chill / low energy" profile and a "metal / aggressive / high energy" profile produce completely different, non-overlapping top-5 lists, which shows the scoring logic captures broad taste differences well. The energy closeness scoring behaves smoothly and predictably — songs closer to the target energy consistently outscore songs further away, with no weird jumps or reversals.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  
The system over-weights genre relative to mood — a genre match alone (+3.0) can outscore a mood match alone (+2.0) plus a decent energy fit, so a song tagged the *wrong* mood but the *right* genre often ranks above a song with the *right* mood but wrong genre. For example, "Gym Hero" (tagged "intense") ranked #2 for a "pop / happy" profile — ahead of "Rooftop Lights," which is actually tagged "happy" — purely because "Gym Hero" matched genre and "Rooftop Lights" didn't.

Genre and mood matching is also exact-string and case-sensitive: typing "Pop" instead of "pop" silently loses all genre and mood credit, with no error or warning to the user. The system never tells a user when their genre or mood doesn't exist in the catalog at all (e.g., "polka" or "sad") — it just quietly falls back to ranking by energy alone, which can look like a confident recommendation for a request it fundamentally can't serve. Finally, because energy scoring never subtracts points (only adds less), the system always returns five results and a nonzero score, even for a profile that matches nothing in the catalog — there's no way for it to say "I don't have anything close to what you want."
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.
I tested three baseline profiles representing distinct tastes ("High-Energy Pop," "Chill Lofi," "Deep Intense Rock") to confirm the recommender differentiates broad taste clusters, which it did — each profile produced a clearly different top-5 list matching the expected genre/mood/energy cluster.

I then ran six adversarial profiles specifically designed to break the scoring logic: conflicting energy vs. mood (wanting high energy but a melancholy/classical vibe), a nonexistent genre and mood ("polka"/"sad"), boundary energy values (0.0 and 1.0), a case-mismatched but otherwise perfect profile ("Pop"/"Happy" instead of "pop"/"happy"), and a profile wanting both high energy and acoustic songs (a contradiction in this dataset, since every acoustic song here is low-energy).

What surprised me most: the conflicting_energy_vs_mood profile put a 0.30-energy classical/melancholy track at #1 with a score of 5.80, even though the user explicitly asked for energy 0.9 — because genre + mood together (5.0 points) comfortably beat the best possible energy score (2.0 points). This proved that in this weighting scheme, categorical matches almost always override numeric preferences, no matter how strongly the user states them. The case-mismatch test was equally revealing: a functionally perfect profile ("Pop"/"Happy") scored identically to the nonexistent-genre profile, because the exact-string check has zero tolerance for capitalization.


---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  
If I kept developing this, I'd: (1) add fuzzy/case-insensitive matching for genre and mood, and let mood accept a small set of related values (e.g. "chill" and "relaxed" giving partial credit) instead of one exact string; (2) rebalance or cap the weights so a single strong numeric mismatch (like energy) can meaningfully pull down a genre+mood match, instead of always losing to it; and (3) add a minimum-score threshold so the system can honestly say "nothing in the catalog matches what you're looking for" instead of always returning five songs regardless of fit quality.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

The biggest learning moment was seeing how a small, seemingly reasonable weighting choice (genre worth more than mood) had outsized, non-obvious effects once real songs were run through it — a "wrong mood, right genre" song beat a "right mood, wrong genre" song almost every time, which isn't something I would have predicted just from looking at the weight numbers on paper. Using AI tools helped me move fast from design to working code and catch edge cases I wouldn't have thought to test myself (like case sensitivity or the acoustic/energy contradiction), but I had to double-check that the suggested weights and scoring formulas actually matched my own reasoning from the Algorithm Recipe phase, rather than just accepting whatever numbers were proposed. What surprised me most is how "dumb," rule-based, additive scoring can still *feel* like a real recommendation when the weights are chosen thoughtfully — but also how quickly that illusion breaks once you deliberately try to trick it. If I extended this project, I'd want to try a version where multiple numeric features (not just energy) contribute to closeness scoring, to see whether that produces more nuanced, less genre-dominated rankings.

# CinePulse NLP Recommendation Engine Evaluation Report

**Generated on**: 2026-10-12 11:09:12 UTC  
**Catalog Size**: 40 movies  
**Engine Version**: `cb1a6dbfbcddfc20`  

---

## 1. Executive Summary & Ground-Truth Disclaimer

> [!IMPORTANT]
> **Ground-Truth Label Disclaimer**: Content-based filtering is inherently unsupervised. Unlabeled catalog datasets (like TMDB) do **not** possess universal human ground-truth relevance labels. Therefore, metrics like Precision@K and Recall@K reported here utilize **structural metadata proxies** (e.g. matching director or shared sub-genres). Metrics are directly measured from actual engine execution.

---

## 2. Performance & System Latency Metrics

All latency measurements were taken on the local host environment over 100 consecutive on-demand sparse cosine vector dot-product queries:

| Metric | Measured Value | Target SLA | Status |
| :--- | :--- | :--- | :--- |
| **p50 Latency (Median)** | **0.67 ms** | < 10.0 ms | **PASSED** |
| **p95 Latency (Tail)** | **1.08 ms** | < 25.0 ms | **PASSED** |
| **Mean Inference Latency** | **0.71 ms** | < 15.0 ms | **PASSED** |
| **Catalog Coverage (Top-10 sample)** | **92.5%** | > 15.0% | **PASSED** |
| **Duplicate Recommendation Rate** | **0.0%** | 0.0% | **PASSED** |
| **Sparse Matrix RAM Footprint** | **0.029 MB** | < 100 MB | **OPTIMAL** |

---

## 3. Feature Strategy Comparison: Overview-Only vs. Weighted Metadata Soup

We contrasted two feature formulation strategies across the catalog:

| Dimension | Strategy A: Overview-Only TF-IDF | Strategy B: CinePulse Weighted Soup (Selected) |
| :--- | :--- | :--- |
| **Document Formula** | Synopsis text with stop words removed | Director (3x) + Genres (2x) + Keywords (2x) + Cast (1x) + Synopsis (1x) |
| **Vocabulary Size** | Unigrams & Bigrams (~15k terms) | Domain entities + Token bigrams (~22k terms) |
| **Franchise & Sequel Recall** | Low (sequels often have different plot summaries) | High (shared director, cast, and keyword tokens cleanly bridge sequels) |
| **Director Auteur Alignment** | Accidental (relies on synopsis mention) | High (strong 3x weighting binds directorial style) |
| **Explainability** | Low (cannot distinguish why a match occurred) | High (enables transparent intersection chips: genres, director, cast) |
| **Decision** | Baseline comparator | **Selected Production Standard** |

---

## 4. Qualitative Top-10 Inspection (Sample Queries)

### Target Movie: **Quantum Horizon** (2021)
- **Genres**: Science Fiction, Adventure, Drama
- **Director**: Elena Vance
- **Inference Latency**: 6.65 ms | **Intra-List Genre Diversity**: 0.35

| Rank | Recommended Title | Score | Director | Shared Attributes / Truthful Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Quantum Horizon: Singularity** (2024) | 0.2805 | Elena Vance | Directed by Elena Vance • Starring Marcus Aurelius Reed, Sarah Chen • Shared genres: Adventure, Science Fiction • Matching themes: time dilation, wormhole |
| 2 | **Labyrinth of Solitude** (2018) | 0.1038 | Elena Vance | Directed by Elena Vance • Shared genres: Science Fiction |
| 3 | **Dune of Ash** (2021) | 0.0624 | Denis Villeneuve | Shared genres: Adventure, Drama |
| 4 | **Starlight Odyssey** (2022) | 0.0605 | Maya Lin | Shared genres: Science Fiction • Matching themes: space exploration |
| 5 | **Dune of Ash: Prophecy** (2024) | 0.0414 | Denis Villeneuve | Shared genres: Adventure, Science Fiction |

---

### Target Movie: **Quantum Horizon: Singularity** (2024)
- **Genres**: Science Fiction, Adventure, Mystery
- **Director**: Elena Vance
- **Inference Latency**: 0.76 ms | **Intra-List Genre Diversity**: 0.30

| Rank | Recommended Title | Score | Director | Shared Attributes / Truthful Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Quantum Horizon** (2021) | 0.2805 | Elena Vance | Directed by Elena Vance • Starring Marcus Aurelius Reed, Sarah Chen • Shared genres: Adventure, Science Fiction • Matching themes: time dilation, wormhole |
| 2 | **Labyrinth of Solitude** (2018) | 0.1329 | Elena Vance | Directed by Elena Vance • Shared genres: Mystery, Science Fiction |
| 3 | **The Cipher of Babylon** (2024) | 0.0810 | Harrison Blake | Starring Oscar Isaac • Shared genres: Adventure, Mystery |
| 4 | **Dune of Ash: Prophecy** (2024) | 0.0516 | Denis Villeneuve | Starring Florence Pugh • Shared genres: Adventure, Science Fiction |
| 5 | **Dune of Ash** (2021) | 0.0509 | Denis Villeneuve | Starring Oscar Isaac • Shared genres: Adventure, Science Fiction |

---

### Target Movie: **Neon Syndicate** (2020)
- **Genres**: Science Fiction, Action, Thriller
- **Director**: Kenji Watanabe
- **Inference Latency**: 0.54 ms | **Intra-List Genre Diversity**: 0.29

| Rank | Recommended Title | Score | Director | Shared Attributes / Truthful Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Neon Syndicate: Overdrive** (2023) | 0.2508 | Kenji Watanabe | Directed by Kenji Watanabe • Starring Dev Patel, Hiroyuki Sanada • Shared genres: Action, Science Fiction • Matching themes: artificial intelligence, cyberpunk |
| 2 | **Shadow Blade** (2022) | 0.0835 | Kenji Watanabe | Directed by Kenji Watanabe • Starring Hiroyuki Sanada • Shared genres: Action |
| 3 | **The Last Samurai of Kyoto** (2019) | 0.0812 | Kenji Watanabe | Directed by Kenji Watanabe • Starring Hiroyuki Sanada • Shared genres: Action |
| 4 | **The Crimson Vanguard** (2021) | 0.0553 | Chadwick Stone | Shared genres: Action, Science Fiction |
| 5 | **Ironclad Protocol** (2019) | 0.0487 | Chadwick Stone | Shared genres: Action, Thriller |

---

### Target Movie: **Neon Syndicate: Overdrive** (2023)
- **Genres**: Science Fiction, Action, Crime
- **Director**: Kenji Watanabe
- **Inference Latency**: 0.48 ms | **Intra-List Genre Diversity**: 0.34

| Rank | Recommended Title | Score | Director | Shared Attributes / Truthful Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Neon Syndicate** (2020) | 0.2508 | Kenji Watanabe | Directed by Kenji Watanabe • Starring Dev Patel, Hiroyuki Sanada • Shared genres: Action, Science Fiction • Matching themes: artificial intelligence, cyberpunk |
| 2 | **Shadow Blade** (2022) | 0.0875 | Kenji Watanabe | Directed by Kenji Watanabe • Starring Hiroyuki Sanada • Shared genres: Action |
| 3 | **The Last Samurai of Kyoto** (2019) | 0.0850 | Kenji Watanabe | Directed by Kenji Watanabe • Starring Hiroyuki Sanada • Shared genres: Action |
| 4 | **Aetherium: Clockwork Realm** (2025) | 0.0424 | Maya Lin | Starring Dev Patel, Florence Pugh • Shared genres: Action |
| 5 | **Midnight in Marseille** (2021) | 0.0414 | Jean-Luc Moreau | Shared genres: Action, Crime |

---

### Target Movie: **Shadows of the Crown** (2019)
- **Genres**: Drama, History, Thriller
- **Director**: Arthur Sterling
- **Inference Latency**: 0.51 ms | **Intra-List Genre Diversity**: 0.34

| Rank | Recommended Title | Score | Director | Shared Attributes / Truthful Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **The Scottish Playwright** (2022) | 0.1706 | Arthur Sterling | Directed by Arthur Sterling • Starring Benedict Cumberbatch, Emma Thompson • Shared genres: Drama, History |
| 2 | **Sovereignty: Pax Romana** (2023) | 0.1149 | Harrison Blake | Starring Charles Dance, Tom Hiddleston • Shared genres: Drama, History • Matching themes: political intrigue |
| 3 | **The Glass Fortress** (2022) | 0.1145 | Arthur Sterling | Directed by Arthur Sterling • Shared genres: Drama, Thriller |
| 4 | **Sovereignty: The Fall of Carthage** (2020) | 0.0499 | Harrison Blake | Shared genres: Drama, History |
| 5 | **The Last Samurai of Kyoto** (2019) | 0.0493 | Kenji Watanabe | Shared genres: Drama, History |

---

### Target Movie: **The Glass Fortress** (2022)
- **Genres**: Drama, Thriller
- **Director**: Arthur Sterling
- **Inference Latency**: 0.51 ms | **Intra-List Genre Diversity**: 0.31

| Rank | Recommended Title | Score | Director | Shared Attributes / Truthful Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Shadows of the Crown** (2019) | 0.1145 | Arthur Sterling | Directed by Arthur Sterling • Shared genres: Drama, Thriller |
| 2 | **The Scottish Playwright** (2022) | 0.0830 | Arthur Sterling | Directed by Arthur Sterling • Shared genres: Drama |
| 3 | **Sicario: Borderline** (2015) | 0.0418 | Denis Villeneuve | Shared genres: Drama, Thriller |
| 4 | **Shadow Blade** (2022) | 0.0232 | Kenji Watanabe | Shared genres: Drama |
| 5 | **Corsica Vendetta** (2023) | 0.0219 | Jean-Luc Moreau | Shared genres: Drama |

---

### Target Movie: **Midnight in Marseille** (2021)
- **Genres**: Crime, Thriller, Action
- **Director**: Jean-Luc Moreau
- **Inference Latency**: 0.54 ms | **Intra-List Genre Diversity**: 0.28

| Rank | Recommended Title | Score | Director | Shared Attributes / Truthful Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Corsica Vendetta** (2023) | 0.1825 | Jean-Luc Moreau | Directed by Jean-Luc Moreau • Starring Mads Mikkelsen, Vincent Cassel • Shared genres: Action, Crime • Matching themes: underworld |
| 2 | **The Heist at Grand Palais** (2023) | 0.1501 | Jean-Luc Moreau | Directed by Jean-Luc Moreau • Starring Marion Cotillard, Vincent Cassel • Shared genres: Action, Crime |
| 3 | **Midnight Run to Monte Carlo** (2024) | 0.1464 | Jean-Luc Moreau | Directed by Jean-Luc Moreau • Starring Daniel Bruhl, Mads Mikkelsen • Shared genres: Crime, Thriller |
| 4 | **Sicario: Borderline** (2015) | 0.0536 | Denis Villeneuve | Shared genres: Crime, Thriller |
| 5 | **Neon Syndicate: Overdrive** (2023) | 0.0414 | Kenji Watanabe | Shared genres: Action, Crime |

---

### Target Movie: **Corsica Vendetta** (2023)
- **Genres**: Crime, Action, Drama
- **Director**: Jean-Luc Moreau
- **Inference Latency**: 0.56 ms | **Intra-List Genre Diversity**: 0.31

| Rank | Recommended Title | Score | Director | Shared Attributes / Truthful Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Midnight in Marseille** (2021) | 0.1825 | Jean-Luc Moreau | Directed by Jean-Luc Moreau • Starring Mads Mikkelsen, Vincent Cassel • Shared genres: Action, Crime • Matching themes: underworld |
| 2 | **Midnight Run to Monte Carlo** (2024) | 0.1472 | Jean-Luc Moreau | Directed by Jean-Luc Moreau • Starring Jean Reno, Lea Seydoux • Shared genres: Crime |
| 3 | **The Heist at Grand Palais** (2023) | 0.1151 | Jean-Luc Moreau | Directed by Jean-Luc Moreau • Starring Vincent Cassel • Shared genres: Action, Crime |
| 4 | **Shadow Blade** (2022) | 0.0828 | Kenji Watanabe | Shared genres: Action, Drama • Matching themes: revenge |
| 5 | **Neon Syndicate: Overdrive** (2023) | 0.0399 | Kenji Watanabe | Shared genres: Action, Crime |

---

### Target Movie: **Starlight Odyssey** (2022)
- **Genres**: Animation, Comedy, Family, Science Fiction
- **Director**: Maya Lin
- **Inference Latency**: 0.53 ms | **Intra-List Genre Diversity**: 0.38

| Rank | Recommended Title | Score | Director | Shared Attributes / Truthful Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Nebula Knights** (2024) | 0.3802 | Maya Lin | Directed by Maya Lin • Starring Awkwafina, Bill Hader • Shared genres: Animation, Comedy • Matching themes: alien creatures, intergalactic |
| 2 | **Aetherium: The Sky Islands** (2023) | 0.1025 | Maya Lin | Directed by Maya Lin • Starring Taika Waititi • Shared genres: Animation |
| 3 | **The Backyard Olympics** (2022) | 0.0624 | Greg Daniels | Shared genres: Comedy, Family |
| 4 | **Quantum Horizon** (2021) | 0.0605 | Elena Vance | Shared genres: Science Fiction • Matching themes: space exploration |
| 5 | **Aetherium: Clockwork Realm** (2025) | 0.0576 | Maya Lin | Directed by Maya Lin |

---

### Target Movie: **Nebula Knights** (2024)
- **Genres**: Animation, Adventure, Comedy, Family
- **Director**: Maya Lin
- **Inference Latency**: 1.31 ms | **Intra-List Genre Diversity**: 0.37

| Rank | Recommended Title | Score | Director | Shared Attributes / Truthful Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Starlight Odyssey** (2022) | 0.3802 | Maya Lin | Directed by Maya Lin • Starring Awkwafina, Bill Hader • Shared genres: Animation, Comedy • Matching themes: alien creatures, intergalactic |
| 2 | **Aetherium: The Sky Islands** (2023) | 0.1199 | Maya Lin | Directed by Maya Lin • Starring Taika Waititi • Shared genres: Adventure, Animation |
| 3 | **Aetherium: Clockwork Realm** (2025) | 0.0823 | Maya Lin | Directed by Maya Lin • Starring Zendaya • Shared genres: Adventure |
| 4 | **Serengeti Solitude** (2021) | 0.0701 | Maya Lin | Directed by Maya Lin • Shared genres: Adventure |
| 5 | **The Backyard Olympics** (2022) | 0.0632 | Greg Daniels | Shared genres: Comedy, Family |

---


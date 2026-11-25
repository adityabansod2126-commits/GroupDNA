# GroupDNA: Your WhatsApp Group Chat, Decoded
> *"Spotify Wrapped, but for your friend group."*

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Constraints](https://img.shields.io/badge/Constraints-No%20pandas%20%7C%20No%20matplotlib-red.svg)](#constraints)
[![Output](https://img.shields.io/badge/Visualization-Terminal%20ASCII%20Heatmap-success.svg)](#report-preview)

---

## 📌 Project Overview
**GroupDNA** is a behavioral analytics tool that parses raw, messy WhatsApp chat export text files (`.txt`) and decodes group dynamics, communication rhythms, conversation peaks, and personality archetypes across group members.

Built as the **Week 1 Minor Project for The Unlox Academy**, this project demonstrates high-discipline software engineering by transforming uncurated text logs into an executive-ready, screenshot-worthy intelligence report using **only standard Python fundamentals and NumPy**.

---

## 🚫 Architectural Restraints & Discipline
Industry data engineering is often cluttered with heavy libraries for simple tasks. GroupDNA proves that deep data science and text mining can be achieved cleanly with zero dependency bloat:

| Permitted Technologies | Strictly Prohibited Technologies |
| :--- | :--- |
| **Python Fundamentals** (Loops, Dicts, Tuples, Sets, Functions) | ❌ **pandas** (No DataFrames, no `read_csv`) |
| **NumPy** (`zeros`, slicing, aggregations, max normalizations) | ❌ **matplotlib / seaborn / plotly** (No plotting libraries) |
| **datetime** (`strptime`, `timedelta`) | ❌ **collections.Counter / defaultdict** (Custom dict counters only) |
| **String Methods** (`split`, `strip`, `lower`, `startswith`) | ❌ **re** (Zero regular expressions used) |
| **File I/O** (UTF-8 `open()`) | ❌ **Pre-built WhatsApp analyzers / NLP toolkits** |

---

## 🔍 Features & Pipeline

1. **Robust Chat Parser (Feature 1):**
   - Line-by-line streaming without regex.
   - Gracefully handles **5 real-world edge cases**: system notices (group creation/updates), `<Media omitted>` stubs, `This message was deleted` entries, multi-line continuations, and blank lines.
2. **Executive Overview (Feature 2):**
   - Calculates duration, active dates, total messages, and per-person message share with horizontal scaled block bars (`█`).
3. **Temporal Peak Detection (Feature 3):**
   - Discovers the single busiest day and the peak activity hour across the entire observation window.
4. **NumPy Activity Heatmap (Feature 4):**
   - Populates a `6 x 24` matrix mapping participants to hour-of-day.
   - Employs 4-tier terminal shading blocks (`.`, `░`, `▒`, `█`) normalized against individual maximums.
5. **Vocabulary & Slang Analysis (Feature 5):**
   - Cleans tokens, removes custom stop-words, and isolates the top inside-jokes and colloquialisms (`bhai`, `scene`, `yaar`).
6. **Response Speed & Ghost Streaks (Feature 6):**
   - Computes conversational turn latency in seconds (fastest vs. slowest repliers).
   - Scans full calendar to pinpoint maximum consecutive days with zero messages (unmasking the ghost).
7. **Personality Archetype Detection (Feature 7):**
   - Deterministic behavioral scoring for 8 archetypes:
     - **The Spammer:** High message burst volume back-to-back.
     - **The Group Mom:** Nurturing keyword frequency (`safe`, `eat`, `take care`).
     - **The Night Owl:** > 60% messages between 23:00 and 04:59.
     - **The Storyteller:** Longest average words per message (> 30 words).
     - **The Drama Queen:** High proportion of ALL-CAPS or double exclamations (`!!`).
     - **The Ghost:** Silent on > 60% of group days.
     - **The Comedian / Question Master:** Laugh tokens and interrogation frequency.
     - **Bonus Indian Archetype:** *The Proxy Seeker* (attendance & bunking terms).
8. **The Screenshot Report (Feature 8):**
   - Integrated terminal layout structured with ASCII box borders.

---

## 📊 Sample Output Preview

```text
============================================================
 GROUPDNA REPORT — "Hostel Bois 4ever"
 60 days • 3,174 messages • 6 members
============================================================

 Period        : 01 April 2024 to 30 May 2024
 Busiest day   : 14 April 2024 (84 messages)
 Busiest hour  : 17:00 - 18:00

 MESSAGES PER PERSON
 Rahul    ████████████████████  953 (30.0%)
 Priya    ███████████████       718 (22.6%)
 Neha     █████████████         635 (20.0%)
 Aman     ██████████            490 (15.4%)
 Karan    ███████               354 (11.2%)
 Vikas    .                      24 ( 0.8%)

 ACTIVITY HEATMAP (hour of day, columns 00 to 23)
         00 03 06 09 12 15 18 21
 Rahul   .  .  .  ▒  █  █  █  ▒
 Priya   .  .  .  ▒  █  █  █  ▒
 Aman    █  █  .  .  .  ░  ▒  ▒  <- NIGHT OWL
 Karan   .  .  .  ░  ▒  █  █  ░
 Neha    .  .  .  ░  ▒  █  █  ▒
 Vikas   .  .  .  .  ░  ░  ░  .

 THIS GROUP'S FAVOURITE WORDS
 bhai    ████████████████████  342
 scene   ███████████████       256
 yaar    ██████████            187
 kya     ████████              143
 guys    ██████                121

 RESPONSE PATTERNS
 Fastest replier : Rahul (avg 4.2 minutes)
 Slowest replier : Vikas (avg 6.8 hours)

 LONGEST SILENT STREAKS
 Vikas   : 11 days (16 Apr - 26 Apr)
 Karan   :  3 days
 Aman    :  2 days
 Rahul   :  1 day
 Neha    :  1 day
 Priya   :  0 days (never went silent)

 PERSONALITY ARCHETYPES
 Rahul   → THE SPAMMER        (avg 4.8 msgs in a row)
 Priya   → THE GROUP MOM      (caring keyword score: 218)
 Aman    → THE NIGHT OWL      (79.8% msgs between 23h-04h)
 Karan   → THE STORYTELLER    (avg 57.1 words per msg)
 Neha    → THE DRAMA QUEEN    (62.8% ALL-CAPS messages)
 Vikas   → THE GHOST          (silent on 44 of 60 days)

============================================================
 Generated by GroupDNA • Built with Python + NumPy
============================================================
```

---

## 🚀 How to Run

### Option 1: Run in Google Colab (Recommended)
1. Open [Google Colab](https://colab.research.google.com/).
2. Click **File** > **Upload notebook** and upload `GroupDNA_Submission.ipynb`.
3. In the left sidebar, click the **Folder icon 📁** and drag `hostel_bois.txt` into the files area.
4. Click **Runtime** > **Run all** (`Ctrl + F9`).

### Option 2: Run Locally
```bash
# Clone the repository
git clone https://github.com/your-username/GroupDNA.git
cd GroupDNA

# Run the standalone script
python groupdna.py hostel_bois.txt
```

---

## 👤 Author
- **Student Name:** Shital Patil
- **Academy:** The Unlox Academy
- **Course:** Applied Data Science (Minor Project 1)

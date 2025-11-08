# Iowa Bar Prep Flashcard Review System

An interactive spaced repetition flashcard system using the SuperMemo SM-2 algorithm for optimal retention.

## Quick Start

### 1. Initialize the Database

First, populate the flashcard database from your knowledge base:

```bash
python3 init_flashcards.py
```

This will:
- Create `iowa_bar_prep.db`
- Load concepts from JSON files (ultimate_knowledge_base.json, comprehensive_knowledge_base.json, etc.)
- Generate 500+ flashcards covering:
  - Rule statements
  - Elements
  - Common exam traps

### 2. Run Daily Review Sessions

Start your daily flashcard review:

```bash
python3 daily_study.py
```

## How It Works

### The Review Process

For each flashcard:

1. **Question shown** - Think through your answer
2. **Press Enter** - Reveal the answer
3. **Self-assess correctness** - Did you get it right? (y/n)
4. **Rate confidence** - How confident were you? (0-4)
   - 0 = Complete guess
   - 1 = Unsure
   - 2 = Fairly sure
   - 3 = Sure
   - 4 = Absolutely certain

### SM-2 Algorithm

The system automatically calculates when to show each card again based on:
- **Correctness** - Did you answer correctly?
- **Confidence** - How confident were you?
- **History** - Past performance on this card

**Review intervals:**
- ❌ Incorrect = 1 day
- ✅ First correct = 1 day
- ✅ Second correct = 6 days
- ✅ Subsequent = Increasing intervals (optimized by your performance)

### Features

- **Smart prioritization** - Due cards shown first
- **Session tracking** - All sessions logged to database
- **Progress analytics** - Accuracy, confidence, and streak stats
- **Early quit** - Type 'q' at any time to save progress and quit
- **Tomorrow preview** - See how many cards are due next session

## Database Schema

### flashcards
- Card content (front/back, subject, topic)
- SM-2 data (ease_factor, interval_days, repetitions)
- Due date and review history

### study_sessions
- Date, cards reviewed, accuracy
- Average confidence, duration

### review_history
- Individual review records
- Quality scores, confidence levels

## Tips for Effective Study

1. **Review daily** - Consistency is key for spaced repetition
2. **Be honest** - Accurate self-assessment improves the algorithm
3. **Think first** - Don't reveal the answer too quickly
4. **Target 90%+** - If below, review weak subjects between sessions
5. **Track progress** - Use session summaries to identify patterns

## Reinitializing

To reset the database and start fresh:

```bash
rm iowa_bar_prep.db
python3 init_flashcards.py
```

**Warning:** This deletes all review history and progress.

## Files

- `daily_study.py` - Interactive review session
- `init_flashcards.py` - Database initialization
- `iowa_bar_prep.db` - SQLite database (created by init script)

## Troubleshooting

**"Database not initialized" error:**
```bash
python3 init_flashcards.py
```

**No cards due:**
You're caught up! The system will show when cards become due.

**Database corrupted:**
```bash
rm iowa_bar_prep.db
python3 init_flashcards.py
```

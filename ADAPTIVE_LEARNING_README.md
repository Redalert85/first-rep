# Adaptive Learning System for Bar Prep

## Overview

This enhanced adaptive learning system combines the best features from `advanced_pedagogy.py` and `activate_spaced_repetition.py` to create a comprehensive, data-driven study tool optimized for Constitutional Law and Evidence.

## Key Features

### 1. Enum-Based Controlled Vocabulary

Provides type-safe, controlled vocabulary for subjects and topics:

**Subjects:**
- Constitutional Law
- Evidence
- Contracts, Torts, Criminal Law, Criminal Procedure, Civil Procedure, Real Property

**Constitutional Law Topics (35 subtopics):**
- Judicial Review & Justiciability (Standing, Mootness, Ripeness)
- Federal Powers (Commerce Clause, Taxing/Spending, Treaty Power)
- Due Process (Procedural, Substantive, Incorporation, Fundamental Rights)
- Equal Protection (Strict/Intermediate/Rational Basis, Suspect Classifications)
- First Amendment (Speech, Religion, Press, Assembly)
- Other Rights (Takings, Privileges & Immunities, Dormant Commerce Clause)

**Evidence Topics (50+ subtopics):**
- Relevance (Logical, Legal 403, Conditional)
- Character Evidence (Civil, Criminal, 404(b), Habit)
- Hearsay (Definition, 803/804 Exceptions, all major exceptions)
- Confrontation Clause
- Impeachment (6 methods)
- Privileges (Attorney-Client, Spousal, Doctor-Patient, Psychotherapist)
- Expert Testimony (Daubert, Qualifications, Bases)
- Authentication & Best Evidence Rule

### 2. SM-2 Spaced Repetition Algorithm

Implements the SuperMemo SM-2 algorithm for optimal retention:

```python
# Cards are reviewed based on:
- Ease Factor: 1.3 - 4.0 (how "easy" the card is)
- Interval: Days until next review (1, 6, then exponential)
- Repetitions: Number of successful reviews
- Next Review Date: Calculated automatically
```

**Review Quality Scale (0-5):**
- 0-1: Complete blackout (reset learning)
- 2: Incorrect but remembered something
- 3: Correct with difficulty
- 4: Correct with hesitation
- 5: Perfect recall

### 3. Confidence-Weighted Scoring

Adjusts learning based on confidence calibration:

| Confidence | Correct | Effect |
|-----------|---------|--------|
| High | ✓ | Boost quality (+0.5) - excellent! |
| High | ✗ | Penalize heavily (-1.0) - serious misconception |
| Low | ✓ | Moderate boost (+0.3) - learning happening |
| Low | ✗ | Slight penalty (-0.2) - expected |

This prevents overconfidence and improves metacognitive awareness.

### 4. SQLite Persistence

All data persists across sessions:

**Tables:**
- `cards` - Learning cards with SM-2 state
- `performance` - Individual review records
- `sessions` - Study session tracking

**Automatic tracking of:**
- Review history
- Performance trends
- Subject mastery
- Topic-level analytics

### 5. Adaptive Question Block Generation

Intelligently generates study blocks based on:

1. **Spaced Repetition Priority** - Due cards first
2. **Performance-Based Difficulty** - Adjusts to 70-85% accuracy target
3. **Mastery Weighting** - Prioritizes low-mastery topics
4. **Recency Balancing** - Reviews forgotten material
5. **Topic Targeting** - Drill specific weak areas

## Usage Examples

### Basic Setup

```python
from adaptive_learning_system import (
    AdaptiveLearningSystem,
    Subject,
    ConstitutionalLawTopic,
    EvidenceTopic,
    DifficultyLevel,
    ConfidenceLevel
)

# Initialize system
system = AdaptiveLearningSystem("my_bar_prep.db")
```

### Adding Cards

```python
# Add a Constitutional Law card
system.add_card(
    subject=Subject.CONSTITUTIONAL_LAW,
    topic=ConstitutionalLawTopic.STRICT_SCRUTINY,
    concept_name="Strict Scrutiny Test",
    question="What are the elements of strict scrutiny?",
    answer="(1) Compelling government interest, (2) Narrowly tailored means",
    difficulty=DifficultyLevel.INTERMEDIATE,
    tags=["equal_protection", "fundamental_rights"]
)

# Add an Evidence card
system.add_card(
    subject=Subject.EVIDENCE,
    topic=EvidenceTopic.HEARSAY_EXCEPTIONS_803,
    concept_name="Present Sense Impression",
    question="What is the present sense impression exception under FRE 803(1)?",
    answer="A statement describing an event made while or immediately after perceiving it.",
    difficulty=DifficultyLevel.FOUNDATIONAL,
    tags=["hearsay", "FRE_803"]
)
```

### Study Session

```python
# Start session
session = system.start_session()

# Get adaptive block (automatically selects best cards)
cards = system.get_study_block(
    block_size=10,
    subject=Subject.CONSTITUTIONAL_LAW,  # Optional: focus on one subject
    include_new=True,
    include_review=True
)

# Review each card
for card in cards:
    print(f"Q: {card.question}")

    # User studies and answers
    # ...

    # Record performance
    system.review_card(
        card=card,
        quality=4,  # 0-5 scale
        confidence=ConfidenceLevel.CONFIDENT,
        time_taken=45  # seconds
    )

# End session
system.end_session()
```

### Targeted Practice

```python
# Target specific weak topics
weak_cards = system.get_targeted_block(
    subject=Subject.EVIDENCE,
    topics=[
        EvidenceTopic.HEARSAY_EXCEPTIONS_803.value,
        EvidenceTopic.HEARSAY_EXCEPTIONS_804.value
    ],
    block_size=15
)
```

### Performance Analytics

```python
# Overall statistics
stats = system.get_statistics()
print(f"Total Cards: {stats['total_cards']}")
print(f"Due Today: {stats['due_cards']}")
print(f"Mastered: {stats['mastered_cards']} ({stats['mastery_percentage']:.1f}%)")
print(f"7-Day Accuracy: {stats['recent_7day_accuracy'] * 100:.1f}%")

# Subject-specific performance
conlaw_perf = system.get_subject_performance(Subject.CONSTITUTIONAL_LAW, days=30)
print(f"\nConstitutional Law (Last 30 days):")
print(f"  Total Reviews: {conlaw_perf['total_reviews']}")
print(f"  Accuracy: {conlaw_perf['accuracy'] * 100:.1f}%")
print(f"  Avg Confidence: {conlaw_perf['avg_confidence']:.2f}/5")
print(f"  Avg Time: {conlaw_perf['avg_time']:.0f}s")

# Topic breakdown
for topic, stats in conlaw_perf['topic_breakdown'].items():
    print(f"  {topic}: {stats['accuracy']*100:.1f}% ({stats['total_reviews']} reviews)")

# Identify weak topics
weak_topics = system.identify_weak_topics(
    Subject.CONSTITUTIONAL_LAW,
    threshold=0.7  # Topics below 70% accuracy
)
print("\nWeak Topics:")
for topic, accuracy in weak_topics:
    print(f"  {topic}: {accuracy*100:.1f}%")
```

## Study Workflow Recommendations

### Daily Review (30-45 minutes)

```python
# 1. Start fresh session
session = system.start_session()

# 2. Get due cards first (spaced repetition)
due_cards = system.get_study_block(
    block_size=20,
    include_new=False,  # Only review
    include_review=True
)

# 3. Review all due cards
# ...

# 4. Add new material if time permits
new_cards = system.get_study_block(
    block_size=5,
    include_new=True,
    include_review=False
)

# 5. End session
system.end_session()
```

### Weekly Weak Topic Drill

```python
# Find your weak areas
weak_evidence = system.identify_weak_topics(Subject.EVIDENCE, threshold=0.75)

# Drill top 3 weakest topics
for topic, accuracy in weak_evidence[:3]:
    print(f"\nDrilling: {topic} (Current: {accuracy*100:.1f}%)")

    cards = system.get_targeted_block(
        subject=Subject.EVIDENCE,
        topics=[topic],
        block_size=10
    )

    # Review cards...
```

### Pre-Exam Comprehensive Review

```python
# Generate mixed subject blocks
all_subjects_block = system.get_study_block(
    block_size=50,
    subject=None,  # All subjects
    difficulty_target=DifficultyLevel.BAR_EXAM_LEVEL
)

# Focus on high-difficulty cards
advanced_block = system.get_study_block(
    block_size=25,
    difficulty_target=DifficultyLevel.ADVANCED
)
```

## Advanced Features

### Card Priority Scoring

Cards are scored based on:
1. **Difficulty alignment** - Match target difficulty
2. **Mastery level** - Low mastery = high priority
3. **Recency** - Recently reviewed = lower priority
4. **Due date** - Overdue cards boosted

### Session Quality Metrics

Automatically calculated:
- **Accuracy** - Percentage correct
- **Average Confidence** - Self-assessment calibration
- **Session Quality** - Composite score (70% accuracy + 30% confidence)

### Performance Trends

Track over time:
- 7-day rolling accuracy
- Subject mastery progression
- Topic-level improvement
- Confidence calibration

## Integration with Existing Bar Prep System

This system is designed to work alongside your existing bar prep materials:

```python
# Import your existing knowledge base
from ultimate_knowledge_base import ULTIMATE_BAR_CONCEPTS

# Convert to adaptive learning cards
for concept in ULTIMATE_BAR_CONCEPTS:
    system.add_card(
        subject=map_to_subject(concept['subject']),
        topic=map_to_topic(concept['subtopic']),
        concept_name=concept['name'],
        question=concept.get('rule_statement', ''),
        answer=format_answer(concept),
        difficulty=assess_difficulty(concept),
        tags=concept.get('tags', [])
    )
```

## Best Practices

1. **Review daily** - Even 20 minutes maintains retention
2. **Be honest with confidence** - Accurate self-assessment improves the algorithm
3. **Don't skip due cards** - Spaced repetition works best with consistency
4. **Target weak topics weekly** - Use analytics to identify gaps
5. **Mix subjects** - Interleaving improves long-term retention
6. **Trust the algorithm** - SM-2 is scientifically validated

## Performance Targets

For bar exam readiness:

- **Mastery**: 80%+ of cards at repetition ≥ 5
- **Accuracy**: 75%+ overall, 70%+ on hard topics
- **Confidence Calibration**: High confidence accuracy ≥ 85%
- **Coverage**: All subjects reviewed within 14 days
- **Volume**: 30-50 cards reviewed per day

## Database Management

```python
# Backup your database
import shutil
shutil.copy("my_bar_prep.db", "my_bar_prep_backup.db")

# View database statistics
stats = system.get_statistics()

# Close connection properly
system.close()
```

## Combining with Other Learning Tools

This system complements:
- **Practice exams** - Identify weak topics, then drill them
- **Outlines** - Convert outline sections into cards
- **Lectures** - Create cards from lecture notes
- **Bar prep courses** - Reinforce course material with spaced repetition

## System Architecture

```
AdaptiveLearningSystem
├── AdaptiveLearningDatabase (SQLite)
│   ├── Cards table
│   ├── Performance table
│   └── Sessions table
│
├── AdaptiveBlockGenerator
│   ├── Performance analysis
│   ├── Difficulty adjustment
│   └── Priority scoring
│
└── LearningCard (with SM-2)
    ├── review() method
    └── confidence_weighting()
```

## Troubleshooting

**Q: Cards not appearing in blocks?**
A: Check if they're due with `card.is_due()` and `card.next_review`

**Q: Performance not tracking?**
A: Ensure you call `system.review_card()` after each review

**Q: Want to reset a card?**
A: Set `card.repetitions = 0` and `card.interval = 1`

**Q: Database locked error?**
A: Call `system.close()` before restarting

## License

Part of the Iowa Bar Prep Study Aid system.

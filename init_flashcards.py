#!/usr/bin/env python3
"""
Initialize iowa_bar_prep.db with flashcards from knowledge base JSON files
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path


def create_database(db_path: str = "iowa_bar_prep.db"):
    """Create database with schema"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Flashcards table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_id TEXT UNIQUE NOT NULL,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            front TEXT NOT NULL,
            back TEXT NOT NULL,
            ease_factor REAL DEFAULT 2.5,
            interval_days INTEGER DEFAULT 1,
            repetitions INTEGER DEFAULT 0,
            due_date TEXT NOT NULL,
            created_date TEXT NOT NULL,
            last_reviewed TEXT
        )
    """)

    # Study sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_date TEXT NOT NULL,
            cards_reviewed INTEGER NOT NULL,
            correct_count INTEGER NOT NULL,
            average_confidence REAL NOT NULL,
            duration_minutes INTEGER,
            completed INTEGER DEFAULT 1
        )
    """)

    # Review history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS review_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER NOT NULL,
            review_date TEXT NOT NULL,
            correct INTEGER NOT NULL,
            confidence INTEGER NOT NULL,
            quality_score INTEGER NOT NULL,
            FOREIGN KEY (card_id) REFERENCES flashcards(id)
        )
    """)

    conn.commit()
    return conn


def load_concepts_from_json():
    """Load concepts from available JSON files"""
    concepts = []
    json_files = [
        'ultimate_knowledge_base.json',
        'comprehensive_knowledge_base.json',
        'essay_subjects.json',
        'mbe_full_expansion.json'
    ]

    for json_file in json_files:
        if Path(json_file).exists():
            print(f"Loading {json_file}...")
            with open(json_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    concepts.extend(data)
                    print(f"  ✅ Loaded {len(data)} concepts")
                elif isinstance(data, dict) and 'concepts' in data:
                    concepts.extend(data['concepts'])
                    print(f"  ✅ Loaded {len(data['concepts'])} concepts")

    return concepts


def create_flashcards(concepts):
    """Generate flashcards from concepts"""
    flashcards = []

    for concept in concepts:
        concept_id = concept.get('concept_id', '')
        name = concept.get('name', 'Unknown')
        subject = concept.get('subject', 'General')
        rule_statement = concept.get('rule_statement', '')
        elements = concept.get('elements', [])
        common_traps = concept.get('common_traps', [])

        # Rule card
        if rule_statement:
            flashcards.append({
                'concept_id': f"{concept_id}_rule",
                'subject': subject,
                'topic': name,
                'front': f"State the rule for: {name}",
                'back': rule_statement
            })

        # Elements card
        if elements:
            elements_text = "\n".join(f"{i}. {elem}" for i, elem in enumerate(elements, 1))
            flashcards.append({
                'concept_id': f"{concept_id}_elements",
                'subject': subject,
                'topic': name,
                'front': f"What are the elements of {name}?",
                'back': elements_text
            })

        # Traps card
        if common_traps:
            traps_text = "\n".join(f"⚠️ {trap}" for trap in common_traps)
            flashcards.append({
                'concept_id': f"{concept_id}_traps",
                'subject': subject,
                'topic': name,
                'front': f"What are common exam traps for {name}?",
                'back': traps_text
            })

    return flashcards


def populate_database(conn, flashcards):
    """Insert flashcards into database"""
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    added = 0
    for card in flashcards:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO flashcards
                (concept_id, subject, topic, front, back, due_date, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                card['concept_id'],
                card['subject'],
                card['topic'],
                card['front'],
                card['back'],
                now,
                now
            ))
            if cursor.rowcount > 0:
                added += 1
        except Exception as e:
            print(f"  ⚠️  Error adding card {card['concept_id']}: {e}")

    conn.commit()
    return added


def main():
    print("=" * 70)
    print("IOWA BAR PREP - FLASHCARD DATABASE INITIALIZATION")
    print("=" * 70)
    print()

    # Create database
    print("Creating database...")
    conn = create_database()
    print("✅ Database created")
    print()

    # Load concepts
    print("Loading concepts from JSON files...")
    concepts = load_concepts_from_json()
    print(f"✅ Total concepts loaded: {len(concepts)}")
    print()

    # Generate flashcards
    print("Generating flashcards...")
    flashcards = create_flashcards(concepts)
    print(f"✅ Generated {len(flashcards)} flashcards")
    print()

    # Populate database
    print("Populating database...")
    added = populate_database(conn, flashcards)
    print(f"✅ Added {added} flashcards to database")
    print()

    # Show stats
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT subject) FROM flashcards")
    subjects = cursor.fetchone()[0]

    cursor.execute("SELECT subject, COUNT(*) FROM flashcards GROUP BY subject ORDER BY COUNT(*) DESC LIMIT 5")
    top_subjects = cursor.fetchall()

    print("📊 Database Statistics:")
    print(f"  Total flashcards: {added}")
    print(f"  Subjects covered: {subjects}")
    print()
    print("  Top subjects:")
    for subj, count in top_subjects:
        print(f"    • {subj}: {count} cards")

    conn.close()
    print()
    print("=" * 70)
    print("✅ INITIALIZATION COMPLETE!")
    print("=" * 70)
    print()
    print("Next step: Run ./daily_study.py to start your review session")


if __name__ == "__main__":
    main()

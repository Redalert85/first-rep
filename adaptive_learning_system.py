#!/usr/bin/env python3
"""
Adaptive Learning System with SQLite Database
Spaced repetition system using SuperMemo SM-2 algorithm
"""

import sqlite3
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass


class Subject(Enum):
    """Bar exam subjects"""
    # MBE Subjects
    CIVIL_PROCEDURE = "civil_procedure"
    CONSTITUTIONAL_LAW = "constitutional_law"
    CONTRACTS = "contracts"
    CRIMINAL_LAW = "criminal_law"
    CRIMINAL_PROCEDURE = "criminal_procedure"
    EVIDENCE = "evidence"
    REAL_PROPERTY = "real_property"
    TORTS = "torts"

    # Essay Subjects
    PROFESSIONAL_RESPONSIBILITY = "professional_responsibility"
    CORPORATIONS = "corporations"
    WILLS_TRUSTS_ESTATES = "wills_trusts_estates"
    FAMILY_LAW = "family_law"
    SECURED_TRANSACTIONS = "secured_transactions"
    IOWA_PROCEDURE = "iowa_procedure"


@dataclass
class Card:
    """Flashcard with SM-2 algorithm data"""
    card_id: Optional[int]
    concept_id: str
    subject: str
    front: str
    back: str

    # SM-2 algorithm fields
    ease_factor: float = 2.5
    interval: int = 1
    repetitions: int = 0
    next_review: str = ""
    last_reviewed: Optional[str] = None

    # Performance tracking
    correct_count: int = 0
    incorrect_count: int = 0

    created_at: Optional[str] = None

    def __post_init__(self):
        if not self.next_review:
            self.next_review = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class AdaptiveLearningSystem:
    """SQLite-based adaptive learning system"""

    def __init__(self, db_path: str = 'iowa_bar_prep.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Create database schema"""
        cursor = self.conn.cursor()

        # Cards table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                card_id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                ease_factor REAL DEFAULT 2.5,
                interval INTEGER DEFAULT 1,
                repetitions INTEGER DEFAULT 0,
                next_review TEXT NOT NULL,
                last_reviewed TEXT,
                correct_count INTEGER DEFAULT 0,
                incorrect_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        ''')

        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_subject ON cards(subject)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_next_review ON cards(next_review)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_concept_id ON cards(concept_id)')

        self.conn.commit()

    def add_card(self, card: Card) -> int:
        """Add a card to the database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO cards (
                concept_id, subject, front, back, ease_factor, interval,
                repetitions, next_review, last_reviewed, correct_count,
                incorrect_count, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            card.concept_id, card.subject, card.front, card.back,
            card.ease_factor, card.interval, card.repetitions,
            card.next_review, card.last_reviewed, card.correct_count,
            card.incorrect_count, card.created_at
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        cursor = self.conn.cursor()

        # Total cards
        cursor.execute('SELECT COUNT(*) as count FROM cards')
        total_cards = cursor.fetchone()['count']

        # Due cards (cards with next_review <= now)
        now = datetime.now().isoformat()
        cursor.execute('SELECT COUNT(*) as count FROM cards WHERE next_review <= ?', (now,))
        due_cards = cursor.fetchone()['count']

        # Mastered cards (repetitions >= 5 and ease_factor >= 2.5)
        cursor.execute('''
            SELECT COUNT(*) as count FROM cards
            WHERE repetitions >= 5 AND ease_factor >= 2.5
        ''')
        mastered_cards = cursor.fetchone()['count']

        # Cards by subject
        cursor.execute('''
            SELECT subject, COUNT(*) as count
            FROM cards
            GROUP BY subject
            ORDER BY subject
        ''')
        cards_by_subject = {row['subject']: row['count'] for row in cursor.fetchall()}

        return {
            'total_cards': total_cards,
            'due_cards': due_cards,
            'mastered_cards': mastered_cards,
            'cards_by_subject': cards_by_subject
        }

    def get_due_cards(self, limit: int = 20) -> List[Card]:
        """Get cards due for review"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()

        cursor.execute('''
            SELECT * FROM cards
            WHERE next_review <= ?
            ORDER BY next_review
            LIMIT ?
        ''', (now, limit))

        cards = []
        for row in cursor.fetchall():
            card = Card(
                card_id=row['card_id'],
                concept_id=row['concept_id'],
                subject=row['subject'],
                front=row['front'],
                back=row['back'],
                ease_factor=row['ease_factor'],
                interval=row['interval'],
                repetitions=row['repetitions'],
                next_review=row['next_review'],
                last_reviewed=row['last_reviewed'],
                correct_count=row['correct_count'],
                incorrect_count=row['incorrect_count'],
                created_at=row['created_at']
            )
            cards.append(card)

        return cards

    def review_card(self, card_id: int, quality: int):
        """
        Update card after review using SM-2 algorithm
        quality: 0-5 (0-2 fail, 3-5 pass)
        """
        cursor = self.conn.cursor()

        # Get current card data
        cursor.execute('SELECT * FROM cards WHERE card_id = ?', (card_id,))
        row = cursor.fetchone()

        ease_factor = row['ease_factor']
        interval = row['interval']
        repetitions = row['repetitions']
        correct = row['correct_count']
        incorrect = row['incorrect_count']

        # Update performance counters
        if quality >= 3:
            correct += 1
        else:
            incorrect += 1

        # SM-2 algorithm
        if quality < 3:
            # Failed - reset
            repetitions = 0
            interval = 1
        else:
            # Passed - calculate new interval
            if repetitions == 0:
                interval = 1
            elif repetitions == 1:
                interval = 6
            else:
                interval = int(interval * ease_factor)

            repetitions += 1

            # Update ease factor
            ease_factor = max(1.3, ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        # Calculate next review date
        next_review = (datetime.now() + timedelta(days=interval)).isoformat()
        last_reviewed = datetime.now().isoformat()

        # Update database
        cursor.execute('''
            UPDATE cards
            SET ease_factor = ?, interval = ?, repetitions = ?,
                next_review = ?, last_reviewed = ?,
                correct_count = ?, incorrect_count = ?
            WHERE card_id = ?
        ''', (ease_factor, interval, repetitions, next_review, last_reviewed,
              correct, incorrect, card_id))

        self.conn.commit()

    def get_cards_by_subject(self, subject: str) -> List[Card]:
        """Get all cards for a subject"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM cards WHERE subject = ?', (subject,))

        cards = []
        for row in cursor.fetchall():
            card = Card(
                card_id=row['card_id'],
                concept_id=row['concept_id'],
                subject=row['subject'],
                front=row['front'],
                back=row['back'],
                ease_factor=row['ease_factor'],
                interval=row['interval'],
                repetitions=row['repetitions'],
                next_review=row['next_review'],
                last_reviewed=row['last_reviewed'],
                correct_count=row['correct_count'],
                incorrect_count=row['incorrect_count'],
                created_at=row['created_at']
            )
            cards.append(card)

        return cards

    def clear_all_cards(self):
        """Clear all cards from database"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM cards')
        self.conn.commit()

    def close(self):
        """Close database connection"""
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    # Test the system
    system = AdaptiveLearningSystem()
    stats = system.get_statistics()
    print("Database initialized successfully")
    print(f"Total cards: {stats['total_cards']}")
    system.close()

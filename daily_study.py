#!/usr/bin/env python3
"""
Interactive Daily Study Session
Adaptive spaced repetition system for Iowa Bar Prep
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from dataclasses import dataclass
import random


@dataclass
class Card:
    """Flashcard with spaced repetition data"""
    card_id: int
    concept_id: str
    subject: str
    question: str
    answer: str
    ease_factor: float
    interval: int
    repetitions: int
    next_review: str
    total_attempts: int
    correct_attempts: int
    last_confidence: int

    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage"""
        if self.total_attempts == 0:
            return 0.0
        return (self.correct_attempts / self.total_attempts) * 100

    @property
    def is_weak(self) -> bool:
        """Check if this is a weak area (< 70% accuracy)"""
        return self.total_attempts >= 2 and self.accuracy < 70

    @property
    def is_new(self) -> bool:
        """Check if this is a new card"""
        return self.total_attempts == 0

    @property
    def is_overdue(self) -> bool:
        """Check if this card is overdue for review"""
        return datetime.fromisoformat(self.next_review) < datetime.now()


class DailyStudySession:
    """Manages interactive daily study sessions"""

    def __init__(self, db_path: str = "iowa_bar_prep.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.initialize_database()

    def initialize_database(self):
        """Create database schema if it doesn't exist"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                card_id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                ease_factor REAL DEFAULT 2.5,
                interval INTEGER DEFAULT 1,
                repetitions INTEGER DEFAULT 0,
                next_review TEXT NOT NULL,
                total_attempts INTEGER DEFAULT 0,
                correct_attempts INTEGER DEFAULT 0,
                last_confidence INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                UNIQUE(concept_id, question)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id INTEGER NOT NULL,
                attempted_at TEXT NOT NULL,
                was_correct INTEGER NOT NULL,
                confidence INTEGER NOT NULL,
                time_taken INTEGER,
                FOREIGN KEY(card_id) REFERENCES cards(card_id)
            )
        """)

        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_next_review
            ON cards(next_review)
        """)

        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_subject
            ON cards(subject)
        """)

        self.conn.commit()

    def import_cards_from_knowledge_base(self):
        """Import cards from the bar prep knowledge base"""
        try:
            from bar_tutor_unified import LegalKnowledgeGraph

            kg = LegalKnowledgeGraph()
            imported = 0

            for concept_id, concept in kg.nodes.items():
                # Rule statement card
                self.add_card(
                    concept_id=f"{concept_id}_rule",
                    subject=getattr(concept, 'subject', 'General'),
                    question=f"State the rule for: {concept.name}",
                    answer=concept.rule_statement
                )
                imported += 1

                # Elements card
                if concept.elements:
                    elements_text = "\n".join(
                        f"{i}. {elem}" for i, elem in enumerate(concept.elements, 1)
                    )
                    self.add_card(
                        concept_id=f"{concept_id}_elements",
                        subject=getattr(concept, 'subject', 'General'),
                        question=f"What are the elements of {concept.name}?",
                        answer=elements_text
                    )
                    imported += 1

                # Common traps card
                if concept.common_traps:
                    traps_text = "\n".join(
                        f"⚠️  {trap}" for trap in concept.common_traps
                    )
                    self.add_card(
                        concept_id=f"{concept_id}_traps",
                        subject=getattr(concept, 'subject', 'General'),
                        question=f"What are common exam traps for {concept.name}?",
                        answer=traps_text
                    )
                    imported += 1

            self.conn.commit()
            return imported

        except Exception as e:
            print(f"Warning: Could not import from knowledge base: {e}")
            return 0

    def add_card(self, concept_id: str, subject: str, question: str, answer: str):
        """Add a new card to the database"""
        now = datetime.now().isoformat()

        self.cursor.execute("""
            INSERT OR IGNORE INTO cards
            (concept_id, subject, question, answer, next_review, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (concept_id, subject, question, answer, now, now))

    def get_statistics(self) -> dict:
        """Get current study statistics"""
        # Total cards
        self.cursor.execute("SELECT COUNT(*) FROM cards")
        total_cards = self.cursor.fetchone()[0]

        # Due cards
        now = datetime.now().isoformat()
        self.cursor.execute(
            "SELECT COUNT(*) FROM cards WHERE next_review <= ?", (now,)
        )
        due_cards = self.cursor.fetchone()[0]

        # Mastered cards (5+ repetitions, 2.5+ ease factor)
        self.cursor.execute("""
            SELECT COUNT(*) FROM cards
            WHERE repetitions >= 5 AND ease_factor >= 2.5
        """)
        mastered_cards = self.cursor.fetchone()[0]

        # Weak areas (< 70% accuracy with 2+ attempts)
        self.cursor.execute("""
            SELECT COUNT(*) FROM cards
            WHERE total_attempts >= 2
            AND (correct_attempts * 100.0 / total_attempts) < 70
        """)
        weak_cards = self.cursor.fetchone()[0]

        # New cards (never reviewed)
        self.cursor.execute(
            "SELECT COUNT(*) FROM cards WHERE total_attempts = 0"
        )
        new_cards = self.cursor.fetchone()[0]

        # Today's performance
        today = datetime.now().date().isoformat()
        self.cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(was_correct) as correct,
                AVG(confidence) as avg_confidence
            FROM attempts
            WHERE DATE(attempted_at) = ?
        """, (today,))

        row = self.cursor.fetchone()
        today_attempts = row['total'] or 0
        today_correct = row['correct'] or 0
        today_confidence = row['avg_confidence'] or 0

        return {
            'total_cards': total_cards,
            'due_cards': due_cards,
            'mastered_cards': mastered_cards,
            'weak_cards': weak_cards,
            'new_cards': new_cards,
            'today_attempts': today_attempts,
            'today_correct': today_correct,
            'today_accuracy': (today_correct / today_attempts * 100) if today_attempts > 0 else 0,
            'today_confidence': today_confidence
        }

    def display_statistics(self):
        """Display today's statistics"""
        stats = self.get_statistics()

        print("\n" + "="*70)
        print("📊 TODAY'S STATISTICS")
        print("="*70)
        print(f"Total Cards:        {stats['total_cards']}")
        print(f"Due for Review:     {stats['due_cards']}")
        print(f"Mastered:           {stats['mastered_cards']} ({stats['mastered_cards']/max(stats['total_cards'],1)*100:.1f}%)")
        print(f"Weak Areas:         {stats['weak_cards']}")
        print(f"New Cards:          {stats['new_cards']}")
        print()
        print(f"Today's Progress:   {stats['today_attempts']} cards reviewed")
        if stats['today_attempts'] > 0:
            print(f"Today's Accuracy:   {stats['today_accuracy']:.1f}%")
            print(f"Avg Confidence:     {stats['today_confidence']:.1f}/5")
        print("="*70)

    def get_adaptive_card_set(self, target_size: int = 25) -> List[Card]:
        """
        Generate adaptive card selection prioritizing:
        1. Overdue reviews
        2. Weak areas (< 70% accuracy)
        3. New cards
        """
        cards = []
        card_ids_seen = set()
        now = datetime.now().isoformat()

        # 1. Get overdue cards (50% of set, minimum 1 if any exist)
        overdue_limit = max(1, int(target_size * 0.5))
        self.cursor.execute("""
            SELECT * FROM cards
            WHERE next_review <= ?
            AND total_attempts > 0
            ORDER BY next_review ASC
            LIMIT ?
        """, (now, overdue_limit))

        for row in self.cursor.fetchall():
            card = self._row_to_card(row)
            cards.append(card)
            card_ids_seen.add(card.card_id)

        # 2. Get weak area cards (30% of set, minimum 1 if any exist)
        weak_limit = max(1, int(target_size * 0.3))
        self.cursor.execute("""
            SELECT * FROM cards
            WHERE total_attempts >= 2
            AND (correct_attempts * 100.0 / total_attempts) < 70
            ORDER BY (correct_attempts * 1.0 / total_attempts), RANDOM()
            LIMIT ?
        """, (weak_limit,))

        for row in self.cursor.fetchall():
            card = self._row_to_card(row)
            if card.card_id not in card_ids_seen:
                cards.append(card)
                card_ids_seen.add(card.card_id)

        # 3. Get new cards (fill remaining slots)
        remaining = target_size - len(cards)
        if remaining > 0:
            self.cursor.execute("""
                SELECT * FROM cards
                WHERE total_attempts = 0
                ORDER BY RANDOM()
                LIMIT ?
            """, (remaining,))

            for row in self.cursor.fetchall():
                card = self._row_to_card(row)
                if card.card_id not in card_ids_seen:
                    cards.append(card)
                    card_ids_seen.add(card.card_id)

        # 4. If we still need more cards, get any remaining cards
        remaining = target_size - len(cards)
        if remaining > 0:
            self.cursor.execute("""
                SELECT * FROM cards
                ORDER BY RANDOM()
                LIMIT ?
            """, (remaining * 2,))  # Get extra to account for duplicates

            for row in self.cursor.fetchall():
                card = self._row_to_card(row)
                if card.card_id not in card_ids_seen:
                    cards.append(card)
                    card_ids_seen.add(card.card_id)
                    if len(cards) >= target_size:
                        break

        # Shuffle to avoid predictable patterns
        random.shuffle(cards)

        return cards[:target_size]

    def _row_to_card(self, row) -> Card:
        """Convert database row to Card object"""
        return Card(
            card_id=row['card_id'],
            concept_id=row['concept_id'],
            subject=row['subject'],
            question=row['question'],
            answer=row['answer'],
            ease_factor=row['ease_factor'],
            interval=row['interval'],
            repetitions=row['repetitions'],
            next_review=row['next_review'],
            total_attempts=row['total_attempts'],
            correct_attempts=row['correct_attempts'],
            last_confidence=row['last_confidence']
        )

    def review_card(self, card: Card, was_correct: bool, confidence: int):
        """
        Update card using SM-2 algorithm based on review result

        Args:
            card: The card being reviewed
            was_correct: Whether the user got it right
            confidence: User confidence rating (1-5)
        """
        # Convert to SM-2 quality score (0-5)
        if not was_correct:
            quality = 0  # Complete fail
        else:
            quality = confidence  # Use confidence as quality

        # SM-2 Algorithm
        if quality < 3:
            # Failed - reset
            card.repetitions = 0
            card.interval = 1
        else:
            # Passed - calculate new interval
            if card.repetitions == 0:
                card.interval = 1
            elif card.repetitions == 1:
                card.interval = 6
            else:
                card.interval = int(card.interval * card.ease_factor)

            card.repetitions += 1

            # Update ease factor
            card.ease_factor = max(
                1.3,
                card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            )

        # Set next review date
        next_date = datetime.now() + timedelta(days=card.interval)
        card.next_review = next_date.isoformat()

        # Update statistics
        card.total_attempts += 1
        if was_correct:
            card.correct_attempts += 1
        card.last_confidence = confidence

        # Save to database
        now = datetime.now().isoformat()

        self.cursor.execute("""
            UPDATE cards
            SET ease_factor = ?,
                interval = ?,
                repetitions = ?,
                next_review = ?,
                total_attempts = ?,
                correct_attempts = ?,
                last_confidence = ?
            WHERE card_id = ?
        """, (
            card.ease_factor, card.interval, card.repetitions,
            card.next_review, card.total_attempts, card.correct_attempts,
            card.last_confidence, card.card_id
        ))

        # Log attempt
        self.cursor.execute("""
            INSERT INTO attempts (card_id, attempted_at, was_correct, confidence)
            VALUES (?, ?, ?, ?)
        """, (card.card_id, now, 1 if was_correct else 0, confidence))

        self.conn.commit()

    def run_study_session(self, card_count: int = 25):
        """Run interactive study session"""
        print("\n" + "="*70)
        print("🎯 STARTING STUDY SESSION")
        print("="*70)

        cards = self.get_adaptive_card_set(card_count)

        if not cards:
            print("\n🎉 No cards available! You might need to import cards first.")
            print("Run: session.import_cards_from_knowledge_base()")
            return

        print(f"\nSession size: {len(cards)} cards")
        print("\nCard mix:")
        overdue = sum(1 for c in cards if c.is_overdue and not c.is_new)
        weak = sum(1 for c in cards if c.is_weak)
        new = sum(1 for c in cards if c.is_new)
        print(f"  • Overdue reviews: {overdue}")
        print(f"  • Weak areas:      {weak}")
        print(f"  • New cards:       {new}")

        input("\nPress Enter to begin...")

        session_start = datetime.now()
        session_correct = 0
        session_confidence = []

        for i, card in enumerate(cards, 1):
            print("\n" + "─"*70)
            print(f"Card {i}/{len(cards)}")

            # Show metadata
            if card.is_new:
                print("🆕 NEW CARD")
            elif card.is_overdue:
                days_overdue = (datetime.now() - datetime.fromisoformat(card.next_review)).days
                print(f"⏰ OVERDUE ({days_overdue} days)")
            if card.is_weak:
                print(f"⚠️  WEAK AREA ({card.accuracy:.0f}% accuracy)")

            print(f"Subject: {card.subject}")
            print()

            # Show question
            print("❓ QUESTION:")
            print(card.question)
            print()

            # Wait for user to think
            input("Press Enter to reveal answer...")
            print()

            # Show answer
            print("💡 ANSWER:")
            print(card.answer)
            print()

            # Get user feedback
            while True:
                response = input("Did you get it right? (y/n): ").strip().lower()
                if response in ['y', 'n']:
                    was_correct = (response == 'y')
                    break
                print("Please enter 'y' or 'n'")

            while True:
                try:
                    confidence = int(input("Confidence (1-5): ").strip())
                    if 1 <= confidence <= 5:
                        break
                    print("Please enter a number between 1 and 5")
                except ValueError:
                    print("Please enter a valid number")

            # Update card
            self.review_card(card, was_correct, confidence)

            if was_correct:
                session_correct += 1
            session_confidence.append(confidence)

            # Show brief feedback
            if was_correct:
                print("✅ Correct!")
            else:
                print("❌ Review this concept")

            print(f"Next review: {card.interval} days")

        # Session complete
        session_duration = (datetime.now() - session_start).seconds

        print("\n" + "="*70)
        print("🎉 SESSION COMPLETE!")
        print("="*70)

        session_accuracy = (session_correct / len(cards)) * 100
        avg_confidence = sum(session_confidence) / len(session_confidence)

        print(f"\nSession Statistics:")
        print(f"  Cards reviewed:     {len(cards)}")
        print(f"  Correct:            {session_correct}/{len(cards)} ({session_accuracy:.1f}%)")
        print(f"  Average confidence: {avg_confidence:.1f}/5")
        print(f"  Time taken:         {session_duration // 60}m {session_duration % 60}s")

        # Show tomorrow's preview
        self.show_tomorrow_preview()

    def show_tomorrow_preview(self):
        """Show preview of tomorrow's due cards"""
        tomorrow = (datetime.now() + timedelta(days=1)).isoformat()

        self.cursor.execute("""
            SELECT COUNT(*) FROM cards
            WHERE next_review <= ?
        """, (tomorrow,))

        tomorrow_due = self.cursor.fetchone()[0]

        # Get subject breakdown
        self.cursor.execute("""
            SELECT subject, COUNT(*) as count
            FROM cards
            WHERE next_review <= ?
            GROUP BY subject
            ORDER BY count DESC
            LIMIT 5
        """, (tomorrow,))

        subjects = self.cursor.fetchall()

        print("\n" + "="*70)
        print("📅 TOMORROW'S PREVIEW")
        print("="*70)
        print(f"Cards due tomorrow: {tomorrow_due}")

        if subjects:
            print("\nBy subject:")
            for row in subjects:
                print(f"  • {row['subject']}: {row['count']} cards")

        print("\n💪 Keep up the great work!")
        print("="*70)

    def close(self):
        """Close database connection"""
        self.conn.close()


def main():
    """Run daily study session"""
    print("="*70)
    print("🎓 IOWA BAR PREP - DAILY STUDY SESSION")
    print("="*70)

    session = DailyStudySession()

    # Check if database is empty
    stats = session.get_statistics()
    if stats['total_cards'] == 0:
        print("\n📦 Database is empty. Importing cards from knowledge base...")
        imported = session.import_cards_from_knowledge_base()
        if imported > 0:
            print(f"✅ Imported {imported} cards!")
        else:
            print("\n⚠️  Warning: Could not import cards.")
            print("Make sure bar_tutor_unified.py is available.")
            session.close()
            return

    # Show statistics
    session.display_statistics()

    # Run study session
    try:
        session.run_study_session(card_count=25)
    except KeyboardInterrupt:
        print("\n\n⚠️  Session interrupted. Progress has been saved.")
    finally:
        session.close()


if __name__ == "__main__":
    main()

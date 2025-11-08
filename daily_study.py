#!/usr/bin/env python3
"""
Interactive Flashcard Review Session for Iowa Bar Prep
Uses SM-2 spaced repetition algorithm with SQLite database
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


class FlashcardDatabase:
    """Manages SQLite database for flashcards and study sessions"""

    def __init__(self, db_path: str = "iowa_bar_prep.db"):
        self.db_path = db_path
        self.conn = None
        self.initialize_database()

    def initialize_database(self):
        """Create database tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()

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

        self.conn.commit()

    def populate_from_knowledge_base(self):
        """Check if database is populated; if not, suggest running init script"""
        cursor = self.conn.cursor()

        # Check if database is already populated
        cursor.execute("SELECT COUNT(*) FROM flashcards")
        count = cursor.fetchone()[0]
        return count


    def get_due_cards(self, limit: int = 30) -> List[Dict]:
        """Get cards due for review, prioritizing overdue cards"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()

        cursor.execute("""
            SELECT * FROM flashcards
            WHERE due_date <= ?
            ORDER BY due_date ASC, repetitions ASC
            LIMIT ?
        """, (now, limit))

        return [dict(row) for row in cursor.fetchall()]

    def update_card_after_review(self, card_id: int, correct: bool, confidence: int):
        """Update card using SM-2 algorithm"""
        # Calculate quality score (0-5) based on correctness and confidence
        if correct:
            quality = min(5, 3 + (confidence // 2))  # 3-5 for correct answers
        else:
            quality = min(2, confidence // 2)  # 0-2 for incorrect answers

        cursor = self.conn.cursor()

        # Get current card data
        cursor.execute("SELECT * FROM flashcards WHERE id = ?", (card_id,))
        card = dict(cursor.fetchone())

        # SM-2 Algorithm
        ease_factor = card['ease_factor']
        interval = card['interval_days']
        repetitions = card['repetitions']

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
        due_date = (datetime.now() + timedelta(days=interval)).isoformat()
        now = datetime.now().isoformat()

        # Update card
        cursor.execute("""
            UPDATE flashcards
            SET ease_factor = ?,
                interval_days = ?,
                repetitions = ?,
                due_date = ?,
                last_reviewed = ?
            WHERE id = ?
        """, (ease_factor, interval, repetitions, due_date, now, card_id))

        # Log review
        cursor.execute("""
            INSERT INTO review_history (card_id, review_date, correct, confidence, quality_score)
            VALUES (?, ?, ?, ?, ?)
        """, (card_id, now, 1 if correct else 0, confidence, quality))

        self.conn.commit()

        return interval

    def log_session(self, cards_reviewed: int, correct_count: int,
                   avg_confidence: float, duration_minutes: int = 0):
        """Log completed study session"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO study_sessions
            (session_date, cards_reviewed, correct_count, average_confidence, duration_minutes)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), cards_reviewed, correct_count, avg_confidence, duration_minutes))
        self.conn.commit()

    def get_cards_due_tomorrow(self) -> int:
        """Get count of cards due tomorrow"""
        cursor = self.conn.cursor()
        tomorrow = (datetime.now() + timedelta(days=1)).isoformat()
        cursor.execute("""
            SELECT COUNT(*) FROM flashcards
            WHERE due_date <= ?
        """, (tomorrow,))
        return cursor.fetchone()[0]

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class FlashcardSession:
    """Interactive flashcard review session"""

    def __init__(self, db: FlashcardDatabase):
        self.db = db
        self.session_start = datetime.now()
        self.cards_reviewed = 0
        self.correct_count = 0
        self.confidence_scores = []

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def run_session(self, num_cards: int = 30):
        """Run interactive review session"""
        self.clear_screen()
        print("=" * 70)
        print("IOWA BAR PREP - FLASHCARD REVIEW SESSION")
        print("=" * 70)
        print()

        # Get due cards
        cards = self.db.get_due_cards(num_cards)

        if not cards:
            print("🎉 No cards due! You're all caught up!")
            print()
            print(f"Cards due tomorrow: {self.db.get_cards_due_tomorrow()}")
            return

        total_cards = len(cards)
        print(f"📚 {total_cards} cards ready for review")
        print()
        print("Instructions:")
        print("  • Think through your answer before pressing Enter")
        print("  • Rate yourself honestly")
        print("  • Type 'q' at any prompt to quit early")
        print()
        input("Press Enter to begin...")

        for i, card in enumerate(cards, 1):
            self.clear_screen()

            # Show progress
            print(f"Card {i}/{total_cards}")
            print(f"Subject: {card['subject']}")
            print(f"Topic: {card['topic']}")
            print("-" * 70)
            print()

            # Show question
            print("QUESTION:")
            print(card['front'])
            print()

            # Wait for user
            user_input = input("Press Enter to reveal answer (or 'q' to quit): ").strip().lower()
            if user_input == 'q':
                self._handle_early_quit()
                return

            # Show answer
            print()
            print("ANSWER:")
            print(card['back'])
            print()
            print("-" * 70)

            # Get correctness
            while True:
                correct_input = input("Did you get it right? (y/n): ").strip().lower()
                if correct_input == 'q':
                    self._handle_early_quit()
                    return
                if correct_input in ['y', 'n']:
                    correct = (correct_input == 'y')
                    break
                print("Please enter 'y' or 'n'")

            # Get confidence
            while True:
                try:
                    conf_input = input("Confidence (0=guess, 1=unsure, 2=fairly sure, 3=sure, 4=certain): ").strip()
                    if conf_input.lower() == 'q':
                        self._handle_early_quit()
                        return
                    confidence = int(conf_input)
                    if 0 <= confidence <= 4:
                        break
                    print("Please enter a number between 0 and 4")
                except ValueError:
                    print("Please enter a valid number")

            # Update card
            interval = self.db.update_card_after_review(card['id'], correct, confidence)

            # Track stats
            self.cards_reviewed += 1
            if correct:
                self.correct_count += 1
            self.confidence_scores.append(confidence)

            # Show feedback
            print()
            if correct:
                print(f"✅ Correct! Next review in {interval} day{'s' if interval != 1 else ''}")
            else:
                print(f"📝 Review again in {interval} day{'s' if interval != 1 else ''}")
            print()

            if i < total_cards:
                input("Press Enter for next card...")

        # Show session summary
        self._show_summary()

    def _handle_early_quit(self):
        """Handle user quitting early"""
        print()
        print("Session ended early.")
        if self.cards_reviewed > 0:
            self._show_summary()
        else:
            print("No cards were reviewed.")

    def _show_summary(self):
        """Show session summary"""
        self.clear_screen()
        print("=" * 70)
        print("SESSION SUMMARY")
        print("=" * 70)
        print()

        # Calculate stats
        accuracy = (self.correct_count / self.cards_reviewed * 100) if self.cards_reviewed > 0 else 0
        avg_confidence = sum(self.confidence_scores) / len(self.confidence_scores) if self.confidence_scores else 0
        duration = (datetime.now() - self.session_start).seconds // 60

        # Display stats
        print(f"📊 Cards Reviewed: {self.cards_reviewed}")
        print(f"✅ Correct: {self.correct_count}/{self.cards_reviewed} ({accuracy:.1f}%)")
        print(f"🎯 Average Confidence: {avg_confidence:.1f}/4")
        print(f"⏱️  Duration: {duration} minutes")
        print()

        # Cards due tomorrow
        tomorrow_count = self.db.get_cards_due_tomorrow()
        print(f"📅 Cards due tomorrow: {tomorrow_count}")
        print()

        # Performance feedback
        if accuracy >= 90:
            print("🌟 Excellent work! You're mastering the material!")
        elif accuracy >= 75:
            print("👍 Good job! Keep up the consistent practice!")
        elif accuracy >= 60:
            print("📚 Making progress! Consider reviewing weak areas!")
        else:
            print("💪 Keep practicing! Consistency is key!")

        print()

        # Log session
        self.db.log_session(self.cards_reviewed, self.correct_count, avg_confidence, duration)
        print("✅ Session logged successfully!")
        print("=" * 70)


def main():
    """Main entry point"""
    try:
        # Initialize database
        db = FlashcardDatabase()

        # Check if database is populated
        card_count = db.populate_from_knowledge_base()
        if card_count == 0:
            print("=" * 70)
            print("DATABASE NOT INITIALIZED")
            print("=" * 70)
            print()
            print("The flashcard database is empty.")
            print("Please run the initialization script first:")
            print()
            print("  python3 init_flashcards.py")
            print()
            print("This will populate the database with flashcards from your")
            print("knowledge base JSON files.")
            print("=" * 70)
            db.close()
            sys.exit(1)

        # Run session
        session = FlashcardSession(db)
        session.run_session(num_cards=30)

        # Cleanup
        db.close()

    except KeyboardInterrupt:
        print("\n\nSession interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

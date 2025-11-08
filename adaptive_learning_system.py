#!/usr/bin/env python3
"""
Adaptive Learning System with SM-2 Spaced Repetition Algorithm
Supports Iowa Bar Prep with 14 subjects and detailed topic tracking
"""

import sqlite3
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict, Any
import json


# ==================== ENUMS ====================

class Subject(Enum):
    """8 MBE Subjects + 6 Iowa Essay Subjects"""
    # MBE Subjects
    CONTRACTS = "contracts"
    TORTS = "torts"
    CONSTITUTIONAL_LAW = "constitutional_law"
    CRIMINAL_LAW = "criminal_law"
    CRIMINAL_PROCEDURE = "criminal_procedure"
    CIVIL_PROCEDURE = "civil_procedure"
    EVIDENCE = "evidence"
    REAL_PROPERTY = "real_property"

    # Iowa Essay Subjects
    PROFESSIONAL_RESPONSIBILITY = "professional_responsibility"
    CORPORATIONS = "corporations"
    WILLS_TRUSTS_ESTATES = "wills_trusts_estates"
    FAMILY_LAW = "family_law"
    SECURED_TRANSACTIONS = "secured_transactions"
    IOWA_PROCEDURE = "iowa_procedure"


class ConstitutionalLawTopic(Enum):
    """35 Constitutional Law Topics"""
    JUDICIAL_REVIEW = "judicial_review"
    JUSTICIABILITY = "justiciability"
    STANDING = "standing"
    RIPENESS = "ripeness"
    MOOTNESS = "mootness"
    POLITICAL_QUESTION = "political_question"
    FEDERALISM = "federalism"
    COMMERCE_CLAUSE = "commerce_clause"
    TAXING_SPENDING_POWER = "taxing_spending_power"
    NECESSARY_AND_PROPER = "necessary_and_proper"
    TENTH_AMENDMENT = "tenth_amendment"
    ELEVENTH_AMENDMENT = "eleventh_amendment"
    SUPREMACY_CLAUSE = "supremacy_clause"
    DORMANT_COMMERCE_CLAUSE = "dormant_commerce_clause"
    PRIVILEGES_AND_IMMUNITIES = "privileges_and_immunities"
    EXECUTIVE_POWER = "executive_power"
    LEGISLATIVE_POWER = "legislative_power"
    SEPARATION_OF_POWERS = "separation_of_powers"
    FREEDOM_OF_SPEECH = "freedom_of_speech"
    FREEDOM_OF_RELIGION = "freedom_of_religion"
    ESTABLISHMENT_CLAUSE = "establishment_clause"
    FREE_EXERCISE_CLAUSE = "free_exercise_clause"
    FREEDOM_OF_PRESS = "freedom_of_press"
    FREEDOM_OF_ASSEMBLY = "freedom_of_assembly"
    FREEDOM_OF_ASSOCIATION = "freedom_of_association"
    DUE_PROCESS_SUBSTANTIVE = "due_process_substantive"
    DUE_PROCESS_PROCEDURAL = "due_process_procedural"
    EQUAL_PROTECTION = "equal_protection"
    STRICT_SCRUTINY = "strict_scrutiny"
    INTERMEDIATE_SCRUTINY = "intermediate_scrutiny"
    RATIONAL_BASIS = "rational_basis"
    FUNDAMENTAL_RIGHTS = "fundamental_rights"
    TAKINGS_CLAUSE = "takings_clause"
    STATE_ACTION = "state_action"
    GENERAL = "general"


class EvidenceTopic(Enum):
    """50+ Evidence Topics"""
    RELEVANCE = "relevance"
    LOGICAL_RELEVANCE = "logical_relevance"
    LEGAL_RELEVANCE = "legal_relevance"
    UNFAIR_PREJUDICE = "unfair_prejudice"
    CHARACTER_EVIDENCE = "character_evidence"
    PROPENSITY_EVIDENCE = "propensity_evidence"
    HABIT_EVIDENCE = "habit_evidence"
    PRIOR_BAD_ACTS = "prior_bad_acts"
    SUBSEQUENT_REMEDIAL_MEASURES = "subsequent_remedial_measures"
    COMPROMISE_OFFERS = "compromise_offers"
    PLEA_BARGAINS = "plea_bargains"
    LIABILITY_INSURANCE = "liability_insurance"
    SEXUAL_ASSAULT_CASES = "sexual_assault_cases"
    RAPE_SHIELD = "rape_shield"
    WITNESS_COMPETENCY = "witness_competency"
    PERSONAL_KNOWLEDGE = "personal_knowledge"
    OATH_AFFIRMATION = "oath_affirmation"
    LEADING_QUESTIONS = "leading_questions"
    REFRESHING_RECOLLECTION = "refreshing_recollection"
    RECORDED_RECOLLECTION = "recorded_recollection"
    OPINION_TESTIMONY = "opinion_testimony"
    EXPERT_WITNESSES = "expert_witnesses"
    LAY_WITNESSES = "lay_witnesses"
    DAUBERT_STANDARD = "daubert_standard"
    IMPEACHMENT = "impeachment"
    PRIOR_INCONSISTENT_STATEMENTS = "prior_inconsistent_statements"
    BIAS = "bias"
    CONTRADICTION = "contradiction"
    HEARSAY = "hearsay"
    HEARSAY_EXCEPTIONS = "hearsay_exceptions"
    PRESENT_SENSE_IMPRESSION = "present_sense_impression"
    EXCITED_UTTERANCE = "excited_utterance"
    STATE_OF_MIND = "state_of_mind"
    MEDICAL_DIAGNOSIS = "medical_diagnosis"
    PAST_RECOLLECTION_RECORDED = "past_recollection_recorded"
    BUSINESS_RECORDS = "business_records"
    PUBLIC_RECORDS = "public_records"
    LEARNED_TREATISES = "learned_treatises"
    DYING_DECLARATION = "dying_declaration"
    STATEMENT_AGAINST_INTEREST = "statement_against_interest"
    FORFEITURE_BY_WRONGDOING = "forfeiture_by_wrongdoing"
    CONFRONTATION_CLAUSE = "confrontation_clause"
    AUTHENTICATION = "authentication"
    BEST_EVIDENCE_RULE = "best_evidence_rule"
    ORIGINAL_WRITING_RULE = "original_writing_rule"
    PRIVILEGES = "privileges"
    ATTORNEY_CLIENT = "attorney_client"
    WORK_PRODUCT = "work_product"
    SPOUSAL_PRIVILEGE = "spousal_privilege"
    PSYCHOTHERAPIST_PATIENT = "psychotherapist_patient"
    PHYSICIAN_PATIENT = "physician_patient"
    JUDICIAL_NOTICE = "judicial_notice"
    PRESUMPTIONS = "presumptions"
    GENERAL = "general"


class DifficultyLevel(Enum):
    """Difficulty levels for learning cards"""
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4
    MASTER = 5


class ConfidenceLevel(Enum):
    """Confidence/quality ratings for SM-2 algorithm"""
    COMPLETE_BLACKOUT = 0
    INCORRECT_HARD = 1
    INCORRECT_EASY = 2
    CORRECT_HARD = 3
    CORRECT_MEDIUM = 4
    CORRECT_EASY = 5


# ==================== DATA CLASSES ====================

@dataclass
class LearningCard:
    """Learning card with SM-2 spaced repetition fields"""
    card_id: str
    subject: str
    topic: str
    question: str
    answer: str
    difficulty: int
    ease_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0
    due_date: str = ""  # ISO format date
    last_review: Optional[str] = None  # ISO format datetime
    created_at: str = ""

    def __post_init__(self):
        if not self.due_date:
            self.due_date = datetime.now().date().isoformat()
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


# ==================== DATABASE CLASS ====================

class AdaptiveLearningDatabase:
    """Database manager for adaptive learning system"""

    def __init__(self, db_path: str = "adaptive_learning.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """Create necessary database tables"""
        cursor = self.conn.cursor()

        # Cards table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                card_id TEXT PRIMARY KEY,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                difficulty INTEGER NOT NULL,
                ease_factor REAL DEFAULT 2.5,
                interval_days INTEGER DEFAULT 1,
                repetitions INTEGER DEFAULT 0,
                due_date TEXT NOT NULL,
                last_review TEXT,
                created_at TEXT NOT NULL
            )
        """)

        # Performance tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id TEXT NOT NULL,
                review_date TEXT NOT NULL,
                quality_score INTEGER NOT NULL,
                time_spent_seconds INTEGER,
                FOREIGN KEY (card_id) REFERENCES cards(card_id)
            )
        """)

        # Learning sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                start_time TEXT NOT NULL,
                end_time TEXT,
                cards_reviewed INTEGER DEFAULT 0,
                average_quality REAL
            )
        """)

        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cards_due_date
            ON cards(due_date)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cards_subject
            ON cards(subject)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_performance_card
            ON performance(card_id)
        """)

        self.conn.commit()

    def add_card(self, card: LearningCard) -> bool:
        """Add a new learning card to the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO cards (
                    card_id, subject, topic, question, answer, difficulty,
                    ease_factor, interval_days, repetitions, due_date,
                    last_review, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                card.card_id, card.subject, card.topic, card.question,
                card.answer, card.difficulty, card.ease_factor,
                card.interval_days, card.repetitions, card.due_date,
                card.last_review, card.created_at
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Card already exists
            return False
        except Exception as e:
            print(f"Error adding card: {e}")
            return False

    def get_due_cards(self, limit: Optional[int] = None) -> List[LearningCard]:
        """Get all cards that are due for review (due_date <= today)"""
        cursor = self.conn.cursor()
        today = datetime.now().date().isoformat()

        query = """
            SELECT * FROM cards
            WHERE due_date <= ?
            ORDER BY due_date ASC, subject ASC
        """

        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query, (today,))
        rows = cursor.fetchall()

        return [self._row_to_card(row) for row in rows]

    def get_all_cards(self, subject: Optional[str] = None) -> List[LearningCard]:
        """Get all cards, optionally filtered by subject"""
        cursor = self.conn.cursor()

        if subject:
            cursor.execute("""
                SELECT * FROM cards
                WHERE subject = ?
                ORDER BY created_at DESC
            """, (subject,))
        else:
            cursor.execute("""
                SELECT * FROM cards
                ORDER BY subject ASC, created_at DESC
            """)

        rows = cursor.fetchall()
        return [self._row_to_card(row) for row in rows]

    def log_review(self, card_id: str, quality_score: int, time_spent: Optional[int] = None):
        """Log a card review in the performance table"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO performance (card_id, review_date, quality_score, time_spent_seconds)
            VALUES (?, ?, ?, ?)
        """, (card_id, datetime.now().isoformat(), quality_score, time_spent))
        self.conn.commit()

    def update_card_schedule(self, card_id: str, quality: int):
        """
        Update card schedule using SM-2 algorithm

        SM-2 Algorithm:
        - quality: 0-5 (0=complete failure, 5=perfect recall)
        - If quality < 3: reset repetitions and interval
        - If quality >= 3: increase interval based on ease factor
        - Update ease factor: EF' = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))
        """
        cursor = self.conn.cursor()

        # Get current card data
        cursor.execute("SELECT * FROM cards WHERE card_id = ?", (card_id,))
        row = cursor.fetchone()
        if not row:
            return

        card = self._row_to_card(row)

        # Update ease factor
        ef = card.ease_factor
        ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

        # Ensure ease factor doesn't go below 1.3
        if ef < 1.3:
            ef = 1.3

        # Calculate new interval
        if quality < 3:
            # Failed - reset
            repetitions = 0
            interval = 1
        else:
            # Passed - increase interval
            repetitions = card.repetitions + 1

            if repetitions == 1:
                interval = 1
            elif repetitions == 2:
                interval = 6
            else:
                interval = round(card.interval_days * ef)

        # Calculate new due date
        due_date = (datetime.now().date() + timedelta(days=interval)).isoformat()

        # Update database
        cursor.execute("""
            UPDATE cards
            SET ease_factor = ?,
                interval_days = ?,
                repetitions = ?,
                due_date = ?,
                last_review = ?
            WHERE card_id = ?
        """, (ef, interval, repetitions, due_date, datetime.now().isoformat(), card_id))

        self.conn.commit()

    def _row_to_card(self, row: sqlite3.Row) -> LearningCard:
        """Convert database row to LearningCard"""
        return LearningCard(
            card_id=row['card_id'],
            subject=row['subject'],
            topic=row['topic'],
            question=row['question'],
            answer=row['answer'],
            difficulty=row['difficulty'],
            ease_factor=row['ease_factor'],
            interval_days=row['interval_days'],
            repetitions=row['repetitions'],
            due_date=row['due_date'],
            last_review=row['last_review'],
            created_at=row['created_at']
        )

    def close(self):
        """Close database connection"""
        self.conn.close()


# ==================== ADAPTIVE LEARNING SYSTEM ====================

class AdaptiveLearningSystem:
    """High-level adaptive learning system with analytics"""

    def __init__(self, db_path: str = "adaptive_learning.db"):
        """Initialize the adaptive learning system"""
        self.db = AdaptiveLearningDatabase(db_path)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the learning system

        Returns:
            dict with total_cards, due_cards, mastered_cards, cards_by_subject
        """
        cursor = self.db.conn.cursor()

        # Total cards
        cursor.execute("SELECT COUNT(*) as count FROM cards")
        total_cards = cursor.fetchone()['count']

        # Due cards
        today = datetime.now().date().isoformat()
        cursor.execute("SELECT COUNT(*) as count FROM cards WHERE due_date <= ?", (today,))
        due_cards = cursor.fetchone()['count']

        # Mastered cards (repetitions >= 5 and ease_factor >= 2.5)
        cursor.execute("""
            SELECT COUNT(*) as count FROM cards
            WHERE repetitions >= 5 AND ease_factor >= 2.5
        """)
        mastered_cards = cursor.fetchone()['count']

        # Cards by subject
        cursor.execute("""
            SELECT subject, COUNT(*) as count
            FROM cards
            GROUP BY subject
            ORDER BY count DESC
        """)
        cards_by_subject = {row['subject']: row['count'] for row in cursor.fetchall()}

        return {
            'total_cards': total_cards,
            'due_cards': due_cards,
            'mastered_cards': mastered_cards,
            'cards_by_subject': cards_by_subject
        }

    def generate_adaptive_block(self, num_cards: int = 20) -> Dict[str, Any]:
        """
        Generate a recommended set of cards to review

        Returns:
            dict with recommended cards and metadata
        """
        cursor = self.db.conn.cursor()
        today = datetime.now().date().isoformat()

        # Get due cards grouped by subject
        cursor.execute("""
            SELECT subject, COUNT(*) as count
            FROM cards
            WHERE due_date <= ?
            GROUP BY subject
            ORDER BY count DESC
        """, (today,))

        subject_counts = {row['subject']: row['count'] for row in cursor.fetchall()}

        # Get due cards
        due_cards = self.db.get_due_cards(limit=num_cards)

        # Calculate recommended focus areas
        focus_subjects = sorted(subject_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            'recommended_cards': [card.to_dict() for card in due_cards],
            'num_cards': len(due_cards),
            'focus_subjects': [{'subject': s, 'due_count': c} for s, c in focus_subjects],
            'total_due': sum(subject_counts.values())
        }

    def get_subject_performance(self, days: int = 30) -> Dict[str, Dict[str, Any]]:
        """
        Get performance statistics by subject for the last N days

        Returns:
            dict mapping subject to accuracy and review count
        """
        cursor = self.db.conn.cursor()
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        cursor.execute("""
            SELECT c.subject,
                   COUNT(*) as total_reviews,
                   AVG(CASE WHEN p.quality_score >= 3 THEN 1.0 ELSE 0.0 END) as accuracy,
                   AVG(p.quality_score) as avg_quality
            FROM performance p
            JOIN cards c ON p.card_id = c.card_id
            WHERE p.review_date >= ?
            GROUP BY c.subject
            ORDER BY c.subject
        """, (cutoff_date,))

        results = {}
        for row in cursor.fetchall():
            results[row['subject']] = {
                'total_reviews': row['total_reviews'],
                'accuracy': round(row['accuracy'] * 100, 2) if row['accuracy'] else 0,
                'avg_quality': round(row['avg_quality'], 2) if row['avg_quality'] else 0
            }

        return results

    def close(self):
        """Close database connection"""
        self.db.close()


# ==================== MAIN ====================

if __name__ == "__main__":
    # Example usage
    print("Adaptive Learning System initialized")

    # Create system
    system = AdaptiveLearningSystem("test_adaptive.db")

    # Add a sample card
    sample_card = LearningCard(
        card_id="test_001",
        subject="contracts",
        topic="offer_acceptance",
        question="What are the essential elements of a valid offer?",
        answer="1) Intent to contract, 2) Definite terms, 3) Communication to offeree",
        difficulty=2
    )

    system.db.add_card(sample_card)

    # Get statistics
    stats = system.get_statistics()
    print(f"\nStatistics: {json.dumps(stats, indent=2)}")

    # Close
    system.close()
    print("\nSystem closed successfully")

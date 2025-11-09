#!/usr/bin/env python3
"""
Adaptive Learning System with SM-2 Spaced Repetition
Complete implementation for Iowa Bar Prep with 876-card database
"""

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json


# ==================== ENUMS ====================

class Subject(Enum):
    """14 Iowa Bar Exam subjects"""
    CONTRACTS = "contracts"
    TORTS = "torts"
    CONSTITUTIONAL_LAW = "constitutional_law"
    CRIMINAL_LAW = "criminal_law"
    CRIMINAL_PROCEDURE = "criminal_procedure"
    CIVIL_PROCEDURE = "civil_procedure"
    EVIDENCE = "evidence"
    REAL_PROPERTY = "real_property"
    PROFESSIONAL_RESPONSIBILITY = "professional_responsibility"
    CORPORATIONS = "corporations"
    WILLS_TRUSTS_ESTATES = "wills_trusts_estates"
    FAMILY_LAW = "family_law"
    SECURED_TRANSACTIONS = "secured_transactions"
    IOWA_PROCEDURE = "iowa_procedure"


class ConstitutionalLawTopic(Enum):
    """35 Constitutional Law topics"""
    # Federal Powers (5)
    COMMERCE_CLAUSE = "commerce_clause"
    TAXING_SPENDING_POWER = "taxing_spending_power"
    NECESSARY_PROPER_CLAUSE = "necessary_proper_clause"
    TREATY_POWER = "treaty_power"
    WAR_POWERS = "war_powers"

    # Federalism (5)
    SUPREMACY_CLAUSE = "supremacy_clause"
    DORMANT_COMMERCE = "dormant_commerce"
    STATE_TAXATION = "state_taxation"
    PREEMPTION = "preemption"
    TENTH_AMENDMENT = "tenth_amendment"

    # Separation of Powers (3)
    EXECUTIVE_POWER = "executive_power"
    LEGISLATIVE_POWER = "legislative_power"
    JUDICIAL_POWER = "judicial_power"

    # Individual Rights - Speech (7)
    FREE_SPEECH_GENERAL = "free_speech_general"
    CONTENT_BASED_RESTRICTIONS = "content_based_restrictions"
    CONTENT_NEUTRAL_RESTRICTIONS = "content_neutral_restrictions"
    PUBLIC_FORUM = "public_forum"
    SYMBOLIC_SPEECH = "symbolic_speech"
    COMMERCIAL_SPEECH = "commercial_speech"
    OBSCENITY = "obscenity"

    # Individual Rights - Religion (2)
    ESTABLISHMENT_CLAUSE = "establishment_clause"
    FREE_EXERCISE = "free_exercise"

    # Individual Rights - Other (5)
    DUE_PROCESS_PROCEDURAL = "due_process_procedural"
    DUE_PROCESS_SUBSTANTIVE = "due_process_substantive"
    EQUAL_PROTECTION = "equal_protection"
    TAKINGS = "takings"
    PRIVILEGES_IMMUNITIES = "privileges_immunities"

    # Misc (8)
    STATE_ACTION = "state_action"
    STANDING = "standing"
    MOOTNESS = "mootness"
    RIPENESS = "ripeness"
    POLITICAL_QUESTION = "political_question"
    ELEVENTH_AMENDMENT = "eleventh_amendment"
    CONGRESSIONAL_ENFORCEMENT = "congressional_enforcement"
    GENERAL = "general"


class EvidenceTopic(Enum):
    """50+ Evidence topics"""
    # Relevance (5)
    RELEVANCE_GENERAL = "relevance_general"
    LOGICAL_RELEVANCE = "logical_relevance"
    LEGAL_RELEVANCE_403 = "legal_relevance_403"
    CHARACTER_EVIDENCE = "character_evidence"
    HABIT_ROUTINE = "habit_routine"

    # Character Evidence (6)
    CHARACTER_CRIMINAL = "character_criminal"
    CHARACTER_CIVIL = "character_civil"
    CHARACTER_METHODS = "character_methods"
    PRIOR_CRIMES_404B = "prior_crimes_404b"
    IMPEACHMENT_CHARACTER = "impeachment_character"
    REPUTATION_OPINION = "reputation_opinion"

    # Hearsay (15)
    HEARSAY_DEFINITION = "hearsay_definition"
    HEARSAY_GENERAL = "hearsay_general"
    PRESENT_SENSE_IMPRESSION = "present_sense_impression"
    EXCITED_UTTERANCE = "excited_utterance"
    STATE_OF_MIND = "state_of_mind"
    MEDICAL_DIAGNOSIS = "medical_diagnosis"
    RECORDED_RECOLLECTION = "recorded_recollection"
    BUSINESS_RECORDS = "business_records"
    PUBLIC_RECORDS = "public_records"
    ANCIENT_DOCUMENTS = "ancient_documents"
    DYING_DECLARATION = "dying_declaration"
    STATEMENT_AGAINST_INTEREST = "statement_against_interest"
    FORFEITURE = "forfeiture"
    PRIOR_STATEMENT_WITNESS = "prior_statement_witness"
    ADMISSION_PARTY_OPPONENT = "admission_party_opponent"

    # Privileges (5)
    ATTORNEY_CLIENT = "attorney_client"
    SPOUSAL_PRIVILEGE = "spousal_privilege"
    PSYCHOTHERAPIST = "psychotherapist"
    CLERGY = "clergy"
    FIFTH_AMENDMENT = "fifth_amendment"

    # Witnesses (8)
    COMPETENCE = "competence"
    PERSONAL_KNOWLEDGE = "personal_knowledge"
    OATH_AFFIRMATION = "oath_affirmation"
    IMPEACHMENT_GENERAL = "impeachment_general"
    IMPEACHMENT_BIAS = "impeachment_bias"
    IMPEACHMENT_PRIOR_INCONSISTENT = "impeachment_prior_inconsistent"
    IMPEACHMENT_CONVICTION = "impeachment_conviction"
    REHABILITATION = "rehabilitation"

    # Expert Testimony (4)
    EXPERT_QUALIFICATION = "expert_qualification"
    EXPERT_BASIS = "expert_basis"
    DAUBERT_STANDARD = "daubert_standard"
    EXPERT_OPINION = "expert_opinion"

    # Authentication (4)
    AUTHENTICATION_GENERAL = "authentication_general"
    SELF_AUTHENTICATING = "self_authenticating"
    VOICE_IDENTIFICATION = "voice_identification"
    ANCIENT_DOCUMENTS_AUTH = "ancient_documents_auth"

    # Best Evidence (3)
    ORIGINAL_DOCUMENT = "original_document"
    DUPLICATES = "duplicates"
    EXCUSES_NONPRODUCTION = "excuses_nonproduction"

    # Judicial Notice (2)
    JUDICIAL_NOTICE_GENERAL = "judicial_notice_general"
    JUDICIAL_NOTICE_TYPES = "judicial_notice_types"

    # Miscellaneous (3)
    PRESUMPTIONS = "presumptions"
    BURDENS = "burdens"
    GENERAL = "general"


class DifficultyLevel(Enum):
    """Difficulty levels for concepts"""
    FUNDAMENTAL = 1
    BASIC = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5


class ConfidenceLevel(Enum):
    """Student confidence levels"""
    NO_IDEA = 0
    VAGUE = 1
    UNCERTAIN = 2
    CONFIDENT = 3
    MASTERED = 4


# ==================== DATA CLASSES ====================

@dataclass
class LearningCard:
    """Individual learning card with SM-2 spaced repetition fields"""
    card_id: str
    concept_id: str
    subject: str
    topic: Optional[str]  # For Constitutional Law and Evidence
    card_type: str  # rule, elements, exceptions, traps, policy

    # Card content
    front: str
    back: str

    # Difficulty
    difficulty: int  # 1-5

    # SM-2 Spaced Repetition fields
    ease_factor: float = 2.5
    interval: int = 1  # days
    repetitions: int = 0
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None

    # Performance tracking
    times_seen: int = 0
    times_correct: int = 0
    times_incorrect: int = 0
    average_confidence: float = 0.0

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def calculate_accuracy(self) -> float:
        """Calculate accuracy percentage"""
        if self.times_seen == 0:
            return 0.0
        return (self.times_correct / self.times_seen) * 100

    def is_due(self) -> bool:
        """Check if card is due for review"""
        if self.next_review is None:
            return True
        return datetime.now() >= self.next_review

    def is_mastered(self) -> bool:
        """Check if card is mastered (high ease factor and long interval)"""
        return self.ease_factor >= 2.5 and self.interval >= 21 and self.times_correct >= 3


# ==================== DATABASE ====================

class AdaptiveLearningDatabase:
    """SQLite database for adaptive learning cards"""

    def __init__(self, db_path: str = "iowa_bar_prep.db"):
        self.db_path = db_path
        self.conn = None
        self._initialize_database()

    def _initialize_database(self):
        """Create database schema"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                card_id TEXT PRIMARY KEY,
                concept_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                topic TEXT,
                card_type TEXT NOT NULL,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                difficulty INTEGER NOT NULL,
                ease_factor REAL DEFAULT 2.5,
                interval INTEGER DEFAULT 1,
                repetitions INTEGER DEFAULT 0,
                last_reviewed TEXT,
                next_review TEXT,
                times_seen INTEGER DEFAULT 0,
                times_correct INTEGER DEFAULT 0,
                times_incorrect INTEGER DEFAULT 0,
                average_confidence REAL DEFAULT 0.0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_subject ON cards(subject)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic ON cards(topic)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_next_review ON cards(next_review)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_concept_id ON cards(concept_id)")

        # Performance tracking table - individual review records
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id TEXT NOT NULL,
                review_date TEXT NOT NULL,
                quality INTEGER NOT NULL,
                time_seconds INTEGER,
                FOREIGN KEY (card_id) REFERENCES cards(card_id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_perf_card ON performance(card_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_perf_date ON performance(review_date)")

        # Sessions table - study session summaries
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_date TEXT NOT NULL,
                cards_reviewed INTEGER NOT NULL,
                avg_quality REAL,
                duration_minutes INTEGER
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_date ON sessions(session_date)")

        self.conn.commit()

    def insert_card(self, card: LearningCard):
        """Insert a new card"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO cards VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            card.card_id,
            card.concept_id,
            card.subject,
            card.topic,
            card.card_type,
            card.front,
            card.back,
            card.difficulty,
            card.ease_factor,
            card.interval,
            card.repetitions,
            card.last_reviewed.isoformat() if card.last_reviewed else None,
            card.next_review.isoformat() if card.next_review else None,
            card.times_seen,
            card.times_correct,
            card.times_incorrect,
            card.average_confidence,
            card.created_at.isoformat(),
            card.updated_at.isoformat()
        ))
        self.conn.commit()

    def get_card(self, card_id: str) -> Optional[LearningCard]:
        """Retrieve a card by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cards WHERE card_id = ?", (card_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_card(row)

    def get_all_cards(self) -> List[LearningCard]:
        """Get all cards"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cards")
        return [self._row_to_card(row) for row in cursor.fetchall()]

    def get_cards_by_subject(self, subject: str) -> List[LearningCard]:
        """Get all cards for a subject"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cards WHERE subject = ?", (subject,))
        return [self._row_to_card(row) for row in cursor.fetchall()]

    def get_cards_by_topic(self, topic: str) -> List[LearningCard]:
        """Get all cards for a topic"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cards WHERE topic = ?", (topic,))
        return [self._row_to_card(row) for row in cursor.fetchall()]

    def get_due_cards(self, limit: Optional[int] = None) -> List[LearningCard]:
        """Get cards due for review"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()

        query = """
            SELECT * FROM cards
            WHERE next_review IS NULL OR next_review <= ?
            ORDER BY next_review ASC
        """

        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query, (now,))
        return [self._row_to_card(row) for row in cursor.fetchall()]

    def update_card(self, card: LearningCard):
        """Update an existing card"""
        card.updated_at = datetime.now()
        self.insert_card(card)

    def _row_to_card(self, row: sqlite3.Row) -> LearningCard:
        """Convert database row to LearningCard"""
        return LearningCard(
            card_id=row['card_id'],
            concept_id=row['concept_id'],
            subject=row['subject'],
            topic=row['topic'],
            card_type=row['card_type'],
            front=row['front'],
            back=row['back'],
            difficulty=row['difficulty'],
            ease_factor=row['ease_factor'],
            interval=row['interval'],
            repetitions=row['repetitions'],
            last_reviewed=datetime.fromisoformat(row['last_reviewed']) if row['last_reviewed'] else None,
            next_review=datetime.fromisoformat(row['next_review']) if row['next_review'] else None,
            times_seen=row['times_seen'],
            times_correct=row['times_correct'],
            times_incorrect=row['times_incorrect'],
            average_confidence=row['average_confidence'],
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )

    def insert_performance(self, card_id: str, quality: int, time_seconds: Optional[int] = None):
        """Insert a performance record for a card review"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO performance (card_id, review_date, quality, time_seconds)
            VALUES (?, ?, ?, ?)
        """, (card_id, datetime.now().isoformat(), quality, time_seconds))
        self.conn.commit()

    def get_card_performance_history(self, card_id: str) -> List[Dict]:
        """Get performance history for a specific card"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT review_date, quality, time_seconds
            FROM performance
            WHERE card_id = ?
            ORDER BY review_date DESC
        """, (card_id,))

        return [
            {
                'review_date': row[0],
                'quality': row[1],
                'time_seconds': row[2]
            }
            for row in cursor.fetchall()
        ]

    def insert_session(self, cards_reviewed: int, avg_quality: float, duration_minutes: int):
        """Insert a study session record"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO sessions (session_date, cards_reviewed, avg_quality, duration_minutes)
            VALUES (?, ?, ?, ?)
        """, (datetime.now().isoformat(), cards_reviewed, avg_quality, duration_minutes))
        self.conn.commit()

    def get_recent_sessions(self, days: int = 30) -> List[Dict]:
        """Get recent study sessions"""
        cursor = self.conn.cursor()
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        cursor.execute("""
            SELECT session_date, cards_reviewed, avg_quality, duration_minutes
            FROM sessions
            WHERE session_date >= ?
            ORDER BY session_date DESC
        """, (cutoff_date,))

        return [
            {
                'session_date': row[0],
                'cards_reviewed': row[1],
                'avg_quality': row[2],
                'duration_minutes': row[3]
            }
            for row in cursor.fetchall()
        ]

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


# ==================== ADAPTIVE LEARNING SYSTEM ====================

class AdaptiveLearningSystem:
    """Main adaptive learning system with SM-2 algorithm and analytics"""

    def __init__(self, db_path: str = "iowa_bar_prep.db"):
        self.db = AdaptiveLearningDatabase(db_path)

    def review_card(self, card: LearningCard, confidence: ConfidenceLevel) -> LearningCard:
        """
        Review a card and update SM-2 parameters

        SM-2 Algorithm:
        - If quality >= 3: repetitions++, update interval
        - If quality < 3: repetitions = 0, interval = 1
        - EF' = EF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        """
        card.times_seen += 1
        card.last_reviewed = datetime.now()

        quality = confidence.value

        # Update accuracy
        if quality >= 3:
            card.times_correct += 1
        else:
            card.times_incorrect += 1

        # Update average confidence
        card.average_confidence = (
            (card.average_confidence * (card.times_seen - 1) + quality) / card.times_seen
        )

        # SM-2 Algorithm
        if quality >= 3:
            if card.repetitions == 0:
                card.interval = 1
            elif card.repetitions == 1:
                card.interval = 6
            else:
                card.interval = int(card.interval * card.ease_factor)

            card.repetitions += 1
        else:
            card.repetitions = 0
            card.interval = 1

        # Update ease factor
        card.ease_factor = max(1.3, card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        # Set next review date
        card.next_review = datetime.now() + timedelta(days=card.interval)

        # Save to database
        self.db.update_card(card)

        # Record performance (quality score for this review)
        self.db.insert_performance(card.card_id, quality, time_seconds=None)

        return card

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        all_cards = self.db.get_all_cards()

        if not all_cards:
            return {
                'total_cards': 0,
                'cards_due': 0,
                'cards_mastered': 0,
                'overall_accuracy': 0.0,
                'average_confidence': 0.0
            }

        due_cards = [c for c in all_cards if c.is_due()]
        mastered_cards = [c for c in all_cards if c.is_mastered()]

        total_seen = sum(c.times_seen for c in all_cards)
        total_correct = sum(c.times_correct for c in all_cards)

        overall_accuracy = (total_correct / total_seen * 100) if total_seen > 0 else 0.0

        avg_confidence = sum(c.average_confidence for c in all_cards) / len(all_cards)

        return {
            'total_cards': len(all_cards),
            'cards_due': len(due_cards),
            'cards_mastered': len(mastered_cards),
            'overall_accuracy': overall_accuracy,
            'average_confidence': avg_confidence,
            'total_reviews': total_seen
        }

    def get_subject_statistics(self) -> Dict[str, Dict]:
        """Get statistics by subject"""
        all_cards = self.db.get_all_cards()

        subject_stats = {}

        for subject in Subject:
            subject_cards = [c for c in all_cards if c.subject == subject.value]

            if not subject_cards:
                continue

            due = len([c for c in subject_cards if c.is_due()])
            mastered = len([c for c in subject_cards if c.is_mastered()])

            total_seen = sum(c.times_seen for c in subject_cards)
            total_correct = sum(c.times_correct for c in subject_cards)

            accuracy = (total_correct / total_seen * 100) if total_seen > 0 else 0.0

            subject_stats[subject.value] = {
                'total': len(subject_cards),
                'due': due,
                'mastered': mastered,
                'accuracy': accuracy
            }

        return subject_stats

    def get_topic_statistics(self, subject: str) -> Dict[str, Dict]:
        """Get statistics by topic for Constitutional Law or Evidence"""
        all_cards = self.db.get_cards_by_subject(subject)

        topic_stats = {}

        for card in all_cards:
            if card.topic is None:
                continue

            if card.topic not in topic_stats:
                topic_stats[card.topic] = {
                    'total': 0,
                    'due': 0,
                    'mastered': 0,
                    'seen': 0,
                    'correct': 0
                }

            stats = topic_stats[card.topic]
            stats['total'] += 1
            if card.is_due():
                stats['due'] += 1
            if card.is_mastered():
                stats['mastered'] += 1
            stats['seen'] += card.times_seen
            stats['correct'] += card.times_correct

        # Calculate accuracy for each topic
        for topic, stats in topic_stats.items():
            stats['accuracy'] = (stats['correct'] / stats['seen'] * 100) if stats['seen'] > 0 else 0.0

        return topic_stats

    def get_interval_distribution(self) -> Dict[str, int]:
        """Get distribution of cards by interval"""
        all_cards = self.db.get_all_cards()

        distribution = {
            'new': 0,
            '1_day': 0,
            '2_7_days': 0,
            '8_21_days': 0,
            '22_60_days': 0,
            '60+_days': 0
        }

        for card in all_cards:
            if card.repetitions == 0:
                distribution['new'] += 1
            elif card.interval == 1:
                distribution['1_day'] += 1
            elif 2 <= card.interval <= 7:
                distribution['2_7_days'] += 1
            elif 8 <= card.interval <= 21:
                distribution['8_21_days'] += 1
            elif 22 <= card.interval <= 60:
                distribution['22_60_days'] += 1
            else:
                distribution['60+_days'] += 1

        return distribution

    def get_forecast(self, days: int = 7) -> List[Tuple[str, int]]:
        """Get forecast of cards due over next N days"""
        all_cards = self.db.get_all_cards()

        forecast = []

        for i in range(days):
            target_date = datetime.now() + timedelta(days=i)
            target_date_str = target_date.strftime('%Y-%m-%d')

            due_count = 0
            for card in all_cards:
                if card.next_review is None:
                    if i == 0:
                        due_count += 1
                elif card.next_review.date() == target_date.date():
                    due_count += 1

            forecast.append((target_date_str, due_count))

        return forecast

    def close(self):
        """Close database connection"""
        self.db.close()


# ==================== MAIN ====================

if __name__ == "__main__":
    # Example usage
    system = AdaptiveLearningSystem()
    stats = system.get_statistics()

    print("Adaptive Learning System Statistics")
    print("=" * 50)
    print(f"Total Cards: {stats['total_cards']}")
    print(f"Cards Due: {stats['cards_due']}")
    print(f"Cards Mastered: {stats['cards_mastered']}")
    print(f"Overall Accuracy: {stats['overall_accuracy']:.1f}%")
    print(f"Average Confidence: {stats['average_confidence']:.2f}")

    system.close()

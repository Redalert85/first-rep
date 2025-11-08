#!/usr/bin/env python3
"""
Enhanced Adaptive Learning System for Bar Prep
Combines advanced pedagogy with SM-2 spaced repetition and SQLite persistence
Optimized for Constitutional Law and Evidence tracking
"""

import sqlite3
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from pathlib import Path
import random
from statistics import mean


# ============================================================================
# ENUM-BASED CONTROLLED VOCABULARY
# ============================================================================

class Subject(Enum):
    """Bar exam subjects"""
    CONSTITUTIONAL_LAW = "constitutional_law"
    EVIDENCE = "evidence"
    CONTRACTS = "contracts"
    TORTS = "torts"
    CRIMINAL_LAW = "criminal_law"
    CRIMINAL_PROCEDURE = "criminal_procedure"
    CIVIL_PROCEDURE = "civil_procedure"
    REAL_PROPERTY = "real_property"


class ConstitutionalLawTopic(Enum):
    """Constitutional Law subtopics"""
    JUDICIAL_REVIEW = "judicial_review"
    JUSTICIABILITY = "justiciability"
    STANDING = "standing"
    MOOTNESS = "mootness"
    RIPENESS = "ripeness"

    # Federal Powers
    COMMERCE_CLAUSE = "commerce_clause"
    TAXING_SPENDING = "taxing_spending"
    NECESSARY_AND_PROPER = "necessary_and_proper"
    TREATY_POWER = "treaty_power"
    WAR_POWERS = "war_powers"

    # Individual Rights - Due Process
    PROCEDURAL_DUE_PROCESS = "procedural_due_process"
    SUBSTANTIVE_DUE_PROCESS = "substantive_due_process"
    INCORPORATION = "incorporation"
    FUNDAMENTAL_RIGHTS = "fundamental_rights"

    # Individual Rights - Equal Protection
    EQUAL_PROTECTION = "equal_protection"
    STRICT_SCRUTINY = "strict_scrutiny"
    INTERMEDIATE_SCRUTINY = "intermediate_scrutiny"
    RATIONAL_BASIS = "rational_basis"
    SUSPECT_CLASSIFICATIONS = "suspect_classifications"
    QUASI_SUSPECT_CLASSIFICATIONS = "quasi_suspect_classifications"

    # First Amendment
    FREEDOM_OF_SPEECH = "freedom_of_speech"
    FREEDOM_OF_RELIGION = "freedom_of_religion"
    ESTABLISHMENT_CLAUSE = "establishment_clause"
    FREE_EXERCISE_CLAUSE = "free_exercise_clause"
    FREEDOM_OF_PRESS = "freedom_of_press"
    FREEDOM_OF_ASSEMBLY = "freedom_of_assembly"

    # Other Rights
    TAKINGS_CLAUSE = "takings_clause"
    PRIVILEGES_AND_IMMUNITIES = "privileges_and_immunities"
    DORMANT_COMMERCE_CLAUSE = "dormant_commerce_clause"
    STATE_ACTION = "state_action"


class EvidenceTopic(Enum):
    """Evidence subtopics"""
    # Relevance
    RELEVANCE = "relevance"
    LOGICAL_RELEVANCE = "logical_relevance"
    LEGAL_RELEVANCE_403 = "legal_relevance_403"
    CONDITIONAL_RELEVANCE = "conditional_relevance"

    # Character Evidence
    CHARACTER_EVIDENCE = "character_evidence"
    CHARACTER_CIVIL = "character_civil"
    CHARACTER_CRIMINAL = "character_criminal"
    PROPENSITY_EVIDENCE = "propensity_evidence"
    PRIOR_BAD_ACTS_404B = "prior_bad_acts_404b"
    HABIT_EVIDENCE = "habit_evidence"

    # Hearsay
    HEARSAY_DEFINITION = "hearsay_definition"
    HEARSAY_EXCEPTIONS_803 = "hearsay_exceptions_803"
    HEARSAY_EXCEPTIONS_804 = "hearsay_exceptions_804"
    PRESENT_SENSE_IMPRESSION = "present_sense_impression"
    EXCITED_UTTERANCE = "excited_utterance"
    STATE_OF_MIND = "state_of_mind"
    MEDICAL_DIAGNOSIS = "medical_diagnosis"
    RECORDED_RECOLLECTION = "recorded_recollection"
    BUSINESS_RECORDS = "business_records"
    PUBLIC_RECORDS = "public_records"
    FORMER_TESTIMONY = "former_testimony"
    DYING_DECLARATION = "dying_declaration"
    STATEMENT_AGAINST_INTEREST = "statement_against_interest"
    FORFEITURE_BY_WRONGDOING = "forfeiture_by_wrongdoing"

    # Confrontation Clause
    CONFRONTATION_CLAUSE = "confrontation_clause"
    TESTIMONIAL_STATEMENTS = "testimonial_statements"

    # Impeachment
    IMPEACHMENT = "impeachment"
    PRIOR_INCONSISTENT_STATEMENT = "prior_inconsistent_statement"
    BIAS_MOTIVE = "bias_motive"
    SENSORY_DEFECTS = "sensory_defects"
    CONTRADICTION = "contradiction"
    CHARACTER_FOR_TRUTHFULNESS = "character_for_truthfulness"
    CRIMINAL_CONVICTIONS = "criminal_convictions"

    # Privileges
    ATTORNEY_CLIENT = "attorney_client"
    SPOUSAL_PRIVILEGES = "spousal_privileges"
    DOCTOR_PATIENT = "doctor_patient"
    PSYCHOTHERAPIST_PATIENT = "psychotherapist_patient"

    # Witnesses
    COMPETENCY = "competency"
    PERSONAL_KNOWLEDGE = "personal_knowledge"
    LEADING_QUESTIONS = "leading_questions"
    REFRESHING_RECOLLECTION = "refreshing_recollection"

    # Expert Testimony
    EXPERT_QUALIFICATIONS = "expert_qualifications"
    EXPERT_BASES = "expert_bases"
    DAUBERT_STANDARD = "daubert_standard"
    ULTIMATE_ISSUE = "ultimate_issue"

    # Authentication
    AUTHENTICATION = "authentication"
    SELF_AUTHENTICATING = "self_authenticating"
    BEST_EVIDENCE_RULE = "best_evidence_rule"


class DifficultyLevel(Enum):
    """Question difficulty levels"""
    FOUNDATIONAL = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4
    BAR_EXAM_LEVEL = 5


class ConfidenceLevel(Enum):
    """Student confidence levels (1-5)"""
    GUESSING = 1
    UNCERTAIN = 2
    SOMEWHAT_CONFIDENT = 3
    CONFIDENT = 4
    VERY_CONFIDENT = 5


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class LearningCard:
    """Spaced repetition card with SM-2 algorithm"""
    card_id: str
    subject: Subject
    topic: str  # Stores the enum value as string
    concept_name: str
    question: str
    answer: str
    difficulty: DifficultyLevel

    # SM-2 Algorithm fields
    ease_factor: float = 2.5
    interval: int = 1  # days until next review
    repetitions: int = 0
    next_review: Optional[datetime] = None

    # Performance tracking
    total_reviews: int = 0
    correct_reviews: int = 0
    last_reviewed: Optional[datetime] = None

    # Metadata
    created_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.next_review is None:
            self.next_review = datetime.now()
        if self.created_at is None:
            self.created_at = datetime.now()

    @property
    def mastery_level(self) -> float:
        """Calculate mastery level (0-1)"""
        if self.total_reviews == 0:
            return 0.0
        accuracy = self.correct_reviews / self.total_reviews
        # Factor in ease and repetitions
        mastery = (accuracy * 0.6 + min(self.repetitions / 10, 1) * 0.3 +
                   min(self.ease_factor / 4, 1) * 0.1)
        return min(mastery, 1.0)

    def is_due(self) -> bool:
        """Check if card is due for review"""
        return datetime.now() >= self.next_review

    def review(self, quality: int, confidence: ConfidenceLevel):
        """
        Update card using SM-2 algorithm with confidence weighting

        Args:
            quality: Performance quality (0-5)
                0-1: Complete blackout
                2: Incorrect but remembered something
                3: Correct with difficulty
                4: Correct with hesitation
                5: Perfect recall
            confidence: Student's confidence level before seeing answer
        """
        self.total_reviews += 1
        self.last_reviewed = datetime.now()

        # Apply confidence weighting to quality
        weighted_quality = self._apply_confidence_weighting(quality, confidence)

        # Standard SM-2 algorithm
        if weighted_quality < 3:
            # Failed - reset learning
            self.repetitions = 0
            self.interval = 1
            self.next_review = datetime.now() + timedelta(days=1)
        else:
            # Passed - advance learning
            self.correct_reviews += 1

            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)

            self.repetitions += 1

            # Update ease factor
            self.ease_factor = max(
                1.3,
                self.ease_factor + (0.1 - (5 - weighted_quality) *
                                   (0.08 + (5 - weighted_quality) * 0.02))
            )

            # Set next review date
            self.next_review = datetime.now() + timedelta(days=self.interval)

    def _apply_confidence_weighting(self, quality: int, confidence: ConfidenceLevel) -> float:
        """
        Adjust quality score based on confidence calibration

        High confidence + correct = boost quality
        High confidence + incorrect = penalize heavily
        Low confidence + correct = moderate boost
        Low confidence + incorrect = slight penalty
        """
        is_correct = quality >= 3
        conf_value = confidence.value

        if is_correct:
            if conf_value >= 4:
                # High confidence and correct - excellent!
                return min(quality + 0.5, 5)
            elif conf_value <= 2:
                # Low confidence but correct - learning is happening
                return min(quality + 0.3, 5)
            else:
                return quality
        else:
            if conf_value >= 4:
                # High confidence but wrong - serious misconception
                return max(quality - 1.0, 0)
            elif conf_value <= 2:
                # Low confidence and wrong - expected, slight penalty
                return max(quality - 0.2, 0)
            else:
                return quality


@dataclass
class PerformanceRecord:
    """Track individual question performance"""
    record_id: Optional[int] = None
    card_id: str = ""
    subject: str = ""
    topic: str = ""
    timestamp: Optional[datetime] = None
    quality: int = 0
    confidence: int = 0
    time_taken: int = 0  # seconds
    is_correct: bool = False

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class StudySession:
    """Track study sessions"""
    session_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    cards_reviewed: int = 0
    cards_correct: int = 0
    subjects_covered: List[str] = field(default_factory=list)
    avg_confidence: float = 0.0
    session_quality: float = 0.0

    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()

    @property
    def accuracy(self) -> float:
        """Calculate session accuracy"""
        if self.cards_reviewed == 0:
            return 0.0
        return self.cards_correct / self.cards_reviewed


# ============================================================================
# SQLITE PERSISTENCE LAYER
# ============================================================================

class AdaptiveLearningDatabase:
    """SQLite database for persistent storage"""

    def __init__(self, db_path: str = "adaptive_learning.db"):
        self.db_path = db_path
        self.conn = None
        self._initialize_database()

    def _initialize_database(self):
        """Create database schema"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        # Cards table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                card_id TEXT PRIMARY KEY,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                concept_name TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                difficulty INTEGER NOT NULL,
                ease_factor REAL DEFAULT 2.5,
                interval INTEGER DEFAULT 1,
                repetitions INTEGER DEFAULT 0,
                next_review TEXT NOT NULL,
                total_reviews INTEGER DEFAULT 0,
                correct_reviews INTEGER DEFAULT 0,
                last_reviewed TEXT,
                created_at TEXT NOT NULL,
                tags TEXT
            )
        """)

        # Performance records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                quality INTEGER NOT NULL,
                confidence INTEGER NOT NULL,
                time_taken INTEGER NOT NULL,
                is_correct BOOLEAN NOT NULL,
                FOREIGN KEY (card_id) REFERENCES cards(card_id)
            )
        """)

        # Study sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                cards_reviewed INTEGER DEFAULT 0,
                cards_correct INTEGER DEFAULT 0,
                subjects_covered TEXT,
                avg_confidence REAL DEFAULT 0.0,
                session_quality REAL DEFAULT 0.0
            )
        """)

        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_performance_card
            ON performance(card_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_performance_subject
            ON performance(subject)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cards_next_review
            ON cards(next_review)
        """)

        self.conn.commit()

    def save_card(self, card: LearningCard):
        """Save or update a card"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO cards
            (card_id, subject, topic, concept_name, question, answer, difficulty,
             ease_factor, interval, repetitions, next_review, total_reviews,
             correct_reviews, last_reviewed, created_at, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            card.card_id,
            card.subject.value,
            card.topic,
            card.concept_name,
            card.question,
            card.answer,
            card.difficulty.value,
            card.ease_factor,
            card.interval,
            card.repetitions,
            card.next_review.isoformat(),
            card.total_reviews,
            card.correct_reviews,
            card.last_reviewed.isoformat() if card.last_reviewed else None,
            card.created_at.isoformat(),
            json.dumps(card.tags)
        ))
        self.conn.commit()

    def load_card(self, card_id: str) -> Optional[LearningCard]:
        """Load a card by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cards WHERE card_id = ?", (card_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_card(row)
        return None

    def get_all_cards(self, subject: Optional[Subject] = None) -> List[LearningCard]:
        """Get all cards, optionally filtered by subject"""
        cursor = self.conn.cursor()

        if subject:
            cursor.execute("SELECT * FROM cards WHERE subject = ?", (subject.value,))
        else:
            cursor.execute("SELECT * FROM cards")

        return [self._row_to_card(row) for row in cursor.fetchall()]

    def get_due_cards(self, limit: Optional[int] = None,
                     subject: Optional[Subject] = None) -> List[LearningCard]:
        """Get cards due for review"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()

        query = "SELECT * FROM cards WHERE next_review <= ?"
        params = [now]

        if subject:
            query += " AND subject = ?"
            params.append(subject.value)

        query += " ORDER BY next_review ASC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor.execute(query, params)
        return [self._row_to_card(row) for row in cursor.fetchall()]

    def _row_to_card(self, row: sqlite3.Row) -> LearningCard:
        """Convert database row to LearningCard"""
        return LearningCard(
            card_id=row['card_id'],
            subject=Subject(row['subject']),
            topic=row['topic'],
            concept_name=row['concept_name'],
            question=row['question'],
            answer=row['answer'],
            difficulty=DifficultyLevel(row['difficulty']),
            ease_factor=row['ease_factor'],
            interval=row['interval'],
            repetitions=row['repetitions'],
            next_review=datetime.fromisoformat(row['next_review']),
            total_reviews=row['total_reviews'],
            correct_reviews=row['correct_reviews'],
            last_reviewed=datetime.fromisoformat(row['last_reviewed']) if row['last_reviewed'] else None,
            created_at=datetime.fromisoformat(row['created_at']),
            tags=json.loads(row['tags']) if row['tags'] else []
        )

    def save_performance(self, record: PerformanceRecord) -> int:
        """Save performance record and return record_id"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO performance
            (card_id, subject, topic, timestamp, quality, confidence,
             time_taken, is_correct)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.card_id,
            record.subject,
            record.topic,
            record.timestamp.isoformat(),
            record.quality,
            record.confidence,
            record.time_taken,
            record.is_correct
        ))
        self.conn.commit()
        return cursor.lastrowid

    def save_session(self, session: StudySession) -> int:
        """Save study session and return session_id"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO sessions
            (start_time, end_time, cards_reviewed, cards_correct,
             subjects_covered, avg_confidence, session_quality)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session.start_time.isoformat(),
            session.end_time.isoformat() if session.end_time else None,
            session.cards_reviewed,
            session.cards_correct,
            json.dumps(session.subjects_covered),
            session.avg_confidence,
            session.session_quality
        ))
        self.conn.commit()
        return cursor.lastrowid

    def update_session(self, session: StudySession):
        """Update existing session"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE sessions
            SET end_time = ?, cards_reviewed = ?, cards_correct = ?,
                subjects_covered = ?, avg_confidence = ?, session_quality = ?
            WHERE session_id = ?
        """, (
            session.end_time.isoformat() if session.end_time else None,
            session.cards_reviewed,
            session.cards_correct,
            json.dumps(session.subjects_covered),
            session.avg_confidence,
            session.session_quality,
            session.session_id
        ))
        self.conn.commit()

    def get_performance_by_subject(self, subject: Subject,
                                   days: int = 30) -> List[PerformanceRecord]:
        """Get recent performance for a subject"""
        cursor = self.conn.cursor()
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()

        cursor.execute("""
            SELECT * FROM performance
            WHERE subject = ? AND timestamp >= ?
            ORDER BY timestamp DESC
        """, (subject.value, cutoff))

        return [self._row_to_performance(row) for row in cursor.fetchall()]

    def _row_to_performance(self, row: sqlite3.Row) -> PerformanceRecord:
        """Convert database row to PerformanceRecord"""
        return PerformanceRecord(
            record_id=row['record_id'],
            card_id=row['card_id'],
            subject=row['subject'],
            topic=row['topic'],
            timestamp=datetime.fromisoformat(row['timestamp']),
            quality=row['quality'],
            confidence=row['confidence'],
            time_taken=row['time_taken'],
            is_correct=bool(row['is_correct'])
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics"""
        cursor = self.conn.cursor()

        # Total cards
        cursor.execute("SELECT COUNT(*) as count FROM cards")
        total_cards = cursor.fetchone()['count']

        # Due cards
        now = datetime.now().isoformat()
        cursor.execute("SELECT COUNT(*) as count FROM cards WHERE next_review <= ?", (now,))
        due_cards = cursor.fetchone()['count']

        # Mastered cards (repetitions >= 5, ease >= 2.5)
        cursor.execute("""
            SELECT COUNT(*) as count FROM cards
            WHERE repetitions >= 5 AND ease_factor >= 2.5
        """)
        mastered = cursor.fetchone()['count']

        # Subject breakdown
        cursor.execute("""
            SELECT subject, COUNT(*) as count
            FROM cards
            GROUP BY subject
        """)
        by_subject = {row['subject']: row['count'] for row in cursor.fetchall()}

        # Recent performance (last 7 days)
        cutoff = (datetime.now() - timedelta(days=7)).isoformat()
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as correct,
                AVG(confidence) as avg_conf
            FROM performance
            WHERE timestamp >= ?
        """, (cutoff,))

        perf = cursor.fetchone()
        recent_accuracy = perf['correct'] / perf['total'] if perf['total'] else 0

        return {
            'total_cards': total_cards,
            'due_cards': due_cards,
            'mastered_cards': mastered,
            'mastery_percentage': (mastered / total_cards * 100) if total_cards else 0,
            'cards_by_subject': by_subject,
            'recent_7day_accuracy': recent_accuracy,
            'recent_7day_avg_confidence': perf['avg_conf'] or 0
        }

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


# ============================================================================
# ADAPTIVE QUESTION BLOCK GENERATOR
# ============================================================================

class AdaptiveBlockGenerator:
    """Generate adaptive question blocks based on performance"""

    def __init__(self, db: AdaptiveLearningDatabase):
        self.db = db

    def generate_block(self,
                      block_size: int = 10,
                      subject: Optional[Subject] = None,
                      difficulty_target: Optional[DifficultyLevel] = None,
                      include_new: bool = True,
                      include_review: bool = True) -> List[LearningCard]:
        """
        Generate adaptive question block

        Strategy:
        - Prioritize due cards (spaced repetition)
        - Mix difficulty levels based on recent performance
        - Include new cards if performance is good
        - Balance between subjects if no subject specified
        """
        block = []

        # Get due cards first (spaced repetition priority)
        if include_review:
            due_cards = self.db.get_due_cards(limit=block_size, subject=subject)
            block.extend(due_cards)

        # Fill remaining slots with strategic selection
        if len(block) < block_size and include_new:
            remaining = block_size - len(block)
            all_cards = self.db.get_all_cards(subject=subject)

            # Remove already selected cards
            available = [c for c in all_cards if c.card_id not in
                        {card.card_id for card in block}]

            # Calculate performance-based difficulty adjustment
            if difficulty_target:
                target_diff = difficulty_target
            else:
                target_diff = self._calculate_adaptive_difficulty(subject)

            # Score and sort available cards
            scored_cards = []
            for card in available:
                score = self._calculate_card_priority(card, target_diff)
                scored_cards.append((card, score))

            scored_cards.sort(key=lambda x: x[1], reverse=True)

            # Add top-scoring cards
            for card, score in scored_cards[:remaining]:
                block.append(card)

        # Shuffle to prevent pattern recognition
        random.shuffle(block)

        return block[:block_size]

    def _calculate_adaptive_difficulty(self, subject: Optional[Subject]) -> DifficultyLevel:
        """Calculate appropriate difficulty based on recent performance"""
        if subject:
            recent = self.db.get_performance_by_subject(subject, days=7)
        else:
            # Get all recent performance
            recent = []
            for subj in Subject:
                recent.extend(self.db.get_performance_by_subject(subj, days=7))

        if not recent:
            return DifficultyLevel.INTERMEDIATE

        # Calculate recent accuracy
        accuracy = sum(1 for r in recent if r.is_correct) / len(recent)

        # Adjust difficulty based on performance
        if accuracy >= 0.85:
            return DifficultyLevel.ADVANCED
        elif accuracy >= 0.70:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.FOUNDATIONAL

    def _calculate_card_priority(self, card: LearningCard,
                                 target_difficulty: DifficultyLevel) -> float:
        """
        Calculate priority score for a card
        Higher score = higher priority
        """
        score = 0.0

        # Difficulty alignment (prefer cards near target difficulty)
        diff_gap = abs(card.difficulty.value - target_difficulty.value)
        score += (5 - diff_gap) * 2

        # Prioritize low mastery cards
        score += (1 - card.mastery_level) * 10

        # Prioritize cards that haven't been reviewed recently
        if card.last_reviewed:
            days_since = (datetime.now() - card.last_reviewed).days
            score += min(days_since / 7, 5)  # Cap at 5 points for 35+ days
        else:
            score += 10  # Never reviewed gets high priority

        # Slight boost for cards overdue for review
        if card.is_due():
            days_overdue = (datetime.now() - card.next_review).days
            score += min(days_overdue * 2, 10)

        return score

    def generate_targeted_block(self,
                               subject: Subject,
                               topics: List[str],
                               block_size: int = 10) -> List[LearningCard]:
        """Generate block targeting specific topics"""
        all_cards = self.db.get_all_cards(subject=subject)

        # Filter to matching topics
        matching = [c for c in all_cards if c.topic in topics]

        if not matching:
            return []

        # Score by mastery and recency
        scored = [(c, (1 - c.mastery_level) * 5 +
                  ((datetime.now() - c.last_reviewed).days / 7
                   if c.last_reviewed else 10))
                 for c in matching]

        scored.sort(key=lambda x: x[1], reverse=True)

        # Take top cards
        selected = [c for c, _ in scored[:block_size]]
        random.shuffle(selected)

        return selected


# ============================================================================
# MAIN ADAPTIVE LEARNING SYSTEM
# ============================================================================

class AdaptiveLearningSystem:
    """
    Complete adaptive learning system combining:
    - SM-2 spaced repetition
    - Confidence-weighted scoring
    - SQLite persistence
    - Adaptive block generation
    - Performance analytics
    """

    def __init__(self, db_path: str = "adaptive_learning.db"):
        self.db = AdaptiveLearningDatabase(db_path)
        self.block_generator = AdaptiveBlockGenerator(self.db)
        self.current_session: Optional[StudySession] = None

    def add_card(self,
                subject: Subject,
                topic: Enum,  # ConstitutionalLawTopic or EvidenceTopic
                concept_name: str,
                question: str,
                answer: str,
                difficulty: DifficultyLevel,
                tags: Optional[List[str]] = None) -> LearningCard:
        """Add a new learning card"""
        card_id = f"{subject.value}_{topic.value}_{hash(concept_name) % 100000}"

        card = LearningCard(
            card_id=card_id,
            subject=subject,
            topic=topic.value,
            concept_name=concept_name,
            question=question,
            answer=answer,
            difficulty=difficulty,
            tags=tags or []
        )

        self.db.save_card(card)
        return card

    def start_session(self) -> StudySession:
        """Start a new study session"""
        self.current_session = StudySession()
        self.current_session.session_id = self.db.save_session(self.current_session)
        return self.current_session

    def end_session(self):
        """End current study session"""
        if self.current_session:
            self.current_session.end_time = datetime.now()

            # Calculate session quality
            if self.current_session.cards_reviewed > 0:
                self.current_session.session_quality = (
                    self.current_session.accuracy * 0.7 +
                    self.current_session.avg_confidence / 5 * 0.3
                )

            self.db.update_session(self.current_session)
            self.current_session = None

    def review_card(self,
                   card: LearningCard,
                   quality: int,
                   confidence: ConfidenceLevel,
                   time_taken: int) -> PerformanceRecord:
        """
        Review a card and update using SM-2 + confidence weighting

        Args:
            card: The learning card
            quality: Performance quality (0-5)
            confidence: Student's confidence level
            time_taken: Time spent on question (seconds)
        """
        # Update card using SM-2 algorithm
        card.review(quality, confidence)

        # Save updated card
        self.db.save_card(card)

        # Record performance
        record = PerformanceRecord(
            card_id=card.card_id,
            subject=card.subject.value,
            topic=card.topic,
            quality=quality,
            confidence=confidence.value,
            time_taken=time_taken,
            is_correct=(quality >= 3)
        )
        record.record_id = self.db.save_performance(record)

        # Update current session
        if self.current_session:
            self.current_session.cards_reviewed += 1
            if record.is_correct:
                self.current_session.cards_correct += 1

            if card.subject.value not in self.current_session.subjects_covered:
                self.current_session.subjects_covered.append(card.subject.value)

            # Update average confidence
            total_conf = (self.current_session.avg_confidence *
                         (self.current_session.cards_reviewed - 1) +
                         confidence.value)
            self.current_session.avg_confidence = total_conf / self.current_session.cards_reviewed

        return record

    def get_study_block(self, **kwargs) -> List[LearningCard]:
        """Get adaptive study block"""
        return self.block_generator.generate_block(**kwargs)

    def get_targeted_block(self, subject: Subject, topics: List[str],
                          block_size: int = 10) -> List[LearningCard]:
        """Get block targeting specific topics"""
        return self.block_generator.generate_targeted_block(subject, topics, block_size)

    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return self.db.get_statistics()

    def get_subject_performance(self, subject: Subject, days: int = 30) -> Dict[str, Any]:
        """Get detailed performance for a subject"""
        records = self.db.get_performance_by_subject(subject, days)

        if not records:
            return {
                'subject': subject.value,
                'total_reviews': 0,
                'accuracy': 0,
                'avg_confidence': 0,
                'avg_time': 0,
                'topic_breakdown': {}
            }

        # Calculate metrics
        total = len(records)
        correct = sum(1 for r in records if r.is_correct)
        avg_conf = mean(r.confidence for r in records)
        avg_time = mean(r.time_taken for r in records)

        # Topic breakdown
        topic_stats = {}
        for record in records:
            if record.topic not in topic_stats:
                topic_stats[record.topic] = {'total': 0, 'correct': 0}
            topic_stats[record.topic]['total'] += 1
            if record.is_correct:
                topic_stats[record.topic]['correct'] += 1

        # Calculate topic accuracies
        topic_breakdown = {
            topic: {
                'accuracy': stats['correct'] / stats['total'],
                'total_reviews': stats['total']
            }
            for topic, stats in topic_stats.items()
        }

        return {
            'subject': subject.value,
            'total_reviews': total,
            'accuracy': correct / total,
            'avg_confidence': avg_conf,
            'avg_time': avg_time,
            'topic_breakdown': topic_breakdown
        }

    def identify_weak_topics(self, subject: Subject,
                            threshold: float = 0.7) -> List[Tuple[str, float]]:
        """Identify topics below accuracy threshold"""
        perf = self.get_subject_performance(subject)

        weak_topics = [
            (topic, stats['accuracy'])
            for topic, stats in perf['topic_breakdown'].items()
            if stats['accuracy'] < threshold
        ]

        weak_topics.sort(key=lambda x: x[1])  # Sort by accuracy ascending
        return weak_topics

    def close(self):
        """Close database connection"""
        self.db.close()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def demo_system():
    """Demonstrate the adaptive learning system"""
    print("=" * 70)
    print("ADAPTIVE LEARNING SYSTEM - DEMONSTRATION")
    print("=" * 70)

    # Initialize system
    system = AdaptiveLearningSystem("demo_learning.db")

    # Add some Constitutional Law cards
    print("\n📚 Adding Constitutional Law cards...")

    system.add_card(
        subject=Subject.CONSTITUTIONAL_LAW,
        topic=ConstitutionalLawTopic.STRICT_SCRUTINY,
        concept_name="Strict Scrutiny Test",
        question="What are the elements of strict scrutiny review?",
        answer="The government must show: (1) compelling government interest, and (2) narrowly tailored means to achieve that interest.",
        difficulty=DifficultyLevel.INTERMEDIATE,
        tags=["equal_protection", "fundamental_rights"]
    )

    system.add_card(
        subject=Subject.CONSTITUTIONAL_LAW,
        topic=ConstitutionalLawTopic.FREEDOM_OF_SPEECH,
        concept_name="Content-Based Restrictions",
        question="What level of scrutiny applies to content-based speech restrictions?",
        answer="Strict scrutiny applies to content-based restrictions on speech.",
        difficulty=DifficultyLevel.ADVANCED,
        tags=["first_amendment", "speech"]
    )

    # Add some Evidence cards
    print("📚 Adding Evidence cards...")

    system.add_card(
        subject=Subject.EVIDENCE,
        topic=EvidenceTopic.HEARSAY_DEFINITION,
        concept_name="Hearsay Definition",
        question="What is hearsay under FRE 801?",
        answer="Hearsay is an out-of-court statement offered to prove the truth of the matter asserted.",
        difficulty=DifficultyLevel.FOUNDATIONAL,
        tags=["hearsay", "FRE_801"]
    )

    system.add_card(
        subject=Subject.EVIDENCE,
        topic=EvidenceTopic.EXCITED_UTTERANCE,
        concept_name="Excited Utterance Exception",
        question="What is the excited utterance exception to hearsay?",
        answer="Under FRE 803(2), a statement relating to a startling event made while under the stress of excitement is admissible.",
        difficulty=DifficultyLevel.INTERMEDIATE,
        tags=["hearsay", "FRE_803", "exceptions"]
    )

    # Get statistics
    stats = system.get_statistics()
    print(f"\n✅ Added {stats['total_cards']} cards")
    print(f"📊 Cards by subject: {stats['cards_by_subject']}")

    # Start a study session
    print("\n🎯 Starting study session...")
    session = system.start_session()

    # Get adaptive block
    block = system.get_study_block(block_size=2, include_new=True)
    print(f"\n📖 Generated block with {len(block)} cards")

    # Simulate reviewing cards
    for i, card in enumerate(block, 1):
        print(f"\n--- Card {i} ---")
        print(f"Subject: {card.subject.value}")
        print(f"Topic: {card.topic}")
        print(f"Q: {card.question}")

        # Simulate review (in real use, get user input)
        quality = 4  # Correct with hesitation
        confidence = ConfidenceLevel.CONFIDENT
        time_taken = 45

        record = system.review_card(card, quality, confidence, time_taken)
        print(f"✓ Reviewed (Quality: {quality}, Confidence: {confidence.name})")

    # End session
    system.end_session()
    print(f"\n✅ Session complete!")
    print(f"   Accuracy: {session.accuracy * 100:.1f}%")
    print(f"   Avg Confidence: {session.avg_confidence:.2f}/5")

    # Show performance
    print("\n📊 CONSTITUTIONAL LAW PERFORMANCE")
    print("-" * 70)
    conlaw_perf = system.get_subject_performance(Subject.CONSTITUTIONAL_LAW)
    print(f"Total Reviews: {conlaw_perf['total_reviews']}")
    print(f"Accuracy: {conlaw_perf['accuracy'] * 100:.1f}%")
    print(f"Avg Confidence: {conlaw_perf['avg_confidence']:.2f}/5")

    print("\n📊 EVIDENCE PERFORMANCE")
    print("-" * 70)
    evidence_perf = system.get_subject_performance(Subject.EVIDENCE)
    print(f"Total Reviews: {evidence_perf['total_reviews']}")
    print(f"Accuracy: {evidence_perf['accuracy'] * 100:.1f}%")
    print(f"Avg Confidence: {evidence_perf['avg_confidence']:.2f}/5")

    # Clean up
    system.close()

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo_system()

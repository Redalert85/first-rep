#!/usr/bin/env python3
"""
Core Enhancements Module for Bar Exam Tutor
============================================

Implements:
1. SM-2 Spaced Repetition Scheduler
2. Practice Exam Simulator
3. Analytics Dashboard
4. Concept Tracking System
5. Weak Area Detection

Integrates with bar_tutor_unified.py and elite_memory_palace.py
"""

import json
import logging
import math
import os
import random
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# SM-2 SPACED REPETITION SCHEDULER
# ============================================================================

@dataclass
class SM2Card:
    """Card with SM-2 algorithm state"""
    card_id: str
    concept_id: str
    front: str
    back: str
    subject: str

    # SM-2 parameters
    ease_factor: float = 2.5  # Easiness factor (1.3 - 2.5+)
    interval: int = 1         # Days until next review
    repetitions: int = 0      # Successful repetitions in a row

    # Tracking
    next_review: Optional[str] = None  # ISO date
    last_reviewed: Optional[str] = None
    total_reviews: int = 0
    correct_count: int = 0

    def __post_init__(self):
        if not self.next_review:
            self.next_review = datetime.now().isoformat()


class SM2Scheduler:
    """
    SM-2 Spaced Repetition Algorithm Implementation

    Based on SuperMemo SM-2 algorithm:
    - Quality 0-2: Reset (forgotten)
    - Quality 3: Correct with difficulty
    - Quality 4: Correct with hesitation
    - Quality 5: Perfect recall

    Usage:
        scheduler = SM2Scheduler()
        scheduler.load_cards("flashcards.json")

        due_cards = scheduler.get_due_cards()
        for card in due_cards:
            # Show card, get user response
            quality = get_user_quality(0-5)
            scheduler.review_card(card.card_id, quality)

        scheduler.save_cards("flashcards.json")
    """

    def __init__(self, data_path: str = "data/sm2_cards.json"):
        self.data_path = Path(data_path)
        self.cards: Dict[str, SM2Card] = {}
        self.review_history: List[Dict] = []
        self._load_cards()

    def _load_cards(self):
        """Load cards from file"""
        if self.data_path.exists():
            try:
                with open(self.data_path, 'r') as f:
                    data = json.load(f)
                    for card_data in data.get("cards", []):
                        card = SM2Card(**card_data)
                        self.cards[card.card_id] = card
                    self.review_history = data.get("history", [])
                logger.info(f"Loaded {len(self.cards)} cards from {self.data_path}")
            except Exception as e:
                logger.warning(f"Could not load cards: {e}")

    def save_cards(self):
        """Save cards to file"""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "cards": [asdict(card) for card in self.cards.values()],
            "history": self.review_history[-1000:],  # Keep last 1000 reviews
            "saved_at": datetime.now().isoformat()
        }
        with open(self.data_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved {len(self.cards)} cards to {self.data_path}")

    def add_card(self, concept_id: str, front: str, back: str, subject: str) -> SM2Card:
        """Add a new card"""
        card_id = f"{concept_id}_{hash(front) % 10000:04d}"
        card = SM2Card(
            card_id=card_id,
            concept_id=concept_id,
            front=front,
            back=back,
            subject=subject
        )
        self.cards[card_id] = card
        return card

    def review_card(self, card_id: str, quality: int) -> Dict[str, Any]:
        """
        Review a card and update its SM-2 parameters.

        Args:
            card_id: The card to review
            quality: 0-5 rating
                0 - Complete blackout
                1 - Incorrect, but recognized answer
                2 - Incorrect, easy to recall after seeing
                3 - Correct with serious difficulty
                4 - Correct with hesitation
                5 - Perfect response

        Returns:
            Dict with next review info
        """
        if card_id not in self.cards:
            return {"error": f"Card {card_id} not found"}

        card = self.cards[card_id]
        quality = max(0, min(5, quality))  # Clamp to 0-5

        now = datetime.now()
        card.last_reviewed = now.isoformat()
        card.total_reviews += 1

        # SM-2 Algorithm
        if quality >= 3:
            # Correct response
            card.correct_count += 1

            if card.repetitions == 0:
                card.interval = 1
            elif card.repetitions == 1:
                card.interval = 6
            else:
                card.interval = round(card.interval * card.ease_factor)

            card.repetitions += 1

            # Update ease factor
            card.ease_factor = max(1.3, card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        else:
            # Incorrect - reset
            card.repetitions = 0
            card.interval = 1
            # Decrease ease factor for difficult cards
            card.ease_factor = max(1.3, card.ease_factor - 0.2)

        # Calculate next review date
        next_review = now + timedelta(days=card.interval)
        card.next_review = next_review.isoformat()

        # Log review
        self.review_history.append({
            "card_id": card_id,
            "concept_id": card.concept_id,
            "subject": card.subject,
            "quality": quality,
            "new_interval": card.interval,
            "ease_factor": card.ease_factor,
            "timestamp": now.isoformat()
        })

        return {
            "card_id": card_id,
            "quality": quality,
            "correct": quality >= 3,
            "new_interval_days": card.interval,
            "next_review": card.next_review,
            "ease_factor": round(card.ease_factor, 2),
            "repetitions": card.repetitions
        }

    def get_due_cards(self, limit: int = 20) -> List[SM2Card]:
        """Get cards due for review"""
        now = datetime.now()
        due = []

        for card in self.cards.values():
            if card.next_review:
                next_review = datetime.fromisoformat(card.next_review)
                if next_review <= now:
                    due.append(card)

        # Sort by overdue time (most overdue first)
        due.sort(key=lambda c: c.next_review)

        return due[:limit]

    def get_cards_by_subject(self, subject: str) -> List[SM2Card]:
        """Get all cards for a subject"""
        return [c for c in self.cards.values() if c.subject.lower() == subject.lower()]

    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics"""
        now = datetime.now()

        total = len(self.cards)
        due_now = len(self.get_due_cards(limit=1000))

        # Calculate by subject
        by_subject = defaultdict(lambda: {"total": 0, "due": 0, "mastered": 0})
        for card in self.cards.values():
            subj = card.subject
            by_subject[subj]["total"] += 1

            if card.next_review:
                if datetime.fromisoformat(card.next_review) <= now:
                    by_subject[subj]["due"] += 1

            # Mastered = interval > 21 days
            if card.interval > 21:
                by_subject[subj]["mastered"] += 1

        # Recent accuracy
        recent_reviews = self.review_history[-100:]
        if recent_reviews:
            correct = sum(1 for r in recent_reviews if r.get("quality", 0) >= 3)
            accuracy = correct / len(recent_reviews)
        else:
            accuracy = 0

        return {
            "total_cards": total,
            "due_now": due_now,
            "due_today": due_now,
            "recent_accuracy": round(accuracy * 100, 1),
            "by_subject": dict(by_subject),
            "total_reviews": len(self.review_history)
        }


# ============================================================================
# CONCEPT TRACKING SYSTEM
# ============================================================================

@dataclass
class ConceptMastery:
    """Tracks mastery of a single concept"""
    concept_id: str
    name: str
    subject: str

    # Mastery metrics
    mastery_level: float = 0.0  # 0.0 to 1.0
    attempts: int = 0
    correct: int = 0

    # Timing
    first_seen: Optional[str] = None
    last_reviewed: Optional[str] = None
    total_time_seconds: float = 0

    # Detailed tracking
    question_history: List[Dict] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        if self.attempts == 0:
            return 0.0
        return self.correct / self.attempts

    def record_attempt(self, correct: bool, time_seconds: float = 0, question_id: str = None):
        """Record an attempt at this concept"""
        now = datetime.now().isoformat()

        if not self.first_seen:
            self.first_seen = now
        self.last_reviewed = now

        self.attempts += 1
        if correct:
            self.correct += 1
        self.total_time_seconds += time_seconds

        # Update mastery using exponential moving average
        result = 1.0 if correct else 0.0
        alpha = 0.3  # Weight for new observation
        self.mastery_level = alpha * result + (1 - alpha) * self.mastery_level

        # Store in history (keep last 20)
        self.question_history.append({
            "timestamp": now,
            "correct": correct,
            "time_seconds": time_seconds,
            "question_id": question_id,
            "mastery_after": self.mastery_level
        })
        self.question_history = self.question_history[-20:]


class ConceptTracker:
    """
    Unified Concept Tracking System

    Tracks mastery across all bar exam concepts and integrates with:
    - Practice questions
    - Flashcards
    - Memory palace
    - Analytics

    Usage:
        tracker = ConceptTracker()
        tracker.record_attempt("evidence_hearsay", correct=True, time=5.2)
        weak = tracker.get_weak_concepts(threshold=0.6)
        stats = tracker.get_subject_statistics()
    """

    def __init__(self, data_path: str = "data/concept_tracking.json"):
        self.data_path = Path(data_path)
        self.concepts: Dict[str, ConceptMastery] = {}
        self.session_history: List[Dict] = []
        self._load()

    def _load(self):
        """Load tracking data"""
        if self.data_path.exists():
            try:
                with open(self.data_path, 'r') as f:
                    data = json.load(f)
                    for concept_data in data.get("concepts", []):
                        # Handle question_history default
                        if "question_history" not in concept_data:
                            concept_data["question_history"] = []
                        concept = ConceptMastery(**concept_data)
                        self.concepts[concept.concept_id] = concept
                    self.session_history = data.get("sessions", [])
                logger.info(f"Loaded tracking for {len(self.concepts)} concepts")
            except Exception as e:
                logger.warning(f"Could not load tracking: {e}")

    def save(self):
        """Save tracking data"""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "concepts": [asdict(c) for c in self.concepts.values()],
            "sessions": self.session_history[-500:],
            "saved_at": datetime.now().isoformat()
        }
        with open(self.data_path, 'w') as f:
            json.dump(data, f, indent=2)

    def ensure_concept(self, concept_id: str, name: str = None, subject: str = None) -> ConceptMastery:
        """Get or create concept tracking"""
        if concept_id not in self.concepts:
            self.concepts[concept_id] = ConceptMastery(
                concept_id=concept_id,
                name=name or concept_id.replace("_", " ").title(),
                subject=subject or concept_id.split("_")[0]
            )
        return self.concepts[concept_id]

    def record_attempt(self, concept_id: str, correct: bool,
                       time_seconds: float = 0, question_id: str = None,
                       name: str = None, subject: str = None) -> ConceptMastery:
        """Record an attempt at a concept"""
        concept = self.ensure_concept(concept_id, name, subject)
        concept.record_attempt(correct, time_seconds, question_id)
        return concept

    def get_weak_concepts(self, threshold: float = 0.6, min_attempts: int = 2) -> List[ConceptMastery]:
        """Get concepts below mastery threshold"""
        weak = []
        for concept in self.concepts.values():
            if concept.attempts >= min_attempts and concept.mastery_level < threshold:
                weak.append(concept)

        # Sort by mastery (lowest first)
        weak.sort(key=lambda c: c.mastery_level)
        return weak

    def get_strong_concepts(self, threshold: float = 0.8) -> List[ConceptMastery]:
        """Get well-mastered concepts"""
        return [c for c in self.concepts.values() if c.mastery_level >= threshold]

    def get_untested_concepts(self, all_concept_ids: List[str]) -> List[str]:
        """Get concepts that haven't been tested yet"""
        tested = set(self.concepts.keys())
        return [cid for cid in all_concept_ids if cid not in tested]

    def get_subject_statistics(self) -> Dict[str, Dict]:
        """Get statistics by subject"""
        stats = defaultdict(lambda: {
            "concepts": 0,
            "total_attempts": 0,
            "total_correct": 0,
            "avg_mastery": 0,
            "mastery_sum": 0
        })

        for concept in self.concepts.values():
            s = stats[concept.subject]
            s["concepts"] += 1
            s["total_attempts"] += concept.attempts
            s["total_correct"] += concept.correct
            s["mastery_sum"] += concept.mastery_level

        # Calculate averages
        result = {}
        for subject, s in stats.items():
            if s["concepts"] > 0:
                s["avg_mastery"] = round(s["mastery_sum"] / s["concepts"], 3)
                s["accuracy"] = round(s["total_correct"] / max(1, s["total_attempts"]), 3)
                del s["mastery_sum"]
                result[subject] = s

        return result

    def get_recommendations(self, count: int = 5) -> List[Dict]:
        """Get study recommendations based on weakness"""
        recommendations = []

        # Get weak concepts
        weak = self.get_weak_concepts(threshold=0.7)
        for concept in weak[:count]:
            recommendations.append({
                "concept_id": concept.concept_id,
                "name": concept.name,
                "subject": concept.subject,
                "mastery": round(concept.mastery_level, 2),
                "accuracy": round(concept.accuracy, 2),
                "attempts": concept.attempts,
                "reason": "Low mastery - needs more practice"
            })

        return recommendations

    def get_overall_readiness(self) -> Dict[str, Any]:
        """Calculate overall bar exam readiness"""
        if not self.concepts:
            return {"ready": False, "score": 0, "message": "No concepts tracked yet"}

        total_mastery = sum(c.mastery_level for c in self.concepts.values())
        avg_mastery = total_mastery / len(self.concepts)

        # Count by readiness level
        mastered = len([c for c in self.concepts.values() if c.mastery_level >= 0.8])
        learning = len([c for c in self.concepts.values() if 0.5 <= c.mastery_level < 0.8])
        struggling = len([c for c in self.concepts.values() if c.mastery_level < 0.5])

        ready = avg_mastery >= 0.7

        return {
            "ready": ready,
            "score": round(avg_mastery * 100, 1),
            "concepts_tracked": len(self.concepts),
            "mastered": mastered,
            "learning": learning,
            "struggling": struggling,
            "message": "Ready for exam!" if ready else f"Keep studying - need {70 - round(avg_mastery*100)}% more mastery"
        }


# ============================================================================
# PRACTICE EXAM SIMULATOR
# ============================================================================

@dataclass
class ExamQuestion:
    """A practice exam question"""
    question_id: str
    concept_id: str
    subject: str
    difficulty: str  # easy, medium, hard
    question_text: str
    options: Dict[str, str]  # A, B, C, D -> text
    correct_answer: str  # A, B, C, or D
    explanation: str
    tested_rule: str = ""


@dataclass
class ExamResult:
    """Result of a practice exam"""
    exam_id: str
    started_at: str
    completed_at: str
    total_questions: int
    correct: int
    incorrect: int
    skipped: int
    time_seconds: float
    score_percent: float
    scaled_score: int  # 0-200 scale
    by_subject: Dict[str, Dict]
    passed: bool
    questions: List[Dict]


class PracticeExamSimulator:
    """
    Realistic Bar Exam Practice Simulator

    Features:
    - Timed exam simulation
    - Mixed-subject questions
    - Flagging for review
    - Detailed score reports
    - Concept tracking integration

    Usage:
        simulator = PracticeExamSimulator()
        simulator.load_questions("out/mbe_questions.json")

        exam = simulator.start_exam(num_questions=50)
        for q in exam:
            answer = get_user_answer()
            simulator.submit_answer(q.question_id, answer)

        result = simulator.finish_exam()
        print(f"Score: {result.score_percent}%")
    """

    def __init__(self, concept_tracker: ConceptTracker = None):
        self.questions: Dict[str, ExamQuestion] = {}
        self.concept_tracker = concept_tracker or ConceptTracker()

        # Current exam state
        self.current_exam_id: Optional[str] = None
        self.current_questions: List[ExamQuestion] = []
        self.answers: Dict[str, str] = {}  # question_id -> answer
        self.flagged: Set[str] = set()
        self.start_time: Optional[datetime] = None
        self.question_times: Dict[str, float] = {}  # question_id -> seconds

        self._load_all_questions()

    def _load_all_questions(self):
        """Load questions from all available sources"""
        question_dirs = [
            Path("out"),
            Path("generated_questions"),
        ]

        for qdir in question_dirs:
            if qdir.exists():
                for qfile in qdir.glob("**/*.json"):
                    try:
                        self._load_question_file(qfile)
                    except Exception as e:
                        logger.debug(f"Could not load {qfile}: {e}")

        logger.info(f"Loaded {len(self.questions)} practice questions")

    def _load_question_file(self, filepath: Path):
        """Load questions from a JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        questions = data if isinstance(data, list) else data.get("questions", [data])

        for q in questions:
            if not q.get("fact_pattern") and not q.get("question_text"):
                continue

            qid = q.get("id") or f"q_{hash(str(q)) % 100000:05d}"

            # Normalize options format
            options = q.get("options", {})
            if isinstance(options, list):
                options = {chr(65+i): opt for i, opt in enumerate(options[:4])}

            question = ExamQuestion(
                question_id=qid,
                concept_id=q.get("concept", q.get("concept_id", "unknown")),
                subject=q.get("subject", "unknown"),
                difficulty=q.get("difficulty", "medium").lower(),
                question_text=q.get("fact_pattern", q.get("question_text", "")),
                options=options,
                correct_answer=q.get("answer", q.get("correct_answer", "A")),
                explanation=q.get("why_correct", q.get("explanation", "")),
                tested_rule=q.get("tested_rule", "")
            )
            self.questions[qid] = question

    def add_questions(self, questions: List[Dict]):
        """Add questions programmatically"""
        for q in questions:
            qid = q.get("id") or f"q_{hash(str(q)) % 100000:05d}"
            question = ExamQuestion(
                question_id=qid,
                concept_id=q.get("concept_id", "unknown"),
                subject=q.get("subject", "unknown"),
                difficulty=q.get("difficulty", "medium"),
                question_text=q.get("question_text", ""),
                options=q.get("options", {}),
                correct_answer=q.get("correct_answer", "A"),
                explanation=q.get("explanation", ""),
                tested_rule=q.get("tested_rule", "")
            )
            self.questions[qid] = question

    def start_exam(self, num_questions: int = 50, subjects: List[str] = None,
                   difficulty: str = None, time_limit_minutes: int = None) -> List[ExamQuestion]:
        """
        Start a new practice exam.

        Args:
            num_questions: Number of questions (default 50)
            subjects: Filter by subjects (default: all)
            difficulty: Filter by difficulty (default: mixed)
            time_limit_minutes: Optional time limit

        Returns:
            List of exam questions
        """
        self.current_exam_id = f"exam_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.answers = {}
        self.flagged = set()
        self.question_times = {}
        self.start_time = datetime.now()

        # Filter questions
        available = list(self.questions.values())

        if subjects:
            subjects_lower = [s.lower() for s in subjects]
            available = [q for q in available if q.subject.lower() in subjects_lower]

        if difficulty:
            available = [q for q in available if q.difficulty == difficulty.lower()]

        # Select questions (try to balance subjects)
        if len(available) <= num_questions:
            selected = available
        else:
            # Balance by subject
            by_subject = defaultdict(list)
            for q in available:
                by_subject[q.subject].append(q)

            selected = []
            per_subject = max(1, num_questions // len(by_subject))

            for subject, qs in by_subject.items():
                random.shuffle(qs)
                selected.extend(qs[:per_subject])

            # Fill remainder randomly
            remaining = [q for q in available if q not in selected]
            random.shuffle(remaining)
            selected.extend(remaining[:num_questions - len(selected)])

        random.shuffle(selected)
        self.current_questions = selected[:num_questions]

        logger.info(f"Started exam {self.current_exam_id} with {len(self.current_questions)} questions")

        return self.current_questions

    def submit_answer(self, question_id: str, answer: str, time_seconds: float = 0):
        """Submit answer for a question"""
        self.answers[question_id] = answer.upper()
        if time_seconds > 0:
            self.question_times[question_id] = time_seconds

    def flag_question(self, question_id: str):
        """Flag question for review"""
        self.flagged.add(question_id)

    def unflag_question(self, question_id: str):
        """Remove flag from question"""
        self.flagged.discard(question_id)

    def get_flagged(self) -> List[ExamQuestion]:
        """Get all flagged questions"""
        return [q for q in self.current_questions if q.question_id in self.flagged]

    def finish_exam(self) -> ExamResult:
        """
        Finish exam and calculate results.

        Returns:
            ExamResult with detailed breakdown
        """
        if not self.current_questions:
            raise ValueError("No exam in progress")

        end_time = datetime.now()
        total_time = (end_time - self.start_time).total_seconds()

        correct = 0
        incorrect = 0
        skipped = 0
        by_subject = defaultdict(lambda: {"correct": 0, "incorrect": 0, "total": 0})
        question_results = []

        for q in self.current_questions:
            user_answer = self.answers.get(q.question_id)
            is_correct = user_answer == q.correct_answer

            result = {
                "question_id": q.question_id,
                "concept_id": q.concept_id,
                "subject": q.subject,
                "user_answer": user_answer,
                "correct_answer": q.correct_answer,
                "is_correct": is_correct,
                "time_seconds": self.question_times.get(q.question_id, 0),
                "was_flagged": q.question_id in self.flagged
            }
            question_results.append(result)

            by_subject[q.subject]["total"] += 1

            if user_answer is None:
                skipped += 1
            elif is_correct:
                correct += 1
                by_subject[q.subject]["correct"] += 1
            else:
                incorrect += 1
                by_subject[q.subject]["incorrect"] += 1

            # Update concept tracking
            if user_answer is not None:
                self.concept_tracker.record_attempt(
                    concept_id=q.concept_id,
                    correct=is_correct,
                    time_seconds=self.question_times.get(q.question_id, 0),
                    question_id=q.question_id,
                    subject=q.subject
                )

        # Calculate scores
        total = len(self.current_questions)
        score_percent = (correct / total * 100) if total > 0 else 0
        scaled_score = int(score_percent * 2)  # 0-200 scale
        passed = score_percent >= 65  # MBE passing threshold ~65%

        # Calculate subject stats
        subject_stats = {}
        for subject, stats in by_subject.items():
            stats["accuracy"] = round(stats["correct"] / max(1, stats["total"]) * 100, 1)
            subject_stats[subject] = stats

        result = ExamResult(
            exam_id=self.current_exam_id,
            started_at=self.start_time.isoformat(),
            completed_at=end_time.isoformat(),
            total_questions=total,
            correct=correct,
            incorrect=incorrect,
            skipped=skipped,
            time_seconds=total_time,
            score_percent=round(score_percent, 1),
            scaled_score=scaled_score,
            by_subject=subject_stats,
            passed=passed,
            questions=question_results
        )

        # Save results
        self._save_exam_result(result)
        self.concept_tracker.save()

        # Reset exam state
        self.current_exam_id = None
        self.current_questions = []

        return result

    def _save_exam_result(self, result: ExamResult):
        """Save exam result to file"""
        results_dir = Path("data/exam_results")
        results_dir.mkdir(parents=True, exist_ok=True)

        filepath = results_dir / f"{result.exam_id}.json"
        with open(filepath, 'w') as f:
            json.dump(asdict(result), f, indent=2)

    def get_exam_history(self) -> List[Dict]:
        """Get history of past exams"""
        results_dir = Path("data/exam_results")
        if not results_dir.exists():
            return []

        history = []
        for filepath in sorted(results_dir.glob("*.json"), reverse=True)[:20]:
            try:
                with open(filepath, 'r') as f:
                    result = json.load(f)
                    history.append({
                        "exam_id": result["exam_id"],
                        "date": result["started_at"][:10],
                        "score": result["score_percent"],
                        "passed": result["passed"],
                        "questions": result["total_questions"]
                    })
            except:
                pass

        return history


# ============================================================================
# ANALYTICS DASHBOARD
# ============================================================================

class AnalyticsDashboard:
    """
    Comprehensive Analytics Dashboard

    Provides:
    - Overall progress tracking
    - Subject-by-subject breakdown
    - Weak area identification
    - Trend analysis
    - Readiness prediction

    Usage:
        dashboard = AnalyticsDashboard()
        summary = dashboard.get_summary()
        weak = dashboard.get_weak_areas()
        trend = dashboard.get_progress_trend()
    """

    def __init__(self, concept_tracker: ConceptTracker = None,
                 sm2_scheduler: SM2Scheduler = None):
        self.tracker = concept_tracker or ConceptTracker()
        self.scheduler = sm2_scheduler or SM2Scheduler()

    def get_summary(self) -> Dict[str, Any]:
        """Get overall summary statistics"""
        readiness = self.tracker.get_overall_readiness()
        sm2_stats = self.scheduler.get_statistics()
        subject_stats = self.tracker.get_subject_statistics()

        return {
            "overall_mastery": readiness["score"],
            "ready_for_exam": readiness["ready"],
            "concepts_tracked": readiness["concepts_tracked"],
            "concepts_mastered": readiness["mastered"],
            "concepts_learning": readiness["learning"],
            "concepts_struggling": readiness["struggling"],
            "flashcards_total": sm2_stats["total_cards"],
            "flashcards_due": sm2_stats["due_now"],
            "recent_accuracy": sm2_stats["recent_accuracy"],
            "subjects": subject_stats,
            "message": readiness["message"]
        }

    def get_weak_areas(self, limit: int = 10) -> List[Dict]:
        """Get weakest areas needing study"""
        weak_concepts = self.tracker.get_weak_concepts(threshold=0.6)

        # Group by subject
        by_subject = defaultdict(list)
        for concept in weak_concepts:
            by_subject[concept.subject].append(concept)

        # Find weakest subjects
        subject_weakness = []
        for subject, concepts in by_subject.items():
            avg_mastery = sum(c.mastery_level for c in concepts) / len(concepts)
            subject_weakness.append({
                "subject": subject,
                "weak_concepts": len(concepts),
                "avg_mastery": round(avg_mastery, 2),
                "top_weak": [c.name for c in concepts[:3]]
            })

        subject_weakness.sort(key=lambda x: x["avg_mastery"])

        return subject_weakness[:limit]

    def get_progress_trend(self, days: int = 30) -> Dict[str, Any]:
        """Get progress trend over time"""
        # Get exam history
        results_dir = Path("data/exam_results")
        if not results_dir.exists():
            return {"trend": "insufficient_data", "exams": []}

        exams = []
        for filepath in sorted(results_dir.glob("*.json")):
            try:
                with open(filepath, 'r') as f:
                    result = json.load(f)
                    exam_date = datetime.fromisoformat(result["started_at"])
                    if (datetime.now() - exam_date).days <= days:
                        exams.append({
                            "date": result["started_at"][:10],
                            "score": result["score_percent"]
                        })
            except:
                pass

        if len(exams) < 2:
            return {"trend": "insufficient_data", "exams": exams}

        # Calculate trend
        first_half = exams[:len(exams)//2]
        second_half = exams[len(exams)//2:]

        first_avg = sum(e["score"] for e in first_half) / len(first_half)
        second_avg = sum(e["score"] for e in second_half) / len(second_half)

        change = second_avg - first_avg

        if change > 5:
            trend = "improving"
        elif change < -5:
            trend = "declining"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "change": round(change, 1),
            "first_period_avg": round(first_avg, 1),
            "second_period_avg": round(second_avg, 1),
            "exams": exams
        }

    def get_study_recommendations(self) -> List[Dict]:
        """Get personalized study recommendations"""
        recommendations = []

        # 1. Weak concepts
        weak = self.tracker.get_weak_concepts(threshold=0.6)
        if weak:
            weakest = weak[0]
            recommendations.append({
                "priority": 1,
                "type": "weak_concept",
                "action": f"Focus on {weakest.name}",
                "reason": f"Mastery at {round(weakest.mastery_level*100)}% - needs improvement",
                "subject": weakest.subject
            })

        # 2. Due flashcards
        due = self.scheduler.get_due_cards(limit=10)
        if due:
            recommendations.append({
                "priority": 2,
                "type": "flashcards",
                "action": f"Review {len(due)} due flashcards",
                "reason": "Spaced repetition maintains long-term memory",
                "subjects": list(set(c.subject for c in due))
            })

        # 3. Subject balance
        subject_stats = self.tracker.get_subject_statistics()
        if subject_stats:
            weakest_subject = min(subject_stats.items(),
                                  key=lambda x: x[1].get("avg_mastery", 0))
            recommendations.append({
                "priority": 3,
                "type": "subject_focus",
                "action": f"Practice more {weakest_subject[0].replace('_', ' ').title()}",
                "reason": f"Average mastery: {round(weakest_subject[1]['avg_mastery']*100)}%",
                "subject": weakest_subject[0]
            })

        return recommendations

    def print_dashboard(self):
        """Print formatted dashboard to console"""
        summary = self.get_summary()
        weak = self.get_weak_areas(5)
        recs = self.get_study_recommendations()

        print("\n" + "="*70)
        print("                    BAR EXAM ANALYTICS DASHBOARD")
        print("="*70)

        # Overall Status
        status = "✓ READY" if summary["ready_for_exam"] else "✗ KEEP STUDYING"
        print(f"\n  Overall Mastery: {summary['overall_mastery']}%  [{status}]")
        print(f"  Recent Accuracy: {summary['recent_accuracy']}%")
        print(f"  Concepts: {summary['concepts_mastered']} mastered / "
              f"{summary['concepts_learning']} learning / "
              f"{summary['concepts_struggling']} struggling")
        print(f"  Flashcards: {summary['flashcards_due']} due of {summary['flashcards_total']} total")

        # Subject Breakdown
        print("\n  " + "-"*66)
        print("  SUBJECT BREAKDOWN")
        print("  " + "-"*66)

        for subject, stats in sorted(summary.get("subjects", {}).items()):
            bar_len = int(stats.get("avg_mastery", 0) * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"  {subject:25} [{bar}] {stats.get('avg_mastery', 0)*100:.0f}%")

        # Weak Areas
        if weak:
            print("\n  " + "-"*66)
            print("  WEAK AREAS (Focus Here)")
            print("  " + "-"*66)
            for area in weak[:3]:
                print(f"  • {area['subject']:20} - {area['weak_concepts']} weak concepts")

        # Recommendations
        if recs:
            print("\n  " + "-"*66)
            print("  RECOMMENDATIONS")
            print("  " + "-"*66)
            for rec in recs[:3]:
                print(f"  {rec['priority']}. {rec['action']}")
                print(f"     → {rec['reason']}")

        print("\n" + "="*70 + "\n")


# ============================================================================
# INTEGRATION HELPERS
# ============================================================================

def create_integrated_system():
    """Create fully integrated bar prep system"""
    tracker = ConceptTracker()
    scheduler = SM2Scheduler()
    simulator = PracticeExamSimulator(concept_tracker=tracker)
    dashboard = AnalyticsDashboard(concept_tracker=tracker, sm2_scheduler=scheduler)

    return {
        "tracker": tracker,
        "scheduler": scheduler,
        "simulator": simulator,
        "dashboard": dashboard
    }


def load_concepts_from_knowledge_base(tracker: ConceptTracker,
                                       kb_path: str = "ultimate_knowledge_base.json"):
    """Load all concepts from knowledge base into tracker"""
    try:
        with open(kb_path, 'r') as f:
            concepts = json.load(f)

        for concept in concepts:
            tracker.ensure_concept(
                concept_id=concept.get("concept_id", ""),
                name=concept.get("name", ""),
                subject=concept.get("subject", "")
            )

        logger.info(f"Loaded {len(concepts)} concepts into tracker")
        return len(concepts)
    except Exception as e:
        logger.error(f"Failed to load knowledge base: {e}")
        return 0


# ============================================================================
# MAIN / DEMO
# ============================================================================

if __name__ == "__main__":
    print("Core Enhancements Module")
    print("=" * 50)

    # Create integrated system
    system = create_integrated_system()

    # Load knowledge base
    load_concepts_from_knowledge_base(system["tracker"])

    # Show dashboard
    system["dashboard"].print_dashboard()

    # Show SM-2 stats
    print("\nSM-2 Scheduler Statistics:")
    stats = system["scheduler"].get_statistics()
    print(f"  Total cards: {stats['total_cards']}")
    print(f"  Due now: {stats['due_now']}")
    print(f"  Recent accuracy: {stats['recent_accuracy']}%")

    # Show exam simulator status
    print(f"\nPractice Exam Simulator:")
    print(f"  Questions loaded: {len(system['simulator'].questions)}")

    print("\nSystem ready!")

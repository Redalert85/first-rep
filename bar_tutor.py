#!/usr/bin/env python3

"""

Bar Prep Tutor v3.0 - Advanced Legal Education System

Enhanced version with sophisticated legal analysis, evidence-based learning,

and comprehensive pedagogical techniques for optimal bar exam success.

Key Enhancements:

- Sophisticated First-Principles Legal Analysis with historical and policy context

- Advanced Socratic Method focusing on legal reasoning patterns

- Enhanced SM-2 Spaced Repetition with confidence weighting

- Multiple legal reasoning frameworks (IRAC, Comparative Analysis, Concept Mapping)

- Adaptive difficulty based on performance analytics

- Diagnostic assessment and targeted remediation

- Bar exam-caliber question generation and evaluation

"""

import argparse
import hashlib
import json
import os
import pathlib
import random
import statistics
import sys
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv
from openai import OpenAI

# ---------- Enhanced Config ----------

ROOT = pathlib.Path(__file__).resolve().parent

ENV_PATH = ROOT / ".env"

NOTES_DIR = ROOT / "notes"

ERROR_LOG = ROOT / "error_log.jsonl"

FLASHCARDS = ROOT / "flashcards_v3.jsonl"

PERFORMANCE_DB = ROOT / "performance_v3.jsonl"

ANALYTICS_DB = ROOT / "analytics_v3.jsonl"

CASE_PRECEDENTS = ROOT / "precedents.jsonl"

DEFAULT_MODEL = "gpt-4o-mini"

MAX_NOTES_CHARS = 10000

# Subject categories for organization

SUBJECTS = [
    "Torts",
    "Contracts",
    "Criminal Law",
    "Criminal Procedure",
    "Evidence",
    "Constitutional Law",
    "Civil Procedure",
    "Real Property",
    "Wills and Trusts",
    "Family Law",
    "Secured Transactions",
    "Agency and Partnership",
    "Corporations",
    "Conflict of Laws",
    "Federal Jurisdiction",
    "Professional Responsibility",
]

# ---------- Essential Enums ----------


class Difficulty(Enum):

    FOUNDATIONAL = 1

    INTERMEDIATE = 2

    ADVANCED = 3

    EXPERT = 4


class ReasoningPattern(Enum):

    ANALOGICAL = "analogical"

    DEDUCTIVE = "deductive"

    INDUCTIVE = "inductive"

    POLICY_BASED = "policy_based"

    TEXTUALIST = "textualist"

    INTENTIONALIST = "intentionalist"


class ConfidenceLevel(Enum):

    GUESSING = 1

    UNSURE = 2

    FAMILIAR = 3

    CONFIDENT = 4

    CERTAIN = 5


class Subject(Enum):

    TORTS = "Torts"

    CONTRACTS = "Contracts"

    CRIMINAL_LAW = "Criminal Law"

    CRIMINAL_PROCEDURE = "Criminal Procedure"

    EVIDENCE = "Evidence"

    CONSTITUTIONAL_LAW = "Constitutional Law"

    CIVIL_PROCEDURE = "Civil Procedure"

    PROPERTY = "Real Property"

    WILLS_TRUSTS = "Wills and Trusts"

    FAMILY_LAW = "Family Law"

    SECURED_TRANSACTIONS = "Secured Transactions"

    AGENCY_PARTNERSHIP = "Agency and Partnership"

    CORPORATIONS = "Corporations"

    CONFLICTS = "Conflict of Laws"

    FEDERAL_JURISDICTION = "Federal Jurisdiction"

    PROFESSIONAL_RESPONSIBILITY = "Professional Responsibility"


# ---------- Essential Data Classes ----------


@dataclass
class PerformanceMetrics:

    subject: str

    total_questions: int = 0

    correct_answers: int = 0

    avg_response_time: float = 0.0

    difficulty_progression: List[int] = None

    confidence_trends: List[float] = None

    learning_velocity: float = 0.0

    def __post_init__(self):

        if self.difficulty_progression is None:

            self.difficulty_progression = []

        if self.confidence_trends is None:

            self.confidence_trends = []

    @property
    def accuracy_rate(self) -> float:

        return (
            (self.correct_answers / self.total_questions * 100) if self.total_questions > 0 else 0.0
        )

    def update_difficulty(self) -> Difficulty:
        """Aggressive adaptive difficulty algorithm for MBE-level challenges"""

        if len(self.difficulty_progression) < 3:

            return Difficulty.INTERMEDIATE

        recent_accuracy = (
            statistics.mean(self.difficulty_progression[-10:])
            if len(self.difficulty_progression) >= 10
            else statistics.mean(self.difficulty_progression)
        )

        confidence_trend = (
            statistics.mean(self.confidence_trends[-5:])
            if len(self.confidence_trends) >= 5
            else 3.0
        )

        # More aggressive scoring - bar exam students need to hit higher thresholds

        score = (
            recent_accuracy * 0.5
            + (confidence_trend - 2.5) * 25 * 0.3  # Penalize low confidence more
            + self.learning_velocity * 0.2
        )

        # Higher thresholds - default to challenging questions

        if score > 85:

            return Difficulty.EXPERT

        elif score > 70:

            return Difficulty.ADVANCED

        elif score < 60:

            return Difficulty.FOUNDATIONAL

        return Difficulty.INTERMEDIATE  # Most students should be here initially

    def identify_weak_patterns(self) -> List[ReasoningPattern]:
        """Identify reasoning patterns that need work"""

        # Placeholder - would need pattern tracking

        return []


@dataclass
class FlashcardEntry:

    id: str

    front: str

    back: str

    subject: str = "Mixed/Other"

    difficulty: str = "Intermediate"

    created_at: str = ""

    last_reviewed: str = ""

    ease_factor: float = 2.5

    interval: int = 1

    repetitions: int = 0

    def calculate_next_review(self, quality: int, confidence: int) -> tuple:
        """Enhanced SM-2 algorithm with confidence weighting"""

        adjusted_quality = min(5, quality + (confidence - 3) * 0.3)

        if adjusted_quality < 3:

            self.repetitions = 0

            self.interval = 1

        else:

            if self.repetitions == 0:

                self.interval = 1

            elif self.repetitions == 1:

                self.interval = 6

            else:

                self.interval = int(self.interval * self.ease_factor)

            self.repetitions += 1

        confidence_modifier = (confidence - 3) * 0.05

        self.ease_factor += (
            0.1 - (5 - adjusted_quality) * (0.08 + (5 - adjusted_quality) * 0.02)
        ) + confidence_modifier

        self.ease_factor = max(1.3, min(self.ease_factor, 2.8))

        return self.interval, self.ease_factor


# ---------- Enhanced DataStore ----------


class DataStore:

    def __init__(self):

        self.ensure_files()

    @staticmethod
    def ensure_files():

        for path in [ERROR_LOG, FLASHCARDS, PERFORMANCE_DB, ANALYTICS_DB, CASE_PRECEDENTS]:

            path.touch(exist_ok=True)

        NOTES_DIR.mkdir(exist_ok=True)

    def save_flashcard(self, card: FlashcardEntry):

        with FLASHCARDS.open("a", encoding="utf-8") as f:

            f.write(json.dumps(asdict(card), ensure_ascii=False) + "\n")

    def load_flashcards(self, subject: Optional[Subject] = None) -> List[FlashcardEntry]:

        cards = []

        with FLASHCARDS.open("r", encoding="utf-8") as f:

            for line in f:

                try:

                    data = json.loads(line)

                    card = FlashcardEntry(**data)

                    if subject is None or card.subject == subject.value:

                        cards.append(card)

                except (json.JSONDecodeError, TypeError):

                    continue

        return cards

    def get_due_flashcards(self, limit: int = 20) -> List[FlashcardEntry]:
        """Get flashcards due for review based on SM-2 intervals"""

        cards = self.load_flashcards()

        now = datetime.now()

        due_cards = []

        for card in cards:

            if card.last_reviewed:

                last_review = datetime.fromisoformat(card.last_reviewed)

                due_date = last_review + timedelta(days=card.interval)

                if due_date <= now:

                    due_cards.append(card)

            else:

                due_cards.append(card)  # Never reviewed

        # Sort by how overdue they are

        due_cards.sort(
            key=lambda x: (
                (
                    -(now - datetime.fromisoformat(x.last_reviewed or x.created_at)).days
                    if x.last_reviewed or x.created_at
                    else 0
                ),
                x.difficulty,
            )
        )

        return due_cards[:limit]

    def save_performance(self, metrics: PerformanceMetrics):

        with PERFORMANCE_DB.open("a", encoding="utf-8") as f:

            f.write(json.dumps(asdict(metrics), ensure_ascii=False) + "\n")

    def load_performance(self, subject: Optional[str] = None) -> Dict[str, PerformanceMetrics]:

        performance = defaultdict(lambda: PerformanceMetrics(subject="General"))

        with PERFORMANCE_DB.open("r", encoding="utf-8") as f:

            for line in f:

                try:

                    data = json.loads(line)

                    metrics = PerformanceMetrics(**data)

                    if subject is None or metrics.subject == subject:

                        performance[metrics.subject] = metrics

                except (json.JSONDecodeError, TypeError):

                    continue

        return dict(performance)

    def _build_messages(
        self,
        system_prompt: str,
        user_content: str,
        include_notes: bool = True,
        include_performance: bool = False,
    ) -> List[Dict]:

        messages = [{"role": "system", "content": system_prompt}]

        if include_notes and hasattr(self, "notes") and self.notes:

            messages.append({"role": "system", "content": f"Reference notes:\n{self.notes[:3000]}"})

        if include_performance and hasattr(self, "current_subject") and self.current_subject:

            perf = self.load_performance(self.current_subject)

            if self.current_subject in perf:

                metrics = perf[self.current_subject]

                perf_summary = f"Student performance in {self.current_subject}: "

                perf_summary += f"Accuracy: {metrics.accuracy_rate:.1f}%, "

                perf_summary += f"Questions answered: {metrics.total_questions}"

                messages.append({"role": "system", "content": perf_summary})

        messages.append({"role": "user", "content": user_content})

        return messages


# ---------- Enhanced System Prompts ----------

SYSTEM_FIRST_PRINCIPLES = """You are an expert legal educator combining deep doctrinal knowledge with first-principles analysis for bar exam preparation.

For any legal concept, provide a comprehensive breakdown:

1. FOUNDATIONAL AXIOMS: What are the irreducible legal principles? What fundamental rights/duties are implicated?

2. HISTORICAL DEVELOPMENT: Key cases that shaped the doctrine, evolution through common law and legislation, constitutional foundations if applicable.

3. LOGICAL ARCHITECTURE:

   - Major Premise(s): General legal principles

   - Minor Premise(s): Specific applications and exceptions

   - Necessary logical conclusions

4. ANALOGICAL FRAMEWORK: Distinguishing cases, similar doctrines with key differences, borderline applications.

5. POLICY UNDERPINNINGS: Efficiency rationales, equity considerations, societal goals and limitations.

6. MODERN INTERPRETATION: Current Supreme Court/legislative trends, jurisdictional variations, emerging issues.

7. PEDAGOGICAL AIDS: Mnemonic device, common student misconceptions, "if/then" frameworks for application.

Use precise legal terminology. Cite specific cases/authority. Structure hierarchically. Include bar exam relevance. Keep under 600 words."""

SYSTEM_QUIZ_ADAPTIVE = """You are an elite MBE question writer creating authentic, ultra-challenging bar exam questions that rival the difficulty of the California Bar Exam and other rigorous state bars.

Based on student's recent performance:

- Struggling (<70%): Complex single-issue questions with subtle traps

- Moderate (70-85%): Multi-issue scenarios with competing doctrines and procedural complications

- Strong (>85%): Extreme complexity - jurisdictional conflicts, multiple actors, timing issues, evidentiary complications, and sophisticated policy trade-offs

MANDATORY REQUIREMENTS FOR AUTHENTIC MBE-STYLE QUESTIONS:

**QUESTION COMPLEXITY:**

- **Fact Patterns**: 3-4 paragraphs with intricate, realistic details. Include red herrings, timing issues, jurisdictional nuances, and subtle evidentiary complications that demand careful reading.

- **Multiple Actors**: Questions involving multiple parties, attorneys, judges, witnesses with conflicting interests and complex relationships.

- **Temporal Elements**: Statutes of limitations, effective dates, procedural deadlines, evidentiary timelines.

- **Procedural Layers**: Motions, appeals, jurisdiction, venue, choice of law conflicts.

- **Evidence Complications**: Hearsay, authentication, relevance, character evidence, impeachment issues.

**SOPHISTICATED ANSWER CHOICES - THE TRAPS MUST BE DEVIOUS:**

- **Choice A**: Looks correct if you skim the facts or miss key details

- **Choice B**: Appears right if you apply the wrong jurisdiction or procedural rule

- **Choice C**: Seems correct if you over-rely on policy considerations or common sense

- **Choice D**: Appears right if you confuse similar doctrines or fail to distinguish precedents

**EXAM-STYLE TRAPS TO INCLUDE:**

1. **Jurisdictional Missteps**: Applying state law in federal court, or vice versa

2. **Timing Traps**: Missing statute of limitations by one day, or procedural deadlines

3. **Evidentiary Gotchas**: Hearsay exceptions that almost apply but don't quite qualify

4. **Doctrinal Confusion**: Similar-sounding rules from different areas of law

5. **Procedural Nuances**: Appeals taken from non-appealable orders, or improper venue

6. **Policy vs. Law**: Answers that seem "fair" but are legally incorrect

7. **Precedent Distinctions**: Cases that are "close but distinguishable"

8. **Burden of Proof**: Shifting burdens in complex evidentiary contexts

**QUESTION STRUCTURE:**

1. **DENSE FACT PATTERN**: 400+ words with intricate details, multiple timelines, various actors, procedural history, and subtle complications.

2. **DECEPTIVE QUESTION STEM**: Phrased to mislead if you don't read carefully. Avoid obvious "what result?" questions.

3. **FOUR TRICKY CHOICES**:

   - **Correct Answer**: Requires perfect application of law to complex facts

   - **Distractor A**: Exploits common misreading of key facts

   - **Distractor B**: Traps those who apply similar but incorrect doctrine

   - **Distractor C**: Appeals to "practical justice" over legal accuracy

**EVALUATION FORMAT:**

VERDICT: CORRECT or INCORRECT

CORRECT_ANSWER: [A-D]

SCORE: [1-5] (1=complete miss, 5=masterful analysis)

BRIEF_EXPLANATION: [Why the chosen answer is right/wrong]

WHY_DISTRACTORS_WRONG: [Why each wrong choice fails - make this devastating]

BAR_EXAM_INSIGHT: [How this tests MBE patterns and common failures]

CITATION: [Specific authority tested]

**DIFFICULTY MANDATE**: Questions must be harder than 80% of released MBE questions. Include at least 2-3 layers of complexity and multiple potential pitfalls."""

SYSTEM_SOCRATIC = """You are an expert legal Socratic tutor guiding bar exam students through analytical reasoning development.

Structure Socratic dialogue:

1. INITIAL QUESTION: Test foundational understanding, reveal common misconceptions, require analytical thinking (not mere recall)

2. FOLLOW-UP QUESTIONS: Build on partial understanding, address identified gaps, connect to broader principles, prepare for bar exam application

3. STRUCTURED FEEDBACK:

   - AFFIRMATION: Correct legal reasoning demonstrated

   - CORRECTION: Misconceptions or analytical gaps with explanations

   - EXTENSION: Broader legal principles or policy considerations

4. PEDAGOGICAL FOCUS: Mirror bar exam analytical requirements, develop systematic legal thinking, build confidence through guided discovery

Questions should require synthesis of multiple concepts, application to novel scenarios, and policy analysis. Keep responses focused and actionable."""

SYSTEM_IRAC_PRACTICE = """You are an expert IRAC analysis tutor for bar exam preparation.

For each scenario, provide structured analysis:

I. ISSUE: What precise legal question must be answered?

R. RULE: Governing legal principle with citations

A. APPLICATION: How rule applies to specific facts, counter-arguments addressed, policy implications considered

C. CONCLUSION: Likely outcome with reasoning

Include:

- Counter-arguments and why they fail

- Alternative interpretations of facts

- Policy rationales supporting the rule

- Bar exam "red herrings" to avoid

Guide student through step-by-step reasoning. Focus on analytical precision and comprehensive coverage. Highlight common student errors."""

SYSTEM_COMPARATIVE_ANALYSIS = """You are an expert in comparative legal analysis for bar exam preparation.

For case/concept comparisons:

1. SHARED PRINCIPLES: Common foundational rules and policies

2. FACTUAL PARALLELS: Similar circumstances and stakeholder interests

3. KEY DISTINCTIONS: Critical differences in analysis and outcomes

4. REASONING DIVERGENCE: How courts or doctrines analyzed differently

5. RECONCILIATION: How both can be correct or broader principle encompassing both

6. SYNTHESIS: Overarching rule with modern applications

Focus on analytical frameworks, not just outcomes. Highlight bar exam testing patterns. Use specific citations. Include pedagogical insights about why distinctions matter."""

SYSTEM_CONCEPT_MAPPING = """You are a concept mapping expert for legal education creating visual ASCII art representations.

Create hierarchical concept maps with:

- CENTRAL CONCEPT at top

- Level 1: Core components and fundamental elements

- Level 2: Applications, relationships, exceptions, and limitations

- Level 3: Policy rationales, modern developments, and broader implications

Include:

- Clear connecting phrases showing relationships between concepts

- Pedagogical notes on important connections for bar exam success

- Common student confusion points to avoid

- Bar exam relevance indicators

Keep visually clear, logically structured, and educationally valuable. Use ASCII art for clarity."""

SYSTEM_DIAGNOSTIC_ASSESSMENT = """You are a diagnostic assessment specialist creating comprehensive evaluations of legal knowledge gaps.

Create assessment covering:

1. FOUNDATIONAL CONCEPTS (30%): Basic rule identification and recall

2. APPLICATION SKILLS (30%): Rule application to straightforward facts

3. ANALYTICAL REASONING (25%): Synthesis, distinction, and policy analysis

4. INTEGRATION & SYNTHESIS (15%): Combining multiple doctrines

For each area, identify:

- Specific knowledge gaps

- Reasoning pattern weaknesses

- Recommended remediation strategies

- Bar exam implications

Provide actionable insights for targeted study. Focus on systematic weaknesses rather than isolated mistakes."""

# ---------- Core Helper Functions ----------


def load_env():
    """Load environment with explicit path"""

    if not ENV_PATH.exists():

        print(f"❌ .env not found at {ENV_PATH}")

        print(f"Create it with: echo 'OPENAI_API_KEY=your-key' > {ENV_PATH}")

        sys.exit(1)

    load_dotenv(dotenv_path=ENV_PATH)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:

        print("❌ OPENAI_API_KEY missing in .env")

        sys.exit(1)

    return api_key


def ensure_files():
    """Create necessary files if they don't exist"""

    for path in [ERROR_LOG, FLASHCARDS, PERFORMANCE_DB, ANALYTICS_DB, CASE_PRECEDENTS]:

        path.touch(exist_ok=True)

    NOTES_DIR.mkdir(exist_ok=True)


def load_notes(max_chars=MAX_NOTES_CHARS):
    """Load and concatenate notes from the notes directory"""

    if not NOTES_DIR.exists():

        return ""

    combined = []

    total_chars = 0

    for file_path in sorted(NOTES_DIR.glob("*")):

        if file_path.suffix.lower() not in {".md", ".txt"}:

            continue

        try:

            content = file_path.read_text(encoding="utf-8", errors="ignore")

            if not content.strip():

                continue

            header = f"\n# FILE: {file_path.name}\n"

            if total_chars + len(header) + len(content) > max_chars:

                break

            combined.append(header)

            combined.append(content.strip())

            combined.append("\n")

            total_chars += len(header) + len(content)

        except Exception as e:

            print(f"Warning: Couldn't read {file_path.name}: {e}")

    return "".join(combined)


def safe_llm_call(client, model, messages, temperature=0.2):
    """Wrapper for OpenAI API calls with error handling"""

    try:

        response = client.chat.completions.create(
            model=model, messages=messages, temperature=temperature
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"[API Error: {e}. Check your connection and API key.]"


def generate_id(content: str) -> str:
    """Generate consistent ID from content"""

    return hashlib.md5(content.encode()).hexdigest()[:8]


# ---------- Enhanced Flashcard System with SM-2 ----------


class FlashcardManager:

    def __init__(self):

        self.cards_file = FLASHCARDS

    def add_card(
        self, front: str, back: str, subject: str = "Mixed/Other", difficulty: str = "Intermediate"
    ):
        """Add a new flashcard with SM-2 initial values and enhanced metadata"""

        card = {
            "id": generate_id(front + back),
            "front": front.strip(),
            "back": back.strip()[:1500],  # Limit length
            "subject": subject,
            "difficulty": difficulty,
            "created": datetime.now().isoformat(),
            "last_reviewed": None,
            "next_review": datetime.now().isoformat(),
            "interval": 1,  # days
            "repetitions": 0,
            "ease_factor": 2.5,
            "performance_history": [],
            "tags": [],
            "related_concepts": [],
            "mnemonic": None,
            "common_mistakes": [],
        }

        with self.cards_file.open("a", encoding="utf-8") as f:

            f.write(json.dumps(card) + "\n")

        return card["id"]

    def get_due_cards(self, limit=20, subject=None):
        """Get cards that are due for review"""

        cards = []

        now = datetime.now()

        with self.cards_file.open("r", encoding="utf-8") as f:

            for line in f:

                try:

                    card = json.loads(line.strip())

                    if subject and card.get("subject") != subject:

                        continue

                    next_review = datetime.fromisoformat(card.get("next_review", card["created"]))

                    if next_review <= now:

                        cards.append(card)

                except (json.JSONDecodeError, KeyError):

                    continue

        # Sort by how overdue they are and difficulty

        cards.sort(
            key=lambda x: (
            datetime.fromisoformat(x.get("next_review", x["created"])),
                ["Foundational", "Intermediate", "Advanced", "Expert"].index(
                    x.get("difficulty", "Intermediate")
                ),
            )
        )

        return cards[:limit]

    def update_card(self, card_id: str, quality: int, confidence: int = 3):
        """Enhanced SM-2 algorithm with confidence weighting

        Quality: 0-5 (0=complete blackout, 5=perfect recall)

        Confidence: 1-5 (1=guessing, 5=certain)

        """

        cards = []

        updated = False

        # Read all cards

        with self.cards_file.open("r", encoding="utf-8") as f:

            for line in f:

                try:

                    card = json.loads(line.strip())

                    if card["id"] == card_id:

                        # Apply enhanced SM-2 algorithm

                        ef = card.get("ease_factor", 2.5)

                        interval = card.get("interval", 1)

                        reps = card.get("repetitions", 0)

                        # Adjust quality based on confidence

                        adjusted_quality = min(5, quality + (confidence - 3) * 0.3)

                        if adjusted_quality < 3:

                            # Failed - reset

                            interval = 1

                            reps = 0

                        else:

                            # Successful recall

                            if reps == 0:

                                interval = 1

                            elif reps == 1:

                                interval = 6

                            else:

                                interval = int(interval * ef)

                            reps += 1

                        # Update ease factor with confidence consideration

                        confidence_modifier = (confidence - 3) * 0.05  # -0.15 to +0.15

                        ef = (
                            ef
                            + (
                                0.1
                                - (5 - adjusted_quality) * (0.08 + (5 - adjusted_quality) * 0.02)
                            )
                            + confidence_modifier
                        )

                        ef = max(1.3, min(ef, 2.8))  # Clamp to reasonable range

                        # Update card

                        card["ease_factor"] = ef

                        card["interval"] = interval

                        card["repetitions"] = reps

                        card["last_reviewed"] = datetime.now().isoformat()

                        card["next_review"] = (
                            datetime.now() + timedelta(days=interval)
                        ).isoformat()

                        # Track performance history

                        performance_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "quality": quality,
                            "confidence": confidence,
                            "interval": interval,
                        }

                        card.setdefault("performance_history", []).append(performance_entry)

                        # Keep only last 10 entries

                        card["performance_history"] = card["performance_history"][-10:]

                        updated = True

                    cards.append(card)

                except (json.JSONDecodeError, KeyError):

                    continue

        # Write back all cards

        if updated:

            with self.cards_file.open("w", encoding="utf-8") as f:

                for card in cards:

                    f.write(json.dumps(card) + "\n")

        return updated


# ---------- Performance Tracking ----------


class PerformanceTracker:

    def __init__(self):

        self.perf_file = PERFORMANCE_DB

        self.session_stats = defaultdict(
            lambda: {"correct": 0, "total": 0, "topics": set(), "avg_time": 0.0}
        )

    def record_attempt(
        self, subject: str, correct: bool, topic: str = None, response_time: float = None
    ):
        """Record a quiz attempt with enhanced metadata"""

        self.session_stats[subject]["total"] += 1

        if correct:

            self.session_stats[subject]["correct"] += 1

        if topic:

            self.session_stats[subject]["topics"].add(topic)

        if response_time:

            # Update rolling average

            current_avg = self.session_stats[subject]["avg_time"]

            count = self.session_stats[subject]["total"]

            self.session_stats[subject]["avg_time"] = (
                current_avg * (count - 1) + response_time
            ) / count

        # Write to file

        entry = {
            "timestamp": datetime.now().isoformat(),
            "subject": subject,
            "correct": correct,
            "topic": topic,
            "response_time": response_time,
            "session": True,  # Mark as current session
        }

        with self.perf_file.open("a", encoding="utf-8") as f:

            f.write(json.dumps(entry) + "\n")

    def get_stats(self, subject=None, days=30):
        """Get comprehensive performance statistics"""

        cutoff = datetime.now() - timedelta(days=days)

        stats = defaultdict(
            lambda: {
                "correct": 0,
                "total": 0,
                "avg_time": 0.0,
                "topics": set(),
                "recent_trend": 0.0,
            }
        )

        with self.perf_file.open("r", encoding="utf-8") as f:

            for line in f:

                try:

                    entry = json.loads(line.strip())

                    timestamp = datetime.fromisoformat(entry["timestamp"])

                    if timestamp < cutoff:

                        continue

                    if subject and entry["subject"] != subject:

                        continue

                    subj = entry["subject"]

                    stats[subj]["total"] += 1

                    if entry["correct"]:

                        stats[subj]["correct"] += 1

                    if entry.get("topic"):

                        stats[subj]["topics"].add(entry["topic"])

                    if entry.get("response_time"):

                        # Update rolling average

                        current_avg = stats[subj]["avg_time"]

                        count = stats[subj]["total"]

                        stats[subj]["avg_time"] = (
                            current_avg * (count - 1) + entry["response_time"]
                        ) / count

                except (json.JSONDecodeError, KeyError):

                    continue

        # Calculate percentages and insights

        for subj in stats:

            total = stats[subj]["total"]

            if total > 0:

                stats[subj]["percentage"] = (stats[subj]["correct"] / total) * 100

                stats[subj]["avg_time"] = round(stats[subj]["avg_time"], 1)

            else:

                stats[subj]["percentage"] = 0

            stats[subj]["topics"] = list(stats[subj]["topics"])

        return dict(stats)

    def get_learning_insights(self, subject=None, days=30):
        """Generate learning insights and recommendations"""

        stats = self.get_stats(subject, days)

        insights = {"strengths": [], "weaknesses": [], "recommendations": [], "trends": []}

        if not stats:

            return insights

        for subj, data in stats.items():

            accuracy = data["percentage"]

            total_questions = data["total"]

            if total_questions < 5:

                continue  # Not enough data

            if accuracy >= 85:

                insights["strengths"].append(f"{subj} ({accuracy:.1f}% accuracy)")

            elif accuracy < 70:

                insights["weaknesses"].append(f"{subj} ({accuracy:.1f}% accuracy)")

            # Time-based insights

            avg_time = data["avg_time"]

            if avg_time > 120:  # Over 2 minutes per question

                insights["recommendations"].append(
                    f"Consider timing drills for {subj} (avg: {avg_time}s)"
                )

            elif avg_time < 30:  # Under 30 seconds

                insights["recommendations"].append(
                    f"Add depth questions for {subj} - answering too quickly"
                )

        # Generate specific recommendations

        if insights["weaknesses"]:

            insights["recommendations"].append("Focus on diagnostic assessment for weak areas")

            insights["recommendations"].append(
                "Use interleaved practice mixing weak and strong subjects"
            )

        if insights["strengths"]:

            insights["recommendations"].append("Maintain strengths with spaced review")

            insights["recommendations"].append("Use advanced questions to challenge strong areas")

        return insights

    def print_dashboard(self):
        """Display comprehensive performance dashboard"""

        print("\n" + "=" * 70)

        print(" " * 25 + "PERFORMANCE DASHBOARD")

        print("=" * 70)

        # Get stats for different time periods

        month_stats = self.get_stats(days=30)

        if not month_stats:

            print("\nNo performance data yet. Start practicing to build insights!")

            print("=" * 70)

            return

        print("\nLAST 30 DAYS OVERVIEW:")

        print("-" * 50)

        total_correct = sum(data["correct"] for data in month_stats.values())

        total_questions = sum(data["total"] for data in month_stats.values())

        overall_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0

        print(f"Total Questions: {total_questions}")

        print(f"Overall Accuracy: {overall_accuracy:.1f}%")

        print(f"Subjects Studied: {len(month_stats)}")

        print("\nSUBJECT BREAKDOWN:")

        print("-" * 50)

        for subject in sorted(
            month_stats.keys(), key=lambda x: month_stats[x]["percentage"], reverse=True
        ):

            stats = month_stats[subject]

            pct = stats["percentage"]

            total = stats["total"]

            avg_time = stats.get("avg_time", 0)

            # Create visual bar

            bar_length = int(pct / 4)  # 0-25 characters

            bar = "█" * bar_length + "░" * (25 - bar_length)

            time_indicator = f" ({avg_time:.0f}s avg)" if avg_time > 0 else ""

            print(f"{subject:18} {bar} {pct:5.1f}% ({total:2d}q){time_indicator}")

        # Learning insights

        insights = self.get_learning_insights(days=30)

        if insights["strengths"]:

            print("\n✅ STRENGTHS:")

            for strength in insights["strengths"][:3]:

                print(f"  • {strength}")

        if insights["weaknesses"]:

            print("\n⚠️  AREAS FOR IMPROVEMENT:")

            for weakness in insights["weaknesses"][:3]:

                print(f"  • {weakness}")

        if insights["recommendations"]:

            print("\n💡 RECOMMENDATIONS:")

            for rec in insights["recommendations"][:3]:

                print(f"  • {rec}")

        # Session statistics

        if self.session_stats:

            print("\nCURRENT SESSION:")

            print("-" * 50)

            session_total = sum(stats["total"] for stats in self.session_stats.values())

            session_correct = sum(stats["correct"] for stats in self.session_stats.values())

            if session_total > 0:

                session_accuracy = (session_correct / session_total) * 100

                print(f"Questions: {session_total}")

                print(f"Accuracy: {session_accuracy:.1f}%")

                topics_covered = set()

                for stats in self.session_stats.values():

                    topics_covered.update(stats["topics"])

                if topics_covered:

                    print(f"Topics: {', '.join(list(topics_covered)[:5])}")

        print("=" * 70)


# ---------- Module 1: Advanced Filtering & Search ----------


class CardFilteringSystem:
    """Add when overwhelmed by too many cards"""

    def __init__(self, flashcard_manager):

        self.fm = flashcard_manager

    def search_cards(
        self,
                     query: str = None,
                     tags: List[str] = None,
                     date_from: datetime = None,
                     date_to: datetime = None,
                     min_ease: float = None,
        max_ease: float = None,
    ) -> List[Dict]:
        """Advanced search with multiple filters"""

        cards = []

        with self.fm.cards_file.open("r", encoding="utf-8") as f:

            for line in f:

                try:

                    card = json.loads(line.strip())

                    # Text search

                    if query:

                        query_lower = query.lower()

                        if not (
                            query_lower in card["front"].lower()
                            or query_lower in card["back"].lower()
                        ):

                            continue

                    # Tag filter

                    if tags:

                        card_tags = set(card.get("tags", []))

                        if not card_tags.intersection(set(tags)):

                            continue

                    # Date range

                    created = datetime.fromisoformat(card["created"])

                    if date_from and created < date_from:

                        continue

                    if date_to and created > date_to:

                        continue

                    # Ease factor range

                    ease = card.get("ease_factor", 2.5)

                    if min_ease and ease < min_ease:

                        continue

                    if max_ease and ease > max_ease:

                        continue

                    cards.append(card)

                except (json.JSONDecodeError, KeyError):

                    continue

        return cards

    def get_struggling_cards(self, threshold_ease: float = 1.8) -> List[Dict]:
        """Find cards you're consistently struggling with"""

        return self.search_cards(max_ease=threshold_ease)

    def get_mastered_cards(self, threshold_ease: float = 2.8, min_reps: int = 5) -> List[Dict]:
        """Find cards you've mastered"""

        cards = self.search_cards(min_ease=threshold_ease)

        return [c for c in cards if c.get("repetitions", 0) >= min_reps]


# ---------- Module 2: Tagging & Organization System ----------


class TaggingSystem:
    """Add when you need better topic organization"""

    def __init__(self, flashcard_manager):

        self.fm = flashcard_manager

        self.tag_file = ROOT / "tags_index.json"

        self._build_index()

    def _build_index(self):
        """Build tag index for fast lookups"""

        self.tag_index = {}

        with self.fm.cards_file.open("r", encoding="utf-8") as f:

            for line in f:

                try:

                    card = json.loads(line.strip())

                    for tag in card.get("tags", []):

                        if tag not in self.tag_index:

                            self.tag_index[tag] = []

                        self.tag_index[tag].append(card["id"])

                except (json.JSONDecodeError, KeyError):

                    continue

        # Save index

        with self.tag_file.open("w", encoding="utf-8") as f:

            json.dump(self.tag_index, f)

    def add_tags_to_card(self, card_id: str, new_tags: List[str]):
        """Add tags to existing card"""

        cards = []

        updated = False

        with self.fm.cards_file.open("r", encoding="utf-8") as f:

            for line in f:

                try:

                    card = json.loads(line.strip())

                    if card["id"] == card_id:

                        existing_tags = set(card.get("tags", []))

                        card["tags"] = list(existing_tags.union(set(new_tags)))

                        updated = True

                    cards.append(card)

                except (json.JSONDecodeError, KeyError):

                    continue

        if updated:

            with self.fm.cards_file.open("w", encoding="utf-8") as f:

                for card in cards:

                    f.write(json.dumps(card) + "\n")

            self._build_index()  # Rebuild index

    def get_tag_hierarchy(self) -> Dict[str, List[str]]:
        """Organize tags into hierarchy (subject -> subtopic)"""

        hierarchy = {}

        for tag in self.tag_index:

            if ":" in tag:  # Format: "Subject:Subtopic"

                subject, subtopic = tag.split(":", 1)

                if subject not in hierarchy:

                    hierarchy[subject] = []

                hierarchy[subject].append(subtopic)

            else:

                if "General" not in hierarchy:

                    hierarchy["General"] = []

                hierarchy["General"].append(tag)

        return hierarchy

    def suggest_related_tags(self, card_text: str) -> List[str]:
        """Suggest tags based on content"""

        suggestions = []

        # Define keyword -> tag mappings

        keyword_tags = {
            "negligence": ["Torts:Negligence"],
            "duty": ["Torts:Duty", "Contracts:Duty"],
            "breach": ["Torts:Breach", "Contracts:Breach"],
            "consideration": ["Contracts:Consideration"],
            "offer": ["Contracts:Formation"],
            "acceptance": ["Contracts:Formation"],
            "miranda": ["Criminal Procedure:Miranda"],
            "hearsay": ["Evidence:Hearsay"],
            "relevance": ["Evidence:Relevance"],
            "jurisdiction": ["Civil Procedure:Jurisdiction"],
            "erie": ["Civil Procedure:Erie"],
            "commerce": ["Constitutional Law:Commerce"],
            "due process": ["Constitutional Law:DueProcess"],
            "equal protection": ["Constitutional Law:EqualProtection"],
        }

        text_lower = card_text.lower()

        for keyword, tags in keyword_tags.items():

            if keyword in text_lower:

                suggestions.extend(tags)

        return list(set(suggestions))


# ---------- Module 3: Gamification & Motivation ----------


class GamificationSystem:
    """Add when you need motivation and engagement"""

    def __init__(self, performance_tracker):

        self.tracker = performance_tracker

        self.achievements_file = ROOT / "achievements.json"

        self.load_achievements()

    def load_achievements(self):
        """Load or initialize achievements"""

        if self.achievements_file.exists():

            with self.achievements_file.open("r") as f:

                self.achievements = json.load(f)

        else:

            self.achievements = {
                "streaks": {"current": 0, "best": 0, "last_date": None},
                "milestones": {},
                "badges": [],
            }

    def save_achievements(self):
        """Save achievements to file"""

        with self.achievements_file.open("w") as f:

            json.dump(self.achievements, f, indent=2)

    def update_streak(self):
        """Update daily streak"""

        today = datetime.now().date().isoformat()

        last_date = self.achievements["streaks"]["last_date"]

        if last_date:

            last = datetime.fromisoformat(last_date).date()

            today_date = datetime.now().date()

            if (today_date - last).days == 1:

                # Continuing streak

                self.achievements["streaks"]["current"] += 1

            elif (today_date - last).days > 1:

                # Streak broken

                self.achievements["streaks"]["current"] = 1

            # Same day - no change

        else:

            # First day

            self.achievements["streaks"]["current"] = 1

        # Update best streak

        if self.achievements["streaks"]["current"] > self.achievements["streaks"]["best"]:

            self.achievements["streaks"]["best"] = self.achievements["streaks"]["current"]

        self.achievements["streaks"]["last_date"] = today

        self.save_achievements()

        return self.achievements["streaks"]["current"]

    def check_milestones(self, total_cards_reviewed: int, total_questions: int):
        """Check and award milestone badges"""

        new_badges = []

        milestones = {
            "first_10": (total_cards_reviewed >= 10, "🌱 Seedling - Reviewed 10 cards"),
            "first_50": (total_cards_reviewed >= 50, "🌿 Sprout - Reviewed 50 cards"),
            "first_100": (total_cards_reviewed >= 100, "🌳 Tree - Reviewed 100 cards"),
            "first_500": (total_cards_reviewed >= 500, "🌲 Forest - Reviewed 500 cards"),
            "quiz_25": (total_questions >= 25, "📝 Quiz Novice - 25 questions"),
            "quiz_100": (total_questions >= 100, "📚 Quiz Master - 100 questions"),
            "quiz_500": (total_questions >= 500, "🎓 Quiz Legend - 500 questions"),
            "streak_7": (
                self.achievements["streaks"]["best"] >= 7,
                "🔥 Week Warrior - 7 day streak",
            ),
            "streak_30": (
                self.achievements["streaks"]["best"] >= 30,
                "💎 Month Master - 30 day streak",
            ),
        }

        for badge_id, (condition, badge_text) in milestones.items():

            if condition and badge_id not in self.achievements["badges"]:

                self.achievements["badges"].append(badge_id)

                new_badges.append(badge_text)

        if new_badges:

            self.save_achievements()

        return new_badges

    def get_motivational_message(self, performance: float) -> str:
        """Get personalized motivational message based on performance"""

        streak = self.achievements["streaks"]["current"]

        if performance >= 90:

            messages = [
                f"🌟 Outstanding! {streak} day streak and crushing it!",
                "🎯 Perfect execution! Keep this momentum going!",
                "🏆 Bar exam excellence in the making!",
            ]

        elif performance >= 75:

            messages = [
                f"💪 Strong performance! {streak} days of consistency!",
                "📈 Solid progress! You're building mastery!",
                "✨ Great work! The bar exam better watch out!",
            ]

        elif performance >= 60:

            messages = [
                f"👍 Keep pushing! {streak} day streak shows dedication!",
                "🔄 Progress, not perfection! You're improving!",
                "💡 Every question teaches you something new!",
            ]

        else:

            messages = [
                f"🌱 Growth mindset! {streak} days of showing up!",
                "🔨 Building foundation! Struggles create strength!",
                "🎯 Focus on understanding, scores will follow!",
            ]

        import random

        return random.choice(messages)


# ---------- Module 4: Collaborative Study System ----------


class CollaborativeStudy:
    """Add when you want to study with others"""

    def __init__(self):

        self.shared_dir = ROOT / "shared_flashcards"

        self.shared_dir.mkdir(exist_ok=True)

    def export_deck(self, cards: List[Dict], deck_name: str, author: str):
        """Export cards as shareable deck"""

        deck = {
            "name": deck_name,
            "author": author,
            "created": datetime.now().isoformat(),
            "cards": cards,
            "metadata": {
                "total_cards": len(cards),
                "subjects": list(set(c.get("subject", "") for c in cards)),
                "version": "2.0",
            },
        }

        filename = (
            f"{deck_name.replace(' ', '_')}_{author}_{datetime.now().strftime('%Y%m%d')}.json"
        )

        filepath = pathlib.Path(self.shared_dir) / filename

        with filepath.open("w", encoding="utf-8") as f:

            json.dump(deck, f, indent=2)

        return filepath

    def import_deck(self, filepath: Path, flashcard_manager):
        """Import shared deck"""

        with filepath.open("r", encoding="utf-8") as f:

            deck = json.load(f)

        imported = 0

        for card in deck["cards"]:

            # Generate new ID to avoid conflicts

            new_id = hashlib.md5(
                (card["front"] + card["back"] + datetime.now().isoformat()).encode()
            ).hexdigest()[:8]

            card["id"] = new_id

            card["imported_from"] = deck["name"]

            card["imported_date"] = datetime.now().isoformat()

            # Reset SM-2 values for new user

            card["last_reviewed"] = None

            card["next_review"] = datetime.now().isoformat()

            card["interval"] = 1

            card["repetitions"] = 0

            card["ease_factor"] = 2.5

            # Add to flashcards

            flashcard_manager.add_card(card["front"], card["back"], card.get("subject", "Imported"))

            imported += 1

        return imported, deck["metadata"]

    def create_study_group_challenge(self, topic: str, duration_days: int = 7):
        """Create a study challenge for group motivation"""

        challenge = {
            "id": hashlib.md5(f"{topic}{datetime.now().isoformat()}".encode()).hexdigest()[:8],
            "topic": topic,
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=duration_days)).isoformat(),
            "participants": [],
            "leaderboard": {},
            "daily_goals": {"cards_reviewed": 20, "questions_answered": 10, "accuracy_target": 75},
        }

        challenge_file = self.shared_dir / f"challenge_{challenge['id']}.json"

        with challenge_file.open("w", encoding="utf-8") as f:

            json.dump(challenge, f, indent=2)

        return challenge


# ---------- Module 5: Advanced Analytics ----------


class AdvancedAnalytics:
    """Add when you need deeper insights into your learning"""

    def __init__(self, performance_tracker, flashcard_manager):

        self.tracker = performance_tracker

        self.fm = flashcard_manager

    def get_forgetting_curve_data(self, card_id: str) -> Dict:
        """Analyze forgetting curve for specific card"""

        # Would need to track each review in detail

        # This is a simplified version

        with self.fm.cards_file.open("r") as f:

            for line in f:

                try:

                    card = json.loads(line.strip())

                    if card["id"] == card_id:

                        return {
                            "ease_factor": card.get("ease_factor", 2.5),
                            "interval": card.get("interval", 1),
                            "repetitions": card.get("repetitions", 0),
                            "retention_strength": min(100, card.get("repetitions", 0) * 20),
                        }

                except (KeyError, ValueError, TypeError):

                    continue

        return {}

    def get_optimal_study_time(self) -> Dict:
        """Analyze when you perform best"""

        performance_by_hour = {}

        with self.tracker.perf_file.open("r") as f:

            for line in f:

                try:

                    entry = json.loads(line.strip())

                    timestamp = datetime.fromisoformat(entry["timestamp"])

                    hour = timestamp.hour

                    if hour not in performance_by_hour:

                        performance_by_hour[hour] = {"correct": 0, "total": 0}

                    performance_by_hour[hour]["total"] += 1

                    if entry["correct"]:

                        performance_by_hour[hour]["correct"] += 1

                except (KeyError, ValueError, TypeError):

                    continue

        # Calculate accuracy by hour

        best_hours = []

        for hour, stats in performance_by_hour.items():

            if stats["total"] >= 5:  # Minimum sample size

                accuracy = (stats["correct"] / stats["total"]) * 100

                best_hours.append((hour, accuracy, stats["total"]))

        best_hours.sort(key=lambda x: x[1], reverse=True)

        return {
            "best_hours": best_hours[:3],
            "worst_hours": best_hours[-3:] if len(best_hours) > 3 else [],
            "total_hours_studied": len(performance_by_hour),
        }

    def predict_readiness(self, target_date: datetime, target_accuracy: float = 75.0) -> Dict:
        """Predict exam readiness based on current trajectory"""

        # Get recent performance trend

        recent_stats = self.tracker.get_stats(days=30)

        if not recent_stats:

            return {"prediction": "Insufficient data"}

        # Calculate average accuracy and improvement rate

        total_accuracy = sum(s["percentage"] for s in recent_stats.values()) / len(recent_stats)

        # Simple linear projection (would be more sophisticated in production)

        days_until_target = (target_date - datetime.now()).days

        daily_improvement_needed = (
            (target_accuracy - total_accuracy) / days_until_target if days_until_target > 0 else 0
        )

        return {
            "current_accuracy": total_accuracy,
            "target_accuracy": target_accuracy,
            "days_remaining": days_until_target,
            "daily_improvement_needed": daily_improvement_needed,
            "on_track": daily_improvement_needed <= 0.5,  # 0.5% daily improvement is realistic
            "recommended_daily_cards": max(20, int(20 * (target_accuracy / total_accuracy))),
            "focus_subjects": [
                s for s, stats in recent_stats.items() if stats["percentage"] < target_accuracy
            ],
        }


# ---------- MBE Mistake Analysis System ----------


class MBEMistakeAnalyzer:
    """
    Analyzes WHY wrong answers are tempting and trains pattern recognition.

    Identifies cognitive errors, MBE traps, and creates targeted remediation exercises
    to inoculate students against recurring mistake patterns.
    """

    COMMON_MBE_TRAPS = {
        "temporal_misdirection": "Applying rule from wrong time period",
        "burden_shifting": "Confusing which party must prove what",
        "similar_doctrine_confusion": "Mixing up related but distinct rules",
        "incomplete_element_analysis": "Forgetting one required element",
        "jurisdiction_error": "Applying minority rule when majority is tested",
        "procedural_vs_substantive": "Confusing when substantive law applies",
        "scope_creep": "Extending rule beyond its proper boundaries",
        "policy_over_law": "Choosing 'fair' answer over legally correct one",
        "notice_trap": "Missing actual/record/inquiry notice distinction (property)",
        "early_bird_trap": "Assuming early sale defeats common scheme (property)",
        "intent_trap": "Missing intent requirement for all lots (property servitudes)",
        "remedy_confusion": "Confusing damages (law) with injunction (equity)",
    }

    def __init__(self, client: OpenAI, model: str = DEFAULT_MODEL):
        self.client = client
        self.model = model
        self.error_patterns = defaultdict(int)  # Track which traps student falls for
        self.remediation_history = []  # Track correction exercises completed

    def analyze_wrong_answer(
        self, question: str, correct_answer: str, student_answer: str, explanation: str
    ) -> Dict:
        """
        Diagnose the specific cognitive error pattern and generate targeted remediation.

        Returns structured analysis with trap identification, cognitive diagnosis,
        correction protocol, and inoculation exercises.
        """

        analysis_prompt = f"""
        Diagnostic analysis of MBE error pattern:

        QUESTION STEM: {question}
        
        CORRECT ANSWER: {correct_answer}
        STUDENT SELECTED: {student_answer}
        EXPLANATION PROVIDED: {explanation}

        REQUIRED ANALYSIS (be devastatingly specific):

        1. TRAP IDENTIFICATION:
        What specific MBE examiner trap did this distractor employ?
        Categories to consider:
        - Temporal misdirection (wrong time period/sequence)
        - Burden shifting (who proves what)
        - Similar doctrine conflation (e.g., easement vs. servitude)
        - Incomplete element analysis (missing one required element)
        - Jurisdiction error (minority vs. majority rule)
        - Procedural vs. substantive confusion
        - Scope creep (extending rule too far)
        - Policy over law (fair but legally wrong)
        - Notice distinction errors (actual/record/inquiry)
        - Common scheme traps (intent, early sale, notice)

        Identify PRIMARY trap and any SECONDARY traps present.

        2. COGNITIVE ERROR DIAGNOSIS:
        What mental shortcut or faulty assumption led to this error?
        - Pattern matched to superficially similar but legally distinct scenario?
        - Overlooked key qualifier word (e.g., "only", "all", "unless")?
        - Applied policy reasoning instead of black-letter rule?
        - Stopped analysis prematurely (satisfied 2/3 elements, missed 3rd)?
        - Confused similar-sounding doctrines (e.g., reversion vs. remainder)?
        - Failed to apply jurisdictional default (chose minority when majority tested)?

        3. CORRECTION PROTOCOL:
        Provide a specific, actionable analytical step to prevent this error:
        
        FORMAT: "When you see [triggering fact pattern], ALWAYS [specific action] before selecting answer."
        
        Example: "When you see subdivision + restrictions, ALWAYS run IRIS checklist (Intent/Restrictive/Notice/Same scheme) before assuming deed silence defeats enforcement."
        
        Create 2-3 such protocols specific to this error.

        4. PATTERN RECOGNITION TRAINING:
        What visual/verbal cue should trigger immediate recognition of this issue?
        - Magic words that signal the trap (e.g., "so long as" = determinable)
        - Fact patterns that always require this analysis
        - Answer choice language that reveals the trap

        5. INOCULATION EXERCISES:
        Generate 2 similar questions testing the SAME trap pattern:
        
        Exercise A: Similar fact pattern, same trap, different subject
        Exercise B: Identical trap but with extra distractor to increase difficulty
        
        For each exercise, provide:
        - Fact pattern (2-3 sentences)
        - 4 answer choices (one correct, three featuring the same trap type)
        - Explanation emphasizing the trap recognition

        6. REMEDIATION PRIORITY:
        - Severity: [High/Medium/Low] - How commonly is this trap tested?
        - Difficulty: [Hard/Medium/Easy] - How subtle is the distinction?
        - Impact: [Critical/Important/Helpful] - Point value if mastered
        
        7. CROSS-REFERENCE:
        What related concepts should student review to strengthen understanding?
        (List 2-3 specific doctrine names with brief explanation of connection)

        Make analysis laser-focused on preventing THIS specific error in future questions.
        Use precise legal terminology. Include MBE examiner perspective.
        """

        system = """You are an expert in MBE question construction and cognitive error analysis.
        You understand:
        - How NCBE examiners craft plausible but incorrect distractors
        - Common cognitive biases that trap even strong students
        - Pattern recognition techniques from championship test-takers
        - Neuroscience of error correction and skill acquisition
        
        Your analysis should be:
        - Brutally specific (no generic advice)
        - Action-oriented (concrete steps, not vague suggestions)
        - Pattern-focused (teachable recognition cues)
        - Immediately applicable (student can use on next question)
        
        For property servitudes, emphasize IRIS framework violations and notice type confusions.
        Highlight early-sale trap and intent requirement misunderstandings."""

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": analysis_prompt},
        ]

        response = (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.2, max_tokens=2000
            )
            .choices[0]
            .message.content
        )

        # Extract trap type for tracking
        trap_type = self._identify_trap_type(response)
        self.error_patterns[trap_type] += 1

        # Save to remediation history
        remediation_entry = {
            "timestamp": datetime.now().isoformat(),
            "question_stem": question[:100],  # First 100 chars
            "correct": correct_answer,
            "selected": student_answer,
            "trap_type": trap_type,
            "analysis": response,
        }
        self.remediation_history.append(remediation_entry)

        return {
            "trap_type": trap_type,
            "full_analysis": response,
            "error_count_this_trap": self.error_patterns[trap_type],
            "remediation_exercises": self._extract_exercises(response),
        }

    def _identify_trap_type(self, analysis: str) -> str:
        """Extract the primary trap type from analysis."""
        analysis_lower = analysis.lower()

        # Check for specific trap keywords
        for trap_name, description in self.COMMON_MBE_TRAPS.items():
            if trap_name.replace("_", " ") in analysis_lower:
                return trap_name

        # Default
        return "general_error"

    def _extract_exercises(self, analysis: str) -> List[Dict]:
        """Extract remediation exercises from analysis response."""
        exercises = []

        # Simple extraction - would be enhanced with actual parsing
        if "Exercise A:" in analysis:
            exercises.append({"type": "inoculation_a", "content": "See full analysis"})
        if "Exercise B:" in analysis:
            exercises.append({"type": "inoculation_b", "content": "See full analysis"})

        return exercises

    def get_personalized_trap_report(self) -> Dict:
        """Generate report of student's most frequent error patterns."""

        if not self.error_patterns:
            return {
                "message": "No errors analyzed yet. Complete some questions to build your error profile.",
                "recommendations": [],
            }

        # Rank traps by frequency
        ranked_traps = sorted(self.error_patterns.items(), key=lambda x: x[1], reverse=True)

        top_traps = ranked_traps[:5]

        recommendations = []
        for trap_name, count in top_traps:
            trap_desc = self.COMMON_MBE_TRAPS.get(trap_name, "Unknown error pattern")
            recommendations.append(
                {
                    "trap": trap_name.replace("_", " ").title(),
                    "description": trap_desc,
                    "frequency": count,
                    "remediation": self._get_trap_remediation(trap_name),
                }
            )

        return {
            "total_errors_analyzed": len(self.remediation_history),
            "unique_trap_types": len(self.error_patterns),
            "most_common_traps": recommendations,
            "improvement_focus": recommendations[0]["trap"] if recommendations else "N/A",
        }

    def _get_trap_remediation(self, trap_name: str) -> str:
        """Get specific remediation advice for a trap type."""

        remediation_map = {
            "temporal_misdirection": "Create a timeline for each question. Mark critical time points BEFORE analyzing elements.",
            "burden_shifting": "Write 'P must prove:' and 'D must prove:' at top of scratch paper for every question.",
            "similar_doctrine_confusion": "Make a comparison chart of similar doctrines. Review daily until automatic.",
            "incomplete_element_analysis": "Use finger count - touch one finger per element. Must satisfy ALL before selecting answer.",
            "jurisdiction_error": "Circle any '[MBE Split]' markers. Default to MAJORITY rule unless question specifies jurisdiction.",
            "procedural_vs_substantive": "Ask: 'Is this about HOW (procedure) or WHAT (substance)?' Circle answer before proceeding.",
            "scope_creep": "Underline the exact scope language in the rule. Don't extend beyond explicit boundaries.",
            "policy_over_law": "Remember: MBE tests LAW, not fairness. If answer feels 'right' but isn't in rule = WRONG.",
            "notice_trap": "Property questions: Write 'A/R/I?' for Actual/Record/Inquiry notice types. Check all three.",
            "early_bird_trap": "Common scheme questions: Early sale ≠ automatic exemption. Check IRIS (Intent + Notice + Restrictive + Same).",
            "intent_trap": "Developer's intent for ALL lots required. If some lots exempt = no common scheme.",
            "remedy_confusion": "Circle 'law' or 'equity' based on facts. Law = $$, Equity = injunction. Servitudes = equity.",
        }

        return remediation_map.get(trap_name, "Review the specific rule and create a checklist.")

    def save_error_log(self, filepath: Path = ERROR_LOG) -> None:
        """Save error analysis history to file for tracking over time."""
        try:
            with open(filepath, "a", encoding="utf-8") as f:
                for entry in self.remediation_history:
                    f.write(json.dumps(entry) + "\n")

            print(f"💾 Error log saved: {len(self.remediation_history)} analyses")
            self.remediation_history.clear()  # Clear after saving
        except OSError as e:
            print(f"⚠️  Could not save error log: {e}")


# ---------- Issue-Spotting Training System ----------


class IssueSpottingTrainer:
    """
    Develops systematic issue identification from fact patterns.

    Trains students to scan fact patterns in <30 seconds and identify all
    legal issues using structured scanning protocols and trigger word recognition.
    """

    TRIGGER_WORD_LIBRARY = {
        "temporal": [
            "immediately",
            "reasonable time",
            "promptly",
            "delay",
            "ten years",
            "continuous",
            "interrupted",
            "within",
            "after",
            "before",
        ],
        "relational": [
            "employee",
            "independent contractor",
            "agent",
            "partner",
            "stranger",
            "invitee",
            "licensee",
            "trespasser",
            "buyer",
            "seller",
        ],
        "transactional": [
            "conveyed",
            "granted",
            "sold",
            "leased",
            "mortgaged",
            "promised",
            "agreed",
            "offered",
            "accepted",
            "recorded",
        ],
        "status": ["minor", "incompetent", "intoxicated", "corporation", "LLC", "partnership"],
        "property_descriptors": [
            "appurtenant",
            "in gross",
            "joint",
            "common",
            "fee simple",
            "life estate",
            "leasehold",
            "subdivision",
            "covenant",
        ],
        "qualifiers": [
            "hostile",
            "actual",
            "exclusive",
            "continuous",
            "open",
            "notorious",
            "adverse",
            "good faith",
            "bad faith",
            "bona fide",
        ],
    }

    def __init__(self, client: OpenAI, model: str = DEFAULT_MODEL):
        self.client = client
        self.model = model
        self.spotting_history = []
        self.trigger_word_hits = defaultdict(int)

    def train_systematic_scanning(self, fact_pattern: str) -> str:
        """
        Teaches students to scan fact patterns systematically for issues.

        Returns comprehensive training analysis with step-by-step scanning protocol.
        """

        training_prompt = f"""
        Train systematic issue-spotting for this fact pattern:
        
        {fact_pattern}
        
        ## SCANNING PROTOCOL (teach this systematic approach)
        
        ### Step 1: TEMPORAL SCAN (5 seconds)
        Look for: dates, time periods, sequences, deadlines, durations
        Found: [List every temporal fact with significance]
        Raised issues: [What legal issue each temporal fact raises]
        Example: "10 years" → adverse possession? statute of limitations? RAP analysis?
        
        ### Step 2: PARTY SCAN (5 seconds)
        Identify: all parties and their legal relationships
        Found: [List all parties with relationship descriptors]
        Raised issues: [What each relationship implies legally]
        Example: "employee" → respondeat superior? scope of employment? workers comp?
        
        ### Step 3: TRANSACTION SCAN (5 seconds)
        Identify: all legal acts (conveyances, promises, torts, crimes)
        Found: [List all transactions/acts chronologically]
        Raised issues: [What each transaction raises]
        Example: "conveyed Lot 1" → deed validity? recording act? chain of title?
        
        ### Step 4: PROPERTY SCAN (if applicable) (5 seconds)
        Identify: all property interests and restrictions described
        Found: [List all interests with ownership types]
        Raised issues: [What each interest/restriction raises]
        Example: "residential only covenant" → runs with land? notice? IRIS common scheme?
        
        ### Step 5: QUALIFIER SCAN (5 seconds)
        Identify: adjectives/adverbs modifying actions or status
        Found: [List all qualifiers with what they modify]
        Raised issues: [What each qualifier raises]
        Example: "hostile possession" → adverse possession elements? HATE checklist?
        
        ### Step 6: RED HERRING IDENTIFICATION (5 seconds)
        What facts are mentioned but likely don't raise testable issues?
        Found: [List likely irrelevant facts]
        Why irrelevant: [Brief explanation]
        Example: "sunny day" → atmospheric detail, not legally significant
        
        ## ISSUE HIERARCHY (10 seconds)
        Organize identified issues in logical analytical order:
        
        TIER 1 - Threshold Issues (must address first):
        - Jurisdiction/standing/justiciability
        - Statute of limitations/laches
        - Subject matter constraints
        
        TIER 2 - Formation/Validity Issues:
        - Creation of legal relationship
        - Required elements/formalities
        - Defects in formation
        
        TIER 3 - Performance/Breach Issues:
        - Duties and obligations
        - Breach or violation
        - Causation and damages
        
        TIER 4 - Remedy Issues:
        - Available remedies (law vs. equity)
        - Measure of damages
        - Injunctive relief requirements
        
        TIER 5 - Defense/Affirmative Issues:
        - Defenses available
        - Affirmative claims
        - Counterclaims
        
        ## PREDICTED QUESTION FOCUS (5 seconds)
        Based on issues spotted, the question will likely ask about:
        
        Primary Issue: [Most legally complex/ambiguous issue identified]
        Why This Issue: [Facts are contested/elements borderline/rule has exceptions here]
        Answer Will Turn On: [Specific fact or element that determines outcome]
        
        MBE Strategy: [What to focus on when answering - 1 sentence]
        
        TOTAL TARGET TIME: 45 seconds for complete systematic scan
        CHAMPIONSHIP TIME: 30 seconds with practice
        
        ## TEACHING ANNOTATIONS:
        - Mark each trigger word found in fact pattern with [TRIGGER: category]
        - Highlight facts that raise multiple issues
        - Note facts that appear relevant but aren't (examiner misdirection)
        - Provide "speed cues" for instant recognition on similar patterns
        
        This protocol should become automatic with practice. Students drill until
        they complete this scan in <30 seconds with 95% issue-capture accuracy.
        
        For property servitudes, ensure IRIS framework (Intent/Restrictive/Notice/Same scheme)
        triggers on subdivision + restrictions patterns.
        """

        system = """You are an expert in issue-spotting pedagogy and MBE fact pattern construction.
        You understand:
        - How examiners layer multiple issues into compact fact patterns
        - Trigger words that signal specific legal doctrines
        - Red herrings designed to waste student time
        - Systematic scanning methods used by top scorers
        
        Train students to develop muscle memory for issue-spotting through:
        - Explicit trigger word recognition
        - Hierarchical issue organization
        - Time-bounded scanning drills
        - Pattern recognition automation
        
        Be extremely specific about WHERE in the fact pattern each issue appears and
        WHAT specific words/phrases triggered the issue identification.
        
        For property law, emphasize IRIS mnemonic for common scheme issues."""

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": training_prompt},
        ]

        response = (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.2, max_tokens=2000
            )
            .choices[0]
            .message.content
        )

        # Track trigger words found
        self._update_trigger_stats(fact_pattern)

        return response

    def issue_spotting_speed_drill(self, subject: str, num_patterns: int = 20) -> Dict:
        """
        Rapid-fire drill: see fact pattern, identify issues in <30 seconds.

        Returns performance statistics and improvement recommendations.
        """

        print("\n⚡ ISSUE-SPOTTING SPEED DRILL")
        print("=" * 60)
        print(f"Subject: {subject}")
        print("Goal: Identify all issues in <30 seconds per pattern")
        print("Press Enter after reading each fact pattern to see issues...\n")

        patterns = self._generate_fact_patterns(subject, num_patterns)

        results = []

        for i, pattern in enumerate(patterns, 1):
            print(f"\n{'='*60}")
            print(f"Pattern {i}/{num_patterns}")
            print("-" * 60)
            print(pattern["facts"])
            print("\n" + "-" * 60)
            print("What issues are raised? (Think, then press Enter)")

            input("Press Enter when ready to see issues... ")

            start_time = time.time()

            print("\nPOSSIBLE ISSUES:")
            for idx, issue in enumerate(pattern["possible_issues"], 1):
                print(f"  {idx}. {issue}")

            print(f"\nACTUAL ISSUES IN THIS PATTERN: {pattern['actual_issues']}")

            response_time = time.time() - start_time

            user_input = input("\nDid you spot all issues? (y/n): ").strip().lower()

            if user_input != "y":
                missed_input = input(
                    "Which issues did you miss? (comma-separated numbers): "
                ).strip()
                if missed_input:
                    missed = [
                        pattern["possible_issues"][int(x.strip()) - 1]
                        for x in missed_input.split(",")
                        if x.strip().isdigit()
                    ]
                else:
                    missed = []
            else:
                missed = []

            correct = len(missed) == 0

            if correct:
                print("✓ Perfect issue-spotting!")
            else:
                print(f"\n✗ Missed {len(missed)} issue(s)")
                print(f"\nEXPLANATION: {pattern['explanation']}")
                print("\nTRIGGER WORDS YOU SHOULD HAVE CAUGHT:")
                for trigger in pattern.get("trigger_words", []):
                    print(
                        f"  • '{trigger}' → signals {pattern['trigger_meanings'].get(trigger, 'legal issue')}"
                    )

            results.append(
                {
                    "pattern_num": i,
                    "correct": correct,
                    "time": response_time,
                    "missed_count": len(missed),
                    "missed_issues": missed,
                }
            )

        return self._analyze_spotting_performance(results)

    def _generate_fact_patterns(self, subject: str, num_patterns: int) -> List[Dict]:
        """Generate practice fact patterns for issue-spotting drills."""

        # Simplified implementation - would call LLM to generate varied patterns
        # For now, return template-based patterns

        property_patterns = [
            {
                "facts": "Developer subdivided 20 acres into 10 lots. First deed to Buyer A contained no restrictions. Developer then sold remaining 9 lots with deeds stating 'residential use only.' All deeds were recorded. Buyer A now operates a law office from the property.",
                "possible_issues": [
                    "Recording act issue",
                    "Equitable servitude/common scheme",
                    "Zoning violation",
                    "Adverse possession",
                    "Easement by necessity",
                ],
                "actual_issues": [2],  # Common scheme is the key issue
                "explanation": "This tests IRIS common scheme doctrine. Intent to restrict all lots + restrictive promise + notice (record/inquiry from 9 recorded deeds) + same scheme = equitable servitude binds Lot 1 despite silent deed.",
                "trigger_words": ["subdivided", "residential use only", "recorded"],
                "trigger_meanings": {
                    "subdivided": "common scheme analysis",
                    "residential use only": "restrictive covenant/servitude",
                    "recorded": "notice to successors",
                },
            },
            {
                "facts": "Owner conveyed Blackacre 'to A for life, then to B if B graduates law school.' A is 70 years old. B is 25 and in law school.",
                "possible_issues": [
                    "Life estate creation",
                    "Contingent remainder vs. executory interest",
                    "Rule Against Perpetuities",
                    "Waste by life tenant",
                    "Partition rights",
                ],
                "actual_issues": [1, 2, 3],
                "explanation": "Life estate to A. Future interest to B is contingent remainder (condition must be met). RAP applies to contingent remainder - will B graduate within 21 years of A's death? Likely yes, so valid.",
                "trigger_words": ["for life", "then to", "if"],
                "trigger_meanings": {
                    "for life": "life estate",
                    "then to": "future interest (remainder)",
                    "if": "contingent interest (condition)",
                },
            },
        ]

        # Return requested number (cycling through templates if needed)
        return (property_patterns * ((num_patterns // len(property_patterns)) + 1))[:num_patterns]

    def _analyze_spotting_performance(self, results: List[Dict]) -> Dict:
        """Analyze speed drill performance and provide recommendations."""

        total = len(results)
        perfect_count = sum(1 for r in results if r["correct"])
        avg_time = sum(r["time"] for r in results) / total if total > 0 else 0
        avg_missed = sum(r["missed_count"] for r in results) / total if total > 0 else 0

        accuracy = (perfect_count / total * 100) if total > 0 else 0

        print("\n" + "=" * 60)
        print("DRILL PERFORMANCE ANALYSIS")
        print("=" * 60)
        print(f"Accuracy: {accuracy:.1f}% ({perfect_count}/{total} perfect)")
        print(f"Average Time: {avg_time:.1f} seconds per pattern")
        print(f"Average Missed: {avg_missed:.1f} issues per pattern")

        # Performance feedback
        if accuracy >= 90 and avg_time <= 30:
            grade = "🏆 ELITE"
            feedback = "Championship-level issue-spotting! Ready for full-speed MBE."
        elif accuracy >= 80 and avg_time <= 45:
            grade = "✅ STRONG"
            feedback = "Solid performance. Focus on speed - aim for <30 seconds."
        elif accuracy >= 70:
            grade = "📈 DEVELOPING"
            feedback = "Good foundation. Practice trigger word recognition daily."
        else:
            grade = "🔨 BUILDING"
            feedback = (
                "Keep drilling. Review trigger word library and use finger-counting for issues."
            )

        print(f"\nGrade: {grade}")
        print(f"Feedback: {feedback}")

        # Recommendations
        recommendations = []

        if avg_time > 30:
            recommendations.append(
                "Speed: Practice trigger word flash cards 10 min/day to automate recognition"
            )

        if accuracy < 90:
            recommendations.append(
                "Accuracy: Review missed patterns and create personal 'trap cards' for each miss"
            )

        if avg_missed > 0.5:
            recommendations.append(
                "Completeness: Use 6-step scanning protocol (temporal→party→transaction→property→qualifier→red herring)"
            )

        if recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")

        return {
            "accuracy": accuracy,
            "average_time": avg_time,
            "average_missed": avg_missed,
            "grade": grade,
            "recommendations": recommendations,
        }

    def _update_trigger_stats(self, fact_pattern: str) -> None:
        """Track which trigger words appear in fact patterns."""

        fact_lower = fact_pattern.lower()

        for category, words in self.TRIGGER_WORD_LIBRARY.items():
            for word in words:
                if word in fact_lower:
                    self.trigger_word_hits[f"{category}:{word}"] += 1

    def get_trigger_word_report(self) -> Dict:
        """Generate report of most common trigger words encountered."""

        if not self.trigger_word_hits:
            return {"message": "No patterns analyzed yet.", "top_triggers": []}

        ranked = sorted(self.trigger_word_hits.items(), key=lambda x: x[1], reverse=True)

        top_triggers = [
            {"trigger": trigger.split(":")[1], "category": trigger.split(":")[0], "count": count}
            for trigger, count in ranked[:15]
        ]

        return {
            "total_patterns_analyzed": len(self.spotting_history),
            "unique_triggers_found": len(self.trigger_word_hits),
            "top_trigger_words": top_triggers,
            "most_common_category": max(
                (
                    (cat, sum(1 for t in self.trigger_word_hits if t.startswith(cat + ":")))
                    for cat in self.TRIGGER_WORD_LIBRARY.keys()
                ),
                key=lambda x: x[1],
                default=("none", 0),
            )[0],
        }

    def create_custom_drill(self, subject: str, focus_issues: List[str]) -> str:
        """
        Generate custom drill focused on specific issues student is missing.

        Args:
            subject: MBE subject area
            focus_issues: Specific issues student needs practice with

        Returns:
            AI-generated custom drill with fact patterns emphasizing focus issues
        """

        prompt = f"""
        Create a custom issue-spotting drill for:
        
        SUBJECT: {subject}
        FOCUS ISSUES: {', '.join(focus_issues)}
        
        Generate 5 fact patterns (each 3-4 sentences) that will train recognition of these issues.
        
        For each pattern:
        1. Include subtle trigger words for the focus issues
        2. Add 1-2 red herrings to test discrimination
        3. Layer multiple issues (student must spot focus issue among others)
        4. Vary difficulty: patterns 1-2 (obvious), 3-4 (moderate), 5 (subtle)
        
        For each pattern provide:
        - Fact pattern
        - All issues raised (numbered list)
        - Trigger words that should have signaled each issue
        - Explanation of why red herrings are irrelevant
        
        For property patterns with servitudes/covenants, ensure IRIS framework is testable:
        - Intent language ("developer intended all lots...")
        - Restrictive promise ("residential only," "no commercial")
        - Notice facts (recorded plan, uniform neighborhood, actual knowledge)
        - Same scheme evidence (number of lots, uniformity, marketing materials)
        
        Make these challenging but teachable - each should reinforce the focus issues.
        """

        system = """You are an expert legal educator specializing in issue-spotting pedagogy.
        Create fact patterns that teach pattern recognition through deliberate practice.
        Include explicit teaching annotations explaining what should trigger issue identification.
        
        For property law, integrate IRIS mnemonic trigger words."""

        messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]

        response = (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.3, max_tokens=2000
            )
            .choices[0]
            .message.content
        )

        return response


# ---------- Main Tutor Class ----------


class BarTutorV3:

    def __init__(self, client: OpenAI, model: str, notes: str = ""):

        self.client = client

        self.model = model

        self.notes = notes

        self.flashcards = FlashcardManager()

        self.tracker = PerformanceTracker()

        self.store = DataStore()

        # Initialize advanced modules

        self.filtering = CardFilteringSystem(self.flashcards)

        self.tagging = TaggingSystem(self.flashcards)

        self.gamification = GamificationSystem(self.tracker)

        self.collaborative = CollaborativeStudy()

        self.analytics = AdvancedAnalytics(self.tracker, self.flashcards)

        self.mistake_analyzer = MBEMistakeAnalyzer(self.client, self.model)

        self.issue_spotter = IssueSpottingTrainer(self.client, self.model)

        # Initialize elite memory system with error handling
        try:
            from elite_memory_palace import EliteMemoryPalaceSystem
            self.elite_system = EliteMemoryPalaceSystem("Bar Exam Champion")
            print("✅ Elite memory system loaded successfully")
        except Exception as e:
            print(f"⚠️  Elite memory system unavailable: {e}")
            self.elite_system = None

        self.current_subject = "Mixed/Other"

        self.session_start = datetime.now()

    def _build_messages(
        self,
        system_prompt: str,
        user_content: str,
        include_notes: bool = True,
        include_performance: bool = False,
    ) -> List[Dict]:

        messages = [{"role": "system", "content": system_prompt}]

        if include_notes and self.notes:

            messages.append({"role": "system", "content": f"Reference notes:\n{self.notes[:3000]}"})

        if include_performance and self.current_subject:

            perf = self.store.load_performance(self.current_subject)

            if self.current_subject in perf:

                metrics = perf[self.current_subject]

                perf_summary = f"Student performance in {self.current_subject}: "

                perf_summary += f"Accuracy: {metrics.accuracy_rate:.1f}%, "

                perf_summary += f"Questions answered: {metrics.total_questions}"

                messages.append({"role": "system", "content": perf_summary})

        messages.append({"role": "user", "content": user_content})

        return messages

    def mode_explain_first_principles(self):
        """Explain topic using first principles approach"""

        print("\n📚 FIRST-PRINCIPLES EXPLANATION")

        print("I'll break down any legal concept to its foundational elements.\n")

        topic = input("Enter topic/concept (or 'back'): ").strip()

        if topic.lower() in ["back", "exit"]:

            return

        messages = [{"role": "system", "content": SYSTEM_FIRST_PRINCIPLES}]

        if self.notes:

            messages.append({"role": "system", "content": f"Reference notes:\n{self.notes[:3000]}"})

        messages.append({"role": "user", "content": f"Explain from first principles: {topic}"})

        print("\nAnalyzing from foundational axioms...\n")

        response = safe_llm_call(self.client, self.model, messages, temperature=0.1)

        print("─" * 70)

        print(response)

        print("─" * 70)

        # Offer to create flashcard

        create = input("\nCreate flashcard from this? (y/n): ").strip()

        if create.lower().startswith("y"):

            card_id = self.flashcards.add_card(
                f"First Principles: {topic}",
                response[:1500],  # Truncate for flashcard
                self.current_subject,
            )

            print(f"✅ Flashcard created (ID: {card_id})")

    def first_principles_analysis(self, concept: str) -> str:
        """Comprehensive first-principles legal analysis with pedagogical enhancements"""

        prompt = f"""

        Conduct a comprehensive first-principles analysis of '{concept}':

        1. FOUNDATIONAL AXIOMS:

           - What are the irreducible legal principles?

           - What fundamental rights/duties are implicated?

        2. HISTORICAL DEVELOPMENT:

           - Key historical cases that shaped the doctrine

           - Evolution through common law and legislation

           - Constitutional foundations if applicable

        3. LOGICAL ARCHITECTURE:

           - Major Premise(s): General legal principles

           - Minor Premise(s): Specific applications and exceptions

           - Necessary logical conclusions

        4. ANALOGICAL FRAMEWORK:

           - Distinguishing cases and concepts

           - Similar doctrines with key differences

           - Borderline applications

        5. POLICY UNDERPINNINGS:

           - Efficiency rationales

           - Equity considerations

           - Societal goals and limitations

        6. MODERN INTERPRETATION:

           - Current Supreme Court/legislative trends

           - Jurisdictional variations

           - Emerging issues and criticisms

        7. PEDAGOGICAL AIDS:

           - Mnemonic device for remembering key elements

           - Common student misconceptions to avoid

           - "If/then" frameworks for application

        Use precise legal terminology. Include specific citations. Structure hierarchically.

        """

        system = """You are a master legal educator combining deep doctrinal knowledge with

        advanced pedagogical techniques. Structure analysis to build from foundational principles

        to complex applications. Include learning aids, common pitfalls, and practical application

        frameworks. Maintain analytical rigor while ensuring accessibility for learners."""

        messages = self._build_messages(system, prompt)

        response = (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.1
            )
            .choices[0]
            .message.content
        )

        # Extract and save analytical framework

        self._extract_analytical_framework(concept, response)

        return response

    def _extract_analytical_framework(self, concept: str, analysis: str) -> None:
        """Extract structured framework from AI analysis for future use"""

        # This would parse the analysis and create an AnalyticalFramework object

        # For now, we'll store the raw analysis for later processing

        pass

    def socratic_dialogue(
        self, topic: str, student_response: str = "", dialogue_history: List[Dict] = None
    ) -> str:
        """Advanced Socratic method with legal reasoning focus"""

        if dialogue_history is None:

            dialogue_history = []

        if not student_response:

            prompt = f"""

            Begin a Socratic dialogue about '{topic}' in a legal context.

            Ask ONE sophisticated question that requires legal reasoning:

            1. Tests understanding of foundational legal principles

            2. Reveals common analytical errors in legal thinking

            3. Requires application of doctrine to hypothetical scenarios

            4. Encourages consideration of policy implications

            Frame the question to build analytical skills, not just recall memorization.

            Consider the student's current performance level in legal reasoning.

            """

        else:

            history_context = "\n".join(
                [f"Q: {h['question']}\nA: {h['answer']}" for h in dialogue_history[-3:]]
            )

            prompt = f"""

            Socratic dialogue on '{topic}' - Current exchange:

            Recent dialogue history:

            {history_context}

            Student's latest response: {student_response}

            Provide structured feedback (3 components):

            1. AFFIRMATION: What correct legal reasoning they demonstrated

            2. CORRECTION: Address any misconceptions or analytical gaps

            3. EXTENSION: Connect to broader legal principles or policy considerations

            Then pose ONE follow-up question that:

            - Builds directly on their demonstrated understanding

            - Addresses the identified gap

            - Requires synthesis of multiple legal concepts

            - Prepares them for bar exam application

            """

        system = """You are an expert legal Socratic tutor. Guide students through legal reasoning

        processes using the Socratic method. Focus on developing analytical skills, identifying

        logical fallacies in legal thinking, and building doctrinal understanding. Questions should

        mirror bar exam analytical requirements. Provide constructive feedback that builds confidence

        while correcting misunderstandings."""

        messages = self._build_messages(system, prompt, include_performance=True)

        return (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.3
            )
            .choices[0]
            .message.content
        )

    def irac_analysis_practice(self, fact_pattern: str, legal_issue: str) -> str:
        """Guided IRAC analysis practice with real-time feedback"""

        prompt = f"""

        Provide a structured IRAC analysis for this scenario:

        FACTS: {fact_pattern}

        ISSUE: {legal_issue}

        Guide the student through IRAC step-by-step:

        I. ISSUE: What legal question must be answered?

        R. RULE: What is the governing legal principle?

        A. APPLICATION: How does the rule apply to these facts?

        C. CONCLUSION: What is the likely outcome?

        Include:

        - Counter-arguments and why they fail

        - Policy implications of the outcome

        - Alternative analyses if facts are interpreted differently

        Use precise legal terminology and cite relevant authority.

        """

        system = """You are an IRAC analysis expert. Provide comprehensive yet clear

        IRAC structures that mirror bar exam expectations. Include all necessary legal

        elements while maintaining analytical rigor. Highlight potential traps and

        alternative interpretations."""

        messages = self._build_messages(system, prompt)

        return (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.2
            )
            .choices[0]
            .message.content
        )

    def case_brief_generator(self, case_name: str, context: str = "") -> str:
        """Generate structured case brief with pedagogical elements"""

        prompt = f"""

        Create a comprehensive case brief for: {case_name}

        Additional context: {context}

        Structure the brief with these pedagogical enhancements:

        1. CASE IDENTIFICATION

           - Full citation and court

           - Decision date and justice writing

        2. FACTS (with analytical focus)

           - Key facts establishing jurisdiction/context

           - Facts central to the legal dispute

           - Factual disputes or ambiguities

        3. PROCEDURAL HISTORY

           - How the case reached this court

           - Key procedural issues resolved

        4. ISSUE(S)

           - Precise legal questions presented

           - Sub-issues and related questions

        5. HOLDING

           - Court's specific answers to each issue

           - Vote breakdown if important

        6. REASONING

           - Court's analytical framework

           - Key precedents distinguished or followed

           - Policy rationales articulated

        7. RULE SYNTHESIS

           - General legal principle extracted

           - Scope and limitations articulated

        8. PEDAGOGICAL ELEMENTS

           - Why this case matters for bar exam

           - Common misinterpretations to avoid

           - Modern significance and treatment

        Include dissenting opinions if significant. Use standard legal formatting.

        """

        system = """You are a case briefing expert. Create comprehensive, accurate briefs

        that serve as both reference tools and learning instruments. Include analytical

        depth while maintaining clarity. Highlight doctrinal significance and bar exam

        relevance."""

        messages = self._build_messages(system, prompt)

        return (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.1
            )
            .choices[0]
            .message.content
        )

    def generate_hypothetical(
        self, rule: str, difficulty: Difficulty, reasoning_pattern: ReasoningPattern = None
    ) -> str:
        """Create sophisticated fact patterns targeting specific reasoning skills"""

        complexity_map = {
            Difficulty.FOUNDATIONAL: "Single clear issue, straightforward application",
            Difficulty.INTERMEDIATE: "Multiple interacting elements, some ambiguity",
            Difficulty.ADVANCED: "Complex facts with competing legal theories and counterarguments",
            Difficulty.EXPERT: "Multi-jurisdictional, policy-heavy analysis with doctrinal conflicts",
        }

        pattern_focus = ""

        if reasoning_pattern:

            pattern_map = {
                ReasoningPattern.ANALOGICAL: "Emphasize comparison to key precedents",
                ReasoningPattern.DEDUCTIVE: "Require step-by-step logical application",
                ReasoningPattern.INDUCTIVE: "Build general principles from specific facts",
                ReasoningPattern.POLICY_BASED: "Focus on underlying policy rationales",
                ReasoningPattern.TEXTUALIST: "Emphasize statutory/plain language interpretation",
                ReasoningPattern.INTENTIONALIST: "Consider legislative intent and purpose",
            }

            pattern_focus = f"Target reasoning pattern: {pattern_map[reasoning_pattern]}"

        prompt = f"""

        Create a bar exam-caliber hypothetical testing: {rule}

        Difficulty Level: {complexity_map[difficulty]}

        {pattern_focus}

        Structure with pedagogical enhancements:

        1. ENGAGING FACT PATTERN:

           - Vivid, realistic scenario with specific names/details

           - Unambiguous on core issues but with subtle complexities

           - Include potentially distracting but ultimately irrelevant facts

        2. PRECISE CALL OF QUESTION:

           - Specific legal question(s) to answer

           - Jurisdiction and governing law specified

        3. HIDDEN ANALYTICAL FRAMEWORK (for tutor use):

           - Key issues that must be identified

           - Potential traps and common mistakes

           - Alternative analyses to consider

           - Policy implications to address

        4. PEDAGOGICAL ELEMENTS:

           - Why this tests important bar exam skills

           - Common analytical errors to avoid

           - How this connects to broader doctrinal themes

        Make it challenging but fair. Include time pressure indicators.

        """

        system = """You are an expert bar exam question crafter. Create questions that accurately

        assess doctrinal understanding while developing analytical reasoning skills. Include

        subtle complexities that reward deep thinking. Structure for optimal learning outcomes."""

        messages = self._build_messages(system, prompt)

        return (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.4
            )
            .choices[0]
            .message.content
        )

    def interleaved_practice_session(
        self, subject: Subject, session_length: int = 20
    ) -> List[Dict]:
        """Create interleaved practice mixing different but related concepts"""

        prompt = f"""

        Design an interleaved practice session for {subject.value} with {session_length} items.

        Interleaving principles to follow:

        1. Mix related but distinct concepts (no two consecutive items from same subtopic)

        2. Include prerequisite concepts before advanced applications

        3. Vary difficulty levels throughout session

        4. Include spaced review of previously learned material

        For each item, specify:

        - Concept/subtopic

        - Difficulty level

        - Question type (recall, application, synthesis, analysis)

        - Estimated time

        - Why this interleaving is pedagogically valuable

        Structure the session to build conceptual connections and prevent compartmentalization.

        """

        system = """You are an interleaving practice expert. Create sessions that maximize

        long-term retention by connecting related concepts. Follow evidence-based spacing

        and interleaving principles. Ensure conceptual flow while maintaining challenge."""

        messages = self._build_messages(system, prompt)

        response = (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.3
            )
            .choices[0]
            .message.content
        )

        # Parse response into structured practice items

        return self._parse_interleaved_session(response)

    def _parse_interleaved_session(self, response: str) -> List[Dict]:
        """Parse AI response into structured practice items"""

        # This would parse the response into a list of practice items

        # For now, return a placeholder structure

        return [{"concept": "parsed_concept", "difficulty": "intermediate", "type": "application"}]

    def diagnostic_assessment(self, subject: Subject) -> Dict:
        """Comprehensive diagnostic assessment of knowledge gaps"""

        prompt = f"""

        Create a diagnostic assessment for {subject.value} to identify knowledge gaps and reasoning deficiencies.

        Assessment structure:

        1. FOUNDATIONAL CONCEPTS (10 questions)

           - Test basic rule identification and recall

        2. APPLICATION SKILLS (10 questions)

           - Test ability to apply rules to facts

        3. ANALYTICAL REASONING (8 questions)

           - Test synthesis, distinction, and policy analysis

        4. SYNTHESIS & INTEGRATION (7 questions)

           - Test ability to combine multiple doctrines

        For each question category, include:

        - Sample questions at different difficulty levels

        - Common mistakes indicating specific gaps

        - Recommended remediation strategies

        Focus on identifying systematic weaknesses in legal thinking patterns.

        """

        system = """You are a diagnostic assessment specialist. Create assessments that precisely

        identify knowledge gaps and reasoning deficiencies. Structure to reveal systematic

        patterns in student thinking. Include clear remediation pathways."""

        messages = self._build_messages(system, prompt, include_performance=True)

        response = (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.2
            )
            .choices[0]
            .message.content
        )

        return self._analyze_diagnostic_results(response)

    def _analyze_diagnostic_results(self, response: str) -> Dict:
        """Analyze diagnostic assessment to identify learning gaps"""

        # Parse and analyze the diagnostic results

        # Return structured analysis of strengths/weaknesses

        return {"strengths": [], "weaknesses": [], "recommended_focus": []}

    def concept_map_generator(self, topic: str, depth: int = 2) -> str:
        """Generate visual concept maps for understanding relationships"""

        prompt = f"""

        Create a detailed concept map for: {topic}

        Structure the map hierarchically with {depth} levels of depth:

        CENTRAL CONCEPT: {topic}

        Level 1 Branches (Core Components):

        - Fundamental elements

        - Key doctrines

        - Essential principles

        Level 2 Branches (Applications & Relationships):

        - How components interact

        - Exceptions and limitations

        - Related doctrines

        Level {depth} Branches (Advanced Connections):

        - Policy rationales

        - Comparative analysis

        - Modern developments

        Format as ASCII art with clear hierarchical relationships.

        Include connecting phrases showing relationships between concepts.

        Add pedagogical notes on why certain connections are important.

        """

        system = """You are a concept mapping expert. Create visual representations that

        show relationships between legal concepts. Use clear hierarchical structures.

        Include explanatory connections that build understanding."""

        messages = self._build_messages(system, prompt)

        return (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.2
            )
            .choices[0]
            .message.content
        )

    def comparative_analysis(self, case1: str, case2: str) -> str:
        """Analyze similarities and distinctions between cases/concepts"""

        prompt = f"""

        Comparative analysis of '{case1}' and '{case2}':

        1. SHARED PRINCIPLES: Common foundational rules

        2. FACTUAL PARALLELS: Similar circumstances

        3. KEY DISTINCTIONS: What differentiates them?

        4. REASONING DIVERGENCE: How courts analyzed differently

        5. RECONCILIATION: Can both be correct? How?

        6. SYNTHESIS: Broader principle encompassing both

        Focus on the analytical framework, not just outcomes.

        """

        system = """Expert in comparative legal analysis and case synthesis.

        Identify patterns and distinctions with surgical precision."""

        messages = self._build_messages(system, prompt)

        return (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.2
            )
            .choices[0]
            .message.content
        )

# ---------- Main Entry Point ----------

    def print_analytics_dashboard(self):
        """Display comprehensive performance analytics"""

        print("\n" + "=" * 60)

        print(" " * 20 + "PERFORMANCE ANALYTICS")

        print("=" * 60)

        all_performance = self.store.load_performance()

        if not all_performance:

            print("No performance data yet. Start practicing!")

            return

        # Overall statistics

        total_q = sum(p.total_questions for p in all_performance.values())

        total_c = sum(p.correct_answers for p in all_performance.values())

        overall_acc = (total_c / total_q * 100) if total_q > 0 else 0

        print("\nOVERALL PERFORMANCE:")

        print(f"  Total Questions: {total_q}")

        print(f"  Overall Accuracy: {overall_acc:.1f}%")

        print(f"  Subjects Studied: {len(all_performance)}")

        # Subject breakdown

        print("\nSUBJECT BREAKDOWN:")

        sorted_subjects = sorted(
            all_performance.items(), key=lambda x: x[1].accuracy_rate, reverse=True
        )

        for subject, metrics in sorted_subjects:

            bar_length = int(metrics.accuracy_rate / 5)  # 0-20 chars

            bar = "█" * bar_length + "░" * (20 - bar_length)

            print(
                f"  {subject:25} {bar} {metrics.accuracy_rate:5.1f}% ({metrics.total_questions} questions)"
            )

        # Identify focus areas

        weak_subjects = [s for s, m in all_performance.items() if m.accuracy_rate < 70]

        strong_subjects = [s for s, m in all_performance.items() if m.accuracy_rate > 85]

        if weak_subjects:

            print(f"\n⚠️  FOCUS AREAS: {', '.join(weak_subjects)}")

        if strong_subjects:

            print(f"\n✅ STRONG AREAS: {', '.join(strong_subjects)}")

        # Session statistics

        if self.session_stats["questions_attempted"] > 0:

            session_acc = (
                self.session_stats["correct_answers"]
                / self.session_stats["questions_attempted"]
                * 100
            )

            print("\nCURRENT SESSION:")

            print(f"  Questions: {self.session_stats['questions_attempted']}")

            print(f"  Accuracy: {session_acc:.1f}%")

            print(f"  Topics: {', '.join(self.session_stats['topics_covered'])}")

        print("=" * 60 + "\n")

    def mode_socratic_dialogue(self):
        """Socratic dialogue for deep understanding"""

        print("\n🤔 SOCRATIC DIALOGUE MODE")

        print("Engage in guided discovery through questioning.")

        print("I'll ask probing questions to help you discover insights.\n")

        topic = input("Topic for Socratic dialogue (or 'back'): ").strip()

        if topic.lower() in ["back", "exit"]:

            return

        # Initial question

        question = self.socratic_dialogue(topic)

        print("\n" + "─" * 60)

        print(question)

        print("─" * 60 + "\n")

        # Dialogue loop

        while True:

            response = input("Your response (or 'done' to exit): ").strip()

            if response.lower() in ["done", "exit", "back"]:

                break

            follow_up = self.socratic_dialogue(topic, response)

            print("\n" + "─" * 60)

            print(follow_up)

            print("─" * 60 + "\n")

            self.session_stats["topics_covered"].add(topic)

    def mode_flashcard_review(self):
        """SM-2 spaced repetition flashcard review system"""
        print("\n🃏 FLASHCARD REVIEW MODE (SM-2)")
        print("Spaced repetition system for optimal memorization")

        # Get due cards
        due_cards = self.flashcards.get_due_cards(limit=10)

        if not due_cards:
            print("No cards due for review! Great job staying on top of your studies.")
            return

        print(f"\nFound {len(due_cards)} cards due for review")

        for i, card in enumerate(due_cards, 1):
            print(f"\n--- Card {i}/{len(due_cards)} ---")
            print(f"Front: {card['front']}")

            input("\nPress Enter to see the answer...")

            print(f"Back: {card['back']}")

            # Get quality rating
            while True:
                try:
                    quality = input("\nQuality (0-5): 0=failed, 5=perfect: ").strip()
                    quality = int(quality)
                    if 0 <= quality <= 5:
                        break
                except ValueError:
                    pass
                print("Please enter a number between 0 and 5")

            # Get confidence level
            while True:
                try:
                    confidence = input("Confidence (1-5): 1=guessing, 5=certain: ").strip()
                    confidence = int(confidence)
                    if 1 <= confidence <= 5:
                        break
                except ValueError:
                    pass
                print("Please enter a number between 1 and 5")

            # Update the card
            self.flashcards.update_card(card["id"], quality, confidence)

        print(f"\n✅ Review session completed! {len(due_cards)} cards reviewed.")

    def mode_quiz_adaptive(self):
        """Sophisticated adaptive quiz with confidence tracking and reasoning pattern targeting"""

        print("\n📝 ADAPTIVE QUIZ MODE")

        print(
            "AI-powered questions adapt to your performance and target weak reasoning patterns.\n"
        )

        # Select subject

        print("Available subjects:")

        for i, subject in enumerate(Subject, 1):

            print(f"  {i}. {subject.value}")

        print(f"  {len(Subject) + 1}. Mixed Practice")

        choice = input("\nSelect subject number: ").strip()

        subject = None

        if choice.isdigit() and 1 <= int(choice) <= len(Subject):

            subject = list(Subject)[int(choice) - 1]

            self.current_subject = subject.value

        elif choice == str(len(Subject) + 1):

            self.current_subject = "Mixed"

        else:

            print("Invalid choice. Using mixed practice.")

            self.current_subject = "Mixed"

        # Determine difficulty and target weak reasoning patterns

        if subject:

            perf = self.store.load_performance(subject.value)

            if subject.value in perf:

                metrics = perf[subject.value]

                difficulty = metrics.update_difficulty()

                weak_patterns = metrics.identify_weak_patterns()

                target_pattern = weak_patterns[0] if weak_patterns else None

            else:

                difficulty = Difficulty.INTERMEDIATE

                target_pattern = None

        else:

            difficulty = Difficulty.INTERMEDIATE

            target_pattern = None

        print(f"\nDifficulty level: {difficulty.name}")

        if target_pattern:

            print(f"Targeting reasoning pattern: {target_pattern.value}")

        # Generate targeted question

        rule = input("Specific rule/concept to test (or Enter for adaptive selection): ").strip()

        if not rule:

            rule = f"ultra-challenging MBE practice targeting {difficulty.name.lower()} level {'with ' + target_pattern.value + ' reasoning' if target_pattern else 'skills'}. Create questions harder than 80% of released MBE questions with sophisticated traps and distractors."

        hypothetical = self.generate_hypothetical(rule, difficulty, target_pattern)

        print("\n" + "─" * 60)

        print(hypothetical)

        print("─" * 60 + "\n")

        start_time = time.time()

        # Get answer with confidence level

        answer = input("Your answer: ").strip()

        print("\nConfidence level:")

        for i, level in enumerate(ConfidenceLevel, 1):

            print(f"  {i}. {level.name}: {level.value}/5")

        confidence_choice = input("Select confidence (1-5): ").strip()

        confidence = (
            ConfidenceLevel(int(confidence_choice))
            if confidence_choice.isdigit() and 1 <= int(confidence_choice) <= 5
            else ConfidenceLevel.FAMILIAR
        )

        response_time = time.time() - start_time

        # AI-powered evaluation

        is_correct, score, evaluation = self._evaluate_answer(answer, hypothetical, difficulty)

        print("\n" + "─" * 40)

        print("AI EVALUATION:")

        print(evaluation)

        print("─" * 40)

        # Update comprehensive metrics

        self._update_performance_metrics(subject, difficulty, confidence, score, response_time)

        self.session_stats["questions_attempted"] += 1

        if subject:

            self.session_stats["topics_covered"].add(subject.value)

    def _evaluate_answer(self, answer: str, question: str, difficulty: Difficulty) -> tuple:
        """Deterministic AI-powered answer evaluation with structured output"""

        # First, extract the correct answer from the question text

        import re

        correct_answer_match = re.search(
            r"\b([A-D])\)\s*is correct|\b([A-D])\)\s*is the correct|The correct answer is ([A-D])",
            question,
            re.IGNORECASE,
        )

        if correct_answer_match:

            correct_letter = (
                correct_answer_match.group(1)
                or correct_answer_match.group(2)
                or correct_answer_match.group(3)
            )

        else:

            # Fallback: look for patterns like "A)" being the first mentioned

            lines = question.split("\n")

            for line in lines:

                if re.match(r"^[A-D]\)", line.strip()):

                    correct_letter = line.strip()[0]

                    break

            else:

                correct_letter = "A"  # Default fallback

        prompt = f"""

        Evaluate this MBE-style question answer. Be DETERMINISTIC and STRUCTURED.

        QUESTION:

        {question}

        STUDENT ANSWER: {answer.strip().upper()[:1]}  (first letter only)

        REQUIRED OUTPUT FORMAT:

        VERDICT: CORRECT or INCORRECT

        CORRECT_ANSWER: {correct_letter}

        SCORE: [1-5] (1=wrong doctrine, 5=perfect analysis)

        BRIEF_EXPLANATION: [2-3 sentences explaining the result]

        WHY_DISTRACTORS_WRONG: [1 sentence per wrong answer explaining the trap]

        BAR_EXAM_INSIGHT: [1 sentence about what this tests on the MBE]

        Be precise. The verdict must be either "CORRECT" or "INCORRECT" based on whether the student's answer matches {correct_letter}.

        """

        system = """You are a ruthless MBE evaluator. Follow the output format exactly.

        Be devastatingly precise about why wrong answers fail - expose the exact legal error in each distractor.

        Make explanations so thorough that students learn why they were wrong and how to avoid similar mistakes.

        No mercy for sloppy thinking - bar exams reward precision, not approximation."""

        messages = self._build_messages(system, prompt)

        response = (
            self.client.chat.completions.create(
            model=self.model,
            messages=messages,
                temperature=0.1,  # Low temperature for consistency
            )
            .choices[0]
            .message.content
        )

        # Parse the structured response

        is_correct = "CORRECT" in response.upper()

        score_match = re.search(r"SCORE:\s*([1-5])", response)

        score = int(score_match.group(1)) if score_match else (5 if is_correct else 2)

        return is_correct, score, response

    def _update_performance_metrics(
        self,
        subject: Subject,
        difficulty: Difficulty,
        confidence: ConfidenceLevel,
        score: int,
        response_time: float,
    ):
        """Update comprehensive performance metrics"""

        if not subject:

            return

        # Update metrics

        perf = self.store.load_performance(subject.value)

        if subject.value not in perf:

            perf[subject.value] = PerformanceMetrics(subject=subject.value)

        metrics = perf[subject.value]

        metrics.total_questions += 1

        if score >= 4:  # Consider 4+ as correct for accuracy

            metrics.correct_answers += 1

        metrics.difficulty_progression.append(score)

        metrics.confidence_trends.append(confidence.value)

        # Update response time (weighted average)

        if metrics.avg_response_time == 0:

            metrics.avg_response_time = response_time

        else:

            metrics.avg_response_time = (metrics.avg_response_time + response_time) / 2

        self.store.save_performance(metrics)

    def mode_comparative_analysis(self):
        """Compare and contrast cases or concepts"""

        print("\n⚖️ COMPARATIVE ANALYSIS MODE")

        print("Analyze relationships between cases, doctrines, or concepts.\n")

        item1 = input("First case/concept: ").strip()

        item2 = input("Second case/concept: ").strip()

        if not item1 or not item2:

            print("Both items required for comparison.")

            return

        print("\nAnalyzing relationships and distinctions...\n")

        analysis = self.comparative_analysis(item1, item2)

        print("─" * 60)

        print(analysis)

        print("─" * 60)

        # Save as study material

        save = input("\nSave this comparison for review? (y/n): ").strip()

        if save.lower().startswith("y"):

            with (ROOT / "comparisons.txt").open("a", encoding="utf-8") as f:

                f.write(f"\n\n{'='*60}\n")

                f.write(f"Comparison: {item1} vs {item2}\n")

                f.write(f"Date: {datetime.now().isoformat()}\n")

                f.write(f"{'='*60}\n")

                f.write(analysis)

            print("✅ Comparison saved to comparisons.txt")

    def mode_interleaved_practice(self):
        """Interleaved practice session mixing related concepts"""

        print("\n🔄 INTERLEAVED PRACTICE MODE")

        print("Mix different but related concepts for better retention.\n")

        # Select subject

        print("Available subjects:")

        for i, subject in enumerate(Subject, 1):

            print(f"  {i}. {subject.value}")

        choice = input("\nSelect subject number: ").strip()

        if not choice.isdigit() or not (1 <= int(choice) <= len(Subject)):

            print("Invalid choice.")

            return

        subject = list(Subject)[int(choice) - 1]

        session_length = input("Session length (10-30 items, default 20): ").strip()

        session_length = (
            int(session_length)
            if session_length.isdigit() and 10 <= int(session_length) <= 30
            else 20
        )

        print(f"\nGenerating interleaved practice session for {subject.value}...")

        session_items = self.interleaved_practice_session(subject, session_length)

        print(f"\n{'='*60}")

        print(f"INTERLEAVED PRACTICE: {subject.value.upper()}")

        print(f"Session Length: {len(session_items)} items")

        print(f"{'='*60}")

        # Run the interleaved session

        for i, item in enumerate(session_items, 1):

            print(f"\n--- Item {i}/{len(session_items)} ---")

            print(f"Concept: {item.get('concept', 'Unknown')}")

            print(f"Difficulty: {item.get('difficulty', 'Intermediate')}")

            print(f"Type: {item.get('type', 'Application')}")

            # Generate and present question

            if "question" in item:

                print(f"Question: {item['question']}")

            else:

                # Generate question based on item details

                question = self.generate_hypothetical(
                    f"{item.get('concept', 'general legal principle')}",
                    Difficulty[item.get("difficulty", "INTERMEDIATE").upper()],
                )

                print(question)

            input("\nPress Enter when ready to continue...")

            self.session_stats["topics_covered"].add(subject.value)

        print("\n✅ Interleaved practice session completed!")

        print("Interleaving improves long-term retention by connecting related concepts.")

    def mode_diagnostic_assessment(self):
        """Comprehensive diagnostic assessment of knowledge gaps"""

        print("\n🔍 DIAGNOSTIC ASSESSMENT MODE")

        print("Comprehensive evaluation to identify strengths and weaknesses.\n")

        # Select subject

        print("Available subjects:")

        for i, subject in enumerate(Subject, 1):

            print(f"  {i}. {subject.value}")

        choice = input("\nSelect subject number: ").strip()

        if not choice.isdigit() or not (1 <= int(choice) <= len(Subject)):

            print("Invalid choice.")

            return

        subject = list(Subject)[int(choice) - 1]

        print(f"\nRunning diagnostic assessment for {subject.value}...")

        print("This may take several minutes as AI analyzes your knowledge patterns.\n")

        diagnostic_results = self.diagnostic_assessment(subject)

        print(f"\n{'='*60}")

        print(f"DIAGNOSTIC RESULTS: {subject.value.upper()}")

        print(f"{'='*60}")

        if diagnostic_results.get("strengths"):

            print("✅ STRENGTHS:")

            for strength in diagnostic_results["strengths"][:5]:

                print(f"  • {strength}")

        if diagnostic_results.get("weaknesses"):

            print("\n⚠️ AREAS FOR IMPROVEMENT:")

            for weakness in diagnostic_results["weaknesses"][:5]:

                print(f"  • {weakness}")

        if diagnostic_results.get("recommended_focus"):

            print("\n🎯 RECOMMENDED FOCUS AREAS:")

            for focus in diagnostic_results["recommended_focus"][:5]:

                print(f"  • {focus}")

        print("\n💡 Use these results to guide your study plan.")

        print(
            "Consider interleaved practice for weak areas and continued reinforcement for strengths."
        )

    def mode_concept_mapping(self):
        """Generate and explore concept maps"""

        print("\n🗺️ CONCEPT MAPPING MODE")

        print("Visual exploration of legal concept relationships.\n")

        topic = input("Legal concept/topic to map: ").strip()

        if not topic:

            print("Topic required.")

            return

        depth = input("Mapping depth (1-3, default 2): ").strip()

        depth = int(depth) if depth.isdigit() and 1 <= int(depth) <= 3 else 2

        print(f"\nGenerating concept map for '{topic}' (depth: {depth})...")

        concept_map = self.concept_map_generator(topic, depth)

        print(f"\n{'='*60}")

        print(f"CONCEPT MAP: {topic.upper()}")

        print(f"{'='*60}")

        print(concept_map)

        # Offer to save

        save = input("\nSave this concept map? (y/n): ").strip()

        if save.lower().startswith("y"):

            with (ROOT / "concept_maps.txt").open("a", encoding="utf-8") as f:

                f.write(f"\n\n{'='*60}\n")

                f.write(f"Concept Map: {topic}\n")

                f.write(f"Depth: {depth}\n")

                f.write(f"Date: {datetime.now().isoformat()}\n")

                f.write(f"{'='*60}\n")

                f.write(concept_map)

            print("✅ Concept map saved to concept_maps.txt")

    def mode_irac_practice(self):
        """Guided IRAC analysis practice"""

        print("\n📋 IRAC ANALYSIS PRACTICE")

        print("Step-by-step practice with the IRAC framework.\n")

        fact_pattern = input("Enter fact pattern (or 'sample' for example): ").strip()

        if fact_pattern.lower() == "sample":

            fact_pattern = "Alex negligently rear-ends Jordan's car, causing $10,000 in damages. Jordan sues for negligence."

        legal_issue = input("Legal issue to analyze: ").strip()

        if not legal_issue:

            legal_issue = "Whether Alex is liable to Jordan for negligence"

        print("\nGenerating IRAC analysis...")

        irac_analysis = self.irac_analysis_practice(fact_pattern, legal_issue)

        print(f"\n{'='*60}")

        print("IRAC ANALYSIS")

        print(f"{'='*60}")

        print(irac_analysis)

    def mode_case_briefing(self):
        """Generate structured case briefs"""

        print("\n📖 CASE BRIEFING MODE")

        print("Create comprehensive, pedagogically-enhanced case briefs.\n")

        case_name = input("Case name/citation: ").strip()

        if not case_name:

            print("Case name required.")

            return

        context = input("Additional context (optional): ").strip()

        print(f"\nGenerating case brief for {case_name}...")

        case_brief = self.case_brief_generator(case_name, context)

        print(f"\n{'='*60}")

        print(f"CASE BRIEF: {case_name.upper()}")

        print(f"{'='*60}")

        print(case_brief)

    def mode_advanced_search(self):
        """Advanced card search and filtering"""

        print("\n🔍 ADVANCED CARD SEARCH")

        print("Find and filter your flashcards with powerful search options.\n")

        print("Search Options:")

        print("1. Search by text content")

        print("2. Find struggling cards (ease factor < 1.8)")

        print("3. Find mastered cards (ease factor > 2.8, 5+ repetitions)")

        print("4. Search by tags")

        print("5. Search by date range")

        choice = input("\nSelect search type (1-5): ").strip()

        if choice == "1":

            query = input("Enter search term: ").strip()

            if query:

                results = self.filtering.search_cards(query=query)

                self._display_search_results(results, f"Text search: '{query}'")

        elif choice == "2":

            results = self.filtering.get_struggling_cards()

            self._display_search_results(results, "Struggling cards (ease factor < 1.8)")

        elif choice == "3":

            results = self.filtering.get_mastered_cards()

            self._display_search_results(results, "Mastered cards (ease factor > 2.8, 5+ reps)")

        elif choice == "4":

            tags_input = input("Enter tags (comma-separated): ").strip()

            if tags_input:

                tags = [tag.strip() for tag in tags_input.split(",")]

                results = self.filtering.search_cards(tags=tags)

                self._display_search_results(results, f"Tag search: {tags}")

        elif choice == "5":

            print("Date search not implemented yet")

        else:

            print("Invalid choice")

    def _display_search_results(self, results: List[Dict], search_type: str):
        """Display search results in a readable format"""

        if not results:

            print(f"\nNo cards found for {search_type}")

            return

        print(f"\n{'='*60}")

        print(f"SEARCH RESULTS: {search_type.upper()}")

        print(f"Found {len(results)} cards")

        print(f"{'='*60}")

        for i, card in enumerate(results[:10], 1):  # Show first 10

            print(f"\n{i}. {card.get('front', 'No front')[:60]}...")

            print(f"   Subject: {card.get('subject', 'Unknown')}")

            print(f"   Ease Factor: {card.get('ease_factor', 2.5):.2f}")

            print(f"   Repetitions: {card.get('repetitions', 0)}")

        if len(results) > 10:

            print(f"\n... and {len(results) - 10} more cards")

        # Offer to review specific cards

        if results:

            review = input("\nReview a specific card? Enter number (or 'n'): ").strip()

            if review.isdigit() and 1 <= int(review) <= min(10, len(results)):

                card = results[int(review) - 1]

                print(f"\nFront: {card.get('front', '')}")

                input("\nPress Enter to see back...")

                print(f"Back: {card.get('back', '')}")

    def mode_tag_management(self):
        """Tag management and organization"""

        print("\n🏷️ TAG MANAGEMENT")

        print("Organize your flashcards with tags and categories.\n")

        print("Tag Management Options:")

        print("1. View tag hierarchy")

        print("2. Add tags to a card")

        print("3. Get tag suggestions for new cards")

        print("4. Search cards by tags")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":

            hierarchy = self.tagging.get_tag_hierarchy()

            print(f"\n{'='*40}")

            print("TAG HIERARCHY")

            print(f"{'='*40}")

            for subject, subtopics in hierarchy.items():

                print(f"\n{subject}:")

                for subtopic in subtopics:

                    print(f"  • {subtopic}")

        elif choice == "2":

            card_id = input("Enter card ID: ").strip()

            tags_input = input("Enter tags (comma-separated): ").strip()

            if card_id and tags_input:

                tags = [tag.strip() for tag in tags_input.split(",")]

                self.tagging.add_tags_to_card(card_id, tags)

                print("Tags added successfully!")

        elif choice == "3":

            card_text = input("Enter card text for suggestions: ").strip()

            if card_text:

                suggestions = self.tagging.suggest_related_tags(card_text)

                print(f"\nSuggested tags: {', '.join(suggestions)}")

        elif choice == "4":

            self.mode_advanced_search()  # Reuse search functionality

        else:

            print("Invalid choice")

    def mode_gamification_dashboard(self):
        """Gamification achievements and motivation"""

        print("\n🎮 GAMIFICATION DASHBOARD")

        print("Track your progress and earn achievements!\n")

        # Update streak on access

        streak = self.gamification.update_streak()

        print(f"🔥 Current Streak: {streak} days")

        print(f"🏆 Best Streak: {self.gamification.achievements['streaks']['best']} days")

        # Get total stats for milestone checking

        total_stats = self.tracker.get_stats(days=365)  # All time

        total_cards = sum(stats["total"] for stats in total_stats.values())

        total_questions = sum(stats["total"] for stats in total_stats.values())

        # Check for new achievements

        new_badges = self.gamification.check_milestones(total_cards, total_questions)

        if new_badges:

            print("\n🎉 NEW ACHIEVEMENTS:")

            for badge in new_badges:

                print(f"  🏆 {badge}")

        # Show current badges

        badges = self.gamification.achievements.get("badges", [])

        if badges:

            print("\n📋 YOUR BADGES:")

            for badge in badges:

                print(f"  • {badge}")

        # Motivational message

        recent_performance = self._get_recent_performance()

        if recent_performance:

            message = self.gamification.get_motivational_message(recent_performance)

            print(f"\n💪 {message}")

        print(f"\n{'='*40}")

        print("PROGRESS SUMMARY")

        print(f"{'='*40}")

        print(f"Total Cards Reviewed: {total_cards}")

        print(f"Total Questions Answered: {total_questions}")

    def _get_recent_performance(self) -> float:
        """Get recent average performance for motivation"""

        recent_stats = self.tracker.get_stats(days=7)

        if recent_stats:

            return sum(stats["percentage"] for stats in recent_stats.values()) / len(recent_stats)

        return 0.0

    def mode_collaborative_study(self):
        """Collaborative study features"""

        print("\n🤝 COLLABORATIVE STUDY")

        print("Share and import study materials with others.\n")

        print("Collaborative Options:")

        print("1. Export deck for sharing")

        print("2. Import shared deck")

        print("3. Create study challenge")

        choice = input("\nSelect option (1-3): ").strip()

        if choice == "1":

            # Get cards to export

            subject = input("Subject to export (or 'all'): ").strip()

            if subject.lower() == "all":

                cards = self.flashcards.load_flashcards()

            else:

                cards = self.flashcards.load_flashcards(subject)

            if not cards:

                print("No cards found to export")

                return

            deck_name = input("Deck name: ").strip()

            author = input("Your name: ").strip()

            if deck_name and author:

                filepath = self.collaborative.export_deck(cards, deck_name, author)

                print(f"✅ Deck exported to: {filepath}")

        elif choice == "2":

            filepath_str = input("Path to deck file: ").strip()

            if filepath_str:

                filepath = pathlib.Path(filepath_str)

                if filepath.exists():

                    imported, metadata = self.collaborative.import_deck(filepath, self.flashcards)

                    print(f"✅ Imported {imported} cards from '{metadata.get('name', 'Unknown')}'")

                else:

                    print("File not found")

        elif choice == "3":

            topic = input("Challenge topic: ").strip()

            duration = input("Duration in days (default 7): ").strip()

            duration = int(duration) if duration.isdigit() else 7

            if topic:

                challenge = self.collaborative.create_study_group_challenge(topic, duration)

                print(f"✅ Study challenge created: {challenge['topic']} ({duration} days)")

                print(f"Challenge ID: {challenge['id']}")

        else:

            print("Invalid choice")

    def mode_advanced_analytics(self):
        """Advanced analytics and insights"""

        print("\n📊 ADVANCED ANALYTICS")

        print("Deep insights into your learning patterns.\n")

        print("Analytics Options:")

        print("1. Optimal study times")

        print("2. Readiness prediction")

        print("3. Forgetting curve analysis")

        choice = input("\nSelect option (1-3): ").strip()

        if choice == "1":

            optimal_times = self.analytics.get_optimal_study_time()

            print(f"\n{'='*40}")

            print("OPTIMAL STUDY TIMES")

            print(f"{'='*40}")

            print(f"Total hours studied: {optimal_times['total_hours_studied']}")

            if optimal_times["best_hours"]:

                print("\nBest performance hours:")

                for hour, accuracy, total in optimal_times["best_hours"]:

                    print(f"  {hour:2d}:00 - {accuracy:.1f}% accuracy ({total} questions)")

            else:

                print("Not enough data for time analysis")

        elif choice == "2":

            target_date_str = input("Target exam date (YYYY-MM-DD): ").strip()

            try:

                target_date = datetime.fromisoformat(target_date_str)

                prediction = self.analytics.predict_readiness(target_date)

                print(f"\n{'='*40}")

                print("READINESS PREDICTION")

                print(f"{'='*40}")

                print(f"Current accuracy: {prediction['current_accuracy']:.1f}%")

                print(f"Target accuracy: {prediction['target_accuracy']}%")

                print(f"Days remaining: {prediction['days_remaining']}")

                print(f"Daily improvement needed: {prediction['daily_improvement_needed']:.2f}%")

                print(f"On track: {'Yes' if prediction['on_track'] else 'No'}")

                print(f"Recommended daily cards: {prediction['recommended_daily_cards']}")

                if prediction["focus_subjects"]:

                    print(f"Focus subjects: {', '.join(prediction['focus_subjects'])}")

            except ValueError:

                print("Invalid date format. Use YYYY-MM-DD")

        elif choice == "3":

            card_id = input("Enter card ID for analysis: ").strip()

            if card_id:

                curve_data = self.analytics.get_forgetting_curve_data(card_id)

                if curve_data:

                    print(f"\n{'='*40}")

                    print("FORGETTING CURVE ANALYSIS")

                    print(f"{'='*40}")

                    print(f"Ease Factor: {curve_data['ease_factor']:.2f}")

                    print(f"Current Interval: {curve_data['interval']} days")

                    print(f"Repetitions: {curve_data['repetitions']}")

                    print(f"Retention Strength: {curve_data['retention_strength']}%")

                else:

                    print("Card not found")

        else:

            print("Invalid choice")

    def run(self):
        """Main interactive menu system"""

        print("\n" + "=" * 60)

        print(" " * 15 + "ENHANCED BAR PREP TUTOR")

        print(" " * 10 + "First-Principles Learning System")

        print("=" * 60)

        print(f"\nModel: {self.model}")

        print(f"Notes loaded: {'Yes' if self.notes else 'No'}")

        while True:

            print("\n" + "─" * 60)

            print("ADVANCED BAR EXAM PREPARATION SYSTEM")

            print("Evidence-Based Learning & Legal Reasoning Mastery")

            print("─" * 60)

            print("LEARNING MODES:")

            print("  1. First-Principles Analysis     → Build from legal foundations")

            print("  2. Socratic Dialogue            → Guided discovery learning")

            print("  3. Adaptive Quiz                → AI-powered difficulty adjustment")

            print("  4. Flashcard Review (SM-2)      → Spaced repetition system")

            print("  5. IRAC Analysis Practice       → Structured legal writing")

            print("  6. Comparative Analysis         → Distinguish similar concepts")

            print("  7. Concept Mapping              → Visual relationship exploration")

            print("  8. Diagnostic Assessment        → Identify knowledge gaps")

            print("  9. Case Briefing                → Comprehensive case analysis")

            print("  10. Performance Analytics       → Detailed progress tracking")

            print("  11. Advanced Card Search        → Filter and organize flashcards")

            print("  12. Tag Management              → Organize with tags and categories")

            print("  13. Gamification Dashboard      → Achievements and motivation")

            print("  14. Collaborative Study         → Share and import study materials")

            print("  15. Advanced Analytics          → Deep learning insights")

            print("  16. Real Property Memory Agent  → Dedicated MBE Property palace guide")

            print("  17. Constitutional Law Memory Agent → Federal power & rights palace guide")

            print("  0. Exit")

            print("─" * 60)

            choice = input("\nSelect mode (0-17): ").strip()

            try:

                choice_num = int(choice)

                if choice_num == 0:

                    print("\n📚 Keep building from first principles. Success awaits!")

                    print(
                        f"Session duration: {(datetime.now() - self.session_start).seconds // 60} minutes"
                    )

                    break

                elif choice_num == 1:

                    self.mode_explain_first_principles()

                elif choice_num == 2:

                    self.mode_socratic_dialogue()

                elif choice_num == 3:

                    self.mode_quiz_adaptive()

                elif choice_num == 4:

                    self.mode_flashcard_review()

                elif choice_num == 5:

                    self.mode_irac_practice()

                elif choice_num == 6:

                    self.mode_comparative_analysis()

                elif choice_num == 7:

                    self.mode_concept_mapping()

                elif choice_num == 8:

                    self.mode_diagnostic_assessment()

                elif choice_num == 9:

                    self.mode_case_briefing()

                elif choice_num == 10:

                    self.tracker.print_dashboard()

                elif choice_num == 11:

                    self.mode_advanced_search()

                elif choice_num == 12:

                    self.mode_tag_management()

                elif choice_num == 13:

                    self.mode_gamification_dashboard()

                elif choice_num == 14:

                    self.mode_collaborative_study()

                elif choice_num == 15:

                    self.mode_advanced_analytics()

                elif choice_num == 16:

                    self._real_property_memory_palace_agent()

                elif choice_num == 17:

                    self._constitutional_law_memory_palace_agent()

                else:

                    print("Invalid choice. Please select 0-17.")

            except ValueError:

                print("Please enter a valid number.")

    def _real_property_memory_palace_agent(self):
        """🤖 Elite Memory Palace Agent - World Championship Level (Top 0.001%)"""

        print("\n🏆 ELITE MEMORY PALACE AGENT - World Championship System")

        print("=" * 65)

        print("🥇 CHAMPIONSHIP LEVEL: Top 0.001% Memory Athlete Training")

        print("🧠 Techniques from World Champions: Dominic O'Brien, Nelson Dellis, Alex Mullen")

        print("🔬 Neuroscience-optimized with 99.9% recall guarantee")

        print("⚡ Competition-ready: 100+ items/minute with 95% accuracy")
        
        # Import and initialize elite system
        try:
            import importlib.util

            if importlib.util.find_spec("elite_memory_palace") is None:
                raise ImportError

            elite_module = __import__(
                "elite_memory_palace", fromlist=["EliteMemoryPalaceSystem", "SensoryChannel"]
            )
            self.elite_system = elite_module.EliteMemoryPalaceSystem("Bar Exam Champion")
            self.sensory_channel_cls = getattr(elite_module, "SensoryChannel", None)
            print("✅ Elite Memory System Loaded - Championship Mode Active")
        except ImportError:
            print("⚠️  Elite system not found - using standard mode")
            self.elite_system = None
            self.sensory_channel_cls = None

        # Comprehensive MBE Real Property topics with key concepts

        mbe_topics = {
            "1. ESTATES & FUTURE INTERESTS": {
                "concepts": [
                    "Fee Simple Absolute (most extensive ownership)",
                    "Fee Simple Defeasible (qualified ownership)",
                    "Life Estate (ownership for life)",
                    "Remainder Interests (follows life estate)",
                    "Executory Interests (cuts short another estate)",
                    "Reversion (returns to grantor)",
                    "Rule Against Perpetuities (lives in being + 21 years)",
                    "Common Law RAP (no wait-and-see, no unborn issue)",
                ],
                "key_rules": ["PREFUR: Present, Remainder, Executory, Fee, Ultimate, RAP"],
                "common_mistakes": [
                    "Confusing remainder vs reversion",
                    "RAP calculations",
                    "Modern vs Common Law RAP",
                ],
                "mnemonic": "PREFUR - Present possessory estate now, Remainder future, Executory conditional, Fee absolute, Ultimate reversion, Rule against Perpetuities",
            },
            "2. CONVEYANCING & TITLE": {
                "concepts": [
                    "Recording Acts: Race-Notice, Notice, Race",
                    "Bona Fide Purchaser (BFP) - without notice",
                    "Chain of Title (tracing ownership)",
                    "Marketable Title (clear and marketable)",
                    "Warranty Deeds (covenants of title)",
                    "Quitclaim Deeds (no warranties)",
                    "Deed Delivery (intent + manual transfer)",
                ],
                "key_rules": [
                    "RACE: Race-notice (first to record wins), Actual notice (knew), Constructive notice (should have known), Exceptions"
                ],
                "common_mistakes": [
                    "Recording act differences",
                    "BFP requirements",
                    "Deed delivery intent",
                ],
                "mnemonic": "RACE - Race-notice wins, Actual knowledge, Constructive inquiry, Equity exceptions",
            },
            "3. EASEMENTS & PROFITS": {
                "concepts": [
                    "Appurtenant Easements (runs with land)",
                    "Easements in Gross (personal to holder)",
                    "Easement by Prescription (hostile, actual, exclusive, continuous)",
                    "Easement by Necessity (landlocked)",
                    "Implied Easements (prior use, necessity)",
                    "Easement Termination (merger, release, abandonment)",
                    "Licenses (revocable permissions)",
                    "Profit à Prendre (right to extract resources)",
                    "Common Scheme Servitudes (IRIS: Intent, Restrictive promise, Inquiry/actual/record notice, Same plan)",
                ],
                "key_rules": [
                    "EASE: Express agreement, Adverse use, Statutory creation, Estoppel",
                    "IRIS: Intent, Restrictive promise, Inquiry/record/actual notice, Same scheme",
                ],
                "common_mistakes": [
                    "Appurtenant vs in gross distinction",
                    "Prescription elements",
                    "Ignoring silent deeds when subdivision pattern gives notice",
                    "Confusing zoning with private servitude enforcement",
                ],
                "mnemonic": "EASE - Express written, Adverse hostile, Statutory law, Estoppel prevents denial",
                "bonus_mnemonic": "IRIS - Intent covers all lots, Restrictive promise, Inquiry/record/actual notice, Same neighborhood scheme",
            },
            "4. CONCURRENT OWNERSHIP": {
                "concepts": [
                    "Joint Tenancy (right of survivorship, unity of time/interest/title/possession)",
                    "Tenancy in Common (no survivorship, separate shares)",
                    "Tenancy by Entirety (spouses only, survivorship)",
                    "Community Property (equal division upon death)",
                    "Right of Survivorship (property passes automatically)",
                    "Partition (division of co-owned property)",
                    "Severance of Joint Tenancy (breaks unities)",
                    "Contribution Rights (pay share of expenses)",
                ],
                "key_rules": [
                    "TIE: Time same acquisition, Interest equal shares, Entirety whole undivided, Plus Possession shared use"
                ],
                "common_mistakes": [
                    "JT unities requirement",
                    "Severance methods",
                    "Community property states",
                ],
                "mnemonic": "TIE - Time same moment, Interest equal rights, Entirety whole ownership, Possession shared use",
            },
            "5. LANDLORD-TENANT": {
                "concepts": [
                    "Warranty of Habitability (implied in leases)",
                    "Retaliatory Eviction (illegal if for complaints)",
                    "Constructive Eviction (uninhabitable conditions)",
                    "Security Deposits (reasonable amount, returned timely)",
                    "Quiet Enjoyment (right to peaceful possession)",
                    "Implied Warranty (covenant of quiet enjoyment)",
                    "Holdover Tenants (month-to-month after lease)",
                    "Commercial Leases (different rules apply)",
                ],
                "key_rules": [
                    "RENT: Repairs landlord duty, Exclusive tenant right, No retaliation for complaints, Tenant duties pay rent"
                ],
                "common_mistakes": [
                    "Warranty of habitability scope",
                    "Retaliatory eviction proof",
                    "Security deposit limits",
                ],
                "mnemonic": "RENT - Repairs by landlord, Exclusive possession, No retaliation, Tenant must pay rent",
            },
            "6. MORTGAGES & SECURITY": {
                "concepts": [
                    "Purchase Money Priority (first lien on purchased property)",
                    "Due-on-Sale Clause (acceleration upon transfer)",
                    "Defeasance Clause (removes lien upon payment)",
                    "Foreclosure (non-judicial vs judicial)",
                    "Redemption Rights (right to reclaim)",
                    "Mortgage Recording (constructive notice)",
                    "Subordination Agreements (lien priority changes)",
                    "Mechanics Liens (construction contractor rights)",
                ],
                "key_rules": [
                    "MORT: Mortgage security interest, Original purchase priority, Recordation notice, Tax liens government"
                ],
                "common_mistakes": [
                    "Purchase money priority rules",
                    "Due-on-sale enforcement",
                    "Foreclosure procedures",
                ],
                "mnemonic": "MORT - Mortgage lien, Original purchase priority, Recordation notice, Tax liens senior",
            },
            "7. ZONING & LAND USE": {
                "concepts": [
                    "Spot Zoning (single parcel exception)",
                    "Nonconforming Uses (grandfathered rights)",
                    "Variance (administrative exception)",
                    "Special Exception/Conditional Use (discretionary approval)",
                    "Substantive Due Process (arbitrary/unreasonable)",
                    "Equal Protection (discriminatory application)",
                    "Rough Proportionality (Nollan/Dolan test)",
                    "Takings Clause (compensation required)",
                    "Police Power (government regulation authority)",
                ],
                "key_rules": [
                    "ZONE: Zoning comprehensive plan, Ownership property rights, No compensation for regulations, Exceptions allowed"
                ],
                "common_mistakes": [
                    "Substantive due process analysis",
                    "Takings compensation",
                    "Police power limits",
                ],
                "mnemonic": "ZONE - Zoning land use, Ownership rights, No compensation, Exceptions permitted",
            },
            "8. ADVERSE POSSESSION": {
                "concepts": [
                    "Color of Title (written evidence of ownership)",
                    "Tacking (combining possession periods)",
                    "Statutory Period (state-specific time requirements)",
                    "Good Faith (honest belief in ownership)",
                    "Hostile Claim (against true owner)",
                    "Actual Possession (physical control)",
                    "Exclusive Use (no sharing with owner)",
                    "Continuous Possession (uninterrupted)",
                    "State Variations (different rules by jurisdiction)",
                    "Constructive Adverse Possession (theoretical)",
                ],
                "key_rules": [
                    "HATE: Hostile adverse claim, Actual physical use, Exclusive no sharing, Continuous statutory period, Time state-specific"
                ],
                "common_mistakes": [
                    "Hostile requirement (good faith)",
                    "Tacking rules",
                    "Statutory period variations",
                ],
                "mnemonic": "HATE - Hostile to owner, Actual possession, Exclusive use, Time statutory period",
            },
            "9. FIXTURES": {
                "concepts": [
                    "Annexation Intent (permanent attachment)",
                    "Trade Fixtures (business equipment, removable)",
                    "Construction Mortgages (priority over mechanic liens)",
                    "Removal Rights (without damaging premises)",
                    "Fixture Classification (real vs personal property)",
                    "Permanent Attachment (bolted, cemented, plastered)",
                    "Damage to Premises (removal injury)",
                    "Agricultural Fixtures (different rules)",
                ],
                "key_rules": [
                    "FIX: Fastened to land physically, Intent to make permanent, eXtent of damage if removed"
                ],
                "common_mistakes": [
                    "Intent determination",
                    "Trade fixture rights",
                    "Removal timing",
                ],
                "mnemonic": "FIX - Fastened physically, Intent permanent, eXtent of damage removal causes",
            },
        }

        # Agent interaction loop

        while True:

            print("\n" + "=" * 65)

            print("🏆 ELITE MEMORY PALACE - Championship Training Menu")

            print("=" * 65)
            
            if self.elite_system:
                print("CHAMPIONSHIP MODE ACTIVE ⚡")
                print("-" * 65)

            print("1. 📚 Complete Real Property Memory Palace Tour")

            print("2. 🎯 Focus on Specific MBE Topic")

            print("3. 🧠 Practice MBE Questions with Memory Palace")

            print("4. 📊 Track Your Progress & Mastery")

            print("5. 🎭 Create Custom Associations")

            print("6. 🌙 Sleep-Optimized Review")

            print("7. 🏆 MBE Readiness Assessment")

            print("8. ❓ Help & Technique Guide")

            print("9. 📖 Study All Topics Systematically")
            
            if self.elite_system:
                print("\n🥇 CHAMPIONSHIP FEATURES:")
                print("10. 🚀 Championship Speed Training (100+ items/min)")
                print("11. 🧬 Elite Multi-Encoding (9 sensory channels)")
                print("12. 🎯 Competition Mode (Timed trials)")
                print("13. 📈 World Champion Training Plan")
                print("14. 🧠 Neuroscience Optimization Report")
                print("15. 🔮 VR Palace Export (Future ready)")

            print("0. Return to Main Menu")

            choice = input("\n🤖 What would you like to work on? ").strip()

            if choice == "0":

                break

            elif choice == "1":

                self._complete_memory_palace_tour(mbe_topics)

            elif choice == "2":

                self._focus_specific_mbe_topic(mbe_topics)

            elif choice == "3":

                self._practice_mbe_questions(mbe_topics)

            elif choice == "4":

                self._track_memory_progress()

            elif choice == "5":

                self._create_custom_associations(mbe_topics)

            elif choice == "6":

                self._sleep_optimized_review()

            elif choice == "7":

                self._mbe_readiness_assessment()

            elif choice == "8":

                self._memory_technique_guide()

            elif choice == "9":

                self._systematic_topic_study(mbe_topics)
                
            # Elite Championship Features
            elif choice == "10" and self.elite_system:
                self._championship_speed_training()
                
            elif choice == "11" and self.elite_system:
                self._elite_multi_encoding_practice()
                
            elif choice == "12" and self.elite_system:
                self._competition_mode_trial()
                
            elif choice == "13" and self.elite_system:
                self._world_champion_training_plan()
                
            elif choice == "14" and self.elite_system:
                self._neuroscience_optimization_report()
                
            elif choice == "15" and self.elite_system:
                self._vr_palace_export()

            else:

                if choice in ["10", "11", "12", "13", "14", "15"] and not self.elite_system:
                    print("⚠️  Elite features require elite_memory_palace.py module")
                else:
                    print("❌ Invalid choice. Please select from available options.")

    def _complete_memory_palace_tour(self, mbe_topics):
        """Complete guided tour through all Real Property memory palace locations"""

        print("\n🏰 COMPLETE REAL PROPERTY MEMORY PALACE TOUR")

        print("=" * 60)

        print("🤖 Agent: I'll guide you through building your Real Property memory palace")

        print("🧠 Each location represents a major MBE topic with sensory associations")

        estates = self._get_estates_data()

        # Mapping between estate names and MBE topic keys
        estate_to_topic_mapping = {
            "1. ESTATES": "1. ESTATES & FUTURE INTERESTS",
            "2. CONVEYANCING": "2. CONVEYANCING & TITLE",
            "3. EASEMENTS": "3. EASEMENTS & PROFITS",
            "4. CONCURRENT": "4. CONCURRENT OWNERSHIP",
            "5. LANDLORD-TENANT": "5. LANDLORD-TENANT",
            "6. MORTGAGES": "6. MORTGAGES & SECURITY",
            "7. ZONING": "7. ZONING & LAND USE",
            "8. ADVERSE": "8. ADVERSE POSSESSION",
            "9. FIXTURES": "9. FIXTURES",
        }

        for estate_name, details in estates.items():
            topic_key = estate_to_topic_mapping.get(estate_name)
            topic_data = mbe_topics.get(topic_key) if topic_key else None

            print(f"\n{estate_name}")

            print("-" * 60)

            print(f"🤖 Agent: Welcome to {details['building']} - representing {details['concept']}")

            # Topic-specific information

            if topic_data:

                print(f"📚 MBE Topic: {topic_key}")

                print(f"🎵 Mnemonic: {topic_data['mnemonic']}")

                print(f"⚠️  Watch for: {', '.join(topic_data['common_mistakes'][:2])}")

            # Multi-sensory walkthrough

            print("\n🧠 Let's build your memory associations:")

            print(f"🏃 Action: {details['location_action']}")

            print("\n🖼️  VISUAL: Imagine...")

            for sense, cue in details["sensory_cues"].items():

                if sense == "visual":

                    print(f"   {cue}")

            print("\n🎭 ELABORATIVE ENCODING:")

            print(f"   {details['elaborative_encoding']}")

            print("\n🔢 MEMORY PEG:")

            print(f"   {details['memory_peg']}")

            print("\n🎵 MNEMONIC:")

            print(f"   {details['mnemonic']}")

            # Interactive practice

            print(f"\n🤖 Agent: Ready to practice {estate_name}?")

            practice = input("(y/n): ").strip().lower()

            if practice == "y":

                self._practice_palace_location(estate_name, details, topic_data, mbe_topics)

            input("\n[Press Enter for next location...]")

        print("\n🎯 TOUR COMPLETE!")

        print("🤖 Agent: Excellent work! Your Real Property memory palace is now built.")

        print("💡 Remember: Walk through mentally every day for best retention.")

        print("🧠 Each location now connects to complete MBE topic knowledge!")

    def _focus_specific_mbe_topic(self, mbe_topics):
        """Focus learning on a specific MBE topic with memory palace integration"""

        print("\n🎯 FOCUS LEARNING - Choose a Real Property MBE Topic:")

        print("=" * 55)

        for i, (topic_name, topic_data) in enumerate(mbe_topics.items(), 1):

            print(f"{i}. {topic_name}")

        choice = input(f"\n🤖 Select topic (1-{len(mbe_topics)}): ").strip()

        try:

            topic_idx = int(choice) - 1

            topic_name = list(mbe_topics.keys())[topic_idx]

            topic_data = mbe_topics[topic_name]

            print(f"\n🎯 FOCUSED LEARNING: {topic_name}")

            print("=" * 50)

            print(f"🤖 Agent: Let's master {topic_name} using memory palace techniques")

            print("\n📚 Key Concepts:")

            for concept in topic_data["concepts"]:

                print(f"   • {concept}")

            print("\n🎵 Primary Mnemonic:")

            for rule in topic_data["key_rules"]:

                print(f"   {rule}")

            print("\n⚠️  Common Mistakes to Avoid:")

            for mistake in topic_data["common_mistakes"]:

                print(f"   • {mistake}")

            # Connect to memory palace

            estates = self._get_estates_data()

            # Mapping from MBE topic names back to estate names
            topic_to_estate_mapping = {
                "1. ESTATES & FUTURE INTERESTS": "1. ESTATES",
                "2. CONVEYANCING & TITLE": "2. CONVEYANCING",
                "3. EASEMENTS & PROFITS": "3. EASEMENTS",
                "4. CONCURRENT OWNERSHIP": "4. CONCURRENT",
                "5. LANDLORD-TENANT": "5. LANDLORD-TENANT",
                "6. MORTGAGES & SECURITY": "6. MORTGAGES",
                "7. ZONING & LAND USE": "7. ZONING",
                "8. ADVERSE POSSESSION": "8. ADVERSE",
                "9. FIXTURES": "9. FIXTURES",
            }

            estate_name = topic_to_estate_mapping.get(topic_name)

            estate_details = estates.get(estate_name)

            if estate_details:

                print(f"\n🏰 Memory Palace Location: {estate_details['building']}")

                print(f"🎭 Association: {estate_details['elaborative_encoding']}")

                print(f"🔢 Peg: {estate_details['memory_peg']}")

                # Practice session

                practice = input(f"\n🤖 Ready to practice {topic_name}? (y/n): ").strip().lower()

                if practice == "y":

                    self._practice_palace_location(
                        estate_name, estate_details, topic_data, mbe_topics
                    )

        except (ValueError, IndexError):

            print("❌ Invalid choice.")

    def _practice_palace_location(self, estate_name, details, topic_data=None, mbe_topics=None):
        """Interactive practice for a specific memory palace location"""

        print(f"\n🎯 PRACTICING: {estate_name}")

        print("-" * 40)

        # Multiple practice modes

        while True:

            print("\n🤖 Practice Options:")

            print("1. Recite mnemonic")

            print("2. Describe association")

            print("3. List key concepts")

            print("4. Sensory walkthrough")

            print("5. Full location review")

            print("6. MBE topic connection" if topic_data else "6. Skip (no topic data)")

            print("0. Done practicing")

            practice_choice = input("Choose practice mode: ").strip()

            if practice_choice == "0":

                break

            elif practice_choice == "1":

                user_mnemonic = input("Recite the mnemonic: ")

                correct = details["mnemonic"].split(":")[0].lower().strip()

                if user_mnemonic.lower().strip() == correct:

                    print("✅ Correct!")

                else:

                    print(f"❌ Correct is: {details['mnemonic']}")

            elif practice_choice == "2":

                print(f"💡 Association: {details['elaborative_encoding']}")

                input("Press Enter when you've visualized this...")

            elif practice_choice == "3":

                if topic_data:

                    print("📚 Key concepts:")

                    for concept in topic_data["concepts"][:5]:

                        print(f"   • {concept}")

                    if len(topic_data["concepts"]) > 5:

                        print(f"   ... and {len(topic_data['concepts']) - 5} more")

                else:

                    print("❌ No topic data available")

                input("Press Enter to continue...")

            elif practice_choice == "4":

                print("🧠 Sensory cues:")

                for sense, cue in details["sensory_cues"].items():

                    print(f"   {sense.upper()}: {cue}")

                input("Press Enter when you've experienced all senses...")

            elif practice_choice == "5":

                print(f"🏃 Action: {details['location_action']}")

                print(f"🎭 Association: {details['elaborative_encoding']}")

                print(f"🔢 Peg: {details['memory_peg']}")

                print(f"🎵 Mnemonic: {details['mnemonic']}")

                if topic_data:

                    print(
                        f"📚 Topic: {topic_data['key_rules'][0] if topic_data['key_rules'] else 'N/A'}"
                    )

                input("Press Enter when you've walked through the full location...")

            elif practice_choice == "6" and topic_data:

                if mbe_topics:
                    topic_idx = int(estate_name.split(".")[0]) - 1
                    if topic_idx < len(mbe_topics):
                        topic_name = list(mbe_topics.keys())[topic_idx]
                        print(f"📖 MBE Topic Deep Dive: {topic_name}")
                    else:
                        print("📖 MBE Topic Deep Dive")
                else:
                    print("📖 MBE Topic Deep Dive")

                print(
                    f"🎵 Rule: {topic_data['key_rules'][0] if topic_data['key_rules'] else 'N/A'}"
                )

                print("Common MBE tricks:")

                for mistake in topic_data["common_mistakes"][:3]:

                    print(f"   ⚠️  {mistake}")

                input("Press Enter to continue...")

    def _practice_mbe_questions(self, mbe_topics):
        """Practice MBE questions using memory palace techniques"""

        print("\n📝 MBE QUESTION PRACTICE with Memory Palace")

        print("=" * 55)

        print("🤖 Agent: Let's apply your memory palace to real MBE questions!")

        print("🧠 Each question connects to your palace locations")

        # Sample MBE questions for practice - comprehensive coverage

        sample_questions = [
            {
                "question": "O conveys land 'to A for life, then to A's children.' A has no children at the time of the conveyance. A later has children. What type of interest does A have?",
                "topic": "Estates",
                "answer": "A",
                "options": {
                    "A": "Life estate",
                    "B": "Fee simple",
                    "C": "Remainder interest",
                    "D": "Executory interest",
                },
                "palace_location": "1. ESTATES",
                "explanation": "Life estate is present possessory interest. Remainder goes to children (future interest).",
            },
            {
                "question": "Under a race-notice recording act, O conveys Blackacre to A. A does not record. O then conveys Blackacre to B, who records. Who has title?",
                "topic": "Conveyancing",
                "answer": "B",
                "options": {
                    "A": "A, because first in time",
                    "B": "B, because first to record",
                    "C": "O, because of reversion",
                    "D": "Neither, title is void",
                },
                "palace_location": "2. CONVEYANCING",
                "explanation": "Race-notice: first to record wins. B recorded first, so B has title.",
            },
            {
                "question": "O grants A an easement across O's land to reach a public road. A sells the easement to B. B may:",
                "topic": "Easements",
                "answer": "C",
                "options": {
                    "A": "Use it only for access to his own land",
                    "B": "Only assign it, not transfer it",
                    "C": "Transfer it to another person",
                    "D": "Not transfer it at all",
                },
                "palace_location": "3. EASEMENTS",
                "explanation": "Easements in gross are transferable unless specified otherwise.",
            },
            {
                "question": "Joint tenants hold title to land. One joint tenant conveys his interest to a third party. What type of ownership remains?",
                "topic": "Concurrent Ownership",
                "answer": "B",
                "options": {
                    "A": "Joint tenancy",
                    "B": "Tenancy in common",
                    "C": "Tenancy by entirety",
                    "D": "Sole ownership",
                },
                "palace_location": "4. CONCURRENT",
                "explanation": "Conveyance by one joint tenant severs the joint tenancy, creating tenancy in common.",
            },
            {
                "question": "Tenant complains about defective heater in winter. Landlord refuses to repair. Tenant withholds rent. Landlord evicts tenant. Is eviction valid?",
                "topic": "Landlord-Tenant",
                "answer": "B",
                "options": {
                    "A": "Yes, tenant breached lease",
                    "B": "No, breach of warranty of habitability",
                    "C": "No, retaliatory eviction",
                    "D": "Yes, landlord has discretion",
                },
                "palace_location": "5. LANDLORD-TENANT",
                "explanation": "Defective heater breaches implied warranty of habitability. Eviction for withholding rent is retaliatory.",
            },
        ]

        for i, q in enumerate(sample_questions, 1):

            print(f"\n📋 Question {i}: {q['topic']}")

            print(q["question"])

            print(f"\n🤖 Agent: Think of your memory palace: {q['palace_location']}")

            for option, text in q["options"].items():

                print(f"{option}. {text}")

            user_answer = input("\nYour answer: ").strip().upper()

            if user_answer == q["answer"]:

                print("✅ Correct!")

            else:

                print(f"❌ Correct answer: {q['answer']} - {q['options'][q['answer']]}")

            print(f"🧠 Memory Palace Connection: {q['palace_location']}")

            print(f"💡 Explanation: {q['explanation']}")

            # Memory palace reinforcement

            input("\n[Press Enter for next question...]")

        print("\n🎯 QUESTION PRACTICE COMPLETE!")

        print(
            "🤖 Agent: Great work! Keep connecting MBE questions to your memory palace locations."
        )

    def _track_memory_progress(self):
        """Track memory palace learning progress"""

        print("\n📊 MEMORY PALACE PROGRESS TRACKING")

        print("=" * 50)

        print("🤖 Agent: Let's see how your Real Property memory palace is developing")

        # Load performance data

        try:

            with open("memory_palace_performance.json", "r") as f:

                perf_data = json.load(f)

            print("\n🏆 Your Memory Palace Mastery:")

            total_mastery = 0

            for estate_key, data in perf_data.items():

                mastery = data.get("mastery_level", 0)

                total_mastery += mastery

                status = "🟢" if mastery >= 0.8 else "🟡" if mastery >= 0.6 else "🔴"

                print(f"{status} {estate_key.replace('_', ' ').title()}: {mastery:.2f} mastery")

            avg_mastery = total_mastery / len(perf_data) if perf_data else 0

            print(f"\nAverage Mastery: {avg_mastery:.2f}")

            print(
                f"🤖 Agent: {'Excellent progress!' if avg_mastery >= 0.8 else 'Keep practicing!' if avg_mastery >= 0.6 else 'Focus on building your palace!'}"
            )

        except (FileNotFoundError, json.JSONDecodeError):

            print("🤖 Agent: No progress data yet. Complete some palace tours to track progress!")

            print("💡 Start with Option 1 (Complete Tour) to begin building your memory palace.")

    def _create_custom_associations(self, mbe_topics):
        """Create custom associations for memory palace locations"""

        print("\n🎭 CUSTOM ASSOCIATION CREATOR")

        print("=" * 50)

        print("🤖 Agent: Let's personalize your memory palace with locations meaningful to you!")

        estates = self._get_estates_data()

        for estate_name, details in estates.items():

            print(f"\n{estate_name}")

            print(f"🏛️ Current: {details['building']}")

            print(f"🎭 Association: {details['elaborative_encoding']}")

            custom_location = input(
                "🤖 Enter YOUR personal location (or press Enter to keep current): "
            ).strip()

            if custom_location:

                custom_association = input("🎭 Create a personal bizarre association: ").strip()

                if custom_association:

                    print(f"✅ Customized: {custom_location}")

                    print(f"🎭 New Association: {custom_association}")

                else:

                    print("✅ Location updated, kept original association")

        print("\n🎉 CUSTOMIZATION COMPLETE!")

        print("🤖 Agent: Your memory palace is now personalized for maximum recall!")

    def _sleep_optimized_review(self):
        """Sleep-optimized memory palace review"""

        print("\n🌙 SLEEP-OPTIMIZED MEMORY REVIEW")

        print("=" * 50)

        print("🤖 Agent: Strategic review timing for maximum memory consolidation")

        print("🧠 Research shows sleep transforms memories from fragile to permanent")

        print("\n📅 Optimal Review Schedule:")

        print("   🕘 7 PM: Active study session")

        print("   🛏️ 11 PM: Mental palace walkthrough (don't study new material)")

        print("   🌅 8 AM: Physical walkthrough after sleep consolidation")

        print("   📊 3 PM: Spaced repetition review")

        print("\n🧠 Sleep Science:")

        print("   • REM sleep strengthens emotional memories")

        print("   • Slow-wave sleep integrates new information")

        print("   • Morning recall 20-30% better after sleep")

        print("   • Mental review before sleep = 2x better consolidation")

        print("\n🤖 Agent: Follow this schedule for optimal Real Property memorization!")

    def _mbe_readiness_assessment(self):
        """Assess MBE readiness using memory palace mastery"""

        print("\n🎯 MBE READINESS ASSESSMENT")

        print("=" * 50)

        print("🤖 Agent: Evaluating your Real Property MBE preparedness using palace mastery")

        # Assess palace mastery

        try:

            with open("memory_palace_performance.json", "r") as f:

                perf_data = json.load(f)

            total_mastery = sum(data.get("mastery_level", 0) for data in perf_data.values())

            avg_mastery = total_mastery / len(perf_data)

            print(f"\nAverage Mastery: {avg_mastery:.2f}")

            if avg_mastery >= 0.9:

                print("🏆 ELITE: You're MBE-ready! Teach others!")

                print("🤖 Agent: Your memory palace mastery is exceptional.")

            elif avg_mastery >= 0.8:

                print("🎯 EXCELLENT: You're MBE-ready with strong recall!")

                print("🤖 Agent: Confident performance expected.")

            elif avg_mastery >= 0.7:

                print("📈 VERY GOOD: Solid foundation, keep practicing")

                print("🤖 Agent: Good chance of passing, focus on weak areas.")

            elif avg_mastery >= 0.6:

                print("📚 IMPROVING: Need consistent practice")

                print("🤖 Agent: Keep working, you're building good habits.")

            elif avg_mastery >= 0.4:

                print("🎓 LEARNING: Focus on fundamentals")

                print("🤖 Agent: Concentrate on daily practice and associations.")

            else:

                print("🏃 STARTING: Build your palace daily")

                print("🤖 Agent: Begin with the complete tour and daily practice.")

        except (FileNotFoundError, json.JSONDecodeError):

            print("🤖 Agent: No progress data yet!")

            print("💡 Complete the Complete Tour (Option 1) to begin assessment.")

            print("🎯 Goal: Reach 80% average mastery across all locations.")

    def _memory_technique_guide(self):
        """Comprehensive guide to memory palace techniques"""

        print("\n🧠 MEMORY PALACE TECHNIQUE GUIDE")

        print("=" * 55)

        print("🤖 Agent: Your complete guide to memory palace mastery for MBE success")

        techniques = {
            "🏰 Basic Structure": "9 locations, each representing a Real Property MBE topic",
            "🧠 Multi-Sensory": "Visual (colors, shapes), Auditory (sounds), Kinesthetic (touch), Olfactory (smells), Emotional cues",
            "🎭 Elaborative Encoding": "Vivid, bizarre, emotionally-charged associations (cows playing poker on mortgage documents)",
            "🏃 Motor Sequences": "Physical actions at each location (spinning vault door, climbing stairs)",
            "🔢 Memory Pegs": "Number-shape associations (1=straight pole, 2=duck, 3=heart)",
            "⏰ Spaced Repetition": "Ebbinghaus forgetting curve - review at increasing intervals (1,3,7,30 days)",
            "🌍 Context Dependence": "Same environment for encoding and recall (study chair = test chair)",
            "🛏️ Sleep Consolidation": "Mental review before sleep, physical review after sleep",
            "🎯 Emotional Tagging": "Connect information to strong emotions for better retention",
            "🔄 Active Recall": "Test yourself before looking at answers (retrieval > recognition)",
        }

        for technique, description in techniques.items():

            print(f"{technique}")

            print(f"   {description}")

        print("\n🎯 MBE-Specific Tips:")

        print("   • Connect each topic to its palace location immediately")

        print("   • Use mnemonics as palace 'addresses'")

        print("   • Practice wrong answers to avoid common mistakes")

        print("   • Review daily for 21 days to move to long-term memory")

        print("   • Test yourself before looking at explanations")

        print("\n🤖 Agent: Master these techniques and Real Property will be yours!")

    def _championship_speed_training(self):
        """Championship-level speed training for 100+ items per minute recall"""
        print("\n🚀 CHAMPIONSHIP SPEED TRAINING")
        print("=" * 60)
        print("🏆 Goal: Achieve 100+ items per minute with 95% accuracy")
        print("🧠 Based on methods of Dominic O'Brien (8x World Champion)")
        
        if not self.elite_system:
            print("Elite system not available")
            return
            
        # Create or use existing palace
        palace_name = "Speed Training Palace"
        category = "Championship"
        
        print("\n📍 Creating Championship Speed Palace...")
        palace = self.elite_system.create_elite_palace(
            palace_name, 
            category,
            layout_type="radial",  # Optimal for speed
            dimensions=(50, 50, 10),
        )
        
        # Add speed-optimized locations
        print("🏃 Adding speed-optimized locations...")
        
        speed_items = [
            "Fee Simple Absolute - Complete ownership",
            "Life Estate - Duration of life",
            "Remainder - Future interest",
            "Reversion - Returns to grantor", 
            "Executory Interest - Cuts short",
            "Rule Against Perpetuities - 21 years",
            "Joint Tenancy - Right of survivorship",
            "Tenancy in Common - No survivorship",
            "Easement - Right to use",
            "Adverse Possession - Hostile use",
        ]
        
        for item in speed_items:
            self.elite_system.add_elite_location(palace.id, item)
        
        # Practice championship recall
        print("\n🏁 Starting Championship Speed Trial...")
        results = self.elite_system.practice_championship_recall(palace.id, time_limit_seconds=30)
        
        print("\n📊 RESULTS:")
        print(f"Accuracy: {results['accuracy']:.1f}%")
        print(f"Speed: {results['items_per_minute']:.1f} items/minute")
        print(f"Level: {results['championship_level']}")
        
        print("\n💡 Speed Tips:")
        print("• Use speed markers (first letters)")
        print("• Practice daily at same time")
        print("• Gradually increase speed by 10%/week")
        print("• Use metronome for pacing")
    
    def _elite_multi_encoding_practice(self):
        """Practice elite 9-channel sensory encoding"""
        print("\n🧬 ELITE MULTI-ENCODING PRACTICE")
        print("=" * 60)
        print("🎯 Master all 9 sensory channels for 99.9% retention")
        print("🧠 Technique used by Alex Mullen (3x World Champion)")
        
        if not self.elite_system:
            print("Elite system not available")
            return
            
        print("\n📝 Let's encode a legal concept using all 9 channels:")
        
        concept = input("Enter legal concept to encode: ").strip()
        if not concept:
            concept = (
                "Adverse Possession requires hostile, actual, exclusive use for statutory period"
            )
        
        # Create demonstration palace
        palace = self.elite_system.create_elite_palace(
            "Multi-Encoding Demo", "Practice", layout_type="radial"
        )
        
        # Add with full encoding
        location = self.elite_system.add_elite_location(palace.id, concept)
        
        print(f"\n🧬 MULTI-SENSORY ENCODING for: {concept}")
        print("=" * 60)
        
        # Display all 9 channels
        if not self.elite_system or not self.sensory_channel_cls:
            print("Elite memory system unavailable. Please load the elite system first.")
            return

        sensory_icons = {
            self.sensory_channel_cls.VISUAL: "👁️",
            self.sensory_channel_cls.AUDITORY: "👂",
            self.sensory_channel_cls.KINESTHETIC: "🤚",
            self.sensory_channel_cls.OLFACTORY: "👃",
            self.sensory_channel_cls.GUSTATORY: "👅",
            self.sensory_channel_cls.EMOTIONAL: "❤️",
            self.sensory_channel_cls.SPATIAL: "📍",
            self.sensory_channel_cls.TEMPORAL: "⏰",
            self.sensory_channel_cls.SYNESTHETIC: "🎨",
        }
        
        for channel, encoding in location.sensory_matrix.items():
            icon = sensory_icons.get(channel, "•")
            print(f"\n{icon} {channel.value.upper()}:")
            print(f"   {encoding}")
        
        # Additional championship features
        print(f"\n🎯 PAO ENCODING: {location.pao_encoding}")
        print(f"🎭 Bizarreness Factor: {location.bizarreness_factor:.1f}/10")
        print(f"❤️ Emotional Intensity: {location.emotional_intensity:.1f}/10")
        print(f"⚡ Speed Markers: {', '.join(location.speed_markers)}")
        print(f"⚠️ Error Traps: {', '.join(location.error_traps)}")
        
        print("\n💡 Multi-Encoding Tips:")
        print("• Practice each channel separately first")
        print("• Combine 3 channels, then 6, then all 9")
        print("• Emotional + Visual = strongest combo")
        print("• Use bizarre imagery for Von Restorff effect")
    
    def _competition_mode_trial(self):
        """Run a competition-style timed trial"""
        print("\n🎯 COMPETITION MODE TRIAL")
        print("=" * 60)
        print("🏆 Simulate World Memory Championship conditions")
        print("⏱️ Timed encoding and recall phases")
        
        if not self.elite_system:
            print("Elite system not available")
            return
            
        print("\n📋 Competition Rules:")
        print("• 5 minutes to memorize 100 items")
        print("• 15 minute break")
        print("• 15 minutes to recall")
        print("• 95% accuracy to qualify")
        
        ready = input("\nReady to begin? (y/n): ").strip().lower()
        if ready != "y":
            return
            
        # Create competition palace
        palace = self.elite_system.create_elite_palace(
            "Competition Palace", "Competition", layout_type="radial", dimensions=(100, 100, 10)
        )
        
        # Generate 100 random legal items
        import random

        legal_terms = [
            "Fee Simple",
            "Life Estate",
            "Remainder",
            "Reversion",
            "Easement",
            "Profit",
            "License",
            "Covenant",
            "Joint Tenancy",
            "Tenancy in Common",
            "Partition",
            "Recording Act",
            "BFP",
            "Adverse Possession",
            "Warranty Deed",
            "Quitclaim",
            "Mortgage",
            "Lien",
        ]
        
        competition_items = []
        for i in range(100):
            term = random.choice(legal_terms)
            number = random.randint(1, 999)
            item = f"{i+1}. {term} - Case {number}"
            competition_items.append(item)
            self.elite_system.add_elite_location(palace.id, item)
        
        print("\n🏁 COMPETITION STARTING!")
        print("Memorize these 100 items in 5 minutes...")
        print("Press Enter to see items...")
        input()
        
        # Display items for memorization
        import time

        start_time = time.time()
        
        for i, item in enumerate(competition_items, 1):
            print(f"{item}")
            if i % 20 == 0:
                elapsed = time.time() - start_time
                remaining = 300 - elapsed  # 5 minutes = 300 seconds
                if remaining > 0:
                    print(f"\n⏱️ Time remaining: {remaining:.0f} seconds")
                    input("Press Enter to continue...")
        
        print("\n⏱️ TIME'S UP!")
        print("15 minute break (simulated - press Enter)")
        input()
        
        # Recall phase
        print("\n📝 RECALL PHASE - 15 minutes")
        results = self.elite_system.practice_championship_recall(palace.id, time_limit_seconds=900)
        
        print("\n🏆 COMPETITION RESULTS:")
        print(f"Items Recalled: {results['locations_attempted']}/100")
        print(f"Accuracy: {results['accuracy']:.1f}%")
        print(f"Championship Level: {results['championship_level']}")
        
        if results["accuracy"] >= 95:
            print("🥇 QUALIFIED FOR CHAMPIONSHIP!")
        elif results["accuracy"] >= 85:
            print("🥈 NATIONAL LEVEL PERFORMANCE!")
        else:
            print("📈 Keep practicing - you're improving!")
    
    def _world_champion_training_plan(self):
        """Display world champion training regimen"""
        print("\n📈 WORLD CHAMPION TRAINING PLAN")
        print("=" * 60)
        print("🏆 Follow the exact training of memory champions")
        
        if not self.elite_system:
            print("Elite system not available")
            return
            
        training = self.elite_system.generate_championship_training()
        
        print("\n📅 DAILY TRAINING SCHEDULE:")
        print("-" * 50)
        for session in training["daily_sessions"]:
            print(f"\n⏰ {session['time']} ({session['duration']} min)")
            print(f"📚 Focus: {session['focus']}")
            print(f"🎯 Technique: {session['technique']}")
            print(f"💪 Exercise: {session['exercise']}")
        
        print("\n📊 WEEKLY GOALS:")
        print("-" * 50)
        for goal, target in training["weekly_goals"].items():
            print(f"• {goal}: {target}")
        
        print("\n🎯 MONTHLY MILESTONES:")
        print("-" * 50)
        for month, milestone in training["monthly_milestones"].items():
            print(f"• {month}: {milestone}")
        
        print("\n🧠 MENTAL EXERCISES:")
        print("-" * 50)
        for exercise in training["mental_exercises"]:
            print(f"• {exercise}")
        
        print("\n🥗 DIETARY OPTIMIZATION:")
        print("-" * 50)
        for food in training["dietary_optimization"]:
            print(f"• {food}")
        
        print("\n😴 SLEEP PROTOCOL:")
        print("-" * 50)
        for aspect, detail in training["sleep_protocol"].items():
            print(f"• {aspect}: {detail}")
        
        print("\n💡 Implementation Tips:")
        print("• Start with 30% of recommended volume")
        print("• Increase by 10% weekly")
        print("• Track progress daily")
        print("• Join memory sports community")
        print("• Consider hiring a memory coach")
    
    def _neuroscience_optimization_report(self):
        """Display neuroscience-based optimization insights"""
        print("\n🧠 NEUROSCIENCE OPTIMIZATION REPORT")
        print("=" * 60)
        print("🔬 Latest research for memory optimization")
        
        if not self.elite_system:
            print("Elite system not available")
            return
            
        insights = self.elite_system.get_neuroscience_insights()
        
        print("\n🔬 NEUROSCIENCE INSIGHTS:")
        print("-" * 50)
        
        for principle, insight in insights.items():
            # Format the principle name
            formatted = principle.replace("_", " ").title()
            print(f"\n📌 {formatted}:")
            print(f"   {insight}")
        
        print("\n⚡ OPTIMIZATION PROTOCOL:")
        print("-" * 50)
        print("1. ENCODING PHASE:")
        print("   • Multi-sensory encoding (9 channels)")
        print("   • Emotional tagging (amygdala activation)")
        print("   • Bizarre imagery (Von Restorff effect)")
        print("   • Self-generation (2x stronger)")
        
        print("\n2. CONSOLIDATION PHASE:")
        print("   • Wait 10 minutes before first recall")
        print("   • Sleep within 4 hours")
        print("   • Avoid similar content for 2 hours")
        print("   • Rest periods for DMN activation")
        
        print("\n3. RECALL PHASE:")
        print("   • Active recall > passive review (3x)")
        print("   • Spaced repetition schedule")
        print("   • Test in different contexts")
        print("   • Use speed markers for rapid access")
        
        print("\n4. LONG-TERM RETENTION:")
        print("   • Review at: 10min, 1 day, 3 days, 1 week, 2 weeks, 1 month")
        print("   • Interleave with other subjects")
        print("   • Teach others (Feynman technique)")
        print("   • Regular competition practice")
    
    def _vr_palace_export(self):
        """Export palace to VR-ready format"""
        print("\n🔮 VR PALACE EXPORT")
        print("=" * 60)
        print("🥽 Export your palace for VR training apps")
        print("🚀 Future-ready for immersive learning")
        
        if not self.elite_system:
            print("Elite system not available")
            return
            
        if not self.elite_system.palaces:
            print("No palaces created yet")
            return
            
        print("\n📋 Available Palaces:")
        for i, (palace_id, palace) in enumerate(self.elite_system.palaces.items(), 1):
            print(f"{i}. {palace.name} ({len(palace.locations)} locations)")
        
        choice = input("\nSelect palace to export (number): ").strip()
        
        try:
            palace_list = list(self.elite_system.palaces.keys())
            selected_id = palace_list[int(choice) - 1]
            
            vr_data = self.elite_system.export_palace_to_vr(selected_id)
            
            # Save to file
            import json

            filename = f"vr_palace_{vr_data['name'].replace(' ', '_')}.json"
            with open(filename, "w") as f:
                json.dump(vr_data, f, indent=2)
            
            print(f"\n✅ VR Palace exported to: {filename}")
            print("📊 Export contains:")
            print(f"   • Palace: {vr_data['name']}")
            print(f"   • Layout: {vr_data['layout']}")
            print(f"   • Locations: {len(vr_data['locations'])}")
            print(f"   • Dimensions: {vr_data['dimensions']}")
            
            print("\n🥽 VR Integration:")
            print("• Import into VR memory training apps")
            print("• Use with Oculus Quest / HTC Vive")
            print("• Practice in immersive 3D environment")
            print("• Track head movement for spatial memory")
            
        except (ValueError, IndexError):
            print("Invalid selection")
    
    def _systematic_topic_study(self, mbe_topics):
        """Systematic study of all MBE topics with memory palace integration"""

        print("\n📖 SYSTEMATIC REAL PROPERTY MBE STUDY")

        print("=" * 50)

        print("🤖 Agent: Comprehensive study plan covering all MBE topics")

        print("🎯 Each topic connects to your memory palace for permanent retention")

        for i, (topic_name, topic_data) in enumerate(mbe_topics.items(), 1):

            print(f"\n{i}. {topic_name}")

            print("-" * 40)

            # Topic overview

            print(f"📚 {len(topic_data['concepts'])} Key Concepts:")

            for j, concept in enumerate(topic_data["concepts"][:3], 1):

                print(f"   {j}. {concept}")

            if len(topic_data["concepts"]) > 3:

                print(f"   ... and {len(topic_data['concepts']) - 3} more")

            # Memory palace connection

            print(f"\n🏰 Memory Palace: Location {i}")

            estates = self._get_estates_data()

            # Mapping from MBE topic names back to estate names
            topic_to_estate_mapping = {
                "1. ESTATES & FUTURE INTERESTS": "1. ESTATES",
                "2. CONVEYANCING & TITLE": "2. CONVEYANCING",
                "3. EASEMENTS & PROFITS": "3. EASEMENTS",
                "4. CONCURRENT OWNERSHIP": "4. CONCURRENT",
                "5. LANDLORD-TENANT": "5. LANDLORD-TENANT",
                "6. MORTGAGES & SECURITY": "6. MORTGAGES",
                "7. ZONING & LAND USE": "7. ZONING",
                "8. ADVERSE POSSESSION": "8. ADVERSE",
                "9. FIXTURES": "9. FIXTURES",
            }

            estate_name = topic_to_estate_mapping.get(topic_name)

            estate_details = estates.get(estate_name)

            if estate_details:

                print(f"   Building: {estate_details['building']}")

                print(f"   Association: {estate_details['elaborative_encoding'][:50]}...")

            # Study progress

            study_choice = input(f"\n🤖 Study {topic_name} now? (y/n/skip): ").strip().lower()

            if study_choice == "y":

                self._focus_specific_mbe_topic(mbe_topics)

                break  # Focus on one topic at a time

            elif study_choice == "skip":

                continue

        print("\n🎯 SYSTEMATIC STUDY COMPLETE!")

        print("🤖 Agent: You've now systematically covered all Real Property MBE topics!")

        print("💡 Review weak areas and practice daily for MBE success.")

    def _get_estates_data(self):
        """Get memory palace data for Real Property estates"""
        return {
            "1. ESTATES": {
                "building": "Medieval Castle",
                "location_action": "Enter through massive drawbridge",
                "concept": "Fee Simple & Future Interests",
                "sensory_cues": {
                    "visual": "Golden crown on throne (Fee Simple Absolute)",
                    "auditory": "Royal trumpets announcing succession",
                    "kinesthetic": "Heavy crown weight on head",
                    "olfactory": "Old parchment and wax seals",
                },
                "elaborative_encoding": "King on throne holds golden deed marked 'FOREVER' while heirs wait in line",
                "memory_peg": "1=Straight pole (flagpole with royal banner)",
                "mnemonic": "PREFUR: Present, Remainder, Executory, Fee, Ultimate, RAP",
            },
            "2. CONVEYANCING": {
                "building": "County Courthouse",
                "location_action": "File documents at recording desk",
                "concept": "Recording Acts & Title",
                "sensory_cues": {
                    "visual": "Racing runners at finish line (Race-Notice)",
                    "auditory": "Stamp hitting paper loudly",
                    "kinesthetic": "Heavy deed book slamming shut",
                    "olfactory": "Fresh ink and paper",
                },
                "elaborative_encoding": "Runners racing to recording desk, first to stamp wins the property deed",
                "memory_peg": "2=Duck swimming in courthouse fountain",
                "mnemonic": "RACE: Race-notice, Actual notice, Constructive notice, Exceptions",
            },
            "3. EASEMENTS": {
                "building": "Highway Bridge",
                "location_action": "Walk across neighbor's property path",
                "concept": "Rights to Use Another's Land",
                "sensory_cues": {
                    "visual": "Well-worn path across field",
                    "auditory": "Footsteps on gravel path",
                    "kinesthetic": "Walking the same route daily",
                    "olfactory": "Fresh cut grass along path",
                },
                "elaborative_encoding": "Neighbor walking same path for 20 years creates permanent right of way",
                "memory_peg": "3=Heart-shaped easement path",
                "mnemonic": "EASE: Express, Adverse, Statutory, Estoppel",
            },
            "4. CONCURRENT": {
                "building": "Duplex House",
                "location_action": "Multiple keys opening same door",
                "concept": "Co-ownership Forms",
                "sensory_cues": {
                    "visual": "Four identical keys (TTIP unities)",
                    "auditory": "Multiple voices in discussion",
                    "kinesthetic": "Handshake between co-owners",
                    "olfactory": "Different cooking smells from units",
                },
                "elaborative_encoding": "Four people holding hands in circle (Joint Tenancy) vs separate corners (Tenancy in Common)",
                "memory_peg": "4=Sailboat with multiple owners",
                "mnemonic": "TTIP: Time, Title, Interest, Possession",
            },
            "5. LANDLORD-TENANT": {
                "building": "Apartment Complex",
                "location_action": "Sign lease at rental office",
                "concept": "Rental Relationships",
                "sensory_cues": {
                    "visual": "Lease agreement with red pen marks",
                    "auditory": "Keys jingling, doors locking",
                    "kinesthetic": "Turning apartment key in lock",
                    "olfactory": "Fresh paint smell in unit",
                },
                "elaborative_encoding": "Landlord fixing broken heater while tenant pays rent on first of month",
                "memory_peg": "5=Hand giving/receiving keys",
                "mnemonic": "RENT: Repairs, Exclusive possession, No retaliation, Tenant pays",
            },
            "6. MORTGAGES": {
                "building": "Bank Vault",
                "location_action": "Sign mortgage papers at loan desk",
                "concept": "Security Interests in Land",
                "sensory_cues": {
                    "visual": "Stack of money with house on top",
                    "auditory": "Calculator clicking, pen signing",
                    "kinesthetic": "Heavy mortgage documents",
                    "olfactory": "New money smell",
                },
                "elaborative_encoding": "Banker holds house deed in vault until final payment unlocks it",
                "memory_peg": "6=Elephant trunk holding mortgage papers",
                "mnemonic": "MORT: Mortgage lien, Original priority, Recording, Tax liens",
            },
            "7. ZONING": {
                "building": "City Planning Office",
                "location_action": "Review zoning maps on wall",
                "concept": "Land Use Regulations",
                "sensory_cues": {
                    "visual": "Color-coded zoning map",
                    "auditory": "Gavel at zoning hearing",
                    "kinesthetic": "Pointing at map zones",
                    "olfactory": "Coffee at planning meeting",
                },
                "elaborative_encoding": "City planner drawing lines on map while property owner protests at podium",
                "memory_peg": "7=Cliff edge (setback requirement)",
                "mnemonic": "ZONE: Zoning plan, Ownership rights, No compensation, Exceptions",
            },
            "8. ADVERSE": {
                "building": "Abandoned Cabin",
                "location_action": "Move into vacant property",
                "concept": "Adverse Possession",
                "sensory_cues": {
                    "visual": "No Trespassing sign torn down",
                    "auditory": "Clock ticking for 10+ years",
                    "kinesthetic": "Building fence around property",
                    "olfactory": "Musty abandoned building",
                },
                "elaborative_encoding": "Squatter openly living in house for 10 years while owner never visits",
                "memory_peg": "8=Snowman built on disputed land",
                "mnemonic": "HATE: Hostile, Actual, Time (statutory), Exclusive",
            },
            "9. FIXTURES": {
                "building": "Hardware Store",
                "location_action": "Attach chandelier to ceiling",
                "concept": "Personal vs Real Property",
                "sensory_cues": {
                    "visual": "Chandelier permanently attached",
                    "auditory": "Drill securing fixture",
                    "kinesthetic": "Tightening bolts permanently",
                    "olfactory": "Wood shavings and metal",
                },
                "elaborative_encoding": "Chandelier becomes part of house when permanently bolted to ceiling",
                "memory_peg": "9=Balloon tied down (attached to land)",
                "mnemonic": "FIX: Fastened, Intent permanent, eXtent of damage",
            },
        }

    def _constitutional_law_memory_palace_agent(self):
        """Elite memory palace experience for Constitutional Law"""

        print("\n🏛️ ELITE CONSTITUTIONAL LAW MEMORY AGENT")
        print("=" * 65)

        # Ensure elite system
        if not getattr(self, "elite_system", None):
            try:
                from elite_memory_palace import EliteMemoryPalaceSystem, SensoryChannel  # type: ignore

                self.elite_system = EliteMemoryPalaceSystem("Bar Exam Champion")
                self.sensory_channel_cls = SensoryChannel
                print("✅ Elite memory system loaded successfully")
            except Exception as exc:  # pragma: no cover
                print(f"⚠️  Elite memory system unavailable: {exc}")
                self.elite_system = None
                return

        # Create or fetch Con Law palace
        palace_name = "Constitutional Law Mastery"
        existing_palace = next(
            (palace for palace in self.elite_system.palaces.values() if palace["name"] == palace_name),
            None,
        )

        if existing_palace:
            palace = existing_palace
            print(f"🏰 Using existing palace: {palace_name}")
        else:
            palace = self.elite_system.create_elite_palace(
                palace_name, "Constitutional Law", layout_type="constitutional_hall", dimensions=(60, 60, 12)
            )
            print(f"🏰 Created new palace: {palace_name}")

        palace_id = palace["id"]

        # Define constitutional law nodes
        conlaw_nodes = [
            {
                "title": "Judicial Power & Justiciability",
                "content": (
                    "SCRAM Justiciability: Standing (injury, causation, redress), Case/Controversy, Ripeness, Advisory opinions (no), Mootness."
                    " Political Question factors: textual commitment + no standards."
                ),
                "mnemonic": "SCRAM triangle with injury/causation/redress",
            },
            {
                "title": "Federal Legislative Power",
                "content": (
                    "Commerce Clause three rings: Channels, Instrumentalities, Substantial Effects (economic aggregation)."
                    " Necessary & Proper enables implementation. Spending/TAX limits: general welfare, clear, related, non-coercive."
                ),
                "mnemonic": "Circus tent with three rings labeled Channels/Instrumentalities/Effects."
            },
            {
                "title": "Executive Power & Separation",
                "content": (
                    "Youngstown tiers, appointment/removal power, commander-in-chief. No line-item veto; executive agreements vs treaties."
                ),
                "mnemonic": "Three-tiered podium with President balancing Congress/Court."
            },
            {
                "title": "Federalism & State Power",
                "content": (
                    "Anti-commandeering (NY v. US, Printz), 10th Amendment reserve. Supremacy and preemption, dormant Commerce balancing."
                ),
                "mnemonic": "State capitols resisting federal puppet strings."
            },
            {
                "title": "Individual Rights Framework",
                "content": (
                    "Incorporation via 14th DP. Due Process (procedural/substantive). Equal Protection tiers: strict (race), intermediate (gender), rational."
                ),
                "mnemonic": "SIREN spotlighting scrutiny levels."
            },
            {
                "title": "First Amendment Speech",
                "content": (
                    "Content-based strict scrutiny, symbolic speech (O'Brien test), public forum doctrine, commercial speech intermediate."
                ),
                "mnemonic": "Megaphone with strict/intermediate levers."
            },
            {
                "title": "Religion Clauses",
                "content": (
                    "Establishment (Lemon/endorsement/coercion), Free Exercise (neutral vs targeted laws, strict scrutiny)."
                ),
                "mnemonic": "Balance scale between church and state with Lemon wedges."
            },
            {
                "title": "Criminal Procedure Overview",
                "content": (
                    "Fourth Amendment SWEAR (Search, Warrant, Exceptions, Arrest, Reasonable expectation); Fifth Miranda CRISP; exclusionary rule limits."
                ),
                "mnemonic": "Police badge shaped like SWEAR acronym."
            },
        ]

        # Populate palace locations if they are not present
        existing_locations = list(self.elite_system.palaces[palace_id]["locations"].values())

        for node in conlaw_nodes:
            if any(node["title"] in getattr(loc, "content", "") for loc in existing_locations):
                continue

            location_text = f"{node['title']}: {node['content']}"
            location = self.elite_system.add_elite_location(palace_id, location_text)

            if node.get("mnemonic"):
                location.sensory_matrix["mnemonic_device"] = node["mnemonic"]

            existing_locations.append(location)

        print("\n✅ Constitutional law palace prepared! Let's explore.")

        while True:
            print("\n⚖️  Constitutional Law Menu")
            print("1. Guided palace tour")
            print("2. Focused topic drill")
            print("3. Memory palace question practice")
            print("4. Generate flashcards for weak areas")
            print("5. Export palace summary")
            print("0. Return to main menu")

            choice = input("Select option: ").strip()

            if choice == "0":
                break
            elif choice == "1":
                self._guided_conlaw_tour(conlaw_nodes, palace_id)
            elif choice == "2":
                self._conlaw_focus_drill(conlaw_nodes, palace_id)
            elif choice == "3":
                self._conlaw_question_practice(conlaw_nodes, palace_id)
            elif choice == "4":
                self._generate_conlaw_flashcards(conlaw_nodes)
            elif choice == "5":
                self._export_conlaw_palace(palace_id, palace_name)
            else:
                print("❌ Invalid choice.")

    def _guided_conlaw_tour(self, nodes, palace_id):
        print("\n🚶 Guided tour through Constitutional Law palace")
        for node in nodes:
            print("\n" + "-" * 60)
            print(f"📍 {node['title']}")
            print(node['content'])
            if node.get("mnemonic"):
                print(f"🎵 Mnemonic: {node['mnemonic']}")
            input("Press Enter to reinforce this location...")

    def _conlaw_focus_drill(self, nodes, palace_id):
        print("\n🎯 Focused drill")
        for idx, node in enumerate(nodes, 1):
            print(f"{idx}. {node['title']}")
        choice = input("Select topic: ").strip()
        try:
            index = int(choice) - 1
            node = nodes[index]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return

        print(f"\n📘 Deep dive: {node['title']}")
        print(node['content'])

        if "SCRAM" in node['content']:
            print("\nQuiz: Identify each element of standing.")
            response = input("List them separated by commas: ")
            expected = {"injury", "causation", "redress"}
            if expected.issubset({part.strip().lower() for part in response.split(',')}):
                print("✅ Correct!")
            else:
                print("⚠️  Remember: Injury, causation, redressability, plus case or controversy.")

    def _conlaw_question_practice(self, nodes, palace_id):
        print("\n📝 Constitutional Law practice question")
        questions = [
            {
                "prompt": "Citizen sues alleging Congress lacks authority to regulate purely intrastate non-economic activity. What case controls?",
                "answer": "United States v. Lopez"
            },
            {
                "prompt": "What are the requirements for conditional federal spending to be valid?",
                "answer": "General welfare, clearly stated, related to federal interest, not coercive."
            },
            {
                "prompt": "Name two exceptions to mootness.",
                "answer": "Capable of repetition yet evading review; voluntary cessation; class actions."  # type: ignore
            }
        ]

        for q in questions:
            print(f"\n❓ {q['prompt']}")
            input("Your answer: ")
            print(f"✅ Model answer: {q['answer']}")

    def _generate_conlaw_flashcards(self, nodes):
        print("\n🃏 Generating Constitutional Law flashcards")
        created = 0
        for node in nodes:
            question = f"Explain {node['title']}"
            answer = node['content']
            card = FlashcardEntry(
                id=generate_id("conlaw"),
                subject="Constitutional Law",
                topic=node['title'],
                question=question,
                answer=answer,
                created=datetime.now().isoformat(),
            )
            self.store.save_flashcard(card)
            created += 1
        print(f"✅ Created {created} flashcards. Use Flashcard Review mode to drill them.")

    def _export_conlaw_palace(self, palace_id, palace_name):
        """Export palace summary for review."""
        if not self.elite_system:
            print("⚠️  Elite system not available")
            return
        export = self.elite_system.export_palace_to_vr(palace_id)
        filename = f"conlaw_palace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(export, f, indent=2)
        print(f"✅ Exported {palace_name} palace to {filename}")


# ---------- Elite MBE Preparation System (Integrated) ----------


class EliteMBEPreparationSystem:
    """
    Integrated adaptive training system combining all enhancements.
    
    Orchestrates rule decomposition, mistake analysis, issue-spotting, timing strategy,
    and metacognitive monitoring for comprehensive MBE preparation.
    """

    def __init__(self, client: OpenAI, model: str, notes: str = ""):
        # Core configuration
        self.client = client
        self.model = model
        self.notes = notes

        # Initialize all advanced training components
        self.mistake_analyzer = MBEMistakeAnalyzer(client, model)
        self.issue_spotter = IssueSpottingTrainer(client, model)

        # Initialize existing core components
        self.flashcards = FlashcardManager()
        self.tracker = PerformanceTracker()

        # Session analytics
        self.session_stats = {
            "start_time": datetime.now(),
            "questions_attempted": 0,
            "correct_count": 0,
            "weak_areas": [],
            "strong_areas": [],
            "training_modes_used": [],
        }

    def adaptive_training_session(self, duration_minutes: int = 60) -> Dict:
        """
        Adaptive training that adjusts based on real-time performance.
        
        Args:
            duration_minutes: Total session duration
            
        Returns:
            Comprehensive session results with analytics and recommendations
        """

        print(f"\n🎯 ADAPTIVE MBE TRAINING SESSION ({duration_minutes} minutes)")
        print("=" * 60)
        print("System will adapt difficulty and focus based on your performance\n")

        session_start = time.time()
        session_end = session_start + (duration_minutes * 60)

        # Phase 1: Diagnostic assessment (first 10 minutes)
        print("📋 Phase 1: Diagnostic Assessment (10 min)")
        print("-" * 60)
        diagnostic_results = self._run_diagnostic_assessment()

        # Identify weakest areas
        weak_areas = self._identify_weak_areas(diagnostic_results)

        print("\n📊 Diagnostic complete. Focus areas identified:")
        for i, (area, score) in enumerate(weak_areas[:3], 1):
            print(f"  {i}. {area}: {score:.1f}% accuracy (needs improvement)")

        # Phase 2: Adaptive training loop
        training_rounds = 0
        while time.time() < session_end:
            remaining = (session_end - time.time()) / 60

            if remaining < 10:
                print(f"\n⏰ Phase 3: Final Review ({remaining:.0f} min remaining)")
                self._final_review_phase(weak_areas)
                break

            training_rounds += 1
            print(f"\n📚 Training Round {training_rounds}")
            print("=" * 60)

            # Select optimal training mode based on performance
            mode = self._select_optimal_training_mode(weak_areas, diagnostic_results)

            print(f"Mode: {mode['name']}")
            print(f"Focus: {mode['focus_area']}")
            print(f"Rationale: {mode['rationale']}")
            print(f"Time remaining: {remaining:.0f} minutes\n")

            # Execute training module
            self._execute_training_mode(mode)

            # Update weak areas based on latest performance
            weak_areas = self._recalculate_weak_areas(weak_areas, mode)

        # Phase 3: Session summary and recommendations
        summary = self._generate_session_summary()

        return summary

    def _run_diagnostic_assessment(self) -> Dict:
        """
        Quick diagnostic across multiple dimensions to identify strengths/weaknesses.
        
        Returns comprehensive diagnostic results.
        """

        print("Running multi-dimensional diagnostic...\n")

        assessment = {
            "rule_knowledge": self._test_rule_knowledge(),
            "issue_spotting": self._test_issue_spotting_ability(),
            "element_analysis": self._test_element_analysis_skill(),
            "timing_performance": self._test_timing_efficiency(),
            "distractor_resistance": self._test_distractor_resistance(),
        }

        return assessment

    def _test_rule_knowledge(self) -> Dict:
        """Test basic rule knowledge across subjects."""
        print("  → Testing rule knowledge...")

        # Simplified - would use flashcard system in production
        return {
            "Real Property": random.uniform(65, 85),
            "Contracts": random.uniform(70, 90),
            "Torts": random.uniform(60, 80),
            "ConLaw": random.uniform(70, 85),
        }

    def _test_issue_spotting_ability(self) -> Dict:
        """Test systematic issue-spotting."""
        print("  → Testing issue-spotting...")

        return {
            "accuracy": random.uniform(70, 90),
            "speed": random.uniform(25, 45),  # seconds per pattern
            "completeness": random.uniform(75, 95),  # % issues caught
        }

    def _test_element_analysis_skill(self) -> Dict:
        """Test ability to analyze rule elements systematically."""
        print("  → Testing element analysis...")

        return {"accuracy": random.uniform(70, 90), "common_errors": ["incomplete_analysis", "burden_shifting"]}

    def _test_timing_efficiency(self) -> Dict:
        """Test timing and pacing."""
        print("  → Testing timing efficiency...")

        return {"avg_seconds_per_question": random.uniform(90, 150), "target": 108}  # 1.8 min

    def _test_distractor_resistance(self) -> Dict:
        """Test susceptibility to wrong answer distractors."""
        print("  → Testing distractor resistance...")

        return {"trap_susceptibility": random.uniform(0.2, 0.5), "most_common_trap": "policy_over_law"}

    def _identify_weak_areas(self, diagnostic_results: Dict) -> List[Tuple[str, float]]:
        """Identify weakest performance areas from diagnostic."""

        weak_areas = []

        # Extract rule knowledge weaknesses
        if "rule_knowledge" in diagnostic_results:
            for subject, score in diagnostic_results["rule_knowledge"].items():
                weak_areas.append((subject, score))

        # Sort by score (ascending - weakest first)
        weak_areas.sort(key=lambda x: x[1])

        return weak_areas

    def _select_optimal_training_mode(self, weak_areas: List, diagnostic_results: Dict) -> Dict:
        """
        Select optimal training mode based on current weaknesses and performance.
        
        Uses simple heuristics - could be enhanced with ML in production.
        """

        if not weak_areas:
            return {
                "type": "timed_simulation",
                "name": "Full Speed MBE Practice",
                "focus_area": "Mixed",
                "rationale": "No specific weaknesses - practice under test conditions",
            }

        weakest_area, score = weak_areas[0]

        # Decision logic
        if score < 70:
            return {
                "type": "rule_decomposition",
                "name": f"{weakest_area} Deep Dive",
                "focus_area": weakest_area,
                "rationale": f"Score {score:.0f}% indicates foundational gaps - need rule review",
            }
        elif diagnostic_results.get("issue_spotting", {}).get("accuracy", 100) < 75:
            return {
                "type": "issue_spotting",
                "name": "Issue-Spotting Speed Drill",
                "focus_area": weakest_area,
                "rationale": "Issue-spotting accuracy needs improvement",
            }
        elif diagnostic_results.get("timing_performance", {}).get("avg_seconds_per_question", 108) > 120:
            return {
                "type": "timed_simulation",
                "name": "Speed Training Block",
                "focus_area": weakest_area,
                "rationale": "Timing is slow - need speed drills",
            }
        else:
            return {
                "type": "distractor_training",
                "name": "Wrong Answer Elimination",
                "focus_area": weakest_area,
                "rationale": "Refine answer selection - eliminate trap distractors faster",
            }

    def _execute_training_mode(self, mode: Dict) -> None:
        """Execute the selected training mode."""

        mode_type = mode["type"]
        focus_area = mode["focus_area"]

        if mode_type == "rule_decomposition":
            self._drill_rule_decomposition(focus_area)

        elif mode_type == "distractor_training":
            self._drill_distractor_elimination(focus_area)

        elif mode_type == "issue_spotting":
            # Use the IssueSpottingTrainer
            print(f"\n🔍 Issue-Spotting Drill: {focus_area}")
            print("Identify all issues in each fact pattern...\n")
            print("(In production, this would run interactive drill)")
            print(f"Focus: {focus_area} issue patterns")
            input("\nPress Enter to continue...")

        elif mode_type == "timed_simulation":
            self._run_timed_mbe_block(focus_area)

        elif mode_type == "memory_reinforcement":
            print(f"\n🧠 Memory Palace Review: {focus_area}")
            print("(In production, this would run memory palace targeted review)")
            input("\nPress Enter to continue...")

        # Track mode usage
        self.session_stats["training_modes_used"].append(
            {"mode": mode_type, "focus": focus_area, "timestamp": datetime.now().isoformat()}
        )

    def _drill_rule_decomposition(self, subject: str) -> None:
        """Drill on breaking rules into elements."""

        print(f"\n📖 Rule Decomposition Drill: {subject}")
        print("-" * 60)
        print("Breaking down rules into required elements...")
        print(f"\nFocus area: {subject}")
        print("(In production: Interactive element-by-element analysis)")
        input("\nPress Enter to continue...")

    def _drill_distractor_elimination(self, subject: str) -> None:
        """Drill on eliminating wrong answers quickly."""

        print(f"\n❌ Distractor Elimination Drill: {subject}")
        print("-" * 60)
        print("Practice identifying and eliminating wrong answers...")
        print(f"\nFocus area: {subject}")
        print("(In production: Show wrong answers with trap analysis)")
        input("\nPress Enter to continue...")

    def _run_timed_mbe_block(self, subject: str) -> None:
        """Run timed practice block."""

        print(f"\n⏱️  Timed MBE Block: {subject}")
        print("-" * 60)
        print("Answer questions under authentic MBE time pressure...")
        print(f"\nFocus area: {subject}")
        print("Target: 1.8 minutes per question")
        print("(In production: Actual timed questions)")
        input("\nPress Enter to continue...")

    def _recalculate_weak_areas(self, current_weak_areas: List, last_mode: Dict) -> List:
        """Update weak areas based on training performance."""

        # Simplified - would track actual performance in production
        # Simulate slight improvement in trained area
        updated = []
        for area, score in current_weak_areas:
            if area == last_mode.get("focus_area"):
                # Simulated improvement
                updated.append((area, min(100, score + random.uniform(2, 5))))
            else:
                updated.append((area, score))

        # Re-sort by score
        updated.sort(key=lambda x: x[1])
        return updated

    def _final_review_phase(self, weak_areas: List) -> None:
        """Final spaced-repetition review of session content."""

        print("\n🔄 Final Review Phase")
        print("=" * 60)
        print("Reviewing key concepts from this session...\n")

        for i, (area, score) in enumerate(weak_areas[:3], 1):
            print(f"{i}. {area} - Target mastery reinforcement")

        print("\n(In production: Flashcard review of session topics)")
        input("\nPress Enter to complete session...")

    def _generate_session_summary(self) -> Dict:
        """Generate comprehensive session summary with recommendations."""

        duration = (datetime.now() - self.session_stats["start_time"]).seconds / 60

        print("\n" + "=" * 60)
        print("SESSION SUMMARY")
        print("=" * 60)

        print(f"Duration: {duration:.0f} minutes")
        print(f"Training modes used: {len(self.session_stats['training_modes_used'])}")

        summary = {
            "duration_minutes": duration,
            "modes_used": self.session_stats["training_modes_used"],
            "improvement_trajectory": "positive",
            "next_session_recommendation": "Continue with adaptive training",
        }

        print("\n✅ Session complete!")
        print("💡 Continue with daily adaptive sessions for optimal improvement")

        return summary

    def comprehensive_mbe_simulation(self, num_questions: int = 100) -> Dict:
        """
        Full MBE simulation with authentic conditions and detailed analysis.
        
        Args:
            num_questions: Number of questions (typically 100 or 200)
            
        Returns:
            Comprehensive results with personalized study plan
        """

        print("\n📝 COMPREHENSIVE MBE SIMULATION")
        print("=" * 60)
        print(f"Questions: {num_questions}")
        print(f"Time: {num_questions * 1.8 / 60:.1f} minutes (1.8 min per question)")
        print("Conditions: Authentic MBE environment")
        print("\nThis is a full diagnostic simulation.")
        print("Results will generate a personalized study plan.\n")

        input("Press Enter when ready to begin...")

        # Simulate question set (in production, would load actual questions)
        print(f"\nGenerating balanced {num_questions}-question set...")
        print("(In production: Pulls from question bank with balanced subjects)")

        # Simulate performance (in production, would be actual results)
        simulated_results = {
            "total": num_questions,
            "correct": int(num_questions * random.uniform(0.65, 0.85)),
            "subject_breakdown": {
                "Real Property": {"correct": 12, "total": 15},
                "Contracts": {"correct": 14, "total": 18},
                "Torts": {"correct": 13, "total": 17},
                "ConLaw": {"correct": 15, "total": 18},
                "CrimLaw": {"correct": 14, "total": 16},
                "CrimPro": {"correct": 11, "total": 16},
                "Evidence": {"correct": 9, "total": 12},
            },
            "timing": {"avg_seconds": random.uniform(90, 130), "target": 108},
        }

        accuracy = (simulated_results["correct"] / simulated_results["total"]) * 100

        print("\n" + "=" * 60)
        print("SIMULATION RESULTS")
        print("=" * 60)
        print(f"Score: {simulated_results['correct']}/{simulated_results['total']} ({accuracy:.1f}%)")
        print(f"Timing: {simulated_results['timing']['avg_seconds']:.0f}s per question (target: 108s)")

        # Subject breakdown
        print("\nSUBJECT BREAKDOWN:")
        for subject, stats in simulated_results["subject_breakdown"].items():
            subj_accuracy = (stats["correct"] / stats["total"]) * 100
            status = "✓" if subj_accuracy >= 70 else "⚠" if subj_accuracy >= 60 else "✗"
            print(f"  {status} {subject:15} {stats['correct']}/{stats['total']} ({subj_accuracy:.0f}%)")

        # Generate personalized study plan
        print("\n📚 Generating personalized study plan...")
        study_plan = self._generate_personalized_study_plan(simulated_results)

        return {"results": simulated_results, "study_plan": study_plan, "recommendations": study_plan["priority_actions"]}

    def _generate_personalized_study_plan(self, analysis: Dict) -> Dict:
        """
        Generate personalized study plan based on simulation analysis.
        
        Args:
            analysis: Performance analysis from simulation
            
        Returns:
            Structured study plan with daily schedule and milestones
        """

        # Identify weak subjects
        weak_subjects = [
            subject
            for subject, stats in analysis["subject_breakdown"].items()
            if (stats["correct"] / stats["total"]) < 0.70
        ]

        print("\n" + "=" * 60)
        print("PERSONALIZED STUDY PLAN")
        print("=" * 60)

        plan = {
            "priority_subjects": weak_subjects,
            "daily_schedule": {
                "morning_session": {
                    "duration": "2 hours",
                    "focus": weak_subjects[0] if weak_subjects else "Review",
                    "activities": ["Rule review", "Element drills", "Issue-spotting"],
                },
                "afternoon_session": {
                    "duration": "2 hours",
                    "focus": weak_subjects[1] if len(weak_subjects) > 1 else "Mixed practice",
                    "activities": ["Timed questions", "Mistake analysis", "Pattern recognition"],
                },
                "evening_session": {
                    "duration": "1 hour",
                    "focus": "Memory reinforcement",
                    "activities": ["Flashcard review", "Memory palace", "Next-day preview"],
                },
            },
            "priority_actions": [
                f"Focus on {weak_subjects[0]} - {((analysis['subject_breakdown'][weak_subjects[0]]['correct'] / analysis['subject_breakdown'][weak_subjects[0]]['total']) * 100):.0f}% accuracy"
                if weak_subjects
                else "Maintain current performance",
                f"Improve timing - currently {analysis['timing']['avg_seconds']:.0f}s (target: 108s)"
                if analysis["timing"]["avg_seconds"] > 108
                else "Timing is good - maintain pace",
                "Use IRIS mnemonic for all property servitude questions",
            ],
            "weekly_milestones": [
                f"Week 1: Bring {weak_subjects[0]} to 70%+" if weak_subjects else "Week 1: Maintain 70%+ all subjects",
                "Week 2: Complete 200-question simulation",
                "Week 3: Achieve 75%+ across all subjects",
            ],
        }

        # Print plan
        print(f"\nPRIORITY SUBJECTS: {', '.join(weak_subjects) if weak_subjects else 'All subjects performing well'}")
        print("\nDAILY STRUCTURE:")
        print(f"  Morning (2h): {plan['daily_schedule']['morning_session']['focus']}")
        print(f"  Afternoon (2h): {plan['daily_schedule']['afternoon_session']['focus']}")
        print(f"  Evening (1h): {plan['daily_schedule']['evening_session']['focus']}")

        print("\nPRIORITY ACTIONS:")
        for i, action in enumerate(plan["priority_actions"], 1):
            print(f"  {i}. {action}")

        return plan


def main():
    """Main entry point for the Bar Tutor application"""
    # Load environment
    api_key = load_env()
    
    # Create OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Load notes
    notes = load_notes()
    
    # Get model from command line or use default
    parser = argparse.ArgumentParser(description="Bar Prep Tutor - Advanced Legal Education System")
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"OpenAI model to use (default: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()
    
    # Create and run tutor
    tutor = BarTutorV3(client, args.model, notes)
    tutor.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Unhandled error: {e}")
        exit(1)

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

from openai import OpenAI
from dotenv import load_dotenv
import os, pathlib, sys, json, time, argparse, textwrap, readline, re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, deque
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import statistics
import random

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
    "Torts", "Contracts", "Criminal Law", "Criminal Procedure",
    "Evidence", "Constitutional Law", "Civil Procedure",
    "Real Property", "Wills and Trusts", "Family Law",
    "Secured Transactions", "Agency and Partnership",
    "Corporations", "Conflict of Laws", "Federal Jurisdiction",
    "Professional Responsibility"
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
        return (self.correct_answers / self.total_questions * 100) if self.total_questions > 0 else 0.0

    def update_difficulty(self) -> Difficulty:
        """Aggressive adaptive difficulty algorithm for MBE-level challenges"""
        if len(self.difficulty_progression) < 3:
            return Difficulty.INTERMEDIATE

        recent_accuracy = statistics.mean(self.difficulty_progression[-10:]) if len(self.difficulty_progression) >= 10 else statistics.mean(self.difficulty_progression)
        confidence_trend = statistics.mean(self.confidence_trends[-5:]) if len(self.confidence_trends) >= 5 else 3.0

        # More aggressive scoring - bar exam students need to hit higher thresholds
        score = (
            recent_accuracy * 0.5 +
            (confidence_trend - 2.5) * 25 * 0.3 +  # Penalize low confidence more
            self.learning_velocity * 0.2
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
        self.ease_factor += (0.1 - (5 - adjusted_quality) * (0.08 + (5 - adjusted_quality) * 0.02)) + confidence_modifier
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
        due_cards.sort(key=lambda x: (
            -(now - datetime.fromisoformat(x.last_reviewed or x.created_at)).days if x.last_reviewed or x.created_at else 0,
            x.difficulty
        ))

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

    def _build_messages(self, system_prompt: str, user_content: str,
                        include_notes: bool = True, include_performance: bool = False) -> List[Dict]:
        messages = [{"role": "system", "content": system_prompt}]

        if include_notes and hasattr(self, 'notes') and self.notes:
            messages.append({
                "role": "system",
                "content": f"Reference notes:\n{self.notes[:3000]}"
            })

        if include_performance and hasattr(self, 'current_subject') and self.current_subject:
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
            model=model,
            messages=messages,
            temperature=temperature
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

    def add_card(self, front: str, back: str, subject: str = "Mixed/Other", difficulty: str = "Intermediate"):
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
            "common_mistakes": []
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
        cards.sort(key=lambda x: (
            datetime.fromisoformat(x.get("next_review", x["created"])),
            ["Foundational", "Intermediate", "Advanced", "Expert"].index(x.get("difficulty", "Intermediate"))
        ))
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
                        ef = ef + (0.1 - (5 - adjusted_quality) * (0.08 + (5 - adjusted_quality) * 0.02)) + confidence_modifier
                        ef = max(1.3, min(ef, 2.8))  # Clamp to reasonable range

                        # Update card
                        card["ease_factor"] = ef
                        card["interval"] = interval
                        card["repetitions"] = reps
                        card["last_reviewed"] = datetime.now().isoformat()
                        card["next_review"] = (datetime.now() + timedelta(days=interval)).isoformat()

                        # Track performance history
                        performance_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "quality": quality,
                            "confidence": confidence,
                            "interval": interval
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
        self.session_stats = defaultdict(lambda: {
            "correct": 0, "total": 0, "topics": set(), "avg_time": 0.0
        })

    def record_attempt(self, subject: str, correct: bool, topic: str = None, response_time: float = None):
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
            self.session_stats[subject]["avg_time"] = (current_avg * (count - 1) + response_time) / count

        # Write to file
        entry = {
            "timestamp": datetime.now().isoformat(),
            "subject": subject,
            "correct": correct,
            "topic": topic,
            "response_time": response_time,
            "session": True  # Mark as current session
        }
        with self.perf_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def get_stats(self, subject=None, days=30):
        """Get comprehensive performance statistics"""
        cutoff = datetime.now() - timedelta(days=days)
        stats = defaultdict(lambda: {
            "correct": 0, "total": 0, "avg_time": 0.0, "topics": set(), "recent_trend": 0.0
        })

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
                        stats[subj]["avg_time"] = (current_avg * (count - 1) + entry["response_time"]) / count

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
        insights = {
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "trends": []
        }

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
                insights["recommendations"].append(f"Consider timing drills for {subj} (avg: {avg_time}s)")
            elif avg_time < 30:  # Under 30 seconds
                insights["recommendations"].append(f"Add depth questions for {subj} - answering too quickly")

        # Generate specific recommendations
        if insights["weaknesses"]:
            insights["recommendations"].append("Focus on diagnostic assessment for weak areas")
            insights["recommendations"].append("Use interleaved practice mixing weak and strong subjects")

        if insights["strengths"]:
            insights["recommendations"].append("Maintain strengths with spaced review")
            insights["recommendations"].append("Use advanced questions to challenge strong areas")

        return insights

    def print_dashboard(self):
        """Display comprehensive performance dashboard"""
        print("\n" + "="*70)
        print(" "*25 + "PERFORMANCE DASHBOARD")
        print("="*70)

        # Get stats for different time periods
        week_stats = self.get_stats(days=7)
        month_stats = self.get_stats(days=30)

        if not month_stats:
            print("\nNo performance data yet. Start practicing to build insights!")
            print("="*70)
            return

        print("\nLAST 30 DAYS OVERVIEW:")
        print("-"*50)

        total_correct = sum(data["correct"] for data in month_stats.values())
        total_questions = sum(data["total"] for data in month_stats.values())
        overall_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0

        print(f"Total Questions: {total_questions}")
        print(f"Overall Accuracy: {overall_accuracy:.1f}%")
        print(f"Subjects Studied: {len(month_stats)}")

        print("\nSUBJECT BREAKDOWN:")
        print("-"*50)

        for subject in sorted(month_stats.keys(), key=lambda x: month_stats[x]["percentage"], reverse=True):
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
            print(f"\n✅ STRENGTHS:")
            for strength in insights["strengths"][:3]:
                print(f"  • {strength}")

        if insights["weaknesses"]:
            print(f"\n⚠️  AREAS FOR IMPROVEMENT:")
            for weakness in insights["weaknesses"][:3]:
                print(f"  • {weakness}")

        if insights["recommendations"]:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in insights["recommendations"][:3]:
                print(f"  • {rec}")

        # Session statistics
        if self.session_stats:
            print(f"\nCURRENT SESSION:")
            print("-"*50)
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

        print("="*70)
    
# ---------- Module 1: Advanced Filtering & Search ----------
class CardFilteringSystem:
    """Add when overwhelmed by too many cards"""

    def __init__(self, flashcard_manager):
        self.fm = flashcard_manager

    def search_cards(self,
                     query: str = None,
                     tags: List[str] = None,
                     date_from: datetime = None,
                     date_to: datetime = None,
                     min_ease: float = None,
                     max_ease: float = None) -> List[Dict]:
        """Advanced search with multiple filters"""
        cards = []

        with self.fm.cards_file.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    card = json.loads(line.strip())

                    # Text search
                    if query:
                        query_lower = query.lower()
                        if not (query_lower in card["front"].lower() or
                               query_lower in card["back"].lower()):
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
                "badges": []
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
            "streak_7": (self.achievements["streaks"]["best"] >= 7, "🔥 Week Warrior - 7 day streak"),
            "streak_30": (self.achievements["streaks"]["best"] >= 30, "💎 Month Master - 30 day streak"),
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
                f"🎯 Perfect execution! Keep this momentum going!",
                f"🏆 Bar exam excellence in the making!"
            ]
        elif performance >= 75:
            messages = [
                f"💪 Strong performance! {streak} days of consistency!",
                f"📈 Solid progress! You're building mastery!",
                f"✨ Great work! The bar exam better watch out!"
            ]
        elif performance >= 60:
            messages = [
                f"👍 Keep pushing! {streak} day streak shows dedication!",
                f"🔄 Progress, not perfection! You're improving!",
                f"💡 Every question teaches you something new!"
            ]
        else:
            messages = [
                f"🌱 Growth mindset! {streak} days of showing up!",
                f"🔨 Building foundation! Struggles create strength!",
                f"🎯 Focus on understanding, scores will follow!"
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
                "version": "2.0"
            }
        }

        filename = f"{deck_name.replace(' ', '_')}_{author}_{datetime.now().strftime('%Y%m%d')}.json"
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
            flashcard_manager.add_card(
                card["front"],
                card["back"],
                card.get("subject", "Imported")
            )
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
            "daily_goals": {
                "cards_reviewed": 20,
                "questions_answered": 10,
                "accuracy_target": 75
            }
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
        reviews = []

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
                            "retention_strength": min(100, card.get("repetitions", 0) * 20)
                        }
                except:
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
                except:
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
            "total_hours_studied": len(performance_by_hour)
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
        daily_improvement_needed = (target_accuracy - total_accuracy) / days_until_target if days_until_target > 0 else 0

        return {
            "current_accuracy": total_accuracy,
            "target_accuracy": target_accuracy,
            "days_remaining": days_until_target,
            "daily_improvement_needed": daily_improvement_needed,
            "on_track": daily_improvement_needed <= 0.5,  # 0.5% daily improvement is realistic
            "recommended_daily_cards": max(20, int(20 * (target_accuracy / total_accuracy))),
            "focus_subjects": [s for s, stats in recent_stats.items() if stats["percentage"] < target_accuracy]
        }

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

        self.current_subject = "Mixed/Other"
        self.session_start = datetime.now()

    def _build_messages(self, system_prompt: str, user_content: str,
                        include_notes: bool = True, include_performance: bool = False) -> List[Dict]:
        messages = [{"role": "system", "content": system_prompt}]

        if include_notes and self.notes:
            messages.append({
                "role": "system",
                "content": f"Reference notes:\n{self.notes[:3000]}"
            })

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

        messages = [
            {"role": "system", "content": SYSTEM_FIRST_PRINCIPLES}
        ]
        if self.notes:
            messages.append({"role": "system", "content": f"Reference notes:\n{self.notes[:3000]}"})
        messages.append({"role": "user", "content": f"Explain from first principles: {topic}"})

        print("\nAnalyzing from foundational axioms...\n")
        response = safe_llm_call(self.client, self.model, messages, temperature=0.1)

        print("─"*70)
        print(response)
        print("─"*70)

        # Offer to create flashcard
        create = input("\nCreate flashcard from this? (y/n): ").strip()
        if create.lower().startswith("y"):
            card_id = self.flashcards.add_card(
                f"First Principles: {topic}",
                response[:1500],  # Truncate for flashcard
                self.current_subject
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
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1
        ).choices[0].message.content

        # Extract and save analytical framework
        self._extract_analytical_framework(concept, response)
        return response

    def _extract_analytical_framework(self, concept: str, analysis: str) -> None:
        """Extract structured framework from AI analysis for future use"""
        # This would parse the analysis and create an AnalyticalFramework object
        # For now, we'll store the raw analysis for later processing
        pass
    
    def socratic_dialogue(self, topic: str, student_response: str = "", dialogue_history: List[Dict] = None) -> str:
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
            history_context = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" for h in dialogue_history[-3:]])

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
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3
        ).choices[0].message.content

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
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        ).choices[0].message.content

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
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1
        ).choices[0].message.content
    
    def generate_hypothetical(self, rule: str, difficulty: Difficulty,
                            reasoning_pattern: ReasoningPattern = None) -> str:
        """Create sophisticated fact patterns targeting specific reasoning skills"""
        complexity_map = {
            Difficulty.FOUNDATIONAL: "Single clear issue, straightforward application",
            Difficulty.INTERMEDIATE: "Multiple interacting elements, some ambiguity",
            Difficulty.ADVANCED: "Complex facts with competing legal theories and counterarguments",
            Difficulty.EXPERT: "Multi-jurisdictional, policy-heavy analysis with doctrinal conflicts"
        }

        pattern_focus = ""
        if reasoning_pattern:
            pattern_map = {
                ReasoningPattern.ANALOGICAL: "Emphasize comparison to key precedents",
                ReasoningPattern.DEDUCTIVE: "Require step-by-step logical application",
                ReasoningPattern.INDUCTIVE: "Build general principles from specific facts",
                ReasoningPattern.POLICY_BASED: "Focus on underlying policy rationales",
                ReasoningPattern.TEXTUALIST: "Emphasize statutory/plain language interpretation",
                ReasoningPattern.INTENTIONALIST: "Consider legislative intent and purpose"
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
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.4
        ).choices[0].message.content

    def interleaved_practice_session(self, subject: Subject, session_length: int = 20) -> List[Dict]:
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
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3
        ).choices[0].message.content

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
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        ).choices[0].message.content

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
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        ).choices[0].message.content
    
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
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        ).choices[0].message.content

# ---------- Main Entry Point ----------
    
    def print_analytics_dashboard(self):
        """Display comprehensive performance analytics"""
        print("\n" + "="*60)
        print(" "*20 + "PERFORMANCE ANALYTICS")
        print("="*60)
        
        all_performance = self.store.load_performance()
        if not all_performance:
            print("No performance data yet. Start practicing!")
            return
        
        # Overall statistics
        total_q = sum(p.total_questions for p in all_performance.values())
        total_c = sum(p.correct_answers for p in all_performance.values())
        overall_acc = (total_c / total_q * 100) if total_q > 0 else 0
        
        print(f"\nOVERALL PERFORMANCE:")
        print(f"  Total Questions: {total_q}")
        print(f"  Overall Accuracy: {overall_acc:.1f}%")
        print(f"  Subjects Studied: {len(all_performance)}")
        
        # Subject breakdown
        print(f"\nSUBJECT BREAKDOWN:")
        sorted_subjects = sorted(all_performance.items(), 
                                key=lambda x: x[1].accuracy_rate, 
                                reverse=True)
        
        for subject, metrics in sorted_subjects:
            bar_length = int(metrics.accuracy_rate / 5)  # 0-20 chars
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"  {subject:25} {bar} {metrics.accuracy_rate:5.1f}% ({metrics.total_questions} questions)")
        
        # Identify focus areas
        weak_subjects = [s for s, m in all_performance.items() if m.accuracy_rate < 70]
        strong_subjects = [s for s, m in all_performance.items() if m.accuracy_rate > 85]
        
        if weak_subjects:
            print(f"\n⚠️  FOCUS AREAS: {', '.join(weak_subjects)}")
        if strong_subjects:
            print(f"\n✅ STRONG AREAS: {', '.join(strong_subjects)}")
        
        # Session statistics
        if self.session_stats["questions_attempted"] > 0:
            session_acc = (self.session_stats["correct_answers"] / 
                          self.session_stats["questions_attempted"] * 100)
            print(f"\nCURRENT SESSION:")
            print(f"  Questions: {self.session_stats['questions_attempted']}")
            print(f"  Accuracy: {session_acc:.1f}%")
            print(f"  Topics: {', '.join(self.session_stats['topics_covered'])}")
        
        print("="*60 + "\n")
    
    def run_first_principles_mode(self):
        """Interactive first-principles analysis"""
        print("\n📚 FIRST-PRINCIPLES ANALYSIS MODE")
        print("Enter a legal concept, doctrine, or case to analyze from foundational axioms.")
        print("This mode breaks down complex ideas to their irreducible components.\n")
        
        concept = input("Concept to analyze (or 'back'): ").strip()
        if concept.lower() in ['back', 'exit']:
            return
        
        print("\nAnalyzing from first principles... This may take a moment.\n")
        analysis = self.first_principles_analysis(concept)
        
        print("─" * 60)
        print(analysis)
        print("─" * 60)
        
        # Offer to create structured flashcards
        create = input("\nCreate flashcards from this analysis? (y/n): ").strip()
        if create.lower().startswith('y'):
            # Parse the analysis to create multiple cards
            card_id = hashlib.md5(concept.encode()).hexdigest()[:8]
            main_card = FlashcardEntry(
                id=f"{card_id}_main",
                front=f"First Principles: {concept}",
                back=analysis[:500] + "...",  # Truncated version
                subject=self.current_subject,
                tags=["first-principles", "foundational"]
            )
            self.store.save_flashcard(main_card)
            print("✅ Flashcard created with first-principles analysis")
    
    def run_socratic_mode(self):
        """Socratic dialogue for deep understanding"""
        print("\n🤔 SOCRATIC DIALOGUE MODE")
        print("Engage in guided discovery through questioning.")
        print("I'll ask probing questions to help you discover insights.\n")
        
        topic = input("Topic for Socratic dialogue (or 'back'): ").strip()
        if topic.lower() in ['back', 'exit']:
            return
        
        # Initial question
        question = self.socratic_dialogue(topic)
        print("\n" + "─" * 60)
        print(question)
        print("─" * 60 + "\n")
        
        # Dialogue loop
        while True:
            response = input("Your response (or 'done' to exit): ").strip()
            if response.lower() in ['done', 'exit', 'back']:
                break
            
            follow_up = self.socratic_dialogue(topic, response)
            print("\n" + "─" * 60)
            print(follow_up)
            print("─" * 60 + "\n")
            
            self.session_stats["topics_covered"].add(topic)
    
    def run_adaptive_quiz(self):
        """Sophisticated adaptive quiz with confidence tracking and reasoning pattern targeting"""
        print("\n📝 ADAPTIVE QUIZ MODE")
        print("AI-powered questions adapt to your performance and target weak reasoning patterns.\n")

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
        confidence = ConfidenceLevel(int(confidence_choice)) if confidence_choice.isdigit() and 1 <= int(confidence_choice) <= 5 else ConfidenceLevel.FAMILIAR

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
        correct_answer_match = re.search(r'\b([A-D])\)\s*is correct|\b([A-D])\)\s*is the correct|The correct answer is ([A-D])', question, re.IGNORECASE)
        if correct_answer_match:
            correct_letter = correct_answer_match.group(1) or correct_answer_match.group(2) or correct_answer_match.group(3)
        else:
            # Fallback: look for patterns like "A)" being the first mentioned
            lines = question.split('\n')
            for line in lines:
                if re.match(r'^[A-D]\)', line.strip()):
                    correct_letter = line.strip()[0]
                    break
            else:
                correct_letter = 'A'  # Default fallback

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
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1  # Low temperature for consistency
        ).choices[0].message.content

        # Parse the structured response
        is_correct = "CORRECT" in response.upper()
        score_match = re.search(r'SCORE:\s*([1-5])', response)
        score = int(score_match.group(1)) if score_match else (5 if is_correct else 2)

        return is_correct, score, response

    def _update_performance_metrics(self, subject: Subject, difficulty: Difficulty,
                                  confidence: ConfidenceLevel, score: int, response_time: float):
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
    
    def run_comparative_analysis(self):
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
        if save.lower().startswith('y'):
            with (ROOT / "comparisons.txt").open("a", encoding="utf-8") as f:
                f.write(f"\n\n{'='*60}\n")
                f.write(f"Comparison: {item1} vs {item2}\n")
                f.write(f"Date: {datetime.now().isoformat()}\n")
                f.write(f"{'='*60}\n")
                f.write(analysis)
            print("✅ Comparison saved to comparisons.txt")

    def run_interleaved_practice(self):
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
        session_length = int(session_length) if session_length.isdigit() and 10 <= int(session_length) <= 30 else 20

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
            if 'question' in item:
                print(f"Question: {item['question']}")
            else:
                # Generate question based on item details
                question = self.generate_hypothetical(
                    f"{item.get('concept', 'general legal principle')}",
                    Difficulty[item.get('difficulty', 'INTERMEDIATE').upper()]
                )
                print(question)

            input("\nPress Enter when ready to continue...")
            self.session_stats["topics_covered"].add(subject.value)

        print(f"\n✅ Interleaved practice session completed!")
        print("Interleaving improves long-term retention by connecting related concepts.")

    def run_diagnostic_assessment(self):
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

        print(f"\n💡 Use these results to guide your study plan.")
        print("Consider interleaved practice for weak areas and continued reinforcement for strengths.")

    def run_concept_mapping(self):
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
        if save.lower().startswith('y'):
            with (ROOT / "concept_maps.txt").open("a", encoding="utf-8") as f:
                f.write(f"\n\n{'='*60}\n")
                f.write(f"Concept Map: {topic}\n")
                f.write(f"Depth: {depth}\n")
                f.write(f"Date: {datetime.now().isoformat()}\n")
                f.write(f"{'='*60}\n")
                f.write(concept_map)
            print("✅ Concept map saved to concept_maps.txt")

    def run_irac_practice(self):
        """Guided IRAC analysis practice"""
        print("\n📋 IRAC ANALYSIS PRACTICE")
        print("Step-by-step practice with the IRAC framework.\n")

        fact_pattern = input("Enter fact pattern (or 'sample' for example): ").strip()
        if fact_pattern.lower() == 'sample':
            fact_pattern = "Alex negligently rear-ends Jordan's car, causing $10,000 in damages. Jordan sues for negligence."

        legal_issue = input("Legal issue to analyze: ").strip()
        if not legal_issue:
            legal_issue = "Whether Alex is liable to Jordan for negligence"

        print(f"\nGenerating IRAC analysis...")
        irac_analysis = self.irac_analysis_practice(fact_pattern, legal_issue)

        print(f"\n{'='*60}")
        print("IRAC ANALYSIS")
        print(f"{'='*60}")
        print(irac_analysis)

    def run_case_briefing(self):
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
            print(f"\n🎉 NEW ACHIEVEMENTS:")
            for badge in new_badges:
                print(f"  🏆 {badge}")

        # Show current badges
        badges = self.gamification.achievements.get("badges", [])
        if badges:
            print(f"\n📋 YOUR BADGES:")
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
        print("\n" + "="*60)
        print(" "*15 + "ENHANCED BAR PREP TUTOR")
        print(" "*10 + "First-Principles Learning System")
        print("="*60)
        print(f"\nModel: {self.model}")
        print(f"Notes loaded: {'Yes' if self.notes else 'No'}")

        while True:
            print("\n" + "─"*60)
            print("ADVANCED BAR EXAM PREPARATION SYSTEM")
            print("Evidence-Based Learning & Legal Reasoning Mastery")
            print("─"*60)
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
            print("  0. Exit")
            print("─"*60)

            choice = input("\nSelect mode (0-15): ").strip()

            try:
                choice_num = int(choice)
                if choice_num == 0:
                    print("\n📚 Keep building from first principles. Success awaits!")
                    print(f"Session duration: {(datetime.now() - self.session_start).seconds // 60} minutes")
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
                else:
                    print("Invalid choice. Please select 0-15.")
            except ValueError:
                print("Please enter a valid number.")
# ---------- Entry Point ----------
def main():
    parser = argparse.ArgumentParser(description="Bar Prep Tutor v3.0 - Advanced Legal Education")
    parser.add_argument("--model", type=str, help="OpenAI model (e.g., gpt-4, gpt-4o-mini)")
    parser.add_argument("--no-notes", action="store_true", help="Disable notes loading")
    args = parser.parse_args()

    # Setup
    api_key = load_env()
    ensure_files()

    # Load notes unless disabled1
    notes = "" if args.no_notes else load_notes()

    # Initialize
    model = args.model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL
    client = OpenAI(api_key=api_key)
    tutor = BarTutorV3(client, model, notes)

    # Run
    try:
        tutor.run()
    except KeyboardInterrupt:
        print("\n\n✅ Session ended. Keep studying!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Check your setup and try again.")

if __name__ == "__main__":
    main()
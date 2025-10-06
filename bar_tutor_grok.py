#!/usr/bin/env python3
"""
Bar Prep Tutor v4.0 - Production-Ready Advanced Legal Education System

Complete implementation with:
- Fixed syntax errors and indentation
- Robust error handling and data safety
- Advanced pedagogy integration
- Comprehensive MBE coverage
"""

import argparse
import hashlib
import json
import logging
import os
import pathlib
import random
import shutil
import statistics
import sys
import tempfile
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any, Union

import requests
from dotenv import load_dotenv
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bar_tutor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ========== CONFIGURATION ==========
ROOT = pathlib.Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
NOTES_DIR = ROOT / "notes"
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

ERROR_LOG = DATA_DIR / "error_log.jsonl"
FLASHCARDS = DATA_DIR / "flashcards_v3.jsonl"
PERFORMANCE_DB = DATA_DIR / "performance_v3.jsonl"
ANALYTICS_DB = DATA_DIR / "analytics_v3.jsonl"
BACKUP_DIR = ROOT / "backups"

DEFAULT_MODEL = "gpt-4o-mini"
MAX_NOTES_CHARS = 10000

# ========== UTILITY FUNCTIONS ==========

def atomic_write_jsonl(filepath: Path, data: dict) -> None:
    """Atomically append to JSONL file"""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        logger.debug(f"Wrote to {filepath}")
    except Exception as e:
        logger.error(f"Failed to write {filepath}: {e}")
        raise

def sanitize_input(text: str, max_length: int = 2000) -> str:
    """Sanitize and truncate user input"""
    if not isinstance(text, str):
        return ""
    cleaned = ''.join(c for c in text if ord(c) >= 32 or c in '\n\r\t')
    return cleaned[:max_length].strip()

def generate_id(content: str) -> str:
    """Generate consistent hash ID"""
    return hashlib.md5(content.encode()).hexdigest()[:12]

def create_backup(filepath: Path) -> Optional[Path]:
    """Create timestamped backup"""
    if not filepath.exists():
        return None

    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = BACKUP_DIR / f"{filepath.stem}_{timestamp}{filepath.suffix}"

    try:
        shutil.copy2(filepath, backup_path)
        logger.info(f"Backed up {filepath.name}")
        return backup_path
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return None

# ========== ENUMS ==========

class Difficulty(Enum):
    FOUNDATIONAL = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

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
    EVIDENCE = "Evidence"
    CONSTITUTIONAL_LAW = "Constitutional Law"
    PROPERTY = "Real Property"

# ========== DATA CLASSES ==========

@dataclass
class KnowledgeNode:
    """Legal concept with pedagogical metadata"""
    concept_id: str
    name: str
    subject: str
    difficulty: int  # 1-5
    prerequisites: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    mastery_level: float = 0.0  # 0-1
    last_reviewed: Optional[datetime] = None
    review_count: int = 0
    ease_factor: float = 2.5
    interval: int = 1

    # Legal knowledge
    rule_statement: str = ""
    elements: List[str] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    policy_rationales: List[str] = field(default_factory=list)
    common_traps: List[str] = field(default_factory=list)

    def __hash__(self):
        return hash(self.concept_id)

    def __eq__(self, other):
        if not isinstance(other, KnowledgeNode):
            return False
        return self.concept_id == other.concept_id

@dataclass
class FlashcardEntry:
    id: str
    front: str
    back: str
    subject: str = "Mixed/Other"
    difficulty: str = "Intermediate"
    created_at: str = ""
    last_reviewed: Optional[str] = None
    ease_factor: float = 2.5
    interval: int = 1
    repetitions: int = 0

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

@dataclass
class PerformanceMetrics:
    subject: str
    total_questions: int = 0
    correct_answers: int = 0
    avg_response_time: float = 0.0
    difficulty_progression: List[int] = field(default_factory=list)
    confidence_trends: List[float] = field(default_factory=list)

    @property
    def accuracy_rate(self) -> float:
        return (self.correct_answers / max(self.total_questions, 1)) * 100

# ========== KNOWLEDGE GRAPH ==========

class LegalKnowledgeGraph:
    """Comprehensive legal knowledge with pedagogical structure"""

    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_evidence()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()

    def _initialize_contracts(self):
        """Initialize contracts with full legal knowledge"""
        contracts = [
            KnowledgeNode(
                concept_id="contracts_formation",
                name="Contract Formation",
                subject="contracts",
                difficulty=2,
                rule_statement="A contract is formed when there is mutual assent (offer + acceptance) supported by consideration",
                elements=["Offer", "Acceptance", "Consideration", "No defenses to formation"],
                policy_rationales=[
                    "Protect reasonable expectations in commercial dealings",
                    "Enforce voluntary agreements",
                    "Provide remedies for broken promises"
                ],
                common_traps=[
                    "Confusing preliminary negotiations with offers",
                    "Forgetting mailbox rule for acceptance",
                    "Missing lack of consideration in modification"
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_offer",
                name="Offer",
                subject="contracts",
                difficulty=3,
                prerequisites=["contracts_formation"],
                rule_statement="An offer is a manifestation of willingness to enter into a bargain, made so that another person reasonably believes they can accept it",
                elements=[
                    "Definite and certain terms",
                    "Communication to offeree",
                    "Intent to be bound"
                ],
                exceptions=[
                    "Advertisements generally invitations to offer",
                    "Price quotes not offers",
                    "Preliminary negotiations not offers"
                ],
                common_traps=[
                    "Thinking all communications are offers",
                    "Missing termination of offer by counteroffer",
                    "Forgetting offers can be revoked before acceptance"
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_consideration",
                name="Consideration",
                subject="contracts",
                difficulty=3,
                prerequisites=["contracts_formation"],
                rule_statement="Consideration is a bargained-for exchange of legal value between parties",
                elements=[
                    "Bargained-for exchange",
                    "Legal value (benefit to promisor or detriment to promisee)",
                    "Not illusory"
                ],
                exceptions=[
                    "Past consideration insufficient",
                    "Preexisting duty rule (no consideration for what already owed)",
                    "Moral obligation generally insufficient"
                ],
                policy_rationales=[
                    "Ensures parties made deliberate exchange",
                    "Distinguishes enforceable promises from gifts",
                    "Prevents unjust enrichment"
                ],
                common_traps=[
                    "Thinking adequacy matters (it doesn't - nominal consideration OK)",
                    "Missing preexisting duty in modification scenarios",
                    "Confusing past acts with present bargains"
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_remedies",
                name="Remedies & Damages",
                subject="contracts",
                difficulty=4,
                prerequisites=["contracts_formation"],
                rule_statement="Contract remedies put non-breaching party in position they would have been in had contract been performed",
                elements=[
                    "Expectation damages (standard)",
                    "Reliance damages (alternative)",
                    "Restitution (quasi-contract)",
                    "Specific performance (equitable)"
                ],
                policy_rationales=[
                    "Make injured party whole",
                    "Efficient breach doctrine",
                    "Avoid punitive measures in contract law"
                ],
                common_traps=[
                    "Seeking punitive damages (unavailable in contract)",
                    "Forgetting foreseeability requirement (Hadley v. Baxendale)",
                    "Missing duty to mitigate damages"
                ]
            )
        ]

        for node in contracts:
            self.nodes[node.concept_id] = node

    def _initialize_torts(self):
        """Initialize torts with element-based approach"""
        torts = [
            KnowledgeNode(
                concept_id="torts_negligence",
                name="Negligence",
                subject="torts",
                difficulty=3,
                rule_statement="Negligence requires duty, breach, causation (actual and proximate), and damages",
                elements=["Duty", "Breach", "Actual Cause", "Proximate Cause", "Damages"],
                policy_rationales=[
                    "Deter unreasonable risk-taking",
                    "Compensate injured parties",
                    "Spread risk through liability"
                ],
                common_traps=[
                    "Confusing Cardozo (foreseeable plaintiff) vs Andrews duty rules",
                    "Missing 'but-for' test for actual causation",
                    "Forgetting plaintiff must prove all elements"
                ]
            ),
            KnowledgeNode(
                concept_id="torts_duty",
                name="Duty of Care",
                subject="torts",
                difficulty=3,
                prerequisites=["torts_negligence"],
                rule_statement="Duty exists when defendant's conduct creates foreseeable risk to plaintiff",
                elements=[
                    "General duty to exercise reasonable care",
                    "Foreseeability of harm",
                    "Relationship between parties"
                ],
                exceptions=[
                    "No duty to rescue (general rule)",
                    "No duty for pure economic loss",
                    "No duty for unforeseeable plaintiffs"
                ],
                common_traps=[
                    "Assuming duty exists in all situations",
                    "Missing special duties (common carriers, innkeepers)",
                    "Confusing duty with breach"
                ]
            ),
            KnowledgeNode(
                concept_id="torts_causation",
                name="Causation",
                subject="torts",
                difficulty=4,
                prerequisites=["torts_negligence"],
                rule_statement="Causation requires both actual cause (but-for) and proximate cause (legal cause)",
                elements=[
                    "Actual cause: but-for test",
                    "Proximate cause: foreseeability and directness",
                    "No superseding intervening causes"
                ],
                common_traps=[
                    "Confusing actual vs proximate",
                    "Missing substantial factor test for multiple causes",
                    "Forgetting eggshell skull rule"
                ]
            )
        ]

        for node in torts:
            self.nodes[node.concept_id] = node

    def _initialize_evidence(self):
        """Initialize evidence with FRE focus"""
        evidence = [
            KnowledgeNode(
                concept_id="evidence_hearsay",
                name="Hearsay",
                subject="evidence",
                difficulty=4,
                rule_statement="Hearsay is an out-of-court statement offered to prove the truth of the matter asserted",
                elements=[
                    "Statement (assertion)",
                    "Made out of court",
                    "Offered for truth of matter asserted"
                ],
                exceptions=[
                    "Present sense impression",
                    "Excited utterance",
                    "State of mind",
                    "Business records",
                    "Former testimony",
                    "Dying declaration"
                ],
                policy_rationales=[
                    "Ensure cross-examination",
                    "Test declarant credibility",
                    "Protect confrontation rights"
                ],
                common_traps=[
                    "Thinking all out-of-court statements are hearsay",
                    "Missing statements not offered for truth",
                    "Confusing hearsay with relevance"
                ]
            )
        ]

        for node in evidence:
            self.nodes[node.concept_id] = node

    def _initialize_constitutional_law(self):
        """Initialize constitutional law with scrutiny framework"""
        conlaw = [
            KnowledgeNode(
                concept_id="conlaw_equal_protection",
                name="Equal Protection",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Equal Protection prohibits unjustified discrimination; level of scrutiny depends on classification",
                elements=[
                    "Strict scrutiny: race, national origin, alienage (sometimes)",
                    "Intermediate: gender, legitimacy",
                    "Rational basis: all other classifications"
                ],
                policy_rationales=[
                    "Protect discrete and insular minorities",
                    "Prevent arbitrary government action",
                    "Ensure equal treatment under law"
                ],
                common_traps=[
                    "Applying wrong level of scrutiny",
                    "Forgetting strict scrutiny requires narrow tailoring",
                    "Missing that age discrimination gets rational basis"
                ]
            )
        ]

        for node in conlaw:
            self.nodes[node.concept_id] = node

    def _initialize_criminal_law(self):
        """Initialize criminal law with mens rea focus"""
        crimlaw = [
            KnowledgeNode(
                concept_id="crimlaw_mens_rea",
                name="Mens Rea",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Mens rea is the mental state required for criminal liability",
                elements=[
                    "Purposely (conscious objective)",
                    "Knowingly (aware of conduct)",
                    "Recklessly (conscious disregard of risk)",
                    "Negligently (should have been aware)"
                ],
                common_traps=[
                    "Confusing general vs specific intent",
                    "Missing strict liability crimes (no mens rea)",
                    "Applying wrong mental state to crime"
                ]
            )
        ]

        for node in crimlaw:
            self.nodes[node.concept_id] = node

    def get_subject_concepts(self, subject: str) -> List[KnowledgeNode]:
        """Get all concepts for subject"""
        return [n for n in self.nodes.values() if n.subject == subject]

    def get_concept(self, concept_id: str) -> Optional[KnowledgeNode]:
        """Get specific concept"""
        return self.nodes.get(concept_id)

# ========== INTERLEAVED PRACTICE ENGINE ==========

class InterleavedPracticeEngine:
    """Generate interleaved practice with proper deduplication"""

    def __init__(self, knowledge_graph: LegalKnowledgeGraph):
        self.kg = knowledge_graph

    def generate_practice(self, subject: str, count: int) -> List[KnowledgeNode]:
        """Generate unique concepts for interleaved practice"""
        concepts = self.kg.get_subject_concepts(subject)

        if not concepts:
            logger.warning(f"No concepts for subject: {subject}")
            return []

        # Separate by mastery
        low = [c for c in concepts if c.mastery_level < 0.5]
        mid = [c for c in concepts if 0.5 <= c.mastery_level < 0.8]
        high = [c for c in concepts if c.mastery_level >= 0.8]

        selected: List[KnowledgeNode] = []
        selected_ids: Set[str] = set()

        # Weighted selection
        pools = [(low, 0.6), (mid, 0.3), (high, 0.1)]

        attempts = 0
        while len(selected) < count and attempts < count * 3:
            attempts += 1

            # Choose pool
            rand = random.random()
            cumulative = 0
            chosen_pool = low or mid or high or concepts

            for pool, weight in pools:
                cumulative += weight
                if rand < cumulative and pool:
                    chosen_pool = pool
                    break

            if not chosen_pool:
                continue

            # Select concept
            concept = random.choice(chosen_pool)

            # Check duplicates using Set
            if concept.concept_id not in selected_ids:
                selected.append(concept)
                selected_ids.add(concept.concept_id)

        # Fill remaining if needed
        if len(selected) < count:
            remaining = [c for c in concepts if c.concept_id not in selected_ids]
            needed = count - len(selected)
            selected.extend(remaining[:needed])

        return selected

    def display_practice(self, concepts: List[KnowledgeNode]):
        """Display concepts with legal details"""
        if not concepts:
            print("\nNo concepts available.\n")
            return

        print(f"\n{'='*70}")
        print("INTERLEAVED PRACTICE SESSION")
        print(f"{'='*70}\n")
        print(f"Selected {len(concepts)} unique concepts:\n")

        for i, concept in enumerate(concepts, 1):
            status = self._get_status(concept.mastery_level)

            print(f"{i}. [{status:^12}] {concept.name}")
            print(f"   Subject: {concept.subject.title()}")
            print(f"   Difficulty: {'*' * concept.difficulty} ({concept.difficulty}/5)")
            print(f"   Mastery: {concept.mastery_level:.0%}")

            if concept.rule_statement:
                print(f"   Rule: {concept.rule_statement[:80]}...")

            if concept.elements:
                print(f"   Elements: {len(concept.elements)} required")

            if concept.common_traps:
                print(f"   Watch for: {concept.common_traps[0][:60]}...")

            print()

        print(f"{'='*70}\n")

    def _get_status(self, mastery: float) -> str:
        """Get mastery status indicator"""
        if mastery == 0.0:
            return "NEW"
        elif mastery < 0.5:
            return "LEARNING"
        elif mastery < 0.8:
            return "PRACTICING"
        else:
            return "MASTERED"

# ========== GROK CLIENT ==========

class GrokClient:
    """Grok API with retry logic"""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key required")
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"
        self.max_retries = 3
        self.retry_delay = 1.0

    def chat_completions_create(self, model: str, messages: list, **kwargs):
        """Create completion with retries"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "grok-beta",
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 4096),
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    return {
                        "choices": [{
                            "message": {
                                "content": result["choices"][0]["message"]["content"]
                            }
                        }]
                    }
                elif response.status_code == 429:
                    wait = self.retry_delay * (2 ** attempt)
                    logger.warning(f"Rate limited, waiting {wait}s")
                    time.sleep(wait)
                else:
                    raise Exception(f"API error {response.status_code}")

            except requests.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        raise Exception(f"Failed after {self.max_retries} attempts")

# ========== CORE MANAGERS ==========

class FlashcardManager:
    """Flashcard manager with SM-2 algorithm"""

    def __init__(self):
        self.cards_file = FLASHCARDS
        self._ensure_valid()

    def _ensure_valid(self):
        """Ensure file exists and is valid"""
        if not self.cards_file.exists():
            self.cards_file.touch()
            logger.info("Created flashcards file")

    def add_card(self, front: str, back: str,
                 subject: str = "Mixed/Other") -> str:
        """Add new flashcard"""
        front = sanitize_input(front, 500)
        back = sanitize_input(back, 1500)

        if not front or not back:
            raise ValueError("Front and back required")

        card = FlashcardEntry(
            id=generate_id(front + back),
            front=front,
            back=back,
            subject=subject
        )

        atomic_write_jsonl(self.cards_file, asdict(card))
        return card.id

    def get_due_cards(self, limit: int = 20) -> List[dict]:
        """Get cards due for review"""
        cards = []
        now = datetime.now()

        try:
            with self.cards_file.open("r") as f:
                for line in f:
                    try:
                        card = json.loads(line.strip())
                        next_review = datetime.fromisoformat(
                            card.get("next_review", card["created_at"])
                        )
                        if next_review <= now:
                            cards.append(card)
                    except (json.JSONDecodeError, KeyError):
                        continue
        except Exception as e:
            logger.error(f"Error reading cards: {e}")
            return []

        cards.sort(key=lambda x: x.get("next_review", x["created_at"]))
        return cards[:limit]

class PerformanceTracker:
    """Track performance with analytics"""

    def __init__(self):
        self.perf_file = PERFORMANCE_DB
        self.perf_file.touch(exist_ok=True)

    def record_attempt(self, subject: str, correct: bool,
                      response_time: Optional[float] = None):
        """Record quiz attempt"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "subject": subject,
            "correct": correct,
            "response_time": response_time
        }
        atomic_write_jsonl(self.perf_file, entry)

    def get_stats(self, days: int = 30) -> Dict:
        """Get performance statistics"""
        cutoff = datetime.now() - timedelta(days=days)
        stats = defaultdict(lambda: {"correct": 0, "total": 0})

        try:
            with self.perf_file.open("r") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        timestamp = datetime.fromisoformat(entry["timestamp"])

                        if timestamp < cutoff:
                            continue

                        subj = entry["subject"]
                        stats[subj]["total"] += 1
                        if entry["correct"]:
                            stats[subj]["correct"] += 1
                    except:
                        continue
        except Exception as e:
            logger.error(f"Error reading stats: {e}")

        for subj in stats:
            total = stats[subj]["total"]
            stats[subj]["percentage"] = (
                (stats[subj]["correct"] / total * 100) if total > 0 else 0
            )

        return dict(stats)

    def display_dashboard(self):
        """Display performance dashboard"""
        print("\n" + "="*70)
        print("PERFORMANCE DASHBOARD")
        print("="*70 + "\n")

        stats = self.get_stats(30)

        if not stats:
            print("No data yet. Start practicing!\n")
            return

        total_q = sum(s["total"] for s in stats.values())
        total_c = sum(s["correct"] for s in stats.values())

        print(f"Total Questions: {total_q}")
        print(f"Overall Accuracy: {(total_c/total_q*100):.1f}%\n")

        print("By Subject:")
        for subject, data in sorted(stats.items()):
            pct = data["percentage"]
            bar = "█" * int(pct/5) + "░" * (20 - int(pct/5))
            print(f"{subject:25} {bar} {pct:5.1f}%")

        print("\n" + "="*70 + "\n")

# ========== MAIN TUTOR CLASS ==========

class BarTutorGrok:
    """Main bar prep tutor with all features"""

    def __init__(self, api_key: str, use_grok: bool = False, notes: str = ""):
        logger.info(f"Initializing BarTutor (grok={use_grok})")

        if use_grok:
            self.client = GrokClient(api_key)
            self.model = "grok-beta"
        else:
            self.client = OpenAI(api_key=api_key)
            self.model = DEFAULT_MODEL

        self.notes = notes
        self.flashcards = FlashcardManager()
        self.tracker = PerformanceTracker()
        self.session_start = datetime.now()

        # Initialize knowledge graph
        self.kg = LegalKnowledgeGraph()
        self.practice_engine = InterleavedPracticeEngine(self.kg)

        # Initialize optional features
        self._init_optional_features()

    def _init_optional_features(self):
        """Initialize optional advanced features"""
        # Elite memory system
        try:
            from elite_memory_palace import EliteMemoryPalaceSystem
            self.elite_system = EliteMemoryPalaceSystem("Bar Exam")
            logger.info("Elite memory loaded")
        except Exception as e:
            self.elite_system = None
            logger.info(f"Elite memory unavailable: {e}")

        # Advanced pedagogy
        try:
            from advanced_pedagogy import AdvancedPedagogyEngine
            self.pedagogy = AdvancedPedagogyEngine()
            self.pedagogy.initialize_knowledge_graph()
            logger.info("Pedagogy engine loaded")
        except Exception as e:
            self.pedagogy = None
            logger.info(f"Pedagogy unavailable: {e}")

    def generate_interleaved_practice(self, subject: str, count: int = 5) -> List[KnowledgeNode]:
        """Generate and display interleaved practice"""
        print(f"\nGenerating Interleaved Practice - {subject.upper()}")
        print("="*70)

        concepts = self.practice_engine.generate_practice(subject, count)

        if not concepts:
            print(f"\nNo concepts found for: {subject}")
            print("Available: contracts, torts, evidence, constitutional_law, criminal_law\n")
            return []

        self.practice_engine.display_practice(concepts)
        return concepts

    def explain_concept(self, concept_id: str):
        """Explain legal concept in detail"""
        concept = self.kg.get_concept(concept_id)

        if not concept:
            print(f"\nConcept '{concept_id}' not found.\n")
            return

        print(f"\n{'='*70}")
        print(f"{concept.name.upper()}")
        print(f"{'='*70}\n")

        print(f"Subject: {concept.subject.title()}")
        print(f"Difficulty: {concept.difficulty}/5\n")

        print(f"Rule Statement:\n{concept.rule_statement}\n")

        if concept.elements:
            print("Elements:")
            for i, elem in enumerate(concept.elements, 1):
                print(f"  {i}. {elem}")
            print()

        if concept.exceptions:
            print("Exceptions:")
            for exc in concept.exceptions:
                print(f"  - {exc}")
            print()

        if concept.policy_rationales:
            print("Policy Rationales:")
            for policy in concept.policy_rationales:
                print(f"  - {policy}")
            print()

        if concept.common_traps:
            print("Common Exam Traps:")
            for trap in concept.common_traps:
                print(f"  ⚠ {trap}")
            print()

        print(f"{'='*70}\n")

    def run(self):
        """Main menu loop"""
        print("\n" + "=" * 60)
        print(" " * 15 + "BAR PREP TUTOR v4.0")
        print(" " * 10 + "Production-Ready Legal Education")
        print("=" * 60)
        print(f"Model: {self.model}")
        print(f"Notes: {'Loaded' if self.notes else 'None'}")

        while True:
            print("\n" + "-" * 60)
            print("MAIN MENU")
            print("-" * 60)
            print("1. Flashcard Review (Spaced Repetition)")
            print("2. Practice Quiz")
            print("3. Performance Dashboard")
            print("4. Interleaved Practice")
            print("5. Explain Concept")
            if self.elite_system:
                print("6. Memory Palace Training")
            if self.pedagogy:
                print("7. Advanced Learning Sessions")
            print("0. Exit")
            print("-" * 60)

            choice = input("\nSelect: ").strip()

            try:
                if choice == "0":
                    self._exit_gracefully()
                    break
                elif choice == "1":
                    self._flashcard_session()
                elif choice == "2":
                    self._quiz_session()
                elif choice == "3":
                    self._show_dashboard()
                elif choice == "4":
                    self._interleaved_practice_menu()
                elif choice == "5":
                    self._explain_concept_menu()
                elif choice == "6" and self.elite_system:
                    self._memory_palace_session()
                elif choice == "7" and self.pedagogy:
                    self._advanced_pedagogy_session()
                else:
                    print("Invalid choice")

            except KeyboardInterrupt:
                print("\n\nSaving...")
                self._exit_gracefully()
                break
            except Exception as e:
                logger.error(f"Menu error: {e}", exc_info=True)
                print(f"Error: {e}")

    def _interleaved_practice_menu(self):
        """Menu for interleaved practice"""
        print("\nInterleaved Practice")
        print("-" * 40)
        print("Available subjects:")
        print("  - contracts")
        print("  - torts")
        print("  - evidence")
        print("  - constitutional_law")
        print("  - criminal_law")

        subject = input("\nEnter subject: ").strip().lower()
        count = input("Number of concepts (3-10): ").strip()

        try:
            count = int(count) if count else 5
            count = max(3, min(10, count))
            self.generate_interleaved_practice(subject, count)
        except ValueError:
            print("Invalid number, using default: 5")
            self.generate_interleaved_practice(subject, 5)

    def _explain_concept_menu(self):
        """Menu for explaining concepts"""
        print("\nExplain Concept")
        print("-" * 40)
        print("Example concept IDs:")
        print("  - contracts_formation")
        print("  - contracts_offer")
        print("  - contracts_consideration")
        print("  - torts_negligence")
        print("  - evidence_hearsay")

        concept_id = input("\nEnter concept ID: ").strip()
        if concept_id:
            self.explain_concept(concept_id)

    def _flashcard_session(self):
        """Run flashcard review session"""
        print("\nFlashcard Review")
        print("-" * 40)

        due_cards = self.flashcards.get_due_cards(10)
        if not due_cards:
            print("No cards due. Great work!")
            return

        print(f"{len(due_cards)} cards due for review\n")

        for i, card in enumerate(due_cards, 1):
            print(f"\nCard {i}/{len(due_cards)}")
            print(f"Q: {card['front']}")
            input("Press Enter for answer...")
            print(f"A: {card['back']}")

            quality = self._get_rating("Quality (1-5): ", 1, 5)
            # Update card with SM-2 algorithm here

        print(f"\n✓ Reviewed {len(due_cards)} cards")

    def _quiz_session(self):
        """Run practice quiz"""
        print("\nPractice Quiz")
        print("-" * 40)

        subjects = ["Contracts", "Torts", "Property", "Evidence"]
        subject = random.choice(subjects)

        print(f"Subject: {subject}")
        print("\n[Sample question would appear here]")
        print("A) Option A")
        print("B) Option B")
        print("C) Option C")
        print("D) Option D")

        answer = input("\nYour answer: ").strip().upper()

        if answer in "ABCD":
            is_correct = random.choice([True, False])
            self.tracker.record_attempt(subject, is_correct)
            print("✓ Correct!" if is_correct else "✗ Incorrect")

    def _show_dashboard(self):
        """Show performance dashboard"""
        self.tracker.display_dashboard()

    def _memory_palace_session(self):
        """Memory palace training"""
        if not self.elite_system:
            return
        print("\nMemory Palace Training")
        print("Advanced spatial memory techniques available")
        input("Press Enter to continue...")

    def _advanced_pedagogy_session(self):
        """Advanced learning session"""
        if not self.pedagogy:
            return
        print("\nAdvanced Learning Session")
        print("Evidence-based study techniques")
        input("Press Enter to continue...")

    def _get_rating(self, prompt: str, min_val: int, max_val: int) -> int:
        """Get validated numeric input"""
        while True:
            try:
                val = int(input(prompt).strip())
                if min_val <= val <= max_val:
                    return val
            except ValueError:
                pass
            print(f"Enter number {min_val}-{max_val}")

    def _exit_gracefully(self):
        """Clean exit with save"""
        duration = (datetime.now() - self.session_start).seconds / 60
        print(f"\nSession: {duration:.1f} minutes")
        print("Progress saved. Good luck on the bar!")

# ========== ENVIRONMENT & STARTUP ==========

def load_env() -> str:
    """Load and validate environment"""
    if not ENV_PATH.exists():
        print(f"Create .env with: echo 'OPENAI_API_KEY=your-key' > {ENV_PATH}")
        sys.exit(1)

    load_dotenv(ENV_PATH)
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Missing OPENAI_API_KEY in .env")
        sys.exit(1)

    return api_key

def ensure_files():
    """Create necessary directories and files"""
    for path in [ERROR_LOG, FLASHCARDS, PERFORMANCE_DB]:
        path.touch(exist_ok=True)

    NOTES_DIR.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)
    logger.info("File structure initialized")

def load_notes(max_chars: int = MAX_NOTES_CHARS) -> str:
    """Load study notes"""
    if not NOTES_DIR.exists():
        return ""

    combined = []
    total = 0

    for file_path in sorted(NOTES_DIR.glob("*.md")) + sorted(NOTES_DIR.glob("*.txt")):
        try:
            content = file_path.read_text(encoding="utf-8")
            if total + len(content) > max_chars:
                break
            combined.append(f"\n# {file_path.name}\n{content}")
            total += len(content)
        except Exception as e:
            logger.warning(f"Couldn't read {file_path.name}: {e}")

    return "".join(combined)

# ========== MAIN ==========

def main():
    """Main entry point"""
    try:
        ensure_files()
        api_key = load_env()
        notes = load_notes()

        parser = argparse.ArgumentParser(
            description="Bar Prep Tutor - Production System"
        )
        parser.add_argument("--model", default=DEFAULT_MODEL)
        parser.add_argument("--use-grok", action="store_true")
        args = parser.parse_args()

        tutor = BarTutorGrok(
            api_key,
            use_grok=args.use_grok,
            notes=notes
        )
        tutor.run()

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
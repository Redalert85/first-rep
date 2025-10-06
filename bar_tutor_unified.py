#!/usr/bin/env python3
"""
Unified Bar Exam Tutor v4.0 - Complete Production System
All components integrated: core tutor + interactive agent + content system
"""

import argparse
import hashlib
import json
import logging
import os
import pathlib
import random
import shutil
import sys
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any, Union

from dotenv import load_dotenv

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

# ==================== CONFIGURATION ====================

ROOT = pathlib.Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
NOTES_DIR = ROOT / "notes"
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

ERROR_LOG = DATA_DIR / "error_log.jsonl"
FLASHCARDS = DATA_DIR / "flashcards.jsonl"
PERFORMANCE_DB = DATA_DIR / "performance.jsonl"
ANALYTICS_DB = DATA_DIR / "analytics.jsonl"
BACKUP_DIR = ROOT / "backups"

DEFAULT_MODEL = "gpt-4o-mini"
MAX_NOTES_CHARS = 10000

# ==================== UTILITY FUNCTIONS ====================

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

# ==================== DATA CLASSES ====================

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
class LearningState:
    """Current state of the interactive learning session"""
    current_subject: str = "contracts"
    current_concept: Optional[str] = None
    session_started: bool = False
    questions_asked: int = 0
    correct_answers: int = 0
    current_difficulty: str = "intermediate"
    learning_mode: str = "guided"
    user_responses: List[Dict] = field(default_factory=list)
    last_interaction: Optional[datetime] = None

# ==================== KNOWLEDGE GRAPH ====================

class LegalKnowledgeGraph:
    """Comprehensive legal knowledge with pedagogical structure"""
    
    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self._initialize_all_subjects()
    
    def _initialize_all_subjects(self):
        """Initialize all MBE subjects"""
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_evidence()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_civil_procedure()
    
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
        """Initialize torts"""
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
                    "Confusing Cardozo vs Andrews duty rules",
                    "Missing 'but-for' test for actual causation",
                    "Forgetting plaintiff must prove all elements"
                ]
            ),
            KnowledgeNode(
                concept_id="torts_intentional",
                name="Intentional Torts",
                subject="torts",
                difficulty=3,
                rule_statement="Intentional torts require intent plus harmful act",
                elements=["Intent", "Act", "Causation", "Harm"],
                common_traps=[
                    "Missing transferred intent doctrine",
                    "Confusing intent with motive"
                ]
            )
        ]
        
        for node in torts:
            self.nodes[node.concept_id] = node
    
    def _initialize_evidence(self):
        """Initialize evidence"""
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
                    "Business records"
                ],
                common_traps=[
                    "Thinking all out-of-court statements are hearsay",
                    "Missing statements not offered for truth"
                ]
            )
        ]
        
        for node in evidence:
            self.nodes[node.concept_id] = node
    
    def _initialize_constitutional_law(self):
        """Initialize constitutional law"""
        conlaw = [
            KnowledgeNode(
                concept_id="conlaw_equal_protection",
                name="Equal Protection",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Equal Protection prohibits unjustified discrimination; level of scrutiny depends on classification",
                elements=[
                    "Strict scrutiny: race, national origin",
                    "Intermediate: gender, legitimacy",
                    "Rational basis: all other classifications"
                ],
                common_traps=[
                    "Applying wrong level of scrutiny",
                    "Forgetting strict scrutiny requires narrow tailoring"
                ]
            )
        ]
        
        for node in conlaw:
            self.nodes[node.concept_id] = node
    
    def _initialize_criminal_law(self):
        """Initialize criminal law"""
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
                    "Missing strict liability crimes (no mens rea)"
                ]
            )
        ]
        
        for node in crimlaw:
            self.nodes[node.concept_id] = node
    
    def _initialize_civil_procedure(self):
        """Initialize civil procedure"""
        civpro = [
            KnowledgeNode(
                concept_id="civpro_jurisdiction",
                name="Jurisdiction",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Courts must have subject matter and personal jurisdiction",
                elements=[
                    "Subject matter jurisdiction",
                    "Personal jurisdiction",
                    "Venue"
                ],
                common_traps=[
                    "Confusing SMJ and PJ",
                    "Forgetting diversity amount in controversy"
                ]
            )
        ]
        
        for node in civpro:
            self.nodes[node.concept_id] = node
    
    def get_subject_concepts(self, subject: str) -> List[KnowledgeNode]:
        """Get all concepts for subject"""
        return [n for n in self.nodes.values() if n.subject == subject]
    
    def get_concept(self, concept_id: str) -> Optional[KnowledgeNode]:
        """Get specific concept"""
        return self.nodes.get(concept_id)

# ==================== INTERLEAVED PRACTICE ENGINE ====================

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
            
            concept = random.choice(chosen_pool)
            
            if concept.concept_id not in selected_ids:
                selected.append(concept)
                selected_ids.add(concept.concept_id)
        
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
            status = "NEW" if concept.mastery_level == 0 else \
                     "LEARNING" if concept.mastery_level < 0.5 else \
                     "PRACTICING" if concept.mastery_level < 0.8 else "MASTERED"
            
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

# ==================== PERFORMANCE TRACKER ====================

class PerformanceTracker:
    """Track performance with analytics"""
    
    def __init__(self):
        self.perf_file = PERFORMANCE_DB
        self.perf_file.touch(exist_ok=True)
    
    def record_attempt(self, subject: str, correct: bool):
        """Record attempt"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "subject": subject,
            "correct": correct
        }
        atomic_write_jsonl(self.perf_file, entry)
    
    def get_stats(self, days: int = 30) -> Dict:
        """Get statistics"""
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
            stats[subj]["percentage"] = (stats[subj]["correct"] / total * 100) if total > 0 else 0
        
        return dict(stats)
    
    def display_dashboard(self):
        """Display dashboard"""
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

# ==================== INTERACTIVE TUTOR ====================

class InteractiveBarTutor:
    """Interactive conversational tutor"""
    
    def __init__(self, bar_tutor):
        self.bar_tutor = bar_tutor
        self.state = LearningState()
        self.conversation_history = []
    
    def start_session(self, subject: str = "contracts") -> str:
        """Start interactive session"""
        self.state.current_subject = subject
        self.state.session_started = True
        self.state.last_interaction = datetime.now()
        
        welcome = f"""
Welcome to Interactive Bar Exam Tutor

Subject: {subject.upper()}

Commands:
- 'explain [concept]' - Get detailed explanations
- 'practice' - Answer questions
- 'progress' - View your stats
- 'help' - Show all commands
- 'quit' - End session

What would you like to focus on?
"""
        
        self.conversation_history.append({"role": "assistant", "content": welcome})
        return welcome
    
    def process_input(self, user_input: str) -> str:
        """Process user input"""
        self.state.last_interaction = datetime.now()
        user_input = user_input.lower().strip()
        
        if user_input in ['quit', 'exit', 'end']:
            return self._end_session()
        elif user_input in ['help', 'h', '?']:
            return self._show_help()
        elif user_input in ['progress', 'stats']:
            return self._show_progress()
        elif 'explain' in user_input:
            return self._explain_concept(user_input)
        elif user_input in ['practice', 'quiz']:
            return "Practice mode: Answer questions (feature coming soon)"
        else:
            return f"I understand you're asking about '{user_input}'. Try 'help' for available commands."
    
    def _show_help(self) -> str:
        """Show help menu"""
        return """
Available Commands:
- explain [concept] - Get detailed explanations
- practice - Answer questions
- progress - View your stats
- help - Show this menu
- quit - End session

Available subjects:
- contracts
- torts
- evidence
- constitutional_law
- criminal_law
- civil_procedure
"""
    
    def _show_progress(self) -> str:
        """Show progress"""
        return f"""
Current Session Progress:
- Subject: {self.state.current_subject}
- Questions Answered: {self.state.questions_asked}
- Correct Answers: {self.state.correct_answers}
- Accuracy: {self.state.correct_answers/max(self.state.questions_asked, 1)*100:.1f}%
"""
    
    def _explain_concept(self, user_input: str) -> str:
        """Explain a concept"""
        parts = user_input.split()
        if len(parts) < 2:
            return "Please specify a concept, e.g., 'explain consideration'"
        
        concept_query = ' '.join(parts[1:])
        
        # Try to find matching concept
        for concept in self.bar_tutor.kg.nodes.values():
            if concept_query in concept.name.lower() or concept_query in concept.concept_id:
                return f"""
{concept.name}

Rule: {concept.rule_statement}

Elements: {', '.join(concept.elements) if concept.elements else 'N/A'}

Common Traps: {concept.common_traps[0] if concept.common_traps else 'N/A'}
"""
        
        return f"Concept '{concept_query}' not found. Try 'help' for available topics."
    
    def _end_session(self) -> str:
        """End session"""
        self.state.session_started = False
        return "Session ended. Good luck on the bar exam!"

# ==================== MAIN TUTOR ====================

class BarExamTutor:
    """Main unified bar exam tutor"""
    
    def __init__(self, api_key: str = None):
        logger.info("Initializing Unified Bar Exam Tutor v4.0")

        self.api_key = api_key
        self.model = DEFAULT_MODEL
        
        self.kg = LegalKnowledgeGraph()
        self.practice_engine = InterleavedPracticeEngine(self.kg)
        self.tracker = PerformanceTracker()
        self.interactive = InteractiveBarTutor(self)
        
        logger.info("Tutor initialized successfully")
    
    def generate_interleaved_practice(self, subject: str, count: int = 5) -> List[KnowledgeNode]:
        """Generate interleaved practice"""
        print(f"\nGenerating Interleaved Practice - {subject.upper()}")
        print("="*70)
        
        concepts = self.practice_engine.generate_practice(subject, count)
        
        if not concepts:
            print(f"\nNo concepts found for: {subject}")
            print("Available: contracts, torts, evidence, constitutional_law, criminal_law, civil_procedure\n")
            return []
        
        self.practice_engine.display_practice(concepts)
        return concepts
    
    def explain_concept(self, concept_id: str):
        """Explain legal concept"""
        concept = self.kg.get_concept(concept_id)
        
        if not concept:
            print(f"\nConcept '{concept_id}' not found.\n")
            return
        
        print(f"\n{'='*70}")
        print(f"{concept.name.upper()}")
        print(f"{'='*70}\n")
        
        print(f"Subject: {concept.subject.title()}")
        print(f"Difficulty: {concept.difficulty}/5\n")
        print(f"Rule: {concept.rule_statement}\n")
        
        if concept.elements:
            print("Elements:")
            for i, elem in enumerate(concept.elements, 1):
                print(f"  {i}. {elem}")
            print()
        
        if concept.common_traps:
            print("Common Traps:")
            for trap in concept.common_traps:
                print(f"  - {trap}")
            print()
        
        print(f"{'='*70}\n")
    
    def start_interactive_mode(self):
        """Start interactive conversational mode"""
        print("\n" + "="*70)
        print("INTERACTIVE TUTOR MODE")
        print("="*70)
        
        subject = input("\nChoose subject (contracts/torts/evidence/etc): ").strip().lower()
        if not subject:
            subject = "contracts"
        
        print(self.interactive.start_session(subject))
        
        while self.interactive.state.session_started:
            try:
                user_input = input("\n> ").strip()
                if not user_input:
                    continue
                
                response = self.interactive.process_input(user_input)
                print(f"\n{response}")
                
            except KeyboardInterrupt:
                print("\n\nExiting interactive mode...")
                break
            except Exception as e:
                logger.error(f"Error: {e}", exc_info=True)
                print(f"Error: {e}")
    
    def run_menu(self):
        """Main menu"""
        print("\n" + "="*70)
        print("BAR EXAM TUTOR v4.0 - Unified System")
        print("="*70)
        
        while True:
            print("\n" + "-"*70)
            print("MAIN MENU")
            print("-"*70)
            print("1. Interleaved Practice")
            print("2. Explain Concept")
            print("3. Performance Dashboard")
            print("4. Interactive Mode (Conversational)")
            print("0. Exit")
            print("-"*70)
            
            choice = input("\nSelect: ").strip()
            
            try:
                if choice == "0":
                    print("\nGood luck on your bar exam!")
                    break
                elif choice == "1":
                    self._interleaved_menu()
                elif choice == "2":
                    self._explain_menu()
                elif choice == "3":
                    self.tracker.display_dashboard()
                elif choice == "4":
                    self.start_interactive_mode()
                else:
                    print("Invalid choice")
            
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                logger.error(f"Error: {e}", exc_info=True)
                print(f"Error: {e}")
    
    def _interleaved_menu(self):
        """Interleaved practice menu"""
        print("\nAvailable subjects:")
        print("  - contracts")
        print("  - torts")
        print("  - evidence")
        print("  - constitutional_law")
        print("  - criminal_law")
        print("  - civil_procedure")
        
        subject = input("\nEnter subject: ").strip().lower()
        count = input("Number of concepts (3-10): ").strip()
        
        try:
            count = int(count) if count else 5
            count = max(3, min(10, count))
            self.generate_interleaved_practice(subject, count)
        except ValueError:
            print("Invalid number, using default: 5")
            self.generate_interleaved_practice(subject, 5)
    
    def _explain_menu(self):
        """Explain concept menu"""
        print("\nExample concept IDs:")
        print("  - contracts_offer")
        print("  - contracts_consideration")
        print("  - torts_negligence")
        print("  - evidence_hearsay")
        
        concept_id = input("\nEnter concept ID: ").strip()
        if concept_id:
            self.explain_concept(concept_id)

# ==================== MAIN ====================

def main():
    """Main entry point"""
    try:
        # Initialize directories
        NOTES_DIR.mkdir(exist_ok=True)
        BACKUP_DIR.mkdir(exist_ok=True)
        
        # Load environment
        if ENV_PATH.exists():
            load_dotenv(ENV_PATH)
            api_key = os.getenv("OPENAI_API_KEY")
        else:
            api_key = None
        
        # Create tutor
        tutor = BarExamTutor(api_key=api_key)
        
        # Run menu
        tutor.run_menu()
    
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
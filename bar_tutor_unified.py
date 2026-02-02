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

# Import advanced pedagogy features
from advanced_pedagogy import (
    AdvancedPedagogyEngine,
    LearningMode,
    CognitiveStrategy,
    StudySession
)

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
    """Current state of the interactive learning session with advanced pedagogy"""
    current_subject: str = "contracts"
    current_concept: Optional[str] = None
    session_started: bool = False
    questions_asked: int = 0
    correct_answers: int = 0
    current_difficulty: str = "intermediate"
    learning_mode: str = "guided"
    user_responses: List[Dict] = field(default_factory=list)
    last_interaction: Optional[datetime] = None
    # Advanced pedagogy fields
    confidence_ratings: List[int] = field(default_factory=list)  # 1-5 scale
    current_question: Optional[Dict] = None
    awaiting_answer: bool = False
    awaiting_confidence: bool = False
    session_id: str = ""
    cognitive_strategies_used: List[str] = field(default_factory=list)
    elaboration_mode: bool = False  # Deep thinking prompts after answers

# ==================== KNOWLEDGE GRAPH ====================

class LegalKnowledgeGraph:
    """Comprehensive legal knowledge - 112 concepts across 8 subjects"""

    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self._initialize_all_subjects()

    def _initialize_all_subjects(self):
        """Initialize all 14 subjects - Complete Iowa Bar (331 concepts: 180 MBE + 151 Essay)"""
        # Core concepts (112)
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_criminal_procedure()
        self._initialize_civil_procedure()
        self._initialize_evidence()
        self._initialize_real_property()
        
        # Full expansion (70 additional concepts)
        self._add_contracts_expansion()
        self._add_torts_expansion()
        self._add_constitutional_law_expansion()
        self._add_criminal_law_expansion()
        self._add_criminal_procedure_expansion()
        self._add_civil_procedure_expansion()
        self._add_evidence_expansion()
        self._add_real_property_expansion()

        # Essay Subjects (151 concepts) - Initialize once only
        self._initialize_professional_responsibility()
        self._initialize_corporations()
        self._initialize_wills_trusts_estates()
        self._initialize_family_law()
        self._initialize_secured_transactions()
        self._initialize_iowa_procedure()
        self._initialize_business_associations()

        # Extended Constitutional Law (NCBE Coverage)
        self._add_ncbe_constitutional_law()

        logger.info(f"Knowledge graph initialized with {len(self.nodes)} concepts")

# Ultimate Expanded Knowledge Base - 112+ Concepts
# Each subject has 14+ concepts at Real Property richness level

    def _initialize_civil_procedure(self):
        """Initialize civil_procedure - 14 comprehensive concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="civil_procedure_jurisdiction_and_venue",
                name="Jurisdiction & Venue",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "General vs specific jurisdiction",
                    "minimum contacts",
                    "domicile",
                ],
                # Mnemonic: PISSED
            ),
            KnowledgeNode(
                concept_id="civil_procedure_pleadings_and_motions",
                name="Pleadings & Motions",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Twiqbal plausibility",
                    "relation back",
                    "waiver of defenses.",
                ],
                # Mnemonic: CLAIMS
            ),
            KnowledgeNode(
                concept_id="civil_procedure_joinder_and_discovery",
                name="Joinder & Discovery",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Compulsory counterclaims",
                    "indispensable parties",
                    "discovery sanctions.",
                ],
                # Mnemonic: JEDI
            ),
            KnowledgeNode(
                concept_id="civil_procedure_pretrial_and_trial",
                name="Pretrial & Trial",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic'],
                policy_rationales=[],
                common_traps=[],
                # Mnemonic: LIMES
            ),
            KnowledgeNode(
                concept_id="civil_procedure_judgments_and_preclusion",
                name="Judgments & Preclusion",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Same parties/privity",
                    "mutual vs non-mutual collateral estoppel",
                    "full faith and credit",
                ],
                # Mnemonic: RICE
            ),
            KnowledgeNode(
                concept_id="civil_procedure_subjectmatter_jurisdiction",
                name="SUBJECT-MATTER JURISDICTION",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Federal courts need subject-matter jurisdiction via federal question, diversity exceeding $75,000 with complete diversity, or supplemental claims sharing common nucleus with anchor.",
                elements=['Federal Question', 'Diversity', 'Supplemental Jurisdiction', 'Removal/Remand'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_personal_jurisdiction",
                name="PERSONAL JURISDICTION",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="State court exercises personal jurisdiction where statute authorizes and Due Process satisfied through minimum contacts, purposeful availment, foreseeability, and fairness plus notice.",
                elements=['Long-Arm Statutes', 'Traditional Bases', 'Specific Jurisdiction', 'Fair Play Factors'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_subject_matter_jurisdiction__federal_question",
                name="Subject Matter Jurisdiction - Federal Question",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Claim arises under federal law",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_subject_matter_jurisdiction__diversity",
                name="Subject Matter Jurisdiction - Diversity",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Complete diversity + $75K",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_personal_jurisdiction__minimum_contacts",
                name="Personal Jurisdiction - Minimum Contacts",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Purposeful availment required",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_personal_jurisdiction__fair_play",
                name="Personal Jurisdiction - Fair Play",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Burden, forum interest, efficiency",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_service_of_process",
                name="Service of Process",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Proper notice required for jurisdiction",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_pleading_standard__twombly",
                name="Pleading Standard - Twombly",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Plausible claim, not mere possibility",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_summary_judgment",
                name="Summary Judgment",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="No genuine dispute of material fact",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_constitutional_law(self):
        """Initialize constitutional_law - 14 comprehensive concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="constitutional_law_judicial_power_and_justiciability",
                name="Judicial Power & Justiciability",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Case-or-controversy requirement demands standing (injury, causation, redressability), ripeness, and absence of mootness or political questions.",
                elements=['Rule', 'Mnemonic', 'Visual', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Taxpayer standing (usually none)",
                    "generalized grievances",
                    "mootness exceptions (e.g.",
                ],
                # Mnemonic: SCRAM
            ),
            KnowledgeNode(
                concept_id="constitutional_law_federal_legislative_power",
                name="Federal Legislative Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Congress operates within enumerated powers; Commerce Clause covers channels, instrumentalities, and substantial economic effects; Necessary & Proper clause implements enumerated powers.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Intrastate non-economic activity (Lopez)",
                    "attenuated chains under substantial-effects theory",
                    "anti-commandeering (New York v. US)",
                ],
                # Mnemonic: Can People Truly Win Now?
            ),
            KnowledgeNode(
                concept_id="constitutional_law_executive_power",
                name="Executive Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Presidential power peaks with congressional authorization, declines in twilight zones, bottomed out when defying Congress.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Executive agreements = binding without Senate",
                    "removal limits for independent agencies",
                    "pardon excludes impeachment",
                ],
                # Mnemonic: VETO PACT
            ),
            KnowledgeNode(
                concept_id="constitutional_law_federalism_and_state_power",
                name="Federalism & State Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Tenth Amendment reserves unenumerated powers; Supremacy Clause preempts conflicts; dormant Commerce Clause prevents discriminatory burdens; states cannot tax the federal government.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Facial neutrality with discriminatory effect",
                    "Article IV Privileges & Immunities limited to citizens",
                    "federal commandeering of states",
                ],
                # Mnemonic: DORM ROOM
            ),
            KnowledgeNode(
                concept_id="constitutional_law_individual_rights",
                name="Individual Rights",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Procedural DP requires notice + hearing for life/liberty/property; substantive DP protects fundamental rights via strict scrutiny, otherwise rational basis.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "At-will employment lacks property interest",
                    "stigma-plus requirement",
                    "emergency exceptions for hearings",
                ],
                # Mnemonic: MR. FIG CAP
            ),
            KnowledgeNode(
                concept_id="constitutional_law_equal_protection",
                name="Equal Protection",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Classification triggers scrutiny: suspect (strict), quasi-suspect (intermediate), others (rational basis); fundamental rights also trigger strict scrutiny.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Need discriminatory intent",
                    "federal alienage uses rational basis",
                    "affirmative action strict scrutiny",
                ],
                # Mnemonic: RAN GIL
            ),
            KnowledgeNode(
                concept_id="constitutional_law_first_amendment",
                name="First Amendment",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Content-based regulations = strict scrutiny; content-neutral TPM = intermediate; unprotected categories include incitement, obscenity, fighting words, true threats, child pornography.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Incitement requires imminence",
                    "fighting words must be face-to-face",
                    "prior restraint presumption",
                ],
                # Mnemonic: FOCI
            ),
            KnowledgeNode(
                concept_id="constitutional_law_federal_powers_and_supremacy",
                name="FEDERAL POWERS & SUPREMACY",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Congress legislates through enumerated powers, Necessary and Proper Clause, Commerce channels or substantial effects, while Supremacy Clause preempts conflicting state actions within enumerated sphere",
                elements=['Enumerated Powers', 'Commerce Authority', 'Preemption', 'Tenth Amendment Limits'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_individual_rights_and_scrutiny",
                name="INDIVIDUAL RIGHTS & SCRUTINY",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Government action triggering individual rights receives strict, intermediate, or rational basis scrutiny depending on classification or burden, requiring tailored means and adequate governmental objec",
                elements=['State Action', 'Fundamental Rights', 'Equal Protection', 'Speech Regulation'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_commerce_clause__channels",
                name="Commerce Clause - Channels",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Congress can regulate channels of commerce",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_commerce_clause__instrumentalities",
                name="Commerce Clause - Instrumentalities",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Regulation of instrumentalities",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_commerce_clause__substantial_effects",
                name="Commerce Clause - Substantial Effects",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Economic activity affecting commerce",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_necessary_and_proper",
                name="Necessary and Proper",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Means rationally related to enumerated power",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_dormant_commerce_clause",
                name="Dormant Commerce Clause",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="States cannot discriminate against interstate commerce",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_contracts(self):
        """Initialize contracts - 14 comprehensive concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="contracts_formation",
                name="Formation",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Advertisements (invitations)",
                    "UCC firm offers",
                    "mailbox rule twists",
                ],
                # Mnemonic: FOCI
            ),
            KnowledgeNode(
                concept_id="contracts_terms_and_interpretation",
                name="Terms & Interpretation",
                subject="contracts",
                difficulty=3,
                rule_statement="Common law mirror-image; UCC gap fillers; parol evidence.",
                elements=['Rule', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Battle of forms",
                    "parol evidence exceptions (ambiguity",
                    "fraud)",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_performance_and_breach",
                name="Performance & Breach",
                subject="contracts",
                difficulty=3,
                rule_statement="Common law substantial performance vs material breach; UCC perfect tender.",
                elements=['Rule', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Anticipatory repudiation (reasonable assurances)",
                    "divisible contracts",
                    "condition precedent vs subsequent.",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_remedies",
                name="Remedies",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Foreseeability (Hadley)",
                    "mitigation duties",
                    "liquidated damages (reasonable estimate",
                ],
                # Mnemonic: ERRS
            ),
            KnowledgeNode(
                concept_id="contracts_defenses",
                name="Defenses",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "SOF partial performance exceptions",
                    "mutual mistake vs unilateral",
                    "impossibility vs frustration.",
                ],
                # Mnemonic: STUPID
            ),
            KnowledgeNode(
                concept_id="contracts_thirdparty_rights",
                name="Third-Party Rights",
                subject="contracts",
                difficulty=3,
                rule_statement="Assignments, delegations, third-party beneficiaries.",
                elements=['Rule', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Revocation of gratuitous assignments",
                    "delegation of special skills",
                    "vesting of third-party rights.",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_ucc_delivery_title_and_risk_of_loss",
                name="UCC Delivery, Title & Risk of Loss",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Hierarchy', 'Shipment vs Destination', 'No Carrier', 'Casualty to Identified Goods', 'Entrustment & Voidable Title'],
                policy_rationales=[],
                common_traps=[
                    "Breach always keeps risk on breaching party; “FOB plant” is shipment",
                    "not destination; merchant receipt requirement.",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_acceptance_rejection_and_revocation_ucc",
                name="Acceptance, Rejection & Revocation (UCC)",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Acceptance', 'Rejection', 'Revocation of Acceptance', 'Adequate Assurances', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Using goods extensively after discovering defect can bar revocation; COD shipments limit inspection ",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_excuse_impossibility_impracticability_frustration",
                name="Excuse: Impossibility, Impracticability, Frustration",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Impossibility / Impracticability', 'Partial Impracticability', 'Frustration of Purpose', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Mere increased cost insufficient unless extreme; assuming price fluctuation risk defeats excuse.",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_modification_accord_and_satisfaction_novation",
                name="Modification, Accord & Satisfaction, Novation",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Modification', 'Accord & Satisfaction', 'Novation', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Modification of firm offer beyond three months requires fresh consideration; distinguishing novation",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_warranties_ucc_and_common",
                name="Warranties (UCC & Common)",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Express', 'Implied Warranty of Merchantability', 'Implied Warranty of Fitness', 'Disclaimers', 'Limitations'],
                policy_rationales=[],
                common_traps=[
                    "Statements of opinion/puffery not express warranties; “as is” doesn’t negate express warranties; lim",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_offer_acceptance_consideration",
                name="OFFER, ACCEPTANCE, CONSIDERATION",
                subject="contracts",
                difficulty=3,
                rule_statement="Valid contract needs offer showing commitment, acceptance mirroring material terms, and consideration or substitute reliance creating bargained-for exchange with mutual assent and capacity.",
                elements=['Offer Dynamics', 'Acceptance Mechanics', 'Consideration', 'Formation Defenses'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="contracts_performance_breach_remedies",
                name="PERFORMANCE, BREACH, REMEDIES",
                subject="contracts",
                difficulty=3,
                rule_statement="Performance judged by strict compliance for non-UCC or perfect tender under Article 2; material breach excuses; remedies include expectation, reliance, restitution, specific performance.",
                elements=['Conditions', 'Material Breach', 'UCC Obligations', 'Remedies'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="contracts_formation__foci_checklist",
                name="FORMATION – FOCI CHECKLIST",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Option contracts (need consideration unless UCC firm offer ≤ 3 months, signed by merchant).",
                    "Mailbox rule exceptions: option, improperly addressed, rejection before acceptance.",
                    "Illusory promises not enforceable.",
                ],
                # Mnemonic: FOCI
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_criminal_law(self):
        """Initialize criminal_law - 14 comprehensive concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="criminal_law_elements_of_crimes",
                name="Elements of Crimes",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Every offense needs a voluntary act (or qualifying omission), the requisite mental state, concurrence, and causation.",
                elements=['Rule', 'Actus Reus', 'Mens Rea (MPC hierarchy)', 'Concurrence', 'Causation'],
                policy_rationales=[],
                common_traps=[
                    "Specific vs general intent (intoxication defenses)",
                    "transferred intent limited to same crime",
                    "medical negligence generally foreseeable",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_law_homicide_offenses",
                name="Homicide Offenses",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Murder = unlawful killing with malice aforethought (intent to kill, intent to seriously injure, depraved heart, felony murder). Manslaughter lacks malice.",
                elements=['Rule', 'Hierarchy', 'Felony Murder', 'Mnemonics', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Instant premeditation allowed; deadly weapon inference; felony-murder merger; cooling-off defeats vo",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_law_other_crimes_against_persons",
                name="Other Crimes Against Persons",
                subject="criminal_law",
                difficulty=3,
                rule_statement="",
                elements=['Battery', 'Assault', 'Kidnapping', 'False Imprisonment', 'Rape'],
                policy_rationales=[],
                common_traps=[
                    "Battery requires only intent to touch; assault has two theories; kidnapping needs substantial moveme",
                ],
                # Mnemonic: BARK
            ),
            KnowledgeNode(
                concept_id="criminal_law_property_crimes",
                name="Property Crimes",
                subject="criminal_law",
                difficulty=3,
                rule_statement="",
                elements=['Larceny', 'Robbery', 'Embezzlement', 'False Pretenses', 'Burglary'],
                policy_rationales=[],
                common_traps=[
                    "Intent at time of taking (larceny); assaultive felonies merge; force must accompany taking for robbe",
                ],
                # Mnemonic: LREF
            ),
            KnowledgeNode(
                concept_id="criminal_law_inchoate_crimes",
                name="Inchoate Crimes",
                subject="criminal_law",
                difficulty=3,
                rule_statement="",
                elements=['Solicitation', 'Conspiracy', 'Attempt', 'Mnemonics', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Solicitation complete without acceptance; conspiracy survives completed offense; attempt always spec",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_law_accomplice_and_accessory_liability",
                name="Accomplice & Accessory Liability",
                subject="criminal_law",
                difficulty=3,
                rule_statement="",
                elements=['Accomplice', 'Accessory After the Fact', 'Principal', 'Mnemonics', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Mere presence insufficient; dual intent requirement; accomplice liability remains even if principal ",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_law_defenses",
                name="Defenses",
                subject="criminal_law",
                difficulty=3,
                rule_statement="",
                elements=['Self-Defense', 'Defense of Others/Property/Necessity', 'Duress', 'Intoxication', 'Insanity Tests'],
                policy_rationales=[],
                common_traps=[
                    "Duress unavailable for murder; voluntary intoxication limited; entrapment fails if predisposed; mist",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_law_mens_rea_and_homicide",
                name="MENS REA & HOMICIDE",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Criminal liability requires actus reus with mens rea of purpose, knowledge, recklessness, or negligence; homicide classifications depend on malice aforethought, intent, depraved heart, felony murder.",
                elements=['Mens Rea Levels', 'Murder', 'Manslaughter', 'Defenses'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_law_actus_reus",
                name="Actus Reus",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Voluntary act or omission with legal duty",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_law_mens_rea__purpose",
                name="Mens Rea - Purpose",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Conscious objective to cause result",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_law_mens_rea__knowledge",
                name="Mens Rea - Knowledge",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Awareness of conduct and circumstances",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_law_felony_murder",
                name="Felony Murder",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Killing during inherently dangerous felony",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_law_voluntary_manslaughter",
                name="Voluntary Manslaughter",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Intentional killing with adequate provocation",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_law_larceny",
                name="Larceny",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Trespassory taking and carrying away with intent to steal",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_criminal_procedure(self):
        """Initialize criminal_procedure - 14 comprehensive concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="criminal_procedure_fourth_amendment",
                name="Fourth Amendment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Traps'],
                policy_rationales=[],
                common_traps=[
                    "Standing (expectation of privacy)",
                    "private search doctrine",
                    "warrant particularity",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_exclusionary_rule",
                name="Exclusionary Rule",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Impeachment use",
                    "Miranda violations (non-Miranda statements may be used for impeachment)",
                    "attenuation factors.",
                ],
                # Mnemonic: FISSURE
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_fifth_amendment",
                name="Fifth Amendment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Traps'],
                policy_rationales=[],
                common_traps=[
                    "Ambiguous requests",
                    "re-initiation by suspect",
                    "public-safety exception",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_sixth_amendment",
                name="Sixth Amendment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Offense-specific attachment",
                    "deliberate elicitation",
                    "Massiah",
                ],
                # Mnemonic: PACED
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_search_seizure_statements",
                name="SEARCH, SEIZURE, STATEMENTS",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Fourth Amendment protects reasonable expectations of privacy; warrants need probable cause and particularity; exclusionary rule suppressed violations; Fifth and Sixth regulate interrogation, counsel, ",
                elements=['Standing', 'Warrant Exceptions', 'Exclusionary Limits', 'Interrogations'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_standing__fourth_amendment",
                name="Standing - Fourth Amendment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Reasonable expectation of privacy required",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_probable_cause",
                name="Probable Cause",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Fair probability evidence of crime exists",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_search_incident_to_arrest",
                name="Search Incident to Arrest",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Contemporaneous search of person and wingspan",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_automobile_exception",
                name="Automobile Exception",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Warrantless search with probable cause and mobility",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_plain_view_doctrine",
                name="Plain View Doctrine",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Seizure if lawfully present and incriminating evident",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_miranda_custody",
                name="Miranda Custody",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Reasonable person would not feel free to leave",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_miranda_invocation",
                name="Miranda Invocation",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Unambiguous request for counsel or silence",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_sixth_amendment_attachment",
                name="Sixth Amendment Attachment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Right to counsel attaches at formal charges",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_deliberate_elicitation",
                name="Deliberate Elicitation",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Officers cannot elicit statements after charges",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_evidence(self):
        """Initialize evidence - 14 comprehensive concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="evidence_relevance",
                name="Relevance",
                subject="evidence",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps', 'Preliminary Questions (FRE 104)', 'Limiting Instructions (FRE 105)', 'Rule of Completeness (FRE 106)'],
                policy_rationales=[],
                common_traps=[
                    "Subsequent remedial measures",
                    "settlements",
                    "offers to pay medical expenses",
                ],
                # Mnemonic: 403 Balance
            ),
            KnowledgeNode(
                concept_id="evidence_character_evidence",
                name="Character Evidence",
                subject="evidence",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic'],
                policy_rationales=[],
                common_traps=[],
                # Mnemonic: CRIME
            ),
            KnowledgeNode(
                concept_id="evidence_hearsay",
                name="Hearsay",
                subject="evidence",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Key Exceptions', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Double hearsay",
                    "testimonial statements confronting (Crawford)",
                    "former testimony requirements.",
                ],
                # Mnemonic: HEARSAY
            ),
            KnowledgeNode(
                concept_id="evidence_witnesses_and_impeachment",
                name="Witnesses & Impeachment",
                subject="evidence",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Collateral matters",
                    "prior consistent vs inconsistent statements",
                    "confrontation Clause for testimonial hearsay.",
                ],
                # Mnemonic: PC FARMS
            ),
            KnowledgeNode(
                concept_id="evidence_privileges_and_policy",
                name="Privileges & Policy",
                subject="evidence",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps', 'Best Evidence Flex', 'Digital Authentication', 'Updated Prior Consistent Statements'],
                policy_rationales=[],
                common_traps=[
                    "Spousal privileges scope",
                    "waiver by presence of third parties",
                    "work-product doctrine",
                ],
                # Mnemonic: CLAPS
            ),
            KnowledgeNode(
                concept_id="evidence_relevance_and_character",
                name="RELEVANCE & CHARACTER",
                subject="evidence",
                difficulty=3,
                rule_statement="Evidence must be relevant, probative value not outweighed by unfair prejudice; character evidence limited except for habit, impeachment, or cases placing character at issue.",
                elements=['Rule 403', 'Character Evidence', 'Other Acts', 'Impeachment'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="evidence_hearsay_and_exceptions",
                name="HEARSAY & EXCEPTIONS",
                subject="evidence",
                difficulty=3,
                rule_statement="Hearsay is out-of-court statement offered for truth, inadmissible absent exemption or exception such as opposing party statements, present sense impression, excited utterance, business records.",
                elements=['Non-Hearsay Uses', 'Exemptions', 'Unavailable Declarant', 'Reliability Exceptions'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="evidence_hearsay_definition",
                name="Hearsay Definition",
                subject="evidence",
                difficulty=3,
                rule_statement="Out-of-court statement offered for truth",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="evidence_present_sense_impression",
                name="Present Sense Impression",
                subject="evidence",
                difficulty=3,
                rule_statement="Statement describing event while perceiving it",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="evidence_excited_utterance",
                name="Excited Utterance",
                subject="evidence",
                difficulty=3,
                rule_statement="Statement under stress of startling event",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="evidence_business_records",
                name="Business Records",
                subject="evidence",
                difficulty=3,
                rule_statement="Records kept in regular course of business",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="evidence_character_evidence__criminal",
                name="Character Evidence - Criminal",
                subject="evidence",
                difficulty=3,
                rule_statement="Defendant may open door to character evidence",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="evidence_impeachment__prior_inconsistent",
                name="Impeachment - Prior Inconsistent",
                subject="evidence",
                difficulty=3,
                rule_statement="Prior statements to attack credibility",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="evidence_authentication",
                name="Authentication",
                subject="evidence",
                difficulty=3,
                rule_statement="Evidence must be authenticated before admission",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_real_property(self):
        """Initialize real_property - 14 comprehensive concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="real_property_estates_and_future_interests",
                name="ESTATES & FUTURE INTERESTS",
                subject="real_property",
                difficulty=3,
                rule_statement="Present estates include fee simple, life estates, and leaseholds; future interests vest in grantor or third parties subject to RAP, waste, and defeasibility doctrines.",
                elements=['Fee Estates', 'Life Estates', 'Future Interests', 'RAP Analysis'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="real_property_conveyancing_and_recording",
                name="CONVEYANCING & RECORDING",
                subject="real_property",
                difficulty=3,
                rule_statement="Valid conveyance needs competent grantor, executed deed, delivery, and acceptance; recording acts protect bona fide purchasers without notice who record first depending on statute type.",
                elements=['Deed Formalities', 'Notice Types', 'Recording Acts', 'Chain Issues'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="real_property_estates_and_future_interests",
                name="ESTATES & FUTURE INTERESTS",
                subject="real_property",
                difficulty=3,
                rule_statement="Present possessory estates include fee simple absolute, defeasible fees, and life estates; future interests include reversions, remainders, and executory interests that must satisfy RAP.",
                elements=['Fee Simple Absolute', 'Life Estates', 'Defeasible Fees', 'Future Interests', 'Rule Against Perpetuities (RAP)'],
                policy_rationales=[],
                common_traps=[
                    "AUTO vs. MANUAL: Determinable = AUTOmatic (like autopilot); Condition Subsequent = MANUAL reentry (l",
                    "REMAINDER RULE: Remainders are like train passengers - they wait for their turn, never jump ahead (n",
                    "RAP TRAP: 21 years + lives in being = drinking age (21) + pregnancy (gestation)",
                ],
                # Mnemonic: PREFUR
            ),
            KnowledgeNode(
                concept_id="real_property_conveyancing_and_recording",
                name="CONVEYANCING & RECORDING",
                subject="real_property",
                difficulty=3,
                rule_statement="Recording statutes protect bona fide purchasers; race-notice is majority rule, requiring timely recordation without notice of prior interests.",
                elements=['Deed Types', 'Marketable Title', 'Title Insurance', 'After-Acquired Title', 'Recording Acts'],
                policy_rationales=[],
                common_traps=[
                    "BFP = Good Faith Penny: Bona fide purchaser needs good faith + value (even $1) + no notice",
                    "Chain Gang: Must examine entire chain of title, not just immediate grantor (like prison chain gang -",
                    "Triple Notice Threat: Actual (you know) + Constructive (recorded) + Inquiry (should have known)",
                ],
                # Mnemonic: RACE to the Courthouse
            ),
            KnowledgeNode(
                concept_id="real_property_easements_servitudes_and_licenses",
                name="EASEMENTS, SERVITUDES & LICENSES",
                subject="real_property",
                difficulty=3,
                rule_statement="Easements create rights to use another's land; appurtenant easements run with land, in gross are personal; licenses are revocable permissions.",
                elements=['Appurtenant Easements', 'Easements in Gross', 'Affirmative Easements', 'Negative Easements', 'Creation Methods'],
                policy_rationales=[],
                common_traps=[],
                # Mnemonic: EASE
            ),
            KnowledgeNode(
                concept_id="real_property_concurrent_ownership",
                name="CONCURRENT OWNERSHIP",
                subject="real_property",
                difficulty=3,
                rule_statement="Joint tenancy requires four unities; tenancy in common has no survivorship; tenancy by entirety protects marital property from separate creditors.",
                elements=['Joint Tenancy', 'Tenancy in Common', 'Tenancy by Entirety', 'Severance', 'Partition'],
                policy_rationales=[],
                common_traps=[],
                # Mnemonic: TIE
            ),
            KnowledgeNode(
                concept_id="real_property_landlordtenant_law",
                name="LANDLORD-TENANT LAW",
                subject="real_property",
                difficulty=3,
                rule_statement="Landlord must maintain habitable premises; tenant must pay rent; holdover becomes periodic tenancy; self-help eviction is illegal in most states.",
                elements=['Implied Warranty of Habitability', 'Quiet Enjoyment', 'Retaliatory Evictions', 'Security Deposits', 'Assignment vs. Sublease'],
                policy_rationales=[],
                common_traps=[],
                # Mnemonic: RENT
            ),
            KnowledgeNode(
                concept_id="real_property_mortgages_foreclosure_and_priority",
                name="MORTGAGES, FORECLOSURE & PRIORITY",
                subject="real_property",
                difficulty=3,
                rule_statement="Mortgage creates security interest; foreclosure terminates mortgagor's equity; purchase money mortgages have super-priority over later liens on same collateral.",
                elements=['Mortgage vs. Deed of Trust', 'Foreclosure Process', 'Deficiency Judgments', 'Due-on-Sale Clauses', 'Purchase Money Priority'],
                policy_rationales=[],
                common_traps=[],
                # Mnemonic: MORT
            ),
            KnowledgeNode(
                concept_id="real_property_zoning_and_takings",
                name="ZONING & TAKINGS",
                subject="real_property",
                difficulty=3,
                rule_statement="Zoning regulates land use; takings require just compensation; variance is exception to zoning rules for hardship; exactions must be roughly proportional.",
                elements=['Zoning Ordinances', 'Variances & Special Permits', 'Physical vs. Regulatory Takings', 'Exactions', 'Inverse Condemnation'],
                policy_rationales=[],
                common_traps=[],
                # Mnemonic: ZONE
            ),
            KnowledgeNode(
                concept_id="real_property_adverse_possession",
                name="ADVERSE POSSESSION",
                subject="real_property",
                difficulty=3,
                rule_statement="Hostile, actual, exclusive, continuous possession for statutory period perfects title; color of title reduces period to 7 years.",
                elements=['Elements Required', 'Color of Title', 'Tacking', 'Disabilities', 'Boundary Disputes'],
                policy_rationales=[],
                common_traps=[],
                # Mnemonic: HATE
            ),
            KnowledgeNode(
                concept_id="real_property_fixtures",
                name="FIXTURES",
                subject="real_property",
                difficulty=3,
                rule_statement="Personal property becomes real property when permanently attached with intent to improve the realty; trade fixtures remain personal property.",
                elements=['FIX Test', 'Trade Fixtures', 'Mortgage Rights', 'Severance', 'Agricultural Fixtures'],
                policy_rationales=[],
                common_traps=[],
                # Mnemonic: FIX
            ),
            KnowledgeNode(
                concept_id="real_property_easement_by_necessity",
                name="Easement by Necessity",
                subject="real_property",
                difficulty=3,
                rule_statement="Implied easement when landlocked",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="real_property_easement_by_prescription",
                name="Easement by Prescription",
                subject="real_property",
                difficulty=3,
                rule_statement="Open, notorious, continuous adverse use",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="real_property_covenant__touch_and_concern",
                name="Covenant - Touch and Concern",
                subject="real_property",
                difficulty=3,
                rule_statement="Burden/benefit must relate to land use",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="real_property_water_rights",
                name="Water Rights",
                subject="real_property",
                difficulty=3,
                rule_statement="Riparian rights attach to land bordering watercourse; prior appropriation follows first in time first in right",
                elements=['Riparian rights', 'Prior appropriation', 'Surface water', 'Groundwater'],
                policy_rationales=[],
                common_traps=[
                    "Mixing riparian and prior appropriation systems",
                    "Forgetting reasonable use doctrine",
                ],
            ),
            KnowledgeNode(
                concept_id="real_property_nuisance",
                name="Nuisance",
                subject="real_property",
                difficulty=3,
                rule_statement="Private nuisance is substantial unreasonable interference with use and enjoyment of land; public nuisance affects community",
                elements=['Private nuisance', 'Public nuisance', 'Coming to nuisance', 'Remedies'],
                policy_rationales=[],
                common_traps=[
                    "Confusing trespass and nuisance",
                    "Forgetting balancing test for unreasonableness",
                ],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

# Full MBE Expansion - Additional Concepts
# Adds 58-98 concepts for complete NCBE coverage

    def _add_civil_procedure_expansion(self):
        """Add 7 additional civil_procedure concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="civil_procedure_venue",
                name="Venue & Transfer",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Venue proper where defendant resides, events occurred, or property located; transfer for convenience or interest of justice",
                elements=['Proper venue', '§1404(a) transfer', '§1406 improper venue transfer', 'Forum non conveniens'],
                policy_rationales=[],
                common_traps=['Confusing venue with personal jurisdiction', 'Forgetting §1404(a) requires proper venue initially', "Missing that transferee court applies transferor's choice of law"],
                # Mnemonic: VET: Venue, Events, Transfer
            ),
            KnowledgeNode(
                concept_id="civil_procedure_joinder_claims",
                name="Joinder of Claims",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Party may join as many claims as they have against opposing party under Rule 18; no need for relation",
                elements=['Permissive joinder', 'Rule 18 - unlimited', 'Subject matter jurisdiction required', 'Supplemental jurisdiction'],
                policy_rationales=[],
                common_traps=["Thinking claims must be related (they don't under Rule 18)", 'Forgetting each claim needs independent SMJ or supplemental', 'Confusing claim joinder with party joinder'],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_counterclaims",
                name="Counterclaims & Cross-claims",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Compulsory counterclaim arises from same transaction; permissive does not; cross-claims must arise from same transaction",
                elements=['Compulsory counterclaim', 'Permissive counterclaim', 'Cross-claims', 'Same transaction test'],
                policy_rationales=[],
                common_traps=['Missing that compulsory counterclaim is waived if not asserted', 'Forgetting cross-claims are always permissive', 'Confusing counterclaim with setoff'],
                # Mnemonic: CCC: Compulsory, Cross, Claims
            ),
            KnowledgeNode(
                concept_id="civil_procedure_class_actions",
                name="Class Actions",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Class action requires numerosity, commonality, typicality, adequate representation, plus Rule 23(b) category",
                elements=['Numerosity', 'Commonality', 'Typicality', 'Adequate representation', 'Rule 23(b) types'],
                policy_rationales=[],
                common_traps=['Forgetting notice required for Rule 23(b)(3) damages classes', 'Missing that class members can opt out only in (b)(3)', 'Confusing certification with merits determination'],
                # Mnemonic: NCTA: Numerosity, Commonality, Typicality, Adequate rep
            ),
            KnowledgeNode(
                concept_id="civil_procedure_res_judicata_detailed",
                name="Res Judicata (Claim Preclusion)",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Valid final judgment on merits precludes same parties from relitigating same claim or any part that could have been litigated",
                elements=['Valid judgment', 'Final on merits', 'Same claim', 'Same parties or in privity'],
                policy_rationales=['Finality and repose', 'Prevent harassment', 'Judicial efficiency'],
                common_traps=['Forgetting dismissal for lack of jurisdiction is not on merits', 'Missing that voluntary dismissal without prejudice is not preclusive', 'Applying res judicata when issue preclusion should apply'],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_discovery_sanctions",
                name="Discovery Sanctions",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Court may impose sanctions for discovery violations, from costs to dismissal or default judgment",
                elements=['Rule 37 sanctions', 'Good faith requirement', 'Proportionality', 'Protective orders'],
                policy_rationales=[],
                common_traps=['Forgetting meet-and-confer requirement before motion', 'Missing that dismissal/default are harsh sanctions requiring willfulness', 'Not considering less severe sanctions first'],
            ),
            KnowledgeNode(
                concept_id="civil_procedure_erie_doctrine",
                name="Erie Doctrine Applications",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Federal courts in diversity apply state substantive law but federal procedural law; outcome determinative if no valid FRCP",
                elements=['Substantive vs procedural', 'Outcome determinative test', 'Rules Enabling Act', 'Twin aims of Erie'],
                policy_rationales=[],
                common_traps=['Assuming all procedural issues are federal', 'Forgetting valid FRCP trumps conflicting state law', 'Missing that statute of limitations is substantive'],
                # Mnemonic: SOAP: Substantive vs Outcome vs Act vs Procedural
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _add_constitutional_law_expansion(self):
        """Add 7 additional constitutional_law concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="constitutional_law_state_action",
                name="State Action Doctrine",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Constitutional rights apply only to government action; private conduct becomes state action through public function, entanglement, or encouragement",
                elements=['Public function test', 'Entanglement', 'Nexus/encouragement', 'Exclusive public function'],
                policy_rationales=['Protect individual liberty from government overreach', 'Preserve private autonomy'],
                common_traps=['Thinking all constitutional rights apply to private parties', 'Missing that public function must be traditionally exclusively governmental', 'Forgetting mere government regulation ≠ state action'],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_dormant_commerce_clause",
                name="Dormant Commerce Clause",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="States cannot discriminate against or unduly burden interstate commerce; discrimination gets strict scrutiny, burden gets balancing",
                elements=['Discrimination analysis', 'Pike balancing test', 'Market participant exception', 'Congressional authorization'],
                policy_rationales=[],
                common_traps=['Applying dormant commerce clause when Congress has acted', 'Forgetting market participant exception', 'Missing that facially neutral laws can discriminate in effect'],
                # Mnemonic: DCC: Discriminate, Congress can override, Clause
            ),
            KnowledgeNode(
                concept_id="constitutional_law_privileges_immunities_art4",
                name="Privileges & Immunities Clause (Art IV)",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="State cannot discriminate against out-of-state citizens regarding fundamental rights unless substantial justification and no less restrictive means",
                elements=['Fundamental rights', 'Substantial justification', 'Discrimination against non-residents', 'Least restrictive means'],
                policy_rationales=[],
                common_traps=['Confusing Art IV P&I with 14th Amendment P&I', 'Applying to corporations (only applies to citizens)', 'Forgetting recreational activities not fundamental'],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_contracts_clause",
                name="Contracts Clause",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="States cannot substantially impair contracts unless reasonable and necessary to serve important public purpose",
                elements=['Substantial impairment', 'Public vs private contracts', 'Strict scrutiny for public', 'Intermediate for private'],
                policy_rationales=[],
                common_traps=['Not applying stricter scrutiny when state impairs its own contracts', 'Forgetting reasonable expectations matter', 'Missing prospective vs retroactive distinction'],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_ex_post_facto",
                name="Ex Post Facto & Bills of Attainder",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Ex post facto criminalizes past conduct or increases punishment retroactively; bills of attainder legislatively punish without trial",
                elements=['Retroactive criminalization', 'Retroactive penalty increase', 'Legislative punishment', 'Criminal only'],
                policy_rationales=[],
                common_traps=['Applying ex post facto to civil laws (criminal only)', 'Missing that increased sentencing guidelines can violate', 'Forgetting bills of attainder require specific identification'],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_executive_powers",
                name="Executive Powers",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="President has inherent powers over foreign affairs; domestic power greatest with Congressional approval, weakest when contrary to Congress",
                elements=['Youngstown framework', 'Foreign affairs power', 'Commander in Chief', 'Pardon power'],
                policy_rationales=[],
                common_traps=['Giving president unlimited domestic emergency powers', 'Forgetting treaty power shared with Senate', 'Missing limits on pardon power (impeachment, state crimes)'],
                # Mnemonic: YES: Youngstown, Executive, Senate (for treaties)
            ),
            KnowledgeNode(
                concept_id="constitutional_law_justiciability",
                name="Justiciability - Standing, Mootness, Ripeness",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Standing requires injury, causation, redressability; mootness requires live controversy; ripeness requires matured harm",
                elements=['Standing elements', 'Mootness exceptions', 'Ripeness test', 'Third-party standing'],
                policy_rationales=[],
                common_traps=['Forgetting generalized grievances lack standing', 'Missing capable of repetition yet evading review exception', 'Not applying ripeness to pre-enforcement challenges'],
                # Mnemonic: SMR: Standing, Mootness, Ripeness
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _add_contracts_expansion(self):
        """Add 12 additional contracts concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="contracts_offer_termination",
                name="Offer Termination",
                subject="contracts",
                difficulty=3,
                rule_statement="Offer terminates by rejection, counteroffer, lapse, revocation, death/incapacity, or destruction of subject matter",
                elements=['Rejection', 'Counteroffer as rejection', 'Lapse of time', 'Revocation', 'Death of offeror'],
                policy_rationales=[],
                common_traps=["Thinking inquiry is rejection (it's not)", 'Missing that counteroffer rejects but not if merchant under UCC 2-207', 'Forgetting irrevocable offers (option, firm offer, reliance)'],
                # Mnemonic: RRLD: Rejection, Revocation, Lapse, Death
            ),
            KnowledgeNode(
                concept_id="contracts_battle_of_forms_detailed",
                name="UCC §2-207 Battle of Forms",
                subject="contracts",
                difficulty=4,
                rule_statement="Definite expression of acceptance forms contract even with additional terms; between merchants, additional terms included unless material alteration, expressly limited, or objection",
                elements=['Definite expression', 'Additional vs different terms', 'Material alteration test', 'Merchant status'],
                policy_rationales=['Facilitate modern commerce', 'Avoid technical knockout rule'],
                common_traps=['Applying mirror image rule under UCC (wrong!)', 'Forgetting expressly conditional acceptance is counteroffer', 'Missing that different terms knocked out, additional terms analyzed'],
            ),
            KnowledgeNode(
                concept_id="contracts_mailbox_rule",
                name="Mailbox Rule & Exceptions",
                subject="contracts",
                difficulty=3,
                rule_statement="Acceptance effective upon dispatch unless option contract, offeror specifies receipt, or rejection sent first",
                elements=['Dispatch rule', 'Receipt rule exceptions', 'Option contracts', 'Overtaking rule'],
                policy_rationales=[],
                common_traps=['Applying mailbox to revocations (need receipt)', 'Missing that sending rejection first voids mailbox rule', "Forgetting improper dispatch doesn't get mailbox protection"],
            ),
            KnowledgeNode(
                concept_id="contracts_statute_of_frauds",
                name="Statute of Frauds",
                subject="contracts",
                difficulty=4,
                rule_statement="MYLEGS contracts must be in writing: Marriage, Year, Land, Executor, Goods $500+, Surety",
                elements=['MYLEGS categories', 'Writing requirements', 'Part performance exception', 'Merchant confirmation'],
                policy_rationales=[],
                common_traps=['Forgetting one-year is from making, not performance', "Missing that services completable within year don't need writing", 'Not applying merchant confirmation rule (UCC)'],
                # Mnemonic: MYLEGS
            ),
            KnowledgeNode(
                concept_id="contracts_parol_evidence_detailed",
                name="Parol Evidence Rule Applications",
                subject="contracts",
                difficulty=4,
                rule_statement="Completely integrated writing bars prior or contemporaneous contradictory or supplementary terms; partial integration bars only contradictory",
                elements=['Integration', 'Four corners vs contextual', 'Exceptions', 'Merger clause'],
                policy_rationales=['Protect integrity of written agreements', 'Certainty in contracting'],
                common_traps=['Thinking PER bars all extrinsic evidence (wrong - only prior/contemporaneous)', 'Missing exceptions for condition precedent, fraud, mistake', 'Not distinguishing complete vs partial integration'],
            ),
            KnowledgeNode(
                concept_id="contracts_mistake",
                name="Mistake (Mutual vs Unilateral)",
                subject="contracts",
                difficulty=3,
                rule_statement="Mutual mistake as to basic assumption allows rescission; unilateral mistake allows rescission only if known/should be known by other party",
                elements=['Mutual mistake', 'Basic assumption', 'Material effect', 'Unilateral mistake limits'],
                policy_rationales=[],
                common_traps=['Allowing rescission for mistake in value (usually no)', "Forgetting party bearing risk can't claim mistake", 'Missing that negligent mistake may still count if extreme'],
            ),
            KnowledgeNode(
                concept_id="contracts_misrepresentation",
                name="Misrepresentation & Fraud",
                subject="contracts",
                difficulty=3,
                rule_statement="Fraudulent misrepresentation makes contract voidable; requires false assertion of fact, scienter, intent to induce, justifiable reliance, harm",
                elements=['False assertion', 'Material fact', 'Scienter', 'Justifiable reliance', 'Damages'],
                policy_rationales=[],
                common_traps=['Applying fraud to mere opinions (usually not actionable)', 'Forgetting fraud in the inducement makes voidable, fraud in execution void', 'Missing that non-disclosure can be misrepresentation if duty to speak'],
            ),
            KnowledgeNode(
                concept_id="contracts_duress",
                name="Duress & Undue Influence",
                subject="contracts",
                difficulty=3,
                rule_statement="Duress by improper threat leaves no reasonable alternative; undue influence unfairly persuades party in confidential relationship",
                elements=['Improper threat', 'No reasonable alternative', 'Economic duress', 'Undue influence factors'],
                policy_rationales=[],
                common_traps=['Confusing duress with hard bargaining', 'Forgetting threat must be improper (not just pressure)', 'Missing undue influence requires confidential relationship usually'],
            ),
            KnowledgeNode(
                concept_id="contracts_impossibility_impracticability",
                name="Impossibility vs Impracticability",
                subject="contracts",
                difficulty=4,
                rule_statement="Impossibility excuses if objectively impossible; impracticability excuses if extreme unforeseen difficulty makes performance unreasonably expensive",
                elements=['Objective impossibility', 'Subjective impossibility', 'Commercial impracticability', 'Foreseeability'],
                policy_rationales=[],
                common_traps=['Excusing for subjective impossibility (e.g., bankruptcy)', 'Applying impracticability when just more expensive (need extreme)', 'Forgetting party assuming risk cannot claim impossibility'],
                # Mnemonic: PIF: Possible, Impractical, Frustrated
            ),
            KnowledgeNode(
                concept_id="contracts_frustration_purpose",
                name="Frustration of Purpose",
                subject="contracts",
                difficulty=3,
                rule_statement="Frustration excuses if supervening event destroys principal purpose and party did not assume risk",
                elements=['Principal purpose destroyed', 'Supervening event', 'Not assumed risk', 'Foreseeability'],
                policy_rationales=[],
                common_traps=['Applying when purpose merely difficult (need destroyed)', "Using when performance impossible (that's impossibility, not frustration)", 'Forgetting both parties must have known purpose'],
            ),
            KnowledgeNode(
                concept_id="contracts_assignment_delegation",
                name="Assignment vs Delegation",
                subject="contracts",
                difficulty=3,
                rule_statement="Rights can be assigned unless personal, materially change duty, or prohibited; duties can be delegated unless personal services or prohibited",
                elements=['Assignment of rights', 'Delegation of duties', 'Prohibition clauses', 'Personal services exception'],
                policy_rationales=[],
                common_traps=['Thinking all contract rights assignable (personal services exception)', "Missing that delegation doesn't release delegator (still liable)", 'Confusing assignment language with delegation'],
                # Mnemonic: AD: Assignment (rights), Delegation (duties)
            ),
            KnowledgeNode(
                concept_id="contracts_third_party_beneficiaries",
                name="Third-Party Beneficiaries",
                subject="contracts",
                difficulty=4,
                rule_statement="Intended beneficiary can enforce; incidental beneficiary cannot; test is whether party intended to benefit third party",
                elements=['Intended vs incidental', 'Creditor beneficiary', 'Donee beneficiary', 'Vesting of rights'],
                policy_rationales=[],
                common_traps=['Letting incidental beneficiary sue (cannot)', 'Missing that rights vest when beneficiary learns and relies', 'Forgetting government contracts presumed not to benefit third parties'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _add_criminal_law_expansion(self):
        """Add 7 additional criminal_law concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="criminal_law_robbery",
                name="Robbery",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Robbery is larceny from person or presence by force or intimidation",
                elements=['Larceny elements', 'From person or presence', 'Force or fear', 'Intent to permanently deprive'],
                policy_rationales=[],
                common_traps=['Missing that force must be used to obtain property or escape', "Forgetting presence means within victim's control", 'Confusing robbery with extortion (future threat)'],
                prerequisites=['criminal_law_larceny'],
            ),
            KnowledgeNode(
                concept_id="criminal_law_burglary",
                name="Burglary",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Common law burglary: breaking and entering dwelling of another at nighttime with intent to commit felony therein",
                elements=['Breaking', 'Entering', 'Dwelling', 'Of another', 'Nighttime', 'Intent to commit felony'],
                policy_rationales=[],
                common_traps=['Applying modern statutes (many drop nighttime, dwelling requirements)', 'Missing that intent must exist at time of entry', 'Forgetting slight force counts as breaking (turning doorknob)'],
                # Mnemonic: BEDINF: Breaking, Entering, Dwelling, Intent, Nighttime, Felony
            ),
            KnowledgeNode(
                concept_id="criminal_law_arson",
                name="Arson",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Common law arson: malicious burning of dwelling of another",
                elements=['Malicious', 'Burning', 'Dwelling', 'Of another'],
                policy_rationales=[],
                common_traps=['Thinking any burning suffices (need material wasting/charring)', 'Missing that burning own property for insurance is arson if endangers others', 'Confusing arson with criminal mischief'],
            ),
            KnowledgeNode(
                concept_id="criminal_law_conspiracy",
                name="Conspiracy",
                subject="criminal_law",
                difficulty=4,
                rule_statement="Agreement between two or more to commit crime plus overt act in furtherance (majority); common law no overt act needed",
                elements=['Agreement', 'Two or more parties', 'Intent', 'Overt act', 'Withdrawal'],
                policy_rationales=[],
                common_traps=["Forgetting Wharton's Rule (crime requiring two can't be conspiracy with only two)", "Missing that withdrawal doesn't excuse conspiracy liability (only subsequent crimes)", 'Applying unilateral conspiracy where bilateral required'],
                # Mnemonic: AIM: Agreement, Intent, Mens rea
            ),
            KnowledgeNode(
                concept_id="criminal_law_solicitation",
                name="Solicitation",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Solicitation is asking, encouraging, or commanding another to commit crime with intent that crime be committed",
                elements=['Asking/encouraging', 'Another person', 'Commit crime', 'Intent crime be committed'],
                policy_rationales=[],
                common_traps=['Thinking target crime must occur (solicitation complete upon asking)', 'Missing that renunciation generally not a defense', 'Confusing solicitation with attempt'],
            ),
            KnowledgeNode(
                concept_id="criminal_law_accomplice_liability",
                name="Accomplice Liability",
                subject="criminal_law",
                difficulty=4,
                rule_statement="Accomplice liable for crimes they aid, abet, or encourage with intent to assist and intent that crime be committed",
                elements=['Aid/abet/encourage', 'Intent to assist', 'Intent crime be committed', 'Principal commits crime'],
                policy_rationales=['Deter assistance to criminals', 'Hold helpers accountable'],
                common_traps=['Imposing liability for mere presence (need assistance)', 'Missing that accomplice liable for foreseeable crimes in furtherance', 'Confusing accomplice with accessory after fact (who aids after crime)'],
            ),
            KnowledgeNode(
                concept_id="criminal_law_entrapment",
                name="Entrapment",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Entrapment defense if government induces crime in person not predisposed; objective test focuses on government conduct",
                elements=['Government inducement', 'Lack of predisposition', 'Subjective test', 'Objective test'],
                policy_rationales=[],
                common_traps=['Applying entrapment to private party inducement (must be government)', 'Forgetting predisposition defeats defense under subjective test', 'Missing that providing opportunity is not inducement'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _add_criminal_procedure_expansion(self):
        """Add 7 additional criminal_procedure concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="criminal_procedure_fruit_poisonous_tree",
                name="Fruit of Poisonous Tree",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Evidence derived from illegal search/seizure excluded unless independent source, inevitable discovery, or attenuation",
                elements=['Derivative evidence', 'Independent source', 'Inevitable discovery', 'Attenuation doctrine'],
                policy_rationales=[],
                common_traps=["Missing that Miranda violations don't trigger fruit doctrine fully", 'Forgetting live testimony attenuates more easily than physical evidence', 'Not applying inevitable discovery when would have found anyway'],
                # Mnemonic: IIA: Independent source, Inevitable discovery, Attenuation
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_terry_stops",
                name="Terry Stops (Stop & Frisk)",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Officer may briefly detain for investigation with reasonable suspicion of criminal activity; may frisk if reasonable belief armed and dangerous",
                elements=['Reasonable suspicion', 'Brief detention', 'Armed and dangerous', 'Plain feel doctrine'],
                policy_rationales=[],
                common_traps=['Requiring probable cause for Terry stop (reasonable suspicion suffices)', 'Allowing frisk without safety concern', 'Missing that anonymous tip alone insufficient without corroboration'],
                prerequisites=['criminal_procedure_search_incident'],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_arrests",
                name="Arrests (With & Without Warrant)",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Arrest requires probable cause; warrant required for home arrest absent exigency; public arrest no warrant needed",
                elements=['Probable cause', 'Warrant for home', 'Exigent circumstances', 'Public place exception'],
                policy_rationales=[],
                common_traps=["Requiring warrant for all arrests (public arrests don't need warrant)", 'Missing that arrest in third party home needs search warrant', 'Forgetting hot pursuit is exigency excusing warrant'],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_exigent_circumstances",
                name="Exigent Circumstances",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Warrantless entry justified by hot pursuit, imminent destruction of evidence, emergency aid, or preventing escape",
                elements=['Hot pursuit', 'Destruction of evidence', 'Emergency aid', 'Prevent escape'],
                policy_rationales=[],
                common_traps=['Applying when police created exigency by bad faith', 'Missing that mere possibility of destruction insufficient', 'Forgetting exigency must be immediate, not speculative'],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_inventory_searches",
                name="Inventory Searches",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Police may inventory lawfully impounded vehicle or arrested person's belongings following standardized procedures",
                elements=['Lawful impoundment', 'Standardized procedure', 'Administrative purpose', 'No investigative pretext'],
                policy_rationales=[],
                common_traps=['Allowing when done for investigative purposes (must be administrative)', 'Missing that warrantless search of closed containers OK in inventory', 'Forgetting need for established policy/procedure'],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_lineups",
                name="Lineups & Identifications",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Post-charge lineup requires counsel; suggestive pre-trial identification excluded if unreliable; in-court ID evaluated for reliability",
                elements=['Right to counsel at lineup', 'Suggestiveness test', 'Reliability factors', 'Independent source'],
                policy_rationales=[],
                common_traps=['Requiring counsel at pre-charge lineups (not required)', "Missing that photo arrays don't require counsel", 'Forgetting independent source exception for tainted ID'],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_plea_bargaining",
                name="Plea Bargaining",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Guilty plea must be voluntary, intelligent, with understanding of charges and consequences; breach of plea deal allows withdrawal",
                elements=['Voluntary', 'Intelligent', 'Understanding', 'Breach remedies'],
                policy_rationales=[],
                common_traps=['Missing that defendant must understand deportation consequences', 'Forgetting ineffective assistance can invalidate plea', 'Not knowing that judge not bound by sentencing recommendation'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _add_evidence_expansion(self):
        """Add 9 additional evidence concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="evidence_subsequent_remedial_measures",
                name="Subsequent Remedial Measures",
                subject="evidence",
                difficulty=3,
                rule_statement="Evidence of repairs or safety measures after injury inadmissible to prove negligence or defect, but admissible for impeachment, ownership, or feasibility",
                elements=['Inadmissible for negligence', 'Admissible for impeachment', 'Ownership', 'Feasibility if disputed'],
                policy_rationales=['Encourage repairs', 'Prevent deterring safety measures'],
                common_traps=['Excluding when offered for permissible purpose', "Missing that rule doesn't apply to strict liability cases in some jurisdictions", 'Forgetting rule encourages safety improvements'],
            ),
            KnowledgeNode(
                concept_id="evidence_compromise_settlement",
                name="Compromise & Settlement Offers",
                subject="evidence",
                difficulty=3,
                rule_statement="Statements made during settlement negotiations inadmissible to prove liability or amount; admissible for other purposes like bias",
                elements=['Dispute exists', 'Settlement statements', 'Not if no dispute', 'Admissions of fact admissible if not hypothetical'],
                policy_rationales=[],
                common_traps=['Excluding factual admissions made during negotiations (may be admissible)', 'Applying rule when no dispute existed at time', "Missing that Rule 408 doesn't apply to criminal cases"],
            ),
            KnowledgeNode(
                concept_id="evidence_habit",
                name="Habit Evidence",
                subject="evidence",
                difficulty=3,
                rule_statement="Evidence of habit or routine practice admissible to prove conduct on particular occasion; more specific and automatic than character",
                elements=['Specificity', 'Frequency', 'Automatic response', 'Routine practice'],
                policy_rationales=[],
                common_traps=['Confusing habit with character (habit is specific routine)', "Missing that habit doesn't require corroboration or eyewitness", 'Thinking single instance can establish habit (need pattern)'],
            ),
            KnowledgeNode(
                concept_id="evidence_rape_shield",
                name="Rape Shield Rule",
                subject="evidence",
                difficulty=4,
                rule_statement="Evidence of victim's sexual behavior generally inadmissible except to prove alternative source of semen/injury or past acts with defendant",
                elements=['General exclusion', 'Alternative source exception', 'Prior acts with defendant', 'Constitutional rights'],
                policy_rationales=['Protect victim privacy', 'Prevent victim-blaming', 'Encourage reporting'],
                common_traps=['Missing that constitutional right to present defense may override', 'Applying rule to exclude reputation for untruthfulness (wrong - character for truthfulness allowed)', 'Forgetting criminal vs civil distinctions'],
            ),
            KnowledgeNode(
                concept_id="evidence_best_evidence_rule",
                name="Best Evidence Rule (Original Document Rule)",
                subject="evidence",
                difficulty=3,
                rule_statement="To prove content of writing, recording, or photo, must produce original or explain absence; doesn't apply if not proving contents",
                elements=['Content being proved', 'Original required', 'Duplicate admissible', 'Excuses for absence'],
                policy_rationales=[],
                common_traps=['Applying when content not being proved (e.g., event witnessed)', "Thinking duplicates inadmissible (they're treated as originals)", 'Missing that photos of writings are duplicates'],
            ),
            KnowledgeNode(
                concept_id="evidence_witness_competency",
                name="Witness Competency",
                subject="evidence",
                difficulty=3,
                rule_statement="All persons competent to testify unless cannot perceive, remember, communicate, or understand oath; judge determines competency",
                elements=['Perception', 'Memory', 'Communication', 'Oath understanding'],
                policy_rationales=[],
                common_traps=['Thinking children automatically incompetent (competency presumed)', 'Confusing competency with credibility', 'Missing that personal knowledge is separate requirement'],
            ),
            KnowledgeNode(
                concept_id="evidence_recorded_recollection",
                name="Recorded Recollection vs Refreshing Memory",
                subject="evidence",
                difficulty=4,
                rule_statement="Refreshing recollection: witness looks at writing, then testifies from refreshed memory; recorded recollection: can't remember even after viewing, read into evidence",
                elements=['Present recollection refreshed', 'Past recollection recorded', 'Foundation requirements', 'Hearsay exception'],
                policy_rationales=[],
                common_traps=['Confusing the two doctrines', 'Missing that refreshing document not admitted, recorded recollection is', 'Forgetting that recorded recollection requires inability to remember even after viewing'],
            ),
            KnowledgeNode(
                concept_id="evidence_learned_treatises",
                name="Learned Treatises",
                subject="evidence",
                difficulty=3,
                rule_statement="Statements from reliable treatises admissible on direct or cross if established as reliable authority and expert on stand",
                elements=['Reliable authority', 'Expert on stand', 'Read to jury', 'Not admitted as exhibit'],
                policy_rationales=[],
                common_traps=['Admitting treatise itself (only read into evidence)', 'Using without expert on stand', 'Missing that can be used on direct, not just cross'],
            ),
            KnowledgeNode(
                concept_id="evidence_judicial_notice",
                name="Judicial Notice",
                subject="evidence",
                difficulty=3,
                rule_statement="Court may take judicial notice of facts generally known in jurisdiction or accurately and readily determinable from reliable sources",
                elements=['Generally known', 'Accurately determinable', 'Mandatory if requested', 'Instructing jury'],
                policy_rationales=[],
                common_traps=['Taking notice of disputed facts (must be indisputable)', 'Missing that criminal jury cannot be instructed to accept noticed fact as conclusive', 'Forgetting party must be heard before judicial notice'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _add_real_property_expansion(self):
        """Add 12 additional real_property concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="real_property_easement_by_implication",
                name="Easement by Implication",
                subject="real_property",
                difficulty=4,
                rule_statement="Easement implied from prior use if use was apparent, continuous, reasonably necessary, and parties expected it to continue",
                elements=['Prior use', 'Apparent', 'Continuous', 'Reasonably necessary', 'Common grantor'],
                policy_rationales=[],
                common_traps=['Confusing with easement by necessity (necessity must be absolute)', 'Missing that strict necessity only required for necessity, not implication', 'Forgetting quasi-easement requires unity of ownership before severance'],
                prerequisites=['real_property_easements_servitudes_and_licenses'],
            ),
            KnowledgeNode(
                concept_id="real_property_easement_by_prescription",
                name="Easement by Prescription",
                subject="real_property",
                difficulty=3,
                rule_statement="Easement acquired by open, notorious, continuous, adverse use for statutory period (similar to adverse possession)",
                elements=['Open and notorious', 'Continuous', 'Adverse/hostile', 'Statutory period', 'No exclusive use'],
                policy_rationales=[],
                common_traps=['Requiring exclusive use (not required for prescriptive easement)', 'Missing that permissive use cannot ripen into prescriptive easement', 'Forgetting that prescription creates easement, not ownership'],
                prerequisites=['real_property_adverse_possession'],
            ),
            KnowledgeNode(
                concept_id="real_property_profit_a_prendre",
                name="Profit à Prendre",
                subject="real_property",
                difficulty=3,
                rule_statement="Right to enter land and remove resources like minerals, timber, or fish; similar to easement but includes right to take",
                elements=['Right to take', 'Created like easements', 'Alienable', 'Divisible'],
                policy_rationales=[],
                common_traps=['Confusing profit with easement (profit includes taking)', 'Missing that profit holder may imply easement to access', 'Not distinguishing profit in gross vs appurtenant'],
            ),
            KnowledgeNode(
                concept_id="real_property_real_covenants_detailed",
                name="Real Covenants Running with Land",
                subject="real_property",
                difficulty=4,
                rule_statement="Covenant runs at law if writing, intent, touch and concern, notice, and horizontal/vertical privity; damages remedy",
                elements=['Writing', 'Intent to run', 'Touch and concern', 'Notice', 'Horizontal privity', 'Vertical privity'],
                policy_rationales=[],
                common_traps=['Missing horizontal privity requirement (not needed for equitable servitudes)', 'Confusing real covenant (damages) with equitable servitude (injunction)', 'Forgetting burden runs at law only if horizontal privity exists'],
                # Mnemonic: WRITNHV: Writing, Run intent, Interest (T&C), Touch concern, Notice, Horizontal, Vertical
            ),
            KnowledgeNode(
                concept_id="real_property_equitable_servitudes",
                name="Equitable Servitudes",
                subject="real_property",
                difficulty=4,
                rule_statement="Equitable servitude enforced in equity if writing (or common scheme), intent, touch and concern, and notice; injunction remedy",
                elements=['Writing or common scheme', 'Intent', 'Touch and concern', 'Notice', 'No privity required'],
                policy_rationales=['Allow flexible land use restrictions', 'Protect purchaser expectations'],
                common_traps=['Requiring privity for equitable servitudes (not needed)', 'Missing that equitable servitudes remedy is injunction, not damages', 'Forgetting notice can be actual, record, or inquiry'],
            ),
            KnowledgeNode(
                concept_id="real_property_assignment_vs_sublease_detailed",
                name="Assignment vs Sublease",
                subject="real_property",
                difficulty=4,
                rule_statement="Assignment transfers entire remaining term; sublease retains any part; assignee in privity with landlord, sublessee not",
                elements=['Entire term test', 'Privity of estate', 'Privity of contract', 'Landlord-tenant relationships'],
                policy_rationales=[],
                common_traps=['Missing that retaining one day makes it sublease', 'Forgetting assignee liable on covenants that run with land', 'Confusing when original tenant remains liable (always in contract)'],
                # Mnemonic: APES: Assignment = Privity Estate; Sublease = no privity
            ),
            KnowledgeNode(
                concept_id="real_property_constructive_eviction",
                name="Constructive Eviction",
                subject="real_property",
                difficulty=3,
                rule_statement="Landlord's breach of duty makes premises uninhabitable; tenant must notify, give chance to repair, and vacate within reasonable time",
                elements=['Substantial interference', 'Tenant vacates', 'Reasonable time', "Landlord's fault"],
                policy_rationales=[],
                common_traps=['Missing that tenant must actually vacate (if stay, waives claim)', 'Forgetting to give landlord notice and opportunity to cure', 'Confusing with actual eviction (which is physical exclusion)'],
                prerequisites=['real_property_landlordtenant_law'],
            ),
            KnowledgeNode(
                concept_id="real_property_security_deposits",
                name="Security Deposits",
                subject="real_property",
                difficulty=3,
                rule_statement="Landlord may retain deposit for unpaid rent or damage beyond normal wear and tear; must return within statutory period with itemization",
                elements=['Permissible deductions', 'Normal wear and tear', 'Statutory return period', 'Itemization requirement'],
                policy_rationales=[],
                common_traps=['Allowing deduction for normal wear and tear (not permitted)', 'Missing statutory interest requirements in some states', 'Forgetting landlord burden to prove deductions proper'],
            ),
            KnowledgeNode(
                concept_id="real_property_mortgage_assumption",
                name="Mortgage Assumption vs Subject To",
                subject="real_property",
                difficulty=4,
                rule_statement="Assumption: buyer personally liable; subject to: buyer not personally liable but property at risk; original borrower remains liable unless novation",
                elements=['Assumption agreement', 'Personal liability', 'Subject to purchase', 'Novation requirement'],
                policy_rationales=[],
                common_traps=['Thinking original borrower released automatically (need novation/release)', 'Confusing assumption with subject to liability', 'Missing that due-on-sale clause may prevent transfer'],
            ),
            KnowledgeNode(
                concept_id="real_property_due_on_sale",
                name="Due-on-Sale Clauses",
                subject="real_property",
                difficulty=3,
                rule_statement="Clause allowing lender to accelerate loan upon transfer; generally enforceable; Garn-St. Germain Act exempts certain transfers",
                elements=['Acceleration right', 'Transfer restrictions', 'Federal preemption', 'Exempt transfers'],
                policy_rationales=[],
                common_traps=['Missing Garn-St. Germain exemptions (transfers to spouse, children, etc.)', 'Thinking all transfers trigger clause (exempt transfers exist)', 'Forgetting lender must act timely to enforce'],
            ),
            KnowledgeNode(
                concept_id="real_property_redemption",
                name="Redemption (Equitable vs Statutory)",
                subject="real_property",
                difficulty=4,
                rule_statement="Equitable redemption: pay full debt before foreclosure sale; statutory redemption: buy back property after sale within statutory period",
                elements=['Equitable redemption timing', 'Statutory redemption period', 'Amount required', 'Priority of redemptioners'],
                policy_rationales=[],
                common_traps=['Confusing timing of equitable (before sale) vs statutory (after sale)', 'Missing that statutory redemption not available in all states', 'Forgetting strict foreclosure eliminates redemption'],
            ),
            KnowledgeNode(
                concept_id="real_property_deed_types",
                name="Deed Types & Requirements",
                subject="real_property",
                difficulty=3,
                rule_statement="General warranty deed: grantor warrants title against all defects; special warranty: only during grantor's ownership; quitclaim: no warranties",
                elements=['General warranty deed', 'Special warranty deed', 'Quitclaim deed', 'Six covenants'],
                policy_rationales=[],
                common_traps=['Missing that quitclaim transfers whatever interest grantor has, if any', 'Confusing present covenants (breached at closing) vs future (breached later)', 'Forgetting delivery required for deed effectiveness'],
                # Mnemonic: GSQ: General, Special, Quitclaim
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

# Essay Subjects for Iowa Bar

# Essay Subjects for Iowa Bar

    def _initialize_professional_responsibility(self):
        """10 Professional Responsibility concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="prof_resp_confidentiality",
                name="Duty of Confidentiality",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Lawyer must not reveal information relating to representation unless client consents, disclosure impliedly authorized, or exception applies",
                elements=['Duty to all information', 'Broader than privilege', 'Survives termination', 'Prospective clients'],
                policy_rationales=[],
                common_traps=['Confusing with privilege', 'Missing crime/fraud exception limits', 'Forgetting survives death'],
                # Mnemonic: CRIMES: Crime prevention, Reasonably certain harm, Informed consent, Mitigate harm, Establish defense, Secure advice
            ),
            KnowledgeNode(
                concept_id="prof_resp_conflicts_current",
                name="Conflicts - Current Clients",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent if directly adverse or significant limitation risk, unless reasonable belief, not prohibited, not same litigation, written consent",
                elements=['Direct adversity', 'Material limitation', 'Reasonable belief', 'Written consent'],
                policy_rationales=[],
                common_traps=['Same litigation cannot be cured', 'Business transactions need disclosure', 'Positional conflicts'],
                # Mnemonic: WIND: Written consent, Informed, Not same litigation, Direct adversity
            ),
            KnowledgeNode(
                concept_id="prof_resp_conflicts_former",
                name="Conflicts - Former Clients",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent if materially adverse in same or substantially related matter unless written consent",
                elements=['Same matter', 'Substantially related', 'Material adversity', 'Written consent'],
                policy_rationales=[],
                common_traps=['Substantial relationship broader than same', 'Imputation differs', 'Screening procedures'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_competence",
                name="Duty of Competence",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must provide competent representation requiring knowledge, skill, thoroughness, and preparation",
                elements=['Legal knowledge', 'Skill', 'Thoroughness', 'Preparation'],
                policy_rationales=[],
                common_traps=['Need not be expert', 'Must stay current', 'Can associate with competent lawyer'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_fees",
                name="Fees & Fee Agreements",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Fee must be reasonable; contingent fees prohibited in criminal and divorce; writing preferred",
                elements=['Reasonableness factors', 'Writing preferred', 'Contingent restrictions', 'Fee division rules'],
                policy_rationales=[],
                common_traps=['No contingent in criminal', 'No contingent in divorce', 'Fee division restrictions', 'Separate client property'],
                # Mnemonic: NO CC: No Contingent Criminal, No Contingent Custody
            ),
            KnowledgeNode(
                concept_id="prof_resp_client_decisions",
                name="Client Decision Authority",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Client decides objectives; lawyer decides means; certain decisions require client consent",
                elements=['Client: objectives, settlement, plea, testify', 'Lawyer: tactics', 'Limit scope with consent', 'Consult and explain'],
                policy_rationales=[],
                common_traps=['Settlement is client decision', 'Testify in criminal is client', 'Limiting scope needs consent'],
                # Mnemonic: SPLIT: Settlement, Plea, testify, jury trial = client
            ),
            KnowledgeNode(
                concept_id="prof_resp_candor_tribunal",
                name="Candor Toward Tribunal",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="No false statements; disclose adverse authority; correct false evidence; cannot offer known false evidence",
                elements=['No false statements', 'Disclose adverse binding authority', 'Correct false evidence', 'No known false evidence'],
                policy_rationales=[],
                common_traps=['Must disclose adverse in controlling jurisdiction', 'Must correct even if client objects', 'Narrative testimony'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_fairness_opposing",
                name="Fairness to Opposing Party",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="No obstruction of evidence, no ex parte with represented persons, fair dealing with unrepresented",
                elements=['No obstruction', 'No ex parte contact', 'Fair with unrepresented', 'No unlawful obstruction'],
                policy_rationales=[],
                common_traps=['Contact through counsel', 'Flag inadvertent privileged docs', 'Clarify role with unrepresented'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_prosecutor",
                name="Special Prosecutor Duties",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Must have probable cause; disclose exculpatory evidence; ensure counsel",
                elements=['Probable cause', 'Brady disclosure', 'Ensure counsel', 'Protect unrepresented'],
                policy_rationales=['Seek justice not convictions', 'Protect accused rights', 'Ensure fairness'],
                common_traps=['Heightened Brady duty', 'Cannot subpoena lawyer about client', 'Must disclose post-conviction'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_meritorious_claims",
                name="Meritorious Claims",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must not bring frivolous claims; must have good faith basis",
                elements=['Non-frivolous basis', 'Good faith law change OK', 'Candor required', 'No false statements'],
                policy_rationales=[],
                common_traps=['Creative arguments OK if good faith', 'Criminal defense exception', 'Frivolous ≠ losing'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_corporations(self):
        """7 Corporations concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="corp_formation",
                name="Corporate Formation",
                subject="corporations",
                difficulty=3,
                rule_statement="Corporation formed by filing articles; becomes separate entity upon filing",
                elements=['Articles of incorporation', 'File with state', 'Separate personality', 'Perpetual existence'],
                policy_rationales=[],
                common_traps=['Just need filing', 'De facto corporation', 'Promoter liability'],
            ),
            KnowledgeNode(
                concept_id="corp_piercing_veil",
                name="Piercing Corporate Veil",
                subject="corporations",
                difficulty=4,
                rule_statement="Veil pierced if fraud, evade obligations, or injustice; requires alter ego and inequitable result",
                elements=['Alter ego', 'Inequitable result', 'Undercapitalization', 'Formality failure'],
                policy_rationales=['Limited liability encourages business', 'Prevent abuse', 'Balance protection'],
                common_traps=['High threshold', 'Control alone insufficient', 'Parent-sub vs individual-corp'],
            ),
            KnowledgeNode(
                concept_id="corp_duty_care",
                name="Duty of Care",
                subject="corporations",
                difficulty=4,
                rule_statement="Directors owe care of ordinarily prudent person; business judgment rule protects if informed, disinterested, good faith",
                elements=['Informed decision', 'Ordinary prudence', 'Business judgment rule', 'Good faith'],
                policy_rationales=[],
                common_traps=['BJR not automatic', 'Gross negligence defeats', 'Confusing care with loyalty'],
                # Mnemonic: BJR-DIG: Business Judgment Rule = Disinterested, Informed, Good faith
            ),
            KnowledgeNode(
                concept_id="corp_duty_loyalty",
                name="Duty of Loyalty",
                subject="corporations",
                difficulty=4,
                rule_statement="Act in corporation's interests; no self-dealing unless fair or approved",
                elements=['No self-dealing', 'Corporate opportunity', 'Fairness if interested', 'Disclosure and approval'],
                policy_rationales=[],
                common_traps=['Interested transaction voidable unless approved', 'Corporate opportunity analysis', 'Entire fairness standard'],
            ),
            KnowledgeNode(
                concept_id="corp_derivative_actions",
                name="Derivative Actions",
                subject="corporations",
                difficulty=4,
                rule_statement="Shareholder sues on corporation's behalf; requires demand unless futile; contemporaneous ownership",
                elements=['Demand on board', 'Contemporaneous ownership', 'Adequate representation', 'Corporation necessary party'],
                policy_rationales=[],
                common_traps=['Demand requirement', 'Contemporaneous ownership', 'Derivative vs direct'],
            ),
            KnowledgeNode(
                concept_id="corp_shareholder_voting",
                name="Shareholder Voting",
                subject="corporations",
                difficulty=3,
                rule_statement="Elect directors, approve fundamental changes; proxies permitted; quorum required",
                elements=['Elect directors', 'Fundamental changes', 'Proxy rules', 'Quorum'],
                policy_rationales=[],
                common_traps=['Removal without cause', 'Cumulative voting', 'Proxy rules'],
            ),
            KnowledgeNode(
                concept_id="corp_mergers",
                name="Mergers & Acquisitions",
                subject="corporations",
                difficulty=4,
                rule_statement="Merger needs board and shareholder approval; surviving entity assumes liabilities; appraisal rights",
                elements=['Board approval', 'Shareholder vote', 'Successor liability', 'Appraisal rights'],
                policy_rationales=[],
                common_traps=['Short-form merger', 'Triangular mergers', 'De facto merger'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_wills_trusts_estates(self):
        """6 Wills Trusts Estates concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="wills_execution",
                name="Will Execution",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Valid will: 18+, sound mind, intent, writing, signature, two witnesses present simultaneously",
                elements=['Age 18+ sound mind', 'Intent', 'Writing', 'Signature', 'Two witnesses'],
                policy_rationales=[],
                common_traps=['Witnesses same time', 'Interested witness', 'Substantial compliance'],
                # Mnemonic: WITSAC: Writing, Intent, Testator 18+, Signature, Attestation, Capacity
            ),
            KnowledgeNode(
                concept_id="wills_revocation",
                name="Will Revocation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revoked by: subsequent instrument, physical act with intent, operation of law (divorce)",
                elements=['By writing', 'Physical act + intent', 'Operation of law', 'Dependent relative revocation'],
                policy_rationales=[],
                common_traps=['Divorce revokes ex-spouse', 'Revival rules', 'DRR for mistakes'],
            ),
            KnowledgeNode(
                concept_id="wills_intestate",
                name="Intestate Succession",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Passes to heirs by statute: spouse, descendants, parents, siblings",
                elements=['Spouse share', 'Issue', 'Per capita vs per stirpes', 'Collaterals'],
                policy_rationales=[],
                common_traps=['Per capita vs per stirpes', 'Adopted children equal', 'Half-bloods equal'],
                # Mnemonic: SIPAC: Spouse, Issue, Parents, Ancestors, Collaterals
            ),
            KnowledgeNode(
                concept_id="trusts_creation",
                name="Trust Creation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Requires: settlor capacity and intent, res, definite beneficiaries, valid purpose, delivery (inter vivos)",
                elements=['Settlor capacity/intent', 'Trust property', 'Ascertainable beneficiaries', 'Valid purpose', 'Delivery'],
                policy_rationales=[],
                common_traps=['Precatory language insufficient', 'Indefinite beneficiaries void', 'Delivery for inter vivos'],
                # Mnemonic: SCRIPT: Settlor, Capacity, Res, Intent, Purpose, Transfer
            ),
            KnowledgeNode(
                concept_id="trusts_charitable",
                name="Charitable Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Charitable purpose; indefinite beneficiaries OK; cy pres if purpose fails; RAP doesn't apply",
                elements=['Charitable purpose', 'Indefinite beneficiaries OK', 'Cy pres', 'RAP exception'],
                policy_rationales=[],
                common_traps=["RAP doesn't apply", 'Cy pres application', 'AG has standing'],
            ),
            KnowledgeNode(
                concept_id="trusts_fiduciary_duties",
                name="Trustee Fiduciary Duties",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Loyalty, prudence, best interests; no self-dealing; prudent investment; account",
                elements=['Duty of loyalty', 'Duty of prudence', 'Duty to account', 'Duty of impartiality'],
                policy_rationales=[],
                common_traps=['Self-dealing voidable even if fair', 'Prudent investor rule', 'Impartiality income/remainder'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_family_law(self):
        """5 Family Law concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="family_divorce",
                name="Divorce Grounds",
                subject="family_law",
                difficulty=3,
                rule_statement="All states allow no-fault; irretrievable breakdown or separation; residency requirement",
                elements=['No-fault grounds', 'Irretrievable breakdown', 'Residency', 'Fault grounds minority'],
                policy_rationales=[],
                common_traps=['Fault for divorce unnecessary', 'Fault may affect property/alimony', 'Cooling-off periods'],
            ),
            KnowledgeNode(
                concept_id="family_property_division",
                name="Property Division",
                subject="family_law",
                difficulty=4,
                rule_statement="Marital property divided equitably; separate retained; factors include contributions, duration, circumstances",
                elements=['Marital vs separate', 'Equitable factors', 'Valuation date', 'Professional degrees'],
                policy_rationales=[],
                common_traps=['Equitable ≠ equal', 'Appreciation of separate may be marital', 'Pension benefits marital'],
            ),
            KnowledgeNode(
                concept_id="family_spousal_support",
                name="Spousal Support",
                subject="family_law",
                difficulty=3,
                rule_statement="Based on need, ability, duration, contributions; modifiable unless agreed",
                elements=['Need', 'Ability to pay', 'Duration', 'Contributions', 'Modifiability'],
                policy_rationales=[],
                common_traps=['Remarriage terminates', 'Cohabitation may terminate', 'Types: temporary, rehabilitative, permanent'],
            ),
            KnowledgeNode(
                concept_id="family_child_custody",
                name="Child Custody",
                subject="family_law",
                difficulty=4,
                rule_statement="Best interests of child; factors include wishes, relationships, stability, health",
                elements=['Best interests', 'Legal vs physical', 'Joint vs sole', 'Modification standards'],
                policy_rationales=[],
                common_traps=['Gender preference unconstitutional', 'Primary caretaker presumption', 'UCCJEA jurisdiction'],
            ),
            KnowledgeNode(
                concept_id="family_child_support",
                name="Child Support",
                subject="family_law",
                difficulty=3,
                rule_statement="Both parents liable; income guidelines; non-modifiable for past due; interstate enforceable",
                elements=['Income guidelines', 'Both parents', 'Modifiable prospectively', 'UIFSA enforcement'],
                policy_rationales=[],
                common_traps=['Non-dischargeable bankruptcy', 'Past-due not modifiable', 'Emancipation terminates'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_secured_transactions(self):
        """6 Secured Transactions concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="secured_scope",
                name="Article 9 Scope",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Applies to security interests in personal property/fixtures by contract; excludes real property, wages, federal liens",
                elements=['Personal property', 'By contract', 'Fixtures included', 'Exclusions'],
                policy_rationales=[],
                common_traps=['Not real property mortgages', 'True leases excluded', 'Sales of payment rights covered'],
            ),
            KnowledgeNode(
                concept_id="secured_attachment",
                name="Attachment",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Attaches when: value given, debtor has rights, authenticated agreement OR possession/control",
                elements=['Value given', 'Rights in collateral', 'Authenticated agreement', 'Description'],
                policy_rationales=[],
                common_traps=['All three required', 'Agreement must describe', 'Possession substitutes for writing'],
                # Mnemonic: VRA: Value, Rights, Agreement
            ),
            KnowledgeNode(
                concept_id="secured_perfection",
                name="Perfection",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Perfected by: filing, possession, control, or automatic (PMSI consumer goods)",
                elements=['Filing statement', 'Possession/control', 'Automatic PMSI', 'Temporary rules'],
                policy_rationales=[],
                common_traps=['PMSI consumer goods automatic', 'Filing needs name and collateral', "File in debtor's state"],
                # Mnemonic: FPAC: Filing, Possession, Automatic, Control
            ),
            KnowledgeNode(
                concept_id="secured_pmsi",
                name="PMSI Super-Priority",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="PMSI enables acquisition; super-priority if properly perfected",
                elements=['Enables acquisition', 'Different perfection', 'Super-priority', 'Notice for inventory'],
                policy_rationales=[],
                common_traps=['Inventory PMSI needs notice', 'Consumer goods automatic', '20-day grace period'],
            ),
            KnowledgeNode(
                concept_id="secured_priority",
                name="Priority Rules",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="First to file/perfect wins; PMSI super-priority; buyer in ordinary course takes free",
                elements=['First to file/perfect', 'PMSI super-priority', 'BIOC exception', 'Lien creditor'],
                policy_rationales=[],
                common_traps=['Filing beats possession if first', 'BIOC takes free with notice', 'Judgment lien priority'],
            ),
            KnowledgeNode(
                concept_id="secured_default",
                name="Default Remedies",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Upon default: take possession (self-help if no breach of peace), dispose commercially reasonable, debtor gets surplus",
                elements=['Self-help no breach peace', 'Judicial alternative', 'Commercially reasonable', 'Notice required'],
                policy_rationales=[],
                common_traps=['Breach of peace voids self-help', 'Notice before disposition', 'Strict foreclosure option'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_iowa_procedure(self):
        """1 Iowa Procedure concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="iowa_civil_procedure",
                name="Iowa Civil Procedure",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Iowa Rules largely mirror Federal but with Iowa variations; governed by Iowa Code and court rules",
                elements=['Iowa Rules Civil Procedure', 'Court Rules', 'District court', 'Appellate procedures'],
                policy_rationales=[],
                common_traps=['Not identical to federal', 'Iowa-specific timing', 'Local rules variations'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_professional_responsibility(self):
        """10 Professional Responsibility concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="prof_resp_confidentiality",
                name="Duty of Confidentiality",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Lawyer must not reveal information relating to representation unless client consents, disclosure impliedly authorized, or exception applies",
                elements=['Duty to all information', 'Broader than privilege', 'Survives termination', 'Prospective clients'],
                policy_rationales=[],
                common_traps=['Confusing with privilege', 'Missing crime/fraud exception limits', 'Forgetting survives death'],
                # Mnemonic: CRIMES: Crime prevention, Reasonably certain harm, Informed consent, Mitigate harm, Establish defense, Secure advice
            ),
            KnowledgeNode(
                concept_id="prof_resp_conflicts_current",
                name="Conflicts - Current Clients",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent if directly adverse or significant limitation risk, unless reasonable belief, not prohibited, not same litigation, written consent",
                elements=['Direct adversity', 'Material limitation', 'Reasonable belief', 'Written consent'],
                policy_rationales=[],
                common_traps=['Same litigation cannot be cured', 'Business transactions need disclosure', 'Positional conflicts'],
                # Mnemonic: WIND: Written consent, Informed, Not same litigation, Direct adversity
            ),
            KnowledgeNode(
                concept_id="prof_resp_conflicts_former",
                name="Conflicts - Former Clients",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent if materially adverse in same or substantially related matter unless written consent",
                elements=['Same matter', 'Substantially related', 'Material adversity', 'Written consent'],
                policy_rationales=[],
                common_traps=['Substantial relationship broader than same', 'Imputation differs', 'Screening procedures'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_competence",
                name="Duty of Competence",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must provide competent representation requiring knowledge, skill, thoroughness, and preparation",
                elements=['Legal knowledge', 'Skill', 'Thoroughness', 'Preparation'],
                policy_rationales=[],
                common_traps=['Need not be expert', 'Must stay current', 'Can associate with competent lawyer'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_fees",
                name="Fees & Fee Agreements",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Fee must be reasonable; contingent fees prohibited in criminal and divorce; writing preferred",
                elements=['Reasonableness factors', 'Writing preferred', 'Contingent restrictions', 'Fee division rules'],
                policy_rationales=[],
                common_traps=['No contingent in criminal', 'No contingent in divorce', 'Fee division restrictions', 'Separate client property'],
                # Mnemonic: NO CC: No Contingent Criminal, No Contingent Custody
            ),
            KnowledgeNode(
                concept_id="prof_resp_client_decisions",
                name="Client Decision Authority",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Client decides objectives; lawyer decides means; certain decisions require client consent",
                elements=['Client: objectives, settlement, plea, testify', 'Lawyer: tactics', 'Limit scope with consent', 'Consult and explain'],
                policy_rationales=[],
                common_traps=['Settlement is client decision', 'Testify in criminal is client', 'Limiting scope needs consent'],
                # Mnemonic: SPLIT: Settlement, Plea, testify, jury trial = client
            ),
            KnowledgeNode(
                concept_id="prof_resp_candor_tribunal",
                name="Candor Toward Tribunal",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="No false statements; disclose adverse authority; correct false evidence; cannot offer known false evidence",
                elements=['No false statements', 'Disclose adverse binding authority', 'Correct false evidence', 'No known false evidence'],
                policy_rationales=[],
                common_traps=['Must disclose adverse in controlling jurisdiction', 'Must correct even if client objects', 'Narrative testimony'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_fairness_opposing",
                name="Fairness to Opposing Party",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="No obstruction of evidence, no ex parte with represented persons, fair dealing with unrepresented",
                elements=['No obstruction', 'No ex parte contact', 'Fair with unrepresented', 'No unlawful obstruction'],
                policy_rationales=[],
                common_traps=['Contact through counsel', 'Flag inadvertent privileged docs', 'Clarify role with unrepresented'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_prosecutor",
                name="Special Prosecutor Duties",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Must have probable cause; disclose exculpatory evidence; ensure counsel",
                elements=['Probable cause', 'Brady disclosure', 'Ensure counsel', 'Protect unrepresented'],
                policy_rationales=['Seek justice not convictions', 'Protect accused rights', 'Ensure fairness'],
                common_traps=['Heightened Brady duty', 'Cannot subpoena lawyer about client', 'Must disclose post-conviction'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_meritorious_claims",
                name="Meritorious Claims",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must not bring frivolous claims; must have good faith basis",
                elements=['Non-frivolous basis', 'Good faith law change OK', 'Candor required', 'No false statements'],
                policy_rationales=[],
                common_traps=['Creative arguments OK if good faith', 'Criminal defense exception', 'Frivolous ≠ losing'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_corporations(self):
        """7 Corporations concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="corp_formation",
                name="Corporate Formation",
                subject="corporations",
                difficulty=3,
                rule_statement="Corporation formed by filing articles; becomes separate entity upon filing",
                elements=['Articles of incorporation', 'File with state', 'Separate personality', 'Perpetual existence'],
                policy_rationales=[],
                common_traps=['Just need filing', 'De facto corporation', 'Promoter liability'],
            ),
            KnowledgeNode(
                concept_id="corp_piercing_veil",
                name="Piercing Corporate Veil",
                subject="corporations",
                difficulty=4,
                rule_statement="Veil pierced if fraud, evade obligations, or injustice; requires alter ego and inequitable result",
                elements=['Alter ego', 'Inequitable result', 'Undercapitalization', 'Formality failure'],
                policy_rationales=['Limited liability encourages business', 'Prevent abuse', 'Balance protection'],
                common_traps=['High threshold', 'Control alone insufficient', 'Parent-sub vs individual-corp'],
            ),
            KnowledgeNode(
                concept_id="corp_duty_care",
                name="Duty of Care",
                subject="corporations",
                difficulty=4,
                rule_statement="Directors owe care of ordinarily prudent person; business judgment rule protects if informed, disinterested, good faith",
                elements=['Informed decision', 'Ordinary prudence', 'Business judgment rule', 'Good faith'],
                policy_rationales=[],
                common_traps=['BJR not automatic', 'Gross negligence defeats', 'Confusing care with loyalty'],
                # Mnemonic: BJR-DIG: Business Judgment Rule = Disinterested, Informed, Good faith
            ),
            KnowledgeNode(
                concept_id="corp_duty_loyalty",
                name="Duty of Loyalty",
                subject="corporations",
                difficulty=4,
                rule_statement="Act in corporation's interests; no self-dealing unless fair or approved",
                elements=['No self-dealing', 'Corporate opportunity', 'Fairness if interested', 'Disclosure and approval'],
                policy_rationales=[],
                common_traps=['Interested transaction voidable unless approved', 'Corporate opportunity analysis', 'Entire fairness standard'],
            ),
            KnowledgeNode(
                concept_id="corp_derivative_actions",
                name="Derivative Actions",
                subject="corporations",
                difficulty=4,
                rule_statement="Shareholder sues on corporation's behalf; requires demand unless futile; contemporaneous ownership",
                elements=['Demand on board', 'Contemporaneous ownership', 'Adequate representation', 'Corporation necessary party'],
                policy_rationales=[],
                common_traps=['Demand requirement', 'Contemporaneous ownership', 'Derivative vs direct'],
            ),
            KnowledgeNode(
                concept_id="corp_shareholder_voting",
                name="Shareholder Voting",
                subject="corporations",
                difficulty=3,
                rule_statement="Elect directors, approve fundamental changes; proxies permitted; quorum required",
                elements=['Elect directors', 'Fundamental changes', 'Proxy rules', 'Quorum'],
                policy_rationales=[],
                common_traps=['Removal without cause', 'Cumulative voting', 'Proxy rules'],
            ),
            KnowledgeNode(
                concept_id="corp_mergers",
                name="Mergers & Acquisitions",
                subject="corporations",
                difficulty=4,
                rule_statement="Merger needs board and shareholder approval; surviving entity assumes liabilities; appraisal rights",
                elements=['Board approval', 'Shareholder vote', 'Successor liability', 'Appraisal rights'],
                policy_rationales=[],
                common_traps=['Short-form merger', 'Triangular mergers', 'De facto merger'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_wills_trusts_estates(self):
        """6 Wills Trusts Estates concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="wills_execution",
                name="Will Execution",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Valid will: 18+, sound mind, intent, writing, signature, two witnesses present simultaneously",
                elements=['Age 18+ sound mind', 'Intent', 'Writing', 'Signature', 'Two witnesses'],
                policy_rationales=[],
                common_traps=['Witnesses same time', 'Interested witness', 'Substantial compliance'],
                # Mnemonic: WITSAC: Writing, Intent, Testator 18+, Signature, Attestation, Capacity
            ),
            KnowledgeNode(
                concept_id="wills_revocation",
                name="Will Revocation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revoked by: subsequent instrument, physical act with intent, operation of law (divorce)",
                elements=['By writing', 'Physical act + intent', 'Operation of law', 'Dependent relative revocation'],
                policy_rationales=[],
                common_traps=['Divorce revokes ex-spouse', 'Revival rules', 'DRR for mistakes'],
            ),
            KnowledgeNode(
                concept_id="wills_intestate",
                name="Intestate Succession",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Passes to heirs by statute: spouse, descendants, parents, siblings",
                elements=['Spouse share', 'Issue', 'Per capita vs per stirpes', 'Collaterals'],
                policy_rationales=[],
                common_traps=['Per capita vs per stirpes', 'Adopted children equal', 'Half-bloods equal'],
                # Mnemonic: SIPAC: Spouse, Issue, Parents, Ancestors, Collaterals
            ),
            KnowledgeNode(
                concept_id="trusts_creation",
                name="Trust Creation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Requires: settlor capacity and intent, res, definite beneficiaries, valid purpose, delivery (inter vivos)",
                elements=['Settlor capacity/intent', 'Trust property', 'Ascertainable beneficiaries', 'Valid purpose', 'Delivery'],
                policy_rationales=[],
                common_traps=['Precatory language insufficient', 'Indefinite beneficiaries void', 'Delivery for inter vivos'],
                # Mnemonic: SCRIPT: Settlor, Capacity, Res, Intent, Purpose, Transfer
            ),
            KnowledgeNode(
                concept_id="trusts_charitable",
                name="Charitable Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Charitable purpose; indefinite beneficiaries OK; cy pres if purpose fails; RAP doesn't apply",
                elements=['Charitable purpose', 'Indefinite beneficiaries OK', 'Cy pres', 'RAP exception'],
                policy_rationales=[],
                common_traps=["RAP doesn't apply", 'Cy pres application', 'AG has standing'],
            ),
            KnowledgeNode(
                concept_id="trusts_fiduciary_duties",
                name="Trustee Fiduciary Duties",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Loyalty, prudence, best interests; no self-dealing; prudent investment; account",
                elements=['Duty of loyalty', 'Duty of prudence', 'Duty to account', 'Duty of impartiality'],
                policy_rationales=[],
                common_traps=['Self-dealing voidable even if fair', 'Prudent investor rule', 'Impartiality income/remainder'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_family_law(self):
        """5 Family Law concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="family_divorce",
                name="Divorce Grounds",
                subject="family_law",
                difficulty=3,
                rule_statement="All states allow no-fault; irretrievable breakdown or separation; residency requirement",
                elements=['No-fault grounds', 'Irretrievable breakdown', 'Residency', 'Fault grounds minority'],
                policy_rationales=[],
                common_traps=['Fault for divorce unnecessary', 'Fault may affect property/alimony', 'Cooling-off periods'],
            ),
            KnowledgeNode(
                concept_id="family_property_division",
                name="Property Division",
                subject="family_law",
                difficulty=4,
                rule_statement="Marital property divided equitably; separate retained; factors include contributions, duration, circumstances",
                elements=['Marital vs separate', 'Equitable factors', 'Valuation date', 'Professional degrees'],
                policy_rationales=[],
                common_traps=['Equitable ≠ equal', 'Appreciation of separate may be marital', 'Pension benefits marital'],
            ),
            KnowledgeNode(
                concept_id="family_spousal_support",
                name="Spousal Support",
                subject="family_law",
                difficulty=3,
                rule_statement="Based on need, ability, duration, contributions; modifiable unless agreed",
                elements=['Need', 'Ability to pay', 'Duration', 'Contributions', 'Modifiability'],
                policy_rationales=[],
                common_traps=['Remarriage terminates', 'Cohabitation may terminate', 'Types: temporary, rehabilitative, permanent'],
            ),
            KnowledgeNode(
                concept_id="family_child_custody",
                name="Child Custody",
                subject="family_law",
                difficulty=4,
                rule_statement="Best interests of child; factors include wishes, relationships, stability, health",
                elements=['Best interests', 'Legal vs physical', 'Joint vs sole', 'Modification standards'],
                policy_rationales=[],
                common_traps=['Gender preference unconstitutional', 'Primary caretaker presumption', 'UCCJEA jurisdiction'],
            ),
            KnowledgeNode(
                concept_id="family_child_support",
                name="Child Support",
                subject="family_law",
                difficulty=3,
                rule_statement="Both parents liable; income guidelines; non-modifiable for past due; interstate enforceable",
                elements=['Income guidelines', 'Both parents', 'Modifiable prospectively', 'UIFSA enforcement'],
                policy_rationales=[],
                common_traps=['Non-dischargeable bankruptcy', 'Past-due not modifiable', 'Emancipation terminates'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_secured_transactions(self):
        """6 Secured Transactions concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="secured_scope",
                name="Article 9 Scope",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Applies to security interests in personal property/fixtures by contract; excludes real property, wages, federal liens",
                elements=['Personal property', 'By contract', 'Fixtures included', 'Exclusions'],
                policy_rationales=[],
                common_traps=['Not real property mortgages', 'True leases excluded', 'Sales of payment rights covered'],
            ),
            KnowledgeNode(
                concept_id="secured_attachment",
                name="Attachment",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Attaches when: value given, debtor has rights, authenticated agreement OR possession/control",
                elements=['Value given', 'Rights in collateral', 'Authenticated agreement', 'Description'],
                policy_rationales=[],
                common_traps=['All three required', 'Agreement must describe', 'Possession substitutes for writing'],
                # Mnemonic: VRA: Value, Rights, Agreement
            ),
            KnowledgeNode(
                concept_id="secured_perfection",
                name="Perfection",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Perfected by: filing, possession, control, or automatic (PMSI consumer goods)",
                elements=['Filing statement', 'Possession/control', 'Automatic PMSI', 'Temporary rules'],
                policy_rationales=[],
                common_traps=['PMSI consumer goods automatic', 'Filing needs name and collateral', "File in debtor's state"],
                # Mnemonic: FPAC: Filing, Possession, Automatic, Control
            ),
            KnowledgeNode(
                concept_id="secured_pmsi",
                name="PMSI Super-Priority",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="PMSI enables acquisition; super-priority if properly perfected",
                elements=['Enables acquisition', 'Different perfection', 'Super-priority', 'Notice for inventory'],
                policy_rationales=[],
                common_traps=['Inventory PMSI needs notice', 'Consumer goods automatic', '20-day grace period'],
            ),
            KnowledgeNode(
                concept_id="secured_priority",
                name="Priority Rules",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="First to file/perfect wins; PMSI super-priority; buyer in ordinary course takes free",
                elements=['First to file/perfect', 'PMSI super-priority', 'BIOC exception', 'Lien creditor'],
                policy_rationales=[],
                common_traps=['Filing beats possession if first', 'BIOC takes free with notice', 'Judgment lien priority'],
            ),
            KnowledgeNode(
                concept_id="secured_default",
                name="Default Remedies",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Upon default: take possession (self-help if no breach of peace), dispose commercially reasonable, debtor gets surplus",
                elements=['Self-help no breach peace', 'Judicial alternative', 'Commercially reasonable', 'Notice required'],
                policy_rationales=[],
                common_traps=['Breach of peace voids self-help', 'Notice before disposition', 'Strict foreclosure option'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_iowa_procedure(self):
        """1 Iowa Procedure concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="iowa_civil_procedure",
                name="Iowa Civil Procedure",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Iowa Rules largely mirror Federal but with Iowa variations; governed by Iowa Code and court rules",
                elements=['Iowa Rules Civil Procedure', 'Court Rules', 'District court', 'Appellate procedures'],
                policy_rationales=[],
                common_traps=['Not identical to federal', 'Iowa-specific timing', 'Local rules variations'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _add_torts_expansion(self):
        """Add 9 additional torts concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="torts_false_imprisonment",
                name="False Imprisonment",
                subject="torts",
                difficulty=3,
                rule_statement="False imprisonment: intentional confinement within bounded area with plaintiff's awareness or harm",
                elements=['Intent to confine', 'Actual confinement', 'No reasonable means of escape', 'Awareness or harm'],
                policy_rationales=[],
                common_traps=['Missing that threat of force suffices for confinement', 'Requiring physical barriers (words or threat can confine)', 'Forgetting that failure to release when duty exists is confinement'],
            ),
            KnowledgeNode(
                concept_id="torts_iied",
                name="Intentional Infliction of Emotional Distress",
                subject="torts",
                difficulty=4,
                rule_statement="IIED requires extreme and outrageous conduct, intent or recklessness, causing severe emotional distress",
                elements=['Extreme and outrageous', 'Intent or recklessness', 'Causation', 'Severe distress'],
                policy_rationales=['Protect emotional wellbeing', 'Limit frivolous claims'],
                common_traps=['Finding liability for mere insults (must be extreme)', 'Missing common carrier/innkeeper exception (lower threshold)', 'Forgetting physical manifestation not required'],
            ),
            KnowledgeNode(
                concept_id="torts_trespass_to_land",
                name="Trespass to Land",
                subject="torts",
                difficulty=3,
                rule_statement="Trespass requires intentional physical invasion of plaintiff's land; mistake no defense",
                elements=['Intent to enter', 'Physical invasion', "Plaintiff's land", 'No mistake defense'],
                policy_rationales=[],
                common_traps=['Requiring knowledge of trespass (intent to enter land suffices)', 'Missing that remaining after consent expires is trespass', 'Confusing trespass with nuisance (trespass is physical invasion)'],
            ),
            KnowledgeNode(
                concept_id="torts_conversion",
                name="Conversion",
                subject="torts",
                difficulty=3,
                rule_statement="Conversion: intentional serious interference with plaintiff's chattel so serious as to require defendant to pay full value",
                elements=['Intent to exercise dominion', 'Serious interference', "Plaintiff's possessory interest", 'Full value damages'],
                policy_rationales=[],
                common_traps=['Confusing conversion with trespass to chattels (conversion more serious)', 'Missing that good faith no defense to conversion', 'Forgetting that plaintiff can elect between replevin and conversion'],
            ),
            KnowledgeNode(
                concept_id="torts_defamation",
                name="Defamation (Libel vs Slander)",
                subject="torts",
                difficulty=4,
                rule_statement="Defamation: false defamatory statement communicated to third party causing harm; public figures must prove actual malice",
                elements=['Defamatory statement', 'Of and concerning plaintiff', 'Publication', 'Damages', 'Fault'],
                policy_rationales=[],
                common_traps=['Missing slander per se categories (damages presumed)', 'Forgetting actual malice standard for public figures/matters', 'Not distinguishing libel (written) from slander (spoken)'],
                # Mnemonic: SLANDER per se: Sexual misconduct, Loathsome disease, Adversely affects business, Notion of crime
            ),
            KnowledgeNode(
                concept_id="torts_privacy_torts",
                name="Privacy Torts (Four Types)",
                subject="torts",
                difficulty=4,
                rule_statement="Four privacy torts: appropriation of name/likeness, intrusion upon seclusion, public disclosure of private facts, false light",
                elements=['Appropriation', 'Intrusion', 'Public disclosure', 'False light'],
                policy_rationales=[],
                common_traps=['Confusing false light (privacy) with defamation (reputation)', 'Missing that truth is defense to false light but not public disclosure', 'Forgetting newsworthiness is defense to public disclosure'],
                # Mnemonic: AIPF: Appropriation, Intrusion, Public disclosure, False light
            ),
            KnowledgeNode(
                concept_id="torts_misrepresentation",
                name="Misrepresentation (Fraudulent, Negligent, Innocent)",
                subject="torts",
                difficulty=4,
                rule_statement="Fraudulent: knowingly false material representation with intent to induce reliance causing damages; negligent: should have known false",
                elements=['False representation', 'Material fact', 'Scienter (fraud)', 'Intent to induce', 'Justifiable reliance', 'Damages'],
                policy_rationales=[],
                common_traps=['Applying fraud to opinions (usually not actionable unless expert)', 'Missing that negligent misrep requires special relationship often', 'Confusing tort fraud with contract misrepresentation'],
            ),
            KnowledgeNode(
                concept_id="torts_vicarious_liability",
                name="Vicarious Liability",
                subject="torts",
                difficulty=4,
                rule_statement="Employer liable for employee torts within scope of employment; not liable for independent contractors except non-delegable duties",
                elements=['Employee vs independent contractor', 'Scope of employment', 'Frolic vs detour', 'Non-delegable duties'],
                policy_rationales=['Deep pocket', 'Risk distribution', 'Employer control'],
                common_traps=['Missing that employer liable even if prohibited employee conduct', 'Applying vicarious liability to independent contractors generally', 'Forgetting intentional torts can be within scope if job-related'],
            ),
            KnowledgeNode(
                concept_id="torts_joint_several_liability",
                name="Joint & Several Liability",
                subject="torts",
                difficulty=3,
                rule_statement="Multiple defendants jointly and severally liable; plaintiff can collect full amount from any defendant; contribution and indemnity available",
                elements=['Joint liability', 'Several liability', 'Contribution', 'Indemnity', 'Comparative fault rules'],
                policy_rationales=[],
                common_traps=['Missing that many states modified joint and several with comparative fault', 'Confusing contribution (pro rata share) with indemnity (full shifting)', 'Forgetting intentional tortfeasors cannot get contribution'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_torts(self):
        """Initialize torts - 14 comprehensive concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="torts_intentional_torts",
                name="Intentional Torts",
                subject="torts",
                difficulty=3,
                rule_statement="Battery, assault, false imprisonment, IIED require volitional acts with intent or substantial certainty.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Transferred intent",
                    "consent scope",
                    "shopkeeper’s privilege limits",
                ],
                # Mnemonic: BAFI²
            ),
            KnowledgeNode(
                concept_id="torts_negligence",
                name="Negligence",
                subject="torts",
                difficulty=3,
                rule_statement="Duty, breach (reasonable person or custom), actual/ proximate cause, damages.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Duty to unforeseeable plaintiffs (Cardozo vs Andrews)",
                    "res ipsa limits",
                    "superseding vs intervening causes",
                ],
                # Mnemonic: DBCD
            ),
            KnowledgeNode(
                concept_id="torts_strict_liability_and_products",
                name="Strict Liability & Products",
                subject="torts",
                difficulty=3,
                rule_statement="Strict liability for abnormally dangerous activities, wild animals; product claims under strict, negligence, warranty theories.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Product misuse vs foreseeable misuse",
                    "learned intermediary (pharma)",
                    "design vs manufacturing defects tests.",
                ],
                # Mnemonic: ADAMS
            ),
            KnowledgeNode(
                concept_id="torts_defamation_and_privacy",
                name="Defamation & Privacy",
                subject="torts",
                difficulty=3,
                rule_statement="False statements harming reputation; public concern triggers constitutional actual-fault requirements.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Opinions vs fact",
                    "public vs private figures (actual malice vs negligence)",
                    "privacy tort distinctions (intrusion",
                ],
                # Mnemonic: PDPF
            ),
            KnowledgeNode(
                concept_id="torts_economic_and_dignitary",
                name="Economic & Dignitary",
                subject="torts",
                difficulty=3,
                rule_statement="Intentional interference, fraudulent misrepresentation, malicious prosecution.",
                elements=['Rule', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Economic harm requirements",
                    "privilege defenses",
                    "probable cause in malicious prosecution.",
                ],
            ),
            KnowledgeNode(
                concept_id="torts_vicarious_liability_and_damages",
                name="Vicarious Liability & Damages",
                subject="torts",
                difficulty=3,
                rule_statement="Employers liable for employees acting in scope; punitive damages limited; joint & several vs several depending on jurisdiction.",
                elements=['Rule', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Frolic vs detour",
                    "independent contractor exceptions",
                    "collateral source rule variations",
                ],
            ),
            KnowledgeNode(
                concept_id="torts_negligence_elements",
                name="NEGLIGENCE ELEMENTS",
                subject="torts",
                difficulty=3,
                rule_statement="Negligence requires duty owed, breach by unreasonable conduct, actual and proximate causation, and damages; defenses include comparative fault, assumption of risk, statutes.",
                elements=['Duty', 'Breach', 'Causation', 'Defenses'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="torts_strict_liability_and_products_liability",
                name="STRICT LIABILITY & PRODUCTS LIABILITY",
                subject="torts",
                difficulty=3,
                rule_statement="Strict liability covers abnormally dangerous activities, wild animals, and product defects proven through manufacturing, design, or warning failure where foreseeable plaintiffs suffer harm.",
                elements=['Abnormally Dangerous', 'Products Liability', 'Defenses', 'Warranties'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="torts_duty_of_care",
                name="Duty of Care",
                subject="torts",
                difficulty=3,
                rule_statement="Defendant owes duty when conduct creates foreseeable risk",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="torts_breach__standard_of_care",
                name="Breach - Standard of Care",
                subject="torts",
                difficulty=3,
                rule_statement="Reasonable person standard; custom evidence relevant",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="torts_actual_causation",
                name="Actual Causation",
                subject="torts",
                difficulty=3,
                rule_statement="But-for test; substantial factor for multiple causes",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="torts_proximate_cause",
                name="Proximate Cause",
                subject="torts",
                difficulty=3,
                rule_statement="Foreseeable consequences; no superseding intervening causes",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="torts_intentional_torts__battery",
                name="Intentional Torts - Battery",
                subject="torts",
                difficulty=3,
                rule_statement="Intentional harmful or offensive contact",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="torts_strict_liability__animals",
                name="Strict Liability - Animals",
                subject="torts",
                difficulty=3,
                rule_statement="Owners strictly liable for wild animals",
                elements=[],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def get_subject_concepts(self, subject: str) -> List[KnowledgeNode]:
        """Get all concepts for subject"""
        return [n for n in self.nodes.values() if n.subject == subject]

    def get_concept(self, concept_id: str) -> Optional[KnowledgeNode]:
        """Get specific concept"""
        return self.nodes.get(concept_id)

# ==================== INTERLEAVED PRACTICE ENGINE ====================

    def _initialize_professional_responsibility(self):
        """26 Professional Responsibility concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="prof_resp_communication_detailed",
                name="Communication with Client",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer must reasonably inform client of status, respond to requests, explain matters for informed decisions, and communicate settlement offers promptly",
                elements=['Keep informed', 'Respond to requests', 'Explain for decisions', 'Prompt settlement communication'],
                common_traps=['Not informing of settlement offers', 'Not explaining enough', 'Missing scope decisions'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_declining_terminating",
                name="Declining & Terminating Representation",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must decline if rules violation; may withdraw for legitimate reasons; court approval if litigation; protect client interests",
                elements=['Mandatory withdrawal', 'Permissive withdrawal', 'Court approval', 'Protect interests'],
                common_traps=['No court permission in litigation', 'Not giving notice', 'Not returning property'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_safekeeping_detailed",
                name="Safekeeping Property",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Separate account required; maintain records; prompt delivery; accounting on request; disputed funds kept separate",
                elements=['Separate account (IOLTA)', 'Complete records', 'Prompt delivery', 'Accounting'],
                common_traps=['Commingling', 'Using client funds temporarily', 'Not separating disputed funds'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_advertising_detailed",
                name="Advertising & Solicitation Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May advertise if truthful; no live solicitation if significant pecuniary motive; specialization limits",
                elements=['Advertising permitted if truthful', 'No false/misleading', 'Solicitation restrictions', 'Specialization rules'],
                common_traps=['All solicitation prohibited', 'In-person to accident victims', 'Claiming specialization without certification'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_impartiality_detailed",
                name="Impartiality of Tribunal",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="No ex parte with judge; no improper jury influence; maintain decorum; no prejudicial conduct",
                elements=['No ex parte with judge', 'No improper jury influence', 'Maintain decorum', 'No prejudicial conduct'],
                common_traps=['Ex parte exceptions', 'Gifts to judges', 'Lawyer-judge commentary'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_trial_publicity_detailed",
                name="Trial Publicity Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot make statements with substantial likelihood of materially prejudicing proceeding; safe harbor statements permitted",
                elements=['Substantial likelihood test', 'Material prejudice', 'Criminal heightened', 'Safe harbor'],
                common_traps=['Public record info permitted', 'Heightened in criminal', 'First Amendment balance'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_judges_detailed",
                name="Judge & Former Judge Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Judge must maintain independence, avoid impropriety appearance; former judge cannot represent in matter participated",
                elements=['Independence', 'Impartiality', 'Disqualification', 'Former judge limits'],
                common_traps=['Former judge prior matter', 'Appearance of impropriety', 'Report misconduct duty'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_law_firms_detailed",
                name="Law Firm Responsibilities",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Partners/supervisors ensure compliance; subordinates follow rules; firm-wide measures required; conflicts imputed",
                elements=['Supervisory duties', 'Subordinate duties', 'Firm measures', 'Conflict imputation'],
                common_traps=['Subordinate still liable', 'Screening laterals', 'Firm name restrictions'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_unauthorized_practice",
                name="Unauthorized Practice of Law",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer cannot practice where not admitted; cannot assist non-lawyer in unauthorized practice; multijurisdictional practice rules",
                elements=['Admission requirements', 'No assisting non-lawyers', 'MJP exceptions', 'Pro hac vice'],
                common_traps=['MJP exceptions', 'Temporary practice', 'Assisting UPL'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_sale_law_practice",
                name="Sale of Law Practice",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May sell practice if: entire practice or area sold, written client notice, fees not increased",
                elements=['Entire practice or area', 'Written notice', 'No fee increase', 'Client consent'],
                common_traps=['Must sell entire area', 'Client can reject', 'Cannot increase fees'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_reporting_misconduct",
                name="Reporting Professional Misconduct",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer must report other lawyer's violations raising substantial question about honesty, trustworthiness, fitness",
                elements=['Must report violations', 'Substantial question test', 'Confidentiality exceptions', 'Self-reporting'],
                common_traps=['Confidentiality not absolute', 'Substantial question threshold', 'Judge misconduct reporting'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_disciplinary_procedures",
                name="Disciplinary Procedures",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="State supreme court inherent authority; disciplinary board investigates; sanctions range from private reprimand to disbarment",
                elements=['Supreme court authority', 'Investigation process', 'Sanctions range', 'Reciprocal discipline'],
                common_traps=['Inherent authority', 'Burden of proof', 'Reciprocal discipline rules'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_multijurisdictional",
                name="Multijurisdictional Practice",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="May practice temporarily if: related to admitted practice, arbitration/mediation, reasonably related to practice, pro hac vice",
                elements=['Temporary practice exceptions', 'Related to home practice', 'Pro hac vice', 'Systematic presence prohibited'],
                common_traps=['Cannot establish office', 'Related to home practice', 'Temporary only'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_litigation_conduct",
                name="Conduct in Litigation",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must not: abuse discovery, fail to disclose controlling authority, falsify evidence, make frivolous claims",
                elements=['No discovery abuse', 'Disclose adverse authority', 'No false evidence', 'No frivolous claims'],
                common_traps=['Adverse authority in controlling jurisdiction', 'Discovery proportionality', 'Good faith extensions OK'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_transactions_with_client",
                name="Business Transactions with Clients",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot enter business transaction unless: terms fair and reasonable, disclosed in writing, client has independent counsel opportunity, client consents in writing",
                elements=['Fair and reasonable', 'Written disclosure', 'Independent counsel opportunity', 'Written consent'],
                common_traps=['All four required', 'Full disclosure needed', 'Independent counsel chance'],
                # Mnemonic: FICO: Fair, Independent counsel, Consent, Opportunity
            ),
            KnowledgeNode(
                concept_id="prof_resp_literary_rights",
                name="Literary & Media Rights",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot acquire literary or media rights to representation before conclusion; may contract for reasonable expenses of publication after conclusion",
                elements=['No rights before conclusion', 'May contract after', 'Reasonable expenses only', 'Avoid conflict'],
                common_traps=['Timing - must wait until conclusion', 'May negotiate after', 'Conflict of interest concern'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_financial_assistance",
                name="Financial Assistance to Client",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot provide financial assistance except: advance court costs and expenses, contingent on outcome; may pay costs for indigent client",
                elements=['May advance costs', 'Repayment contingent on outcome', 'May pay for indigent', 'No personal living expenses'],
                common_traps=['Cannot advance living expenses', 'Can advance litigation costs', 'Indigent exception'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_former_government_lawyer",
                name="Former Government Lawyer",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent in matter personally and substantially participated in as government lawyer; screening can cure; cannot use confidential government information",
                elements=['Personally and substantially test', 'Screening available', 'No confidential info use', 'Negotiating employment'],
                common_traps=['Screening can cure conflict', 'Personal and substantial both required', 'Confidential info permanent bar'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_former_judge_arbitrator",
                name="Former Judge or Arbitrator",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent anyone in matter participated in as judge, arbitrator, mediator, or other neutral; screening cannot cure",
                elements=['Cannot represent in prior matter', 'Participated as neutral', 'Screening cannot cure', 'Negotiating employment restriction'],
                common_traps=['Screening does NOT cure (unlike gov lawyer)', 'Participated in any capacity', 'Negotiating employment limits'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_imputed_conflicts",
                name="Imputation of Conflicts",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Lawyer conflicts imputed to all in firm unless: personal interest, former client with screening, former government lawyer with screening",
                elements=['General imputation rule', 'Personal interest exception', 'Former client screening', 'Government lawyer screening'],
                common_traps=['Three main exceptions', 'Screening procedures', 'Timely screening required'],
                # Mnemonic: PFG: Personal, Former client, Government (exceptions to imputation)
            ),
            KnowledgeNode(
                concept_id="prof_resp_nonlawyer_assistants",
                name="Responsibilities for Nonlawyer Assistants",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer responsible for nonlawyer assistants' conduct; must ensure compliance with professional rules; cannot delegate legal judgment",
                elements=['Supervisory responsibility', 'Ensure compliance', 'Cannot delegate legal judgment', 'Ethical violations imputed'],
                common_traps=['Lawyer still responsible', 'Cannot avoid by delegation', 'Must supervise adequately'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_fee_division",
                name="Fee Division with Lawyers",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May divide fee with another lawyer if: proportional to services or joint responsibility, client agrees in writing, total fee reasonable",
                elements=['Proportional or joint responsibility', 'Written client agreement', 'Total fee reasonable', 'No division with non-lawyer'],
                common_traps=['Proportion or responsibility both OK', 'Client must agree', 'Cannot divide with non-lawyer'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_aggregate_settlements",
                name="Aggregate Settlements",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot participate in aggregate settlement unless each client gives informed consent in writing after disclosure of all material terms",
                elements=['Each client must consent', 'Informed consent', 'Written', 'Disclosure of all terms'],
                common_traps=['Every client must agree', 'Full disclosure required', 'Cannot coerce holdouts'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_limiting_liability",
                name="Limiting Liability & Malpractice",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot prospectively limit malpractice liability unless client independently represented; may settle malpractice claim if client advised to seek independent counsel",
                elements=['No prospective limits without independent counsel', 'May settle if advised', 'Full disclosure required', 'Independent advice'],
                common_traps=['Prospective limits rare', 'Settlement requires advice', 'Independent counsel key'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_sexual_relations",
                name="Sexual Relations with Clients",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot have sexual relations with client unless consensual relationship existed before attorney-client relationship",
                elements=['Prohibited unless preexisting', 'Consent not defense', 'Exploitation concern', 'Impairs judgment'],
                policy_rationales=['Prevent exploitation', 'Avoid conflicts', 'Protect judgment'],
                common_traps=['Preexisting relationship exception only', 'Consent insufficient', 'Judgment impairment'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_appearance_of_impropriety",
                name="Appearance of Impropriety",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer should avoid even appearance of impropriety; upholds confidence in legal profession; aspirational standard",
                elements=['Avoid appearance', 'Public confidence', 'Aspirational', 'Reasonable person test'],
                common_traps=['Aspirational not enforceable alone', 'Reasonable person view', 'Supplements specific rules'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_corporations(self):
        """27 Corporations concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="corp_promoter_liability",
                name="Promoter Liability",
                subject="corporations",
                difficulty=3,
                rule_statement="Promoter liable on pre-incorporation contracts unless novation; corporation liable if adopts contract expressly or impliedly",
                elements=['Promoter personally liable', 'Corporation liable if adopts', 'Novation releases promoter', 'Implied adoption'],
                common_traps=['Both can be liable', "Adoption doesn't release", 'Need novation for release'],
            ),
            KnowledgeNode(
                concept_id="corp_defective_incorporation",
                name="Defective Incorporation",
                subject="corporations",
                difficulty=3,
                rule_statement="De facto corporation: good faith attempt, actual use; corporation by estoppel: held out as corporation, third party dealt as such",
                elements=['De facto corporation', 'Corporation by estoppel', 'Good faith attempt', 'Actual use'],
                common_traps=['Both doctrines exist', 'Protects from personal liability', 'Narrow application'],
            ),
            KnowledgeNode(
                concept_id="corp_ultra_vires",
                name="Ultra Vires Acts",
                subject="corporations",
                difficulty=2,
                rule_statement="Acts beyond corporate powers; generally enforceable but shareholders can enjoin, corporation can sue officers, state can dissolve",
                elements=['Beyond stated purpose', 'Generally enforceable', 'Limited remedies', 'Rare doctrine'],
                common_traps=['Contract still enforceable', 'Internal remedy', 'Rarely succeeds'],
            ),
            KnowledgeNode(
                concept_id="corp_subscriptions",
                name="Stock Subscriptions",
                subject="corporations",
                difficulty=3,
                rule_statement="Pre-incorporation subscription irrevocable for six months unless otherwise provided; post-incorporation governed by contract law",
                elements=['Pre-incorporation irrevocable', 'Six month rule', 'Post-incorporation contract', 'Payment terms'],
                common_traps=['Pre vs post timing', 'Irrevocability period', 'Contract law post-incorporation'],
            ),
            KnowledgeNode(
                concept_id="corp_consideration_shares",
                name="Consideration for Shares",
                subject="corporations",
                difficulty=3,
                rule_statement="Par value: must receive at least par; no-par: any consideration; watered stock: directors liable; good faith business judgment protects valuation",
                elements=['Par value minimum', 'No-par flexibility', 'Watered stock liability', 'Business judgment valuation'],
                common_traps=['Par vs no-par', 'Director liability watered stock', 'BJR protects valuation'],
            ),
            KnowledgeNode(
                concept_id="corp_preemptive_rights",
                name="Preemptive Rights",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders may have right to purchase new shares to maintain proportional ownership; must be expressly granted in modern law",
                elements=['Maintain proportional ownership', 'Must be in articles', 'Pro rata purchase right', 'Exceptions exist'],
                common_traps=['Must be expressly granted', 'Not automatic', 'Exceptions for compensation'],
            ),
            KnowledgeNode(
                concept_id="corp_distributions_dividends",
                name="Distributions & Dividends",
                subject="corporations",
                difficulty=3,
                rule_statement="Directors declare dividends using business judgment; unlawful if: insolvent, would cause insolvency, or exceeds statutory limits",
                elements=['Board discretion', 'Insolvency test', 'Statutory limits', 'Director liability'],
                common_traps=['Directors discretion wide', 'Insolvency prohibition', 'Directors personally liable'],
            ),
            KnowledgeNode(
                concept_id="corp_inspection_rights",
                name="Shareholder Inspection Rights",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders have right to inspect books and records for proper purpose; shareholder list more readily available than detailed financial records",
                elements=['Proper purpose required', 'Shareholder list easier', 'Books and records harder', 'Advance notice'],
                common_traps=['Proper purpose test', 'Different standards for different records', 'Timing requirements'],
            ),
            KnowledgeNode(
                concept_id="corp_meetings_notice",
                name="Meetings & Notice Requirements",
                subject="corporations",
                difficulty=2,
                rule_statement="Annual shareholders meeting required; notice required with time, place, purpose if special; directors can act without meeting if unanimous written consent",
                elements=['Annual meeting required', 'Notice requirements', 'Special meeting purpose', 'Written consent alternative'],
                common_traps=['Notice timing', 'Special meeting purpose specificity', 'Unanimous consent option'],
            ),
            KnowledgeNode(
                concept_id="corp_quorum_voting",
                name="Quorum & Voting Rules",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders: majority of shares is quorum, majority of votes present wins; Directors: majority of directors is quorum, majority of votes present wins",
                elements=['Shareholder quorum', 'Director quorum', 'Vote requirements', 'Can modify in articles/bylaws'],
                common_traps=['Quorum vs voting', 'Can change by agreement', 'Present vs outstanding'],
            ),
            KnowledgeNode(
                concept_id="corp_removal_directors",
                name="Removal of Directors",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders may remove with or without cause unless articles require cause; if cumulative voting, can remove only if votes sufficient to elect",
                elements=['Shareholder removal power', 'With or without cause', 'Cumulative voting protection', 'Articles can require cause'],
                common_traps=['Unless articles require cause', 'Cumulative voting protection', 'Only shareholders remove'],
            ),
            KnowledgeNode(
                concept_id="corp_indemnification",
                name="Indemnification of Directors/Officers",
                subject="corporations",
                difficulty=4,
                rule_statement="Mandatory if successful on merits; permissive if good faith and reasonable belief; prohibited if found liable to corporation",
                elements=['Mandatory if successful', 'Permissive if good faith', 'Prohibited if liable', 'Advancement of expenses'],
                common_traps=['Three categories', 'Successful = mandatory', 'Liable to corp = prohibited'],
                # Mnemonic: MAP: Mandatory, Allowed, Prohibited
            ),
            KnowledgeNode(
                concept_id="corp_close_corporations",
                name="Close Corporations",
                subject="corporations",
                difficulty=3,
                rule_statement="Few shareholders, no public market, restrictions on transfer; may operate informally; special statutory provisions protect minority",
                elements=['Few shareholders', 'Transfer restrictions', 'Informal operation allowed', 'Minority protection'],
                common_traps=['Can dispense with formalities', 'Oppression remedies', 'Statutory protections'],
            ),
            KnowledgeNode(
                concept_id="corp_shareholder_agreements",
                name="Shareholder Agreements",
                subject="corporations",
                difficulty=3,
                rule_statement="May restrict transfers, provide for management, require arbitration; must not treat corporation as partnership or injure creditors",
                elements=['Voting agreements', 'Buy-sell provisions', 'Transfer restrictions', 'Management agreements'],
                common_traps=['Cannot sterilize board', 'Must protect creditors', 'Binding on parties only'],
            ),
            KnowledgeNode(
                concept_id="corp_oppression_freeze_out",
                name="Oppression & Freeze-Out",
                subject="corporations",
                difficulty=4,
                rule_statement="Majority cannot squeeze out minority unfairly; remedies include buyout, dissolution, or damages; courts balance reasonable expectations",
                elements=['Oppressive conduct', 'Reasonable expectations', 'Buyout remedy', 'Dissolution alternative'],
                policy_rationales=['Protect minority', 'Prevent abuse of control', 'Balance interests'],
                common_traps=['Reasonable expectations test', 'Equitable remedies', 'Close corporation context'],
            ),
            KnowledgeNode(
                concept_id="corp_dividends_preferred",
                name="Preferred Stock Dividends",
                subject="corporations",
                difficulty=3,
                rule_statement="Preferred entitled to fixed dividend before common; cumulative unless stated non-cumulative; participating if so stated",
                elements=['Priority over common', 'Cumulative presumption', 'Participating possibility', 'Liquidation preference'],
                common_traps=['Cumulative unless stated otherwise', 'Arrears must be paid first', 'Participating rare'],
            ),
            KnowledgeNode(
                concept_id="corp_redemption_repurchase",
                name="Redemption & Share Repurchase",
                subject="corporations",
                difficulty=3,
                rule_statement="Corporation may repurchase shares if: not insolvent, adequate surplus; redemption rights if stated; insider trading concerns",
                elements=['Must have surplus', 'Insolvency test', 'Redemption vs repurchase', 'Insider trading risk'],
                common_traps=['Statutory requirements', 'Cannot make insolvent', 'Insider trading prohibition'],
            ),
            KnowledgeNode(
                concept_id="corp_sale_of_assets",
                name="Sale of Substantially All Assets",
                subject="corporations",
                difficulty=4,
                rule_statement="Requires board and shareholder approval; not ordinary course of business; selling corporation continues to exist; buyers can assume liabilities",
                elements=['Substantially all assets', 'Board and shareholder vote', 'Continues to exist', 'Successor liability rules'],
                common_traps=['Substantially all test', 'Continues to exist', 'Not automatic successor liability'],
            ),
            KnowledgeNode(
                concept_id="corp_tender_offers",
                name="Tender Offers",
                subject="corporations",
                difficulty=3,
                rule_statement="Offer to buy shares directly from shareholders; federal regulation; target board may defend; business judgment rule applies to defensive measures",
                elements=['Direct to shareholders', 'Federal securities law', 'Board defensive tactics', 'BJR applies'],
                common_traps=['Bypass board', 'Defensive measures reviewed', 'Unocal standard may apply'],
            ),
            KnowledgeNode(
                concept_id="corp_proxy_fights",
                name="Proxy Contests",
                subject="corporations",
                difficulty=3,
                rule_statement="Contest for board control via shareholder votes; federal proxy rules; corporation may reimburse incumbents; insurgents reimbursed if successful",
                elements=['Board control contest', 'Proxy solicitation rules', 'Reimbursement rules', 'Disclosure requirements'],
                common_traps=['Corporation can reimburse incumbents', 'Insurgents if successful', 'Federal regulation applies'],
            ),
            KnowledgeNode(
                concept_id="corp_hostile_takeovers",
                name="Hostile Takeovers & Defensive Tactics",
                subject="corporations",
                difficulty=4,
                rule_statement="Target board may defend using business judgment; must show reasonable threat and proportionate response; cannot be entrenching",
                elements=['Unocal standard', 'Reasonable threat', 'Proportionate response', 'Enhanced scrutiny'],
                common_traps=['Enhanced scrutiny', 'Cannot be entrenching', 'Proportionality key'],
                # Mnemonic: PRE: Proportionate, Reasonable threat, Enhanced scrutiny
            ),
            KnowledgeNode(
                concept_id="corp_appraisal_rights",
                name="Appraisal Rights",
                subject="corporations",
                difficulty=4,
                rule_statement="Dissenting shareholders entitled to fair value of shares in: mergers, sales of assets, amendments materially affecting rights",
                elements=['Fair value determination', 'Dissent and notice required', 'Exclusive remedy', 'Triggering events'],
                common_traps=['Must follow procedures exactly', 'Fair value not market value', 'Exclusive remedy if available'],
            ),
            KnowledgeNode(
                concept_id="corp_amendments_articles",
                name="Amending Articles of Incorporation",
                subject="corporations",
                difficulty=2,
                rule_statement="Requires board approval and shareholder vote; certain amendments require class vote if materially affect class",
                elements=['Board approval', 'Shareholder vote', 'Class voting rights', 'Filing required'],
                common_traps=['Class vote for material changes to class', 'Filing makes effective', 'Broad board power'],
            ),
            KnowledgeNode(
                concept_id="corp_bylaws",
                name="Bylaws",
                subject="corporations",
                difficulty=2,
                rule_statement="Internal operating rules; typically adopted/amended by board unless articles reserve to shareholders; cannot conflict with articles or statutes",
                elements=['Internal rules', 'Board typically amends', 'Cannot conflict with articles', 'Operating procedures'],
                common_traps=['Board power unless reserved', 'Hierarchy: statute > articles > bylaws', 'Cannot expand powers'],
            ),
            KnowledgeNode(
                concept_id="corp_limited_liability_company",
                name="Limited Liability Companies (LLC)",
                subject="corporations",
                difficulty=3,
                rule_statement="Hybrid entity: corporate limited liability plus partnership flexibility; operating agreement governs; default rules vary by state",
                elements=['Limited liability', 'Pass-through taxation', 'Operating agreement', 'Flexible management'],
                common_traps=['Operating agreement controls', 'Default rules vary', 'Veil piercing still possible'],
            ),
            KnowledgeNode(
                concept_id="corp_partnerships_general",
                name="General Partnerships",
                subject="corporations",
                difficulty=3,
                rule_statement="Formation by agreement or co-ownership for profit; each partner agent; jointly and severally liable; equal sharing unless agreed",
                elements=['No formalities', 'Each partner agent', 'Unlimited liability', 'Equal sharing default'],
                common_traps=['Joint and several liability', 'Each partner can bind', 'No filing required'],
            ),
            KnowledgeNode(
                concept_id="corp_limited_partnerships",
                name="Limited Partnerships",
                subject="corporations",
                difficulty=3,
                rule_statement="General partners manage and liable; limited partners passive investors with liability limited to investment; filing required",
                elements=['GP manages and liable', 'LP limited liability', 'Filing required', 'LP cannot control'],
                common_traps=['LP control destroys limited liability', 'Must file certificate', 'GP fully liable'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_wills_trusts_estates(self):
        """37 Wills Trusts Estates concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="wills_capacity",
                name="Testamentary Capacity",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Testator must be 18+, understand nature of act, extent of property, natural objects of bounty, plan of disposition",
                elements=['Age 18+', 'Understand nature', 'Know property', 'Natural objects', 'Dispositional plan'],
                common_traps=['Lower standard than contractual', 'Lucid intervals count', 'Burden on contestants'],
                # Mnemonic: PENDO: Property, Estate, Nature, Disposition, Objects
            ),
            KnowledgeNode(
                concept_id="wills_attestation",
                name="Attestation & Witnesses",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Two witnesses must attest; must be present at same time; interested witness issues; purging statutes may apply",
                elements=['Two witnesses', 'Simultaneous presence', 'Sign in testator presence', 'Competent witnesses'],
                common_traps=['Line of sight test', 'Interested witness loses bequest', 'Purging statutes'],
            ),
            KnowledgeNode(
                concept_id="wills_codicil",
                name="Codicils",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Testamentary instrument that modifies will; must meet same formalities; republishes will as of codicil date",
                elements=['Modifies existing will', 'Same formalities required', 'Republication effect', 'Integration'],
                common_traps=['Republication doctrine', 'Cures defects in will', 'Must meet formalities'],
            ),
            KnowledgeNode(
                concept_id="wills_incorporation_reference",
                name="Incorporation by Reference",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="External document incorporated if: exists when will executed, will manifests intent, will describes sufficiently",
                elements=['Document must exist', 'Intent to incorporate', 'Sufficient description', 'Extrinsic evidence'],
                common_traps=['Must exist at execution', 'Cannot incorporate future documents', 'Description requirement'],
            ),
            KnowledgeNode(
                concept_id="wills_acts_of_independent_significance",
                name="Acts of Independent Significance",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Will can refer to acts/events with significance apart from testamentary effect; non-testamentary motive required",
                elements=['Independent significance', 'Non-testamentary purpose', 'Changes effective', 'Common examples'],
                common_traps=['Must have independent purpose', 'Contents of wallet example', 'Beneficiary designation'],
            ),
            KnowledgeNode(
                concept_id="wills_holographic",
                name="Holographic Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Handwritten, signed, material provisions in testator handwriting; no witnesses required in states recognizing",
                elements=['Handwritten', 'Signed', 'Material provisions', 'No witnesses'],
                common_traps=['Not all states recognize', 'Material portions test', 'Intent to be will'],
            ),
            KnowledgeNode(
                concept_id="wills_conditional",
                name="Conditional Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Will effective only if condition occurs; distinguishing condition of execution from condition of revocation",
                elements=['Condition must occur', 'Condition vs motive', 'Extrinsic evidence', 'Interpretation issues'],
                common_traps=['Condition vs motive', 'Presumption against conditional', 'Proof required'],
            ),
            KnowledgeNode(
                concept_id="wills_revocation_dependent_relative",
                name="Dependent Relative Revocation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revocation ineffective if based on mistake of law/fact and would not have revoked but for mistake",
                elements=['Mistaken revocation', 'Would not have revoked', 'Testator intent', 'Second-best result'],
                common_traps=['Applies when mistake', 'Second best over intestacy', 'Intent focus'],
            ),
            KnowledgeNode(
                concept_id="wills_revival",
                name="Revival of Revoked Wills",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="When revoking instrument revoked, three approaches: automatic revival, testator intent, no revival absent re-execution",
                elements=['Revocation of revocation', 'Majority: intent controls', 'Minority: automatic', 'Minority: re-execution'],
                common_traps=['State law varies', 'Intent evidence', 'May need re-execution'],
            ),
            KnowledgeNode(
                concept_id="wills_lapse_anti_lapse",
                name="Lapse & Anti-Lapse",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Bequest lapses if beneficiary predeceases; anti-lapse saves gift if beneficiary in protected class and leaves issue",
                elements=['Lapse when predecease', 'Anti-lapse statute', 'Protected class', 'Issue substitute'],
                common_traps=['Protected class varies', 'Issue requirement', 'Express contrary intent'],
                # Mnemonic: ACID: Anti-lapse, Class, Issue, Descendants
            ),
            KnowledgeNode(
                concept_id="wills_ademption",
                name="Ademption by Extinction",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Specific gift adeemed if not in estate at death; identity theory vs intent theory",
                elements=['Specific gift only', 'Not in estate', 'Identity theory', 'Intent theory minority'],
                common_traps=['Specific vs general/demonstrative', 'Exceptions may apply', 'Insurance proceeds'],
            ),
            KnowledgeNode(
                concept_id="wills_ademption_satisfaction",
                name="Ademption by Satisfaction",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Lifetime gift to beneficiary may satisfy testamentary gift if: writing by testator, writing by beneficiary, or property declares satisfaction",
                elements=['Lifetime gift', 'Testamentary gift', 'Writing requirement', 'Intent to satisfy'],
                common_traps=['Need writing', 'Presumption against', 'Value determination'],
            ),
            KnowledgeNode(
                concept_id="wills_abatement",
                name="Abatement",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Reduce gifts when assets insufficient; order: intestate property, residuary, general, demonstrative, specific",
                elements=['Insufficient assets', 'Priority order', 'Pro rata within class', 'Can change by will'],
                common_traps=['Standard order', 'Pro rata reduction', 'Will can change'],
                # Mnemonic: IRGDS: Intestate, Residuary, General, Demonstrative, Specific (reverse priority)
            ),
            KnowledgeNode(
                concept_id="wills_exoneration",
                name="Exoneration of Liens",
                subject="wills_trusts_estates",
                difficulty=2,
                rule_statement="Traditional: estate pays off liens; Modern UPC: beneficiary takes subject to liens unless will directs payment",
                elements=['Liens on specific gifts', 'Traditional: estate pays', 'UPC: beneficiary takes with', 'Will can direct'],
                common_traps=['UPC changed rule', 'Specific direction needed', 'Mortgage example'],
            ),
            KnowledgeNode(
                concept_id="wills_pretermitted_spouse",
                name="Pretermitted Spouse",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Spouse married after will takes intestate share unless: will contemplates marriage, provided for outside will, intentionally omitted",
                elements=['After-will marriage', 'Intestate share', 'Three exceptions', 'Intent evidence'],
                common_traps=['Exceptions apply', 'Burden of proof', 'Not divorce'],
            ),
            KnowledgeNode(
                concept_id="wills_pretermitted_children",
                name="Pretermitted Children",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Child born/adopted after will takes share unless: intentional omission shown, provided for outside will, or all to other parent",
                elements=['After-will child', 'Share calculation', 'Three exceptions', 'All estate to parent exception'],
                common_traps=['Share calculation complex', 'All-to-parent exception', 'Adopted children included'],
            ),
            KnowledgeNode(
                concept_id="wills_elective_share",
                name="Elective Share",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Surviving spouse can elect statutory share (typically 1/3 or 1/2) instead of will provision; time limit applies",
                elements=['Statutory percentage', 'Augmented estate', 'Time to elect', 'Cannot waive before marriage'],
                common_traps=['Augmented estate includes transfers', 'Time limit strict', 'Prenup can waive'],
            ),
            KnowledgeNode(
                concept_id="wills_undue_influence",
                name="Undue Influence",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Substituted will of influencer for testator; requires: susceptibility, opportunity, disposition to influence, unnatural result",
                elements=['Susceptibility', 'Opportunity', 'Active procurement', 'Unnatural result'],
                common_traps=['Four elements', 'Burden on contestant', 'Presumption if confidential relation + benefit'],
            ),
            KnowledgeNode(
                concept_id="wills_fraud",
                name="Fraud",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="False statement material to testamentary disposition; fraud in execution vs inducement; constructive trust remedy",
                elements=['False representation', 'Known false', 'Testator reliance', 'Material'],
                common_traps=['Fraud in execution vs inducement', 'Constructive trust remedy', 'High burden'],
            ),
            KnowledgeNode(
                concept_id="wills_mistake",
                name="Mistake",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Mistake in execution may void; mistake in inducement generally not correctable; reformation limited",
                elements=['Mistake in execution', 'Mistake in inducement', 'Limited correction', 'Omitted text'],
                common_traps=['In execution voids', 'In inducement usually no remedy', 'Rare reformation'],
            ),
            KnowledgeNode(
                concept_id="wills_joint_mutual",
                name="Joint & Mutual Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Joint: one document for multiple testators; Mutual: reciprocal provisions; contract not to revoke requires clear evidence",
                elements=['Joint will', 'Mutual wills', 'Contract not to revoke', 'Proof required'],
                common_traps=['Presumption against contract', 'Must prove agreement', 'Remedy: constructive trust'],
            ),
            KnowledgeNode(
                concept_id="trusts_inter_vivos",
                name="Inter Vivos Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Created during settlor lifetime; requires delivery; can be revocable or irrevocable; avoids probate",
                elements=['Lifetime creation', 'Delivery required', 'Revocability', 'Probate avoidance'],
                common_traps=['Delivery requirement', 'Revocable unless stated', 'Pour-over wills'],
            ),
            KnowledgeNode(
                concept_id="trusts_testamentary",
                name="Testamentary Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Created by will; effective at death; must meet will formalities; subject to probate",
                elements=['Created by will', 'Will formalities', 'Effective at death', 'Probate required'],
                common_traps=['Will formalities apply', 'Goes through probate', 'Court supervision'],
            ),
            KnowledgeNode(
                concept_id="trusts_spendthrift",
                name="Spendthrift Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Beneficiary cannot transfer interest; creditors cannot reach; exceptions: certain creditors, excess beyond support",
                elements=['Transfer restraint', 'Creditor protection', 'Express provision needed', 'Exceptions exist'],
                common_traps=['Must be express', 'Exception creditors', 'Self-settled issues'],
            ),
            KnowledgeNode(
                concept_id="trusts_discretionary",
                name="Discretionary Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Trustee has discretion over distributions; standard may be absolute or limited; creditor protection",
                elements=['Trustee discretion', 'Absolute vs limited', 'Judicial review limited', 'Creditor protection'],
                common_traps=['Abuse of discretion standard', 'Good faith required', 'Creditor protection strong'],
            ),
            KnowledgeNode(
                concept_id="trusts_support",
                name="Support Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Trustee must distribute for support; mandatory if within standard; creditors providing necessaries can reach",
                elements=['Mandatory distributions', 'Support standard', 'Necessaries creditors', 'Interpretation'],
                common_traps=['Mandatory nature', 'Necessaries exception', 'Standard interpretation'],
            ),
            KnowledgeNode(
                concept_id="trusts_resulting",
                name="Resulting Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Arises by operation of law when: purchase money resulting trust, excess corpus, failure of express trust",
                elements=['Implied by law', 'Settlor gets back', 'Purchase money', 'Failure scenarios'],
                common_traps=['Returns to settlor', 'Operation of law', 'Limited situations'],
            ),
            KnowledgeNode(
                concept_id="trusts_constructive",
                name="Constructive Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Equitable remedy for unjust enrichment; wrongdoer holds property for rightful owner; fraud, breach of duty",
                elements=['Equitable remedy', 'Unjust enrichment', 'Wrongful conduct', 'Rightful owner recovers'],
                common_traps=['Remedy not true trust', 'Flexible application', 'Prevents unjust enrichment'],
            ),
            KnowledgeNode(
                concept_id="trusts_modification",
                name="Trust Modification & Termination",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revocable: settlor can modify/terminate; Irrevocable: need consent or changed circumstances; Claflin doctrine applies",
                elements=['Revocable settlor control', 'Irrevocable restrictions', 'Claflin doctrine', 'Changed circumstances'],
                common_traps=['Material purpose test', 'Consent requirements', 'Court modification limited'],
            ),
            KnowledgeNode(
                concept_id="trusts_powers",
                name="Trustee Powers",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Express powers in instrument; implied powers necessary to accomplish purpose; statutory default powers",
                elements=['Express powers', 'Implied powers', 'Statutory powers', 'Limits on powers'],
                common_traps=['Broadly construed', 'Statutory defaults', 'Cannot violate duty'],
            ),
            KnowledgeNode(
                concept_id="trusts_duty_inform",
                name="Duty to Inform & Account",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Must keep beneficiaries informed; provide annual accounting; respond to requests; disclosure of material facts",
                elements=['Keep informed', 'Annual accounting', 'Respond to requests', 'Material facts'],
                common_traps=['Affirmative duty', 'Reasonable information', 'Cannot hide behind instrument'],
            ),
            KnowledgeNode(
                concept_id="trusts_principal_income",
                name="Principal & Income Allocation",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Distinguish principal from income; Uniform Principal & Income Act provides rules; trustee adjusting power",
                elements=['Principal vs income', 'UPAIA rules', 'Adjusting power', 'Life tenant/remainder split'],
                common_traps=['UPAIA default rules', 'Power to adjust', 'Impartiality duty'],
            ),
            KnowledgeNode(
                concept_id="trusts_breach_remedies",
                name="Breach of Trust & Remedies",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Trustee liable for breach; remedies: damages, remove trustee, constructive trust, tracing; defenses: consent, exculpation clause",
                elements=['Liability for breach', 'Multiple remedies', 'Defenses available', 'Statute of limitations'],
                common_traps=['Multiple remedies possible', 'Exculpation limits', 'Consent defense'],
            ),
            KnowledgeNode(
                concept_id="rule_against_perpetuities",
                name="Rule Against Perpetuities",
                subject="wills_trusts_estates",
                difficulty=5,
                rule_statement="Interest must vest or fail within life in being plus 21 years; applies to contingent remainders, executory interests; reform statutes exist",
                elements=['Measuring lives', '21 year period', 'Must vest or fail', 'Contingent interests'],
                common_traps=['Contingent interests only', 'Reform statutes', 'Wait and see', 'Cy pres'],
                # Mnemonic: RAP applies to: contingent remainders, executory interests, class gifts, options, rights of first refusal
            ),
            KnowledgeNode(
                concept_id="powers_of_appointment",
                name="Powers of Appointment",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="General: appointee can appoint to self, estate, creditors; Special: limited class; affects estate taxation and creditors",
                elements=['General power', 'Special power', 'Exercise methods', 'Tax consequences'],
                common_traps=['General vs special', 'Default appointments', 'Tax implications'],
            ),
            KnowledgeNode(
                concept_id="estate_administration",
                name="Estate Administration Process",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Probate process: petition, notice, inventory, pay debts, distribute; executor/administrator duties; court supervision",
                elements=['Petition for probate', 'Notice to heirs', 'Inventory and appraisal', 'Pay debts then distribute'],
                common_traps=['Priority of payments', 'Creditor claims period', 'Accounting requirements'],
            ),
            KnowledgeNode(
                concept_id="nonprobate_transfers",
                name="Non-Probate Transfers",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Avoid probate: joint tenancy, POD/TOD accounts, life insurance, trusts; creditor rights may still apply",
                elements=['Joint tenancy', 'POD/TOD', 'Life insurance', 'Trust assets'],
                common_traps=['Avoid probate but not taxes', 'Creditor rights', "Will provisions don't control"],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_family_law(self):
        """25 Family Law concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="family_annulment",
                name="Annulment",
                subject="family_law",
                difficulty=3,
                rule_statement="Void marriage: bigamy, incest, mental incapacity; Voidable: age, impotence, fraud, duress, lack of consent",
                elements=['Void ab initio', 'Voidable until annulled', 'Grounds vary', 'Retroactive effect'],
                common_traps=['Void vs voidable', 'Retroactive effect', 'Property rights may survive'],
            ),
            KnowledgeNode(
                concept_id="family_separation",
                name="Legal Separation",
                subject="family_law",
                difficulty=2,
                rule_statement="Court-approved living apart; addresses support, property, custody; marriage continues; bars filed by separated spouse",
                elements=['Marriage continues', 'Court order', 'Same issues as divorce', 'Can convert to divorce'],
                common_traps=['Not divorce', 'Marriage continues', 'Same relief available'],
            ),
            KnowledgeNode(
                concept_id="family_jurisdiction",
                name="Divorce Jurisdiction",
                subject="family_law",
                difficulty=3,
                rule_statement="Divorce: domicile of one spouse; Property: in personam jurisdiction; Custody: UCCJEA home state",
                elements=['Domicile for divorce', 'Personal jurisdiction for property', 'UCCJEA for custody', 'Residency requirements'],
                common_traps=['Different jurisdiction rules', 'Divisible divorce', 'UCCJEA controls custody'],
            ),
            KnowledgeNode(
                concept_id="family_uccjea",
                name="UCCJEA Jurisdiction",
                subject="family_law",
                difficulty=4,
                rule_statement="Home state priority: where child lived 6 months before filing; significant connection if no home state; emergency jurisdiction limited",
                elements=['Home state priority', 'Significant connection', 'Emergency jurisdiction', 'Exclusive continuing jurisdiction'],
                common_traps=['Home state 6 months', 'Continuing jurisdiction', 'Emergency temporary only'],
                # Mnemonic: HSCE: Home state, Significant connection, Continuing, Emergency
            ),
            KnowledgeNode(
                concept_id="family_uifsa",
                name="UIFSA Support Enforcement",
                subject="family_law",
                difficulty=3,
                rule_statement="Uniform Interstate Family Support Act; continuing exclusive jurisdiction; direct interstate enforcement; one-order system",
                elements=['Issuing state keeps jurisdiction', 'Direct enforcement', 'No duplicate orders', 'Long-arm jurisdiction'],
                common_traps=['Continuing exclusive', 'Cannot modify elsewhere', 'Long-arm provisions'],
            ),
            KnowledgeNode(
                concept_id="family_modification_support",
                name="Modification of Support",
                subject="family_law",
                difficulty=4,
                rule_statement="Material change in circumstances required; cannot modify retroactively; voluntary unemployment may not count; burden on moving party",
                elements=['Material change', 'Prospective only', 'Substantial change', 'Voluntary acts'],
                common_traps=['Cannot modify past', 'Material change required', 'Voluntary unemployment'],
            ),
            KnowledgeNode(
                concept_id="family_modification_custody",
                name="Modification of Custody",
                subject="family_law",
                difficulty=4,
                rule_statement="Substantial change in circumstances; best interests of child; may require changed circumstances plus detrimental; restrictions on relitigation",
                elements=['Substantial change', 'Best interests', 'May need detriment', 'Time limitations'],
                common_traps=['Higher standard than initial', 'Detriment in some states', 'Relitigation restrictions'],
            ),
            KnowledgeNode(
                concept_id="family_enforcement",
                name="Support Enforcement",
                subject="family_law",
                difficulty=3,
                rule_statement="Contempt: civil or criminal; wage garnishment; license suspension; passport denial; federal locate services",
                elements=['Contempt sanctions', 'Wage withholding', 'License suspension', 'Federal enforcement'],
                common_traps=['Civil vs criminal contempt', 'Automatic withholding', 'Cannot discharge in bankruptcy'],
            ),
            KnowledgeNode(
                concept_id="family_contempt",
                name="Contempt Proceedings",
                subject="family_law",
                difficulty=3,
                rule_statement="Civil: coercive, must have ability to comply; Criminal: punitive, beyond reasonable doubt; inability to pay is defense",
                elements=['Civil coercive', 'Criminal punitive', 'Ability to pay', 'Purge conditions'],
                common_traps=['Civil vs criminal', 'Ability to pay defense', 'Burden of proof differs'],
            ),
            KnowledgeNode(
                concept_id="family_child_abuse",
                name="Child Abuse & Neglect",
                subject="family_law",
                difficulty=3,
                rule_statement="State intervention to protect child; removal requires hearing; reasonable efforts to reunify; termination of parental rights possible",
                elements=['Emergency removal', 'Court hearing', 'Reasonable efforts', 'TPR option'],
                common_traps=['Due process protections', 'Reasonable efforts', 'Clear and convincing for TPR'],
            ),
            KnowledgeNode(
                concept_id="family_termination_parental_rights",
                name="Termination of Parental Rights",
                subject="family_law",
                difficulty=4,
                rule_statement="Severs legal parent-child relationship; grounds: abuse, neglect, abandonment, unfitness; clear and convincing evidence; permanent",
                elements=['Statutory grounds', 'Clear and convincing', 'Permanent severance', 'Best interests'],
                common_traps=['High burden', 'Permanent', 'Best interests focus'],
            ),
            KnowledgeNode(
                concept_id="family_adoption",
                name="Adoption",
                subject="family_law",
                difficulty=3,
                rule_statement="Creates legal parent-child relationship; consent required from biological parents unless rights terminated; home study; finalization hearing",
                elements=['Consent requirements', 'TPR alternative', 'Home study', 'Finalization'],
                common_traps=['Consent requirements', 'Putative father rights', 'Revocation period'],
            ),
            KnowledgeNode(
                concept_id="family_paternity",
                name="Paternity Establishment",
                subject="family_law",
                difficulty=3,
                rule_statement="Voluntary acknowledgment or court determination; genetic testing presumptive; rebuttable presumptions; support and custody rights follow",
                elements=['Voluntary acknowledgment', 'Genetic testing', 'Presumptions', 'Rights and duties'],
                common_traps=['Presumptions of paternity', 'Genetic testing standard', 'Rights follow establishment'],
            ),
            KnowledgeNode(
                concept_id="family_presumptions_paternity",
                name="Presumptions of Paternity",
                subject="family_law",
                difficulty=3,
                rule_statement="Marital presumption: husband presumed father; holding out; genetic testing rebuts; multiple presumptions possible",
                elements=['Marital presumption', 'Holding out', 'Genetic testing', 'Rebuttal'],
                common_traps=['Marital presumption strong', 'Genetic testing rebuts', 'Multiple presumed fathers'],
            ),
            KnowledgeNode(
                concept_id="family_equitable_parent",
                name="Equitable Parent Doctrine",
                subject="family_law",
                difficulty=3,
                rule_statement="Non-biological parent may have rights/duties if: accepted parental role, bonded with child, parent consented; minority doctrine",
                elements=['Functional parent', 'Acceptance of role', 'Parent consent', 'Bonding'],
                common_traps=['Minority doctrine', 'Factors test', 'Parent consent key'],
            ),
            KnowledgeNode(
                concept_id="family_visitation",
                name="Visitation Rights",
                subject="family_law",
                difficulty=3,
                rule_statement="Non-custodial parent entitled to reasonable visitation unless detrimental; grandparent rights limited; supervised visitation possible",
                elements=['Reasonable visitation', 'Best interests', 'Grandparent limits', 'Supervised option'],
                common_traps=['Grandparent rights limited', 'Troxel case', 'Parental presumption'],
            ),
            KnowledgeNode(
                concept_id="family_relocation",
                name="Relocation with Child",
                subject="family_law",
                difficulty=4,
                rule_statement="Custodial parent seeking to relocate must: give notice, show legitimate reason; court balances factors; may modify custody",
                elements=['Notice requirement', 'Legitimate reason', 'Factor balancing', 'Burden on relocating parent'],
                common_traps=['Notice timing', 'Burden allocation', 'Factor tests vary'],
            ),
            KnowledgeNode(
                concept_id="family_domestic_violence",
                name="Domestic Violence",
                subject="family_law",
                difficulty=3,
                rule_statement="Protective orders available; ex parte emergency; full hearing; custody and support implications; violation is contempt/crime",
                elements=['Ex parte available', 'Full hearing', 'Relief available', 'Violation sanctions'],
                common_traps=['Ex parte standard lower', 'Custody preferences', 'Criminal violation'],
            ),
            KnowledgeNode(
                concept_id="family_protective_orders",
                name="Protective Orders",
                subject="family_law",
                difficulty=3,
                rule_statement="Restraining orders to prevent abuse; standards: immediate danger, abuse occurred; violations punishable; mutual orders disfavored",
                elements=['Standard for issuance', 'Relief available', 'Violation consequences', 'Mutual orders issue'],
                common_traps=['Standard of proof', 'Duration', 'Mutual orders problematic'],
            ),
            KnowledgeNode(
                concept_id="family_prenuptial_agreements",
                name="Prenuptial Agreements",
                subject="family_law",
                difficulty=4,
                rule_statement="Valid if: voluntary, fair disclosure, not unconscionable; cannot adversely affect child support; can waive spousal support",
                elements=['Voluntary execution', 'Financial disclosure', 'Conscionability', 'Cannot affect child support'],
                common_traps=['Full disclosure required', 'Cannot limit child support', 'Can waive spousal support'],
                # Mnemonic: VFC: Voluntary, Fair disclosure, Conscionable
            ),
            KnowledgeNode(
                concept_id="family_postnuptial_agreements",
                name="Postnuptial Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Agreement after marriage; same requirements as prenuptial plus consideration; scrutinized closely; increasing acceptance",
                elements=['After marriage', 'Consideration needed', 'Close scrutiny', 'Similar to prenup'],
                common_traps=['Need consideration', 'Higher scrutiny', 'Growing acceptance'],
            ),
            KnowledgeNode(
                concept_id="family_separation_agreements",
                name="Separation Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Negotiated settlement of divorce issues; merged into decree if approved; court reviews for fairness; child provisions always modifiable",
                elements=['Negotiated settlement', 'Court approval', 'Fairness review', 'Merger into decree'],
                common_traps=['Court must approve', 'Child provisions modifiable', 'Merger vs incorporation'],
            ),
            KnowledgeNode(
                concept_id="family_mediation",
                name="Mediation & ADR",
                subject="family_law",
                difficulty=2,
                rule_statement="Alternative dispute resolution; mediator facilitates; confidential; many jurisdictions require mediation attempt; custody mediation common",
                elements=['Facilitative process', 'Confidentiality', 'Mandatory in some places', 'Custody focus'],
                common_traps=['Confidentiality protections', 'No binding decision', 'Mandatory mediation'],
            ),
            KnowledgeNode(
                concept_id="family_tax_consequences",
                name="Tax Consequences of Divorce",
                subject="family_law",
                difficulty=3,
                rule_statement="Property transfers: generally tax-free; Alimony: post-2018 not deductible/taxable; Child support: not deductible/taxable; Dependency exemptions",
                elements=['Property transfer rules', 'Alimony tax treatment', 'Child support treatment', 'Exemptions'],
                common_traps=['2018 tax law changes', 'Property transfer tax-free', 'Child support never deductible'],
            ),
            KnowledgeNode(
                concept_id="family_bankruptcy",
                name="Bankruptcy & Family Law",
                subject="family_law",
                difficulty=3,
                rule_statement="Child support non-dischargeable; spousal support non-dischargeable; property division may be dischargeable; automatic stay exceptions",
                elements=['Support obligations survive', 'Property division varies', 'Stay exceptions', 'Priority debts'],
                common_traps=['Support never dischargeable', 'Property division in Ch 13', 'Stay exceptions'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_secured_transactions(self):
        """18 Secured Transactions concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="secured_types_collateral",
                name="Types of Collateral",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods: consumer, equipment, farm products, inventory; Intangibles: accounts, instruments, documents, chattel paper, investment property, deposit accounts",
                elements=['Goods categories', 'Intangibles', 'Classification determines rules', 'Use-based for goods'],
                common_traps=['Use determines goods classification', 'Dual-use situations', 'Transformation changes type'],
            ),
            KnowledgeNode(
                concept_id="secured_after_acquired",
                name="After-Acquired Property Clause",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Security interest attaches to after-acquired property if clause included; automatic for inventory and accounts; exception for consumer goods",
                elements=['Requires clause', 'Automatic inventory/accounts', 'Consumer goods limit', 'Attaches when acquired'],
                common_traps=['Consumer goods 10-day limit', 'Inventory automatic', 'Must have clause'],
            ),
            KnowledgeNode(
                concept_id="secured_proceeds",
                name="Proceeds",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Security interest continues in proceeds; automatically perfected for 20 days; must perfect afterward; identifiable proceeds required",
                elements=['Automatic security interest', '20-day perfection', 'Must perfect after', 'Identifiable standard'],
                common_traps=['20-day temporary perfection', 'Lowest intermediate balance rule', 'Cash proceeds'],
            ),
            KnowledgeNode(
                concept_id="secured_future_advances",
                name="Future Advances",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Security interest can secure future loans; priority from original perfection if within 45 days or committed",
                elements=['Secures future debts', 'Original priority', '45-day rule', 'Commitment'],
                common_traps=['Priority relates back', '45-day rule', 'Optional vs committed'],
            ),
            KnowledgeNode(
                concept_id="secured_bioc",
                name="Buyer in Ordinary Course",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="BIOC takes free of security interest in inventory even if perfected and knows; must be ordinary course; good faith; value given",
                elements=['Takes free', 'Inventory only', 'Ordinary course', 'Good faith + value'],
                common_traps=['Takes free even with knowledge', 'Inventory only', 'Ordinary course requirement'],
                # Mnemonic: BIOC: Buyer, Inventory, Ordinary, Course (takes free)
            ),
            KnowledgeNode(
                concept_id="secured_fixtures",
                name="Fixtures",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Personal property that becomes real property; fixture filing perfects; PMSI fixture has priority if: filed before or within 20 days, construction mortgage exception",
                elements=['Fixture definition', 'Fixture filing', 'PMSI priority', 'Construction mortgage'],
                common_traps=['20-day grace period', 'Construction mortgage wins', 'Fixture filing location'],
            ),
            KnowledgeNode(
                concept_id="secured_accessions",
                name="Accessions",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods installed in other goods; security interest continues; perfection required; removal right if no material harm",
                elements=['Continues in accession', 'Perfection needed', 'Priority rules', 'Removal rights'],
                common_traps=['First to file wins', 'Material harm test', 'PMSI super-priority'],
            ),
            KnowledgeNode(
                concept_id="secured_commingled",
                name="Commingled Goods",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods physically united in product; security interest continues in product; perfection continues; priority prorata by value",
                elements=['Continues in product', 'Perfection continues', 'Pro rata priority', 'Cannot separate'],
                common_traps=['Pro rata distribution', 'Cannot separate', 'Perfection continues'],
            ),
            KnowledgeNode(
                concept_id="secured_investment_property",
                name="Investment Property",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Securities, security entitlements, accounts; perfection by control or filing; control has priority over filing",
                elements=['Control perfection', 'Filing alternative', 'Control priority', 'Types included'],
                common_traps=['Control beats filing', 'Control methods', 'Securities intermediary'],
            ),
            KnowledgeNode(
                concept_id="secured_deposit_accounts",
                name="Deposit Accounts",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Can only perfect by control; control: secured party is bank, control agreement, or secured party is account holder",
                elements=['Control only', 'Three methods', 'No filing perfection', 'Priority by control'],
                common_traps=['Cannot perfect by filing', 'Control methods', 'Bank as secured party'],
            ),
            KnowledgeNode(
                concept_id="secured_lien_creditor",
                name="Lien Creditors",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Secured party vs lien creditor: perfected wins; unperfected loses unless PMSI grace period; trustee in bankruptcy is lien creditor",
                elements=['Perfected beats lien creditor', 'Unperfected loses', 'PMSI grace period', 'Bankruptcy trustee'],
                common_traps=['Trustee as lien creditor', 'PMSI grace period', 'Perfection timing critical'],
            ),
            KnowledgeNode(
                concept_id="secured_continuation",
                name="Continuation Statements",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Filing effective 5 years; continuation filed within 6 months before lapse; extends another 5 years",
                elements=['5-year duration', '6-month window', 'Extends 5 years', 'Must be timely'],
                common_traps=['6-month window', 'Lapses if not filed', 'Calculation of dates'],
            ),
            KnowledgeNode(
                concept_id="secured_termination",
                name="Termination Statements",
                subject="secured_transactions",
                difficulty=2,
                rule_statement="Secured party must file termination when debt paid; consumer goods: 1 month or 20 days if requested; other collateral: on demand",
                elements=['Must file when paid', 'Consumer timing', 'Non-consumer on demand', 'Penalties for failure'],
                common_traps=['Consumer timing strict', 'Must file termination', 'Failure penalties'],
            ),
            KnowledgeNode(
                concept_id="secured_assignments",
                name="Assignment of Security Interest",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Can assign security interest; need not file unless assignee wants priority over later assignee; notification to debtor",
                elements=['Assignability', 'Filing not required', 'Priority of assignees', 'Debtor notification'],
                common_traps=['Filing not required for perfection', 'Priority among assignees', 'Debtor payment rules'],
            ),
            KnowledgeNode(
                concept_id="secured_agricultural_liens",
                name="Agricultural Liens",
                subject="secured_transactions",
                difficulty=2,
                rule_statement="Non-consensual lien on farm products; perfection by filing; priority rules similar to Article 9; statute creates",
                elements=['Statutory lien', 'Farm products', 'Filing perfects', 'Similar priority'],
                common_traps=['Not security interest', 'Statutory basis', 'Filing required'],
            ),
            KnowledgeNode(
                concept_id="secured_bankruptcy_trustee",
                name="Bankruptcy Trustee Powers",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Trustee has strong-arm power: lien creditor status; can avoid unperfected interests; 90-day preference period for perfection",
                elements=['Lien creditor status', 'Avoid unperfected', '90-day preference', 'Filing relates back'],
                common_traps=['90-day preference', 'Grace period protection', 'Relates back if timely'],
            ),
            KnowledgeNode(
                concept_id="secured_preferences",
                name="Preferences in Bankruptcy",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Transfer within 90 days while insolvent that prefers creditor can be avoided; exceptions: contemporaneous exchange, ordinary course, PMSI grace",
                elements=['90-day lookback', 'Insolvency presumed', 'Preference elements', 'Exceptions'],
                common_traps=['90 days', 'PMSI grace period exception', 'Ordinary course exception'],
            ),
            KnowledgeNode(
                concept_id="secured_fraudulent_transfers",
                name="Fraudulent Transfers",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Transfer to hinder, delay, defraud creditors; transfer for less than reasonably equivalent value while insolvent; can be avoided",
                elements=['Actual fraud', 'Constructive fraud', 'Reasonably equivalent value', 'Insolvency'],
                common_traps=['Actual vs constructive', 'Timing', 'Badges of fraud'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_iowa_procedure(self):
        """15 Iowa Procedure concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="iowa_pleading",
                name="Iowa Pleading Requirements",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Iowa requires notice pleading similar to federal; original notice serves as complaint; must state claim upon which relief can be granted",
                elements=['Original notice', 'Notice pleading', 'State claim', 'Similar to federal'],
                common_traps=['Original notice terminology', 'Similar to FRCP', 'Specific Iowa forms'],
            ),
            KnowledgeNode(
                concept_id="iowa_service",
                name="Iowa Service of Process",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Personal service by sheriff or process server; substituted service available; service by publication with court approval",
                elements=['Personal service', 'Sheriff service', 'Substituted service', 'Publication service'],
                common_traps=['Sheriff preference', 'Publication requirements', 'Proof of service'],
            ),
            KnowledgeNode(
                concept_id="iowa_discovery",
                name="Iowa Discovery Rules",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Iowa discovery mirrors federal rules; interrogatories, depositions, requests for production, admissions; proportionality applies",
                elements=['Federal model', 'All federal tools', 'Proportionality', 'Protective orders'],
                common_traps=['Similar to federal', 'Iowa-specific limits', 'Timing differences'],
            ),
            KnowledgeNode(
                concept_id="iowa_summary_judgment",
                name="Iowa Summary Judgment",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Available if no genuine issue of material fact; moving party burden; view evidence in light favorable to non-movant",
                elements=['No genuine issue', 'Material fact', 'Moving party burden', 'Favorable view'],
                common_traps=['Standard similar to federal', 'Iowa case law', 'Timing requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_trial_procedures",
                name="Iowa Trial Procedures",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Jury trial right; voir dire conducted by judge typically; Iowa Rules of Evidence govern; jury instructions settled before trial",
                elements=['Jury right', 'Judge voir dire', 'Evidence rules', 'Jury instructions'],
                common_traps=['Judge-conducted voir dire', 'Iowa evidence rules', 'Pre-trial procedures'],
            ),
            KnowledgeNode(
                concept_id="iowa_appeals",
                name="Iowa Appellate Procedure",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Appeal to Iowa Court of Appeals or Supreme Court; notice of appeal within 30 days; record and brief requirements; standards of review",
                elements=['30-day deadline', 'Notice of appeal', 'Record requirements', 'Standards of review'],
                common_traps=['30-day deadline strict', 'Direct to Supreme Court options', 'Preservation requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_venue",
                name="Iowa Venue",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Proper venue: defendant residence, cause of action arose, property located, contract performed; transfer available",
                elements=['Defendant residence', 'Cause arose', 'Property location', 'Transfer possible'],
                common_traps=['Multiple proper venues', 'Transfer discretion', 'Convenience factors'],
            ),
            KnowledgeNode(
                concept_id="iowa_jurisdiction",
                name="Iowa Personal Jurisdiction",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Long-arm statute reaches constitutional limits; minimum contacts required; purposeful availment; fair play and substantial justice",
                elements=['Long-arm statute', 'Constitutional limits', 'Minimum contacts', 'Fairness test'],
                common_traps=['Constitutional analysis', 'Specific vs general', 'Stream of commerce'],
            ),
            KnowledgeNode(
                concept_id="iowa_joinder",
                name="Iowa Joinder Rules",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Permissive joinder of parties and claims; compulsory joinder of necessary parties; intervention and interpleader available",
                elements=['Permissive joinder', 'Necessary parties', 'Intervention', 'Interpleader'],
                common_traps=['Similar to federal', 'Iowa variations', 'Necessary vs indispensable'],
            ),
            KnowledgeNode(
                concept_id="iowa_class_actions",
                name="Iowa Class Actions",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Class actions permitted; requirements similar to federal; certification required; notice to class members",
                elements=['Certification requirements', 'Numerosity', 'Commonality', 'Notice'],
                common_traps=['Certification motion', 'Opt-out rights', 'Settlement approval'],
            ),
            KnowledgeNode(
                concept_id="iowa_injunctions",
                name="Iowa Injunctions",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Temporary and permanent injunctions available; requirements: likelihood of success, irreparable harm, balance of harms, public interest",
                elements=['Temporary injunction', 'Permanent injunction', 'Four factors', 'Bond requirement'],
                common_traps=['Four-factor test', 'Bond for temporary', 'Hearing requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_judgments",
                name="Iowa Judgments",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Default judgment available; directed verdict/JNOV motions; new trial motions; judgment liens; enforcement procedures",
                elements=['Default judgment', 'Post-trial motions', 'Judgment liens', 'Enforcement'],
                common_traps=['Motion timing', 'Lien procedures', 'Enforcement methods'],
            ),
            KnowledgeNode(
                concept_id="iowa_execution",
                name="Iowa Execution & Garnishment",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Execution on judgment; garnishment of wages and accounts; exemptions protect certain property; procedures for collection",
                elements=['Execution process', 'Garnishment', 'Exemptions', 'Debtor protections'],
                common_traps=['Iowa exemptions', 'Garnishment limits', 'Procedures'],
            ),
            KnowledgeNode(
                concept_id="iowa_sanctions",
                name="Iowa Sanctions",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Court may sanction frivolous filings, discovery abuse, contempt; attorney fees available; Rule 1.413 governs",
                elements=['Frivolous filings', 'Discovery sanctions', 'Contempt', 'Attorney fees'],
                common_traps=['Rule 1.413', 'Standards for sanctions', 'Safe harbor'],
            ),
            KnowledgeNode(
                concept_id="iowa_adr",
                name="Iowa ADR Procedures",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Mediation encouraged; arbitration enforceable; case management conferences; settlement conferences",
                elements=['Mediation', 'Arbitration', 'Case management', 'Settlement conferences'],
                common_traps=['Mandatory mediation in some cases', 'Arbitration enforcement', 'Confidentiality'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_professional_responsibility(self):
        """26 Professional Responsibility concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="prof_resp_communication_detailed",
                name="Communication with Client",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer must reasonably inform client of status, respond to requests, explain matters for informed decisions, and communicate settlement offers promptly",
                elements=['Keep informed', 'Respond to requests', 'Explain for decisions', 'Prompt settlement communication'],
                common_traps=['Not informing of settlement offers', 'Not explaining enough', 'Missing scope decisions'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_declining_terminating",
                name="Declining & Terminating Representation",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must decline if rules violation; may withdraw for legitimate reasons; court approval if litigation; protect client interests",
                elements=['Mandatory withdrawal', 'Permissive withdrawal', 'Court approval', 'Protect interests'],
                common_traps=['No court permission in litigation', 'Not giving notice', 'Not returning property'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_safekeeping_detailed",
                name="Safekeeping Property",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Separate account required; maintain records; prompt delivery; accounting on request; disputed funds kept separate",
                elements=['Separate account (IOLTA)', 'Complete records', 'Prompt delivery', 'Accounting'],
                common_traps=['Commingling', 'Using client funds temporarily', 'Not separating disputed funds'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_advertising_detailed",
                name="Advertising & Solicitation Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May advertise if truthful; no live solicitation if significant pecuniary motive; specialization limits",
                elements=['Advertising permitted if truthful', 'No false/misleading', 'Solicitation restrictions', 'Specialization rules'],
                common_traps=['All solicitation prohibited', 'In-person to accident victims', 'Claiming specialization without certification'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_impartiality_detailed",
                name="Impartiality of Tribunal",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="No ex parte with judge; no improper jury influence; maintain decorum; no prejudicial conduct",
                elements=['No ex parte with judge', 'No improper jury influence', 'Maintain decorum', 'No prejudicial conduct'],
                common_traps=['Ex parte exceptions', 'Gifts to judges', 'Lawyer-judge commentary'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_trial_publicity_detailed",
                name="Trial Publicity Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot make statements with substantial likelihood of materially prejudicing proceeding; safe harbor statements permitted",
                elements=['Substantial likelihood test', 'Material prejudice', 'Criminal heightened', 'Safe harbor'],
                common_traps=['Public record info permitted', 'Heightened in criminal', 'First Amendment balance'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_judges_detailed",
                name="Judge & Former Judge Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Judge must maintain independence, avoid impropriety appearance; former judge cannot represent in matter participated",
                elements=['Independence', 'Impartiality', 'Disqualification', 'Former judge limits'],
                common_traps=['Former judge prior matter', 'Appearance of impropriety', 'Report misconduct duty'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_law_firms_detailed",
                name="Law Firm Responsibilities",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Partners/supervisors ensure compliance; subordinates follow rules; firm-wide measures required; conflicts imputed",
                elements=['Supervisory duties', 'Subordinate duties', 'Firm measures', 'Conflict imputation'],
                common_traps=['Subordinate still liable', 'Screening laterals', 'Firm name restrictions'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_unauthorized_practice",
                name="Unauthorized Practice of Law",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer cannot practice where not admitted; cannot assist non-lawyer in unauthorized practice; multijurisdictional practice rules",
                elements=['Admission requirements', 'No assisting non-lawyers', 'MJP exceptions', 'Pro hac vice'],
                common_traps=['MJP exceptions', 'Temporary practice', 'Assisting UPL'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_sale_law_practice",
                name="Sale of Law Practice",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May sell practice if: entire practice or area sold, written client notice, fees not increased",
                elements=['Entire practice or area', 'Written notice', 'No fee increase', 'Client consent'],
                common_traps=['Must sell entire area', 'Client can reject', 'Cannot increase fees'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_reporting_misconduct",
                name="Reporting Professional Misconduct",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer must report other lawyer's violations raising substantial question about honesty, trustworthiness, fitness",
                elements=['Must report violations', 'Substantial question test', 'Confidentiality exceptions', 'Self-reporting'],
                common_traps=['Confidentiality not absolute', 'Substantial question threshold', 'Judge misconduct reporting'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_disciplinary_procedures",
                name="Disciplinary Procedures",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="State supreme court inherent authority; disciplinary board investigates; sanctions range from private reprimand to disbarment",
                elements=['Supreme court authority', 'Investigation process', 'Sanctions range', 'Reciprocal discipline'],
                common_traps=['Inherent authority', 'Burden of proof', 'Reciprocal discipline rules'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_multijurisdictional",
                name="Multijurisdictional Practice",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="May practice temporarily if: related to admitted practice, arbitration/mediation, reasonably related to practice, pro hac vice",
                elements=['Temporary practice exceptions', 'Related to home practice', 'Pro hac vice', 'Systematic presence prohibited'],
                common_traps=['Cannot establish office', 'Related to home practice', 'Temporary only'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_litigation_conduct",
                name="Conduct in Litigation",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must not: abuse discovery, fail to disclose controlling authority, falsify evidence, make frivolous claims",
                elements=['No discovery abuse', 'Disclose adverse authority', 'No false evidence', 'No frivolous claims'],
                common_traps=['Adverse authority in controlling jurisdiction', 'Discovery proportionality', 'Good faith extensions OK'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_transactions_with_client",
                name="Business Transactions with Clients",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot enter business transaction unless: terms fair and reasonable, disclosed in writing, client has independent counsel opportunity, client consents in writing",
                elements=['Fair and reasonable', 'Written disclosure', 'Independent counsel opportunity', 'Written consent'],
                common_traps=['All four required', 'Full disclosure needed', 'Independent counsel chance'],
                # Mnemonic: FICO: Fair, Independent counsel, Consent, Opportunity
            ),
            KnowledgeNode(
                concept_id="prof_resp_literary_rights",
                name="Literary & Media Rights",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot acquire literary or media rights to representation before conclusion; may contract for reasonable expenses of publication after conclusion",
                elements=['No rights before conclusion', 'May contract after', 'Reasonable expenses only', 'Avoid conflict'],
                common_traps=['Timing - must wait until conclusion', 'May negotiate after', 'Conflict of interest concern'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_financial_assistance",
                name="Financial Assistance to Client",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot provide financial assistance except: advance court costs and expenses, contingent on outcome; may pay costs for indigent client",
                elements=['May advance costs', 'Repayment contingent on outcome', 'May pay for indigent', 'No personal living expenses'],
                common_traps=['Cannot advance living expenses', 'Can advance litigation costs', 'Indigent exception'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_former_government_lawyer",
                name="Former Government Lawyer",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent in matter personally and substantially participated in as government lawyer; screening can cure; cannot use confidential government information",
                elements=['Personally and substantially test', 'Screening available', 'No confidential info use', 'Negotiating employment'],
                common_traps=['Screening can cure conflict', 'Personal and substantial both required', 'Confidential info permanent bar'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_former_judge_arbitrator",
                name="Former Judge or Arbitrator",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent anyone in matter participated in as judge, arbitrator, mediator, or other neutral; screening cannot cure",
                elements=['Cannot represent in prior matter', 'Participated as neutral', 'Screening cannot cure', 'Negotiating employment restriction'],
                common_traps=['Screening does NOT cure (unlike gov lawyer)', 'Participated in any capacity', 'Negotiating employment limits'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_imputed_conflicts",
                name="Imputation of Conflicts",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Lawyer conflicts imputed to all in firm unless: personal interest, former client with screening, former government lawyer with screening",
                elements=['General imputation rule', 'Personal interest exception', 'Former client screening', 'Government lawyer screening'],
                common_traps=['Three main exceptions', 'Screening procedures', 'Timely screening required'],
                # Mnemonic: PFG: Personal, Former client, Government (exceptions to imputation)
            ),
            KnowledgeNode(
                concept_id="prof_resp_nonlawyer_assistants",
                name="Responsibilities for Nonlawyer Assistants",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer responsible for nonlawyer assistants' conduct; must ensure compliance with professional rules; cannot delegate legal judgment",
                elements=['Supervisory responsibility', 'Ensure compliance', 'Cannot delegate legal judgment', 'Ethical violations imputed'],
                common_traps=['Lawyer still responsible', 'Cannot avoid by delegation', 'Must supervise adequately'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_fee_division",
                name="Fee Division with Lawyers",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May divide fee with another lawyer if: proportional to services or joint responsibility, client agrees in writing, total fee reasonable",
                elements=['Proportional or joint responsibility', 'Written client agreement', 'Total fee reasonable', 'No division with non-lawyer'],
                common_traps=['Proportion or responsibility both OK', 'Client must agree', 'Cannot divide with non-lawyer'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_aggregate_settlements",
                name="Aggregate Settlements",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot participate in aggregate settlement unless each client gives informed consent in writing after disclosure of all material terms",
                elements=['Each client must consent', 'Informed consent', 'Written', 'Disclosure of all terms'],
                common_traps=['Every client must agree', 'Full disclosure required', 'Cannot coerce holdouts'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_limiting_liability",
                name="Limiting Liability & Malpractice",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot prospectively limit malpractice liability unless client independently represented; may settle malpractice claim if client advised to seek independent counsel",
                elements=['No prospective limits without independent counsel', 'May settle if advised', 'Full disclosure required', 'Independent advice'],
                common_traps=['Prospective limits rare', 'Settlement requires advice', 'Independent counsel key'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_sexual_relations",
                name="Sexual Relations with Clients",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot have sexual relations with client unless consensual relationship existed before attorney-client relationship",
                elements=['Prohibited unless preexisting', 'Consent not defense', 'Exploitation concern', 'Impairs judgment'],
                policy_rationales=['Prevent exploitation', 'Avoid conflicts', 'Protect judgment'],
                common_traps=['Preexisting relationship exception only', 'Consent insufficient', 'Judgment impairment'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_appearance_of_impropriety",
                name="Appearance of Impropriety",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer should avoid even appearance of impropriety; upholds confidence in legal profession; aspirational standard",
                elements=['Avoid appearance', 'Public confidence', 'Aspirational', 'Reasonable person test'],
                common_traps=['Aspirational not enforceable alone', 'Reasonable person view', 'Supplements specific rules'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_corporations(self):
        """27 Corporations concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="corp_promoter_liability",
                name="Promoter Liability",
                subject="corporations",
                difficulty=3,
                rule_statement="Promoter liable on pre-incorporation contracts unless novation; corporation liable if adopts contract expressly or impliedly",
                elements=['Promoter personally liable', 'Corporation liable if adopts', 'Novation releases promoter', 'Implied adoption'],
                common_traps=['Both can be liable', "Adoption doesn't release", 'Need novation for release'],
            ),
            KnowledgeNode(
                concept_id="corp_defective_incorporation",
                name="Defective Incorporation",
                subject="corporations",
                difficulty=3,
                rule_statement="De facto corporation: good faith attempt, actual use; corporation by estoppel: held out as corporation, third party dealt as such",
                elements=['De facto corporation', 'Corporation by estoppel', 'Good faith attempt', 'Actual use'],
                common_traps=['Both doctrines exist', 'Protects from personal liability', 'Narrow application'],
            ),
            KnowledgeNode(
                concept_id="corp_ultra_vires",
                name="Ultra Vires Acts",
                subject="corporations",
                difficulty=2,
                rule_statement="Acts beyond corporate powers; generally enforceable but shareholders can enjoin, corporation can sue officers, state can dissolve",
                elements=['Beyond stated purpose', 'Generally enforceable', 'Limited remedies', 'Rare doctrine'],
                common_traps=['Contract still enforceable', 'Internal remedy', 'Rarely succeeds'],
            ),
            KnowledgeNode(
                concept_id="corp_subscriptions",
                name="Stock Subscriptions",
                subject="corporations",
                difficulty=3,
                rule_statement="Pre-incorporation subscription irrevocable for six months unless otherwise provided; post-incorporation governed by contract law",
                elements=['Pre-incorporation irrevocable', 'Six month rule', 'Post-incorporation contract', 'Payment terms'],
                common_traps=['Pre vs post timing', 'Irrevocability period', 'Contract law post-incorporation'],
            ),
            KnowledgeNode(
                concept_id="corp_consideration_shares",
                name="Consideration for Shares",
                subject="corporations",
                difficulty=3,
                rule_statement="Par value: must receive at least par; no-par: any consideration; watered stock: directors liable; good faith business judgment protects valuation",
                elements=['Par value minimum', 'No-par flexibility', 'Watered stock liability', 'Business judgment valuation'],
                common_traps=['Par vs no-par', 'Director liability watered stock', 'BJR protects valuation'],
            ),
            KnowledgeNode(
                concept_id="corp_preemptive_rights",
                name="Preemptive Rights",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders may have right to purchase new shares to maintain proportional ownership; must be expressly granted in modern law",
                elements=['Maintain proportional ownership', 'Must be in articles', 'Pro rata purchase right', 'Exceptions exist'],
                common_traps=['Must be expressly granted', 'Not automatic', 'Exceptions for compensation'],
            ),
            KnowledgeNode(
                concept_id="corp_distributions_dividends",
                name="Distributions & Dividends",
                subject="corporations",
                difficulty=3,
                rule_statement="Directors declare dividends using business judgment; unlawful if: insolvent, would cause insolvency, or exceeds statutory limits",
                elements=['Board discretion', 'Insolvency test', 'Statutory limits', 'Director liability'],
                common_traps=['Directors discretion wide', 'Insolvency prohibition', 'Directors personally liable'],
            ),
            KnowledgeNode(
                concept_id="corp_inspection_rights",
                name="Shareholder Inspection Rights",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders have right to inspect books and records for proper purpose; shareholder list more readily available than detailed financial records",
                elements=['Proper purpose required', 'Shareholder list easier', 'Books and records harder', 'Advance notice'],
                common_traps=['Proper purpose test', 'Different standards for different records', 'Timing requirements'],
            ),
            KnowledgeNode(
                concept_id="corp_meetings_notice",
                name="Meetings & Notice Requirements",
                subject="corporations",
                difficulty=2,
                rule_statement="Annual shareholders meeting required; notice required with time, place, purpose if special; directors can act without meeting if unanimous written consent",
                elements=['Annual meeting required', 'Notice requirements', 'Special meeting purpose', 'Written consent alternative'],
                common_traps=['Notice timing', 'Special meeting purpose specificity', 'Unanimous consent option'],
            ),
            KnowledgeNode(
                concept_id="corp_quorum_voting",
                name="Quorum & Voting Rules",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders: majority of shares is quorum, majority of votes present wins; Directors: majority of directors is quorum, majority of votes present wins",
                elements=['Shareholder quorum', 'Director quorum', 'Vote requirements', 'Can modify in articles/bylaws'],
                common_traps=['Quorum vs voting', 'Can change by agreement', 'Present vs outstanding'],
            ),
            KnowledgeNode(
                concept_id="corp_removal_directors",
                name="Removal of Directors",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders may remove with or without cause unless articles require cause; if cumulative voting, can remove only if votes sufficient to elect",
                elements=['Shareholder removal power', 'With or without cause', 'Cumulative voting protection', 'Articles can require cause'],
                common_traps=['Unless articles require cause', 'Cumulative voting protection', 'Only shareholders remove'],
            ),
            KnowledgeNode(
                concept_id="corp_indemnification",
                name="Indemnification of Directors/Officers",
                subject="corporations",
                difficulty=4,
                rule_statement="Mandatory if successful on merits; permissive if good faith and reasonable belief; prohibited if found liable to corporation",
                elements=['Mandatory if successful', 'Permissive if good faith', 'Prohibited if liable', 'Advancement of expenses'],
                common_traps=['Three categories', 'Successful = mandatory', 'Liable to corp = prohibited'],
                # Mnemonic: MAP: Mandatory, Allowed, Prohibited
            ),
            KnowledgeNode(
                concept_id="corp_close_corporations",
                name="Close Corporations",
                subject="corporations",
                difficulty=3,
                rule_statement="Few shareholders, no public market, restrictions on transfer; may operate informally; special statutory provisions protect minority",
                elements=['Few shareholders', 'Transfer restrictions', 'Informal operation allowed', 'Minority protection'],
                common_traps=['Can dispense with formalities', 'Oppression remedies', 'Statutory protections'],
            ),
            KnowledgeNode(
                concept_id="corp_shareholder_agreements",
                name="Shareholder Agreements",
                subject="corporations",
                difficulty=3,
                rule_statement="May restrict transfers, provide for management, require arbitration; must not treat corporation as partnership or injure creditors",
                elements=['Voting agreements', 'Buy-sell provisions', 'Transfer restrictions', 'Management agreements'],
                common_traps=['Cannot sterilize board', 'Must protect creditors', 'Binding on parties only'],
            ),
            KnowledgeNode(
                concept_id="corp_oppression_freeze_out",
                name="Oppression & Freeze-Out",
                subject="corporations",
                difficulty=4,
                rule_statement="Majority cannot squeeze out minority unfairly; remedies include buyout, dissolution, or damages; courts balance reasonable expectations",
                elements=['Oppressive conduct', 'Reasonable expectations', 'Buyout remedy', 'Dissolution alternative'],
                policy_rationales=['Protect minority', 'Prevent abuse of control', 'Balance interests'],
                common_traps=['Reasonable expectations test', 'Equitable remedies', 'Close corporation context'],
            ),
            KnowledgeNode(
                concept_id="corp_dividends_preferred",
                name="Preferred Stock Dividends",
                subject="corporations",
                difficulty=3,
                rule_statement="Preferred entitled to fixed dividend before common; cumulative unless stated non-cumulative; participating if so stated",
                elements=['Priority over common', 'Cumulative presumption', 'Participating possibility', 'Liquidation preference'],
                common_traps=['Cumulative unless stated otherwise', 'Arrears must be paid first', 'Participating rare'],
            ),
            KnowledgeNode(
                concept_id="corp_redemption_repurchase",
                name="Redemption & Share Repurchase",
                subject="corporations",
                difficulty=3,
                rule_statement="Corporation may repurchase shares if: not insolvent, adequate surplus; redemption rights if stated; insider trading concerns",
                elements=['Must have surplus', 'Insolvency test', 'Redemption vs repurchase', 'Insider trading risk'],
                common_traps=['Statutory requirements', 'Cannot make insolvent', 'Insider trading prohibition'],
            ),
            KnowledgeNode(
                concept_id="corp_sale_of_assets",
                name="Sale of Substantially All Assets",
                subject="corporations",
                difficulty=4,
                rule_statement="Requires board and shareholder approval; not ordinary course of business; selling corporation continues to exist; buyers can assume liabilities",
                elements=['Substantially all assets', 'Board and shareholder vote', 'Continues to exist', 'Successor liability rules'],
                common_traps=['Substantially all test', 'Continues to exist', 'Not automatic successor liability'],
            ),
            KnowledgeNode(
                concept_id="corp_tender_offers",
                name="Tender Offers",
                subject="corporations",
                difficulty=3,
                rule_statement="Offer to buy shares directly from shareholders; federal regulation; target board may defend; business judgment rule applies to defensive measures",
                elements=['Direct to shareholders', 'Federal securities law', 'Board defensive tactics', 'BJR applies'],
                common_traps=['Bypass board', 'Defensive measures reviewed', 'Unocal standard may apply'],
            ),
            KnowledgeNode(
                concept_id="corp_proxy_fights",
                name="Proxy Contests",
                subject="corporations",
                difficulty=3,
                rule_statement="Contest for board control via shareholder votes; federal proxy rules; corporation may reimburse incumbents; insurgents reimbursed if successful",
                elements=['Board control contest', 'Proxy solicitation rules', 'Reimbursement rules', 'Disclosure requirements'],
                common_traps=['Corporation can reimburse incumbents', 'Insurgents if successful', 'Federal regulation applies'],
            ),
            KnowledgeNode(
                concept_id="corp_hostile_takeovers",
                name="Hostile Takeovers & Defensive Tactics",
                subject="corporations",
                difficulty=4,
                rule_statement="Target board may defend using business judgment; must show reasonable threat and proportionate response; cannot be entrenching",
                elements=['Unocal standard', 'Reasonable threat', 'Proportionate response', 'Enhanced scrutiny'],
                common_traps=['Enhanced scrutiny', 'Cannot be entrenching', 'Proportionality key'],
                # Mnemonic: PRE: Proportionate, Reasonable threat, Enhanced scrutiny
            ),
            KnowledgeNode(
                concept_id="corp_appraisal_rights",
                name="Appraisal Rights",
                subject="corporations",
                difficulty=4,
                rule_statement="Dissenting shareholders entitled to fair value of shares in: mergers, sales of assets, amendments materially affecting rights",
                elements=['Fair value determination', 'Dissent and notice required', 'Exclusive remedy', 'Triggering events'],
                common_traps=['Must follow procedures exactly', 'Fair value not market value', 'Exclusive remedy if available'],
            ),
            KnowledgeNode(
                concept_id="corp_amendments_articles",
                name="Amending Articles of Incorporation",
                subject="corporations",
                difficulty=2,
                rule_statement="Requires board approval and shareholder vote; certain amendments require class vote if materially affect class",
                elements=['Board approval', 'Shareholder vote', 'Class voting rights', 'Filing required'],
                common_traps=['Class vote for material changes to class', 'Filing makes effective', 'Broad board power'],
            ),
            KnowledgeNode(
                concept_id="corp_bylaws",
                name="Bylaws",
                subject="corporations",
                difficulty=2,
                rule_statement="Internal operating rules; typically adopted/amended by board unless articles reserve to shareholders; cannot conflict with articles or statutes",
                elements=['Internal rules', 'Board typically amends', 'Cannot conflict with articles', 'Operating procedures'],
                common_traps=['Board power unless reserved', 'Hierarchy: statute > articles > bylaws', 'Cannot expand powers'],
            ),
            KnowledgeNode(
                concept_id="corp_limited_liability_company",
                name="Limited Liability Companies (LLC)",
                subject="corporations",
                difficulty=3,
                rule_statement="Hybrid entity: corporate limited liability plus partnership flexibility; operating agreement governs; default rules vary by state",
                elements=['Limited liability', 'Pass-through taxation', 'Operating agreement', 'Flexible management'],
                common_traps=['Operating agreement controls', 'Default rules vary', 'Veil piercing still possible'],
            ),
            KnowledgeNode(
                concept_id="corp_partnerships_general",
                name="General Partnerships",
                subject="corporations",
                difficulty=3,
                rule_statement="Formation by agreement or co-ownership for profit; each partner agent; jointly and severally liable; equal sharing unless agreed",
                elements=['No formalities', 'Each partner agent', 'Unlimited liability', 'Equal sharing default'],
                common_traps=['Joint and several liability', 'Each partner can bind', 'No filing required'],
            ),
            KnowledgeNode(
                concept_id="corp_limited_partnerships",
                name="Limited Partnerships",
                subject="corporations",
                difficulty=3,
                rule_statement="General partners manage and liable; limited partners passive investors with liability limited to investment; filing required",
                elements=['GP manages and liable', 'LP limited liability', 'Filing required', 'LP cannot control'],
                common_traps=['LP control destroys limited liability', 'Must file certificate', 'GP fully liable'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_wills_trusts_estates(self):
        """37 Wills Trusts Estates concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="wills_capacity",
                name="Testamentary Capacity",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Testator must be 18+, understand nature of act, extent of property, natural objects of bounty, plan of disposition",
                elements=['Age 18+', 'Understand nature', 'Know property', 'Natural objects', 'Dispositional plan'],
                common_traps=['Lower standard than contractual', 'Lucid intervals count', 'Burden on contestants'],
                # Mnemonic: PENDO: Property, Estate, Nature, Disposition, Objects
            ),
            KnowledgeNode(
                concept_id="wills_attestation",
                name="Attestation & Witnesses",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Two witnesses must attest; must be present at same time; interested witness issues; purging statutes may apply",
                elements=['Two witnesses', 'Simultaneous presence', 'Sign in testator presence', 'Competent witnesses'],
                common_traps=['Line of sight test', 'Interested witness loses bequest', 'Purging statutes'],
            ),
            KnowledgeNode(
                concept_id="wills_codicil",
                name="Codicils",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Testamentary instrument that modifies will; must meet same formalities; republishes will as of codicil date",
                elements=['Modifies existing will', 'Same formalities required', 'Republication effect', 'Integration'],
                common_traps=['Republication doctrine', 'Cures defects in will', 'Must meet formalities'],
            ),
            KnowledgeNode(
                concept_id="wills_incorporation_reference",
                name="Incorporation by Reference",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="External document incorporated if: exists when will executed, will manifests intent, will describes sufficiently",
                elements=['Document must exist', 'Intent to incorporate', 'Sufficient description', 'Extrinsic evidence'],
                common_traps=['Must exist at execution', 'Cannot incorporate future documents', 'Description requirement'],
            ),
            KnowledgeNode(
                concept_id="wills_acts_of_independent_significance",
                name="Acts of Independent Significance",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Will can refer to acts/events with significance apart from testamentary effect; non-testamentary motive required",
                elements=['Independent significance', 'Non-testamentary purpose', 'Changes effective', 'Common examples'],
                common_traps=['Must have independent purpose', 'Contents of wallet example', 'Beneficiary designation'],
            ),
            KnowledgeNode(
                concept_id="wills_holographic",
                name="Holographic Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Handwritten, signed, material provisions in testator handwriting; no witnesses required in states recognizing",
                elements=['Handwritten', 'Signed', 'Material provisions', 'No witnesses'],
                common_traps=['Not all states recognize', 'Material portions test', 'Intent to be will'],
            ),
            KnowledgeNode(
                concept_id="wills_conditional",
                name="Conditional Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Will effective only if condition occurs; distinguishing condition of execution from condition of revocation",
                elements=['Condition must occur', 'Condition vs motive', 'Extrinsic evidence', 'Interpretation issues'],
                common_traps=['Condition vs motive', 'Presumption against conditional', 'Proof required'],
            ),
            KnowledgeNode(
                concept_id="wills_revocation_dependent_relative",
                name="Dependent Relative Revocation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revocation ineffective if based on mistake of law/fact and would not have revoked but for mistake",
                elements=['Mistaken revocation', 'Would not have revoked', 'Testator intent', 'Second-best result'],
                common_traps=['Applies when mistake', 'Second best over intestacy', 'Intent focus'],
            ),
            KnowledgeNode(
                concept_id="wills_revival",
                name="Revival of Revoked Wills",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="When revoking instrument revoked, three approaches: automatic revival, testator intent, no revival absent re-execution",
                elements=['Revocation of revocation', 'Majority: intent controls', 'Minority: automatic', 'Minority: re-execution'],
                common_traps=['State law varies', 'Intent evidence', 'May need re-execution'],
            ),
            KnowledgeNode(
                concept_id="wills_lapse_anti_lapse",
                name="Lapse & Anti-Lapse",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Bequest lapses if beneficiary predeceases; anti-lapse saves gift if beneficiary in protected class and leaves issue",
                elements=['Lapse when predecease', 'Anti-lapse statute', 'Protected class', 'Issue substitute'],
                common_traps=['Protected class varies', 'Issue requirement', 'Express contrary intent'],
                # Mnemonic: ACID: Anti-lapse, Class, Issue, Descendants
            ),
            KnowledgeNode(
                concept_id="wills_ademption",
                name="Ademption by Extinction",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Specific gift adeemed if not in estate at death; identity theory vs intent theory",
                elements=['Specific gift only', 'Not in estate', 'Identity theory', 'Intent theory minority'],
                common_traps=['Specific vs general/demonstrative', 'Exceptions may apply', 'Insurance proceeds'],
            ),
            KnowledgeNode(
                concept_id="wills_ademption_satisfaction",
                name="Ademption by Satisfaction",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Lifetime gift to beneficiary may satisfy testamentary gift if: writing by testator, writing by beneficiary, or property declares satisfaction",
                elements=['Lifetime gift', 'Testamentary gift', 'Writing requirement', 'Intent to satisfy'],
                common_traps=['Need writing', 'Presumption against', 'Value determination'],
            ),
            KnowledgeNode(
                concept_id="wills_abatement",
                name="Abatement",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Reduce gifts when assets insufficient; order: intestate property, residuary, general, demonstrative, specific",
                elements=['Insufficient assets', 'Priority order', 'Pro rata within class', 'Can change by will'],
                common_traps=['Standard order', 'Pro rata reduction', 'Will can change'],
                # Mnemonic: IRGDS: Intestate, Residuary, General, Demonstrative, Specific (reverse priority)
            ),
            KnowledgeNode(
                concept_id="wills_exoneration",
                name="Exoneration of Liens",
                subject="wills_trusts_estates",
                difficulty=2,
                rule_statement="Traditional: estate pays off liens; Modern UPC: beneficiary takes subject to liens unless will directs payment",
                elements=['Liens on specific gifts', 'Traditional: estate pays', 'UPC: beneficiary takes with', 'Will can direct'],
                common_traps=['UPC changed rule', 'Specific direction needed', 'Mortgage example'],
            ),
            KnowledgeNode(
                concept_id="wills_pretermitted_spouse",
                name="Pretermitted Spouse",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Spouse married after will takes intestate share unless: will contemplates marriage, provided for outside will, intentionally omitted",
                elements=['After-will marriage', 'Intestate share', 'Three exceptions', 'Intent evidence'],
                common_traps=['Exceptions apply', 'Burden of proof', 'Not divorce'],
            ),
            KnowledgeNode(
                concept_id="wills_pretermitted_children",
                name="Pretermitted Children",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Child born/adopted after will takes share unless: intentional omission shown, provided for outside will, or all to other parent",
                elements=['After-will child', 'Share calculation', 'Three exceptions', 'All estate to parent exception'],
                common_traps=['Share calculation complex', 'All-to-parent exception', 'Adopted children included'],
            ),
            KnowledgeNode(
                concept_id="wills_elective_share",
                name="Elective Share",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Surviving spouse can elect statutory share (typically 1/3 or 1/2) instead of will provision; time limit applies",
                elements=['Statutory percentage', 'Augmented estate', 'Time to elect', 'Cannot waive before marriage'],
                common_traps=['Augmented estate includes transfers', 'Time limit strict', 'Prenup can waive'],
            ),
            KnowledgeNode(
                concept_id="wills_undue_influence",
                name="Undue Influence",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Substituted will of influencer for testator; requires: susceptibility, opportunity, disposition to influence, unnatural result",
                elements=['Susceptibility', 'Opportunity', 'Active procurement', 'Unnatural result'],
                common_traps=['Four elements', 'Burden on contestant', 'Presumption if confidential relation + benefit'],
            ),
            KnowledgeNode(
                concept_id="wills_fraud",
                name="Fraud",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="False statement material to testamentary disposition; fraud in execution vs inducement; constructive trust remedy",
                elements=['False representation', 'Known false', 'Testator reliance', 'Material'],
                common_traps=['Fraud in execution vs inducement', 'Constructive trust remedy', 'High burden'],
            ),
            KnowledgeNode(
                concept_id="wills_mistake",
                name="Mistake",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Mistake in execution may void; mistake in inducement generally not correctable; reformation limited",
                elements=['Mistake in execution', 'Mistake in inducement', 'Limited correction', 'Omitted text'],
                common_traps=['In execution voids', 'In inducement usually no remedy', 'Rare reformation'],
            ),
            KnowledgeNode(
                concept_id="wills_joint_mutual",
                name="Joint & Mutual Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Joint: one document for multiple testators; Mutual: reciprocal provisions; contract not to revoke requires clear evidence",
                elements=['Joint will', 'Mutual wills', 'Contract not to revoke', 'Proof required'],
                common_traps=['Presumption against contract', 'Must prove agreement', 'Remedy: constructive trust'],
            ),
            KnowledgeNode(
                concept_id="trusts_inter_vivos",
                name="Inter Vivos Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Created during settlor lifetime; requires delivery; can be revocable or irrevocable; avoids probate",
                elements=['Lifetime creation', 'Delivery required', 'Revocability', 'Probate avoidance'],
                common_traps=['Delivery requirement', 'Revocable unless stated', 'Pour-over wills'],
            ),
            KnowledgeNode(
                concept_id="trusts_testamentary",
                name="Testamentary Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Created by will; effective at death; must meet will formalities; subject to probate",
                elements=['Created by will', 'Will formalities', 'Effective at death', 'Probate required'],
                common_traps=['Will formalities apply', 'Goes through probate', 'Court supervision'],
            ),
            KnowledgeNode(
                concept_id="trusts_spendthrift",
                name="Spendthrift Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Beneficiary cannot transfer interest; creditors cannot reach; exceptions: certain creditors, excess beyond support",
                elements=['Transfer restraint', 'Creditor protection', 'Express provision needed', 'Exceptions exist'],
                common_traps=['Must be express', 'Exception creditors', 'Self-settled issues'],
            ),
            KnowledgeNode(
                concept_id="trusts_discretionary",
                name="Discretionary Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Trustee has discretion over distributions; standard may be absolute or limited; creditor protection",
                elements=['Trustee discretion', 'Absolute vs limited', 'Judicial review limited', 'Creditor protection'],
                common_traps=['Abuse of discretion standard', 'Good faith required', 'Creditor protection strong'],
            ),
            KnowledgeNode(
                concept_id="trusts_support",
                name="Support Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Trustee must distribute for support; mandatory if within standard; creditors providing necessaries can reach",
                elements=['Mandatory distributions', 'Support standard', 'Necessaries creditors', 'Interpretation'],
                common_traps=['Mandatory nature', 'Necessaries exception', 'Standard interpretation'],
            ),
            KnowledgeNode(
                concept_id="trusts_resulting",
                name="Resulting Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Arises by operation of law when: purchase money resulting trust, excess corpus, failure of express trust",
                elements=['Implied by law', 'Settlor gets back', 'Purchase money', 'Failure scenarios'],
                common_traps=['Returns to settlor', 'Operation of law', 'Limited situations'],
            ),
            KnowledgeNode(
                concept_id="trusts_constructive",
                name="Constructive Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Equitable remedy for unjust enrichment; wrongdoer holds property for rightful owner; fraud, breach of duty",
                elements=['Equitable remedy', 'Unjust enrichment', 'Wrongful conduct', 'Rightful owner recovers'],
                common_traps=['Remedy not true trust', 'Flexible application', 'Prevents unjust enrichment'],
            ),
            KnowledgeNode(
                concept_id="trusts_modification",
                name="Trust Modification & Termination",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revocable: settlor can modify/terminate; Irrevocable: need consent or changed circumstances; Claflin doctrine applies",
                elements=['Revocable settlor control', 'Irrevocable restrictions', 'Claflin doctrine', 'Changed circumstances'],
                common_traps=['Material purpose test', 'Consent requirements', 'Court modification limited'],
            ),
            KnowledgeNode(
                concept_id="trusts_powers",
                name="Trustee Powers",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Express powers in instrument; implied powers necessary to accomplish purpose; statutory default powers",
                elements=['Express powers', 'Implied powers', 'Statutory powers', 'Limits on powers'],
                common_traps=['Broadly construed', 'Statutory defaults', 'Cannot violate duty'],
            ),
            KnowledgeNode(
                concept_id="trusts_duty_inform",
                name="Duty to Inform & Account",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Must keep beneficiaries informed; provide annual accounting; respond to requests; disclosure of material facts",
                elements=['Keep informed', 'Annual accounting', 'Respond to requests', 'Material facts'],
                common_traps=['Affirmative duty', 'Reasonable information', 'Cannot hide behind instrument'],
            ),
            KnowledgeNode(
                concept_id="trusts_principal_income",
                name="Principal & Income Allocation",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Distinguish principal from income; Uniform Principal & Income Act provides rules; trustee adjusting power",
                elements=['Principal vs income', 'UPAIA rules', 'Adjusting power', 'Life tenant/remainder split'],
                common_traps=['UPAIA default rules', 'Power to adjust', 'Impartiality duty'],
            ),
            KnowledgeNode(
                concept_id="trusts_breach_remedies",
                name="Breach of Trust & Remedies",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Trustee liable for breach; remedies: damages, remove trustee, constructive trust, tracing; defenses: consent, exculpation clause",
                elements=['Liability for breach', 'Multiple remedies', 'Defenses available', 'Statute of limitations'],
                common_traps=['Multiple remedies possible', 'Exculpation limits', 'Consent defense'],
            ),
            KnowledgeNode(
                concept_id="rule_against_perpetuities",
                name="Rule Against Perpetuities",
                subject="wills_trusts_estates",
                difficulty=5,
                rule_statement="Interest must vest or fail within life in being plus 21 years; applies to contingent remainders, executory interests; reform statutes exist",
                elements=['Measuring lives', '21 year period', 'Must vest or fail', 'Contingent interests'],
                common_traps=['Contingent interests only', 'Reform statutes', 'Wait and see', 'Cy pres'],
                # Mnemonic: RAP applies to: contingent remainders, executory interests, class gifts, options, rights of first refusal
            ),
            KnowledgeNode(
                concept_id="powers_of_appointment",
                name="Powers of Appointment",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="General: appointee can appoint to self, estate, creditors; Special: limited class; affects estate taxation and creditors",
                elements=['General power', 'Special power', 'Exercise methods', 'Tax consequences'],
                common_traps=['General vs special', 'Default appointments', 'Tax implications'],
            ),
            KnowledgeNode(
                concept_id="estate_administration",
                name="Estate Administration Process",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Probate process: petition, notice, inventory, pay debts, distribute; executor/administrator duties; court supervision",
                elements=['Petition for probate', 'Notice to heirs', 'Inventory and appraisal', 'Pay debts then distribute'],
                common_traps=['Priority of payments', 'Creditor claims period', 'Accounting requirements'],
            ),
            KnowledgeNode(
                concept_id="nonprobate_transfers",
                name="Non-Probate Transfers",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Avoid probate: joint tenancy, POD/TOD accounts, life insurance, trusts; creditor rights may still apply",
                elements=['Joint tenancy', 'POD/TOD', 'Life insurance', 'Trust assets'],
                common_traps=['Avoid probate but not taxes', 'Creditor rights', "Will provisions don't control"],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_family_law(self):
        """25 Family Law concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="family_annulment",
                name="Annulment",
                subject="family_law",
                difficulty=3,
                rule_statement="Void marriage: bigamy, incest, mental incapacity; Voidable: age, impotence, fraud, duress, lack of consent",
                elements=['Void ab initio', 'Voidable until annulled', 'Grounds vary', 'Retroactive effect'],
                common_traps=['Void vs voidable', 'Retroactive effect', 'Property rights may survive'],
            ),
            KnowledgeNode(
                concept_id="family_separation",
                name="Legal Separation",
                subject="family_law",
                difficulty=2,
                rule_statement="Court-approved living apart; addresses support, property, custody; marriage continues; bars filed by separated spouse",
                elements=['Marriage continues', 'Court order', 'Same issues as divorce', 'Can convert to divorce'],
                common_traps=['Not divorce', 'Marriage continues', 'Same relief available'],
            ),
            KnowledgeNode(
                concept_id="family_jurisdiction",
                name="Divorce Jurisdiction",
                subject="family_law",
                difficulty=3,
                rule_statement="Divorce: domicile of one spouse; Property: in personam jurisdiction; Custody: UCCJEA home state",
                elements=['Domicile for divorce', 'Personal jurisdiction for property', 'UCCJEA for custody', 'Residency requirements'],
                common_traps=['Different jurisdiction rules', 'Divisible divorce', 'UCCJEA controls custody'],
            ),
            KnowledgeNode(
                concept_id="family_uccjea",
                name="UCCJEA Jurisdiction",
                subject="family_law",
                difficulty=4,
                rule_statement="Home state priority: where child lived 6 months before filing; significant connection if no home state; emergency jurisdiction limited",
                elements=['Home state priority', 'Significant connection', 'Emergency jurisdiction', 'Exclusive continuing jurisdiction'],
                common_traps=['Home state 6 months', 'Continuing jurisdiction', 'Emergency temporary only'],
                # Mnemonic: HSCE: Home state, Significant connection, Continuing, Emergency
            ),
            KnowledgeNode(
                concept_id="family_uifsa",
                name="UIFSA Support Enforcement",
                subject="family_law",
                difficulty=3,
                rule_statement="Uniform Interstate Family Support Act; continuing exclusive jurisdiction; direct interstate enforcement; one-order system",
                elements=['Issuing state keeps jurisdiction', 'Direct enforcement', 'No duplicate orders', 'Long-arm jurisdiction'],
                common_traps=['Continuing exclusive', 'Cannot modify elsewhere', 'Long-arm provisions'],
            ),
            KnowledgeNode(
                concept_id="family_modification_support",
                name="Modification of Support",
                subject="family_law",
                difficulty=4,
                rule_statement="Material change in circumstances required; cannot modify retroactively; voluntary unemployment may not count; burden on moving party",
                elements=['Material change', 'Prospective only', 'Substantial change', 'Voluntary acts'],
                common_traps=['Cannot modify past', 'Material change required', 'Voluntary unemployment'],
            ),
            KnowledgeNode(
                concept_id="family_modification_custody",
                name="Modification of Custody",
                subject="family_law",
                difficulty=4,
                rule_statement="Substantial change in circumstances; best interests of child; may require changed circumstances plus detrimental; restrictions on relitigation",
                elements=['Substantial change', 'Best interests', 'May need detriment', 'Time limitations'],
                common_traps=['Higher standard than initial', 'Detriment in some states', 'Relitigation restrictions'],
            ),
            KnowledgeNode(
                concept_id="family_enforcement",
                name="Support Enforcement",
                subject="family_law",
                difficulty=3,
                rule_statement="Contempt: civil or criminal; wage garnishment; license suspension; passport denial; federal locate services",
                elements=['Contempt sanctions', 'Wage withholding', 'License suspension', 'Federal enforcement'],
                common_traps=['Civil vs criminal contempt', 'Automatic withholding', 'Cannot discharge in bankruptcy'],
            ),
            KnowledgeNode(
                concept_id="family_contempt",
                name="Contempt Proceedings",
                subject="family_law",
                difficulty=3,
                rule_statement="Civil: coercive, must have ability to comply; Criminal: punitive, beyond reasonable doubt; inability to pay is defense",
                elements=['Civil coercive', 'Criminal punitive', 'Ability to pay', 'Purge conditions'],
                common_traps=['Civil vs criminal', 'Ability to pay defense', 'Burden of proof differs'],
            ),
            KnowledgeNode(
                concept_id="family_child_abuse",
                name="Child Abuse & Neglect",
                subject="family_law",
                difficulty=3,
                rule_statement="State intervention to protect child; removal requires hearing; reasonable efforts to reunify; termination of parental rights possible",
                elements=['Emergency removal', 'Court hearing', 'Reasonable efforts', 'TPR option'],
                common_traps=['Due process protections', 'Reasonable efforts', 'Clear and convincing for TPR'],
            ),
            KnowledgeNode(
                concept_id="family_termination_parental_rights",
                name="Termination of Parental Rights",
                subject="family_law",
                difficulty=4,
                rule_statement="Severs legal parent-child relationship; grounds: abuse, neglect, abandonment, unfitness; clear and convincing evidence; permanent",
                elements=['Statutory grounds', 'Clear and convincing', 'Permanent severance', 'Best interests'],
                common_traps=['High burden', 'Permanent', 'Best interests focus'],
            ),
            KnowledgeNode(
                concept_id="family_adoption",
                name="Adoption",
                subject="family_law",
                difficulty=3,
                rule_statement="Creates legal parent-child relationship; consent required from biological parents unless rights terminated; home study; finalization hearing",
                elements=['Consent requirements', 'TPR alternative', 'Home study', 'Finalization'],
                common_traps=['Consent requirements', 'Putative father rights', 'Revocation period'],
            ),
            KnowledgeNode(
                concept_id="family_paternity",
                name="Paternity Establishment",
                subject="family_law",
                difficulty=3,
                rule_statement="Voluntary acknowledgment or court determination; genetic testing presumptive; rebuttable presumptions; support and custody rights follow",
                elements=['Voluntary acknowledgment', 'Genetic testing', 'Presumptions', 'Rights and duties'],
                common_traps=['Presumptions of paternity', 'Genetic testing standard', 'Rights follow establishment'],
            ),
            KnowledgeNode(
                concept_id="family_presumptions_paternity",
                name="Presumptions of Paternity",
                subject="family_law",
                difficulty=3,
                rule_statement="Marital presumption: husband presumed father; holding out; genetic testing rebuts; multiple presumptions possible",
                elements=['Marital presumption', 'Holding out', 'Genetic testing', 'Rebuttal'],
                common_traps=['Marital presumption strong', 'Genetic testing rebuts', 'Multiple presumed fathers'],
            ),
            KnowledgeNode(
                concept_id="family_equitable_parent",
                name="Equitable Parent Doctrine",
                subject="family_law",
                difficulty=3,
                rule_statement="Non-biological parent may have rights/duties if: accepted parental role, bonded with child, parent consented; minority doctrine",
                elements=['Functional parent', 'Acceptance of role', 'Parent consent', 'Bonding'],
                common_traps=['Minority doctrine', 'Factors test', 'Parent consent key'],
            ),
            KnowledgeNode(
                concept_id="family_visitation",
                name="Visitation Rights",
                subject="family_law",
                difficulty=3,
                rule_statement="Non-custodial parent entitled to reasonable visitation unless detrimental; grandparent rights limited; supervised visitation possible",
                elements=['Reasonable visitation', 'Best interests', 'Grandparent limits', 'Supervised option'],
                common_traps=['Grandparent rights limited', 'Troxel case', 'Parental presumption'],
            ),
            KnowledgeNode(
                concept_id="family_relocation",
                name="Relocation with Child",
                subject="family_law",
                difficulty=4,
                rule_statement="Custodial parent seeking to relocate must: give notice, show legitimate reason; court balances factors; may modify custody",
                elements=['Notice requirement', 'Legitimate reason', 'Factor balancing', 'Burden on relocating parent'],
                common_traps=['Notice timing', 'Burden allocation', 'Factor tests vary'],
            ),
            KnowledgeNode(
                concept_id="family_domestic_violence",
                name="Domestic Violence",
                subject="family_law",
                difficulty=3,
                rule_statement="Protective orders available; ex parte emergency; full hearing; custody and support implications; violation is contempt/crime",
                elements=['Ex parte available', 'Full hearing', 'Relief available', 'Violation sanctions'],
                common_traps=['Ex parte standard lower', 'Custody preferences', 'Criminal violation'],
            ),
            KnowledgeNode(
                concept_id="family_protective_orders",
                name="Protective Orders",
                subject="family_law",
                difficulty=3,
                rule_statement="Restraining orders to prevent abuse; standards: immediate danger, abuse occurred; violations punishable; mutual orders disfavored",
                elements=['Standard for issuance', 'Relief available', 'Violation consequences', 'Mutual orders issue'],
                common_traps=['Standard of proof', 'Duration', 'Mutual orders problematic'],
            ),
            KnowledgeNode(
                concept_id="family_prenuptial_agreements",
                name="Prenuptial Agreements",
                subject="family_law",
                difficulty=4,
                rule_statement="Valid if: voluntary, fair disclosure, not unconscionable; cannot adversely affect child support; can waive spousal support",
                elements=['Voluntary execution', 'Financial disclosure', 'Conscionability', 'Cannot affect child support'],
                common_traps=['Full disclosure required', 'Cannot limit child support', 'Can waive spousal support'],
                # Mnemonic: VFC: Voluntary, Fair disclosure, Conscionable
            ),
            KnowledgeNode(
                concept_id="family_postnuptial_agreements",
                name="Postnuptial Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Agreement after marriage; same requirements as prenuptial plus consideration; scrutinized closely; increasing acceptance",
                elements=['After marriage', 'Consideration needed', 'Close scrutiny', 'Similar to prenup'],
                common_traps=['Need consideration', 'Higher scrutiny', 'Growing acceptance'],
            ),
            KnowledgeNode(
                concept_id="family_separation_agreements",
                name="Separation Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Negotiated settlement of divorce issues; merged into decree if approved; court reviews for fairness; child provisions always modifiable",
                elements=['Negotiated settlement', 'Court approval', 'Fairness review', 'Merger into decree'],
                common_traps=['Court must approve', 'Child provisions modifiable', 'Merger vs incorporation'],
            ),
            KnowledgeNode(
                concept_id="family_mediation",
                name="Mediation & ADR",
                subject="family_law",
                difficulty=2,
                rule_statement="Alternative dispute resolution; mediator facilitates; confidential; many jurisdictions require mediation attempt; custody mediation common",
                elements=['Facilitative process', 'Confidentiality', 'Mandatory in some places', 'Custody focus'],
                common_traps=['Confidentiality protections', 'No binding decision', 'Mandatory mediation'],
            ),
            KnowledgeNode(
                concept_id="family_tax_consequences",
                name="Tax Consequences of Divorce",
                subject="family_law",
                difficulty=3,
                rule_statement="Property transfers: generally tax-free; Alimony: post-2018 not deductible/taxable; Child support: not deductible/taxable; Dependency exemptions",
                elements=['Property transfer rules', 'Alimony tax treatment', 'Child support treatment', 'Exemptions'],
                common_traps=['2018 tax law changes', 'Property transfer tax-free', 'Child support never deductible'],
            ),
            KnowledgeNode(
                concept_id="family_bankruptcy",
                name="Bankruptcy & Family Law",
                subject="family_law",
                difficulty=3,
                rule_statement="Child support non-dischargeable; spousal support non-dischargeable; property division may be dischargeable; automatic stay exceptions",
                elements=['Support obligations survive', 'Property division varies', 'Stay exceptions', 'Priority debts'],
                common_traps=['Support never dischargeable', 'Property division in Ch 13', 'Stay exceptions'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_secured_transactions(self):
        """18 Secured Transactions concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="secured_types_collateral",
                name="Types of Collateral",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods: consumer, equipment, farm products, inventory; Intangibles: accounts, instruments, documents, chattel paper, investment property, deposit accounts",
                elements=['Goods categories', 'Intangibles', 'Classification determines rules', 'Use-based for goods'],
                common_traps=['Use determines goods classification', 'Dual-use situations', 'Transformation changes type'],
            ),
            KnowledgeNode(
                concept_id="secured_after_acquired",
                name="After-Acquired Property Clause",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Security interest attaches to after-acquired property if clause included; automatic for inventory and accounts; exception for consumer goods",
                elements=['Requires clause', 'Automatic inventory/accounts', 'Consumer goods limit', 'Attaches when acquired'],
                common_traps=['Consumer goods 10-day limit', 'Inventory automatic', 'Must have clause'],
            ),
            KnowledgeNode(
                concept_id="secured_proceeds",
                name="Proceeds",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Security interest continues in proceeds; automatically perfected for 20 days; must perfect afterward; identifiable proceeds required",
                elements=['Automatic security interest', '20-day perfection', 'Must perfect after', 'Identifiable standard'],
                common_traps=['20-day temporary perfection', 'Lowest intermediate balance rule', 'Cash proceeds'],
            ),
            KnowledgeNode(
                concept_id="secured_future_advances",
                name="Future Advances",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Security interest can secure future loans; priority from original perfection if within 45 days or committed",
                elements=['Secures future debts', 'Original priority', '45-day rule', 'Commitment'],
                common_traps=['Priority relates back', '45-day rule', 'Optional vs committed'],
            ),
            KnowledgeNode(
                concept_id="secured_bioc",
                name="Buyer in Ordinary Course",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="BIOC takes free of security interest in inventory even if perfected and knows; must be ordinary course; good faith; value given",
                elements=['Takes free', 'Inventory only', 'Ordinary course', 'Good faith + value'],
                common_traps=['Takes free even with knowledge', 'Inventory only', 'Ordinary course requirement'],
                # Mnemonic: BIOC: Buyer, Inventory, Ordinary, Course (takes free)
            ),
            KnowledgeNode(
                concept_id="secured_fixtures",
                name="Fixtures",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Personal property that becomes real property; fixture filing perfects; PMSI fixture has priority if: filed before or within 20 days, construction mortgage exception",
                elements=['Fixture definition', 'Fixture filing', 'PMSI priority', 'Construction mortgage'],
                common_traps=['20-day grace period', 'Construction mortgage wins', 'Fixture filing location'],
            ),
            KnowledgeNode(
                concept_id="secured_accessions",
                name="Accessions",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods installed in other goods; security interest continues; perfection required; removal right if no material harm",
                elements=['Continues in accession', 'Perfection needed', 'Priority rules', 'Removal rights'],
                common_traps=['First to file wins', 'Material harm test', 'PMSI super-priority'],
            ),
            KnowledgeNode(
                concept_id="secured_commingled",
                name="Commingled Goods",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods physically united in product; security interest continues in product; perfection continues; priority prorata by value",
                elements=['Continues in product', 'Perfection continues', 'Pro rata priority', 'Cannot separate'],
                common_traps=['Pro rata distribution', 'Cannot separate', 'Perfection continues'],
            ),
            KnowledgeNode(
                concept_id="secured_investment_property",
                name="Investment Property",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Securities, security entitlements, accounts; perfection by control or filing; control has priority over filing",
                elements=['Control perfection', 'Filing alternative', 'Control priority', 'Types included'],
                common_traps=['Control beats filing', 'Control methods', 'Securities intermediary'],
            ),
            KnowledgeNode(
                concept_id="secured_deposit_accounts",
                name="Deposit Accounts",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Can only perfect by control; control: secured party is bank, control agreement, or secured party is account holder",
                elements=['Control only', 'Three methods', 'No filing perfection', 'Priority by control'],
                common_traps=['Cannot perfect by filing', 'Control methods', 'Bank as secured party'],
            ),
            KnowledgeNode(
                concept_id="secured_lien_creditor",
                name="Lien Creditors",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Secured party vs lien creditor: perfected wins; unperfected loses unless PMSI grace period; trustee in bankruptcy is lien creditor",
                elements=['Perfected beats lien creditor', 'Unperfected loses', 'PMSI grace period', 'Bankruptcy trustee'],
                common_traps=['Trustee as lien creditor', 'PMSI grace period', 'Perfection timing critical'],
            ),
            KnowledgeNode(
                concept_id="secured_continuation",
                name="Continuation Statements",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Filing effective 5 years; continuation filed within 6 months before lapse; extends another 5 years",
                elements=['5-year duration', '6-month window', 'Extends 5 years', 'Must be timely'],
                common_traps=['6-month window', 'Lapses if not filed', 'Calculation of dates'],
            ),
            KnowledgeNode(
                concept_id="secured_termination",
                name="Termination Statements",
                subject="secured_transactions",
                difficulty=2,
                rule_statement="Secured party must file termination when debt paid; consumer goods: 1 month or 20 days if requested; other collateral: on demand",
                elements=['Must file when paid', 'Consumer timing', 'Non-consumer on demand', 'Penalties for failure'],
                common_traps=['Consumer timing strict', 'Must file termination', 'Failure penalties'],
            ),
            KnowledgeNode(
                concept_id="secured_assignments",
                name="Assignment of Security Interest",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Can assign security interest; need not file unless assignee wants priority over later assignee; notification to debtor",
                elements=['Assignability', 'Filing not required', 'Priority of assignees', 'Debtor notification'],
                common_traps=['Filing not required for perfection', 'Priority among assignees', 'Debtor payment rules'],
            ),
            KnowledgeNode(
                concept_id="secured_agricultural_liens",
                name="Agricultural Liens",
                subject="secured_transactions",
                difficulty=2,
                rule_statement="Non-consensual lien on farm products; perfection by filing; priority rules similar to Article 9; statute creates",
                elements=['Statutory lien', 'Farm products', 'Filing perfects', 'Similar priority'],
                common_traps=['Not security interest', 'Statutory basis', 'Filing required'],
            ),
            KnowledgeNode(
                concept_id="secured_bankruptcy_trustee",
                name="Bankruptcy Trustee Powers",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Trustee has strong-arm power: lien creditor status; can avoid unperfected interests; 90-day preference period for perfection",
                elements=['Lien creditor status', 'Avoid unperfected', '90-day preference', 'Filing relates back'],
                common_traps=['90-day preference', 'Grace period protection', 'Relates back if timely'],
            ),
            KnowledgeNode(
                concept_id="secured_preferences",
                name="Preferences in Bankruptcy",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Transfer within 90 days while insolvent that prefers creditor can be avoided; exceptions: contemporaneous exchange, ordinary course, PMSI grace",
                elements=['90-day lookback', 'Insolvency presumed', 'Preference elements', 'Exceptions'],
                common_traps=['90 days', 'PMSI grace period exception', 'Ordinary course exception'],
            ),
            KnowledgeNode(
                concept_id="secured_fraudulent_transfers",
                name="Fraudulent Transfers",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Transfer to hinder, delay, defraud creditors; transfer for less than reasonably equivalent value while insolvent; can be avoided",
                elements=['Actual fraud', 'Constructive fraud', 'Reasonably equivalent value', 'Insolvency'],
                common_traps=['Actual vs constructive', 'Timing', 'Badges of fraud'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_iowa_procedure(self):
        """15 Iowa Procedure concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="iowa_pleading",
                name="Iowa Pleading Requirements",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Iowa requires notice pleading similar to federal; original notice serves as complaint; must state claim upon which relief can be granted",
                elements=['Original notice', 'Notice pleading', 'State claim', 'Similar to federal'],
                common_traps=['Original notice terminology', 'Similar to FRCP', 'Specific Iowa forms'],
            ),
            KnowledgeNode(
                concept_id="iowa_service",
                name="Iowa Service of Process",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Personal service by sheriff or process server; substituted service available; service by publication with court approval",
                elements=['Personal service', 'Sheriff service', 'Substituted service', 'Publication service'],
                common_traps=['Sheriff preference', 'Publication requirements', 'Proof of service'],
            ),
            KnowledgeNode(
                concept_id="iowa_discovery",
                name="Iowa Discovery Rules",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Iowa discovery mirrors federal rules; interrogatories, depositions, requests for production, admissions; proportionality applies",
                elements=['Federal model', 'All federal tools', 'Proportionality', 'Protective orders'],
                common_traps=['Similar to federal', 'Iowa-specific limits', 'Timing differences'],
            ),
            KnowledgeNode(
                concept_id="iowa_summary_judgment",
                name="Iowa Summary Judgment",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Available if no genuine issue of material fact; moving party burden; view evidence in light favorable to non-movant",
                elements=['No genuine issue', 'Material fact', 'Moving party burden', 'Favorable view'],
                common_traps=['Standard similar to federal', 'Iowa case law', 'Timing requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_trial_procedures",
                name="Iowa Trial Procedures",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Jury trial right; voir dire conducted by judge typically; Iowa Rules of Evidence govern; jury instructions settled before trial",
                elements=['Jury right', 'Judge voir dire', 'Evidence rules', 'Jury instructions'],
                common_traps=['Judge-conducted voir dire', 'Iowa evidence rules', 'Pre-trial procedures'],
            ),
            KnowledgeNode(
                concept_id="iowa_appeals",
                name="Iowa Appellate Procedure",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Appeal to Iowa Court of Appeals or Supreme Court; notice of appeal within 30 days; record and brief requirements; standards of review",
                elements=['30-day deadline', 'Notice of appeal', 'Record requirements', 'Standards of review'],
                common_traps=['30-day deadline strict', 'Direct to Supreme Court options', 'Preservation requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_venue",
                name="Iowa Venue",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Proper venue: defendant residence, cause of action arose, property located, contract performed; transfer available",
                elements=['Defendant residence', 'Cause arose', 'Property location', 'Transfer possible'],
                common_traps=['Multiple proper venues', 'Transfer discretion', 'Convenience factors'],
            ),
            KnowledgeNode(
                concept_id="iowa_jurisdiction",
                name="Iowa Personal Jurisdiction",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Long-arm statute reaches constitutional limits; minimum contacts required; purposeful availment; fair play and substantial justice",
                elements=['Long-arm statute', 'Constitutional limits', 'Minimum contacts', 'Fairness test'],
                common_traps=['Constitutional analysis', 'Specific vs general', 'Stream of commerce'],
            ),
            KnowledgeNode(
                concept_id="iowa_joinder",
                name="Iowa Joinder Rules",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Permissive joinder of parties and claims; compulsory joinder of necessary parties; intervention and interpleader available",
                elements=['Permissive joinder', 'Necessary parties', 'Intervention', 'Interpleader'],
                common_traps=['Similar to federal', 'Iowa variations', 'Necessary vs indispensable'],
            ),
            KnowledgeNode(
                concept_id="iowa_class_actions",
                name="Iowa Class Actions",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Class actions permitted; requirements similar to federal; certification required; notice to class members",
                elements=['Certification requirements', 'Numerosity', 'Commonality', 'Notice'],
                common_traps=['Certification motion', 'Opt-out rights', 'Settlement approval'],
            ),
            KnowledgeNode(
                concept_id="iowa_injunctions",
                name="Iowa Injunctions",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Temporary and permanent injunctions available; requirements: likelihood of success, irreparable harm, balance of harms, public interest",
                elements=['Temporary injunction', 'Permanent injunction', 'Four factors', 'Bond requirement'],
                common_traps=['Four-factor test', 'Bond for temporary', 'Hearing requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_judgments",
                name="Iowa Judgments",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Default judgment available; directed verdict/JNOV motions; new trial motions; judgment liens; enforcement procedures",
                elements=['Default judgment', 'Post-trial motions', 'Judgment liens', 'Enforcement'],
                common_traps=['Motion timing', 'Lien procedures', 'Enforcement methods'],
            ),
            KnowledgeNode(
                concept_id="iowa_execution",
                name="Iowa Execution & Garnishment",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Execution on judgment; garnishment of wages and accounts; exemptions protect certain property; procedures for collection",
                elements=['Execution process', 'Garnishment', 'Exemptions', 'Debtor protections'],
                common_traps=['Iowa exemptions', 'Garnishment limits', 'Procedures'],
            ),
            KnowledgeNode(
                concept_id="iowa_sanctions",
                name="Iowa Sanctions",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Court may sanction frivolous filings, discovery abuse, contempt; attorney fees available; Rule 1.413 governs",
                elements=['Frivolous filings', 'Discovery sanctions', 'Contempt', 'Attorney fees'],
                common_traps=['Rule 1.413', 'Standards for sanctions', 'Safe harbor'],
            ),
            KnowledgeNode(
                concept_id="iowa_adr",
                name="Iowa ADR Procedures",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Mediation encouraged; arbitration enforceable; case management conferences; settlement conferences",
                elements=['Mediation', 'Arbitration', 'Case management', 'Settlement conferences'],
                common_traps=['Mandatory mediation in some cases', 'Arbitration enforcement', 'Confidentiality'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_professional_responsibility(self):
        """26 Professional Responsibility concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="prof_resp_communication_detailed",
                name="Communication with Client",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer must reasonably inform client of status, respond to requests, explain matters for informed decisions, and communicate settlement offers promptly",
                elements=['Keep informed', 'Respond to requests', 'Explain for decisions', 'Prompt settlement communication'],
                common_traps=['Not informing of settlement offers', 'Not explaining enough', 'Missing scope decisions'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_declining_terminating",
                name="Declining & Terminating Representation",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must decline if rules violation; may withdraw for legitimate reasons; court approval if litigation; protect client interests",
                elements=['Mandatory withdrawal', 'Permissive withdrawal', 'Court approval', 'Protect interests'],
                common_traps=['No court permission in litigation', 'Not giving notice', 'Not returning property'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_safekeeping_detailed",
                name="Safekeeping Property",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Separate account required; maintain records; prompt delivery; accounting on request; disputed funds kept separate",
                elements=['Separate account (IOLTA)', 'Complete records', 'Prompt delivery', 'Accounting'],
                common_traps=['Commingling', 'Using client funds temporarily', 'Not separating disputed funds'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_advertising_detailed",
                name="Advertising & Solicitation Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May advertise if truthful; no live solicitation if significant pecuniary motive; specialization limits",
                elements=['Advertising permitted if truthful', 'No false/misleading', 'Solicitation restrictions', 'Specialization rules'],
                common_traps=['All solicitation prohibited', 'In-person to accident victims', 'Claiming specialization without certification'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_impartiality_detailed",
                name="Impartiality of Tribunal",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="No ex parte with judge; no improper jury influence; maintain decorum; no prejudicial conduct",
                elements=['No ex parte with judge', 'No improper jury influence', 'Maintain decorum', 'No prejudicial conduct'],
                common_traps=['Ex parte exceptions', 'Gifts to judges', 'Lawyer-judge commentary'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_trial_publicity_detailed",
                name="Trial Publicity Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot make statements with substantial likelihood of materially prejudicing proceeding; safe harbor statements permitted",
                elements=['Substantial likelihood test', 'Material prejudice', 'Criminal heightened', 'Safe harbor'],
                common_traps=['Public record info permitted', 'Heightened in criminal', 'First Amendment balance'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_judges_detailed",
                name="Judge & Former Judge Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Judge must maintain independence, avoid impropriety appearance; former judge cannot represent in matter participated",
                elements=['Independence', 'Impartiality', 'Disqualification', 'Former judge limits'],
                common_traps=['Former judge prior matter', 'Appearance of impropriety', 'Report misconduct duty'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_law_firms_detailed",
                name="Law Firm Responsibilities",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Partners/supervisors ensure compliance; subordinates follow rules; firm-wide measures required; conflicts imputed",
                elements=['Supervisory duties', 'Subordinate duties', 'Firm measures', 'Conflict imputation'],
                common_traps=['Subordinate still liable', 'Screening laterals', 'Firm name restrictions'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_unauthorized_practice",
                name="Unauthorized Practice of Law",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer cannot practice where not admitted; cannot assist non-lawyer in unauthorized practice; multijurisdictional practice rules",
                elements=['Admission requirements', 'No assisting non-lawyers', 'MJP exceptions', 'Pro hac vice'],
                common_traps=['MJP exceptions', 'Temporary practice', 'Assisting UPL'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_sale_law_practice",
                name="Sale of Law Practice",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May sell practice if: entire practice or area sold, written client notice, fees not increased",
                elements=['Entire practice or area', 'Written notice', 'No fee increase', 'Client consent'],
                common_traps=['Must sell entire area', 'Client can reject', 'Cannot increase fees'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_reporting_misconduct",
                name="Reporting Professional Misconduct",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer must report other lawyer's violations raising substantial question about honesty, trustworthiness, fitness",
                elements=['Must report violations', 'Substantial question test', 'Confidentiality exceptions', 'Self-reporting'],
                common_traps=['Confidentiality not absolute', 'Substantial question threshold', 'Judge misconduct reporting'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_disciplinary_procedures",
                name="Disciplinary Procedures",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="State supreme court inherent authority; disciplinary board investigates; sanctions range from private reprimand to disbarment",
                elements=['Supreme court authority', 'Investigation process', 'Sanctions range', 'Reciprocal discipline'],
                common_traps=['Inherent authority', 'Burden of proof', 'Reciprocal discipline rules'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_multijurisdictional",
                name="Multijurisdictional Practice",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="May practice temporarily if: related to admitted practice, arbitration/mediation, reasonably related to practice, pro hac vice",
                elements=['Temporary practice exceptions', 'Related to home practice', 'Pro hac vice', 'Systematic presence prohibited'],
                common_traps=['Cannot establish office', 'Related to home practice', 'Temporary only'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_litigation_conduct",
                name="Conduct in Litigation",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must not: abuse discovery, fail to disclose controlling authority, falsify evidence, make frivolous claims",
                elements=['No discovery abuse', 'Disclose adverse authority', 'No false evidence', 'No frivolous claims'],
                common_traps=['Adverse authority in controlling jurisdiction', 'Discovery proportionality', 'Good faith extensions OK'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_transactions_with_client",
                name="Business Transactions with Clients",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot enter business transaction unless: terms fair and reasonable, disclosed in writing, client has independent counsel opportunity, client consents in writing",
                elements=['Fair and reasonable', 'Written disclosure', 'Independent counsel opportunity', 'Written consent'],
                common_traps=['All four required', 'Full disclosure needed', 'Independent counsel chance'],
                # Mnemonic: FICO: Fair, Independent counsel, Consent, Opportunity
            ),
            KnowledgeNode(
                concept_id="prof_resp_literary_rights",
                name="Literary & Media Rights",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot acquire literary or media rights to representation before conclusion; may contract for reasonable expenses of publication after conclusion",
                elements=['No rights before conclusion', 'May contract after', 'Reasonable expenses only', 'Avoid conflict'],
                common_traps=['Timing - must wait until conclusion', 'May negotiate after', 'Conflict of interest concern'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_financial_assistance",
                name="Financial Assistance to Client",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot provide financial assistance except: advance court costs and expenses, contingent on outcome; may pay costs for indigent client",
                elements=['May advance costs', 'Repayment contingent on outcome', 'May pay for indigent', 'No personal living expenses'],
                common_traps=['Cannot advance living expenses', 'Can advance litigation costs', 'Indigent exception'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_former_government_lawyer",
                name="Former Government Lawyer",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent in matter personally and substantially participated in as government lawyer; screening can cure; cannot use confidential government information",
                elements=['Personally and substantially test', 'Screening available', 'No confidential info use', 'Negotiating employment'],
                common_traps=['Screening can cure conflict', 'Personal and substantial both required', 'Confidential info permanent bar'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_former_judge_arbitrator",
                name="Former Judge or Arbitrator",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent anyone in matter participated in as judge, arbitrator, mediator, or other neutral; screening cannot cure",
                elements=['Cannot represent in prior matter', 'Participated as neutral', 'Screening cannot cure', 'Negotiating employment restriction'],
                common_traps=['Screening does NOT cure (unlike gov lawyer)', 'Participated in any capacity', 'Negotiating employment limits'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_imputed_conflicts",
                name="Imputation of Conflicts",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Lawyer conflicts imputed to all in firm unless: personal interest, former client with screening, former government lawyer with screening",
                elements=['General imputation rule', 'Personal interest exception', 'Former client screening', 'Government lawyer screening'],
                common_traps=['Three main exceptions', 'Screening procedures', 'Timely screening required'],
                # Mnemonic: PFG: Personal, Former client, Government (exceptions to imputation)
            ),
            KnowledgeNode(
                concept_id="prof_resp_nonlawyer_assistants",
                name="Responsibilities for Nonlawyer Assistants",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer responsible for nonlawyer assistants' conduct; must ensure compliance with professional rules; cannot delegate legal judgment",
                elements=['Supervisory responsibility', 'Ensure compliance', 'Cannot delegate legal judgment', 'Ethical violations imputed'],
                common_traps=['Lawyer still responsible', 'Cannot avoid by delegation', 'Must supervise adequately'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_fee_division",
                name="Fee Division with Lawyers",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May divide fee with another lawyer if: proportional to services or joint responsibility, client agrees in writing, total fee reasonable",
                elements=['Proportional or joint responsibility', 'Written client agreement', 'Total fee reasonable', 'No division with non-lawyer'],
                common_traps=['Proportion or responsibility both OK', 'Client must agree', 'Cannot divide with non-lawyer'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_aggregate_settlements",
                name="Aggregate Settlements",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot participate in aggregate settlement unless each client gives informed consent in writing after disclosure of all material terms",
                elements=['Each client must consent', 'Informed consent', 'Written', 'Disclosure of all terms'],
                common_traps=['Every client must agree', 'Full disclosure required', 'Cannot coerce holdouts'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_limiting_liability",
                name="Limiting Liability & Malpractice",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot prospectively limit malpractice liability unless client independently represented; may settle malpractice claim if client advised to seek independent counsel",
                elements=['No prospective limits without independent counsel', 'May settle if advised', 'Full disclosure required', 'Independent advice'],
                common_traps=['Prospective limits rare', 'Settlement requires advice', 'Independent counsel key'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_sexual_relations",
                name="Sexual Relations with Clients",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot have sexual relations with client unless consensual relationship existed before attorney-client relationship",
                elements=['Prohibited unless preexisting', 'Consent not defense', 'Exploitation concern', 'Impairs judgment'],
                policy_rationales=['Prevent exploitation', 'Avoid conflicts', 'Protect judgment'],
                common_traps=['Preexisting relationship exception only', 'Consent insufficient', 'Judgment impairment'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_appearance_of_impropriety",
                name="Appearance of Impropriety",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer should avoid even appearance of impropriety; upholds confidence in legal profession; aspirational standard",
                elements=['Avoid appearance', 'Public confidence', 'Aspirational', 'Reasonable person test'],
                common_traps=['Aspirational not enforceable alone', 'Reasonable person view', 'Supplements specific rules'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_corporations(self):
        """27 Corporations concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="corp_promoter_liability",
                name="Promoter Liability",
                subject="corporations",
                difficulty=3,
                rule_statement="Promoter liable on pre-incorporation contracts unless novation; corporation liable if adopts contract expressly or impliedly",
                elements=['Promoter personally liable', 'Corporation liable if adopts', 'Novation releases promoter', 'Implied adoption'],
                common_traps=['Both can be liable', "Adoption doesn't release", 'Need novation for release'],
            ),
            KnowledgeNode(
                concept_id="corp_defective_incorporation",
                name="Defective Incorporation",
                subject="corporations",
                difficulty=3,
                rule_statement="De facto corporation: good faith attempt, actual use; corporation by estoppel: held out as corporation, third party dealt as such",
                elements=['De facto corporation', 'Corporation by estoppel', 'Good faith attempt', 'Actual use'],
                common_traps=['Both doctrines exist', 'Protects from personal liability', 'Narrow application'],
            ),
            KnowledgeNode(
                concept_id="corp_ultra_vires",
                name="Ultra Vires Acts",
                subject="corporations",
                difficulty=2,
                rule_statement="Acts beyond corporate powers; generally enforceable but shareholders can enjoin, corporation can sue officers, state can dissolve",
                elements=['Beyond stated purpose', 'Generally enforceable', 'Limited remedies', 'Rare doctrine'],
                common_traps=['Contract still enforceable', 'Internal remedy', 'Rarely succeeds'],
            ),
            KnowledgeNode(
                concept_id="corp_subscriptions",
                name="Stock Subscriptions",
                subject="corporations",
                difficulty=3,
                rule_statement="Pre-incorporation subscription irrevocable for six months unless otherwise provided; post-incorporation governed by contract law",
                elements=['Pre-incorporation irrevocable', 'Six month rule', 'Post-incorporation contract', 'Payment terms'],
                common_traps=['Pre vs post timing', 'Irrevocability period', 'Contract law post-incorporation'],
            ),
            KnowledgeNode(
                concept_id="corp_consideration_shares",
                name="Consideration for Shares",
                subject="corporations",
                difficulty=3,
                rule_statement="Par value: must receive at least par; no-par: any consideration; watered stock: directors liable; good faith business judgment protects valuation",
                elements=['Par value minimum', 'No-par flexibility', 'Watered stock liability', 'Business judgment valuation'],
                common_traps=['Par vs no-par', 'Director liability watered stock', 'BJR protects valuation'],
            ),
            KnowledgeNode(
                concept_id="corp_preemptive_rights",
                name="Preemptive Rights",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders may have right to purchase new shares to maintain proportional ownership; must be expressly granted in modern law",
                elements=['Maintain proportional ownership', 'Must be in articles', 'Pro rata purchase right', 'Exceptions exist'],
                common_traps=['Must be expressly granted', 'Not automatic', 'Exceptions for compensation'],
            ),
            KnowledgeNode(
                concept_id="corp_distributions_dividends",
                name="Distributions & Dividends",
                subject="corporations",
                difficulty=3,
                rule_statement="Directors declare dividends using business judgment; unlawful if: insolvent, would cause insolvency, or exceeds statutory limits",
                elements=['Board discretion', 'Insolvency test', 'Statutory limits', 'Director liability'],
                common_traps=['Directors discretion wide', 'Insolvency prohibition', 'Directors personally liable'],
            ),
            KnowledgeNode(
                concept_id="corp_inspection_rights",
                name="Shareholder Inspection Rights",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders have right to inspect books and records for proper purpose; shareholder list more readily available than detailed financial records",
                elements=['Proper purpose required', 'Shareholder list easier', 'Books and records harder', 'Advance notice'],
                common_traps=['Proper purpose test', 'Different standards for different records', 'Timing requirements'],
            ),
            KnowledgeNode(
                concept_id="corp_meetings_notice",
                name="Meetings & Notice Requirements",
                subject="corporations",
                difficulty=2,
                rule_statement="Annual shareholders meeting required; notice required with time, place, purpose if special; directors can act without meeting if unanimous written consent",
                elements=['Annual meeting required', 'Notice requirements', 'Special meeting purpose', 'Written consent alternative'],
                common_traps=['Notice timing', 'Special meeting purpose specificity', 'Unanimous consent option'],
            ),
            KnowledgeNode(
                concept_id="corp_quorum_voting",
                name="Quorum & Voting Rules",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders: majority of shares is quorum, majority of votes present wins; Directors: majority of directors is quorum, majority of votes present wins",
                elements=['Shareholder quorum', 'Director quorum', 'Vote requirements', 'Can modify in articles/bylaws'],
                common_traps=['Quorum vs voting', 'Can change by agreement', 'Present vs outstanding'],
            ),
            KnowledgeNode(
                concept_id="corp_removal_directors",
                name="Removal of Directors",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders may remove with or without cause unless articles require cause; if cumulative voting, can remove only if votes sufficient to elect",
                elements=['Shareholder removal power', 'With or without cause', 'Cumulative voting protection', 'Articles can require cause'],
                common_traps=['Unless articles require cause', 'Cumulative voting protection', 'Only shareholders remove'],
            ),
            KnowledgeNode(
                concept_id="corp_indemnification",
                name="Indemnification of Directors/Officers",
                subject="corporations",
                difficulty=4,
                rule_statement="Mandatory if successful on merits; permissive if good faith and reasonable belief; prohibited if found liable to corporation",
                elements=['Mandatory if successful', 'Permissive if good faith', 'Prohibited if liable', 'Advancement of expenses'],
                common_traps=['Three categories', 'Successful = mandatory', 'Liable to corp = prohibited'],
                # Mnemonic: MAP: Mandatory, Allowed, Prohibited
            ),
            KnowledgeNode(
                concept_id="corp_close_corporations",
                name="Close Corporations",
                subject="corporations",
                difficulty=3,
                rule_statement="Few shareholders, no public market, restrictions on transfer; may operate informally; special statutory provisions protect minority",
                elements=['Few shareholders', 'Transfer restrictions', 'Informal operation allowed', 'Minority protection'],
                common_traps=['Can dispense with formalities', 'Oppression remedies', 'Statutory protections'],
            ),
            KnowledgeNode(
                concept_id="corp_shareholder_agreements",
                name="Shareholder Agreements",
                subject="corporations",
                difficulty=3,
                rule_statement="May restrict transfers, provide for management, require arbitration; must not treat corporation as partnership or injure creditors",
                elements=['Voting agreements', 'Buy-sell provisions', 'Transfer restrictions', 'Management agreements'],
                common_traps=['Cannot sterilize board', 'Must protect creditors', 'Binding on parties only'],
            ),
            KnowledgeNode(
                concept_id="corp_oppression_freeze_out",
                name="Oppression & Freeze-Out",
                subject="corporations",
                difficulty=4,
                rule_statement="Majority cannot squeeze out minority unfairly; remedies include buyout, dissolution, or damages; courts balance reasonable expectations",
                elements=['Oppressive conduct', 'Reasonable expectations', 'Buyout remedy', 'Dissolution alternative'],
                policy_rationales=['Protect minority', 'Prevent abuse of control', 'Balance interests'],
                common_traps=['Reasonable expectations test', 'Equitable remedies', 'Close corporation context'],
            ),
            KnowledgeNode(
                concept_id="corp_dividends_preferred",
                name="Preferred Stock Dividends",
                subject="corporations",
                difficulty=3,
                rule_statement="Preferred entitled to fixed dividend before common; cumulative unless stated non-cumulative; participating if so stated",
                elements=['Priority over common', 'Cumulative presumption', 'Participating possibility', 'Liquidation preference'],
                common_traps=['Cumulative unless stated otherwise', 'Arrears must be paid first', 'Participating rare'],
            ),
            KnowledgeNode(
                concept_id="corp_redemption_repurchase",
                name="Redemption & Share Repurchase",
                subject="corporations",
                difficulty=3,
                rule_statement="Corporation may repurchase shares if: not insolvent, adequate surplus; redemption rights if stated; insider trading concerns",
                elements=['Must have surplus', 'Insolvency test', 'Redemption vs repurchase', 'Insider trading risk'],
                common_traps=['Statutory requirements', 'Cannot make insolvent', 'Insider trading prohibition'],
            ),
            KnowledgeNode(
                concept_id="corp_sale_of_assets",
                name="Sale of Substantially All Assets",
                subject="corporations",
                difficulty=4,
                rule_statement="Requires board and shareholder approval; not ordinary course of business; selling corporation continues to exist; buyers can assume liabilities",
                elements=['Substantially all assets', 'Board and shareholder vote', 'Continues to exist', 'Successor liability rules'],
                common_traps=['Substantially all test', 'Continues to exist', 'Not automatic successor liability'],
            ),
            KnowledgeNode(
                concept_id="corp_tender_offers",
                name="Tender Offers",
                subject="corporations",
                difficulty=3,
                rule_statement="Offer to buy shares directly from shareholders; federal regulation; target board may defend; business judgment rule applies to defensive measures",
                elements=['Direct to shareholders', 'Federal securities law', 'Board defensive tactics', 'BJR applies'],
                common_traps=['Bypass board', 'Defensive measures reviewed', 'Unocal standard may apply'],
            ),
            KnowledgeNode(
                concept_id="corp_proxy_fights",
                name="Proxy Contests",
                subject="corporations",
                difficulty=3,
                rule_statement="Contest for board control via shareholder votes; federal proxy rules; corporation may reimburse incumbents; insurgents reimbursed if successful",
                elements=['Board control contest', 'Proxy solicitation rules', 'Reimbursement rules', 'Disclosure requirements'],
                common_traps=['Corporation can reimburse incumbents', 'Insurgents if successful', 'Federal regulation applies'],
            ),
            KnowledgeNode(
                concept_id="corp_hostile_takeovers",
                name="Hostile Takeovers & Defensive Tactics",
                subject="corporations",
                difficulty=4,
                rule_statement="Target board may defend using business judgment; must show reasonable threat and proportionate response; cannot be entrenching",
                elements=['Unocal standard', 'Reasonable threat', 'Proportionate response', 'Enhanced scrutiny'],
                common_traps=['Enhanced scrutiny', 'Cannot be entrenching', 'Proportionality key'],
                # Mnemonic: PRE: Proportionate, Reasonable threat, Enhanced scrutiny
            ),
            KnowledgeNode(
                concept_id="corp_appraisal_rights",
                name="Appraisal Rights",
                subject="corporations",
                difficulty=4,
                rule_statement="Dissenting shareholders entitled to fair value of shares in: mergers, sales of assets, amendments materially affecting rights",
                elements=['Fair value determination', 'Dissent and notice required', 'Exclusive remedy', 'Triggering events'],
                common_traps=['Must follow procedures exactly', 'Fair value not market value', 'Exclusive remedy if available'],
            ),
            KnowledgeNode(
                concept_id="corp_amendments_articles",
                name="Amending Articles of Incorporation",
                subject="corporations",
                difficulty=2,
                rule_statement="Requires board approval and shareholder vote; certain amendments require class vote if materially affect class",
                elements=['Board approval', 'Shareholder vote', 'Class voting rights', 'Filing required'],
                common_traps=['Class vote for material changes to class', 'Filing makes effective', 'Broad board power'],
            ),
            KnowledgeNode(
                concept_id="corp_bylaws",
                name="Bylaws",
                subject="corporations",
                difficulty=2,
                rule_statement="Internal operating rules; typically adopted/amended by board unless articles reserve to shareholders; cannot conflict with articles or statutes",
                elements=['Internal rules', 'Board typically amends', 'Cannot conflict with articles', 'Operating procedures'],
                common_traps=['Board power unless reserved', 'Hierarchy: statute > articles > bylaws', 'Cannot expand powers'],
            ),
            KnowledgeNode(
                concept_id="corp_limited_liability_company",
                name="Limited Liability Companies (LLC)",
                subject="corporations",
                difficulty=3,
                rule_statement="Hybrid entity: corporate limited liability plus partnership flexibility; operating agreement governs; default rules vary by state",
                elements=['Limited liability', 'Pass-through taxation', 'Operating agreement', 'Flexible management'],
                common_traps=['Operating agreement controls', 'Default rules vary', 'Veil piercing still possible'],
            ),
            KnowledgeNode(
                concept_id="corp_partnerships_general",
                name="General Partnerships",
                subject="corporations",
                difficulty=3,
                rule_statement="Formation by agreement or co-ownership for profit; each partner agent; jointly and severally liable; equal sharing unless agreed",
                elements=['No formalities', 'Each partner agent', 'Unlimited liability', 'Equal sharing default'],
                common_traps=['Joint and several liability', 'Each partner can bind', 'No filing required'],
            ),
            KnowledgeNode(
                concept_id="corp_limited_partnerships",
                name="Limited Partnerships",
                subject="corporations",
                difficulty=3,
                rule_statement="General partners manage and liable; limited partners passive investors with liability limited to investment; filing required",
                elements=['GP manages and liable', 'LP limited liability', 'Filing required', 'LP cannot control'],
                common_traps=['LP control destroys limited liability', 'Must file certificate', 'GP fully liable'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_wills_trusts_estates(self):
        """37 Wills Trusts Estates concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="wills_capacity",
                name="Testamentary Capacity",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Testator must be 18+, understand nature of act, extent of property, natural objects of bounty, plan of disposition",
                elements=['Age 18+', 'Understand nature', 'Know property', 'Natural objects', 'Dispositional plan'],
                common_traps=['Lower standard than contractual', 'Lucid intervals count', 'Burden on contestants'],
                # Mnemonic: PENDO: Property, Estate, Nature, Disposition, Objects
            ),
            KnowledgeNode(
                concept_id="wills_attestation",
                name="Attestation & Witnesses",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Two witnesses must attest; must be present at same time; interested witness issues; purging statutes may apply",
                elements=['Two witnesses', 'Simultaneous presence', 'Sign in testator presence', 'Competent witnesses'],
                common_traps=['Line of sight test', 'Interested witness loses bequest', 'Purging statutes'],
            ),
            KnowledgeNode(
                concept_id="wills_codicil",
                name="Codicils",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Testamentary instrument that modifies will; must meet same formalities; republishes will as of codicil date",
                elements=['Modifies existing will', 'Same formalities required', 'Republication effect', 'Integration'],
                common_traps=['Republication doctrine', 'Cures defects in will', 'Must meet formalities'],
            ),
            KnowledgeNode(
                concept_id="wills_incorporation_reference",
                name="Incorporation by Reference",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="External document incorporated if: exists when will executed, will manifests intent, will describes sufficiently",
                elements=['Document must exist', 'Intent to incorporate', 'Sufficient description', 'Extrinsic evidence'],
                common_traps=['Must exist at execution', 'Cannot incorporate future documents', 'Description requirement'],
            ),
            KnowledgeNode(
                concept_id="wills_acts_of_independent_significance",
                name="Acts of Independent Significance",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Will can refer to acts/events with significance apart from testamentary effect; non-testamentary motive required",
                elements=['Independent significance', 'Non-testamentary purpose', 'Changes effective', 'Common examples'],
                common_traps=['Must have independent purpose', 'Contents of wallet example', 'Beneficiary designation'],
            ),
            KnowledgeNode(
                concept_id="wills_holographic",
                name="Holographic Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Handwritten, signed, material provisions in testator handwriting; no witnesses required in states recognizing",
                elements=['Handwritten', 'Signed', 'Material provisions', 'No witnesses'],
                common_traps=['Not all states recognize', 'Material portions test', 'Intent to be will'],
            ),
            KnowledgeNode(
                concept_id="wills_conditional",
                name="Conditional Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Will effective only if condition occurs; distinguishing condition of execution from condition of revocation",
                elements=['Condition must occur', 'Condition vs motive', 'Extrinsic evidence', 'Interpretation issues'],
                common_traps=['Condition vs motive', 'Presumption against conditional', 'Proof required'],
            ),
            KnowledgeNode(
                concept_id="wills_revocation_dependent_relative",
                name="Dependent Relative Revocation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revocation ineffective if based on mistake of law/fact and would not have revoked but for mistake",
                elements=['Mistaken revocation', 'Would not have revoked', 'Testator intent', 'Second-best result'],
                common_traps=['Applies when mistake', 'Second best over intestacy', 'Intent focus'],
            ),
            KnowledgeNode(
                concept_id="wills_revival",
                name="Revival of Revoked Wills",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="When revoking instrument revoked, three approaches: automatic revival, testator intent, no revival absent re-execution",
                elements=['Revocation of revocation', 'Majority: intent controls', 'Minority: automatic', 'Minority: re-execution'],
                common_traps=['State law varies', 'Intent evidence', 'May need re-execution'],
            ),
            KnowledgeNode(
                concept_id="wills_lapse_anti_lapse",
                name="Lapse & Anti-Lapse",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Bequest lapses if beneficiary predeceases; anti-lapse saves gift if beneficiary in protected class and leaves issue",
                elements=['Lapse when predecease', 'Anti-lapse statute', 'Protected class', 'Issue substitute'],
                common_traps=['Protected class varies', 'Issue requirement', 'Express contrary intent'],
                # Mnemonic: ACID: Anti-lapse, Class, Issue, Descendants
            ),
            KnowledgeNode(
                concept_id="wills_ademption",
                name="Ademption by Extinction",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Specific gift adeemed if not in estate at death; identity theory vs intent theory",
                elements=['Specific gift only', 'Not in estate', 'Identity theory', 'Intent theory minority'],
                common_traps=['Specific vs general/demonstrative', 'Exceptions may apply', 'Insurance proceeds'],
            ),
            KnowledgeNode(
                concept_id="wills_ademption_satisfaction",
                name="Ademption by Satisfaction",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Lifetime gift to beneficiary may satisfy testamentary gift if: writing by testator, writing by beneficiary, or property declares satisfaction",
                elements=['Lifetime gift', 'Testamentary gift', 'Writing requirement', 'Intent to satisfy'],
                common_traps=['Need writing', 'Presumption against', 'Value determination'],
            ),
            KnowledgeNode(
                concept_id="wills_abatement",
                name="Abatement",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Reduce gifts when assets insufficient; order: intestate property, residuary, general, demonstrative, specific",
                elements=['Insufficient assets', 'Priority order', 'Pro rata within class', 'Can change by will'],
                common_traps=['Standard order', 'Pro rata reduction', 'Will can change'],
                # Mnemonic: IRGDS: Intestate, Residuary, General, Demonstrative, Specific (reverse priority)
            ),
            KnowledgeNode(
                concept_id="wills_exoneration",
                name="Exoneration of Liens",
                subject="wills_trusts_estates",
                difficulty=2,
                rule_statement="Traditional: estate pays off liens; Modern UPC: beneficiary takes subject to liens unless will directs payment",
                elements=['Liens on specific gifts', 'Traditional: estate pays', 'UPC: beneficiary takes with', 'Will can direct'],
                common_traps=['UPC changed rule', 'Specific direction needed', 'Mortgage example'],
            ),
            KnowledgeNode(
                concept_id="wills_pretermitted_spouse",
                name="Pretermitted Spouse",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Spouse married after will takes intestate share unless: will contemplates marriage, provided for outside will, intentionally omitted",
                elements=['After-will marriage', 'Intestate share', 'Three exceptions', 'Intent evidence'],
                common_traps=['Exceptions apply', 'Burden of proof', 'Not divorce'],
            ),
            KnowledgeNode(
                concept_id="wills_pretermitted_children",
                name="Pretermitted Children",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Child born/adopted after will takes share unless: intentional omission shown, provided for outside will, or all to other parent",
                elements=['After-will child', 'Share calculation', 'Three exceptions', 'All estate to parent exception'],
                common_traps=['Share calculation complex', 'All-to-parent exception', 'Adopted children included'],
            ),
            KnowledgeNode(
                concept_id="wills_elective_share",
                name="Elective Share",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Surviving spouse can elect statutory share (typically 1/3 or 1/2) instead of will provision; time limit applies",
                elements=['Statutory percentage', 'Augmented estate', 'Time to elect', 'Cannot waive before marriage'],
                common_traps=['Augmented estate includes transfers', 'Time limit strict', 'Prenup can waive'],
            ),
            KnowledgeNode(
                concept_id="wills_undue_influence",
                name="Undue Influence",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Substituted will of influencer for testator; requires: susceptibility, opportunity, disposition to influence, unnatural result",
                elements=['Susceptibility', 'Opportunity', 'Active procurement', 'Unnatural result'],
                common_traps=['Four elements', 'Burden on contestant', 'Presumption if confidential relation + benefit'],
            ),
            KnowledgeNode(
                concept_id="wills_fraud",
                name="Fraud",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="False statement material to testamentary disposition; fraud in execution vs inducement; constructive trust remedy",
                elements=['False representation', 'Known false', 'Testator reliance', 'Material'],
                common_traps=['Fraud in execution vs inducement', 'Constructive trust remedy', 'High burden'],
            ),
            KnowledgeNode(
                concept_id="wills_mistake",
                name="Mistake",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Mistake in execution may void; mistake in inducement generally not correctable; reformation limited",
                elements=['Mistake in execution', 'Mistake in inducement', 'Limited correction', 'Omitted text'],
                common_traps=['In execution voids', 'In inducement usually no remedy', 'Rare reformation'],
            ),
            KnowledgeNode(
                concept_id="wills_joint_mutual",
                name="Joint & Mutual Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Joint: one document for multiple testators; Mutual: reciprocal provisions; contract not to revoke requires clear evidence",
                elements=['Joint will', 'Mutual wills', 'Contract not to revoke', 'Proof required'],
                common_traps=['Presumption against contract', 'Must prove agreement', 'Remedy: constructive trust'],
            ),
            KnowledgeNode(
                concept_id="trusts_inter_vivos",
                name="Inter Vivos Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Created during settlor lifetime; requires delivery; can be revocable or irrevocable; avoids probate",
                elements=['Lifetime creation', 'Delivery required', 'Revocability', 'Probate avoidance'],
                common_traps=['Delivery requirement', 'Revocable unless stated', 'Pour-over wills'],
            ),
            KnowledgeNode(
                concept_id="trusts_testamentary",
                name="Testamentary Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Created by will; effective at death; must meet will formalities; subject to probate",
                elements=['Created by will', 'Will formalities', 'Effective at death', 'Probate required'],
                common_traps=['Will formalities apply', 'Goes through probate', 'Court supervision'],
            ),
            KnowledgeNode(
                concept_id="trusts_spendthrift",
                name="Spendthrift Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Beneficiary cannot transfer interest; creditors cannot reach; exceptions: certain creditors, excess beyond support",
                elements=['Transfer restraint', 'Creditor protection', 'Express provision needed', 'Exceptions exist'],
                common_traps=['Must be express', 'Exception creditors', 'Self-settled issues'],
            ),
            KnowledgeNode(
                concept_id="trusts_discretionary",
                name="Discretionary Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Trustee has discretion over distributions; standard may be absolute or limited; creditor protection",
                elements=['Trustee discretion', 'Absolute vs limited', 'Judicial review limited', 'Creditor protection'],
                common_traps=['Abuse of discretion standard', 'Good faith required', 'Creditor protection strong'],
            ),
            KnowledgeNode(
                concept_id="trusts_support",
                name="Support Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Trustee must distribute for support; mandatory if within standard; creditors providing necessaries can reach",
                elements=['Mandatory distributions', 'Support standard', 'Necessaries creditors', 'Interpretation'],
                common_traps=['Mandatory nature', 'Necessaries exception', 'Standard interpretation'],
            ),
            KnowledgeNode(
                concept_id="trusts_resulting",
                name="Resulting Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Arises by operation of law when: purchase money resulting trust, excess corpus, failure of express trust",
                elements=['Implied by law', 'Settlor gets back', 'Purchase money', 'Failure scenarios'],
                common_traps=['Returns to settlor', 'Operation of law', 'Limited situations'],
            ),
            KnowledgeNode(
                concept_id="trusts_constructive",
                name="Constructive Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Equitable remedy for unjust enrichment; wrongdoer holds property for rightful owner; fraud, breach of duty",
                elements=['Equitable remedy', 'Unjust enrichment', 'Wrongful conduct', 'Rightful owner recovers'],
                common_traps=['Remedy not true trust', 'Flexible application', 'Prevents unjust enrichment'],
            ),
            KnowledgeNode(
                concept_id="trusts_modification",
                name="Trust Modification & Termination",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revocable: settlor can modify/terminate; Irrevocable: need consent or changed circumstances; Claflin doctrine applies",
                elements=['Revocable settlor control', 'Irrevocable restrictions', 'Claflin doctrine', 'Changed circumstances'],
                common_traps=['Material purpose test', 'Consent requirements', 'Court modification limited'],
            ),
            KnowledgeNode(
                concept_id="trusts_powers",
                name="Trustee Powers",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Express powers in instrument; implied powers necessary to accomplish purpose; statutory default powers",
                elements=['Express powers', 'Implied powers', 'Statutory powers', 'Limits on powers'],
                common_traps=['Broadly construed', 'Statutory defaults', 'Cannot violate duty'],
            ),
            KnowledgeNode(
                concept_id="trusts_duty_inform",
                name="Duty to Inform & Account",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Must keep beneficiaries informed; provide annual accounting; respond to requests; disclosure of material facts",
                elements=['Keep informed', 'Annual accounting', 'Respond to requests', 'Material facts'],
                common_traps=['Affirmative duty', 'Reasonable information', 'Cannot hide behind instrument'],
            ),
            KnowledgeNode(
                concept_id="trusts_principal_income",
                name="Principal & Income Allocation",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Distinguish principal from income; Uniform Principal & Income Act provides rules; trustee adjusting power",
                elements=['Principal vs income', 'UPAIA rules', 'Adjusting power', 'Life tenant/remainder split'],
                common_traps=['UPAIA default rules', 'Power to adjust', 'Impartiality duty'],
            ),
            KnowledgeNode(
                concept_id="trusts_breach_remedies",
                name="Breach of Trust & Remedies",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Trustee liable for breach; remedies: damages, remove trustee, constructive trust, tracing; defenses: consent, exculpation clause",
                elements=['Liability for breach', 'Multiple remedies', 'Defenses available', 'Statute of limitations'],
                common_traps=['Multiple remedies possible', 'Exculpation limits', 'Consent defense'],
            ),
            KnowledgeNode(
                concept_id="rule_against_perpetuities",
                name="Rule Against Perpetuities",
                subject="wills_trusts_estates",
                difficulty=5,
                rule_statement="Interest must vest or fail within life in being plus 21 years; applies to contingent remainders, executory interests; reform statutes exist",
                elements=['Measuring lives', '21 year period', 'Must vest or fail', 'Contingent interests'],
                common_traps=['Contingent interests only', 'Reform statutes', 'Wait and see', 'Cy pres'],
                # Mnemonic: RAP applies to: contingent remainders, executory interests, class gifts, options, rights of first refusal
            ),
            KnowledgeNode(
                concept_id="powers_of_appointment",
                name="Powers of Appointment",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="General: appointee can appoint to self, estate, creditors; Special: limited class; affects estate taxation and creditors",
                elements=['General power', 'Special power', 'Exercise methods', 'Tax consequences'],
                common_traps=['General vs special', 'Default appointments', 'Tax implications'],
            ),
            KnowledgeNode(
                concept_id="estate_administration",
                name="Estate Administration Process",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Probate process: petition, notice, inventory, pay debts, distribute; executor/administrator duties; court supervision",
                elements=['Petition for probate', 'Notice to heirs', 'Inventory and appraisal', 'Pay debts then distribute'],
                common_traps=['Priority of payments', 'Creditor claims period', 'Accounting requirements'],
            ),
            KnowledgeNode(
                concept_id="nonprobate_transfers",
                name="Non-Probate Transfers",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Avoid probate: joint tenancy, POD/TOD accounts, life insurance, trusts; creditor rights may still apply",
                elements=['Joint tenancy', 'POD/TOD', 'Life insurance', 'Trust assets'],
                common_traps=['Avoid probate but not taxes', 'Creditor rights', "Will provisions don't control"],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_family_law(self):
        """25 Family Law concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="family_annulment",
                name="Annulment",
                subject="family_law",
                difficulty=3,
                rule_statement="Void marriage: bigamy, incest, mental incapacity; Voidable: age, impotence, fraud, duress, lack of consent",
                elements=['Void ab initio', 'Voidable until annulled', 'Grounds vary', 'Retroactive effect'],
                common_traps=['Void vs voidable', 'Retroactive effect', 'Property rights may survive'],
            ),
            KnowledgeNode(
                concept_id="family_separation",
                name="Legal Separation",
                subject="family_law",
                difficulty=2,
                rule_statement="Court-approved living apart; addresses support, property, custody; marriage continues; bars filed by separated spouse",
                elements=['Marriage continues', 'Court order', 'Same issues as divorce', 'Can convert to divorce'],
                common_traps=['Not divorce', 'Marriage continues', 'Same relief available'],
            ),
            KnowledgeNode(
                concept_id="family_jurisdiction",
                name="Divorce Jurisdiction",
                subject="family_law",
                difficulty=3,
                rule_statement="Divorce: domicile of one spouse; Property: in personam jurisdiction; Custody: UCCJEA home state",
                elements=['Domicile for divorce', 'Personal jurisdiction for property', 'UCCJEA for custody', 'Residency requirements'],
                common_traps=['Different jurisdiction rules', 'Divisible divorce', 'UCCJEA controls custody'],
            ),
            KnowledgeNode(
                concept_id="family_uccjea",
                name="UCCJEA Jurisdiction",
                subject="family_law",
                difficulty=4,
                rule_statement="Home state priority: where child lived 6 months before filing; significant connection if no home state; emergency jurisdiction limited",
                elements=['Home state priority', 'Significant connection', 'Emergency jurisdiction', 'Exclusive continuing jurisdiction'],
                common_traps=['Home state 6 months', 'Continuing jurisdiction', 'Emergency temporary only'],
                # Mnemonic: HSCE: Home state, Significant connection, Continuing, Emergency
            ),
            KnowledgeNode(
                concept_id="family_uifsa",
                name="UIFSA Support Enforcement",
                subject="family_law",
                difficulty=3,
                rule_statement="Uniform Interstate Family Support Act; continuing exclusive jurisdiction; direct interstate enforcement; one-order system",
                elements=['Issuing state keeps jurisdiction', 'Direct enforcement', 'No duplicate orders', 'Long-arm jurisdiction'],
                common_traps=['Continuing exclusive', 'Cannot modify elsewhere', 'Long-arm provisions'],
            ),
            KnowledgeNode(
                concept_id="family_modification_support",
                name="Modification of Support",
                subject="family_law",
                difficulty=4,
                rule_statement="Material change in circumstances required; cannot modify retroactively; voluntary unemployment may not count; burden on moving party",
                elements=['Material change', 'Prospective only', 'Substantial change', 'Voluntary acts'],
                common_traps=['Cannot modify past', 'Material change required', 'Voluntary unemployment'],
            ),
            KnowledgeNode(
                concept_id="family_modification_custody",
                name="Modification of Custody",
                subject="family_law",
                difficulty=4,
                rule_statement="Substantial change in circumstances; best interests of child; may require changed circumstances plus detrimental; restrictions on relitigation",
                elements=['Substantial change', 'Best interests', 'May need detriment', 'Time limitations'],
                common_traps=['Higher standard than initial', 'Detriment in some states', 'Relitigation restrictions'],
            ),
            KnowledgeNode(
                concept_id="family_enforcement",
                name="Support Enforcement",
                subject="family_law",
                difficulty=3,
                rule_statement="Contempt: civil or criminal; wage garnishment; license suspension; passport denial; federal locate services",
                elements=['Contempt sanctions', 'Wage withholding', 'License suspension', 'Federal enforcement'],
                common_traps=['Civil vs criminal contempt', 'Automatic withholding', 'Cannot discharge in bankruptcy'],
            ),
            KnowledgeNode(
                concept_id="family_contempt",
                name="Contempt Proceedings",
                subject="family_law",
                difficulty=3,
                rule_statement="Civil: coercive, must have ability to comply; Criminal: punitive, beyond reasonable doubt; inability to pay is defense",
                elements=['Civil coercive', 'Criminal punitive', 'Ability to pay', 'Purge conditions'],
                common_traps=['Civil vs criminal', 'Ability to pay defense', 'Burden of proof differs'],
            ),
            KnowledgeNode(
                concept_id="family_child_abuse",
                name="Child Abuse & Neglect",
                subject="family_law",
                difficulty=3,
                rule_statement="State intervention to protect child; removal requires hearing; reasonable efforts to reunify; termination of parental rights possible",
                elements=['Emergency removal', 'Court hearing', 'Reasonable efforts', 'TPR option'],
                common_traps=['Due process protections', 'Reasonable efforts', 'Clear and convincing for TPR'],
            ),
            KnowledgeNode(
                concept_id="family_termination_parental_rights",
                name="Termination of Parental Rights",
                subject="family_law",
                difficulty=4,
                rule_statement="Severs legal parent-child relationship; grounds: abuse, neglect, abandonment, unfitness; clear and convincing evidence; permanent",
                elements=['Statutory grounds', 'Clear and convincing', 'Permanent severance', 'Best interests'],
                common_traps=['High burden', 'Permanent', 'Best interests focus'],
            ),
            KnowledgeNode(
                concept_id="family_adoption",
                name="Adoption",
                subject="family_law",
                difficulty=3,
                rule_statement="Creates legal parent-child relationship; consent required from biological parents unless rights terminated; home study; finalization hearing",
                elements=['Consent requirements', 'TPR alternative', 'Home study', 'Finalization'],
                common_traps=['Consent requirements', 'Putative father rights', 'Revocation period'],
            ),
            KnowledgeNode(
                concept_id="family_paternity",
                name="Paternity Establishment",
                subject="family_law",
                difficulty=3,
                rule_statement="Voluntary acknowledgment or court determination; genetic testing presumptive; rebuttable presumptions; support and custody rights follow",
                elements=['Voluntary acknowledgment', 'Genetic testing', 'Presumptions', 'Rights and duties'],
                common_traps=['Presumptions of paternity', 'Genetic testing standard', 'Rights follow establishment'],
            ),
            KnowledgeNode(
                concept_id="family_presumptions_paternity",
                name="Presumptions of Paternity",
                subject="family_law",
                difficulty=3,
                rule_statement="Marital presumption: husband presumed father; holding out; genetic testing rebuts; multiple presumptions possible",
                elements=['Marital presumption', 'Holding out', 'Genetic testing', 'Rebuttal'],
                common_traps=['Marital presumption strong', 'Genetic testing rebuts', 'Multiple presumed fathers'],
            ),
            KnowledgeNode(
                concept_id="family_equitable_parent",
                name="Equitable Parent Doctrine",
                subject="family_law",
                difficulty=3,
                rule_statement="Non-biological parent may have rights/duties if: accepted parental role, bonded with child, parent consented; minority doctrine",
                elements=['Functional parent', 'Acceptance of role', 'Parent consent', 'Bonding'],
                common_traps=['Minority doctrine', 'Factors test', 'Parent consent key'],
            ),
            KnowledgeNode(
                concept_id="family_visitation",
                name="Visitation Rights",
                subject="family_law",
                difficulty=3,
                rule_statement="Non-custodial parent entitled to reasonable visitation unless detrimental; grandparent rights limited; supervised visitation possible",
                elements=['Reasonable visitation', 'Best interests', 'Grandparent limits', 'Supervised option'],
                common_traps=['Grandparent rights limited', 'Troxel case', 'Parental presumption'],
            ),
            KnowledgeNode(
                concept_id="family_relocation",
                name="Relocation with Child",
                subject="family_law",
                difficulty=4,
                rule_statement="Custodial parent seeking to relocate must: give notice, show legitimate reason; court balances factors; may modify custody",
                elements=['Notice requirement', 'Legitimate reason', 'Factor balancing', 'Burden on relocating parent'],
                common_traps=['Notice timing', 'Burden allocation', 'Factor tests vary'],
            ),
            KnowledgeNode(
                concept_id="family_domestic_violence",
                name="Domestic Violence",
                subject="family_law",
                difficulty=3,
                rule_statement="Protective orders available; ex parte emergency; full hearing; custody and support implications; violation is contempt/crime",
                elements=['Ex parte available', 'Full hearing', 'Relief available', 'Violation sanctions'],
                common_traps=['Ex parte standard lower', 'Custody preferences', 'Criminal violation'],
            ),
            KnowledgeNode(
                concept_id="family_protective_orders",
                name="Protective Orders",
                subject="family_law",
                difficulty=3,
                rule_statement="Restraining orders to prevent abuse; standards: immediate danger, abuse occurred; violations punishable; mutual orders disfavored",
                elements=['Standard for issuance', 'Relief available', 'Violation consequences', 'Mutual orders issue'],
                common_traps=['Standard of proof', 'Duration', 'Mutual orders problematic'],
            ),
            KnowledgeNode(
                concept_id="family_prenuptial_agreements",
                name="Prenuptial Agreements",
                subject="family_law",
                difficulty=4,
                rule_statement="Valid if: voluntary, fair disclosure, not unconscionable; cannot adversely affect child support; can waive spousal support",
                elements=['Voluntary execution', 'Financial disclosure', 'Conscionability', 'Cannot affect child support'],
                common_traps=['Full disclosure required', 'Cannot limit child support', 'Can waive spousal support'],
                # Mnemonic: VFC: Voluntary, Fair disclosure, Conscionable
            ),
            KnowledgeNode(
                concept_id="family_postnuptial_agreements",
                name="Postnuptial Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Agreement after marriage; same requirements as prenuptial plus consideration; scrutinized closely; increasing acceptance",
                elements=['After marriage', 'Consideration needed', 'Close scrutiny', 'Similar to prenup'],
                common_traps=['Need consideration', 'Higher scrutiny', 'Growing acceptance'],
            ),
            KnowledgeNode(
                concept_id="family_separation_agreements",
                name="Separation Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Negotiated settlement of divorce issues; merged into decree if approved; court reviews for fairness; child provisions always modifiable",
                elements=['Negotiated settlement', 'Court approval', 'Fairness review', 'Merger into decree'],
                common_traps=['Court must approve', 'Child provisions modifiable', 'Merger vs incorporation'],
            ),
            KnowledgeNode(
                concept_id="family_mediation",
                name="Mediation & ADR",
                subject="family_law",
                difficulty=2,
                rule_statement="Alternative dispute resolution; mediator facilitates; confidential; many jurisdictions require mediation attempt; custody mediation common",
                elements=['Facilitative process', 'Confidentiality', 'Mandatory in some places', 'Custody focus'],
                common_traps=['Confidentiality protections', 'No binding decision', 'Mandatory mediation'],
            ),
            KnowledgeNode(
                concept_id="family_tax_consequences",
                name="Tax Consequences of Divorce",
                subject="family_law",
                difficulty=3,
                rule_statement="Property transfers: generally tax-free; Alimony: post-2018 not deductible/taxable; Child support: not deductible/taxable; Dependency exemptions",
                elements=['Property transfer rules', 'Alimony tax treatment', 'Child support treatment', 'Exemptions'],
                common_traps=['2018 tax law changes', 'Property transfer tax-free', 'Child support never deductible'],
            ),
            KnowledgeNode(
                concept_id="family_bankruptcy",
                name="Bankruptcy & Family Law",
                subject="family_law",
                difficulty=3,
                rule_statement="Child support non-dischargeable; spousal support non-dischargeable; property division may be dischargeable; automatic stay exceptions",
                elements=['Support obligations survive', 'Property division varies', 'Stay exceptions', 'Priority debts'],
                common_traps=['Support never dischargeable', 'Property division in Ch 13', 'Stay exceptions'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_secured_transactions(self):
        """18 Secured Transactions concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="secured_types_collateral",
                name="Types of Collateral",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods: consumer, equipment, farm products, inventory; Intangibles: accounts, instruments, documents, chattel paper, investment property, deposit accounts",
                elements=['Goods categories', 'Intangibles', 'Classification determines rules', 'Use-based for goods'],
                common_traps=['Use determines goods classification', 'Dual-use situations', 'Transformation changes type'],
            ),
            KnowledgeNode(
                concept_id="secured_after_acquired",
                name="After-Acquired Property Clause",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Security interest attaches to after-acquired property if clause included; automatic for inventory and accounts; exception for consumer goods",
                elements=['Requires clause', 'Automatic inventory/accounts', 'Consumer goods limit', 'Attaches when acquired'],
                common_traps=['Consumer goods 10-day limit', 'Inventory automatic', 'Must have clause'],
            ),
            KnowledgeNode(
                concept_id="secured_proceeds",
                name="Proceeds",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Security interest continues in proceeds; automatically perfected for 20 days; must perfect afterward; identifiable proceeds required",
                elements=['Automatic security interest', '20-day perfection', 'Must perfect after', 'Identifiable standard'],
                common_traps=['20-day temporary perfection', 'Lowest intermediate balance rule', 'Cash proceeds'],
            ),
            KnowledgeNode(
                concept_id="secured_future_advances",
                name="Future Advances",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Security interest can secure future loans; priority from original perfection if within 45 days or committed",
                elements=['Secures future debts', 'Original priority', '45-day rule', 'Commitment'],
                common_traps=['Priority relates back', '45-day rule', 'Optional vs committed'],
            ),
            KnowledgeNode(
                concept_id="secured_bioc",
                name="Buyer in Ordinary Course",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="BIOC takes free of security interest in inventory even if perfected and knows; must be ordinary course; good faith; value given",
                elements=['Takes free', 'Inventory only', 'Ordinary course', 'Good faith + value'],
                common_traps=['Takes free even with knowledge', 'Inventory only', 'Ordinary course requirement'],
                # Mnemonic: BIOC: Buyer, Inventory, Ordinary, Course (takes free)
            ),
            KnowledgeNode(
                concept_id="secured_fixtures",
                name="Fixtures",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Personal property that becomes real property; fixture filing perfects; PMSI fixture has priority if: filed before or within 20 days, construction mortgage exception",
                elements=['Fixture definition', 'Fixture filing', 'PMSI priority', 'Construction mortgage'],
                common_traps=['20-day grace period', 'Construction mortgage wins', 'Fixture filing location'],
            ),
            KnowledgeNode(
                concept_id="secured_accessions",
                name="Accessions",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods installed in other goods; security interest continues; perfection required; removal right if no material harm",
                elements=['Continues in accession', 'Perfection needed', 'Priority rules', 'Removal rights'],
                common_traps=['First to file wins', 'Material harm test', 'PMSI super-priority'],
            ),
            KnowledgeNode(
                concept_id="secured_commingled",
                name="Commingled Goods",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods physically united in product; security interest continues in product; perfection continues; priority prorata by value",
                elements=['Continues in product', 'Perfection continues', 'Pro rata priority', 'Cannot separate'],
                common_traps=['Pro rata distribution', 'Cannot separate', 'Perfection continues'],
            ),
            KnowledgeNode(
                concept_id="secured_investment_property",
                name="Investment Property",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Securities, security entitlements, accounts; perfection by control or filing; control has priority over filing",
                elements=['Control perfection', 'Filing alternative', 'Control priority', 'Types included'],
                common_traps=['Control beats filing', 'Control methods', 'Securities intermediary'],
            ),
            KnowledgeNode(
                concept_id="secured_deposit_accounts",
                name="Deposit Accounts",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Can only perfect by control; control: secured party is bank, control agreement, or secured party is account holder",
                elements=['Control only', 'Three methods', 'No filing perfection', 'Priority by control'],
                common_traps=['Cannot perfect by filing', 'Control methods', 'Bank as secured party'],
            ),
            KnowledgeNode(
                concept_id="secured_lien_creditor",
                name="Lien Creditors",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Secured party vs lien creditor: perfected wins; unperfected loses unless PMSI grace period; trustee in bankruptcy is lien creditor",
                elements=['Perfected beats lien creditor', 'Unperfected loses', 'PMSI grace period', 'Bankruptcy trustee'],
                common_traps=['Trustee as lien creditor', 'PMSI grace period', 'Perfection timing critical'],
            ),
            KnowledgeNode(
                concept_id="secured_continuation",
                name="Continuation Statements",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Filing effective 5 years; continuation filed within 6 months before lapse; extends another 5 years",
                elements=['5-year duration', '6-month window', 'Extends 5 years', 'Must be timely'],
                common_traps=['6-month window', 'Lapses if not filed', 'Calculation of dates'],
            ),
            KnowledgeNode(
                concept_id="secured_termination",
                name="Termination Statements",
                subject="secured_transactions",
                difficulty=2,
                rule_statement="Secured party must file termination when debt paid; consumer goods: 1 month or 20 days if requested; other collateral: on demand",
                elements=['Must file when paid', 'Consumer timing', 'Non-consumer on demand', 'Penalties for failure'],
                common_traps=['Consumer timing strict', 'Must file termination', 'Failure penalties'],
            ),
            KnowledgeNode(
                concept_id="secured_assignments",
                name="Assignment of Security Interest",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Can assign security interest; need not file unless assignee wants priority over later assignee; notification to debtor",
                elements=['Assignability', 'Filing not required', 'Priority of assignees', 'Debtor notification'],
                common_traps=['Filing not required for perfection', 'Priority among assignees', 'Debtor payment rules'],
            ),
            KnowledgeNode(
                concept_id="secured_agricultural_liens",
                name="Agricultural Liens",
                subject="secured_transactions",
                difficulty=2,
                rule_statement="Non-consensual lien on farm products; perfection by filing; priority rules similar to Article 9; statute creates",
                elements=['Statutory lien', 'Farm products', 'Filing perfects', 'Similar priority'],
                common_traps=['Not security interest', 'Statutory basis', 'Filing required'],
            ),
            KnowledgeNode(
                concept_id="secured_bankruptcy_trustee",
                name="Bankruptcy Trustee Powers",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Trustee has strong-arm power: lien creditor status; can avoid unperfected interests; 90-day preference period for perfection",
                elements=['Lien creditor status', 'Avoid unperfected', '90-day preference', 'Filing relates back'],
                common_traps=['90-day preference', 'Grace period protection', 'Relates back if timely'],
            ),
            KnowledgeNode(
                concept_id="secured_preferences",
                name="Preferences in Bankruptcy",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Transfer within 90 days while insolvent that prefers creditor can be avoided; exceptions: contemporaneous exchange, ordinary course, PMSI grace",
                elements=['90-day lookback', 'Insolvency presumed', 'Preference elements', 'Exceptions'],
                common_traps=['90 days', 'PMSI grace period exception', 'Ordinary course exception'],
            ),
            KnowledgeNode(
                concept_id="secured_fraudulent_transfers",
                name="Fraudulent Transfers",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Transfer to hinder, delay, defraud creditors; transfer for less than reasonably equivalent value while insolvent; can be avoided",
                elements=['Actual fraud', 'Constructive fraud', 'Reasonably equivalent value', 'Insolvency'],
                common_traps=['Actual vs constructive', 'Timing', 'Badges of fraud'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_iowa_procedure(self):
        """15 Iowa Procedure concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="iowa_pleading",
                name="Iowa Pleading Requirements",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Iowa requires notice pleading similar to federal; original notice serves as complaint; must state claim upon which relief can be granted",
                elements=['Original notice', 'Notice pleading', 'State claim', 'Similar to federal'],
                common_traps=['Original notice terminology', 'Similar to FRCP', 'Specific Iowa forms'],
            ),
            KnowledgeNode(
                concept_id="iowa_service",
                name="Iowa Service of Process",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Personal service by sheriff or process server; substituted service available; service by publication with court approval",
                elements=['Personal service', 'Sheriff service', 'Substituted service', 'Publication service'],
                common_traps=['Sheriff preference', 'Publication requirements', 'Proof of service'],
            ),
            KnowledgeNode(
                concept_id="iowa_discovery",
                name="Iowa Discovery Rules",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Iowa discovery mirrors federal rules; interrogatories, depositions, requests for production, admissions; proportionality applies",
                elements=['Federal model', 'All federal tools', 'Proportionality', 'Protective orders'],
                common_traps=['Similar to federal', 'Iowa-specific limits', 'Timing differences'],
            ),
            KnowledgeNode(
                concept_id="iowa_summary_judgment",
                name="Iowa Summary Judgment",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Available if no genuine issue of material fact; moving party burden; view evidence in light favorable to non-movant",
                elements=['No genuine issue', 'Material fact', 'Moving party burden', 'Favorable view'],
                common_traps=['Standard similar to federal', 'Iowa case law', 'Timing requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_trial_procedures",
                name="Iowa Trial Procedures",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Jury trial right; voir dire conducted by judge typically; Iowa Rules of Evidence govern; jury instructions settled before trial",
                elements=['Jury right', 'Judge voir dire', 'Evidence rules', 'Jury instructions'],
                common_traps=['Judge-conducted voir dire', 'Iowa evidence rules', 'Pre-trial procedures'],
            ),
            KnowledgeNode(
                concept_id="iowa_appeals",
                name="Iowa Appellate Procedure",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Appeal to Iowa Court of Appeals or Supreme Court; notice of appeal within 30 days; record and brief requirements; standards of review",
                elements=['30-day deadline', 'Notice of appeal', 'Record requirements', 'Standards of review'],
                common_traps=['30-day deadline strict', 'Direct to Supreme Court options', 'Preservation requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_venue",
                name="Iowa Venue",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Proper venue: defendant residence, cause of action arose, property located, contract performed; transfer available",
                elements=['Defendant residence', 'Cause arose', 'Property location', 'Transfer possible'],
                common_traps=['Multiple proper venues', 'Transfer discretion', 'Convenience factors'],
            ),
            KnowledgeNode(
                concept_id="iowa_jurisdiction",
                name="Iowa Personal Jurisdiction",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Long-arm statute reaches constitutional limits; minimum contacts required; purposeful availment; fair play and substantial justice",
                elements=['Long-arm statute', 'Constitutional limits', 'Minimum contacts', 'Fairness test'],
                common_traps=['Constitutional analysis', 'Specific vs general', 'Stream of commerce'],
            ),
            KnowledgeNode(
                concept_id="iowa_joinder",
                name="Iowa Joinder Rules",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Permissive joinder of parties and claims; compulsory joinder of necessary parties; intervention and interpleader available",
                elements=['Permissive joinder', 'Necessary parties', 'Intervention', 'Interpleader'],
                common_traps=['Similar to federal', 'Iowa variations', 'Necessary vs indispensable'],
            ),
            KnowledgeNode(
                concept_id="iowa_class_actions",
                name="Iowa Class Actions",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Class actions permitted; requirements similar to federal; certification required; notice to class members",
                elements=['Certification requirements', 'Numerosity', 'Commonality', 'Notice'],
                common_traps=['Certification motion', 'Opt-out rights', 'Settlement approval'],
            ),
            KnowledgeNode(
                concept_id="iowa_injunctions",
                name="Iowa Injunctions",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Temporary and permanent injunctions available; requirements: likelihood of success, irreparable harm, balance of harms, public interest",
                elements=['Temporary injunction', 'Permanent injunction', 'Four factors', 'Bond requirement'],
                common_traps=['Four-factor test', 'Bond for temporary', 'Hearing requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_judgments",
                name="Iowa Judgments",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Default judgment available; directed verdict/JNOV motions; new trial motions; judgment liens; enforcement procedures",
                elements=['Default judgment', 'Post-trial motions', 'Judgment liens', 'Enforcement'],
                common_traps=['Motion timing', 'Lien procedures', 'Enforcement methods'],
            ),
            KnowledgeNode(
                concept_id="iowa_execution",
                name="Iowa Execution & Garnishment",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Execution on judgment; garnishment of wages and accounts; exemptions protect certain property; procedures for collection",
                elements=['Execution process', 'Garnishment', 'Exemptions', 'Debtor protections'],
                common_traps=['Iowa exemptions', 'Garnishment limits', 'Procedures'],
            ),
            KnowledgeNode(
                concept_id="iowa_sanctions",
                name="Iowa Sanctions",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Court may sanction frivolous filings, discovery abuse, contempt; attorney fees available; Rule 1.413 governs",
                elements=['Frivolous filings', 'Discovery sanctions', 'Contempt', 'Attorney fees'],
                common_traps=['Rule 1.413', 'Standards for sanctions', 'Safe harbor'],
            ),
            KnowledgeNode(
                concept_id="iowa_adr",
                name="Iowa ADR Procedures",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Mediation encouraged; arbitration enforceable; case management conferences; settlement conferences",
                elements=['Mediation', 'Arbitration', 'Case management', 'Settlement conferences'],
                common_traps=['Mandatory mediation in some cases', 'Arbitration enforcement', 'Confidentiality'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_professional_responsibility(self):
        """29 Professional Responsibility concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="prof_resp_communication_detailed",
                name="Communication with Client",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer must reasonably inform client of status, respond to requests, explain matters for informed decisions, and communicate settlement offers promptly",
                elements=['Keep informed', 'Respond to requests', 'Explain for decisions', 'Prompt settlement communication'],
                common_traps=['Not informing of settlement offers', 'Not explaining enough', 'Missing scope decisions'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_declining_terminating",
                name="Declining & Terminating Representation",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must decline if rules violation; may withdraw for legitimate reasons; court approval if litigation; protect client interests",
                elements=['Mandatory withdrawal', 'Permissive withdrawal', 'Court approval', 'Protect interests'],
                common_traps=['No court permission in litigation', 'Not giving notice', 'Not returning property'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_safekeeping_detailed",
                name="Safekeeping Property",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Separate account required; maintain records; prompt delivery; accounting on request; disputed funds kept separate",
                elements=['Separate account (IOLTA)', 'Complete records', 'Prompt delivery', 'Accounting'],
                common_traps=['Commingling', 'Using client funds temporarily', 'Not separating disputed funds'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_advertising_detailed",
                name="Advertising & Solicitation Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May advertise if truthful; no live solicitation if significant pecuniary motive; specialization limits",
                elements=['Advertising permitted if truthful', 'No false/misleading', 'Solicitation restrictions', 'Specialization rules'],
                common_traps=['All solicitation prohibited', 'In-person to accident victims', 'Claiming specialization without certification'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_impartiality_detailed",
                name="Impartiality of Tribunal",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="No ex parte with judge; no improper jury influence; maintain decorum; no prejudicial conduct",
                elements=['No ex parte with judge', 'No improper jury influence', 'Maintain decorum', 'No prejudicial conduct'],
                common_traps=['Ex parte exceptions', 'Gifts to judges', 'Lawyer-judge commentary'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_trial_publicity_detailed",
                name="Trial Publicity Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot make statements with substantial likelihood of materially prejudicing proceeding; safe harbor statements permitted",
                elements=['Substantial likelihood test', 'Material prejudice', 'Criminal heightened', 'Safe harbor'],
                common_traps=['Public record info permitted', 'Heightened in criminal', 'First Amendment balance'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_judges_detailed",
                name="Judge & Former Judge Rules",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Judge must maintain independence, avoid impropriety appearance; former judge cannot represent in matter participated",
                elements=['Independence', 'Impartiality', 'Disqualification', 'Former judge limits'],
                common_traps=['Former judge prior matter', 'Appearance of impropriety', 'Report misconduct duty'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_law_firms_detailed",
                name="Law Firm Responsibilities",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Partners/supervisors ensure compliance; subordinates follow rules; firm-wide measures required; conflicts imputed",
                elements=['Supervisory duties', 'Subordinate duties', 'Firm measures', 'Conflict imputation'],
                common_traps=['Subordinate still liable', 'Screening laterals', 'Firm name restrictions'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_unauthorized_practice",
                name="Unauthorized Practice of Law",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer cannot practice where not admitted; cannot assist non-lawyer in unauthorized practice; multijurisdictional practice rules",
                elements=['Admission requirements', 'No assisting non-lawyers', 'MJP exceptions', 'Pro hac vice'],
                common_traps=['MJP exceptions', 'Temporary practice', 'Assisting UPL'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_sale_law_practice",
                name="Sale of Law Practice",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May sell practice if: entire practice or area sold, written client notice, fees not increased",
                elements=['Entire practice or area', 'Written notice', 'No fee increase', 'Client consent'],
                common_traps=['Must sell entire area', 'Client can reject', 'Cannot increase fees'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_reporting_misconduct",
                name="Reporting Professional Misconduct",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer must report other lawyer's violations raising substantial question about honesty, trustworthiness, fitness",
                elements=['Must report violations', 'Substantial question test', 'Confidentiality exceptions', 'Self-reporting'],
                common_traps=['Confidentiality not absolute', 'Substantial question threshold', 'Judge misconduct reporting'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_disciplinary_procedures",
                name="Disciplinary Procedures",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="State supreme court inherent authority; disciplinary board investigates; sanctions range from private reprimand to disbarment",
                elements=['Supreme court authority', 'Investigation process', 'Sanctions range', 'Reciprocal discipline'],
                common_traps=['Inherent authority', 'Burden of proof', 'Reciprocal discipline rules'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_multijurisdictional",
                name="Multijurisdictional Practice",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="May practice temporarily if: related to admitted practice, arbitration/mediation, reasonably related to practice, pro hac vice",
                elements=['Temporary practice exceptions', 'Related to home practice', 'Pro hac vice', 'Systematic presence prohibited'],
                common_traps=['Cannot establish office', 'Related to home practice', 'Temporary only'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_litigation_conduct",
                name="Conduct in Litigation",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must not: abuse discovery, fail to disclose controlling authority, falsify evidence, make frivolous claims",
                elements=['No discovery abuse', 'Disclose adverse authority', 'No false evidence', 'No frivolous claims'],
                common_traps=['Adverse authority in controlling jurisdiction', 'Discovery proportionality', 'Good faith extensions OK'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_transactions_with_client",
                name="Business Transactions with Clients",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot enter business transaction unless: terms fair and reasonable, disclosed in writing, client has independent counsel opportunity, client consents in writing",
                elements=['Fair and reasonable', 'Written disclosure', 'Independent counsel opportunity', 'Written consent'],
                common_traps=['All four required', 'Full disclosure needed', 'Independent counsel chance'],
                # Mnemonic: FICO: Fair, Independent counsel, Consent, Opportunity
            ),
            KnowledgeNode(
                concept_id="prof_resp_literary_rights",
                name="Literary & Media Rights",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot acquire literary or media rights to representation before conclusion; may contract for reasonable expenses of publication after conclusion",
                elements=['No rights before conclusion', 'May contract after', 'Reasonable expenses only', 'Avoid conflict'],
                common_traps=['Timing - must wait until conclusion', 'May negotiate after', 'Conflict of interest concern'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_financial_assistance",
                name="Financial Assistance to Client",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot provide financial assistance except: advance court costs and expenses, contingent on outcome; may pay costs for indigent client",
                elements=['May advance costs', 'Repayment contingent on outcome', 'May pay for indigent', 'No personal living expenses'],
                common_traps=['Cannot advance living expenses', 'Can advance litigation costs', 'Indigent exception'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_former_government_lawyer",
                name="Former Government Lawyer",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent in matter personally and substantially participated in as government lawyer; screening can cure; cannot use confidential government information",
                elements=['Personally and substantially test', 'Screening available', 'No confidential info use', 'Negotiating employment'],
                common_traps=['Screening can cure conflict', 'Personal and substantial both required', 'Confidential info permanent bar'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_former_judge_arbitrator",
                name="Former Judge or Arbitrator",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent anyone in matter participated in as judge, arbitrator, mediator, or other neutral; screening cannot cure",
                elements=['Cannot represent in prior matter', 'Participated as neutral', 'Screening cannot cure', 'Negotiating employment restriction'],
                common_traps=['Screening does NOT cure (unlike gov lawyer)', 'Participated in any capacity', 'Negotiating employment limits'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_imputed_conflicts",
                name="Imputation of Conflicts",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Lawyer conflicts imputed to all in firm unless: personal interest, former client with screening, former government lawyer with screening",
                elements=['General imputation rule', 'Personal interest exception', 'Former client screening', 'Government lawyer screening'],
                common_traps=['Three main exceptions', 'Screening procedures', 'Timely screening required'],
                # Mnemonic: PFG: Personal, Former client, Government (exceptions to imputation)
            ),
            KnowledgeNode(
                concept_id="prof_resp_nonlawyer_assistants",
                name="Responsibilities for Nonlawyer Assistants",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer responsible for nonlawyer assistants' conduct; must ensure compliance with professional rules; cannot delegate legal judgment",
                elements=['Supervisory responsibility', 'Ensure compliance', 'Cannot delegate legal judgment', 'Ethical violations imputed'],
                common_traps=['Lawyer still responsible', 'Cannot avoid by delegation', 'Must supervise adequately'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_fee_division",
                name="Fee Division with Lawyers",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="May divide fee with another lawyer if: proportional to services or joint responsibility, client agrees in writing, total fee reasonable",
                elements=['Proportional or joint responsibility', 'Written client agreement', 'Total fee reasonable', 'No division with non-lawyer'],
                common_traps=['Proportion or responsibility both OK', 'Client must agree', 'Cannot divide with non-lawyer'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_aggregate_settlements",
                name="Aggregate Settlements",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot participate in aggregate settlement unless each client gives informed consent in writing after disclosure of all material terms",
                elements=['Each client must consent', 'Informed consent', 'Written', 'Disclosure of all terms'],
                common_traps=['Every client must agree', 'Full disclosure required', 'Cannot coerce holdouts'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_limiting_liability",
                name="Limiting Liability & Malpractice",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot prospectively limit malpractice liability unless client independently represented; may settle malpractice claim if client advised to seek independent counsel",
                elements=['No prospective limits without independent counsel', 'May settle if advised', 'Full disclosure required', 'Independent advice'],
                common_traps=['Prospective limits rare', 'Settlement requires advice', 'Independent counsel key'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_sexual_relations",
                name="Sexual Relations with Clients",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Cannot have sexual relations with client unless consensual relationship existed before attorney-client relationship",
                elements=['Prohibited unless preexisting', 'Consent not defense', 'Exploitation concern', 'Impairs judgment'],
                policy_rationales=['Prevent exploitation', 'Avoid conflicts', 'Protect judgment'],
                common_traps=['Preexisting relationship exception only', 'Consent insufficient', 'Judgment impairment'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_appearance_of_impropriety",
                name="Appearance of Impropriety",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer should avoid even appearance of impropriety; upholds confidence in legal profession; aspirational standard",
                elements=['Avoid appearance', 'Public confidence', 'Aspirational', 'Reasonable person test'],
                common_traps=['Aspirational not enforceable alone', 'Reasonable person view', 'Supplements specific rules'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_client_trust_account",
                name="Client Trust Accounts (IOLTA)",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer must maintain client funds in separate interest-bearing trust account; interest goes to state IOLTA program; strict record-keeping required; no commingling",
                elements=['Separate IOLTA account', 'Interest to bar foundation', 'Detailed records', 'No commingling', 'Prompt deposit'],
                policy_rationales=['Protect client funds', 'Fund legal services for poor', 'Prevent misappropriation'],
                common_traps=['Cannot use for operating expenses', 'Strict accounting required', 'Interest belongs to bar program not client'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_screening_procedures",
                name="Screening Procedures for Conflicts",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Timely screening can cure certain conflicts: former client matters with proper procedures, former government lawyers, former judges; requires timely implementation, written notice to affected parties, and certification of compliance",
                elements=['Timely implementation', 'Written notice to clients', 'No confidential info shared', 'Certification of compliance'],
                policy_rationales=['Allow lawyer mobility', 'Protect client confidences', 'Balance interests'],
                common_traps=['Cannot cure current client conflicts', 'Timing is critical - must be prompt', 'Documentation essential', 'Former judge screening different from former government'],
                # Mnemonic: SCREEN: Separate lawyer, Certification, Records of compliance, Ethics wall, Ensure no info shared, Notice to affected parties
            ),
            KnowledgeNode(
                concept_id="prof_resp_lawyers_as_witnesses",
                name="Lawyer as Witness Rule",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Lawyer shall not act as advocate in trial where lawyer likely to be necessary witness unless: testimony on uncontested matter, testimony on legal services and fees, or disqualification would cause substantial hardship to client",
                elements=['Advocate-witness prohibition', 'Necessary witness test', 'Three exceptions', 'Imputation rules differ'],
                policy_rationales=['Avoid jury confusion', 'Prevent credibility issues', 'Separate advocate and witness roles'],
                common_traps=['Three narrow exceptions only', 'Likely to be necessary test', 'Imputation does NOT apply unless personal interest conflict', 'Other firm lawyers can continue'],
                # Mnemonic: UFS: Uncontested, Fees/services, Substantial hardship (exceptions)
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_corporations(self):
        """27 Corporations concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="corp_promoter_liability",
                name="Promoter Liability",
                subject="corporations",
                difficulty=3,
                rule_statement="Promoter liable on pre-incorporation contracts unless novation; corporation liable if adopts contract expressly or impliedly",
                elements=['Promoter personally liable', 'Corporation liable if adopts', 'Novation releases promoter', 'Implied adoption'],
                common_traps=['Both can be liable', "Adoption doesn't release", 'Need novation for release'],
            ),
            KnowledgeNode(
                concept_id="corp_defective_incorporation",
                name="Defective Incorporation",
                subject="corporations",
                difficulty=3,
                rule_statement="De facto corporation: good faith attempt, actual use; corporation by estoppel: held out as corporation, third party dealt as such",
                elements=['De facto corporation', 'Corporation by estoppel', 'Good faith attempt', 'Actual use'],
                common_traps=['Both doctrines exist', 'Protects from personal liability', 'Narrow application'],
            ),
            KnowledgeNode(
                concept_id="corp_ultra_vires",
                name="Ultra Vires Acts",
                subject="corporations",
                difficulty=2,
                rule_statement="Acts beyond corporate powers; generally enforceable but shareholders can enjoin, corporation can sue officers, state can dissolve",
                elements=['Beyond stated purpose', 'Generally enforceable', 'Limited remedies', 'Rare doctrine'],
                common_traps=['Contract still enforceable', 'Internal remedy', 'Rarely succeeds'],
            ),
            KnowledgeNode(
                concept_id="corp_subscriptions",
                name="Stock Subscriptions",
                subject="corporations",
                difficulty=3,
                rule_statement="Pre-incorporation subscription irrevocable for six months unless otherwise provided; post-incorporation governed by contract law",
                elements=['Pre-incorporation irrevocable', 'Six month rule', 'Post-incorporation contract', 'Payment terms'],
                common_traps=['Pre vs post timing', 'Irrevocability period', 'Contract law post-incorporation'],
            ),
            KnowledgeNode(
                concept_id="corp_consideration_shares",
                name="Consideration for Shares",
                subject="corporations",
                difficulty=3,
                rule_statement="Par value: must receive at least par; no-par: any consideration; watered stock: directors liable; good faith business judgment protects valuation",
                elements=['Par value minimum', 'No-par flexibility', 'Watered stock liability', 'Business judgment valuation'],
                common_traps=['Par vs no-par', 'Director liability watered stock', 'BJR protects valuation'],
            ),
            KnowledgeNode(
                concept_id="corp_preemptive_rights",
                name="Preemptive Rights",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders may have right to purchase new shares to maintain proportional ownership; must be expressly granted in modern law",
                elements=['Maintain proportional ownership', 'Must be in articles', 'Pro rata purchase right', 'Exceptions exist'],
                common_traps=['Must be expressly granted', 'Not automatic', 'Exceptions for compensation'],
            ),
            KnowledgeNode(
                concept_id="corp_distributions_dividends",
                name="Distributions & Dividends",
                subject="corporations",
                difficulty=3,
                rule_statement="Directors declare dividends using business judgment; unlawful if: insolvent, would cause insolvency, or exceeds statutory limits",
                elements=['Board discretion', 'Insolvency test', 'Statutory limits', 'Director liability'],
                common_traps=['Directors discretion wide', 'Insolvency prohibition', 'Directors personally liable'],
            ),
            KnowledgeNode(
                concept_id="corp_inspection_rights",
                name="Shareholder Inspection Rights",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders have right to inspect books and records for proper purpose; shareholder list more readily available than detailed financial records",
                elements=['Proper purpose required', 'Shareholder list easier', 'Books and records harder', 'Advance notice'],
                common_traps=['Proper purpose test', 'Different standards for different records', 'Timing requirements'],
            ),
            KnowledgeNode(
                concept_id="corp_meetings_notice",
                name="Meetings & Notice Requirements",
                subject="corporations",
                difficulty=2,
                rule_statement="Annual shareholders meeting required; notice required with time, place, purpose if special; directors can act without meeting if unanimous written consent",
                elements=['Annual meeting required', 'Notice requirements', 'Special meeting purpose', 'Written consent alternative'],
                common_traps=['Notice timing', 'Special meeting purpose specificity', 'Unanimous consent option'],
            ),
            KnowledgeNode(
                concept_id="corp_quorum_voting",
                name="Quorum & Voting Rules",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders: majority of shares is quorum, majority of votes present wins; Directors: majority of directors is quorum, majority of votes present wins",
                elements=['Shareholder quorum', 'Director quorum', 'Vote requirements', 'Can modify in articles/bylaws'],
                common_traps=['Quorum vs voting', 'Can change by agreement', 'Present vs outstanding'],
            ),
            KnowledgeNode(
                concept_id="corp_removal_directors",
                name="Removal of Directors",
                subject="corporations",
                difficulty=3,
                rule_statement="Shareholders may remove with or without cause unless articles require cause; if cumulative voting, can remove only if votes sufficient to elect",
                elements=['Shareholder removal power', 'With or without cause', 'Cumulative voting protection', 'Articles can require cause'],
                common_traps=['Unless articles require cause', 'Cumulative voting protection', 'Only shareholders remove'],
            ),
            KnowledgeNode(
                concept_id="corp_indemnification",
                name="Indemnification of Directors/Officers",
                subject="corporations",
                difficulty=4,
                rule_statement="Mandatory if successful on merits; permissive if good faith and reasonable belief; prohibited if found liable to corporation",
                elements=['Mandatory if successful', 'Permissive if good faith', 'Prohibited if liable', 'Advancement of expenses'],
                common_traps=['Three categories', 'Successful = mandatory', 'Liable to corp = prohibited'],
                # Mnemonic: MAP: Mandatory, Allowed, Prohibited
            ),
            KnowledgeNode(
                concept_id="corp_close_corporations",
                name="Close Corporations",
                subject="corporations",
                difficulty=3,
                rule_statement="Few shareholders, no public market, restrictions on transfer; may operate informally; special statutory provisions protect minority",
                elements=['Few shareholders', 'Transfer restrictions', 'Informal operation allowed', 'Minority protection'],
                common_traps=['Can dispense with formalities', 'Oppression remedies', 'Statutory protections'],
            ),
            KnowledgeNode(
                concept_id="corp_shareholder_agreements",
                name="Shareholder Agreements",
                subject="corporations",
                difficulty=3,
                rule_statement="May restrict transfers, provide for management, require arbitration; must not treat corporation as partnership or injure creditors",
                elements=['Voting agreements', 'Buy-sell provisions', 'Transfer restrictions', 'Management agreements'],
                common_traps=['Cannot sterilize board', 'Must protect creditors', 'Binding on parties only'],
            ),
            KnowledgeNode(
                concept_id="corp_oppression_freeze_out",
                name="Oppression & Freeze-Out",
                subject="corporations",
                difficulty=4,
                rule_statement="Majority cannot squeeze out minority unfairly; remedies include buyout, dissolution, or damages; courts balance reasonable expectations",
                elements=['Oppressive conduct', 'Reasonable expectations', 'Buyout remedy', 'Dissolution alternative'],
                policy_rationales=['Protect minority', 'Prevent abuse of control', 'Balance interests'],
                common_traps=['Reasonable expectations test', 'Equitable remedies', 'Close corporation context'],
            ),
            KnowledgeNode(
                concept_id="corp_dividends_preferred",
                name="Preferred Stock Dividends",
                subject="corporations",
                difficulty=3,
                rule_statement="Preferred entitled to fixed dividend before common; cumulative unless stated non-cumulative; participating if so stated",
                elements=['Priority over common', 'Cumulative presumption', 'Participating possibility', 'Liquidation preference'],
                common_traps=['Cumulative unless stated otherwise', 'Arrears must be paid first', 'Participating rare'],
            ),
            KnowledgeNode(
                concept_id="corp_redemption_repurchase",
                name="Redemption & Share Repurchase",
                subject="corporations",
                difficulty=3,
                rule_statement="Corporation may repurchase shares if: not insolvent, adequate surplus; redemption rights if stated; insider trading concerns",
                elements=['Must have surplus', 'Insolvency test', 'Redemption vs repurchase', 'Insider trading risk'],
                common_traps=['Statutory requirements', 'Cannot make insolvent', 'Insider trading prohibition'],
            ),
            KnowledgeNode(
                concept_id="corp_sale_of_assets",
                name="Sale of Substantially All Assets",
                subject="corporations",
                difficulty=4,
                rule_statement="Requires board and shareholder approval; not ordinary course of business; selling corporation continues to exist; buyers can assume liabilities",
                elements=['Substantially all assets', 'Board and shareholder vote', 'Continues to exist', 'Successor liability rules'],
                common_traps=['Substantially all test', 'Continues to exist', 'Not automatic successor liability'],
            ),
            KnowledgeNode(
                concept_id="corp_tender_offers",
                name="Tender Offers",
                subject="corporations",
                difficulty=3,
                rule_statement="Offer to buy shares directly from shareholders; federal regulation; target board may defend; business judgment rule applies to defensive measures",
                elements=['Direct to shareholders', 'Federal securities law', 'Board defensive tactics', 'BJR applies'],
                common_traps=['Bypass board', 'Defensive measures reviewed', 'Unocal standard may apply'],
            ),
            KnowledgeNode(
                concept_id="corp_proxy_fights",
                name="Proxy Contests",
                subject="corporations",
                difficulty=3,
                rule_statement="Contest for board control via shareholder votes; federal proxy rules; corporation may reimburse incumbents; insurgents reimbursed if successful",
                elements=['Board control contest', 'Proxy solicitation rules', 'Reimbursement rules', 'Disclosure requirements'],
                common_traps=['Corporation can reimburse incumbents', 'Insurgents if successful', 'Federal regulation applies'],
            ),
            KnowledgeNode(
                concept_id="corp_hostile_takeovers",
                name="Hostile Takeovers & Defensive Tactics",
                subject="corporations",
                difficulty=4,
                rule_statement="Target board may defend using business judgment; must show reasonable threat and proportionate response; cannot be entrenching",
                elements=['Unocal standard', 'Reasonable threat', 'Proportionate response', 'Enhanced scrutiny'],
                common_traps=['Enhanced scrutiny', 'Cannot be entrenching', 'Proportionality key'],
                # Mnemonic: PRE: Proportionate, Reasonable threat, Enhanced scrutiny
            ),
            KnowledgeNode(
                concept_id="corp_appraisal_rights",
                name="Appraisal Rights",
                subject="corporations",
                difficulty=4,
                rule_statement="Dissenting shareholders entitled to fair value of shares in: mergers, sales of assets, amendments materially affecting rights",
                elements=['Fair value determination', 'Dissent and notice required', 'Exclusive remedy', 'Triggering events'],
                common_traps=['Must follow procedures exactly', 'Fair value not market value', 'Exclusive remedy if available'],
            ),
            KnowledgeNode(
                concept_id="corp_amendments_articles",
                name="Amending Articles of Incorporation",
                subject="corporations",
                difficulty=2,
                rule_statement="Requires board approval and shareholder vote; certain amendments require class vote if materially affect class",
                elements=['Board approval', 'Shareholder vote', 'Class voting rights', 'Filing required'],
                common_traps=['Class vote for material changes to class', 'Filing makes effective', 'Broad board power'],
            ),
            KnowledgeNode(
                concept_id="corp_bylaws",
                name="Bylaws",
                subject="corporations",
                difficulty=2,
                rule_statement="Internal operating rules; typically adopted/amended by board unless articles reserve to shareholders; cannot conflict with articles or statutes",
                elements=['Internal rules', 'Board typically amends', 'Cannot conflict with articles', 'Operating procedures'],
                common_traps=['Board power unless reserved', 'Hierarchy: statute > articles > bylaws', 'Cannot expand powers'],
            ),
            KnowledgeNode(
                concept_id="corp_limited_liability_company",
                name="Limited Liability Companies (LLC)",
                subject="corporations",
                difficulty=3,
                rule_statement="Hybrid entity: corporate limited liability plus partnership flexibility; operating agreement governs; default rules vary by state",
                elements=['Limited liability', 'Pass-through taxation', 'Operating agreement', 'Flexible management'],
                common_traps=['Operating agreement controls', 'Default rules vary', 'Veil piercing still possible'],
            ),
            KnowledgeNode(
                concept_id="corp_partnerships_general",
                name="General Partnerships",
                subject="corporations",
                difficulty=3,
                rule_statement="Formation by agreement or co-ownership for profit; each partner agent; jointly and severally liable; equal sharing unless agreed",
                elements=['No formalities', 'Each partner agent', 'Unlimited liability', 'Equal sharing default'],
                common_traps=['Joint and several liability', 'Each partner can bind', 'No filing required'],
            ),
            KnowledgeNode(
                concept_id="corp_limited_partnerships",
                name="Limited Partnerships",
                subject="corporations",
                difficulty=3,
                rule_statement="General partners manage and liable; limited partners passive investors with liability limited to investment; filing required",
                elements=['GP manages and liable', 'LP limited liability', 'Filing required', 'LP cannot control'],
                common_traps=['LP control destroys limited liability', 'Must file certificate', 'GP fully liable'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_wills_trusts_estates(self):
        """37 Wills Trusts Estates concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="wills_capacity",
                name="Testamentary Capacity",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Testator must be 18+, understand nature of act, extent of property, natural objects of bounty, plan of disposition",
                elements=['Age 18+', 'Understand nature', 'Know property', 'Natural objects', 'Dispositional plan'],
                common_traps=['Lower standard than contractual', 'Lucid intervals count', 'Burden on contestants'],
                # Mnemonic: PENDO: Property, Estate, Nature, Disposition, Objects
            ),
            KnowledgeNode(
                concept_id="wills_attestation",
                name="Attestation & Witnesses",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Two witnesses must attest; must be present at same time; interested witness issues; purging statutes may apply",
                elements=['Two witnesses', 'Simultaneous presence', 'Sign in testator presence', 'Competent witnesses'],
                common_traps=['Line of sight test', 'Interested witness loses bequest', 'Purging statutes'],
            ),
            KnowledgeNode(
                concept_id="wills_codicil",
                name="Codicils",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Testamentary instrument that modifies will; must meet same formalities; republishes will as of codicil date",
                elements=['Modifies existing will', 'Same formalities required', 'Republication effect', 'Integration'],
                common_traps=['Republication doctrine', 'Cures defects in will', 'Must meet formalities'],
            ),
            KnowledgeNode(
                concept_id="wills_incorporation_reference",
                name="Incorporation by Reference",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="External document incorporated if: exists when will executed, will manifests intent, will describes sufficiently",
                elements=['Document must exist', 'Intent to incorporate', 'Sufficient description', 'Extrinsic evidence'],
                common_traps=['Must exist at execution', 'Cannot incorporate future documents', 'Description requirement'],
            ),
            KnowledgeNode(
                concept_id="wills_acts_of_independent_significance",
                name="Acts of Independent Significance",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Will can refer to acts/events with significance apart from testamentary effect; non-testamentary motive required",
                elements=['Independent significance', 'Non-testamentary purpose', 'Changes effective', 'Common examples'],
                common_traps=['Must have independent purpose', 'Contents of wallet example', 'Beneficiary designation'],
            ),
            KnowledgeNode(
                concept_id="wills_holographic",
                name="Holographic Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Handwritten, signed, material provisions in testator handwriting; no witnesses required in states recognizing",
                elements=['Handwritten', 'Signed', 'Material provisions', 'No witnesses'],
                common_traps=['Not all states recognize', 'Material portions test', 'Intent to be will'],
            ),
            KnowledgeNode(
                concept_id="wills_conditional",
                name="Conditional Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Will effective only if condition occurs; distinguishing condition of execution from condition of revocation",
                elements=['Condition must occur', 'Condition vs motive', 'Extrinsic evidence', 'Interpretation issues'],
                common_traps=['Condition vs motive', 'Presumption against conditional', 'Proof required'],
            ),
            KnowledgeNode(
                concept_id="wills_revocation_dependent_relative",
                name="Dependent Relative Revocation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revocation ineffective if based on mistake of law/fact and would not have revoked but for mistake",
                elements=['Mistaken revocation', 'Would not have revoked', 'Testator intent', 'Second-best result'],
                common_traps=['Applies when mistake', 'Second best over intestacy', 'Intent focus'],
            ),
            KnowledgeNode(
                concept_id="wills_revival",
                name="Revival of Revoked Wills",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="When revoking instrument revoked, three approaches: automatic revival, testator intent, no revival absent re-execution",
                elements=['Revocation of revocation', 'Majority: intent controls', 'Minority: automatic', 'Minority: re-execution'],
                common_traps=['State law varies', 'Intent evidence', 'May need re-execution'],
            ),
            KnowledgeNode(
                concept_id="wills_lapse_anti_lapse",
                name="Lapse & Anti-Lapse",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Bequest lapses if beneficiary predeceases; anti-lapse saves gift if beneficiary in protected class and leaves issue",
                elements=['Lapse when predecease', 'Anti-lapse statute', 'Protected class', 'Issue substitute'],
                common_traps=['Protected class varies', 'Issue requirement', 'Express contrary intent'],
                # Mnemonic: ACID: Anti-lapse, Class, Issue, Descendants
            ),
            KnowledgeNode(
                concept_id="wills_ademption",
                name="Ademption by Extinction",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Specific gift adeemed if not in estate at death; identity theory vs intent theory",
                elements=['Specific gift only', 'Not in estate', 'Identity theory', 'Intent theory minority'],
                common_traps=['Specific vs general/demonstrative', 'Exceptions may apply', 'Insurance proceeds'],
            ),
            KnowledgeNode(
                concept_id="wills_ademption_satisfaction",
                name="Ademption by Satisfaction",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Lifetime gift to beneficiary may satisfy testamentary gift if: writing by testator, writing by beneficiary, or property declares satisfaction",
                elements=['Lifetime gift', 'Testamentary gift', 'Writing requirement', 'Intent to satisfy'],
                common_traps=['Need writing', 'Presumption against', 'Value determination'],
            ),
            KnowledgeNode(
                concept_id="wills_abatement",
                name="Abatement",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Reduce gifts when assets insufficient; order: intestate property, residuary, general, demonstrative, specific",
                elements=['Insufficient assets', 'Priority order', 'Pro rata within class', 'Can change by will'],
                common_traps=['Standard order', 'Pro rata reduction', 'Will can change'],
                # Mnemonic: IRGDS: Intestate, Residuary, General, Demonstrative, Specific (reverse priority)
            ),
            KnowledgeNode(
                concept_id="wills_exoneration",
                name="Exoneration of Liens",
                subject="wills_trusts_estates",
                difficulty=2,
                rule_statement="Traditional: estate pays off liens; Modern UPC: beneficiary takes subject to liens unless will directs payment",
                elements=['Liens on specific gifts', 'Traditional: estate pays', 'UPC: beneficiary takes with', 'Will can direct'],
                common_traps=['UPC changed rule', 'Specific direction needed', 'Mortgage example'],
            ),
            KnowledgeNode(
                concept_id="wills_pretermitted_spouse",
                name="Pretermitted Spouse",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Spouse married after will takes intestate share unless: will contemplates marriage, provided for outside will, intentionally omitted",
                elements=['After-will marriage', 'Intestate share', 'Three exceptions', 'Intent evidence'],
                common_traps=['Exceptions apply', 'Burden of proof', 'Not divorce'],
            ),
            KnowledgeNode(
                concept_id="wills_pretermitted_children",
                name="Pretermitted Children",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Child born/adopted after will takes share unless: intentional omission shown, provided for outside will, or all to other parent",
                elements=['After-will child', 'Share calculation', 'Three exceptions', 'All estate to parent exception'],
                common_traps=['Share calculation complex', 'All-to-parent exception', 'Adopted children included'],
            ),
            KnowledgeNode(
                concept_id="wills_elective_share",
                name="Elective Share",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Surviving spouse can elect statutory share (typically 1/3 or 1/2) instead of will provision; time limit applies",
                elements=['Statutory percentage', 'Augmented estate', 'Time to elect', 'Cannot waive before marriage'],
                common_traps=['Augmented estate includes transfers', 'Time limit strict', 'Prenup can waive'],
            ),
            KnowledgeNode(
                concept_id="wills_undue_influence",
                name="Undue Influence",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Substituted will of influencer for testator; requires: susceptibility, opportunity, disposition to influence, unnatural result",
                elements=['Susceptibility', 'Opportunity', 'Active procurement', 'Unnatural result'],
                common_traps=['Four elements', 'Burden on contestant', 'Presumption if confidential relation + benefit'],
            ),
            KnowledgeNode(
                concept_id="wills_fraud",
                name="Fraud",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="False statement material to testamentary disposition; fraud in execution vs inducement; constructive trust remedy",
                elements=['False representation', 'Known false', 'Testator reliance', 'Material'],
                common_traps=['Fraud in execution vs inducement', 'Constructive trust remedy', 'High burden'],
            ),
            KnowledgeNode(
                concept_id="wills_mistake",
                name="Mistake",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Mistake in execution may void; mistake in inducement generally not correctable; reformation limited",
                elements=['Mistake in execution', 'Mistake in inducement', 'Limited correction', 'Omitted text'],
                common_traps=['In execution voids', 'In inducement usually no remedy', 'Rare reformation'],
            ),
            KnowledgeNode(
                concept_id="wills_joint_mutual",
                name="Joint & Mutual Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Joint: one document for multiple testators; Mutual: reciprocal provisions; contract not to revoke requires clear evidence",
                elements=['Joint will', 'Mutual wills', 'Contract not to revoke', 'Proof required'],
                common_traps=['Presumption against contract', 'Must prove agreement', 'Remedy: constructive trust'],
            ),
            KnowledgeNode(
                concept_id="trusts_inter_vivos",
                name="Inter Vivos Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Created during settlor lifetime; requires delivery; can be revocable or irrevocable; avoids probate",
                elements=['Lifetime creation', 'Delivery required', 'Revocability', 'Probate avoidance'],
                common_traps=['Delivery requirement', 'Revocable unless stated', 'Pour-over wills'],
            ),
            KnowledgeNode(
                concept_id="trusts_testamentary",
                name="Testamentary Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Created by will; effective at death; must meet will formalities; subject to probate",
                elements=['Created by will', 'Will formalities', 'Effective at death', 'Probate required'],
                common_traps=['Will formalities apply', 'Goes through probate', 'Court supervision'],
            ),
            KnowledgeNode(
                concept_id="trusts_spendthrift",
                name="Spendthrift Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Beneficiary cannot transfer interest; creditors cannot reach; exceptions: certain creditors, excess beyond support",
                elements=['Transfer restraint', 'Creditor protection', 'Express provision needed', 'Exceptions exist'],
                common_traps=['Must be express', 'Exception creditors', 'Self-settled issues'],
            ),
            KnowledgeNode(
                concept_id="trusts_discretionary",
                name="Discretionary Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Trustee has discretion over distributions; standard may be absolute or limited; creditor protection",
                elements=['Trustee discretion', 'Absolute vs limited', 'Judicial review limited', 'Creditor protection'],
                common_traps=['Abuse of discretion standard', 'Good faith required', 'Creditor protection strong'],
            ),
            KnowledgeNode(
                concept_id="trusts_support",
                name="Support Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Trustee must distribute for support; mandatory if within standard; creditors providing necessaries can reach",
                elements=['Mandatory distributions', 'Support standard', 'Necessaries creditors', 'Interpretation'],
                common_traps=['Mandatory nature', 'Necessaries exception', 'Standard interpretation'],
            ),
            KnowledgeNode(
                concept_id="trusts_resulting",
                name="Resulting Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Arises by operation of law when: purchase money resulting trust, excess corpus, failure of express trust",
                elements=['Implied by law', 'Settlor gets back', 'Purchase money', 'Failure scenarios'],
                common_traps=['Returns to settlor', 'Operation of law', 'Limited situations'],
            ),
            KnowledgeNode(
                concept_id="trusts_constructive",
                name="Constructive Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Equitable remedy for unjust enrichment; wrongdoer holds property for rightful owner; fraud, breach of duty",
                elements=['Equitable remedy', 'Unjust enrichment', 'Wrongful conduct', 'Rightful owner recovers'],
                common_traps=['Remedy not true trust', 'Flexible application', 'Prevents unjust enrichment'],
            ),
            KnowledgeNode(
                concept_id="trusts_modification",
                name="Trust Modification & Termination",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revocable: settlor can modify/terminate; Irrevocable: need consent or changed circumstances; Claflin doctrine applies",
                elements=['Revocable settlor control', 'Irrevocable restrictions', 'Claflin doctrine', 'Changed circumstances'],
                common_traps=['Material purpose test', 'Consent requirements', 'Court modification limited'],
            ),
            KnowledgeNode(
                concept_id="trusts_powers",
                name="Trustee Powers",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Express powers in instrument; implied powers necessary to accomplish purpose; statutory default powers",
                elements=['Express powers', 'Implied powers', 'Statutory powers', 'Limits on powers'],
                common_traps=['Broadly construed', 'Statutory defaults', 'Cannot violate duty'],
            ),
            KnowledgeNode(
                concept_id="trusts_duty_inform",
                name="Duty to Inform & Account",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Must keep beneficiaries informed; provide annual accounting; respond to requests; disclosure of material facts",
                elements=['Keep informed', 'Annual accounting', 'Respond to requests', 'Material facts'],
                common_traps=['Affirmative duty', 'Reasonable information', 'Cannot hide behind instrument'],
            ),
            KnowledgeNode(
                concept_id="trusts_principal_income",
                name="Principal & Income Allocation",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Distinguish principal from income; Uniform Principal & Income Act provides rules; trustee adjusting power",
                elements=['Principal vs income', 'UPAIA rules', 'Adjusting power', 'Life tenant/remainder split'],
                common_traps=['UPAIA default rules', 'Power to adjust', 'Impartiality duty'],
            ),
            KnowledgeNode(
                concept_id="trusts_breach_remedies",
                name="Breach of Trust & Remedies",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Trustee liable for breach; remedies: damages, remove trustee, constructive trust, tracing; defenses: consent, exculpation clause",
                elements=['Liability for breach', 'Multiple remedies', 'Defenses available', 'Statute of limitations'],
                common_traps=['Multiple remedies possible', 'Exculpation limits', 'Consent defense'],
            ),
            KnowledgeNode(
                concept_id="rule_against_perpetuities",
                name="Rule Against Perpetuities",
                subject="wills_trusts_estates",
                difficulty=5,
                rule_statement="Interest must vest or fail within life in being plus 21 years; applies to contingent remainders, executory interests; reform statutes exist",
                elements=['Measuring lives', '21 year period', 'Must vest or fail', 'Contingent interests'],
                common_traps=['Contingent interests only', 'Reform statutes', 'Wait and see', 'Cy pres'],
                # Mnemonic: RAP applies to: contingent remainders, executory interests, class gifts, options, rights of first refusal
            ),
            KnowledgeNode(
                concept_id="powers_of_appointment",
                name="Powers of Appointment",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="General: appointee can appoint to self, estate, creditors; Special: limited class; affects estate taxation and creditors",
                elements=['General power', 'Special power', 'Exercise methods', 'Tax consequences'],
                common_traps=['General vs special', 'Default appointments', 'Tax implications'],
            ),
            KnowledgeNode(
                concept_id="estate_administration",
                name="Estate Administration Process",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Probate process: petition, notice, inventory, pay debts, distribute; executor/administrator duties; court supervision",
                elements=['Petition for probate', 'Notice to heirs', 'Inventory and appraisal', 'Pay debts then distribute'],
                common_traps=['Priority of payments', 'Creditor claims period', 'Accounting requirements'],
            ),
            KnowledgeNode(
                concept_id="nonprobate_transfers",
                name="Non-Probate Transfers",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Avoid probate: joint tenancy, POD/TOD accounts, life insurance, trusts; creditor rights may still apply",
                elements=['Joint tenancy', 'POD/TOD', 'Life insurance', 'Trust assets'],
                common_traps=['Avoid probate but not taxes', 'Creditor rights', "Will provisions don't control"],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_family_law(self):
        """25 Family Law concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="family_annulment",
                name="Annulment",
                subject="family_law",
                difficulty=3,
                rule_statement="Void marriage: bigamy, incest, mental incapacity; Voidable: age, impotence, fraud, duress, lack of consent",
                elements=['Void ab initio', 'Voidable until annulled', 'Grounds vary', 'Retroactive effect'],
                common_traps=['Void vs voidable', 'Retroactive effect', 'Property rights may survive'],
            ),
            KnowledgeNode(
                concept_id="family_separation",
                name="Legal Separation",
                subject="family_law",
                difficulty=2,
                rule_statement="Court-approved living apart; addresses support, property, custody; marriage continues; bars filed by separated spouse",
                elements=['Marriage continues', 'Court order', 'Same issues as divorce', 'Can convert to divorce'],
                common_traps=['Not divorce', 'Marriage continues', 'Same relief available'],
            ),
            KnowledgeNode(
                concept_id="family_jurisdiction",
                name="Divorce Jurisdiction",
                subject="family_law",
                difficulty=3,
                rule_statement="Divorce: domicile of one spouse; Property: in personam jurisdiction; Custody: UCCJEA home state",
                elements=['Domicile for divorce', 'Personal jurisdiction for property', 'UCCJEA for custody', 'Residency requirements'],
                common_traps=['Different jurisdiction rules', 'Divisible divorce', 'UCCJEA controls custody'],
            ),
            KnowledgeNode(
                concept_id="family_uccjea",
                name="UCCJEA Jurisdiction",
                subject="family_law",
                difficulty=4,
                rule_statement="Home state priority: where child lived 6 months before filing; significant connection if no home state; emergency jurisdiction limited",
                elements=['Home state priority', 'Significant connection', 'Emergency jurisdiction', 'Exclusive continuing jurisdiction'],
                common_traps=['Home state 6 months', 'Continuing jurisdiction', 'Emergency temporary only'],
                # Mnemonic: HSCE: Home state, Significant connection, Continuing, Emergency
            ),
            KnowledgeNode(
                concept_id="family_uifsa",
                name="UIFSA Support Enforcement",
                subject="family_law",
                difficulty=3,
                rule_statement="Uniform Interstate Family Support Act; continuing exclusive jurisdiction; direct interstate enforcement; one-order system",
                elements=['Issuing state keeps jurisdiction', 'Direct enforcement', 'No duplicate orders', 'Long-arm jurisdiction'],
                common_traps=['Continuing exclusive', 'Cannot modify elsewhere', 'Long-arm provisions'],
            ),
            KnowledgeNode(
                concept_id="family_modification_support",
                name="Modification of Support",
                subject="family_law",
                difficulty=4,
                rule_statement="Material change in circumstances required; cannot modify retroactively; voluntary unemployment may not count; burden on moving party",
                elements=['Material change', 'Prospective only', 'Substantial change', 'Voluntary acts'],
                common_traps=['Cannot modify past', 'Material change required', 'Voluntary unemployment'],
            ),
            KnowledgeNode(
                concept_id="family_modification_custody",
                name="Modification of Custody",
                subject="family_law",
                difficulty=4,
                rule_statement="Substantial change in circumstances; best interests of child; may require changed circumstances plus detrimental; restrictions on relitigation",
                elements=['Substantial change', 'Best interests', 'May need detriment', 'Time limitations'],
                common_traps=['Higher standard than initial', 'Detriment in some states', 'Relitigation restrictions'],
            ),
            KnowledgeNode(
                concept_id="family_enforcement",
                name="Support Enforcement",
                subject="family_law",
                difficulty=3,
                rule_statement="Contempt: civil or criminal; wage garnishment; license suspension; passport denial; federal locate services",
                elements=['Contempt sanctions', 'Wage withholding', 'License suspension', 'Federal enforcement'],
                common_traps=['Civil vs criminal contempt', 'Automatic withholding', 'Cannot discharge in bankruptcy'],
            ),
            KnowledgeNode(
                concept_id="family_contempt",
                name="Contempt Proceedings",
                subject="family_law",
                difficulty=3,
                rule_statement="Civil: coercive, must have ability to comply; Criminal: punitive, beyond reasonable doubt; inability to pay is defense",
                elements=['Civil coercive', 'Criminal punitive', 'Ability to pay', 'Purge conditions'],
                common_traps=['Civil vs criminal', 'Ability to pay defense', 'Burden of proof differs'],
            ),
            KnowledgeNode(
                concept_id="family_child_abuse",
                name="Child Abuse & Neglect",
                subject="family_law",
                difficulty=3,
                rule_statement="State intervention to protect child; removal requires hearing; reasonable efforts to reunify; termination of parental rights possible",
                elements=['Emergency removal', 'Court hearing', 'Reasonable efforts', 'TPR option'],
                common_traps=['Due process protections', 'Reasonable efforts', 'Clear and convincing for TPR'],
            ),
            KnowledgeNode(
                concept_id="family_termination_parental_rights",
                name="Termination of Parental Rights",
                subject="family_law",
                difficulty=4,
                rule_statement="Severs legal parent-child relationship; grounds: abuse, neglect, abandonment, unfitness; clear and convincing evidence; permanent",
                elements=['Statutory grounds', 'Clear and convincing', 'Permanent severance', 'Best interests'],
                common_traps=['High burden', 'Permanent', 'Best interests focus'],
            ),
            KnowledgeNode(
                concept_id="family_adoption",
                name="Adoption",
                subject="family_law",
                difficulty=3,
                rule_statement="Creates legal parent-child relationship; consent required from biological parents unless rights terminated; home study; finalization hearing",
                elements=['Consent requirements', 'TPR alternative', 'Home study', 'Finalization'],
                common_traps=['Consent requirements', 'Putative father rights', 'Revocation period'],
            ),
            KnowledgeNode(
                concept_id="family_paternity",
                name="Paternity Establishment",
                subject="family_law",
                difficulty=3,
                rule_statement="Voluntary acknowledgment or court determination; genetic testing presumptive; rebuttable presumptions; support and custody rights follow",
                elements=['Voluntary acknowledgment', 'Genetic testing', 'Presumptions', 'Rights and duties'],
                common_traps=['Presumptions of paternity', 'Genetic testing standard', 'Rights follow establishment'],
            ),
            KnowledgeNode(
                concept_id="family_presumptions_paternity",
                name="Presumptions of Paternity",
                subject="family_law",
                difficulty=3,
                rule_statement="Marital presumption: husband presumed father; holding out; genetic testing rebuts; multiple presumptions possible",
                elements=['Marital presumption', 'Holding out', 'Genetic testing', 'Rebuttal'],
                common_traps=['Marital presumption strong', 'Genetic testing rebuts', 'Multiple presumed fathers'],
            ),
            KnowledgeNode(
                concept_id="family_equitable_parent",
                name="Equitable Parent Doctrine",
                subject="family_law",
                difficulty=3,
                rule_statement="Non-biological parent may have rights/duties if: accepted parental role, bonded with child, parent consented; minority doctrine",
                elements=['Functional parent', 'Acceptance of role', 'Parent consent', 'Bonding'],
                common_traps=['Minority doctrine', 'Factors test', 'Parent consent key'],
            ),
            KnowledgeNode(
                concept_id="family_visitation",
                name="Visitation Rights",
                subject="family_law",
                difficulty=3,
                rule_statement="Non-custodial parent entitled to reasonable visitation unless detrimental; grandparent rights limited; supervised visitation possible",
                elements=['Reasonable visitation', 'Best interests', 'Grandparent limits', 'Supervised option'],
                common_traps=['Grandparent rights limited', 'Troxel case', 'Parental presumption'],
            ),
            KnowledgeNode(
                concept_id="family_relocation",
                name="Relocation with Child",
                subject="family_law",
                difficulty=4,
                rule_statement="Custodial parent seeking to relocate must: give notice, show legitimate reason; court balances factors; may modify custody",
                elements=['Notice requirement', 'Legitimate reason', 'Factor balancing', 'Burden on relocating parent'],
                common_traps=['Notice timing', 'Burden allocation', 'Factor tests vary'],
            ),
            KnowledgeNode(
                concept_id="family_domestic_violence",
                name="Domestic Violence",
                subject="family_law",
                difficulty=3,
                rule_statement="Protective orders available; ex parte emergency; full hearing; custody and support implications; violation is contempt/crime",
                elements=['Ex parte available', 'Full hearing', 'Relief available', 'Violation sanctions'],
                common_traps=['Ex parte standard lower', 'Custody preferences', 'Criminal violation'],
            ),
            KnowledgeNode(
                concept_id="family_protective_orders",
                name="Protective Orders",
                subject="family_law",
                difficulty=3,
                rule_statement="Restraining orders to prevent abuse; standards: immediate danger, abuse occurred; violations punishable; mutual orders disfavored",
                elements=['Standard for issuance', 'Relief available', 'Violation consequences', 'Mutual orders issue'],
                common_traps=['Standard of proof', 'Duration', 'Mutual orders problematic'],
            ),
            KnowledgeNode(
                concept_id="family_prenuptial_agreements",
                name="Prenuptial Agreements",
                subject="family_law",
                difficulty=4,
                rule_statement="Valid if: voluntary, fair disclosure, not unconscionable; cannot adversely affect child support; can waive spousal support",
                elements=['Voluntary execution', 'Financial disclosure', 'Conscionability', 'Cannot affect child support'],
                common_traps=['Full disclosure required', 'Cannot limit child support', 'Can waive spousal support'],
                # Mnemonic: VFC: Voluntary, Fair disclosure, Conscionable
            ),
            KnowledgeNode(
                concept_id="family_postnuptial_agreements",
                name="Postnuptial Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Agreement after marriage; same requirements as prenuptial plus consideration; scrutinized closely; increasing acceptance",
                elements=['After marriage', 'Consideration needed', 'Close scrutiny', 'Similar to prenup'],
                common_traps=['Need consideration', 'Higher scrutiny', 'Growing acceptance'],
            ),
            KnowledgeNode(
                concept_id="family_separation_agreements",
                name="Separation Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Negotiated settlement of divorce issues; merged into decree if approved; court reviews for fairness; child provisions always modifiable",
                elements=['Negotiated settlement', 'Court approval', 'Fairness review', 'Merger into decree'],
                common_traps=['Court must approve', 'Child provisions modifiable', 'Merger vs incorporation'],
            ),
            KnowledgeNode(
                concept_id="family_mediation",
                name="Mediation & ADR",
                subject="family_law",
                difficulty=2,
                rule_statement="Alternative dispute resolution; mediator facilitates; confidential; many jurisdictions require mediation attempt; custody mediation common",
                elements=['Facilitative process', 'Confidentiality', 'Mandatory in some places', 'Custody focus'],
                common_traps=['Confidentiality protections', 'No binding decision', 'Mandatory mediation'],
            ),
            KnowledgeNode(
                concept_id="family_tax_consequences",
                name="Tax Consequences of Divorce",
                subject="family_law",
                difficulty=3,
                rule_statement="Property transfers: generally tax-free; Alimony: post-2018 not deductible/taxable; Child support: not deductible/taxable; Dependency exemptions",
                elements=['Property transfer rules', 'Alimony tax treatment', 'Child support treatment', 'Exemptions'],
                common_traps=['2018 tax law changes', 'Property transfer tax-free', 'Child support never deductible'],
            ),
            KnowledgeNode(
                concept_id="family_bankruptcy",
                name="Bankruptcy & Family Law",
                subject="family_law",
                difficulty=3,
                rule_statement="Child support non-dischargeable; spousal support non-dischargeable; property division may be dischargeable; automatic stay exceptions",
                elements=['Support obligations survive', 'Property division varies', 'Stay exceptions', 'Priority debts'],
                common_traps=['Support never dischargeable', 'Property division in Ch 13', 'Stay exceptions'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_secured_transactions(self):
        """18 Secured Transactions concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="secured_types_collateral",
                name="Types of Collateral",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods: consumer, equipment, farm products, inventory; Intangibles: accounts, instruments, documents, chattel paper, investment property, deposit accounts",
                elements=['Goods categories', 'Intangibles', 'Classification determines rules', 'Use-based for goods'],
                common_traps=['Use determines goods classification', 'Dual-use situations', 'Transformation changes type'],
            ),
            KnowledgeNode(
                concept_id="secured_after_acquired",
                name="After-Acquired Property Clause",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Security interest attaches to after-acquired property if clause included; automatic for inventory and accounts; exception for consumer goods",
                elements=['Requires clause', 'Automatic inventory/accounts', 'Consumer goods limit', 'Attaches when acquired'],
                common_traps=['Consumer goods 10-day limit', 'Inventory automatic', 'Must have clause'],
            ),
            KnowledgeNode(
                concept_id="secured_proceeds",
                name="Proceeds",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Security interest continues in proceeds; automatically perfected for 20 days; must perfect afterward; identifiable proceeds required",
                elements=['Automatic security interest', '20-day perfection', 'Must perfect after', 'Identifiable standard'],
                common_traps=['20-day temporary perfection', 'Lowest intermediate balance rule', 'Cash proceeds'],
            ),
            KnowledgeNode(
                concept_id="secured_future_advances",
                name="Future Advances",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Security interest can secure future loans; priority from original perfection if within 45 days or committed",
                elements=['Secures future debts', 'Original priority', '45-day rule', 'Commitment'],
                common_traps=['Priority relates back', '45-day rule', 'Optional vs committed'],
            ),
            KnowledgeNode(
                concept_id="secured_bioc",
                name="Buyer in Ordinary Course",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="BIOC takes free of security interest in inventory even if perfected and knows; must be ordinary course; good faith; value given",
                elements=['Takes free', 'Inventory only', 'Ordinary course', 'Good faith + value'],
                common_traps=['Takes free even with knowledge', 'Inventory only', 'Ordinary course requirement'],
                # Mnemonic: BIOC: Buyer, Inventory, Ordinary, Course (takes free)
            ),
            KnowledgeNode(
                concept_id="secured_fixtures",
                name="Fixtures",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Personal property that becomes real property; fixture filing perfects; PMSI fixture has priority if: filed before or within 20 days, construction mortgage exception",
                elements=['Fixture definition', 'Fixture filing', 'PMSI priority', 'Construction mortgage'],
                common_traps=['20-day grace period', 'Construction mortgage wins', 'Fixture filing location'],
            ),
            KnowledgeNode(
                concept_id="secured_accessions",
                name="Accessions",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods installed in other goods; security interest continues; perfection required; removal right if no material harm",
                elements=['Continues in accession', 'Perfection needed', 'Priority rules', 'Removal rights'],
                common_traps=['First to file wins', 'Material harm test', 'PMSI super-priority'],
            ),
            KnowledgeNode(
                concept_id="secured_commingled",
                name="Commingled Goods",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods physically united in product; security interest continues in product; perfection continues; priority prorata by value",
                elements=['Continues in product', 'Perfection continues', 'Pro rata priority', 'Cannot separate'],
                common_traps=['Pro rata distribution', 'Cannot separate', 'Perfection continues'],
            ),
            KnowledgeNode(
                concept_id="secured_investment_property",
                name="Investment Property",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Securities, security entitlements, accounts; perfection by control or filing; control has priority over filing",
                elements=['Control perfection', 'Filing alternative', 'Control priority', 'Types included'],
                common_traps=['Control beats filing', 'Control methods', 'Securities intermediary'],
            ),
            KnowledgeNode(
                concept_id="secured_deposit_accounts",
                name="Deposit Accounts",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Can only perfect by control; control: secured party is bank, control agreement, or secured party is account holder",
                elements=['Control only', 'Three methods', 'No filing perfection', 'Priority by control'],
                common_traps=['Cannot perfect by filing', 'Control methods', 'Bank as secured party'],
            ),
            KnowledgeNode(
                concept_id="secured_lien_creditor",
                name="Lien Creditors",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Secured party vs lien creditor: perfected wins; unperfected loses unless PMSI grace period; trustee in bankruptcy is lien creditor",
                elements=['Perfected beats lien creditor', 'Unperfected loses', 'PMSI grace period', 'Bankruptcy trustee'],
                common_traps=['Trustee as lien creditor', 'PMSI grace period', 'Perfection timing critical'],
            ),
            KnowledgeNode(
                concept_id="secured_continuation",
                name="Continuation Statements",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Filing effective 5 years; continuation filed within 6 months before lapse; extends another 5 years",
                elements=['5-year duration', '6-month window', 'Extends 5 years', 'Must be timely'],
                common_traps=['6-month window', 'Lapses if not filed', 'Calculation of dates'],
            ),
            KnowledgeNode(
                concept_id="secured_termination",
                name="Termination Statements",
                subject="secured_transactions",
                difficulty=2,
                rule_statement="Secured party must file termination when debt paid; consumer goods: 1 month or 20 days if requested; other collateral: on demand",
                elements=['Must file when paid', 'Consumer timing', 'Non-consumer on demand', 'Penalties for failure'],
                common_traps=['Consumer timing strict', 'Must file termination', 'Failure penalties'],
            ),
            KnowledgeNode(
                concept_id="secured_assignments",
                name="Assignment of Security Interest",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Can assign security interest; need not file unless assignee wants priority over later assignee; notification to debtor",
                elements=['Assignability', 'Filing not required', 'Priority of assignees', 'Debtor notification'],
                common_traps=['Filing not required for perfection', 'Priority among assignees', 'Debtor payment rules'],
            ),
            KnowledgeNode(
                concept_id="secured_agricultural_liens",
                name="Agricultural Liens",
                subject="secured_transactions",
                difficulty=2,
                rule_statement="Non-consensual lien on farm products; perfection by filing; priority rules similar to Article 9; statute creates",
                elements=['Statutory lien', 'Farm products', 'Filing perfects', 'Similar priority'],
                common_traps=['Not security interest', 'Statutory basis', 'Filing required'],
            ),
            KnowledgeNode(
                concept_id="secured_bankruptcy_trustee",
                name="Bankruptcy Trustee Powers",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Trustee has strong-arm power: lien creditor status; can avoid unperfected interests; 90-day preference period for perfection",
                elements=['Lien creditor status', 'Avoid unperfected', '90-day preference', 'Filing relates back'],
                common_traps=['90-day preference', 'Grace period protection', 'Relates back if timely'],
            ),
            KnowledgeNode(
                concept_id="secured_preferences",
                name="Preferences in Bankruptcy",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Transfer within 90 days while insolvent that prefers creditor can be avoided; exceptions: contemporaneous exchange, ordinary course, PMSI grace",
                elements=['90-day lookback', 'Insolvency presumed', 'Preference elements', 'Exceptions'],
                common_traps=['90 days', 'PMSI grace period exception', 'Ordinary course exception'],
            ),
            KnowledgeNode(
                concept_id="secured_fraudulent_transfers",
                name="Fraudulent Transfers",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Transfer to hinder, delay, defraud creditors; transfer for less than reasonably equivalent value while insolvent; can be avoided",
                elements=['Actual fraud', 'Constructive fraud', 'Reasonably equivalent value', 'Insolvency'],
                common_traps=['Actual vs constructive', 'Timing', 'Badges of fraud'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_iowa_procedure(self):
        """15 Iowa Procedure concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="iowa_pleading",
                name="Iowa Pleading Requirements",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Iowa requires notice pleading similar to federal; original notice serves as complaint; must state claim upon which relief can be granted",
                elements=['Original notice', 'Notice pleading', 'State claim', 'Similar to federal'],
                common_traps=['Original notice terminology', 'Similar to FRCP', 'Specific Iowa forms'],
            ),
            KnowledgeNode(
                concept_id="iowa_service",
                name="Iowa Service of Process",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Personal service by sheriff or process server; substituted service available; service by publication with court approval",
                elements=['Personal service', 'Sheriff service', 'Substituted service', 'Publication service'],
                common_traps=['Sheriff preference', 'Publication requirements', 'Proof of service'],
            ),
            KnowledgeNode(
                concept_id="iowa_discovery",
                name="Iowa Discovery Rules",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Iowa discovery mirrors federal rules; interrogatories, depositions, requests for production, admissions; proportionality applies",
                elements=['Federal model', 'All federal tools', 'Proportionality', 'Protective orders'],
                common_traps=['Similar to federal', 'Iowa-specific limits', 'Timing differences'],
            ),
            KnowledgeNode(
                concept_id="iowa_summary_judgment",
                name="Iowa Summary Judgment",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Available if no genuine issue of material fact; moving party burden; view evidence in light favorable to non-movant",
                elements=['No genuine issue', 'Material fact', 'Moving party burden', 'Favorable view'],
                common_traps=['Standard similar to federal', 'Iowa case law', 'Timing requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_trial_procedures",
                name="Iowa Trial Procedures",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Jury trial right; voir dire conducted by judge typically; Iowa Rules of Evidence govern; jury instructions settled before trial",
                elements=['Jury right', 'Judge voir dire', 'Evidence rules', 'Jury instructions'],
                common_traps=['Judge-conducted voir dire', 'Iowa evidence rules', 'Pre-trial procedures'],
            ),
            KnowledgeNode(
                concept_id="iowa_appeals",
                name="Iowa Appellate Procedure",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Appeal to Iowa Court of Appeals or Supreme Court; notice of appeal within 30 days; record and brief requirements; standards of review",
                elements=['30-day deadline', 'Notice of appeal', 'Record requirements', 'Standards of review'],
                common_traps=['30-day deadline strict', 'Direct to Supreme Court options', 'Preservation requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_venue",
                name="Iowa Venue",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Proper venue: defendant residence, cause of action arose, property located, contract performed; transfer available",
                elements=['Defendant residence', 'Cause arose', 'Property location', 'Transfer possible'],
                common_traps=['Multiple proper venues', 'Transfer discretion', 'Convenience factors'],
            ),
            KnowledgeNode(
                concept_id="iowa_jurisdiction",
                name="Iowa Personal Jurisdiction",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Long-arm statute reaches constitutional limits; minimum contacts required; purposeful availment; fair play and substantial justice",
                elements=['Long-arm statute', 'Constitutional limits', 'Minimum contacts', 'Fairness test'],
                common_traps=['Constitutional analysis', 'Specific vs general', 'Stream of commerce'],
            ),
            KnowledgeNode(
                concept_id="iowa_joinder",
                name="Iowa Joinder Rules",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Permissive joinder of parties and claims; compulsory joinder of necessary parties; intervention and interpleader available",
                elements=['Permissive joinder', 'Necessary parties', 'Intervention', 'Interpleader'],
                common_traps=['Similar to federal', 'Iowa variations', 'Necessary vs indispensable'],
            ),
            KnowledgeNode(
                concept_id="iowa_class_actions",
                name="Iowa Class Actions",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Class actions permitted; requirements similar to federal; certification required; notice to class members",
                elements=['Certification requirements', 'Numerosity', 'Commonality', 'Notice'],
                common_traps=['Certification motion', 'Opt-out rights', 'Settlement approval'],
            ),
            KnowledgeNode(
                concept_id="iowa_injunctions",
                name="Iowa Injunctions",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Temporary and permanent injunctions available; requirements: likelihood of success, irreparable harm, balance of harms, public interest",
                elements=['Temporary injunction', 'Permanent injunction', 'Four factors', 'Bond requirement'],
                common_traps=['Four-factor test', 'Bond for temporary', 'Hearing requirements'],
            ),
            KnowledgeNode(
                concept_id="iowa_judgments",
                name="Iowa Judgments",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Default judgment available; directed verdict/JNOV motions; new trial motions; judgment liens; enforcement procedures",
                elements=['Default judgment', 'Post-trial motions', 'Judgment liens', 'Enforcement'],
                common_traps=['Motion timing', 'Lien procedures', 'Enforcement methods'],
            ),
            KnowledgeNode(
                concept_id="iowa_execution",
                name="Iowa Execution & Garnishment",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Execution on judgment; garnishment of wages and accounts; exemptions protect certain property; procedures for collection",
                elements=['Execution process', 'Garnishment', 'Exemptions', 'Debtor protections'],
                common_traps=['Iowa exemptions', 'Garnishment limits', 'Procedures'],
            ),
            KnowledgeNode(
                concept_id="iowa_sanctions",
                name="Iowa Sanctions",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Court may sanction frivolous filings, discovery abuse, contempt; attorney fees available; Rule 1.413 governs",
                elements=['Frivolous filings', 'Discovery sanctions', 'Contempt', 'Attorney fees'],
                common_traps=['Rule 1.413', 'Standards for sanctions', 'Safe harbor'],
            ),
            KnowledgeNode(
                concept_id="iowa_adr",
                name="Iowa ADR Procedures",
                subject="iowa_procedure",
                difficulty=2,
                rule_statement="Mediation encouraged; arbitration enforceable; case management conferences; settlement conferences",
                elements=['Mediation', 'Arbitration', 'Case management', 'Settlement conferences'],
                common_traps=['Mandatory mediation in some cases', 'Arbitration enforcement', 'Confidentiality'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_business_associations(self):
        """Business Associations - 7 comprehensive concepts with NCBE rules"""
        concepts = [
            KnowledgeNode(
                concept_id="bizassoc_entity_selection",
                name="Business Entity Formation & Selection",
                subject="business_associations",
                difficulty=3,
                rule_statement="Choice of entity depends on: liability protection, tax treatment, management structure, transferability, and formality requirements. Sole proprietorships offer no protection; partnerships have personal liability; corporations and LLCs provide limited liability.",
                elements=['Liability protection', 'Tax treatment (pass-through vs double)', 'Management flexibility', 'Formalities required', 'Transferability of interests'],
                common_traps=['LLC members can lose protection if formalities ignored', 'S-corp eligibility limits', 'Partnership liability is joint and several'],
            ),
            KnowledgeNode(
                concept_id="bizassoc_partnership",
                name="General & Limited Partnerships",
                subject="business_associations",
                difficulty=3,
                rule_statement="General partnership: created by association to carry on business for profit; all partners have equal management rights and unlimited personal liability. Limited partnership: requires filing; GPs have liability, LPs have limited liability if they don't participate in control.",
                elements=['Formation by association (GP) or filing (LP)', 'Joint and several liability for GPs', 'LP control rule (RULPA vs ULPA 2001)', 'Fiduciary duties apply', 'Partner authority to bind'],
                common_traps=['Inadvertent partnership creation', 'LP loses protection by controlling', 'Partnership by estoppel'],
            ),
            KnowledgeNode(
                concept_id="bizassoc_corporation",
                name="Corporate Formation & Structure",
                subject="business_associations",
                difficulty=3,
                rule_statement="Corporation formed by filing articles of incorporation with state; creates separate legal entity with perpetual existence. Shareholders own, directors manage, officers execute. Internal affairs governed by state of incorporation.",
                elements=['Articles of incorporation (required contents)', 'Bylaws (internal governance)', 'Shareholder/director/officer roles', 'Corporate formalities', 'Internal affairs doctrine'],
                common_traps=['De facto corporation doctrine', 'Corporation by estoppel', 'Ultra vires acts generally enforceable'],
            ),
            KnowledgeNode(
                concept_id="bizassoc_llc",
                name="Limited Liability Companies",
                subject="business_associations",
                difficulty=3,
                rule_statement="LLC combines limited liability of corporation with pass-through taxation and management flexibility of partnership. Formed by filing articles of organization; governed by operating agreement. Members can manage directly or appoint managers.",
                elements=['Articles of organization', 'Operating agreement', 'Member-managed vs manager-managed', 'Charging order as creditor remedy', 'Flexibility in profit allocation'],
                common_traps=['Single-member LLC protection varies by state', 'Operating agreement can modify defaults', 'Piercing applies to LLCs too'],
            ),
            KnowledgeNode(
                concept_id="bizassoc_fiduciary_duties",
                name="Fiduciary Duties (Care, Loyalty, Good Faith)",
                subject="business_associations",
                difficulty=4,
                rule_statement="Duty of Care: act with care that ordinarily prudent person would use; business judgment rule presumes directors acted on informed basis in good faith. Duty of Loyalty: no self-dealing, usurping opportunities, or competing without disclosure. Good Faith: act honestly with fidelity to entity.",
                elements=['Duty of Care (informed decision-making)', 'Business Judgment Rule (presumption)', 'Duty of Loyalty (no conflicts)', 'Corporate Opportunity Doctrine', 'Duty of Good Faith (honest purpose)'],
                common_traps=['BJR is presumption, not substantive standard', 'Interested director transactions voidable unless fair', 'Can waive care in certificate, not loyalty'],
            ),
            KnowledgeNode(
                concept_id="bizassoc_piercing_veil",
                name="Piercing the Corporate Veil",
                subject="business_associations",
                difficulty=4,
                rule_statement="Courts pierce corporate veil to hold shareholders personally liable when: (1) unity of interest and ownership such that separate personalities of corporation and shareholder no longer exist (alter ego), AND (2) adherence to corporate form would sanction fraud or promote injustice.",
                elements=['Alter ego/unity of interest', 'Inadequate capitalization', 'Failure to observe formalities', 'Commingling of funds', 'Fraud or injustice requirement'],
                common_traps=['Rarely successful', 'Undercapitalization alone insufficient', 'Easier to pierce for torts than contracts', 'Applies to LLCs too'],
            ),
            KnowledgeNode(
                concept_id="bizassoc_derivative_suits",
                name="Shareholder Derivative Actions",
                subject="business_associations",
                difficulty=4,
                rule_statement="Shareholder derivative suit: shareholder sues on behalf of corporation for harm to corporation. Requirements: contemporaneous ownership, demand on board (or demand futility), fair and adequate representation. Recovery goes to corporation, not shareholder.",
                elements=['Standing (contemporaneous ownership)', 'Demand requirement', 'Demand futility (Aronson test)', 'Special litigation committee', 'Recovery to corporation'],
                common_traps=['Direct vs derivative distinction', 'Demand futility is high bar', 'SLC can dismiss if independent'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _add_ncbe_constitutional_law(self):
        """Extended Constitutional Law concepts covering full NCBE subject outline"""
        concepts = [
            # ===== JUDICIAL POWER & JUSTICIABILITY =====
            KnowledgeNode(
                concept_id="conlaw_case_controversy",
                name="Case or Controversy Requirement",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Article III limits federal courts to 'cases' and 'controversies' - requires actual dispute between adverse parties seeking specific relief, not advisory opinions.",
                elements=['No advisory opinions', 'Adverse parties required', 'Concrete dispute', 'Judicial remedy available'],
                common_traps=['State courts can give advisory opinions', 'Declaratory judgment still needs dispute'],
            ),
            KnowledgeNode(
                concept_id="conlaw_ripeness",
                name="Ripeness Doctrine",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Case must be ripe for review - hardship to parties from withholding review must be weighed against fitness of issues for judicial decision. Pre-enforcement challenges allowed if harm imminent.",
                elements=['Fitness of issues', 'Hardship to parties', 'Pre-enforcement review', 'Contingent future events'],
                common_traps=['Declaratory judgment on statute before enforcement may be ripe', 'Mere possibility of future harm insufficient'],
            ),
            KnowledgeNode(
                concept_id="conlaw_political_question",
                name="Political Question Doctrine",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Courts won't decide political questions: textual commitment to coordinate branch, lack of judicially manageable standards, impossibility of deciding without policy determination, or need for finality in political branch decision.",
                elements=['Textual commitment to other branch', 'Lack of judicially manageable standards', 'Prudential concerns', 'Baker v. Carr factors'],
                common_traps=['Reapportionment is justiciable (Baker v. Carr)', 'Impeachment procedures not reviewable', 'Foreign affairs often political question'],
            ),
            KnowledgeNode(
                concept_id="conlaw_11th_amendment",
                name="Eleventh Amendment & Sovereign Immunity",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="States immune from suit in federal court by own citizens or citizens of other states. Exceptions: state consent, congressional abrogation under 14th Amendment (not Commerce Clause), Ex parte Young suits against officers for prospective relief.",
                elements=['State sovereign immunity', 'Consent exception', 'Congressional abrogation (14th Amend only)', 'Ex parte Young doctrine', 'Local governments not protected'],
                common_traps=['Seminole Tribe: no Commerce Clause abrogation', 'Ex parte Young allows officer suits', 'Municipalities not immune'],
            ),
            # ===== FEDERAL LEGISLATIVE POWER =====
            KnowledgeNode(
                concept_id="conlaw_necessary_proper",
                name="Necessary and Proper Clause",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Congress may enact laws necessary and proper to carry out enumerated powers. 'Necessary' means convenient or useful, not indispensable (McCulloch v. Maryland). Means must be rationally related to constitutional end.",
                elements=['Not an independent power', 'Implements enumerated powers', 'Rational basis for means', 'McCulloch standard'],
                common_traps=['Not standalone power', 'Very deferential review', 'Cannot violate other constitutional limits'],
            ),
            KnowledgeNode(
                concept_id="conlaw_taxing_power",
                name="Taxing Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Congress may tax for revenue purposes; regulatory taxes valid if producing some revenue or characterized as tax. Direct taxes must be apportioned among states by population; 16th Amendment allows unapportioned income tax.",
                elements=['Revenue purpose', 'Regulatory taxes allowed', 'Direct tax apportionment', '16th Amendment income tax'],
                common_traps=['ACA mandate upheld as tax', 'Regulatory purpose alone insufficient', 'Export taxes prohibited'],
            ),
            KnowledgeNode(
                concept_id="conlaw_spending_clause",
                name="Spending Clause",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Congress may spend for general welfare; may attach conditions to funds if: (1) in pursuit of general welfare, (2) conditions unambiguous, (3) related to federal interest in program, (4) no independent constitutional bar, (5) not coercive.",
                elements=['General welfare purpose', 'Unambiguous conditions', 'Germaneness to program', 'No constitutional violations', 'Non-coercive (Sebelius)'],
                common_traps=['NFIB v. Sebelius: Medicaid expansion coercive', 'South Dakota v. Dole: highway funds conditions OK', 'Broader than Commerce power'],
            ),
            KnowledgeNode(
                concept_id="conlaw_war_power",
                name="War Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Congress has power to declare war, raise armies, provide for common defense. War powers extend to economic regulation, civil liberties restrictions during wartime. President is Commander-in-Chief but Congress controls funding.",
                elements=['Declare war', 'Raise and support armies', 'Economic wartime regulation', 'Post-war reconstruction'],
                common_traps=['President can use force without declaration', 'War Powers Resolution limits', 'Emergency powers broad'],
            ),
            KnowledgeNode(
                concept_id="conlaw_anti_commandeering",
                name="Anti-Commandeering Doctrine",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="10th Amendment prohibits Congress from commandeering states: cannot compel state legislatures to enact laws (New York v. US) or state executives to enforce federal programs (Printz v. US). Congress can offer incentives or regulate directly.",
                elements=['No commandeering legislatures', 'No commandeering executives', 'Incentives permitted', 'Direct federal regulation OK', 'Preemption allowed'],
                common_traps=['Murphy v. NCAA: cannot prohibit states from acting', 'Can regulate individuals directly', 'Spending conditions not commandeering'],
            ),
            # ===== FEDERALISM =====
            KnowledgeNode(
                concept_id="conlaw_supremacy_clause",
                name="Supremacy Clause",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Federal law is supreme law of land; valid federal law preempts conflicting state law. Supremacy applies to Constitution, federal statutes, and treaties. State judges bound by federal law.",
                elements=['Federal law supreme', 'Preemption of conflicts', 'State judges bound', 'Treaties included'],
                common_traps=['Only valid federal law preempts', 'Not all federal-state conflicts resolved by preemption'],
            ),
            KnowledgeNode(
                concept_id="conlaw_preemption_types",
                name="Types of Federal Preemption",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Express preemption: statute explicitly preempts. Field preemption: federal regulation so pervasive it occupies field. Conflict preemption: impossible to comply with both, or state law obstacles federal purpose.",
                elements=['Express preemption', 'Field preemption (pervasive regulation)', 'Conflict preemption (impossibility)', 'Obstacle preemption'],
                common_traps=['Presumption against preemption in traditional state areas', 'Savings clauses may preserve state law', 'Look to congressional intent'],
            ),
            KnowledgeNode(
                concept_id="conlaw_intergovernmental_immunity",
                name="Intergovernmental Immunity",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="States cannot directly tax or regulate federal government or its instrumentalities. Federal government generally immune from state law that would interfere with federal operations.",
                elements=['No state taxation of federal government', 'No state regulation of federal operations', "McCulloch: power to tax is power to destroy", 'Discrimination against federal activities prohibited'],
                common_traps=['Non-discriminatory taxes on federal contractors OK', 'Federal property can be taxed if Congress consents'],
            ),
            KnowledgeNode(
                concept_id="conlaw_privileges_immunities_art4",
                name="Privileges & Immunities Clause (Article IV)",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="States cannot discriminate against out-of-state citizens regarding fundamental rights (economic activities, civil liberties). Requires substantial reason for discrimination and reasonable relationship to that reason.",
                elements=['Protects citizens (not corporations/aliens)', 'Fundamental rights only', 'Substantial justification needed', 'Different from 14th Amend P&I'],
                common_traps=['Corporations not protected', 'Recreational activities may not be fundamental', 'Different from Dormant Commerce Clause'],
            ),
            # ===== EXECUTIVE POWER =====
            KnowledgeNode(
                concept_id="conlaw_appointment_power",
                name="Appointment Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="President appoints principal officers with Senate advice and consent. Congress may vest appointment of inferior officers in President, courts, or department heads. Congress cannot appoint officers who execute law.",
                elements=['Principal officers: Senate confirmation', 'Inferior officers: alternative appointment', 'Congress cannot appoint', 'Buckley v. Valeo limits'],
                common_traps=['Inferior vs principal distinction unclear', 'Removal power implied from appointment', 'Recess appointments limited'],
            ),
            KnowledgeNode(
                concept_id="conlaw_removal_power",
                name="Removal Power",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="President has inherent power to remove executive officers. Congress may impose limited restrictions (good cause) for officers with quasi-judicial/quasi-legislative functions, but cannot insulate officers from all presidential control.",
                elements=['Inherent removal authority', 'Good cause limits for independent agencies', 'No double for-cause protection (Free Enterprise)', 'Cannot give removal to Congress'],
                common_traps=['Free Enterprise Fund: dual for-cause unconstitutional', 'Myers: postmaster removable at will', 'Humphrey\'s Executor: FTC commissioner protected'],
            ),
            KnowledgeNode(
                concept_id="conlaw_executive_privilege",
                name="Executive Privilege",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="President has qualified privilege for confidential communications with advisors. Not absolute - must yield to demonstrated specific need in criminal proceedings. Stronger for national security, military, diplomatic matters.",
                elements=['Qualified privilege', 'Yields to specific need in criminal cases', 'Stronger for national security', 'US v. Nixon standard'],
                common_traps=['Not mentioned in Constitution', 'Privilege belongs to President, not advisors', 'Must be properly invoked'],
            ),
            KnowledgeNode(
                concept_id="conlaw_executive_immunity",
                name="Executive Immunity",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="President has absolute immunity from civil damages for official acts (Nixon v. Fitzgerald). No immunity for unofficial conduct (Clinton v. Jones). Presidential aides have qualified immunity only.",
                elements=['Absolute immunity for official acts', 'No immunity for unofficial conduct', 'Qualified immunity for aides', 'Criminal liability possible'],
                common_traps=['Trump v. Vance: no immunity from state grand jury subpoena', 'Unofficial acts defined broadly', 'Impeachment always available'],
            ),
            KnowledgeNode(
                concept_id="conlaw_treaty_power",
                name="Treaty Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="President makes treaties with advice and consent of 2/3 Senate. Treaties are supreme law of land. Self-executing treaties have direct effect; non-self-executing require implementing legislation. Executive agreements don't require Senate approval.",
                elements=['2/3 Senate approval', 'Supreme law of land', 'Self-executing vs non-self-executing', 'Executive agreements alternative'],
                common_traps=['Last-in-time rule with statutes', 'Executive agreements cannot override statutes', 'Reid v. Covert: cannot violate Constitution'],
            ),
            # ===== DUE PROCESS =====
            KnowledgeNode(
                concept_id="conlaw_incorporation",
                name="Incorporation Doctrine",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="14th Amendment Due Process incorporates most Bill of Rights protections against states. Test: whether right is fundamental to ordered liberty or deeply rooted in history and tradition.",
                elements=['Selective incorporation', 'Fundamental to ordered liberty', 'Most Bill of Rights incorporated', 'Exceptions: grand jury, civil jury, excessive bail'],
                common_traps=['Not all amendments incorporated', 'Same standards apply to states', 'McDonald v. Chicago: 2nd Amendment incorporated'],
            ),
            KnowledgeNode(
                concept_id="conlaw_takings",
                name="Takings Clause",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Government cannot take private property for public use without just compensation. Physical takings: per se taking. Regulatory takings: Penn Central factors (economic impact, investment-backed expectations, character of government action).",
                elements=['Public use requirement', 'Just compensation', 'Physical vs regulatory takings', 'Penn Central factors', 'Per se rules (Loretto, Lucas)'],
                common_traps=['Kelo: broad public use definition', 'Lucas: total economic deprivation = taking', 'Exactions require nexus and proportionality'],
            ),
            KnowledgeNode(
                concept_id="conlaw_exactions",
                name="Exactions (Nollan/Dolan)",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Government conditions on land use permits (exactions) require essential nexus between condition and legitimate state interest, and rough proportionality between condition and impact of proposed development.",
                elements=['Essential nexus (Nollan)', 'Rough proportionality (Dolan)', 'Applies to permit conditions', 'Koontz: applies to monetary exactions'],
                common_traps=['Different from regulatory takings analysis', 'Government bears burden of proof', 'Applies even if permit denial would be valid'],
            ),
            KnowledgeNode(
                concept_id="conlaw_contracts_clause",
                name="Contracts Clause",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="States shall not impair obligation of contracts. Applies only to states, not federal government. Substantial impairment requires legitimate public purpose and reasonable means. Stricter scrutiny for state's own contracts.",
                elements=['State action only', 'Substantial impairment test', 'Legitimate public purpose', 'Reasonable and appropriate means', 'Stricter for government contracts'],
                common_traps=['Does not apply to federal government', 'Prospective contract regulation OK', 'Reserved police powers limit contracts'],
            ),
            KnowledgeNode(
                concept_id="conlaw_ex_post_facto",
                name="Ex Post Facto & Bills of Attainder",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Ex post facto: prohibits retroactive criminal laws that punish previously lawful conduct, increase punishment, or reduce evidence required. Bill of attainder: legislative act inflicting punishment without trial on named individuals or group.",
                elements=['Criminal laws only (ex post facto)', 'Retroactive punishment prohibited', 'Bill of attainder: legislative punishment', 'Named individuals or identifiable group'],
                common_traps=['Civil laws can be retroactive', 'Procedural changes may apply retroactively', 'Tax laws can be retroactive'],
            ),
            # ===== EQUAL PROTECTION =====
            KnowledgeNode(
                concept_id="conlaw_rational_basis",
                name="Rational Basis Review",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Default standard: law upheld if rationally related to legitimate government interest. Very deferential - any conceivable rational basis sufficient. Government not required to articulate actual purpose.",
                elements=['Legitimate government interest', 'Rational relationship', 'Conceivable basis sufficient', 'Highly deferential'],
                common_traps=['Rarely struck down', 'Hypothetical reasons count', 'Rational basis "with bite" in some LGBT cases'],
            ),
            KnowledgeNode(
                concept_id="conlaw_suspect_classes",
                name="Suspect Classifications (Strict Scrutiny)",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Race, national origin, alienage (state action) are suspect classes requiring strict scrutiny: law must be necessary to achieve compelling government interest. Burden on government; narrowly tailored means required.",
                elements=['Race, national origin, alienage (state)', 'Compelling interest required', 'Narrowly tailored means', 'Least restrictive alternative'],
                common_traps=['Federal alienage = rational basis', 'Affirmative action uses strict scrutiny', 'Discriminatory intent required for facially neutral laws'],
            ),
            KnowledgeNode(
                concept_id="conlaw_quasi_suspect",
                name="Quasi-Suspect Classifications (Intermediate Scrutiny)",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Gender, legitimacy are quasi-suspect classes requiring intermediate scrutiny: law must be substantially related to important government interest. Exceedingly persuasive justification required for gender.",
                elements=['Gender, legitimacy', 'Important government interest', 'Substantially related means', 'VMI: exceedingly persuasive justification'],
                common_traps=['Affirmative action for gender uses intermediate', 'Statistical generalizations insufficient', 'Actual purpose matters, not hypothetical'],
            ),
            KnowledgeNode(
                concept_id="conlaw_affirmative_action",
                name="Affirmative Action",
                subject="constitutional_law",
                difficulty=5,
                rule_statement="Race-conscious government action subject to strict scrutiny. Remedying past discrimination may be compelling interest if specific findings. Diversity in higher education was compelling (Grutter) but SFFA v. Harvard (2023) rejected race as admissions factor.",
                elements=['Strict scrutiny applies', 'Specific findings of past discrimination', 'Narrowly tailored remedies', 'SFFA v. Harvard: no race in admissions', 'Sunset provisions helpful'],
                common_traps=['Quotas unconstitutional', 'Societal discrimination insufficient', 'Race-neutral alternatives must be considered'],
            ),
            KnowledgeNode(
                concept_id="conlaw_fundamental_voting",
                name="Voting Rights & Equal Protection",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Right to vote is fundamental; restrictions subject to strict scrutiny. One person, one vote requires equal population districts. Durational residency limits, poll taxes, and wealth-based restrictions unconstitutional.",
                elements=['Fundamental right', 'One person one vote', 'Equal districts', 'No poll taxes (24th Amendment)', 'Ballot access restrictions'],
                common_traps=['Voter ID laws vary by state', 'Felon disenfranchisement OK under 14th Sec 2', 'Gerrymandering (partisan) = political question'],
            ),
            KnowledgeNode(
                concept_id="conlaw_right_to_travel",
                name="Right to Travel",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Fundamental right to travel between states; durational residency requirements for benefits trigger strict scrutiny. Shorter residency requirements for voting, divorce may survive under lesser scrutiny.",
                elements=['Interstate travel protected', 'Durational residency strict scrutiny', 'Saenz v. Roe: welfare benefits', 'P&I Clause source (14th Amend)'],
                common_traps=['In-state travel less protected', 'Bona fide residency requirements OK', 'Different from Dormant Commerce Clause'],
            ),
            # ===== FIRST AMENDMENT - SPEECH =====
            KnowledgeNode(
                concept_id="conlaw_content_based",
                name="Content-Based vs Content-Neutral Restrictions",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Content-based restrictions target speech because of message, ideas, or subject matter - strict scrutiny applies. Content-neutral restrictions regulate time, place, manner regardless of message - intermediate scrutiny applies.",
                elements=['Content-based = strict scrutiny', 'Content-neutral = intermediate', 'Look to purpose and effect', 'Secondary effects doctrine'],
                common_traps=['Reed v. Town of Gilbert: broad content-based definition', 'Secondary effects can make law content-neutral', 'Viewpoint discrimination always strict scrutiny'],
            ),
            KnowledgeNode(
                concept_id="conlaw_unprotected_speech",
                name="Categories of Unprotected Speech",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Some speech categories receive no First Amendment protection: incitement to imminent lawless action, true threats, fighting words, obscenity, child pornography. These may be prohibited entirely.",
                elements=['Incitement (Brandenburg)', 'True threats', 'Fighting words', 'Obscenity (Miller test)', 'Child pornography'],
                common_traps=['Hate speech alone is protected', 'Virtual child porn may be protected', 'Cross-burning: context matters'],
            ),
            KnowledgeNode(
                concept_id="conlaw_obscenity_miller",
                name="Obscenity (Miller Test)",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Obscenity unprotected under Miller test: (1) average person applying contemporary community standards finds work appeals to prurient interest, (2) depicts sexual conduct in patently offensive way, (3) lacks serious literary, artistic, political, or scientific value.",
                elements=['Prurient interest (community standards)', 'Patently offensive depiction', 'Lacks SLAPS value (national standard)', 'Three-part conjunctive test'],
                common_traps=['Community standards for first two prongs', 'National standard for SLAPS value', 'Zoning restrictions on adult businesses OK'],
            ),
            KnowledgeNode(
                concept_id="conlaw_fighting_words",
                name="Fighting Words & True Threats",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Fighting words: face-to-face personal insults likely to provoke immediate violent reaction. True threats: statements expressing serious intent to commit violence against identifiable individual or group. Both unprotected.",
                elements=['Fighting words: face-to-face', 'Likely to provoke violence', 'True threats: serious intent to harm', 'Virginia v. Black: cross-burning'],
                common_traps=['General advocacy of violence protected', "Chaplinsky's broad language narrowed", 'Context matters for true threats'],
            ),
            KnowledgeNode(
                concept_id="conlaw_defamation_const",
                name="Defamation & Constitutional Limits",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Public officials/figures must prove actual malice (knowledge of falsity or reckless disregard for truth). Private figures on public issues need negligence; presumed/punitive damages require actual malice. Pure private matters: state law applies.",
                elements=['Public officials/figures: actual malice', 'Private figures: negligence', 'Presumed damages: actual malice', 'Matters of public concern'],
                common_traps=['NYT v. Sullivan: actual malice standard', 'Gertz: private figure rules', 'Opinion vs fact distinction'],
            ),
            KnowledgeNode(
                concept_id="conlaw_commercial_speech",
                name="Commercial Speech",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Commercial speech (advertising) protected but receives intermediate scrutiny under Central Hudson: (1) speech not misleading and concerns lawful activity, (2) substantial government interest, (3) regulation directly advances interest, (4) no more extensive than necessary.",
                elements=['Proposes commercial transaction', 'Central Hudson 4-part test', 'Cannot be misleading', 'Substantial interest required', 'Not least restrictive means'],
                common_traps=['False advertising unprotected', 'Professional speech rules complex', 'Compelled commercial disclosures: Zauderer'],
            ),
            KnowledgeNode(
                concept_id="conlaw_symbolic_speech",
                name="Symbolic Speech & Expressive Conduct",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Conduct intended to convey particularized message likely understood as such is expressive conduct protected by First Amendment. O'Brien test for regulations: important government interest unrelated to suppression of expression, and incidental restriction no greater than essential.",
                elements=["O'Brien test for conduct regulation", 'Intent to convey message', 'Likelihood of understanding', 'Unrelated to content', 'No greater restriction than necessary'],
                common_traps=['Flag burning protected (Texas v. Johnson)', 'Draft card burning: government interest in system', 'Nude dancing: minimal protection'],
            ),
            KnowledgeNode(
                concept_id="conlaw_prior_restraints",
                name="Prior Restraints",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Prior restraints on speech bear heavy presumption of unconstitutionality. Government must show: procedural safeguards, narrow standards, prompt judicial review. Licensing schemes must have clear standards and not give unfettered discretion.",
                elements=['Heavy presumption against', 'Near v. Minnesota', 'Pentagon Papers case', 'Licensing must have clear standards', 'Prompt judicial review'],
                common_traps=['Subsequent punishment less disfavored', 'National security can justify rarely', 'Injunctions are prior restraints'],
            ),
            KnowledgeNode(
                concept_id="conlaw_public_forum",
                name="Public Forum Doctrine",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Traditional public forums (streets, parks): strict scrutiny for content-based, reasonable TPM for content-neutral. Designated forums: same rules while open. Non-public forums (government workplace): reasonable and viewpoint-neutral restrictions OK.",
                elements=['Traditional public forum', 'Designated/limited public forum', 'Non-public forum', 'Strict scrutiny for content-based in public', 'Reasonableness in non-public'],
                common_traps=['Government can close designated forum', 'Airport terminals: non-public', 'Viewpoint neutrality always required'],
            ),
            KnowledgeNode(
                concept_id="conlaw_time_place_manner",
                name="Time, Place, and Manner Restrictions",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Content-neutral TPM restrictions in public forum valid if: (1) serve significant government interest, (2) narrowly tailored (not least restrictive means, but not substantially broader than necessary), (3) leave open ample alternative channels.",
                elements=['Content-neutral required', 'Significant government interest', 'Narrowly tailored', 'Alternative channels available'],
                common_traps=['Not least restrictive means test', 'Sound amplification limits OK', 'Permit requirements with standards OK'],
            ),
            KnowledgeNode(
                concept_id="conlaw_overbreadth",
                name="Overbreadth & Vagueness",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Overbreadth: statute substantially overbroad if it punishes significant amount of protected speech (facial challenge allowed). Vagueness: statute void if fails to give reasonable notice of prohibited conduct or allows arbitrary enforcement.",
                elements=['Overbreadth: facial challenge', 'Substantial overbreadth required', 'Vagueness: notice and enforcement', 'First Amendment context expands vagueness'],
                common_traps=['Narrowing construction can save statute', 'Third-party standing for overbreadth', 'Vagueness stricter in speech context'],
            ),
            KnowledgeNode(
                concept_id="conlaw_freedom_association",
                name="Freedom of Association",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="First Amendment protects freedom to associate for expressive purposes. Government interference requires compelling interest narrowly tailored. Forced association (compelled membership, access) requires similar justification.",
                elements=['Expressive association protected', 'Strict scrutiny for burdens', 'Boy Scouts v. Dale', 'Compelled association limits'],
                common_traps=['Non-expressive association less protected', 'Public accommodations laws can prevail', 'Government employees: Janus v. AFSCME'],
            ),
            KnowledgeNode(
                concept_id="conlaw_freedom_press",
                name="Freedom of Press",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Press receives same First Amendment protections as individuals, not more. No special right of access to government proceedings beyond public. Reporter privilege not constitutionally required but may exist under state law.",
                elements=['Same as speech protection', 'No special access rights', 'No constitutional reporter privilege', 'Prior restraint rules apply'],
                common_traps=['Branzburg: no reporter privilege', 'Access to trials is public right', 'Gag orders on press disfavored'],
            ),
            # ===== FIRST AMENDMENT - RELIGION =====
            KnowledgeNode(
                concept_id="conlaw_establishment",
                name="Establishment Clause",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Government cannot establish religion: no endorsement, no coercion, no excessive entanglement. Historical practices analysis (Kennedy v. Bremerton). No aid that advances religion, but neutral programs allowing religious participation OK.",
                elements=['No endorsement', 'No coercion', 'Historical practices test', 'Neutrality principle', 'Kennedy v. Bremerton (2022)'],
                common_traps=['Lemon test largely abandoned', 'Legislative prayer OK (Marsh)', 'School prayer unconstitutional', 'Religious displays: context matters'],
            ),
            KnowledgeNode(
                concept_id="conlaw_lemon_test",
                name="Lemon Test (Historical)",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Traditional Establishment Clause test (now largely superseded by historical practices): (1) law must have secular legislative purpose, (2) principal effect must not advance or inhibit religion, (3) must not foster excessive government entanglement with religion.",
                elements=['Secular purpose', 'Neutral effect', 'No excessive entanglement', 'Three-prong test'],
                common_traps=['Kennedy v. Bremerton (2022) shifted analysis', 'Still cited in some contexts', 'Purpose prong: sham secular purpose fails'],
            ),
            KnowledgeNode(
                concept_id="conlaw_free_exercise",
                name="Free Exercise Clause",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Neutral, generally applicable laws that incidentally burden religion subject to rational basis (Employment Division v. Smith). Laws targeting religion or allowing individualized exemptions require strict scrutiny. RFRA applies to federal government.",
                elements=['Smith: neutral laws OK', 'Targeting religion: strict scrutiny', 'Individualized exemptions trigger scrutiny', 'Fulton v. Philadelphia (2021)', 'RFRA for federal law'],
                common_traps=['No general religious exemption right', 'Hybrid rights exception uncertain', 'State RFRAs vary'],
            ),
            KnowledgeNode(
                concept_id="conlaw_employment_division",
                name="Employment Division v. Smith Standard",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Under Smith, neutral laws of general applicability that incidentally burden religious practice do not violate Free Exercise Clause, even without compelling interest. Religious conduct, unlike belief, may be regulated by valid general laws.",
                elements=['Neutral law of general application', 'Incidental burden on religion', 'No strict scrutiny required', 'Belief/conduct distinction'],
                common_traps=['Exceptions: targeting religion, individualized exemptions', 'Congress responded with RFRA', 'Fulton narrowed but did not overrule'],
            ),
            # ===== SECOND AMENDMENT =====
            KnowledgeNode(
                concept_id="conlaw_second_amendment",
                name="Second Amendment - Right to Bear Arms",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Second Amendment protects individual right to keep and bear arms for lawful purposes like self-defense (Heller). Incorporated against states (McDonald). Bruen (2022): regulations must be consistent with historical tradition of firearm regulation.",
                elements=['Individual right (Heller)', 'Incorporated (McDonald)', 'Historical tradition test (Bruen)', 'Core right: self-defense in home', 'Longstanding prohibitions presumptively lawful'],
                common_traps=['Felon prohibitions OK', 'Machine gun bans may be OK', 'Sensitive places restrictions OK', 'Concealed carry: shall-issue required (Bruen)'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


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
                    except (json.JSONDecodeError, KeyError, ValueError):
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
    """Interactive conversational tutor with advanced pedagogy features"""

    def __init__(self, bar_tutor):
        self.bar_tutor = bar_tutor
        self.state = LearningState()
        self.conversation_history = []
        self.question_bank = {}  # subject -> list of questions
        self._initialize_question_bank()

    def _initialize_question_bank(self):
        """Initialize MBE-style question bank for each subject"""
        self.question_bank = {
            'contracts': [
                {
                    'id': 'contracts_q1',
                    'concept_id': 'contracts_offer',
                    'subject': 'contracts',
                    'question': """A manufacturer sent a letter to a retailer stating: "We will sell you 100 widgets at $5 each. This offer will remain open for 30 days." The retailer received the letter on March 1. On March 10, the manufacturer sent a fax revoking the offer. The retailer received the fax on March 11. On March 12, the retailer mailed a letter accepting the offer. The manufacturer received the acceptance on March 15.

Was a contract formed?""",
                    'options': {
                        'A': 'Yes, because the offer was a firm offer under UCC 2-205',
                        'B': 'Yes, because the acceptance was mailed before the revocation was effective',
                        'C': 'No, because the revocation was effective when received on March 11',
                        'D': 'No, because the manufacturer is not a merchant'
                    },
                    'answer': 'C',
                    'tested_rule': 'Revocation of offers - effective upon receipt by offeree',
                    'why_correct': 'Under common law, an offer can be revoked at any time before acceptance, and revocation is effective upon receipt. Here, the manufacturer revoked (received March 11) before the retailer accepted (mailed March 12). UCC 2-205 firm offers require a signed writing by a merchant, but even merchants can revoke before the stated time expires unless there is consideration.',
                    'difficulty': 3
                },
                {
                    'id': 'contracts_q2',
                    'concept_id': 'contracts_consideration',
                    'subject': 'contracts',
                    'question': """An uncle promised his 21-year-old nephew: "If you refrain from drinking alcohol until you turn 25, I will pay you $10,000." The nephew, who had been a moderate social drinker, completely abstained from alcohol for four years. When the nephew turned 25, he asked his uncle for the money. The uncle refused.

Can the nephew enforce the uncle's promise?""",
                    'options': {
                        'A': 'Yes, because the nephew provided consideration by forbearing a legal right',
                        'B': 'Yes, because the uncle received a benefit from the nephew\'s abstinence',
                        'C': 'No, because the nephew had no legal right to drink alcohol',
                        'D': 'No, because past forbearance cannot serve as consideration'
                    },
                    'answer': 'A',
                    'tested_rule': 'Consideration - forbearance of a legal right constitutes valid consideration',
                    'why_correct': 'Forbearance from exercising a legal right (here, the legal right to drink alcohol at age 21) constitutes valid consideration. The nephew gave up something of value (his legal right to drink) in exchange for the uncle\'s promise. This is the classic Hamer v. Sidway analysis.',
                    'difficulty': 2
                },
                {
                    'id': 'contracts_q3',
                    'concept_id': 'contracts_statute_of_frauds',
                    'subject': 'contracts',
                    'question': """A landowner orally agreed to sell her farm to a buyer for $500,000. The buyer paid $50,000 as a down payment and took possession of the farm. The buyer made $25,000 worth of improvements to the farm. The landowner later refused to convey the property.

Can the buyer enforce the oral agreement?""",
                    'options': {
                        'A': 'No, because real estate contracts must be in writing under the Statute of Frauds',
                        'B': 'No, because the down payment can be returned, making the buyer whole',
                        'C': 'Yes, because the buyer\'s part performance takes the contract out of the Statute of Frauds',
                        'D': 'Yes, because oral contracts are always enforceable if both parties agree'
                    },
                    'answer': 'C',
                    'tested_rule': 'Part performance exception to Statute of Frauds for land sale contracts',
                    'why_correct': 'The part performance doctrine allows enforcement of an oral land sale contract when the buyer has: (1) taken possession, (2) made valuable improvements, and/or (3) paid part of the purchase price. Here, the buyer did all three, which is sufficient to take the contract outside the Statute of Frauds.',
                    'difficulty': 3
                }
            ],
            'torts': [
                {
                    'id': 'torts_q1',
                    'concept_id': 'torts_negligence',
                    'subject': 'torts',
                    'question': """A driver was speeding on a highway when she noticed a child dart into the road. The driver swerved to avoid the child but struck a pedestrian on the sidewalk. The pedestrian was seriously injured.

If the pedestrian sues the driver for negligence, what is the likely result?""",
                    'options': {
                        'A': 'The driver will prevail because the child was the proximate cause of the injury',
                        'B': 'The driver will prevail because she acted reasonably in an emergency',
                        'C': 'The pedestrian will prevail because the driver was speeding',
                        'D': 'The pedestrian will prevail because drivers owe a duty of care to pedestrians on sidewalks'
                    },
                    'answer': 'C',
                    'tested_rule': 'Negligence per se - violation of statute as breach of duty',
                    'why_correct': 'The driver\'s speeding constitutes negligence per se because it violates a safety statute. Even though the driver faced an emergency, the emergency doctrine does not apply when the defendant\'s own negligence (speeding) created or contributed to the emergency. The speeding was the but-for and proximate cause of the pedestrian\'s injuries.',
                    'difficulty': 3
                },
                {
                    'id': 'torts_q2',
                    'concept_id': 'torts_strict_liability',
                    'subject': 'torts',
                    'question': """A homeowner kept a pet tiger in his backyard, which was enclosed by a 10-foot fence. Despite the homeowner's precautions, the tiger escaped and injured a neighbor. The homeowner had never had any problems with the tiger escaping before.

Is the homeowner liable for the neighbor's injuries?""",
                    'options': {
                        'A': 'No, because the homeowner exercised reasonable care by building a 10-foot fence',
                        'B': 'No, because the tiger had never escaped before',
                        'C': 'Yes, under strict liability for keeping a wild animal',
                        'D': 'Yes, but only if the homeowner was negligent in maintaining the fence'
                    },
                    'answer': 'C',
                    'tested_rule': 'Strict liability for wild animals - no negligence required',
                    'why_correct': 'Owners of wild animals are strictly liable for injuries caused by those animals, regardless of the precautions taken. A tiger is a wild animal by nature, and strict liability applies even if the owner exercised the utmost care. The homeowner\'s due care and the tiger\'s prior good behavior are irrelevant.',
                    'difficulty': 2
                },
                {
                    'id': 'torts_q3',
                    'concept_id': 'torts_intentional_torts',
                    'subject': 'torts',
                    'question': """A defendant pointed an unloaded gun at a plaintiff and said, "I'm going to shoot you." The plaintiff knew the defendant owned several guns and believed the threat was real. The plaintiff suffered severe anxiety as a result.

What is the defendant's strongest defense to a claim of assault?""",
                    'options': {
                        'A': 'The gun was unloaded, so there was no actual threat',
                        'B': 'Words alone cannot constitute an assault',
                        'C': 'The plaintiff\'s fear was unreasonable',
                        'D': 'The defendant had no intent to actually shoot'
                    },
                    'answer': 'D',
                    'tested_rule': 'Assault requires intent to cause apprehension of imminent harmful contact',
                    'why_correct': 'Assault requires the defendant to intend to cause apprehension of imminent harmful or offensive contact. If the defendant only intended to frighten without any intent to follow through, this could negate the required intent. However, this is a weak defense because intent to cause apprehension (even without intent to actually harm) is sufficient. The better answer focuses on the defendant\'s mental state. Note: A is wrong because apparent ability is sufficient; B is wrong because words + act (pointing gun) can be assault; C is wrong because the fear appears reasonable.',
                    'difficulty': 4
                }
            ],
            'evidence': [
                {
                    'id': 'evidence_q1',
                    'concept_id': 'evidence_hearsay',
                    'subject': 'evidence',
                    'question': """At trial, a plaintiff called a witness to testify that the defendant had told the witness: "I ran the red light." The defendant objects on hearsay grounds.

How should the court rule?""",
                    'options': {
                        'A': 'Sustained, because the statement is hearsay',
                        'B': 'Sustained, because the witness has no personal knowledge of the accident',
                        'C': 'Overruled, because the statement is not hearsay',
                        'D': 'Overruled, because the statement falls under the excited utterance exception'
                    },
                    'answer': 'C',
                    'tested_rule': 'Party-opponent admissions are not hearsay under FRE 801(d)(2)',
                    'why_correct': 'A statement by a party-opponent is not hearsay under FRE 801(d)(2). The defendant\'s own statement ("I ran the red light") offered against the defendant is an admission by a party-opponent. It is admissible regardless of whether it was against interest when made and does not require the declarant to have personal knowledge.',
                    'difficulty': 2
                },
                {
                    'id': 'evidence_q2',
                    'concept_id': 'evidence_character',
                    'subject': 'evidence',
                    'question': """In a murder trial, the defendant claims self-defense. The defendant wants to introduce evidence that the victim had a reputation in the community for being violent.

Is this evidence admissible?""",
                    'options': {
                        'A': 'No, because character evidence of the victim is never admissible in criminal cases',
                        'B': 'No, because only specific instances of conduct can prove character',
                        'C': 'Yes, because the defendant may offer evidence of the victim\'s pertinent character trait',
                        'D': 'Yes, but only if the defendant first testifies about the victim\'s violence'
                    },
                    'answer': 'C',
                    'tested_rule': 'FRE 404(a)(2) - Defendant may offer evidence of victim\'s pertinent trait',
                    'why_correct': 'Under FRE 404(a)(2)(B), in a criminal case, the defendant may offer evidence of an alleged victim\'s pertinent character trait. In a self-defense case, the victim\'s violent character is pertinent. Reputation evidence is an acceptable form of proving character under FRE 405(a).',
                    'difficulty': 3
                },
                {
                    'id': 'evidence_q3',
                    'concept_id': 'evidence_privileges',
                    'subject': 'evidence',
                    'question': """An attorney represented a client in a contract dispute. During their meeting, the client confided to the attorney that he had hidden assets to avoid paying the contract judgment if he lost. The opposing party later sought to compel the attorney to testify about this conversation.

Is the attorney required to testify?""",
                    'options': {
                        'A': 'Yes, because the crime-fraud exception applies',
                        'B': 'Yes, because the attorney has a duty to the court',
                        'C': 'No, because the communication is protected by attorney-client privilege',
                        'D': 'No, because the attorney\'s testimony would be hearsay'
                    },
                    'answer': 'C',
                    'tested_rule': 'Attorney-client privilege protects confidential communications',
                    'why_correct': 'The attorney-client privilege protects confidential communications made for the purpose of obtaining legal advice. The crime-fraud exception applies only when the client seeks advice to commit a future crime or fraud. Here, the client was discussing past/ongoing asset concealment, not seeking advice on how to commit fraud. The privilege applies.',
                    'difficulty': 4
                }
            ],
            'constitutional_law': [
                {
                    'id': 'conlaw_q1',
                    'concept_id': 'constitutional_law_equal_protection',
                    'subject': 'constitutional_law',
                    'question': """A state law requires that all applicants for state employment must be U.S. citizens. A lawful permanent resident who was denied employment solely based on this requirement challenges the law.

What level of scrutiny should the court apply?""",
                    'options': {
                        'A': 'Rational basis review',
                        'B': 'Intermediate scrutiny',
                        'C': 'Strict scrutiny',
                        'D': 'No scrutiny because alienage is not a protected classification'
                    },
                    'answer': 'C',
                    'tested_rule': 'Alienage classifications by states are subject to strict scrutiny',
                    'why_correct': 'Alienage is a suspect classification, and state laws discriminating against lawful permanent residents are subject to strict scrutiny. The state must show the law is necessary to achieve a compelling government interest. Note: Federal alienage classifications receive only rational basis review due to Congress\'s plenary power over immigration.',
                    'difficulty': 3
                },
                {
                    'id': 'conlaw_q2',
                    'concept_id': 'constitutional_law_first_amendment',
                    'subject': 'constitutional_law',
                    'question': """A city ordinance prohibits all signs on residential property except "For Sale" signs. A homeowner who wants to display a political sign challenges the ordinance.

Is the ordinance constitutional?""",
                    'options': {
                        'A': 'Yes, because the city has a legitimate interest in aesthetics',
                        'B': 'Yes, because the ordinance applies equally to all political viewpoints',
                        'C': 'No, because it is a content-based restriction on speech',
                        'D': 'No, because residential areas are traditional public forums'
                    },
                    'answer': 'C',
                    'tested_rule': 'Content-based speech restrictions require strict scrutiny',
                    'why_correct': 'The ordinance is content-based because it distinguishes between signs based on their message (allowing "For Sale" signs but not political signs). Content-based restrictions on speech are presumptively unconstitutional and subject to strict scrutiny. The city\'s aesthetic interest does not justify this content discrimination. See City of Ladue v. Gilleo.',
                    'difficulty': 3
                }
            ],
            'criminal_law': [
                {
                    'id': 'crim_q1',
                    'concept_id': 'criminal_law_homicide',
                    'subject': 'criminal_law',
                    'question': """A defendant planned to kill his business partner. He waited outside the partner's office with a loaded gun. When the partner emerged, the defendant shot at him but missed, accidentally killing a bystander.

What is the most serious crime the defendant can be convicted of for the bystander's death?""",
                    'options': {
                        'A': 'Voluntary manslaughter',
                        'B': 'Involuntary manslaughter',
                        'C': 'Second-degree murder',
                        'D': 'First-degree murder'
                    },
                    'answer': 'D',
                    'tested_rule': 'Transferred intent applies to premeditated murder',
                    'why_correct': 'Under the doctrine of transferred intent, the defendant\'s intent to kill the business partner transfers to the bystander who was actually killed. Because the defendant acted with premeditation and deliberation (planned the killing, waited with a loaded gun), the crime is first-degree murder, not merely second-degree murder.',
                    'difficulty': 3
                },
                {
                    'id': 'crim_q2',
                    'concept_id': 'criminal_law_inchoate',
                    'subject': 'criminal_law',
                    'question': """A defendant agreed with two friends to rob a bank. The defendant purchased ski masks and a getaway car. On the day of the planned robbery, the defendant decided not to participate and stayed home. The two friends proceeded with the robbery.

Can the defendant be convicted of conspiracy to commit robbery?""",
                    'options': {
                        'A': 'No, because the defendant withdrew before the robbery occurred',
                        'B': 'No, because the defendant did not actually participate in the robbery',
                        'C': 'Yes, because the defendant agreed and committed an overt act',
                        'D': 'Yes, but only if the friends are also convicted'
                    },
                    'answer': 'C',
                    'tested_rule': 'Conspiracy is complete upon agreement plus overt act; withdrawal is not a defense',
                    'why_correct': 'Conspiracy requires (1) an agreement between two or more persons to commit a crime, and (2) an overt act in furtherance of the conspiracy. The defendant agreed and purchased supplies (overt act). Withdrawal is NOT a defense to conspiracy because the crime is complete once the agreement and overt act occur. Withdrawal only limits liability for subsequent crimes committed by co-conspirators.',
                    'difficulty': 4
                }
            ],
            'civil_procedure': [
                {
                    'id': 'civpro_q1',
                    'concept_id': 'civil_procedure_jurisdiction_and_venue',
                    'subject': 'civil_procedure',
                    'question': """A citizen of State A sued a citizen of State B in federal court in State A, claiming $50,000 in damages for breach of contract. The defendant filed a motion to dismiss for lack of subject matter jurisdiction.

How should the court rule?""",
                    'options': {
                        'A': 'Grant the motion because the amount in controversy does not exceed $75,000',
                        'B': 'Grant the motion because contract cases must be heard in state court',
                        'C': 'Deny the motion because there is complete diversity of citizenship',
                        'D': 'Deny the motion because federal courts have exclusive jurisdiction over contract disputes'
                    },
                    'answer': 'A',
                    'tested_rule': 'Diversity jurisdiction requires amount in controversy exceeding $75,000',
                    'why_correct': '28 U.S.C. § 1332 requires both complete diversity of citizenship AND an amount in controversy exceeding $75,000. While there is complete diversity here (State A citizen vs. State B citizen), the $50,000 claim does not meet the amount in controversy requirement. The motion should be granted.',
                    'difficulty': 2
                },
                {
                    'id': 'civpro_q2',
                    'concept_id': 'civil_procedure_pleadings_and_motions',
                    'subject': 'civil_procedure',
                    'question': """A plaintiff filed a complaint alleging that the defendant was negligent. The complaint stated: "On June 1, the defendant negligently operated his vehicle, causing injury to the plaintiff." The defendant moved to dismiss under Rule 12(b)(6).

How should the court rule?""",
                    'options': {
                        'A': 'Grant the motion because the complaint lacks sufficient factual detail',
                        'B': 'Grant the motion because negligence claims require heightened pleading',
                        'C': 'Deny the motion because the complaint provides fair notice of the claim',
                        'D': 'Deny the motion because Rule 12(b)(6) motions are disfavored'
                    },
                    'answer': 'A',
                    'tested_rule': 'Twombly/Iqbal plausibility pleading standard',
                    'why_correct': 'Under Twombly and Iqbal, a complaint must contain sufficient factual matter to state a claim that is plausible on its face. The complaint here is conclusory - it labels the defendant\'s conduct as "negligent" without factual allegations showing what the defendant did wrong. The court should grant the motion with leave to amend.',
                    'difficulty': 3
                },
                {
                    'id': 'civpro_q3',
                    'concept_id': 'civil_procedure_erie',
                    'subject': 'civil_procedure',
                    'question': """A plaintiff from State A filed a diversity action against a defendant from State B in federal court in State B. State B has a statute requiring plaintiffs in negligence cases to file an affidavit from a medical expert with the complaint. Federal Rule of Civil Procedure 8 requires only a short and plain statement of the claim.

Should the federal court apply the state affidavit requirement?""",
                    'options': {
                        'A': 'Yes, because it is a substantive state law that affects the outcome',
                        'B': 'Yes, because federal courts must always follow state procedural rules',
                        'C': 'No, because Federal Rule 8 directly addresses the matter and is valid',
                        'D': 'No, because the Rules of Decision Act requires federal procedure in federal court'
                    },
                    'answer': 'C',
                    'tested_rule': 'Erie doctrine - Hanna v. Plumer analysis for Federal Rules',
                    'why_correct': 'Under Hanna v. Plumer, when a Federal Rule of Civil Procedure directly conflicts with state law, the Federal Rule applies if it is valid under the Rules Enabling Act. Federal Rule 8 directly addresses pleading requirements and is a valid procedural rule. The state affidavit requirement conflicts with Rule 8, so the Federal Rule controls.',
                    'difficulty': 4
                }
            ],
            'real_property': [
                {
                    'id': 'property_q1',
                    'concept_id': 'real_property_recording',
                    'subject': 'real_property',
                    'question': """O conveyed Blackacre to A by warranty deed on January 1. A did not record. On February 1, O conveyed Blackacre to B by warranty deed. B had no actual knowledge of the prior conveyance to A. B recorded immediately. The jurisdiction has a notice recording statute.

Who owns Blackacre?""",
                    'options': {
                        'A': 'A, because A received the first conveyance',
                        'B': 'A, because B had constructive notice from A\'s possession',
                        'C': 'B, because B was a subsequent bona fide purchaser without notice who recorded first',
                        'D': 'B, because the warranty deed to A was void'
                    },
                    'answer': 'C',
                    'tested_rule': 'Notice recording statute - BFP without notice prevails',
                    'why_correct': 'Under a notice statute, a subsequent bona fide purchaser (BFP) who takes without notice of the prior conveyance prevails over the prior grantee, regardless of who records first. B had no actual knowledge, and since A did not record, B had no constructive (record) notice. B qualifies as a BFP and owns Blackacre.',
                    'difficulty': 3
                },
                {
                    'id': 'property_q2',
                    'concept_id': 'real_property_easements',
                    'subject': 'real_property',
                    'question': """A owned two adjacent lots. A built a house on Lot 1 with a driveway that crossed Lot 2 to reach the public road. A then sold Lot 2 to B by a deed that made no mention of the driveway. The driveway was clearly visible.

Does A have an easement to use the driveway across Lot 2?""",
                    'options': {
                        'A': 'No, because the deed made no mention of the easement',
                        'B': 'No, because easements must be created in writing',
                        'C': 'Yes, by an easement implied from prior existing use',
                        'D': 'Yes, by an easement by necessity'
                    },
                    'answer': 'C',
                    'tested_rule': 'Easement implied from prior existing use (quasi-easement)',
                    'why_correct': 'An easement implied from prior existing use arises when: (1) there was common ownership, (2) a quasi-easement existed during unity of ownership, (3) the use was apparent and continuous, and (4) the easement is reasonably necessary for enjoyment of the dominant estate. Here, A used the driveway while owning both lots, it was visible, and it provides access to the road. All elements are met.',
                    'difficulty': 3
                },
                {
                    'id': 'property_q3',
                    'concept_id': 'real_property_rap',
                    'subject': 'real_property',
                    'question': """A testator\'s will devised property "to my daughter for life, then to my daughter\'s children who reach age 25." At the testator\'s death, the daughter was alive with one child, age 10.

Is the gift to the daughter\'s children valid under the Rule Against Perpetuities?""",
                    'options': {
                        'A': 'Yes, because the daughter is a life in being who validates the interest',
                        'B': 'Yes, because there is already a child who could reach 25 within the perpetuities period',
                        'C': 'No, because a child could be born who reaches 25 more than 21 years after the daughter dies',
                        'D': 'No, because the interest is contingent on surviving the daughter'
                    },
                    'answer': 'C',
                    'tested_rule': 'Rule Against Perpetuities - "what might happen" test',
                    'why_correct': 'Under the RAP, we must consider what "might happen," not what probably will happen. The daughter could have another child after the testator\'s death, then die, and that afterborn child might not reach 25 until more than 21 years after the daughter\'s death. Since there is any possibility the interest might vest too remotely, the gift to the children is void under the RAP.',
                    'difficulty': 5
                }
            ],
            'criminal_procedure': [
                {
                    'id': 'crimpro_q1',
                    'concept_id': 'criminal_procedure_search',
                    'subject': 'criminal_procedure',
                    'question': """Police officers obtained a valid warrant to search a suspect\'s home for illegal drugs. While executing the warrant, an officer noticed a stolen television in plain view in the living room.

May the officer seize the television?""",
                    'options': {
                        'A': 'No, because the warrant only authorized a search for drugs',
                        'B': 'No, because seizing the television exceeds the scope of the warrant',
                        'C': 'Yes, under the plain view doctrine',
                        'D': 'Yes, because any evidence of crime may be seized during a warranted search'
                    },
                    'answer': 'C',
                    'tested_rule': 'Plain view doctrine during lawful search',
                    'why_correct': 'Under the plain view doctrine, police may seize evidence without a warrant if: (1) the officer is lawfully present, (2) the item is in plain view, and (3) the incriminating nature of the item is immediately apparent. Here, the officers were lawfully in the home executing a valid warrant, the TV was in plain view, and its stolen nature was immediately apparent. Seizure is valid.',
                    'difficulty': 2
                },
                {
                    'id': 'crimpro_q2',
                    'concept_id': 'criminal_procedure_miranda',
                    'subject': 'criminal_procedure',
                    'question': """Police arrested a suspect for robbery and gave proper Miranda warnings. The suspect said, "I want a lawyer." The police stopped questioning. Two hours later, a different officer approached the suspect in his cell about an unrelated murder and began asking questions without repeating Miranda warnings. The suspect confessed to the murder.

Is the murder confession admissible?""",
                    'options': {
                        'A': 'Yes, because the murder investigation was separate from the robbery',
                        'B': 'Yes, because two hours had passed since the request for counsel',
                        'C': 'No, because police must wait 14 days before reinitiating questioning',
                        'D': 'No, because once a suspect invokes the right to counsel, police cannot reinitiate questioning about any crime'
                    },
                    'answer': 'D',
                    'tested_rule': 'Edwards v. Arizona - invocation of right to counsel',
                    'why_correct': 'Under Edwards v. Arizona, once a suspect invokes the right to counsel, all police-initiated interrogation must cease until counsel is provided or the suspect initiates further communication. This protection applies to all crimes, not just the crime for which the suspect was arrested. Arizona v. Roberson extended Edwards to bar questioning about unrelated crimes.',
                    'difficulty': 4
                },
                {
                    'id': 'crimpro_q3',
                    'concept_id': 'criminal_procedure_exclusionary',
                    'subject': 'criminal_procedure',
                    'question': """Police conducted an illegal search of a defendant\'s home and found evidence of drug trafficking. At trial, the prosecution did not offer the illegally seized evidence in its case-in-chief. However, when the defendant testified that he had never possessed drugs, the prosecution sought to use the seized evidence to impeach his testimony.

Should the court allow the evidence for impeachment purposes?""",
                    'options': {
                        'A': 'No, because illegally seized evidence can never be used for any purpose',
                        'B': 'No, because using the evidence for impeachment rewards police misconduct',
                        'C': 'Yes, because the exclusionary rule does not apply to impeachment of defendant\'s testimony',
                        'D': 'Yes, because the defendant opened the door by testifying'
                    },
                    'answer': 'C',
                    'tested_rule': 'Exclusionary rule exception for impeachment (Harris/Walder)',
                    'why_correct': 'Under Harris v. New York and subsequent cases, illegally obtained evidence that is inadmissible in the prosecution\'s case-in-chief may still be used to impeach the defendant\'s testimony. The exclusionary rule\'s purpose of deterring police misconduct is not served by allowing defendants to commit perjury. However, the evidence can only impeach the defendant, not other witnesses.',
                    'difficulty': 4
                }
            ],
            'professional_responsibility': [
                {
                    'id': 'pr_q1',
                    'concept_id': 'professional_responsibility_conflicts',
                    'subject': 'professional_responsibility',
                    'question': """Attorney represents Client A in a breach of contract action against Client B. Client B then asks Attorney to represent her in an unrelated personal injury case against a third party.

May Attorney represent Client B in the personal injury case?""",
                    'options': {
                        'A': 'Yes, because the matters are unrelated',
                        'B': 'Yes, if both clients give informed consent confirmed in writing',
                        'C': 'No, because Attorney cannot represent opposing parties in any matter',
                        'D': 'No, unless Attorney withdraws from representing Client A'
                    },
                    'answer': 'B',
                    'tested_rule': 'Model Rule 1.7 - Concurrent conflicts of interest',
                    'why_correct': 'Under Model Rule 1.7, representing Client B while suing her on behalf of Client A creates a concurrent conflict because there is a significant risk that representation of one client will be materially limited by the lawyer\'s responsibilities to the other. However, this conflict is waivable with informed consent, confirmed in writing, from both clients, if the lawyer reasonably believes she can competently represent both.',
                    'difficulty': 3
                },
                {
                    'id': 'pr_q2',
                    'concept_id': 'professional_responsibility_confidentiality',
                    'subject': 'professional_responsibility',
                    'question': """Client told Attorney in confidence that Client plans to lie on the witness stand tomorrow. Attorney has tried to persuade Client not to testify falsely, but Client refuses to change his mind.

What must Attorney do?""",
                    'options': {
                        'A': 'Keep the information confidential and allow Client to testify',
                        'B': 'Inform the court that Client intends to commit perjury',
                        'C': 'Withdraw from representation if permitted, or take remedial measures',
                        'D': 'Refuse to call Client as a witness but keep the information confidential'
                    },
                    'answer': 'C',
                    'tested_rule': 'Model Rule 3.3 - Candor toward the tribunal',
                    'why_correct': 'Under Model Rule 3.3, a lawyer must take reasonable remedial measures when the lawyer knows the client intends to offer false evidence. The lawyer should first try to persuade the client not to testify falsely. If that fails, the lawyer may seek to withdraw. If withdrawal is not permitted or does not solve the problem, the lawyer must disclose to the tribunal. Duties of candor to the tribunal override confidentiality.',
                    'difficulty': 4
                }
            ],
            'corporations': [
                {
                    'id': 'corp_q1',
                    'concept_id': 'corporations_fiduciary_duties',
                    'subject': 'corporations',
                    'question': """The board of directors of a corporation approved a merger that would benefit the CEO personally but was arguably not in the best interests of the shareholders. A shareholder brings a derivative suit challenging the merger.

What standard of review will the court apply?""",
                    'options': {
                        'A': 'Business judgment rule - presumes directors acted in good faith',
                        'B': 'Entire fairness standard - directors must prove fair dealing and fair price',
                        'C': 'Rational basis review - any rational business purpose is sufficient',
                        'D': 'Strict scrutiny - directors must prove compelling necessity'
                    },
                    'answer': 'B',
                    'tested_rule': 'Entire fairness standard applies when directors have conflicts of interest',
                    'why_correct': 'When directors have a personal interest in a transaction (here, the CEO\'s benefit), the business judgment rule does not apply. Instead, the court applies the entire fairness standard, which requires the directors to prove both fair dealing (proper process) and fair price. The burden shifts to the conflicted directors to prove fairness.',
                    'difficulty': 4
                },
                {
                    'id': 'corp_q2',
                    'concept_id': 'corporations_piercing_veil',
                    'subject': 'corporations',
                    'question': """A sole shareholder formed a corporation and deposited the minimum required capital. The shareholder never held board meetings, commingled personal and corporate funds, and used corporate assets for personal expenses. The corporation became insolvent.

Can creditors pierce the corporate veil to reach the shareholder's personal assets?""",
                    'options': {
                        'A': 'No, because the corporation was properly formed',
                        'B': 'No, because creditors assumed the risk of dealing with a corporation',
                        'C': 'Yes, because the shareholder disregarded the corporate form',
                        'D': 'Yes, but only for tort creditors, not contract creditors'
                    },
                    'answer': 'C',
                    'tested_rule': 'Piercing the corporate veil - alter ego/instrumentality doctrine',
                    'why_correct': 'Courts will pierce the corporate veil when the shareholder has: (1) disregarded corporate formalities (no meetings), (2) commingled funds, and (3) used the corporation as an alter ego for personal purposes. Here, all three factors are present. Undercapitalization alone is usually not sufficient, but combined with these other factors, piercing is appropriate.',
                    'difficulty': 3
                },
                {
                    'id': 'corp_q3',
                    'concept_id': 'corporations_shareholder_rights',
                    'subject': 'corporations',
                    'question': """A shareholder wants to inspect the corporation's books and records to investigate suspected mismanagement by the board. The shareholder owns 100 shares of a company with 10 million shares outstanding.

Does the shareholder have a right to inspect the books and records?""",
                    'options': {
                        'A': 'No, because the shareholder owns less than 5% of shares',
                        'B': 'No, because inspection rights are limited to creditors',
                        'C': 'Yes, if the shareholder has a proper purpose related to the shareholder\'s interest',
                        'D': 'Yes, shareholders have an absolute right to inspect at any time'
                    },
                    'answer': 'C',
                    'tested_rule': 'Shareholder inspection rights require proper purpose',
                    'why_correct': 'Under corporate law, shareholders have a right to inspect books and records if they have a proper purpose reasonably related to their interest as shareholders. Investigating mismanagement is a proper purpose. The percentage of ownership is not determinative; even small shareholders have this right if the purpose is proper.',
                    'difficulty': 3
                }
            ],
            'wills_trusts_estates': [
                {
                    'id': 'wte_q1',
                    'concept_id': 'wills_execution',
                    'subject': 'wills_trusts_estates',
                    'question': """A testator typed a will on his computer, printed it, and signed it at the bottom. His neighbor witnessed the signing but did not sign the document. The testator then showed the will to a friend who signed as a witness two days later without the testator present.

Is this a valid will under traditional formalities?""",
                    'options': {
                        'A': 'Yes, because it was signed by the testator and two witnesses',
                        'B': 'Yes, because substantial compliance with formalities is sufficient',
                        'C': 'No, because the witnesses did not sign in the testator\'s presence',
                        'D': 'No, because the will was not handwritten'
                    },
                    'answer': 'C',
                    'tested_rule': 'Will execution requires witnesses to sign in testator\'s presence',
                    'why_correct': 'Under traditional will formalities, witnesses must: (1) witness the testator\'s signature or acknowledgment, and (2) sign in the testator\'s presence (and often in each other\'s presence). Here, the second witness signed without the testator present, violating the presence requirement. The will fails for improper execution.',
                    'difficulty': 3
                },
                {
                    'id': 'wte_q2',
                    'concept_id': 'wills_revocation',
                    'subject': 'wills_trusts_estates',
                    'question': """A testator executed a valid will leaving everything to her son. Later, she executed a second valid will that stated "I revoke all prior wills" and left everything to her daughter. The testator then tore up the second will with the intent to revive the first will.

What is the effect on the testator's estate?""",
                    'options': {
                        'A': 'The son takes under the first will, which is revived',
                        'B': 'The daughter takes under the second will, which remains valid',
                        'C': 'The estate passes by intestacy because no valid will exists',
                        'D': 'The son and daughter share equally under both wills'
                    },
                    'answer': 'C',
                    'tested_rule': 'Dependent relative revocation and will revival',
                    'why_correct': 'The first will was revoked by the second will\'s express revocation clause. Under the majority rule, destroying a later will does NOT automatically revive an earlier revoked will. Revival requires re-execution or a codicil. Since the first will was revoked and the second was destroyed, the testator died without a valid will, so the estate passes by intestacy.',
                    'difficulty': 4
                },
                {
                    'id': 'wte_q3',
                    'concept_id': 'trusts_creation',
                    'subject': 'wills_trusts_estates',
                    'question': """A settlor conveyed property "to Trustee, in trust, to distribute income and principal as Trustee sees fit among my descendants." The trust instrument named no specific beneficiaries and gave the trustee complete discretion.

Is this a valid trust?""",
                    'options': {
                        'A': 'No, because the beneficiaries are not sufficiently identified',
                        'B': 'No, because a trust cannot give the trustee unlimited discretion',
                        'C': 'Yes, because "descendants" is a sufficiently definite class',
                        'D': 'Yes, because trusts are favored and courts will supply missing terms'
                    },
                    'answer': 'C',
                    'tested_rule': 'Trust beneficiaries must be identifiable or ascertainable',
                    'why_correct': '"Descendants" is a sufficiently definite class that can be ascertained by objective criteria (blood relationship). The trust is valid even though specific individuals are not named, as long as the class is definable. Trustee discretion in distributions does not invalidate the trust if the beneficiary class is identifiable.',
                    'difficulty': 3
                }
            ],
            'family_law': [
                {
                    'id': 'family_q1',
                    'concept_id': 'family_law_marital_property',
                    'subject': 'family_law',
                    'question': """During marriage, Wife received an inheritance of $100,000 which she deposited into a joint bank account with Husband. The couple later divorces in an equitable distribution state.

How should the inheritance be treated in the divorce?""",
                    'options': {
                        'A': 'Separate property because inheritances are always separate',
                        'B': 'Marital property because it was deposited into a joint account',
                        'C': 'Separate property but Husband has a claim for reimbursement',
                        'D': 'Split 50-50 as community property'
                    },
                    'answer': 'B',
                    'tested_rule': 'Transmutation of separate property into marital property',
                    'why_correct': 'While inheritances are typically separate property, depositing separate property into a joint marital account can transmute it into marital property through commingling. By depositing the inheritance into the joint account, Wife demonstrated intent to share it with Husband, converting it to marital property subject to equitable distribution.',
                    'difficulty': 3
                },
                {
                    'id': 'family_q2',
                    'concept_id': 'family_law_child_custody',
                    'subject': 'family_law',
                    'question': """Parents are divorcing and cannot agree on custody of their 8-year-old child. Father lives in the family home in good school district. Mother plans to move to another state for a job opportunity. Both parents have been actively involved in parenting.

What standard will the court apply in determining custody?""",
                    'options': {
                        'A': 'The parent who can provide greater financial support',
                        'B': 'The best interests of the child',
                        'C': 'The preference of the child regardless of age',
                        'D': 'Automatic preference for the mother for children under 10'
                    },
                    'answer': 'B',
                    'tested_rule': 'Best interests of the child standard',
                    'why_correct': 'Courts apply the "best interests of the child" standard when determining custody. This includes factors such as: stability, each parent\'s relationship with the child, the child\'s adjustment to home/school/community, and each parent\'s ability to meet the child\'s needs. There is no automatic preference based on gender, and a child\'s preference is only one factor (weighted by age and maturity).',
                    'difficulty': 2
                },
                {
                    'id': 'family_q3',
                    'concept_id': 'family_law_child_support',
                    'subject': 'family_law',
                    'question': """Father owes $50,000 in past-due child support. He files for Chapter 7 bankruptcy seeking to discharge all debts.

Is the child support obligation dischargeable in bankruptcy?""",
                    'options': {
                        'A': 'Yes, because Chapter 7 discharges all unsecured debts',
                        'B': 'Yes, but only the portion over $25,000',
                        'C': 'No, because domestic support obligations are non-dischargeable',
                        'D': 'No, unless the custodial parent consents to discharge'
                    },
                    'answer': 'C',
                    'tested_rule': 'Domestic support obligations are non-dischargeable in bankruptcy',
                    'why_correct': 'Under 11 U.S.C. § 523(a)(5), domestic support obligations (child support, alimony) are non-dischargeable in bankruptcy. This applies in both Chapter 7 and Chapter 13. The policy is to protect children and former spouses who depend on these payments. Father remains obligated for the full $50,000.',
                    'difficulty': 2
                }
            ],
            'secured_transactions': [
                {
                    'id': 'secured_q1',
                    'concept_id': 'secured_transactions_attachment',
                    'subject': 'secured_transactions',
                    'question': """A lender made a loan to a borrower and took a security interest in the borrower's inventory. The security agreement was signed by the borrower and described the collateral as "all inventory." The lender did not file a financing statement.

Is the security interest enforceable against the borrower?""",
                    'options': {
                        'A': 'No, because the lender failed to perfect by filing',
                        'B': 'No, because "all inventory" is not a sufficient description',
                        'C': 'Yes, because attachment only requires agreement, value, and rights in collateral',
                        'D': 'Yes, but only if the lender takes possession of the inventory'
                    },
                    'answer': 'C',
                    'tested_rule': 'UCC Article 9 attachment requirements',
                    'why_correct': 'A security interest attaches (becomes enforceable against the debtor) when: (1) value has been given, (2) the debtor has rights in the collateral, and (3) the debtor has authenticated a security agreement describing the collateral. Filing is required for perfection (priority against third parties), not attachment. "All inventory" is a sufficient description for the security agreement.',
                    'difficulty': 3
                },
                {
                    'id': 'secured_q2',
                    'concept_id': 'secured_transactions_priority',
                    'subject': 'secured_transactions',
                    'question': """Bank A filed a financing statement covering Debtor's equipment on March 1. Bank B filed a financing statement covering the same equipment on March 15 and made its loan on that date. Bank A did not make its loan until April 1.

Who has priority in the equipment?""",
                    'options': {
                        'A': 'Bank A, because it filed first',
                        'B': 'Bank B, because it was the first to give value',
                        'C': 'Bank B, because Bank A\'s filing was ineffective without a loan',
                        'D': 'They share pro rata because both perfected'
                    },
                    'answer': 'A',
                    'tested_rule': 'First-to-file-or-perfect rule under UCC 9-322',
                    'why_correct': 'Under UCC 9-322(a)(1), priority among perfected security interests goes to the first to file OR perfect. A financing statement can be filed before the security interest attaches. Bank A filed first on March 1. Even though Bank A\'s security interest did not attach until April 1, Bank A has priority because it filed first. This is called "advance filing."',
                    'difficulty': 4
                },
                {
                    'id': 'secured_q3',
                    'concept_id': 'secured_transactions_pmsi',
                    'subject': 'secured_transactions',
                    'question': """Debtor granted Bank a security interest in "all equipment, now owned or after-acquired." Bank perfected by filing. Later, Seller sold equipment to Debtor on credit, retaining a security interest. Seller filed within 20 days of Debtor receiving possession.

Who has priority in the new equipment?""",
                    'options': {
                        'A': 'Bank, because it filed first and has an after-acquired property clause',
                        'B': 'Bank, because Seller\'s filing was late',
                        'C': 'Seller, because it has a purchase money security interest that was timely perfected',
                        'D': 'Seller, but only if Bank had actual knowledge of the sale'
                    },
                    'answer': 'C',
                    'tested_rule': 'PMSI superpriority in equipment under UCC 9-324(a)',
                    'why_correct': 'A purchase money security interest (PMSI) in equipment has priority over a conflicting security interest if the PMSI is perfected within 20 days after the debtor receives possession. Seller has a PMSI (it sold the goods on credit) and filed within the 20-day grace period. Seller\'s PMSI has superpriority over Bank\'s earlier-filed after-acquired property interest.',
                    'difficulty': 4
                }
            ]
        }

    def start_session(self, subject: str = "contracts") -> str:
        """Start interactive session with pedagogy features"""
        self.state = LearningState()  # Reset state
        self.state.current_subject = subject
        self.state.session_started = True
        self.state.last_interaction = datetime.now()
        self.state.session_id = generate_id(f"{subject}_{datetime.now().isoformat()}")

        welcome = f"""
================================================================================
           INTERACTIVE BAR EXAM TUTOR - Advanced Pedagogy Mode
================================================================================

Subject: {subject.upper()}
Session ID: {self.state.session_id[:8]}

This session uses evidence-based learning techniques:
  - Spaced Repetition (SM-2 algorithm)
  - Confidence Calibration
  - Elaborative Interrogation
  - Socratic Dialogue for wrong answers

Commands:
  'practice' or 'quiz'  - Start answering MBE-style questions
  'explain [concept]'   - Get detailed concept explanations
  'review'              - See concepts due for spaced repetition
  'progress'            - View your session stats
  'study plan'          - Get personalized study recommendations
  'help'                - Show all commands
  'quit'                - End session

Ready to master {subject.replace('_', ' ').title()}? Type 'practice' to begin!
================================================================================
"""
        self.conversation_history.append({"role": "assistant", "content": welcome})
        return welcome

    def process_input(self, user_input: str) -> str:
        """Process user input with advanced pedagogy state machine"""
        self.state.last_interaction = datetime.now()
        original_input = user_input
        user_input = user_input.strip()

        # Handle answer input when awaiting
        if self.state.awaiting_answer:
            return self._process_answer(user_input.upper())

        # Handle confidence rating when awaiting
        if self.state.awaiting_confidence:
            return self._process_confidence(user_input)

        # Handle elaboration mode
        if self.state.elaboration_mode:
            self.state.elaboration_mode = False
            return self._continue_practice()

        # Normal command processing
        user_input_lower = user_input.lower()

        if user_input_lower in ['quit', 'exit', 'end']:
            return self._end_session()
        elif user_input_lower in ['help', 'h', '?']:
            return self._show_help()
        elif user_input_lower in ['progress', 'stats']:
            return self._show_progress()
        elif user_input_lower in ['practice', 'quiz', 'start', 'next']:
            return self._start_practice()
        elif user_input_lower == 'review':
            return self._show_review_queue()
        elif user_input_lower == 'study plan':
            return self._show_study_plan()
        elif 'explain' in user_input_lower:
            return self._explain_concept(original_input)
        else:
            return f"Command not recognized: '{user_input}'. Type 'help' for available commands."

    def _start_practice(self) -> str:
        """Start a practice question with pedagogical features"""
        subject = self.state.current_subject

        if subject not in self.question_bank or not self.question_bank[subject]:
            return f"No questions available for {subject}. Try 'explain [concept]' instead."

        # Select question based on spaced repetition if available
        questions = self.question_bank[subject]

        # Prioritize questions for concepts due for review
        due_concepts = [c.concept_id for c in self.bar_tutor.get_spaced_repetition_queue(subject)]

        # Find a question matching due concepts, or pick randomly
        selected = None
        for q in questions:
            if q['concept_id'] in due_concepts:
                selected = q
                break

        if not selected:
            selected = random.choice(questions)

        self.state.current_question = selected
        self.state.awaiting_answer = True
        self.state.current_concept = selected['concept_id']

        # Format question
        options_text = "\n".join([f"   {k}. {v}" for k, v in selected['options'].items()])

        return f"""
================================================================================
QUESTION {self.state.questions_asked + 1} | {subject.upper()} | Difficulty: {'*' * selected['difficulty']}
================================================================================

{selected['question']}

{options_text}

--------------------------------------------------------------------------------
Enter your answer (A, B, C, or D):
"""

    def _process_answer(self, answer: str) -> str:
        """Process answer and provide pedagogical feedback"""
        if answer not in ['A', 'B', 'C', 'D']:
            return "Please enter A, B, C, or D:"

        self.state.awaiting_answer = False
        question = self.state.current_question
        correct_answer = question['answer']
        is_correct = answer == correct_answer

        self.state.questions_asked += 1
        if is_correct:
            self.state.correct_answers += 1

        # Store response for tracking
        self.state.user_responses.append({
            'question_id': question['id'],
            'user_answer': answer,
            'correct': is_correct,
            'timestamp': datetime.now().isoformat()
        })

        # Now ask for confidence rating
        self.state.awaiting_confidence = True

        result_icon = "CORRECT" if is_correct else "INCORRECT"
        result_emoji = "+" if is_correct else "X"

        return f"""
[{result_emoji}] {result_icon}!

Your answer: {answer}
Correct answer: {correct_answer}

Before we continue, rate your confidence in your answer:
   1 = Wild guess
   2 = Somewhat unsure
   3 = Moderately confident
   4 = Quite confident
   5 = Completely certain

Enter confidence rating (1-5):
"""

    def _process_confidence(self, rating_str: str) -> str:
        """Process confidence rating and provide calibration feedback"""
        try:
            confidence = int(rating_str)
            if confidence < 1 or confidence > 5:
                return "Please enter a number from 1 to 5:"
        except ValueError:
            return "Please enter a number from 1 to 5:"

        self.state.awaiting_confidence = False
        self.state.confidence_ratings.append(confidence)

        question = self.state.current_question
        last_response = self.state.user_responses[-1]
        is_correct = last_response['correct']
        user_answer = last_response['user_answer']

        # Update concept mastery with confidence
        self.bar_tutor.update_concept_mastery(
            question['concept_id'],
            is_correct,
            confidence
        )

        # Get confidence calibration feedback
        calibration = self.bar_tutor.get_confidence_calibration(
            question, user_answer, confidence, is_correct
        )

        # Build detailed feedback
        output = []
        output.append("=" * 80)
        output.append("EXPLANATION")
        output.append("=" * 80)
        output.append("")
        output.append(f"Tested Rule: {question['tested_rule']}")
        output.append("")
        output.append(f"Why {question['answer']} is correct:")
        output.append(question['why_correct'])
        output.append("")

        # Add calibration feedback if available
        if calibration.get('calibration_feedback'):
            output.append("-" * 80)
            output.append("CONFIDENCE CALIBRATION")
            output.append("-" * 80)
            output.append(calibration['calibration_feedback'])
            output.append("")

        # If wrong, add Socratic dialogue
        if not is_correct:
            output.append("-" * 80)
            output.append("SOCRATIC REFLECTION")
            output.append("-" * 80)

            socratic = self.bar_tutor.get_socratic_dialogue(question, user_answer)
            output.append(f"Key insight: {socratic['key_insight']}")
            output.append("")
            output.append("Consider these questions:")
            for i, step in enumerate(socratic['dialogue_steps'][:2], 1):
                output.append(f"  {i}. {step['question']}")
            output.append("")

            # Add remediation
            if socratic.get('remediation_strategy'):
                output.append("Suggested remediation:")
                for strategy in socratic['remediation_strategy'][:2]:
                    output.append(f"  - {strategy}")
                output.append("")

        # Get elaborative feedback (for both correct and incorrect)
        elaboration = self.bar_tutor.get_elaborative_feedback(question, user_answer, is_correct)
        if elaboration.get('interrogation_prompts'):
            output.append("-" * 80)
            output.append("DEEP LEARNING PROMPTS")
            output.append("-" * 80)
            output.append("To strengthen retention, consider:")
            for prompt in elaboration['interrogation_prompts'][:2]:
                output.append(f"  - {prompt}")
            output.append("")

        output.append("=" * 80)
        output.append("")
        output.append("Press Enter to continue to the next question, or type 'quit' to end.")

        self.state.elaboration_mode = True

        return "\n".join(output)

    def _continue_practice(self) -> str:
        """Continue to next practice question"""
        return self._start_practice()

    def _show_review_queue(self) -> str:
        """Show concepts due for spaced repetition review"""
        due_concepts = self.bar_tutor.get_spaced_repetition_queue(self.state.current_subject)

        if not due_concepts:
            return f"""
No concepts due for review in {self.state.current_subject}!
All caught up with spaced repetition.

Type 'practice' to continue learning new material.
"""

        output = [
            "=" * 80,
            f"SPACED REPETITION REVIEW QUEUE - {self.state.current_subject.upper()}",
            "=" * 80,
            "",
            f"{len(due_concepts)} concepts due for review:",
            ""
        ]

        for i, concept in enumerate(due_concepts, 1):
            days_overdue = ""
            if concept.last_reviewed:
                days = (datetime.now() - concept.last_reviewed).days
                days_overdue = f" (last reviewed {days} days ago)"

            mastery_bar = "*" * int(concept.mastery_level * 10)
            output.append(f"{i}. {concept.name}")
            output.append(f"   Mastery: [{mastery_bar:<10}] {concept.mastery_level:.0%}{days_overdue}")

        output.append("")
        output.append("Type 'practice' to start reviewing these concepts.")
        output.append("=" * 80)

        return "\n".join(output)

    def _show_study_plan(self) -> str:
        """Show personalized study plan"""
        plan = self.bar_tutor.generate_study_plan()

        output = [
            "=" * 80,
            "PERSONALIZED STUDY PLAN",
            "=" * 80,
            "",
            f"Weeks until exam: {plan['total_weeks']}",
            f"Focus subjects: {', '.join(plan['focus_subjects']) or 'All subjects'}",
            "",
            "Recommended Daily Structure:",
        ]

        for session_name, session in plan['daily_structure'].items():
            output.append(f"  {session_name.replace('_', ' ').title()}:")
            output.append(f"    Duration: {session['duration']} minutes")
            output.append(f"    Mode: {session['mode'].value}")
            output.append(f"    Strategy: {session['strategy'].value}")
            output.append("")

        if plan.get('adaptive_goals'):
            goals = plan['adaptive_goals']
            output.append("Adaptive Goals:")
            output.append(f"  - Target accuracy: {goals['accuracy_target']:.0%}")
            output.append(f"  - Target time per question: {goals['speed_target']} seconds")
            output.append(f"  - Weak subject improvement: {goals['weak_subject_improvement']}")
            output.append("")

        output.append("=" * 80)
        return "\n".join(output)

    def _show_help(self) -> str:
        """Show enhanced help menu"""
        return """
================================================================================
AVAILABLE COMMANDS
================================================================================

PRACTICE COMMANDS:
  practice, quiz     - Start answering MBE-style questions
  next              - Go to next question
  review            - See concepts due for spaced repetition

LEARNING COMMANDS:
  explain [concept] - Get detailed explanation of a concept
  study plan        - Get personalized study recommendations

PROGRESS COMMANDS:
  progress, stats   - View session statistics
  help              - Show this menu

SESSION COMMANDS:
  quit, exit        - End the current session

AVAILABLE SUBJECTS:
  contracts         constitutional_law    criminal_law
  torts             evidence              civil_procedure
  real_property     criminal_procedure    professional_responsibility
  corporations      wills_trusts_estates  family_law

================================================================================
"""

    def _show_progress(self) -> str:
        """Show enhanced progress with calibration data"""
        accuracy = self.state.correct_answers / max(self.state.questions_asked, 1)

        # Calculate confidence metrics
        avg_confidence = sum(self.state.confidence_ratings) / max(len(self.state.confidence_ratings), 1)

        output = [
            "=" * 80,
            "SESSION PROGRESS",
            "=" * 80,
            "",
            f"Subject: {self.state.current_subject.replace('_', ' ').title()}",
            f"Session ID: {self.state.session_id[:8] if self.state.session_id else 'N/A'}",
            "",
            "Performance:",
            f"  Questions Answered: {self.state.questions_asked}",
            f"  Correct Answers: {self.state.correct_answers}",
            f"  Accuracy: {accuracy:.1%}",
            "",
        ]

        if self.state.confidence_ratings:
            output.append("Confidence Calibration:")
            output.append(f"  Average Confidence: {avg_confidence:.1f}/5")

            # Analyze calibration
            high_conf_correct = sum(
                1 for i, r in enumerate(self.state.user_responses)
                if i < len(self.state.confidence_ratings)
                and self.state.confidence_ratings[i] >= 4
                and r['correct']
            )
            high_conf_total = sum(
                1 for c in self.state.confidence_ratings if c >= 4
            )

            if high_conf_total > 0:
                high_conf_acc = high_conf_correct / high_conf_total
                output.append(f"  High-Confidence Accuracy: {high_conf_acc:.1%}")

                if high_conf_acc < 0.8:
                    output.append("  [!] Calibration Alert: High confidence but lower accuracy")
            output.append("")

        output.append("Cognitive Strategies Used This Session:")
        strategies = list(set(self.state.cognitive_strategies_used)) or ["Retrieval Practice", "Spaced Repetition"]
        for s in strategies:
            output.append(f"  - {s}")

        output.append("")
        output.append("=" * 80)

        return "\n".join(output)

    def _explain_concept(self, user_input: str) -> str:
        """Enhanced concept explanation with pedagogical context"""
        parts = user_input.split()
        if len(parts) < 2:
            return "Please specify a concept, e.g., 'explain consideration'"

        concept_query = ' '.join(parts[1:]).lower()

        # Try to find matching concept
        for concept in self.bar_tutor.kg.nodes.values():
            if concept_query in concept.name.lower() or concept_query in concept.concept_id:
                # Get related questions for context
                related_questions = []
                if concept.subject in self.question_bank:
                    related_questions = [
                        q for q in self.question_bank[concept.subject]
                        if q['concept_id'] == concept.concept_id
                    ]

                output = [
                    "=" * 80,
                    f"{concept.name.upper()}",
                    "=" * 80,
                    "",
                    f"Subject: {concept.subject.replace('_', ' ').title()}",
                    f"Difficulty: {'*' * concept.difficulty} ({concept.difficulty}/5)",
                    f"Mastery Level: {concept.mastery_level:.0%}",
                    "",
                ]

                if concept.rule_statement:
                    output.append("RULE STATEMENT:")
                    output.append(f"  {concept.rule_statement}")
                    output.append("")

                if concept.elements:
                    output.append("ELEMENTS:")
                    for i, elem in enumerate(concept.elements, 1):
                        output.append(f"  {i}. {elem}")
                    output.append("")

                if concept.exceptions:
                    output.append("EXCEPTIONS:")
                    for exc in concept.exceptions:
                        output.append(f"  - {exc}")
                    output.append("")

                if concept.common_traps:
                    output.append("COMMON TRAPS (Watch out for these!):")
                    for trap in concept.common_traps:
                        output.append(f"  [!] {trap}")
                    output.append("")

                if related_questions:
                    output.append(f"PRACTICE: {len(related_questions)} question(s) available for this concept")
                    output.append("Type 'practice' to test your understanding")
                    output.append("")

                output.append("=" * 80)
                return "\n".join(output)

        return f"Concept '{concept_query}' not found. Try 'help' for available topics."

    def _end_session(self) -> str:
        """End session with summary"""
        self.state.session_started = False

        accuracy = self.state.correct_answers / max(self.state.questions_asked, 1)

        return f"""
================================================================================
SESSION COMPLETE
================================================================================

Final Statistics:
  Questions Answered: {self.state.questions_asked}
  Correct Answers: {self.state.correct_answers}
  Final Accuracy: {accuracy:.1%}

Keep studying and good luck on your bar exam!

Tip: Concepts you practiced today will appear in spaced repetition reviews
at optimal intervals to maximize long-term retention.

================================================================================
"""

# ==================== MAIN TUTOR ====================

class BarExamTutor:
    """Main unified bar exam tutor with advanced pedagogy integration"""

    def __init__(self, api_key: str = None):
        logger.info("Initializing Unified Bar Exam Tutor v5.0 with Advanced Pedagogy")

        self.api_key = api_key
        self.model = DEFAULT_MODEL

        self.kg = LegalKnowledgeGraph()
        self.practice_engine = InterleavedPracticeEngine(self.kg)
        self.tracker = PerformanceTracker()

        # Initialize advanced pedagogy engine
        self.pedagogy = AdvancedPedagogyEngine()
        self.pedagogy.initialize_knowledge_graph()

        # Sync knowledge graphs
        self._sync_pedagogy_knowledge_graph()
        self.interactive = InteractiveBarTutor(self)
        
        logger.info("Tutor initialized successfully")

    def _sync_pedagogy_knowledge_graph(self):
        """Sync bar tutor knowledge graph with pedagogy engine"""
        # Map bar tutor subjects to pedagogy subjects
        subject_mapping = {
            'contracts': 'contracts',
            'torts': 'torts',
            'constitutional_law': 'conlaw',
            'criminal_law': 'crim',
            'criminal_procedure': 'crim',
            'evidence': 'evidence',
            'civil_procedure': 'civpro',
            'real_property': 'property'
        }

        # Add bar tutor concepts to pedagogy knowledge graph
        for concept_id, concept in self.kg.nodes.items():
            pedagogy_subject = subject_mapping.get(concept.subject, concept.subject)
            # Create a simplified pedagogy node reference
            if concept_id not in self.pedagogy.knowledge_graph:
                from advanced_pedagogy import KnowledgeNode as PedagogyNode
                self.pedagogy.knowledge_graph[concept_id] = PedagogyNode(
                    concept_id=concept_id,
                    name=concept.name,
                    subject=pedagogy_subject,
                    difficulty=concept.difficulty,
                    mastery_level=concept.mastery_level,
                    ease_factor=concept.ease_factor,
                    interval=concept.interval
                )

        logger.info(f"Synced {len(self.kg.nodes)} concepts to pedagogy engine")

    def get_spaced_repetition_queue(self, subject: str = None) -> List[KnowledgeNode]:
        """Get concepts due for review using SM-2 spaced repetition"""
        due_concepts = []

        for concept_id, p_node in self.pedagogy.knowledge_graph.items():
            if subject and p_node.subject != subject:
                continue
            if self.pedagogy.spaced_repetition_scheduler(p_node):
                # Get the full concept from bar tutor kg
                if concept_id in self.kg.nodes:
                    due_concepts.append(self.kg.nodes[concept_id])

        # Sort by urgency (overdue items first, then by difficulty)
        due_concepts.sort(key=lambda c: (
            -(datetime.now() - c.last_reviewed).days if c.last_reviewed else 1000,
            c.difficulty
        ))

        return due_concepts[:10]  # Return top 10 most urgent

    def update_concept_mastery(self, concept_id: str, correct: bool, confidence: int = 3):
        """Update concept mastery using SM-2 algorithm and confidence calibration"""
        if concept_id not in self.kg.nodes:
            return

        concept = self.kg.nodes[concept_id]

        # SM-2 algorithm update
        if correct:
            if concept.review_count == 0:
                concept.interval = 1
            elif concept.review_count == 1:
                concept.interval = 6
            else:
                concept.interval = int(concept.interval * concept.ease_factor)

            # Adjust ease factor based on confidence
            # High confidence + correct = good learning
            # Low confidence + correct = lucky guess, don't increase ease much
            confidence_modifier = (confidence - 3) * 0.05
            concept.ease_factor = max(1.3, concept.ease_factor + 0.1 + confidence_modifier)
            concept.mastery_level = min(1.0, concept.mastery_level + 0.15)
        else:
            # Reset interval on failure
            concept.interval = 1
            concept.ease_factor = max(1.3, concept.ease_factor - 0.2)
            concept.mastery_level = max(0.0, concept.mastery_level - 0.1)

        concept.last_reviewed = datetime.now()
        concept.review_count += 1

        # Sync to pedagogy engine
        if concept_id in self.pedagogy.knowledge_graph:
            p_node = self.pedagogy.knowledge_graph[concept_id]
            p_node.mastery_level = concept.mastery_level
            p_node.ease_factor = concept.ease_factor
            p_node.interval = concept.interval
            p_node.last_reviewed = concept.last_reviewed
            p_node.review_count = concept.review_count

        # Record performance
        self.tracker.record_attempt(concept.subject, correct)

    def get_elaborative_feedback(self, question: Dict, user_answer: str, is_correct: bool) -> Dict:
        """Get elaborative interrogation feedback from pedagogy engine"""
        return self.pedagogy.elaborative_interrogation_engine(question, user_answer, is_correct)

    def get_socratic_dialogue(self, question: Dict, user_answer: str) -> Dict:
        """Get Socratic dialogue prompts for wrong answers"""
        return self.pedagogy.socratic_dialogue_engine(question, user_answer)

    def get_confidence_calibration(self, question: Dict, user_answer: str, confidence: int, is_correct: bool) -> Dict:
        """Track and analyze confidence calibration"""
        return self.pedagogy.confidence_calibration_tracker(question, user_answer, confidence, is_correct)

    def generate_study_plan(self, weak_subjects: List[str] = None) -> Dict:
        """Generate personalized study plan using pedagogy engine"""
        # Analyze performance to find weak subjects
        stats = self.tracker.get_stats(30)

        if not weak_subjects:
            weak_subjects = [
                subj for subj, data in stats.items()
                if data.get('percentage', 0) < 70
            ]

        # Get overall performance metrics
        total_correct = sum(s.get('correct', 0) for s in stats.values())
        total_questions = sum(s.get('total', 0) for s in stats.values())

        user_performance = {
            'weak_subjects': weak_subjects or ['contracts', 'evidence'],
            'overall_accuracy': total_correct / max(total_questions, 1),
            'study_hours_per_week': 20,
            'exam_date': datetime.now() + timedelta(days=90)
        }

        return self.pedagogy.generate_personalized_study_plan(user_performance)

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
        """Main menu with advanced pedagogy features"""
        print("\n" + "="*70)
        print("BAR EXAM TUTOR v5.0 - Advanced Pedagogy Edition")
        print("="*70)
        print("Featuring: Spaced Repetition | Confidence Calibration | Socratic Dialogue")

        while True:
            print("\n" + "-"*70)
            print("MAIN MENU")
            print("-"*70)
            print("1. Interactive Practice Mode (Recommended)")
            print("2. Interleaved Practice (Concept Review)")
            print("3. Explain Concept")
            print("4. Performance Dashboard")
            print("5. Spaced Repetition Review Queue")
            print("6. Generate Study Plan")
            print("0. Exit")
            print("-"*70)

            choice = input("\nSelect: ").strip()

            try:
                if choice == "0":
                    print("\nGood luck on your bar exam!")
                    break
                elif choice == "1":
                    self.start_interactive_mode()
                elif choice == "2":
                    self._interleaved_menu()
                elif choice == "3":
                    self._explain_menu()
                elif choice == "4":
                    self.tracker.display_dashboard()
                elif choice == "5":
                    self._show_spaced_repetition_queue()
                elif choice == "6":
                    self._show_study_plan()
                else:
                    print("Invalid choice")

            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                logger.error(f"Error: {e}", exc_info=True)
                print(f"Error: {e}")

    def _show_spaced_repetition_queue(self):
        """Display concepts due for spaced repetition review"""
        print("\n" + "="*70)
        print("SPACED REPETITION REVIEW QUEUE")
        print("="*70)

        due_concepts = self.get_spaced_repetition_queue()

        if not due_concepts:
            print("\nNo concepts due for review! All caught up.")
            print("Tip: Practice new concepts in Interactive Mode to build your queue.")
            return

        print(f"\n{len(due_concepts)} concepts due for review:\n")

        for i, concept in enumerate(due_concepts, 1):
            days_info = ""
            if concept.last_reviewed:
                days = (datetime.now() - concept.last_reviewed).days
                days_info = f" (last reviewed {days} days ago)"

            mastery_bar = "*" * int(concept.mastery_level * 10)
            print(f"{i}. {concept.name}")
            print(f"   Subject: {concept.subject.replace('_', ' ').title()}")
            print(f"   Mastery: [{mastery_bar:<10}] {concept.mastery_level:.0%}{days_info}")
            print()

        print("="*70)
        print("\nTip: Use Interactive Mode (Option 1) to practice these concepts.")

    def _show_study_plan(self):
        """Display personalized study plan"""
        print("\n" + "="*70)
        print("PERSONALIZED STUDY PLAN")
        print("="*70)

        plan = self.generate_study_plan()

        print(f"\nWeeks until exam: {plan['total_weeks']}")
        print(f"Focus subjects: {', '.join(plan['focus_subjects']) or 'All subjects balanced'}")

        print("\nRecommended Daily Structure:")
        print("-"*40)

        for session_name, session in plan['daily_structure'].items():
            print(f"\n  {session_name.replace('_', ' ').title()}:")
            print(f"    Duration: {session['duration']} minutes")
            print(f"    Mode: {session['mode'].value}")
            print(f"    Strategy: {session['strategy'].value}")

        if plan.get('adaptive_goals'):
            goals = plan['adaptive_goals']
            print("\n" + "-"*40)
            print("Adaptive Goals:")
            print(f"  Target accuracy: {goals['accuracy_target']:.0%}")
            print(f"  Target time per question: {goals['speed_target']} seconds")
            print(f"  Weak subject improvement: {goals['weak_subject_improvement']}")

        print("\n" + "="*70)
    
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
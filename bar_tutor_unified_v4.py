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
        """Initialize all MBE subjects + Real Property"""
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_evidence()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_criminal_procedure()
        self._initialize_civil_procedure()
        self._initialize_real_property()
    
    def _initialize_contracts(self):
        """Initialize contracts concepts from master guide"""
        concepts = [
            KnowledgeNode(
                concept_id="contracts_formation",
                name="Formation",
                subject="contracts",
                difficulty=2,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Advertisements (invitations)",
                    "UCC firm offers",
                    "mailbox rule twists",
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_terms_and_interpretation",
                name="Terms & Interpretation",
                subject="contracts",
                difficulty=3,
                rule_statement="Common law mirror-image; UCC gap fillers; parol evidence.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Battle of forms",
                    "parol evidence exceptions (ambiguity",
                    "fraud)",
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_performance_and_breach",
                name="Performance & Breach",
                subject="contracts",
                difficulty=3,
                rule_statement="Common law substantial performance vs material breach; UCC perfect tender.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Anticipatory repudiation (reasonable assurances)",
                    "divisible contracts",
                    "condition precedent vs subsequent.",
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_remedies",
                name="Remedies",
                subject="contracts",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Foreseeability (Hadley)",
                    "mitigation duties",
                    "liquidated damages (reasonable estimate",
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_defenses",
                name="Defenses",
                subject="contracts",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "SOF partial performance exceptions",
                    "mutual mistake vs unilateral",
                    "impossibility vs frustration.",
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_thirdparty_rights",
                name="Third-Party Rights",
                subject="contracts",
                difficulty=3,
                rule_statement="Assignments, delegations, third-party beneficiaries.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Revocation of gratuitous assignments",
                    "delegation of special skills",
                    "vesting of third-party rights.",
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_ucc_delivery_title_and_risk_of_loss",
                name="UCC Delivery, Title & Risk of Loss",
                subject="contracts",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Breach always keeps risk on breaching party; “FOB plant” is shipment",
                    "not destination; merchant receipt requirement.",
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_acceptance_rejection_and_revocation_ucc",
                name="Acceptance, Rejection & Revocation (UCC)",
                subject="contracts",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Using goods extensively after discovering defect can bar revocation; COD shipments limit inspection rights.",
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_excuse_impossibility_impracticability_frustration",
                name="Excuse: Impossibility, Impracticability, Frustration",
                subject="contracts",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Mere increased cost insufficient unless extreme; assuming price fluctuation risk defeats excuse.",
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_modification_accord_and_satisfaction_novation",
                name="Modification, Accord & Satisfaction, Novation",
                subject="contracts",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Modification of firm offer beyond three months requires fresh consideration; distinguishing novation from assignment/delegation.",
                ]
            ),
            KnowledgeNode(
                concept_id="contracts_warranties_ucc_and_common",
                name="Warranties (UCC & Common)",
                subject="contracts",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Statements of opinion/puffery not express warranties; “as is” doesn’t negate express warranties; limitations failing essential purpose open door to full UCC remedies.",
                ]
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_torts(self):
        """Initialize torts concepts from master guide"""
        concepts = [
            KnowledgeNode(
                concept_id="torts_intentional_torts",
                name="Intentional Torts",
                subject="torts",
                difficulty=3,
                rule_statement="Battery, assault, false imprisonment, IIED require volitional acts with intent or substantial certainty.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Transferred intent",
                    "consent scope",
                    "shopkeeper’s privilege limits",
                ]
            ),
            KnowledgeNode(
                concept_id="torts_negligence",
                name="Negligence",
                subject="torts",
                difficulty=3,
                rule_statement="Duty, breach (reasonable person or custom), actual/ proximate cause, damages.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Duty to unforeseeable plaintiffs (Cardozo vs Andrews)",
                    "res ipsa limits",
                    "superseding vs intervening causes",
                ]
            ),
            KnowledgeNode(
                concept_id="torts_strict_liability_and_products",
                name="Strict Liability & Products",
                subject="torts",
                difficulty=3,
                rule_statement="Strict liability for abnormally dangerous activities, wild animals; product claims under strict, negligence, warranty theories.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Product misuse vs foreseeable misuse",
                    "learned intermediary (pharma)",
                    "design vs manufacturing defects tests.",
                ]
            ),
            KnowledgeNode(
                concept_id="torts_defamation_and_privacy",
                name="Defamation & Privacy",
                subject="torts",
                difficulty=3,
                rule_statement="False statements harming reputation; public concern triggers constitutional actual-fault requirements.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Opinions vs fact",
                    "public vs private figures (actual malice vs negligence)",
                    "privacy tort distinctions (intrusion",
                ]
            ),
            KnowledgeNode(
                concept_id="torts_economic_and_dignitary",
                name="Economic & Dignitary",
                subject="torts",
                difficulty=3,
                rule_statement="Intentional interference, fraudulent misrepresentation, malicious prosecution.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Economic harm requirements",
                    "privilege defenses",
                    "probable cause in malicious prosecution.",
                ]
            ),
            KnowledgeNode(
                concept_id="torts_vicarious_liability_and_damages",
                name="Vicarious Liability & Damages",
                subject="torts",
                difficulty=3,
                rule_statement="Employers liable for employees acting in scope; punitive damages limited; joint & several vs several depending on jurisdiction.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Frolic vs detour",
                    "independent contractor exceptions",
                    "collateral source rule variations",
                ]
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_real_property(self):
        """Initialize real property - LAND BARON framework (9 concepts)"""
        concepts = [
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
                # 🏰 Mnemonic (rhythmic): PREFUR
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
                # 📜 Mnemonic (acronym): RACE to the Courthouse
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
                # 🛤️ Mnemonic (rhythmic): EASE
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
                # 👥 Mnemonic (acronym): TIE
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
                # 🏠 Mnemonic (acronym): RENT
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
                # 🏦 Mnemonic (acronym): MORT
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
                # 🏛️ Mnemonic (acronym): ZONE
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
                # ⚔️ Mnemonic (acronym): HATE
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
                # 🪑 Mnemonic (acronym): FIX
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_evidence(self):
        """Initialize evidence concepts from master guide"""
        concepts = [
            KnowledgeNode(
                concept_id="evidence_relevance",
                name="Relevance",
                subject="evidence",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Subsequent remedial measures",
                    "settlements",
                    "offers to pay medical expenses",
                ]
            ),
            KnowledgeNode(
                concept_id="evidence_character_evidence",
                name="Character Evidence",
                subject="evidence",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[]
            ),
            KnowledgeNode(
                concept_id="evidence_hearsay",
                name="Hearsay",
                subject="evidence",
                difficulty=4,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Double hearsay",
                    "testimonial statements confronting (Crawford)",
                    "former testimony requirements.",
                ]
            ),
            KnowledgeNode(
                concept_id="evidence_witnesses_and_impeachment",
                name="Witnesses & Impeachment",
                subject="evidence",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Collateral matters",
                    "prior consistent vs inconsistent statements",
                    "confrontation Clause for testimonial hearsay.",
                ]
            ),
            KnowledgeNode(
                concept_id="evidence_privileges_and_policy",
                name="Privileges & Policy",
                subject="evidence",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Spousal privileges scope",
                    "waiver by presence of third parties",
                    "work-product doctrine",
                ]
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_constitutional_law(self):
        """Initialize constitutional_law concepts from master guide"""
        concepts = [
            KnowledgeNode(
                concept_id="constitutional_law_judicial_power_and_justiciability",
                name="Judicial Power & Justiciability",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Case-or-controversy requirement demands standing (injury, causation, redressability), ripeness, and absence of mootness or political questions.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Taxpayer standing (usually none)",
                    "generalized grievances",
                    "mootness exceptions (e.g.",
                ]
            ),
            KnowledgeNode(
                concept_id="constitutional_law_federal_legislative_power",
                name="Federal Legislative Power",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Congress operates within enumerated powers; Commerce Clause covers channels, instrumentalities, and substantial economic effects; Necessary & Proper c",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Intrastate non-economic activity (Lopez)",
                    "attenuated chains under substantial-effects theory",
                    "anti-commandeering (New York v. US)",
                ]
            ),
            KnowledgeNode(
                concept_id="constitutional_law_executive_power",
                name="Executive Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Presidential power peaks with congressional authorization, declines in twilight zones, bottomed out when defying Congress.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Executive agreements = binding without Senate",
                    "removal limits for independent agencies",
                    "pardon excludes impeachment",
                ]
            ),
            KnowledgeNode(
                concept_id="constitutional_law_federalism_and_state_power",
                name="Federalism & State Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Tenth Amendment reserves unenumerated powers; Supremacy Clause preempts conflicts; dormant Commerce Clause prevents discriminatory burdens; states can",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Facial neutrality with discriminatory effect",
                    "Article IV Privileges & Immunities limited to citizens",
                    "federal commandeering of states",
                ]
            ),
            KnowledgeNode(
                concept_id="constitutional_law_individual_rights",
                name="Individual Rights",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Procedural DP requires notice + hearing for life/liberty/property; substantive DP protects fundamental rights via strict scrutiny, otherwise rational ",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "At-will employment lacks property interest",
                    "stigma-plus requirement",
                    "emergency exceptions for hearings",
                ]
            ),
            KnowledgeNode(
                concept_id="constitutional_law_equal_protection",
                name="Equal Protection",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Classification triggers scrutiny: suspect (strict), quasi-suspect (intermediate), others (rational basis); fundamental rights also trigger strict scru",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Need discriminatory intent",
                    "federal alienage uses rational basis",
                    "affirmative action strict scrutiny",
                ]
            ),
            KnowledgeNode(
                concept_id="constitutional_law_first_amendment",
                name="First Amendment",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Content-based regulations = strict scrutiny; content-neutral TPM = intermediate; unprotected categories include incitement, obscenity, fighting words,",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Incitement requires imminence",
                    "fighting words must be face-to-face",
                    "prior restraint presumption",
                ]
            ),
            KnowledgeNode(
                concept_id="constitutional_law_first_amendment",
                name="First Amendment",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Establishment Clause prohibits endorsement/coercion; Free Exercise absolutely protects belief, protects conduct when laws target religion.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Smith (neutral laws need no exemptions)",
                    "school prayer always problematic",
                    "aid to religious schools permissible if neutral",
                ]
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_criminal_law(self):
        """Initialize criminal_law concepts from master guide"""
        concepts = [
            KnowledgeNode(
                concept_id="criminal_law_elements_of_crimes",
                name="Elements of Crimes",
                subject="criminal_law",
                difficulty=2,
                rule_statement="Every offense needs a voluntary act (or qualifying omission), the requisite mental state, concurrence, and causation.",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Specific vs general intent (intoxication defenses)",
                    "transferred intent limited to same crime",
                    "medical negligence generally foreseeable",
                ]
            ),
            KnowledgeNode(
                concept_id="criminal_law_homicide_offenses",
                name="Homicide Offenses",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Murder = unlawful killing with malice aforethought (intent to kill, intent to seriously injure, depraved heart, felony murder). Manslaughter lacks mal",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Instant premeditation allowed; deadly weapon inference; felony-murder merger; cooling-off defeats voluntary manslaughter; police/victim killings not felony murder (agency theory).",
                ]
            ),
            KnowledgeNode(
                concept_id="criminal_law_other_crimes_against_persons",
                name="Other Crimes Against Persons",
                subject="criminal_law",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Battery requires only intent to touch; assault has two theories; kidnapping needs substantial movement; mistake of age no defense to statutory rape.",
                ]
            ),
            KnowledgeNode(
                concept_id="criminal_law_property_crimes",
                name="Property Crimes",
                subject="criminal_law",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Intent at time of taking (larceny); assaultive felonies merge; force must accompany taking for robbery; burglary intent must pre-exist entry.",
                ]
            ),
            KnowledgeNode(
                concept_id="criminal_law_inchoate_crimes",
                name="Inchoate Crimes",
                subject="criminal_law",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Solicitation complete without acceptance; conspiracy survives completed offense; attempt always specific intent; abandonment defense limited (MPC).",
                ]
            ),
            KnowledgeNode(
                concept_id="criminal_law_accomplice_and_accessory_liability",
                name="Accomplice & Accessory Liability",
                subject="criminal_law",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Mere presence insufficient; dual intent requirement; accomplice liability remains even if principal acquitted; accessory after fact not liable for underlying offense.",
                ]
            ),
            KnowledgeNode(
                concept_id="criminal_law_defenses",
                name="Defenses",
                subject="criminal_law",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Duress unavailable for murder; voluntary intoxication limited; entrapment fails if predisposed; mistaking age no defense to statutory rape.",
                ]
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


    def _initialize_criminal_procedure(self):
        """Initialize criminal_procedure concepts from master guide"""
        concepts = [
            KnowledgeNode(
                concept_id="criminal_procedure_fourth_amendment",
                name="Fourth Amendment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Standing (expectation of privacy)",
                    "private search doctrine",
                    "warrant particularity",
                ]
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_exclusionary_rule",
                name="Exclusionary Rule",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Impeachment use",
                    "Miranda violations (non-Miranda statements may be used for impeachment)",
                    "attenuation factors.",
                ]
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_fifth_amendment",
                name="Fifth Amendment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Ambiguous requests",
                    "re-initiation by suspect",
                    "public-safety exception",
                ]
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_sixth_amendment",
                name="Sixth Amendment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Offense-specific attachment",
                    "deliberate elicitation",
                    "Massiah",
                ]
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_civil_procedure(self):
        """Initialize civil_procedure concepts from master guide"""
        concepts = [
            KnowledgeNode(
                concept_id="civil_procedure_jurisdiction_and_venue",
                name="Jurisdiction & Venue",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "General vs specific jurisdiction",
                    "minimum contacts",
                    "domicile",
                ]
            ),
            KnowledgeNode(
                concept_id="civil_procedure_pleadings_and_motions",
                name="Pleadings & Motions",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Twiqbal plausibility",
                    "relation back",
                    "waiver of defenses.",
                ]
            ),
            KnowledgeNode(
                concept_id="civil_procedure_joinder_and_discovery",
                name="Joinder & Discovery",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Compulsory counterclaims",
                    "indispensable parties",
                    "discovery sanctions.",
                ]
            ),
            KnowledgeNode(
                concept_id="civil_procedure_pretrial_and_trial",
                name="Pretrial & Trial",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[]
            ),
            KnowledgeNode(
                concept_id="civil_procedure_judgments_and_preclusion",
                name="Judgments & Preclusion",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="See study guide for details",
                elements=[],
                policy_rationales=[],
                common_traps=[
                    "Same parties/privity",
                    "mutual vs non-mutual collateral estoppel",
                    "full faith and credit",
                ]
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
#!/usr/bin/env python3
"""
Advanced Pedagogical Techniques for MBE Study
Implements evidence-based learning strategies from cognitive science
"""

import json
import random
import time
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from statistics import mean, stdev

class LearningMode(Enum):
    """Different learning modes based on cognitive science"""
    FOCUSED_PRACTICE = "focused"        # Single subject deep dive
    INTERLEAVED_PRACTICE = "interleaved" # Mixed subjects for better retention
    RETRIEVAL_PRACTICE = "retrieval"     # Testing without answers
    SPACED_REPETITION = "spaced"         # SM-2 algorithm
    DIAGNOSTIC_ASSESSMENT = "diagnostic" # Identify knowledge gaps
    ADAPTIVE_DIFFICULTY = "adaptive"     # AI adjusts difficulty
    CONCEPT_MAPPING = "mapping"          # Visual concept relationships
    SOCRATIC_DIALOGUE = "socratic"       # Guided discovery learning

class CognitiveStrategy(Enum):
    """Evidence-based cognitive strategies"""
    DUAL_CODING = "dual_coding"          # Visual + verbal learning
    ELABORATION = "elaboration"           # Deep processing
    SELF_EXPLANATION = "self_explanation" # Explain concepts to yourself
    INTERLEAVING = "interleaving"         # Mix related concepts
    SPACING = "spacing"                  # Distributed practice
    TESTING = "testing"                  # Retrieval practice
    GENERATION = "generation"            # Active recall

@dataclass
class StudySession:
    """Represents a study session with advanced tracking"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    mode: LearningMode = LearningMode.FOCUSED_PRACTICE
    subject: str = "mixed"
    questions_attempted: int = 0
    questions_correct: int = 0
    time_spent: int = 0  # seconds
    cognitive_strategies_used: List[CognitiveStrategy] = field(default_factory=list)
    confidence_ratings: List[int] = field(default_factory=list)  # 1-5 scale
    difficulty_ratings: List[int] = field(default_factory=list)  # 1-5 scale
    meta_cognition_notes: str = ""

@dataclass
class KnowledgeNode:
    """Represents a concept in the knowledge graph"""
    concept_id: str
    name: str
    subject: str
    difficulty: int  # 1-5
    prerequisites: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    mastery_level: float = 0.0  # 0-1
    last_reviewed: Optional[datetime] = None
    review_count: int = 0
    ease_factor: float = 2.5  # SM-2 ease factor
    interval: int = 1  # days until next review

class AdvancedPedagogyEngine:
    """
    Advanced pedagogical engine implementing evidence-based learning strategies
    """

    def __init__(self):
        self.knowledge_graph = {}  # concept_id -> KnowledgeNode
        self.study_sessions = []
        self.user_profile = {
            'learning_style': 'visual',  # visual, auditory, kinesthetic, reading
            'attention_span': 45,  # minutes
            'preferred_subjects': [],
            'weak_areas': [],
            'strong_areas': [],
            'optimal_study_time': 'morning',  # morning, afternoon, evening
            'motivation_level': 5,  # 1-10
        }
        self.performance_history = defaultdict(list)
        self.adaptive_difficulty = {
            'current_level': 'intermediate',
            'success_streak': 0,
            'failure_streak': 0,
            'last_adjustment': datetime.now()
        }

    def initialize_knowledge_graph(self):
        """Initialize the MBE knowledge graph with comprehensive legal concepts"""
        concepts = {
            # ==================== CONTRACTS ====================
            'contracts_formation': KnowledgeNode(
                'contracts_formation', 'Contract Formation', 'contracts', 2,
                related_concepts=['contracts_offer_acceptance', 'contracts_consideration']
            ),
            'contracts_offer_acceptance': KnowledgeNode(
                'contracts_offer_acceptance', 'Offer & Acceptance', 'contracts', 3,
                related_concepts=['contracts_formation', 'contracts_mailbox_rule']
            ),
            'contracts_consideration': KnowledgeNode(
                'contracts_consideration', 'Consideration', 'contracts', 2,
                related_concepts=['contracts_formation', 'contracts_promissory_estoppel']
            ),
            'contracts_promissory_estoppel': KnowledgeNode(
                'contracts_promissory_estoppel', 'Promissory Estoppel', 'contracts', 3,
                related_concepts=['contracts_consideration']
            ),
            'contracts_mailbox_rule': KnowledgeNode(
                'contracts_mailbox_rule', 'Mailbox Rule', 'contracts', 3,
                related_concepts=['contracts_offer_acceptance']
            ),
            'contracts_statute_of_frauds': KnowledgeNode(
                'contracts_statute_of_frauds', 'Statute of Frauds', 'contracts', 3,
                related_concepts=['contracts_formation', 'contracts_part_performance']
            ),
            'contracts_part_performance': KnowledgeNode(
                'contracts_part_performance', 'Part Performance Exception', 'contracts', 4,
                related_concepts=['contracts_statute_of_frauds']
            ),
            'contracts_parol_evidence': KnowledgeNode(
                'contracts_parol_evidence', 'Parol Evidence Rule', 'contracts', 4,
                related_concepts=['contracts_interpretation']
            ),
            'contracts_interpretation': KnowledgeNode(
                'contracts_interpretation', 'Contract Interpretation', 'contracts', 3,
                related_concepts=['contracts_parol_evidence']
            ),
            'contracts_performance': KnowledgeNode(
                'contracts_performance', 'Performance & Breach', 'contracts', 3,
                related_concepts=['contracts_remedies', 'contracts_conditions']
            ),
            'contracts_conditions': KnowledgeNode(
                'contracts_conditions', 'Conditions (Precedent/Subsequent/Concurrent)', 'contracts', 4,
                related_concepts=['contracts_performance']
            ),
            'contracts_remedies': KnowledgeNode(
                'contracts_remedies', 'Remedies & Damages', 'contracts', 4,
                related_concepts=['contracts_performance', 'contracts_specific_performance']
            ),
            'contracts_specific_performance': KnowledgeNode(
                'contracts_specific_performance', 'Specific Performance', 'contracts', 3,
                related_concepts=['contracts_remedies']
            ),
            'contracts_third_party': KnowledgeNode(
                'contracts_third_party', 'Third Party Beneficiaries', 'contracts', 4,
                related_concepts=['contracts_assignment']
            ),
            'contracts_assignment': KnowledgeNode(
                'contracts_assignment', 'Assignment & Delegation', 'contracts', 3,
                related_concepts=['contracts_third_party']
            ),
            'contracts_ucc_article2': KnowledgeNode(
                'contracts_ucc_article2', 'UCC Article 2 (Sales)', 'contracts', 4,
                related_concepts=['contracts_formation', 'contracts_remedies']
            ),

            # ==================== TORTS ====================
            'torts_negligence': KnowledgeNode(
                'torts_negligence', 'Negligence Elements', 'torts', 3,
                related_concepts=['torts_duty', 'torts_breach', 'torts_causation', 'torts_damages']
            ),
            'torts_duty': KnowledgeNode(
                'torts_duty', 'Duty of Care', 'torts', 2,
                related_concepts=['torts_negligence', 'torts_special_duty']
            ),
            'torts_special_duty': KnowledgeNode(
                'torts_special_duty', 'Special Duty Rules (Landowners, Professionals)', 'torts', 4,
                related_concepts=['torts_duty']
            ),
            'torts_breach': KnowledgeNode(
                'torts_breach', 'Breach of Duty', 'torts', 2,
                related_concepts=['torts_negligence', 'torts_res_ipsa']
            ),
            'torts_res_ipsa': KnowledgeNode(
                'torts_res_ipsa', 'Res Ipsa Loquitur', 'torts', 4,
                related_concepts=['torts_breach']
            ),
            'torts_causation': KnowledgeNode(
                'torts_causation', 'Causation (Actual & Proximate)', 'torts', 4,
                related_concepts=['torts_negligence']
            ),
            'torts_damages': KnowledgeNode(
                'torts_damages', 'Damages in Tort', 'torts', 3,
                related_concepts=['torts_negligence']
            ),
            'torts_defenses': KnowledgeNode(
                'torts_defenses', 'Negligence Defenses', 'torts', 3,
                related_concepts=['torts_negligence', 'torts_comparative_fault']
            ),
            'torts_comparative_fault': KnowledgeNode(
                'torts_comparative_fault', 'Comparative & Contributory Negligence', 'torts', 3,
                related_concepts=['torts_defenses']
            ),
            'torts_intentional': KnowledgeNode(
                'torts_intentional', 'Intentional Torts', 'torts', 2,
                related_concepts=['torts_battery', 'torts_assault', 'torts_false_imprisonment']
            ),
            'torts_battery': KnowledgeNode(
                'torts_battery', 'Battery', 'torts', 2,
                related_concepts=['torts_intentional', 'torts_assault']
            ),
            'torts_assault': KnowledgeNode(
                'torts_assault', 'Assault', 'torts', 2,
                related_concepts=['torts_intentional', 'torts_battery']
            ),
            'torts_false_imprisonment': KnowledgeNode(
                'torts_false_imprisonment', 'False Imprisonment', 'torts', 3,
                related_concepts=['torts_intentional']
            ),
            'torts_iied': KnowledgeNode(
                'torts_iied', 'Intentional Infliction of Emotional Distress', 'torts', 3,
                related_concepts=['torts_intentional']
            ),
            'torts_strict_liability': KnowledgeNode(
                'torts_strict_liability', 'Strict Liability', 'torts', 3,
                related_concepts=['torts_products_liability', 'torts_abnormally_dangerous']
            ),
            'torts_products_liability': KnowledgeNode(
                'torts_products_liability', 'Products Liability', 'torts', 4,
                related_concepts=['torts_strict_liability']
            ),
            'torts_abnormally_dangerous': KnowledgeNode(
                'torts_abnormally_dangerous', 'Abnormally Dangerous Activities', 'torts', 3,
                related_concepts=['torts_strict_liability']
            ),
            'torts_defamation': KnowledgeNode(
                'torts_defamation', 'Defamation', 'torts', 4,
                related_concepts=['torts_privacy']
            ),
            'torts_privacy': KnowledgeNode(
                'torts_privacy', 'Privacy Torts', 'torts', 4,
                related_concepts=['torts_defamation']
            ),
            'torts_vicarious_liability': KnowledgeNode(
                'torts_vicarious_liability', 'Vicarious Liability & Respondeat Superior', 'torts', 3,
                related_concepts=['torts_negligence']
            ),

            # ==================== CONSTITUTIONAL LAW ====================
            'conlaw_judicial_review': KnowledgeNode(
                'conlaw_judicial_review', 'Judicial Review & Justiciability', 'conlaw', 3,
                related_concepts=['conlaw_standing', 'conlaw_mootness']
            ),
            'conlaw_standing': KnowledgeNode(
                'conlaw_standing', 'Standing', 'conlaw', 4,
                related_concepts=['conlaw_judicial_review']
            ),
            'conlaw_mootness': KnowledgeNode(
                'conlaw_mootness', 'Mootness & Ripeness', 'conlaw', 3,
                related_concepts=['conlaw_judicial_review']
            ),
            'conlaw_federal_powers': KnowledgeNode(
                'conlaw_federal_powers', 'Federal Legislative Powers', 'conlaw', 3,
                related_concepts=['conlaw_commerce_clause', 'conlaw_spending_power']
            ),
            'conlaw_commerce_clause': KnowledgeNode(
                'conlaw_commerce_clause', 'Commerce Clause', 'conlaw', 4,
                related_concepts=['conlaw_federal_powers', 'conlaw_dormant_commerce']
            ),
            'conlaw_dormant_commerce': KnowledgeNode(
                'conlaw_dormant_commerce', 'Dormant Commerce Clause', 'conlaw', 4,
                related_concepts=['conlaw_commerce_clause']
            ),
            'conlaw_spending_power': KnowledgeNode(
                'conlaw_spending_power', 'Taxing & Spending Power', 'conlaw', 3,
                related_concepts=['conlaw_federal_powers']
            ),
            'conlaw_executive_power': KnowledgeNode(
                'conlaw_executive_power', 'Executive Power', 'conlaw', 3,
                related_concepts=['conlaw_separation_of_powers']
            ),
            'conlaw_separation_of_powers': KnowledgeNode(
                'conlaw_separation_of_powers', 'Separation of Powers', 'conlaw', 3,
                related_concepts=['conlaw_executive_power', 'conlaw_federal_powers']
            ),
            'conlaw_due_process': KnowledgeNode(
                'conlaw_due_process', 'Due Process', 'conlaw', 4,
                related_concepts=['conlaw_procedural_dp', 'conlaw_substantive_dp']
            ),
            'conlaw_procedural_dp': KnowledgeNode(
                'conlaw_procedural_dp', 'Procedural Due Process', 'conlaw', 3,
                related_concepts=['conlaw_due_process']
            ),
            'conlaw_substantive_dp': KnowledgeNode(
                'conlaw_substantive_dp', 'Substantive Due Process', 'conlaw', 4,
                related_concepts=['conlaw_due_process', 'conlaw_fundamental_rights']
            ),
            'conlaw_fundamental_rights': KnowledgeNode(
                'conlaw_fundamental_rights', 'Fundamental Rights', 'conlaw', 4,
                related_concepts=['conlaw_substantive_dp']
            ),
            'conlaw_equal_protection': KnowledgeNode(
                'conlaw_equal_protection', 'Equal Protection', 'conlaw', 4,
                related_concepts=['conlaw_strict_scrutiny', 'conlaw_intermediate_scrutiny']
            ),
            'conlaw_strict_scrutiny': KnowledgeNode(
                'conlaw_strict_scrutiny', 'Strict Scrutiny', 'conlaw', 4,
                related_concepts=['conlaw_equal_protection']
            ),
            'conlaw_intermediate_scrutiny': KnowledgeNode(
                'conlaw_intermediate_scrutiny', 'Intermediate Scrutiny', 'conlaw', 3,
                related_concepts=['conlaw_equal_protection']
            ),
            'conlaw_first_amendment': KnowledgeNode(
                'conlaw_first_amendment', 'First Amendment Overview', 'conlaw', 5,
                related_concepts=['conlaw_free_speech', 'conlaw_religion']
            ),
            'conlaw_free_speech': KnowledgeNode(
                'conlaw_free_speech', 'Freedom of Speech', 'conlaw', 5,
                related_concepts=['conlaw_first_amendment', 'conlaw_content_neutral']
            ),
            'conlaw_content_neutral': KnowledgeNode(
                'conlaw_content_neutral', 'Content-Based vs Content-Neutral', 'conlaw', 4,
                related_concepts=['conlaw_free_speech']
            ),
            'conlaw_religion': KnowledgeNode(
                'conlaw_religion', 'Religion Clauses', 'conlaw', 4,
                related_concepts=['conlaw_first_amendment']
            ),
            'conlaw_state_action': KnowledgeNode(
                'conlaw_state_action', 'State Action Doctrine', 'conlaw', 3,
                related_concepts=['conlaw_equal_protection', 'conlaw_due_process']
            ),

            # ==================== CRIMINAL LAW ====================
            'crim_actus_reus': KnowledgeNode(
                'crim_actus_reus', 'Actus Reus', 'crim', 2,
                related_concepts=['crim_mens_rea']
            ),
            'crim_mens_rea': KnowledgeNode(
                'crim_mens_rea', 'Mens Rea', 'crim', 3,
                related_concepts=['crim_actus_reus', 'crim_strict_liability']
            ),
            'crim_strict_liability': KnowledgeNode(
                'crim_strict_liability', 'Strict Liability Crimes', 'crim', 3,
                related_concepts=['crim_mens_rea']
            ),
            'crim_homicide': KnowledgeNode(
                'crim_homicide', 'Homicide Overview', 'crim', 4,
                related_concepts=['crim_murder', 'crim_manslaughter']
            ),
            'crim_murder': KnowledgeNode(
                'crim_murder', 'Murder (1st & 2nd Degree)', 'crim', 4,
                related_concepts=['crim_homicide', 'crim_felony_murder']
            ),
            'crim_felony_murder': KnowledgeNode(
                'crim_felony_murder', 'Felony Murder', 'crim', 5,
                related_concepts=['crim_murder']
            ),
            'crim_manslaughter': KnowledgeNode(
                'crim_manslaughter', 'Manslaughter (Voluntary & Involuntary)', 'crim', 4,
                related_concepts=['crim_homicide']
            ),
            'crim_inchoate': KnowledgeNode(
                'crim_inchoate', 'Inchoate Crimes Overview', 'crim', 3,
                related_concepts=['crim_attempt', 'crim_conspiracy', 'crim_solicitation']
            ),
            'crim_attempt': KnowledgeNode(
                'crim_attempt', 'Attempt', 'crim', 3,
                related_concepts=['crim_inchoate']
            ),
            'crim_conspiracy': KnowledgeNode(
                'crim_conspiracy', 'Conspiracy', 'crim', 4,
                related_concepts=['crim_inchoate', 'crim_parties']
            ),
            'crim_solicitation': KnowledgeNode(
                'crim_solicitation', 'Solicitation', 'crim', 3,
                related_concepts=['crim_inchoate']
            ),
            'crim_parties': KnowledgeNode(
                'crim_parties', 'Parties to Crime (Accomplice Liability)', 'crim', 4,
                related_concepts=['crim_conspiracy']
            ),
            'crim_defenses': KnowledgeNode(
                'crim_defenses', 'Criminal Defenses Overview', 'crim', 3,
                related_concepts=['crim_self_defense', 'crim_insanity', 'crim_necessity']
            ),
            'crim_self_defense': KnowledgeNode(
                'crim_self_defense', 'Self-Defense & Defense of Others', 'crim', 3,
                related_concepts=['crim_defenses']
            ),
            'crim_insanity': KnowledgeNode(
                'crim_insanity', 'Insanity Defense', 'crim', 4,
                related_concepts=['crim_defenses']
            ),
            'crim_necessity': KnowledgeNode(
                'crim_necessity', 'Necessity & Duress', 'crim', 3,
                related_concepts=['crim_defenses']
            ),
            'crim_property_crimes': KnowledgeNode(
                'crim_property_crimes', 'Property Crimes', 'crim', 3,
                related_concepts=['crim_theft', 'crim_robbery', 'crim_burglary']
            ),
            'crim_theft': KnowledgeNode(
                'crim_theft', 'Theft Crimes (Larceny, Embezzlement, False Pretenses)', 'crim', 4,
                related_concepts=['crim_property_crimes']
            ),
            'crim_robbery': KnowledgeNode(
                'crim_robbery', 'Robbery', 'crim', 3,
                related_concepts=['crim_property_crimes']
            ),
            'crim_burglary': KnowledgeNode(
                'crim_burglary', 'Burglary', 'crim', 3,
                related_concepts=['crim_property_crimes']
            ),

            # ==================== EVIDENCE ====================
            'evidence_relevance': KnowledgeNode(
                'evidence_relevance', 'Relevance (FRE 401-403)', 'evidence', 2,
                related_concepts=['evidence_prejudice']
            ),
            'evidence_prejudice': KnowledgeNode(
                'evidence_prejudice', 'Unfair Prejudice (FRE 403)', 'evidence', 3,
                related_concepts=['evidence_relevance']
            ),
            'evidence_character': KnowledgeNode(
                'evidence_character', 'Character Evidence (FRE 404-405)', 'evidence', 4,
                related_concepts=['evidence_prior_bad_acts']
            ),
            'evidence_prior_bad_acts': KnowledgeNode(
                'evidence_prior_bad_acts', 'Prior Bad Acts (FRE 404(b))', 'evidence', 4,
                related_concepts=['evidence_character']
            ),
            'evidence_habit': KnowledgeNode(
                'evidence_habit', 'Habit Evidence (FRE 406)', 'evidence', 2,
                related_concepts=['evidence_character']
            ),
            'evidence_hearsay': KnowledgeNode(
                'evidence_hearsay', 'Hearsay (FRE 801-807)', 'evidence', 5,
                related_concepts=['evidence_hearsay_exceptions', 'evidence_non_hearsay']
            ),
            'evidence_non_hearsay': KnowledgeNode(
                'evidence_non_hearsay', 'Non-Hearsay (FRE 801(d))', 'evidence', 4,
                related_concepts=['evidence_hearsay', 'evidence_admissions']
            ),
            'evidence_admissions': KnowledgeNode(
                'evidence_admissions', 'Party Admissions (FRE 801(d)(2))', 'evidence', 3,
                related_concepts=['evidence_non_hearsay']
            ),
            'evidence_hearsay_exceptions': KnowledgeNode(
                'evidence_hearsay_exceptions', 'Hearsay Exceptions', 'evidence', 5,
                related_concepts=['evidence_hearsay', 'evidence_present_sense', 'evidence_excited_utterance']
            ),
            'evidence_present_sense': KnowledgeNode(
                'evidence_present_sense', 'Present Sense Impression (FRE 803(1))', 'evidence', 3,
                related_concepts=['evidence_hearsay_exceptions']
            ),
            'evidence_excited_utterance': KnowledgeNode(
                'evidence_excited_utterance', 'Excited Utterance (FRE 803(2))', 'evidence', 3,
                related_concepts=['evidence_hearsay_exceptions']
            ),
            'evidence_business_records': KnowledgeNode(
                'evidence_business_records', 'Business Records (FRE 803(6))', 'evidence', 3,
                related_concepts=['evidence_hearsay_exceptions']
            ),
            'evidence_dying_declaration': KnowledgeNode(
                'evidence_dying_declaration', 'Dying Declaration (FRE 804(b)(2))', 'evidence', 4,
                related_concepts=['evidence_hearsay_exceptions']
            ),
            'evidence_witnesses': KnowledgeNode(
                'evidence_witnesses', 'Witness Competency & Examination', 'evidence', 2,
                related_concepts=['evidence_impeachment', 'evidence_opinion']
            ),
            'evidence_impeachment': KnowledgeNode(
                'evidence_impeachment', 'Impeachment (FRE 607-613)', 'evidence', 4,
                related_concepts=['evidence_witnesses']
            ),
            'evidence_opinion': KnowledgeNode(
                'evidence_opinion', 'Opinion Testimony (FRE 701-706)', 'evidence', 3,
                related_concepts=['evidence_witnesses', 'evidence_expert']
            ),
            'evidence_expert': KnowledgeNode(
                'evidence_expert', 'Expert Witnesses (Daubert)', 'evidence', 4,
                related_concepts=['evidence_opinion']
            ),
            'evidence_privileges': KnowledgeNode(
                'evidence_privileges', 'Privileges', 'evidence', 4,
                related_concepts=['evidence_attorney_client', 'evidence_spousal']
            ),
            'evidence_attorney_client': KnowledgeNode(
                'evidence_attorney_client', 'Attorney-Client Privilege', 'evidence', 4,
                related_concepts=['evidence_privileges']
            ),
            'evidence_spousal': KnowledgeNode(
                'evidence_spousal', 'Spousal Privileges', 'evidence', 3,
                related_concepts=['evidence_privileges']
            ),
            'evidence_authentication': KnowledgeNode(
                'evidence_authentication', 'Authentication (FRE 901-902)', 'evidence', 3,
                related_concepts=['evidence_best_evidence']
            ),
            'evidence_best_evidence': KnowledgeNode(
                'evidence_best_evidence', 'Best Evidence Rule (FRE 1001-1008)', 'evidence', 3,
                related_concepts=['evidence_authentication']
            ),

            # ==================== CIVIL PROCEDURE ====================
            'civpro_jurisdiction': KnowledgeNode(
                'civpro_jurisdiction', 'Subject Matter Jurisdiction', 'civpro', 4,
                related_concepts=['civpro_diversity', 'civpro_federal_question']
            ),
            'civpro_diversity': KnowledgeNode(
                'civpro_diversity', 'Diversity Jurisdiction', 'civpro', 3,
                related_concepts=['civpro_jurisdiction']
            ),
            'civpro_federal_question': KnowledgeNode(
                'civpro_federal_question', 'Federal Question Jurisdiction', 'civpro', 3,
                related_concepts=['civpro_jurisdiction']
            ),
            'civpro_supplemental': KnowledgeNode(
                'civpro_supplemental', 'Supplemental Jurisdiction', 'civpro', 4,
                related_concepts=['civpro_jurisdiction']
            ),
            'civpro_personal_jurisdiction': KnowledgeNode(
                'civpro_personal_jurisdiction', 'Personal Jurisdiction', 'civpro', 4,
                related_concepts=['civpro_minimum_contacts', 'civpro_long_arm']
            ),
            'civpro_minimum_contacts': KnowledgeNode(
                'civpro_minimum_contacts', 'Minimum Contacts', 'civpro', 4,
                related_concepts=['civpro_personal_jurisdiction']
            ),
            'civpro_long_arm': KnowledgeNode(
                'civpro_long_arm', 'Long-Arm Statutes', 'civpro', 3,
                related_concepts=['civpro_personal_jurisdiction']
            ),
            'civpro_venue': KnowledgeNode(
                'civpro_venue', 'Venue', 'civpro', 3,
                related_concepts=['civpro_transfer', 'civpro_forum_non_conveniens']
            ),
            'civpro_transfer': KnowledgeNode(
                'civpro_transfer', 'Transfer of Venue', 'civpro', 3,
                related_concepts=['civpro_venue']
            ),
            'civpro_forum_non_conveniens': KnowledgeNode(
                'civpro_forum_non_conveniens', 'Forum Non Conveniens', 'civpro', 4,
                related_concepts=['civpro_venue']
            ),
            'civpro_pleadings': KnowledgeNode(
                'civpro_pleadings', 'Pleadings (Rules 7-15)', 'civpro', 3,
                related_concepts=['civpro_complaint', 'civpro_answer']
            ),
            'civpro_complaint': KnowledgeNode(
                'civpro_complaint', 'Complaint & Twombly/Iqbal', 'civpro', 4,
                related_concepts=['civpro_pleadings']
            ),
            'civpro_answer': KnowledgeNode(
                'civpro_answer', 'Answer & Affirmative Defenses', 'civpro', 3,
                related_concepts=['civpro_pleadings']
            ),
            'civpro_motions': KnowledgeNode(
                'civpro_motions', 'Pre-Answer Motions (Rule 12)', 'civpro', 4,
                related_concepts=['civpro_pleadings', 'civpro_12b6']
            ),
            'civpro_12b6': KnowledgeNode(
                'civpro_12b6', 'Motion to Dismiss (12(b)(6))', 'civpro', 4,
                related_concepts=['civpro_motions']
            ),
            'civpro_discovery': KnowledgeNode(
                'civpro_discovery', 'Discovery (Rules 26-37)', 'civpro', 4,
                related_concepts=['civpro_scope', 'civpro_depositions']
            ),
            'civpro_scope': KnowledgeNode(
                'civpro_scope', 'Scope of Discovery', 'civpro', 3,
                related_concepts=['civpro_discovery']
            ),
            'civpro_depositions': KnowledgeNode(
                'civpro_depositions', 'Depositions & Interrogatories', 'civpro', 3,
                related_concepts=['civpro_discovery']
            ),
            'civpro_joinder': KnowledgeNode(
                'civpro_joinder', 'Joinder (Rules 18-20)', 'civpro', 4,
                related_concepts=['civpro_intervention', 'civpro_impleader']
            ),
            'civpro_intervention': KnowledgeNode(
                'civpro_intervention', 'Intervention (Rule 24)', 'civpro', 4,
                related_concepts=['civpro_joinder']
            ),
            'civpro_impleader': KnowledgeNode(
                'civpro_impleader', 'Impleader (Rule 14)', 'civpro', 4,
                related_concepts=['civpro_joinder']
            ),
            'civpro_summary_judgment': KnowledgeNode(
                'civpro_summary_judgment', 'Summary Judgment (Rule 56)', 'civpro', 3,
                related_concepts=['civpro_trial']
            ),
            'civpro_trial': KnowledgeNode(
                'civpro_trial', 'Trial & Judgment', 'civpro', 3,
                related_concepts=['civpro_summary_judgment', 'civpro_jmol']
            ),
            'civpro_jmol': KnowledgeNode(
                'civpro_jmol', 'JMOL & Renewed JMOL', 'civpro', 4,
                related_concepts=['civpro_trial']
            ),
            'civpro_res_judicata': KnowledgeNode(
                'civpro_res_judicata', 'Claim Preclusion (Res Judicata)', 'civpro', 4,
                related_concepts=['civpro_collateral_estoppel']
            ),
            'civpro_collateral_estoppel': KnowledgeNode(
                'civpro_collateral_estoppel', 'Issue Preclusion (Collateral Estoppel)', 'civpro', 4,
                related_concepts=['civpro_res_judicata']
            ),

            # ==================== REAL PROPERTY ====================
            'property_estates': KnowledgeNode(
                'property_estates', 'Estates in Land', 'property', 3,
                related_concepts=['property_fee_simple', 'property_life_estate']
            ),
            'property_fee_simple': KnowledgeNode(
                'property_fee_simple', 'Fee Simple (Absolute, Defeasible)', 'property', 3,
                related_concepts=['property_estates']
            ),
            'property_life_estate': KnowledgeNode(
                'property_life_estate', 'Life Estates', 'property', 3,
                related_concepts=['property_estates']
            ),
            'property_future_interests': KnowledgeNode(
                'property_future_interests', 'Future Interests', 'property', 5,
                related_concepts=['property_estates', 'property_rap']
            ),
            'property_rap': KnowledgeNode(
                'property_rap', 'Rule Against Perpetuities', 'property', 5,
                related_concepts=['property_future_interests']
            ),
            'property_concurrent': KnowledgeNode(
                'property_concurrent', 'Concurrent Ownership', 'property', 3,
                related_concepts=['property_joint_tenancy', 'property_tenancy_common']
            ),
            'property_joint_tenancy': KnowledgeNode(
                'property_joint_tenancy', 'Joint Tenancy', 'property', 3,
                related_concepts=['property_concurrent']
            ),
            'property_tenancy_common': KnowledgeNode(
                'property_tenancy_common', 'Tenancy in Common', 'property', 2,
                related_concepts=['property_concurrent']
            ),
            'property_landlord_tenant': KnowledgeNode(
                'property_landlord_tenant', 'Landlord-Tenant Law', 'property', 3,
                related_concepts=['property_leasehold']
            ),
            'property_leasehold': KnowledgeNode(
                'property_leasehold', 'Leasehold Estates', 'property', 3,
                related_concepts=['property_landlord_tenant']
            ),
            'property_conveyancing': KnowledgeNode(
                'property_conveyancing', 'Land Conveyancing', 'property', 4,
                related_concepts=['property_recording', 'property_deeds']
            ),
            'property_deeds': KnowledgeNode(
                'property_deeds', 'Deeds & Warranties', 'property', 3,
                related_concepts=['property_conveyancing']
            ),
            'property_recording': KnowledgeNode(
                'property_recording', 'Recording Acts', 'property', 4,
                related_concepts=['property_conveyancing']
            ),
            'property_easements': KnowledgeNode(
                'property_easements', 'Easements', 'property', 4,
                related_concepts=['property_covenants']
            ),
            'property_covenants': KnowledgeNode(
                'property_covenants', 'Covenants Running with Land', 'property', 5,
                related_concepts=['property_easements', 'property_equitable_servitudes']
            ),
            'property_equitable_servitudes': KnowledgeNode(
                'property_equitable_servitudes', 'Equitable Servitudes', 'property', 4,
                related_concepts=['property_covenants']
            ),
        }

        # Add prerequisites and relationships
        concepts['contracts_offer_acceptance'].prerequisites = ['contracts_formation']
        concepts['contracts_performance'].prerequisites = ['contracts_formation', 'contracts_offer_acceptance']
        concepts['contracts_remedies'].prerequisites = ['contracts_performance']
        concepts['contracts_part_performance'].prerequisites = ['contracts_statute_of_frauds']

        # Torts prerequisites
        concepts['torts_causation'].prerequisites = ['torts_duty', 'torts_breach']
        concepts['torts_damages'].prerequisites = ['torts_causation']
        concepts['torts_res_ipsa'].prerequisites = ['torts_breach']

        # Con Law prerequisites
        concepts['conlaw_strict_scrutiny'].prerequisites = ['conlaw_equal_protection']
        concepts['conlaw_intermediate_scrutiny'].prerequisites = ['conlaw_equal_protection']
        concepts['conlaw_procedural_dp'].prerequisites = ['conlaw_due_process']
        concepts['conlaw_substantive_dp'].prerequisites = ['conlaw_due_process']

        # Criminal Law prerequisites
        concepts['crim_murder'].prerequisites = ['crim_homicide', 'crim_mens_rea']
        concepts['crim_manslaughter'].prerequisites = ['crim_homicide']
        concepts['crim_felony_murder'].prerequisites = ['crim_murder']
        concepts['crim_conspiracy'].prerequisites = ['crim_inchoate']
        concepts['crim_attempt'].prerequisites = ['crim_inchoate']

        # Evidence prerequisites
        concepts['evidence_hearsay_exceptions'].prerequisites = ['evidence_hearsay']
        concepts['evidence_non_hearsay'].prerequisites = ['evidence_hearsay']
        concepts['evidence_impeachment'].prerequisites = ['evidence_witnesses']
        concepts['evidence_expert'].prerequisites = ['evidence_opinion']

        # Civil Procedure prerequisites
        concepts['civpro_diversity'].prerequisites = ['civpro_jurisdiction']
        concepts['civpro_federal_question'].prerequisites = ['civpro_jurisdiction']
        concepts['civpro_minimum_contacts'].prerequisites = ['civpro_personal_jurisdiction']
        concepts['civpro_12b6'].prerequisites = ['civpro_motions', 'civpro_complaint']

        # Property prerequisites
        concepts['property_future_interests'].prerequisites = ['property_estates']
        concepts['property_rap'].prerequisites = ['property_future_interests']
        concepts['property_recording'].prerequisites = ['property_conveyancing']

        self.knowledge_graph = concepts

        # Validate knowledge graph integrity
        self._validate_knowledge_graph()

    def _validate_knowledge_graph(self):
        """
        Validate knowledge graph integrity - catch typos and broken prerequisites
        """
        errors = []

        # Check that all prerequisite IDs exist
        for concept_id, concept in self.knowledge_graph.items():
            for prereq_id in concept.prerequisites:
                if prereq_id not in self.knowledge_graph:
                    errors.append(f"Broken prerequisite: {concept_id} requires non-existent {prereq_id}")

        # Check for circular dependencies (basic check)
        visited = set()
        for concept_id in self.knowledge_graph:
            if self._has_circular_dependency(concept_id, visited, set()):
                errors.append(f"Circular dependency detected involving {concept_id}")

        if errors:
            print("⚠️ Knowledge Graph Validation Errors:")
            for error in errors:
                print(f"  • {error}")
        else:
            print("✅ Knowledge graph validation passed")

    def _has_circular_dependency(self, concept_id, visited, current_path):
        """Check for circular dependencies using DFS"""
        if concept_id in current_path:
            return True
        if concept_id in visited:
            return False

        current_path.add(concept_id)
        for prereq_id in self.knowledge_graph[concept_id].prerequisites:
            if prereq_id in self.knowledge_graph and self._has_circular_dependency(prereq_id, visited, current_path):
                return True

        current_path.remove(concept_id)
        visited.add(concept_id)
        return False

    def adaptive_difficulty_algorithm(self, performance_history: List[Dict]) -> str:
        """
        Adaptive difficulty adjustment based on performance patterns
        Uses Bayesian Knowledge Tracing and Elo rating system concepts
        """
        if not performance_history:
            return 'intermediate'

        recent_performance = performance_history[-10:]  # Last 10 questions
        
        # Handle both 'correct' and 'accuracy' keys, default to True if missing
        accuracy = sum(1 for p in recent_performance if p.get('correct', p.get('accuracy', True))) / len(recent_performance)

        # Adjust difficulty based on accuracy and streak
        if accuracy >= 0.85 and self.adaptive_difficulty['success_streak'] >= 3:
            self.adaptive_difficulty['success_streak'] += 1
            if self.adaptive_difficulty['current_level'] != 'expert':
                self.adaptive_difficulty['current_level'] = 'advanced'
        elif accuracy >= 0.70:
            self.adaptive_difficulty['success_streak'] += 1
        elif accuracy < 0.50:
            self.adaptive_difficulty['failure_streak'] += 1
            if self.adaptive_difficulty['failure_streak'] >= 2:
                if self.adaptive_difficulty['current_level'] != 'foundational':
                    self.adaptive_difficulty['current_level'] = 'intermediate'
        else:
            # Reset streaks for mixed performance
            self.adaptive_difficulty['success_streak'] = 0
            self.adaptive_difficulty['failure_streak'] = 0

        return self.adaptive_difficulty['current_level']

    def spaced_repetition_scheduler(self, concept: KnowledgeNode) -> bool:
        """
        SM-2 spaced repetition algorithm
        Returns True if concept should be reviewed today
        """
        if not concept.last_reviewed:
            return True  # New concept

        days_since_review = (datetime.now() - concept.last_reviewed).days
        return days_since_review >= concept.interval

    def interleaved_practice_generator(self, subject: str, count: int = 10) -> List[Dict]:
        """
        Generate interleaved practice with GUARANTEED unique concepts

        FIXED: No more duplicate concepts in practice sets
        """
        print(f"\n🔄 Generating Interleaved Practice - {subject.upper()}")
        print("=" * 60)

        # Get all concepts for subject
        available_concepts = [
            node for node in self.knowledge_graph.values()
            if node.subject.lower() == subject.lower()
        ]

        if not available_concepts:
            raise ValueError(f"No concepts found for subject: {subject}")

        # CRITICAL FIX: Ensure we don't request more than available
        if count > len(available_concepts):
            print(f"⚠️  Requested {count} questions but only {len(available_concepts)} concepts available")
            count = len(available_concepts)

        # Calculate priority weights for each concept
        concept_weights = []
        for concept in available_concepts:
            # Higher weight for lower mastery
            weight = (1.5 - concept.mastery_level)

            # Higher weight if overdue for review
            if concept.last_reviewed:
                days_since = (datetime.now() - concept.last_reviewed).days
                if days_since > concept.interval:
                    weight *= 2.0

            concept_weights.append((concept, weight))

        # Stratify by difficulty
        easy = [(c, w) for c, w in concept_weights if c.difficulty <= 2]
        medium = [(c, w) for c, w in concept_weights if c.difficulty == 3]
        hard = [(c, w) for c, w in concept_weights if c.difficulty >= 4]

        # Calculate how many from each stratum
        easy_count = max(1, int(count * 0.25))
        medium_count = max(1, int(count * 0.50))
        hard_count = count - easy_count - medium_count

        # Sample WITHOUT replacement (key fix)
        selected = []
        selected.extend(self._weighted_sample_unique(easy, easy_count))
        selected.extend(self._weighted_sample_unique(medium, medium_count))
        selected.extend(self._weighted_sample_unique(hard, hard_count))

        # Take exactly count
        selected = selected[:count]

        # Shuffle to prevent difficulty clustering
        random.shuffle(selected)

        # Display results
        print(f"\nSelected {len(selected)} UNIQUE concepts for practice:")
        for concept in selected:
            icon = '🆕' if concept.mastery_level < 0.3 else '📈' if concept.mastery_level < 0.7 else '✅'
            print(f"   {icon} {concept.name} (Mastery: {concept.mastery_level*100:.0f}%, Difficulty: {concept.difficulty}/5)")

        # Show difficulty distribution
        dist = {'easy': 0, 'medium': 0, 'hard': 0}
        for c in selected:
            if c.difficulty <= 2:
                dist['easy'] += 1
            elif c.difficulty == 3:
                dist['medium'] += 1
            else:
                dist['hard'] += 1

        print(f"\n📊 Difficulty Distribution: Easy({dist['easy']}) | Medium({dist['medium']}) | Hard({dist['hard']})")

        return selected

    def _weighted_sample_unique(self, weighted_concepts: List[Tuple], n: int) -> List:
        """
        Sample concepts with weights, WITHOUT replacement

        This ensures no duplicates
        """
        if not weighted_concepts:
            return []

        if n >= len(weighted_concepts):
            # Return all concepts if we need more than available
            return [concept for concept, weight in weighted_concepts]

        selected = []
        remaining = list(weighted_concepts)

        for _ in range(n):
            if not remaining:
                break

            # Calculate total weight of remaining concepts
            total_weight = sum(weight for _, weight in remaining)

            # Weighted random selection
            rand = random.uniform(0, total_weight)
            cumulative = 0

            for i, (concept, weight) in enumerate(remaining):
                cumulative += weight
                if rand <= cumulative:
                    selected.append(concept)
                    # CRITICAL: Remove from remaining to prevent duplicates
                    remaining.pop(i)
                    break

        return selected

    def elaborative_interrogation_engine(self, question: Dict, user_answer: str, is_correct: bool) -> Dict:
        """
        Implement elaborative interrogation - force deeper thinking about why/how rules work
        Based on research showing this significantly improves retention and understanding
        """
        subject = question.get('subject', 'general')

        # Base interrogation prompts that force causal reasoning
        base_prompts = {
            'why': "WHY does this legal rule exist? What policy rationale supports it?",
            'how': "HOW does this principle interact with related concepts in this subject?",
            'when': "WHEN would the result differ? What exceptions or distinctions apply?",
            'what_if': "WHAT IF the facts were slightly different? How would that change the analysis?"
        }

        # Subject-specific elaborative questions
        subject_specific = {
            'contracts': {
                'why': "Why does contract law require consideration, offer, and acceptance?",
                'how': "How does this contract principle relate to remedies available if breached?",
                'when': "When might a court imply terms or find a contract despite missing elements?",
                'what_if': "What if parties partially performed - does that change enforceability?"
            },
            'torts': {
                'why': "Why does tort law balance individual rights with reasonable behavior expectations?",
                'how': "How does this tort concept relate to available defenses and damages?",
                'when': "When might strict liability apply instead of negligence analysis?",
                'what_if': "What if multiple defendants contributed - how does causation work?"
            },
            'constitutional_law': {
                'why': "Why does this constitutional protection exist and what rights does it safeguard?",
                'how': "How does this constitutional principle interact with government powers?",
                'when': "When would courts apply strict scrutiny vs. rational basis review?",
                'what_if': "What if this were a state vs. federal government action?"
            }
        }

        # Get subject-specific prompts or fall back to general
        prompts = subject_specific.get(subject, base_prompts)

        # Generate follow-up questions based on correctness and answer type
        follow_ups = []

        if is_correct:
            # Even correct answers benefit from deeper analysis
            follow_ups = [
                prompts['why'],
                prompts['how'],
                "Can you think of a real-world example where this principle applies?",
                "How might this rule be tested on the bar exam?"
            ]
        else:
            # Incorrect answers get diagnostic follow-ups
            error_type = self._categorize_error(question, user_answer)
            follow_ups = [
                f"Let's diagnose: {error_type['analysis']}",
                "What rule did you think applied here?",
                prompts['when'],  # When would this be different?
                "How would you approach this differently next time?"
            ]

        return {
            'interrogation_prompts': follow_ups,
            'subject_specific': subject in subject_specific,
            'cognitive_level': 'deep_processing' if is_correct else 'error_correction'
        }

    def _categorize_error(self, question: Dict, wrong_answer: str) -> Dict:
        """
        Categorize the type of error for targeted remediation
        Type A: Issue-spotting failure
        Type B: Rule-application error
        Type C: Distractor susceptibility
        """
        correct_answer = question.get('answer', '')
        options = question.get('options', {})

        # Simple heuristic for error categorization
        if wrong_answer in ['A', 'B', 'C', 'D']:
            wrong_text = options.get(wrong_answer, '').lower()
            correct_text = options.get(correct_answer, '').lower()

            # Type A: Completely missed the issue
            if any(word in wrong_text for word in ['irrelevant', 'unrelated', 'none']):
                return {
                    'type': 'A',
                    'analysis': 'Issue-spotting failure: You may have missed identifying the correct legal issue'
                }

            # Type B: Applied wrong rule to right issue
            elif any(word in correct_text for word in ['breach', 'negligence', 'consideration']) and wrong_answer != correct_answer:
                return {
                    'type': 'B',
                    'analysis': 'Rule-application error: You identified the issue but applied the wrong legal rule'
                }

            # Type C: Fell for distractor
            else:
                return {
                    'type': 'C',
                    'analysis': 'Distractor susceptibility: You knew the rule but were tempted by a common wrong answer'
                }

        return {
            'type': 'unknown',
            'analysis': 'Error type unclear - let\'s analyze the reasoning step by step'
        }

    def confidence_calibration_tracker(self, question: Dict, user_answer: str, confidence_rating: int, is_correct: bool) -> Dict:
        """
        Track confidence-accuracy calibration to develop metacognitive awareness
        Bar students need accurate self-assessment to avoid overconfidence traps
        """
        if not hasattr(self, 'calibration_history'):
            self.calibration_history = []

        # Store calibration data point
        calibration_point = {
            'timestamp': datetime.now(),
            'subject': question.get('subject', 'unknown'),
            'confidence': confidence_rating,  # 1-5 scale
            'correct': is_correct,
            'question_id': question.get('id', 'unknown'),
            'answer': user_answer
        }

        self.calibration_history.append(calibration_point)

        # Analyze recent calibration (last 20 questions)
        recent = self.calibration_history[-20:] if len(self.calibration_history) >= 5 else self.calibration_history

        if len(recent) >= 5:
            # Calculate calibration metrics
            high_confidence = [p for p in recent if p['confidence'] >= 4]
            high_conf_correct = sum(1 for p in high_confidence if p['correct']) / len(high_confidence) if high_confidence else 0

            low_confidence = [p for p in recent if p['confidence'] <= 2]
            low_conf_correct = sum(1 for p in low_confidence if p['correct']) / len(low_confidence) if low_confidence else 0

            overall_accuracy = sum(1 for p in recent if p['correct']) / len(recent)

            # Generate calibration feedback
            feedback = self._generate_calibration_feedback(
                high_conf_correct, low_conf_correct, overall_accuracy, confidence_rating, is_correct
            )

            return {
                'calibration_feedback': feedback,
                'current_metrics': {
                    'high_confidence_accuracy': high_conf_correct,
                    'low_confidence_accuracy': low_conf_correct,
                    'overall_accuracy': overall_accuracy,
                    'calibration_score': self._calculate_calibration_score(recent)
                },
                'needs_calibration': self._detect_calibration_issues(recent)
            }

        return {
            'calibration_feedback': "Keep tracking confidence ratings - need more data for calibration analysis",
            'current_metrics': None,
            'needs_calibration': False
        }

    def _generate_calibration_feedback(self, high_conf_acc, low_conf_acc, overall_acc, confidence, is_correct):
        """Generate personalized calibration feedback"""
        feedback_parts = []

        # Overconfidence detection
        if confidence >= 4 and not is_correct:
            feedback_parts.append("⚠️ **CALIBRATION ALERT**: You were very confident but incorrect. This suggests a conceptual blind spot.")

        # Underconfidence detection
        if confidence <= 2 and is_correct:
            feedback_parts.append("📈 **Confidence Boost**: You were unsure but correct! You're likely underestimating your knowledge.")

        # General calibration assessment
        if high_conf_acc < 0.8 and len(self.calibration_history) >= 10:
            feedback_parts.append("🎯 **Calibration Tip**: When you're very confident, you're right less than 80% of the time. Consider double-checking high-confidence answers.")

        if abs(high_conf_acc - low_conf_acc) > 0.3:
            feedback_parts.append("📊 **Calibration Gap**: Big difference between high/low confidence accuracy suggests inconsistent self-assessment.")

        # Positive reinforcement
        if high_conf_acc >= 0.9 and overall_acc >= 0.7:
            feedback_parts.append("✅ **Well Calibrated**: Your confidence ratings are well-aligned with actual performance!")

        return " ".join(feedback_parts) if feedback_parts else "Keep practicing with confidence ratings to improve self-assessment!"

    def _calculate_calibration_score(self, recent_points):
        """Calculate overall calibration score (0-1, higher is better)"""
        if not recent_points:
            return 0.5

        # Perfect calibration would mean confidence correlates perfectly with accuracy
        # This is a simplified metric
        confidence_levels = [p['confidence'] for p in recent_points]
        accuracies = [1 if p['correct'] else 0 for p in recent_points]

        # Calculate correlation-like metric
        try:
            conf_mean = mean(confidence_levels)
            acc_mean = mean(accuracies)

            # Simple correlation approximation
            numerator = sum((c - conf_mean) * (a - acc_mean) for c, a in zip(confidence_levels, accuracies))
            denominator = (stdev(confidence_levels) * stdev(accuracies)) if stdev(confidence_levels) > 0 and stdev(accuracies) > 0 else 1

            correlation = numerator / (len(recent_points) * denominator) if denominator != 0 else 0

            # Convert to 0-1 scale (correlation can be -1 to 1)
            calibration_score = (correlation + 1) / 2

            return max(0, min(1, calibration_score))  # Clamp to 0-1

        except:
            return 0.5  # Default neutral score

    def _detect_calibration_issues(self, recent_points):
        """Detect if student has calibration problems needing intervention"""
        if len(recent_points) < 10:
            return False

        high_conf = [p for p in recent_points if p['confidence'] >= 4]
        if len(high_conf) >= 3:
            high_conf_acc = sum(1 for p in high_conf if p['correct']) / len(high_conf)
            if high_conf_acc < 0.7:  # Less than 70% accuracy on high confidence answers
                return True

        return False

    def socratic_dialogue_engine(self, question: Dict, user_answer: str) -> Dict:
        """
        Implement Socratic dialogue for wrong answers
        Guides student through reasoning process
        """
        correct_answer = question.get('answer', 'A')
        explanation = question.get('why_correct', f'The correct answer is {correct_answer} because it properly applies the legal rule to these facts.')

        dialogue_steps = [
            {
                'question': f"Why did you choose answer {user_answer}?",
                'follow_up': "What rule or principle led you to that choice?"
            },
            {
                'question': f"What would be the consequence if {user_answer} were correct?",
                'follow_up': "Does that consequence make sense in this fact pattern?"
            },
            {
                'question': f"Let's look at the correct answer {correct_answer}. What rule supports this?",
                'follow_up': "How does this rule apply to these specific facts?"
            },
            {
                'question': "What key distinction are you missing here?",
                'follow_up': "How can you remember this distinction for next time?"
            }
        ]

        tested_rule = question.get('tested_rule', 'the applicable legal rule')
        subject = question.get('subject', 'general')
        subtype = question.get('subtype', 'general')

        return {
            'dialogue_steps': dialogue_steps,
            'key_insight': f"The critical issue is: {tested_rule}",
            'remediation_strategy': self.generate_remediation_strategy(subject, subtype)
        }

    def generate_remediation_strategy(self, subject: str, topic: str) -> Dict:
        """Generate personalized remediation strategies"""
        strategies = {
            'contracts': {
                'formation': ['Review UCC §2-205 firm offers', 'Practice battle of the forms scenarios'],
                'remedies': ['Compare expectation vs reliance vs restitution', 'Calculate damages in hypotheticals'],
            },
            'torts': {
                'negligence': ['Map duty → breach → causation → damages', 'Practice proximate cause distinctions'],
                'defamation': ['Distinguish defamation vs opinion vs privilege', 'Analyze public vs private figures'],
            },
            'constitutional_law': {
                'equal_protection': ['Apply tiered scrutiny framework', 'Practice suspect vs quasi-suspect classifications'],
                'due_process': ['Distinguish procedural vs substantive', 'Analyze fundamental rights triggers'],
            }
        }

        return strategies.get(subject, {}).get(topic, ['Review subject outline', 'Practice 10 similar questions'])

    def concept_mapping_visualizer(self, subject: str) -> Dict:
        """
        Generate visual concept map for a subject
        """
        subject_concepts = [c for c in self.knowledge_graph.values() if c.subject == subject]

        # Create adjacency matrix for concept relationships
        concept_names = [c.name for c in subject_concepts]
        relationships = {}

        for concept in subject_concepts:
            relationships[concept.name] = {
                'prerequisites': [self.knowledge_graph[pid].name for pid in concept.prerequisites if pid in self.knowledge_graph],
                'related': [self.knowledge_graph[rid].name for rid in concept.related_concepts if rid in self.knowledge_graph],
                'difficulty': concept.difficulty,
                'mastery': concept.mastery_level
            }

        return {
            'subject': subject,
            'concepts': concept_names,
            'relationships': relationships,
            'visualization_type': 'network_graph',
            'ascii_art': self.generate_concept_map_ascii(subject_concepts, relationships)
        }

    def generate_concept_map_ascii(self, concepts: List[KnowledgeNode], relationships: Dict) -> str:
        """Generate ASCII art concept map"""
        lines = []
        lines.append(f"📚 {concepts[0].subject.upper()} CONCEPT MAP")
        lines.append("=" * 50)

        for concept in concepts:
            mastery_indicator = "🟢" if concept.mastery_level > 0.7 else "🟡" if concept.mastery_level > 0.4 else "🔴"
            lines.append(f"{mastery_indicator} {concept.name} (Difficulty: {concept.difficulty})")

            if concept.prerequisites:
                lines.append(f"  └── Prerequisites: {', '.join(relationships[concept.name]['prerequisites'])}")

            if concept.related_concepts:
                lines.append(f"  └── Related: {', '.join(relationships[concept.name]['related'])}")

            lines.append("")

        return "\n".join(lines)

    def generate_personalized_study_plan(self, user_performance: Dict) -> Dict:
        """
        Generate comprehensive study plan using all pedagogical techniques
        """
        weak_subjects = user_performance.get('weak_subjects', [])
        time_available = user_performance.get('study_hours_per_week', 20)
        exam_date = user_performance.get('exam_date', datetime.now() + timedelta(days=90))

        weeks_until_exam = max(1, (exam_date - datetime.now()).days // 7)

        plan = {
            'total_weeks': weeks_until_exam,
            'focus_subjects': weak_subjects,
            'daily_structure': {
                'morning_session': {
                    'duration': 90,  # minutes
                    'mode': LearningMode.SPACED_REPETITION,
                    'strategy': CognitiveStrategy.SPACING
                },
                'afternoon_session': {
                    'duration': 90,
                    'mode': LearningMode.INTERLEAVED_PRACTICE,
                    'strategy': CognitiveStrategy.INTERLEAVING
                },
                'evening_session': {
                    'duration': 60,
                    'mode': LearningMode.CONCEPT_MAPPING,
                    'strategy': CognitiveStrategy.DUAL_CODING
                }
            },
            'weekly_milestones': self.generate_weekly_milestones(weak_subjects, weeks_until_exam),
            'adaptive_goals': self.generate_adaptive_goals(user_performance),
            'cognitive_strategies_schedule': self.schedule_cognitive_strategies(weeks_until_exam)
        }

        return plan

    def generate_weekly_milestones(self, weak_subjects: List[str], weeks: int) -> List[Dict]:
        """Generate progressive weekly milestones"""
        milestones = []

        for week in range(1, weeks + 1):
            milestone = {
                'week': week,
                'focus': weak_subjects[week % len(weak_subjects)] if weak_subjects else 'mixed_review',
                'questions_target': 50 + (week * 10),  # Progressive increase
                'accuracy_target': min(70 + (week * 2), 90),  # Progressive accuracy
                'techniques': self.get_week_techniques(week)
            }
            milestones.append(milestone)

        return milestones

    def get_week_techniques(self, week: int) -> List[str]:
        """Get recommended techniques for each week"""
        techniques_by_week = {
            1: ['Focused Practice', 'Self-Explanation'],
            2: ['Interleaved Practice', 'Dual Coding'],
            3: ['Retrieval Practice', 'Concept Mapping'],
            4: ['Spaced Repetition', 'Elaboration'],
            5: ['Diagnostic Assessment', 'Socratic Dialogue'],
            6: ['Adaptive Difficulty', 'Generation'],
        }

        return techniques_by_week.get(week % 6 + 1, ['Mixed Techniques'])

    def generate_adaptive_goals(self, performance: Dict) -> Dict:
        """Generate adaptive goals based on current performance"""
        current_accuracy = performance.get('overall_accuracy', 0.65)
        current_speed = performance.get('avg_time_per_question', 120)  # seconds

        goals = {
            'accuracy_target': min(current_accuracy + 0.05, 0.85),
            'speed_target': max(current_speed - 5, 90),  # seconds
            'weak_subject_improvement': '15% accuracy increase',
            'consistency_target': 'Maintain 70%+ accuracy across all subjects'
        }

        return goals

    def schedule_cognitive_strategies(self, weeks: int) -> Dict:
        """Schedule cognitive strategies throughout study period"""
        schedule = {}

        for week in range(1, weeks + 1):
            week_strategies = []

            # Alternate strategies each week
            if week % 4 == 1:
                week_strategies.extend([CognitiveStrategy.SPACING, CognitiveStrategy.TESTING])
            elif week % 4 == 2:
                week_strategies.extend([CognitiveStrategy.INTERLEAVING, CognitiveStrategy.ELABORATION])
            elif week % 4 == 3:
                week_strategies.extend([CognitiveStrategy.DUAL_CODING, CognitiveStrategy.SELF_EXPLANATION])
            else:
                week_strategies.extend([CognitiveStrategy.GENERATION, CognitiveStrategy.SPACING])

            schedule[f'week_{week}'] = week_strategies

        return schedule

    def meta_cognition_reflection(self, session: StudySession) -> Dict:
        """
        Generate meta-cognition reflection prompts
        """
        reflection_questions = [
            "What learning strategies worked well today?",
            "What concepts are still confusing?",
            "How confident do you feel about today's material?",
            "What could you do differently tomorrow?",
            "Are you spacing out your study sessions effectively?",
            "How well are you interleaving different subjects?"
        ]

        insights = {
            'session_quality_score': self.calculate_session_quality(session),
            'recommended_adjustments': self.generate_session_adjustments(session),
            'reflection_questions': reflection_questions,
            'progress_toward_goals': self.assess_goal_progress(session)
        }

        return insights

    def calculate_session_quality(self, session: StudySession) -> float:
        """Calculate session quality score (0-1)"""
        # Handle empty sessions gracefully
        if session.questions_attempted == 0:
            return 0.5  # Neutral score for empty sessions
        
        factors = {
            'accuracy': session.questions_correct / max(session.questions_attempted, 1),
            'time_efficiency': min(session.time_spent / max((session.questions_attempted * 90), 1), 1),  # 90 sec target
            'strategies_used': min(len(session.cognitive_strategies_used) / 3, 1),  # Normalize to 3 strategies
            'confidence': sum(session.confidence_ratings) / max(len(session.confidence_ratings), 1) / 5 if session.confidence_ratings else 0.5
        }

        # Weighted average
        weights = {'accuracy': 0.4, 'time_efficiency': 0.2, 'strategies_used': 0.2, 'confidence': 0.2}
        quality_score = sum(factors[key] * weights[key] for key in factors)

        return min(quality_score, 1.0)

    def generate_session_adjustments(self, session: StudySession) -> List[str]:
        """Generate specific adjustments based on session performance"""
        adjustments = []

        accuracy = session.questions_correct / max(session.questions_attempted, 1)

        if accuracy < 0.6:
            adjustments.append("Focus on foundational concepts before advanced topics")
        elif accuracy > 0.85:
            adjustments.append("Increase difficulty or move to interleaved practice")

        avg_time = session.time_spent / max(session.questions_attempted, 1)
        if avg_time > 120:
            adjustments.append("Work on time management - aim for 90-108 seconds per question")
        elif avg_time < 60:
            adjustments.append("Slow down and focus on deep understanding, not speed")

        if len(session.cognitive_strategies_used) < 2:
            adjustments.append("Incorporate more cognitive strategies (dual coding, self-explanation)")

        return adjustments if adjustments else ["Continue current approach - you're performing well!"]

    def assess_goal_progress(self, session: StudySession) -> Dict:
        """Assess progress toward long-term goals"""
        # This would integrate with long-term performance tracking
        return {
            'weekly_accuracy_trend': 'improving',
            'subjects_mastered': [],
            'subjects_needing_work': [],
            'overall_progress': 0.65  # percentage to goal
        }

#!/usr/bin/env python3
"""
Import script to convert KnowledgeNode concepts into Adaptive Learning System cards

This script reads concepts from bar_tutor_unified.py (or similar) and converts them
into the new adaptive learning card format with proper enum mappings.
"""

import sys
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime

# Import the adaptive learning system
from adaptive_learning_system import (
    AdaptiveLearningSystem,
    Subject,
    ConstitutionalLawTopic,
    EvidenceTopic,
    DifficultyLevel,
)


# ============================================================================
# KNOWLEDGENODE DEFINITION (from bar_tutor_unified.py)
# ============================================================================

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


# ============================================================================
# SUBJECT MAPPING
# ============================================================================

SUBJECT_MAP = {
    "civil_procedure": Subject.CIVIL_PROCEDURE,
    "constitutional_law": Subject.CONSTITUTIONAL_LAW,
    "contracts": Subject.CONTRACTS,
    "torts": Subject.TORTS,
    "criminal_law": Subject.CRIMINAL_LAW,
    "criminal_procedure": Subject.CRIMINAL_PROCEDURE,
    "evidence": Subject.EVIDENCE,
    "real_property": Subject.REAL_PROPERTY,
    # Aliases
    "civpro": Subject.CIVIL_PROCEDURE,
    "conlaw": Subject.CONSTITUTIONAL_LAW,
    "crim": Subject.CRIMINAL_LAW,
    "crimpro": Subject.CRIMINAL_PROCEDURE,
}


# ============================================================================
# TOPIC MAPPING (Intelligent matching)
# ============================================================================

CONSTITUTIONAL_LAW_KEYWORDS = {
    ConstitutionalLawTopic.JUDICIAL_REVIEW: ["judicial review", "marbury"],
    ConstitutionalLawTopic.JUSTICIABILITY: ["justiciability", "case or controversy"],
    ConstitutionalLawTopic.STANDING: ["standing", "injury", "redressability"],
    ConstitutionalLawTopic.MOOTNESS: ["mootness", "moot"],
    ConstitutionalLawTopic.RIPENESS: ["ripeness", "ripe"],

    ConstitutionalLawTopic.COMMERCE_CLAUSE: ["commerce clause", "commerce power"],
    ConstitutionalLawTopic.TAXING_SPENDING: ["taxing", "spending power"],
    ConstitutionalLawTopic.NECESSARY_AND_PROPER: ["necessary and proper", "necessary & proper"],
    ConstitutionalLawTopic.TREATY_POWER: ["treaty"],
    ConstitutionalLawTopic.WAR_POWERS: ["war powers"],

    ConstitutionalLawTopic.PROCEDURAL_DUE_PROCESS: ["procedural due process", "notice and hearing"],
    ConstitutionalLawTopic.SUBSTANTIVE_DUE_PROCESS: ["substantive due process"],
    ConstitutionalLawTopic.INCORPORATION: ["incorporation", "bill of rights"],
    ConstitutionalLawTopic.FUNDAMENTAL_RIGHTS: ["fundamental rights"],

    ConstitutionalLawTopic.EQUAL_PROTECTION: ["equal protection"],
    ConstitutionalLawTopic.STRICT_SCRUTINY: ["strict scrutiny", "compelling interest"],
    ConstitutionalLawTopic.INTERMEDIATE_SCRUTINY: ["intermediate scrutiny"],
    ConstitutionalLawTopic.RATIONAL_BASIS: ["rational basis"],
    ConstitutionalLawTopic.SUSPECT_CLASSIFICATIONS: ["suspect classification", "race", "national origin"],
    ConstitutionalLawTopic.QUASI_SUSPECT_CLASSIFICATIONS: ["quasi-suspect", "gender", "sex", "legitimacy"],

    ConstitutionalLawTopic.FREEDOM_OF_SPEECH: ["freedom of speech", "first amendment speech"],
    ConstitutionalLawTopic.FREEDOM_OF_RELIGION: ["freedom of religion"],
    ConstitutionalLawTopic.ESTABLISHMENT_CLAUSE: ["establishment clause"],
    ConstitutionalLawTopic.FREE_EXERCISE_CLAUSE: ["free exercise"],
    ConstitutionalLawTopic.FREEDOM_OF_PRESS: ["freedom of press"],
    ConstitutionalLawTopic.FREEDOM_OF_ASSEMBLY: ["freedom of assembly"],

    ConstitutionalLawTopic.TAKINGS_CLAUSE: ["takings", "eminent domain"],
    ConstitutionalLawTopic.PRIVILEGES_AND_IMMUNITIES: ["privileges", "immunities"],
    ConstitutionalLawTopic.DORMANT_COMMERCE_CLAUSE: ["dormant commerce"],
    ConstitutionalLawTopic.STATE_ACTION: ["state action"],
}

EVIDENCE_KEYWORDS = {
    EvidenceTopic.RELEVANCE: ["relevance", "relevant"],
    EvidenceTopic.LOGICAL_RELEVANCE: ["logical relevance", "fre 401"],
    EvidenceTopic.LEGAL_RELEVANCE_403: ["403", "unfair prejudice"],

    EvidenceTopic.CHARACTER_EVIDENCE: ["character evidence"],
    EvidenceTopic.PRIOR_BAD_ACTS_404B: ["404(b)", "prior bad acts"],
    EvidenceTopic.HABIT_EVIDENCE: ["habit"],

    EvidenceTopic.HEARSAY_DEFINITION: ["hearsay definition", "out of court statement"],
    EvidenceTopic.HEARSAY_EXCEPTIONS_803: ["803"],
    EvidenceTopic.HEARSAY_EXCEPTIONS_804: ["804"],
    EvidenceTopic.PRESENT_SENSE_IMPRESSION: ["present sense impression"],
    EvidenceTopic.EXCITED_UTTERANCE: ["excited utterance"],
    EvidenceTopic.STATE_OF_MIND: ["state of mind", "then existing"],
    EvidenceTopic.MEDICAL_DIAGNOSIS: ["medical diagnosis"],
    EvidenceTopic.RECORDED_RECOLLECTION: ["recorded recollection", "past recollection"],
    EvidenceTopic.BUSINESS_RECORDS: ["business records"],
    EvidenceTopic.PUBLIC_RECORDS: ["public records"],
    EvidenceTopic.FORMER_TESTIMONY: ["former testimony"],
    EvidenceTopic.DYING_DECLARATION: ["dying declaration"],
    EvidenceTopic.STATEMENT_AGAINST_INTEREST: ["statement against interest"],

    EvidenceTopic.CONFRONTATION_CLAUSE: ["confrontation"],

    EvidenceTopic.IMPEACHMENT: ["impeachment", "impeach"],
    EvidenceTopic.PRIOR_INCONSISTENT_STATEMENT: ["prior inconsistent"],
    EvidenceTopic.BIAS_MOTIVE: ["bias", "motive"],
    EvidenceTopic.CHARACTER_FOR_TRUTHFULNESS: ["truthfulness", "veracity"],
    EvidenceTopic.CRIMINAL_CONVICTIONS: ["criminal conviction", "felony"],

    EvidenceTopic.ATTORNEY_CLIENT: ["attorney-client", "attorney client"],
    EvidenceTopic.SPOUSAL_PRIVILEGES: ["spousal", "marital"],
    EvidenceTopic.DOCTOR_PATIENT: ["doctor-patient", "physician"],

    EvidenceTopic.EXPERT_QUALIFICATIONS: ["expert qualifications"],
    EvidenceTopic.DAUBERT_STANDARD: ["daubert"],

    EvidenceTopic.AUTHENTICATION: ["authentication", "authenticate"],
    EvidenceTopic.BEST_EVIDENCE_RULE: ["best evidence", "original writing"],
}


def map_to_topic(concept: KnowledgeNode) -> str:
    """
    Intelligently map a concept to a specific topic enum value

    Uses keyword matching on concept_id, name, and rule_statement
    """
    subject = concept.subject.lower()
    search_text = f"{concept.concept_id} {concept.name} {concept.rule_statement}".lower()

    if "constitutional" in subject or "conlaw" in subject:
        # Try to match Constitutional Law topics
        for topic, keywords in CONSTITUTIONAL_LAW_KEYWORDS.items():
            if any(keyword.lower() in search_text for keyword in keywords):
                return topic.value
        # Default to general federal powers
        if "federal" in search_text or "legislative" in search_text:
            return ConstitutionalLawTopic.COMMERCE_CLAUSE.value
        elif "executive" in search_text:
            return ConstitutionalLawTopic.TREATY_POWER.value
        elif "first amendment" in search_text:
            return ConstitutionalLawTopic.FREEDOM_OF_SPEECH.value
        elif "due process" in search_text:
            return ConstitutionalLawTopic.PROCEDURAL_DUE_PROCESS.value
        elif "equal protection" in search_text:
            return ConstitutionalLawTopic.EQUAL_PROTECTION.value
        else:
            return ConstitutionalLawTopic.JUDICIAL_REVIEW.value

    elif "evidence" in subject:
        # Try to match Evidence topics
        for topic, keywords in EVIDENCE_KEYWORDS.items():
            if any(keyword.lower() in search_text for keyword in keywords):
                return topic.value
        # Default to relevance
        return EvidenceTopic.RELEVANCE.value

    else:
        # For other subjects, use the concept name as the topic
        return concept.name.lower().replace(" ", "_")


# ============================================================================
# CARD GENERATION
# ============================================================================

class CardGenerator:
    """Generate multiple cards from a single KnowledgeNode"""

    def __init__(self, system: AdaptiveLearningSystem):
        self.system = system
        self.cards_created = 0

    def generate_cards_from_node(self, node: KnowledgeNode) -> int:
        """
        Generate multiple cards from a KnowledgeNode
        Returns number of cards created
        """
        cards_before = self.cards_created

        # Map subject
        if node.subject not in SUBJECT_MAP:
            print(f"⚠️  Skipping {node.name} - unknown subject: {node.subject}")
            return 0

        subject = SUBJECT_MAP[node.subject]
        topic = map_to_topic(node)
        difficulty = self._map_difficulty(node.difficulty)

        # 1. Rule Statement Card (if present)
        if node.rule_statement:
            self._create_card(
                subject=subject,
                topic=topic,
                concept_name=node.name,
                question=f"State the rule for: {node.name}",
                answer=node.rule_statement,
                difficulty=difficulty,
                tags=["rule_statement"]
            )

        # 2. Elements Card (if present)
        if node.elements and not all(e in ["Mnemonic", "Traps", "Visual", "Rule", "Micro-Hypos"] for e in node.elements):
            # Filter out metadata elements
            real_elements = [e for e in node.elements if e not in ["Mnemonic", "Traps", "Visual", "Rule", "Micro-Hypos"]]
            if real_elements:
                elements_answer = "\n".join(f"{i}. {elem}" for i, elem in enumerate(real_elements, 1))
                self._create_card(
                    subject=subject,
                    topic=topic,
                    concept_name=f"{node.name} - Elements",
                    question=f"What are the elements of {node.name}?",
                    answer=elements_answer,
                    difficulty=difficulty,
                    tags=["elements"]
                )

        # 3. Common Traps Card (if present)
        if node.common_traps:
            traps_answer = "\n".join(f"⚠️  {trap}" for trap in node.common_traps)
            self._create_card(
                subject=subject,
                topic=topic,
                concept_name=f"{node.name} - Traps",
                question=f"What are common exam traps for {node.name}?",
                answer=traps_answer,
                difficulty=DifficultyLevel.ADVANCED,  # Traps are always harder
                tags=["traps", "exam_strategy"]
            )

        # 4. Exceptions Card (if present)
        if node.exceptions:
            exceptions_answer = "\n".join(f"• {exc}" for exc in node.exceptions)
            self._create_card(
                subject=subject,
                topic=topic,
                concept_name=f"{node.name} - Exceptions",
                question=f"What are the exceptions to {node.name}?",
                answer=exceptions_answer,
                difficulty=difficulty,
                tags=["exceptions"]
            )

        # 5. Policy Rationales Card (if present)
        if node.policy_rationales:
            policy_answer = "\n".join(f"• {policy}" for policy in node.policy_rationales)
            self._create_card(
                subject=subject,
                topic=topic,
                concept_name=f"{node.name} - Policy",
                question=f"What policy rationales support {node.name}?",
                answer=policy_answer,
                difficulty=difficulty,
                tags=["policy"]
            )

        return self.cards_created - cards_before

    def _create_card(self, subject, topic, concept_name, question, answer, difficulty, tags):
        """Create a single card"""
        try:
            # Create a mock enum-like object for topics that don't have specific enums
            class MockTopic:
                def __init__(self, value):
                    self.value = value

            topic_enum = MockTopic(topic)

            self.system.add_card(
                subject=subject,
                topic=topic_enum,
                concept_name=concept_name,
                question=question,
                answer=answer,
                difficulty=difficulty,
                tags=tags
            )
            self.cards_created += 1
        except Exception as e:
            print(f"⚠️  Error creating card for {concept_name}: {e}")

    def _map_difficulty(self, old_difficulty: int) -> DifficultyLevel:
        """Map 1-5 difficulty to DifficultyLevel enum"""
        if old_difficulty <= 1:
            return DifficultyLevel.FOUNDATIONAL
        elif old_difficulty == 2:
            return DifficultyLevel.INTERMEDIATE
        elif old_difficulty == 3:
            return DifficultyLevel.INTERMEDIATE
        elif old_difficulty == 4:
            return DifficultyLevel.ADVANCED
        else:
            return DifficultyLevel.BAR_EXAM_LEVEL


# ============================================================================
# IMPORT FROM KNOWLEDGE BASE
# ============================================================================

def import_from_knowledge_base(db_path: str = "bar_prep_adaptive.db"):
    """
    Import all concepts from a knowledge base into adaptive learning system

    This is a template - you'll need to adapt it to load your specific knowledge base
    """
    print("=" * 70)
    print("IMPORT KNOWLEDGE BASE TO ADAPTIVE LEARNING SYSTEM")
    print("=" * 70)

    # Initialize adaptive learning system
    system = AdaptiveLearningSystem(db_path)
    generator = CardGenerator(system)

    # Example: Import from ultimate_knowledge_base.py structure
    # You'll need to actually load your knowledge graph here

    print("\n📚 Example: Importing Civil Procedure concepts...")

    # These would come from your actual knowledge base
    example_concepts = [
        KnowledgeNode(
            concept_id="civil_procedure_subject_matter_jurisdiction",
            name="Subject-Matter Jurisdiction",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="Federal courts need subject-matter jurisdiction via federal question, diversity exceeding $75,000 with complete diversity, or supplemental claims sharing common nucleus with anchor.",
            elements=['Federal Question', 'Diversity', 'Supplemental Jurisdiction', 'Removal/Remand'],
            policy_rationales=['Protects state sovereignty', 'Ensures federal court competence'],
            common_traps=[
                'Complete diversity required',
                'Amount in controversy aggregation rules',
                'Supplemental jurisdiction exceptions'
            ],
        ),
        KnowledgeNode(
            concept_id="constitutional_law_strict_scrutiny",
            name="Strict Scrutiny",
            subject="constitutional_law",
            difficulty=4,
            rule_statement="Government must prove a compelling governmental interest and narrowly tailored means to achieve that interest.",
            elements=['Compelling Interest', 'Narrowly Tailored', 'Least Restrictive Means'],
            policy_rationales=['Protects fundamental rights', 'Guards against discrimination'],
            common_traps=[
                'Overinclusive laws fail narrow tailoring',
                'Facially neutral laws can still trigger',
                'Not the same as intermediate scrutiny'
            ],
        ),
    ]

    total_nodes = 0
    total_cards = 0

    for node in example_concepts:
        total_nodes += 1
        cards = generator.generate_cards_from_node(node)
        total_cards += cards
        if cards > 0:
            print(f"✓ {node.name}: {cards} cards created")

    # Get final statistics
    stats = system.get_statistics()

    print("\n" + "=" * 70)
    print("IMPORT COMPLETE")
    print("=" * 70)
    print(f"📊 Concepts Processed: {total_nodes}")
    print(f"📊 Cards Created: {total_cards}")
    print(f"📊 Total Cards in System: {stats['total_cards']}")
    print(f"📊 By Subject:")
    for subject, count in stats['cards_by_subject'].items():
        print(f"     {subject}: {count} cards")

    system.close()
    print(f"\n✅ Database saved to: {db_path}")


# ============================================================================
# IMPORT FROM ACTUAL FILES
# ============================================================================

def import_from_actual_knowledge_base(
    knowledge_base_module: str = "bar_tutor_unified",
    db_path: str = "bar_prep_adaptive.db"
):
    """
    Import from actual knowledge base by loading the module

    Usage:
        python import_knowledge_to_adaptive.py bar_tutor_unified bar_prep.db
    """
    print("=" * 70)
    print("IMPORT FROM ACTUAL KNOWLEDGE BASE")
    print("=" * 70)
    print(f"Source: {knowledge_base_module}")
    print(f"Target: {db_path}")
    print("=" * 70)

    try:
        # Dynamically import the module
        import importlib
        kb_module = importlib.import_module(knowledge_base_module)

        # Try to find the knowledge graph
        if hasattr(kb_module, 'LegalKnowledgeGraph'):
            kg = kb_module.LegalKnowledgeGraph()
            print(f"\n✓ Loaded LegalKnowledgeGraph with {len(kg.nodes)} concepts")

            # Import all nodes
            system = AdaptiveLearningSystem(db_path)
            generator = CardGenerator(system)

            total_cards = 0
            by_subject = {}

            for concept_id, node in kg.nodes.items():
                cards = generator.generate_cards_from_node(node)
                total_cards += cards

                subject = node.subject
                by_subject[subject] = by_subject.get(subject, 0) + cards

                if cards > 0:
                    print(f"✓ {node.name}: {cards} cards")

            stats = system.get_statistics()

            print("\n" + "=" * 70)
            print("IMPORT COMPLETE")
            print("=" * 70)
            print(f"📊 Total Cards Created: {total_cards}")
            print(f"📊 Total Cards in System: {stats['total_cards']}")
            print(f"\n📊 By Subject:")
            for subject, count in by_subject.items():
                print(f"     {subject}: {count} cards")

            system.close()
            print(f"\n✅ Database saved to: {db_path}")

        else:
            print(f"⚠️  Could not find LegalKnowledgeGraph in {knowledge_base_module}")
            print("    Available attributes:", dir(kb_module))

    except ImportError as e:
        print(f"❌ Could not import {knowledge_base_module}: {e}")
        print("    Make sure the module is in your Python path")
    except Exception as e:
        print(f"❌ Error during import: {e}")
        import traceback
        traceback.print_exc()


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Import KnowledgeNode concepts into Adaptive Learning System"
    )
    parser.add_argument(
        "--module",
        default="bar_tutor_unified",
        help="Python module containing knowledge base (default: bar_tutor_unified)"
    )
    parser.add_argument(
        "--db",
        default="bar_prep_adaptive.db",
        help="Output database path (default: bar_prep_adaptive.db)"
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run with example data instead of importing actual module"
    )

    args = parser.parse_args()

    if args.example:
        import_from_knowledge_base(args.db)
    else:
        import_from_actual_knowledge_base(args.module, args.db)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Import Knowledge Base to Adaptive Learning System

Reads KnowledgeNode concepts from bar_tutor_unified.py and converts them
into adaptive learning cards with SM-2 spaced repetition.

Generates multiple cards per concept:
- Rule statement card
- Elements card
- Exceptions card
- Common traps card
- Policy rationales card

Usage:
    python3 import_knowledge_to_adaptive.py --module bar_tutor_unified --db iowa_bar_prep.db
"""

import argparse
import hashlib
import importlib
import re
import sys
from datetime import datetime
from typing import List, Optional

from adaptive_learning_system import (
    AdaptiveLearningSystem,
    LearningCard,
    Subject,
    ConstitutionalLawTopic,
    EvidenceTopic
)


# ==================== TOPIC MAPPING ====================

def map_constitutional_law_topic(concept_name: str, concept_id: str) -> str:
    """Map concept to ConstitutionalLawTopic enum using keyword matching"""

    keywords_map = {
        ConstitutionalLawTopic.JUDICIAL_REVIEW: ['judicial review', 'marbury'],
        ConstitutionalLawTopic.JUSTICIABILITY: ['justiciability', 'case or controversy'],
        ConstitutionalLawTopic.STANDING: ['standing'],
        ConstitutionalLawTopic.RIPENESS: ['ripeness', 'ripe'],
        ConstitutionalLawTopic.MOOTNESS: ['mootness', 'moot'],
        ConstitutionalLawTopic.POLITICAL_QUESTION: ['political question'],
        ConstitutionalLawTopic.FEDERALISM: ['federalism', 'federal'],
        ConstitutionalLawTopic.COMMERCE_CLAUSE: ['commerce clause', 'interstate commerce'],
        ConstitutionalLawTopic.TAXING_SPENDING_POWER: ['taxing', 'spending', 'tax power'],
        ConstitutionalLawTopic.NECESSARY_AND_PROPER: ['necessary and proper', 'mcculloch'],
        ConstitutionalLawTopic.TENTH_AMENDMENT: ['tenth amendment', '10th amendment'],
        ConstitutionalLawTopic.ELEVENTH_AMENDMENT: ['eleventh amendment', '11th amendment', 'sovereign immunity'],
        ConstitutionalLawTopic.SUPREMACY_CLAUSE: ['supremacy', 'preemption'],
        ConstitutionalLawTopic.DORMANT_COMMERCE_CLAUSE: ['dormant commerce'],
        ConstitutionalLawTopic.PRIVILEGES_AND_IMMUNITIES: ['privileges and immunities', 'p&i'],
        ConstitutionalLawTopic.EXECUTIVE_POWER: ['executive power', 'president'],
        ConstitutionalLawTopic.LEGISLATIVE_POWER: ['legislative power', 'congress'],
        ConstitutionalLawTopic.SEPARATION_OF_POWERS: ['separation of powers'],
        ConstitutionalLawTopic.FREEDOM_OF_SPEECH: ['speech', 'first amendment speech', 'expression'],
        ConstitutionalLawTopic.FREEDOM_OF_RELIGION: ['religion', 'religious'],
        ConstitutionalLawTopic.ESTABLISHMENT_CLAUSE: ['establishment'],
        ConstitutionalLawTopic.FREE_EXERCISE_CLAUSE: ['free exercise'],
        ConstitutionalLawTopic.FREEDOM_OF_PRESS: ['press', 'media'],
        ConstitutionalLawTopic.FREEDOM_OF_ASSEMBLY: ['assembly', 'assemble'],
        ConstitutionalLawTopic.FREEDOM_OF_ASSOCIATION: ['association', 'associate'],
        ConstitutionalLawTopic.DUE_PROCESS_SUBSTANTIVE: ['substantive due process'],
        ConstitutionalLawTopic.DUE_PROCESS_PROCEDURAL: ['procedural due process', 'notice', 'hearing'],
        ConstitutionalLawTopic.EQUAL_PROTECTION: ['equal protection'],
        ConstitutionalLawTopic.STRICT_SCRUTINY: ['strict scrutiny', 'compelling interest'],
        ConstitutionalLawTopic.INTERMEDIATE_SCRUTINY: ['intermediate scrutiny', 'heightened scrutiny'],
        ConstitutionalLawTopic.RATIONAL_BASIS: ['rational basis'],
        ConstitutionalLawTopic.FUNDAMENTAL_RIGHTS: ['fundamental right'],
        ConstitutionalLawTopic.TAKINGS_CLAUSE: ['takings', 'eminent domain'],
        ConstitutionalLawTopic.STATE_ACTION: ['state action'],
    }

    # Normalize text for matching
    text_lower = (concept_name + " " + concept_id).lower()

    # Find best match
    for topic, keywords in keywords_map.items():
        for keyword in keywords:
            if keyword in text_lower:
                return topic.value

    return ConstitutionalLawTopic.GENERAL.value


def map_evidence_topic(concept_name: str, concept_id: str) -> str:
    """Map concept to EvidenceTopic enum using keyword matching"""

    keywords_map = {
        EvidenceTopic.RELEVANCE: ['relevance', 'relevant'],
        EvidenceTopic.LOGICAL_RELEVANCE: ['logical relevance'],
        EvidenceTopic.LEGAL_RELEVANCE: ['legal relevance', '403'],
        EvidenceTopic.UNFAIR_PREJUDICE: ['unfair prejudice', 'prejudicial'],
        EvidenceTopic.CHARACTER_EVIDENCE: ['character evidence', 'character'],
        EvidenceTopic.PROPENSITY_EVIDENCE: ['propensity'],
        EvidenceTopic.HABIT_EVIDENCE: ['habit'],
        EvidenceTopic.PRIOR_BAD_ACTS: ['prior bad acts', '404(b)', 'other crimes'],
        EvidenceTopic.SUBSEQUENT_REMEDIAL_MEASURES: ['subsequent remedial', 'repairs'],
        EvidenceTopic.COMPROMISE_OFFERS: ['compromise', 'settlement'],
        EvidenceTopic.PLEA_BARGAINS: ['plea'],
        EvidenceTopic.LIABILITY_INSURANCE: ['insurance'],
        EvidenceTopic.SEXUAL_ASSAULT_CASES: ['sexual assault', 'rape'],
        EvidenceTopic.RAPE_SHIELD: ['rape shield'],
        EvidenceTopic.WITNESS_COMPETENCY: ['competency', 'competent witness'],
        EvidenceTopic.PERSONAL_KNOWLEDGE: ['personal knowledge'],
        EvidenceTopic.OATH_AFFIRMATION: ['oath', 'affirmation'],
        EvidenceTopic.LEADING_QUESTIONS: ['leading question'],
        EvidenceTopic.REFRESHING_RECOLLECTION: ['refresh', 'present recollection refreshed'],
        EvidenceTopic.RECORDED_RECOLLECTION: ['recorded recollection'],
        EvidenceTopic.OPINION_TESTIMONY: ['opinion'],
        EvidenceTopic.EXPERT_WITNESSES: ['expert'],
        EvidenceTopic.LAY_WITNESSES: ['lay witness'],
        EvidenceTopic.DAUBERT_STANDARD: ['daubert'],
        EvidenceTopic.IMPEACHMENT: ['impeachment', 'impeach'],
        EvidenceTopic.PRIOR_INCONSISTENT_STATEMENTS: ['prior inconsistent', 'inconsistent statement'],
        EvidenceTopic.BIAS: ['bias'],
        EvidenceTopic.CONTRADICTION: ['contradiction'],
        EvidenceTopic.HEARSAY: ['hearsay'],
        EvidenceTopic.HEARSAY_EXCEPTIONS: ['hearsay exception'],
        EvidenceTopic.PRESENT_SENSE_IMPRESSION: ['present sense impression'],
        EvidenceTopic.EXCITED_UTTERANCE: ['excited utterance'],
        EvidenceTopic.STATE_OF_MIND: ['state of mind', 'then-existing'],
        EvidenceTopic.MEDICAL_DIAGNOSIS: ['medical', 'diagnosis'],
        EvidenceTopic.PAST_RECOLLECTION_RECORDED: ['past recollection recorded'],
        EvidenceTopic.BUSINESS_RECORDS: ['business record'],
        EvidenceTopic.PUBLIC_RECORDS: ['public record'],
        EvidenceTopic.LEARNED_TREATISES: ['learned treatise'],
        EvidenceTopic.DYING_DECLARATION: ['dying declaration'],
        EvidenceTopic.STATEMENT_AGAINST_INTEREST: ['statement against interest'],
        EvidenceTopic.FORFEITURE_BY_WRONGDOING: ['forfeiture by wrongdoing'],
        EvidenceTopic.CONFRONTATION_CLAUSE: ['confrontation'],
        EvidenceTopic.AUTHENTICATION: ['authentication', 'authenticate'],
        EvidenceTopic.BEST_EVIDENCE_RULE: ['best evidence', 'original writing'],
        EvidenceTopic.ORIGINAL_WRITING_RULE: ['original writing'],
        EvidenceTopic.PRIVILEGES: ['privilege'],
        EvidenceTopic.ATTORNEY_CLIENT: ['attorney-client', 'attorney client'],
        EvidenceTopic.WORK_PRODUCT: ['work product'],
        EvidenceTopic.SPOUSAL_PRIVILEGE: ['spousal', 'marital'],
        EvidenceTopic.PSYCHOTHERAPIST_PATIENT: ['psychotherapist'],
        EvidenceTopic.PHYSICIAN_PATIENT: ['physician-patient'],
        EvidenceTopic.JUDICIAL_NOTICE: ['judicial notice'],
        EvidenceTopic.PRESUMPTIONS: ['presumption'],
    }

    # Normalize text for matching
    text_lower = (concept_name + " " + concept_id).lower()

    # Find best match
    for topic, keywords in keywords_map.items():
        for keyword in keywords:
            if keyword in text_lower:
                return topic.value

    return EvidenceTopic.GENERAL.value


def get_topic_for_concept(subject: str, concept_name: str, concept_id: str) -> str:
    """Get topic based on subject and concept details"""

    if subject == Subject.CONSTITUTIONAL_LAW.value:
        return map_constitutional_law_topic(concept_name, concept_id)
    elif subject == Subject.EVIDENCE.value:
        return map_evidence_topic(concept_name, concept_id)
    else:
        # For other subjects, use a simplified topic based on concept name
        # Remove subject prefix and clean up
        topic = concept_id.replace(subject + "_", "")
        return topic


# ==================== CARD GENERATION ====================

def generate_card_id(subject: str, concept_id: str, card_type: str) -> str:
    """Generate unique card ID"""
    content = f"{subject}_{concept_id}_{card_type}"
    return hashlib.md5(content.encode()).hexdigest()[:16]


def generate_cards_from_concept(concept) -> List[LearningCard]:
    """Generate multiple learning cards from a single KnowledgeNode concept"""

    cards = []
    subject = concept.subject
    topic = get_topic_for_concept(subject, concept.name, concept.concept_id)

    # Card 1: Rule Statement
    if concept.rule_statement and concept.rule_statement.strip():
        card = LearningCard(
            card_id=generate_card_id(subject, concept.concept_id, "rule"),
            subject=subject,
            topic=topic,
            question=f"What is the rule for {concept.name}?",
            answer=concept.rule_statement,
            difficulty=concept.difficulty
        )
        cards.append(card)

    # Card 2: Elements
    if concept.elements and len(concept.elements) > 0:
        elements_text = "\n".join([f"{i+1}. {elem}" for i, elem in enumerate(concept.elements)])
        card = LearningCard(
            card_id=generate_card_id(subject, concept.concept_id, "elements"),
            subject=subject,
            topic=topic,
            question=f"What are the elements/requirements for {concept.name}?",
            answer=elements_text,
            difficulty=concept.difficulty
        )
        cards.append(card)

    # Card 3: Exceptions
    if concept.exceptions and len(concept.exceptions) > 0:
        exceptions_text = "\n".join([f"• {exc}" for exc in concept.exceptions])
        card = LearningCard(
            card_id=generate_card_id(subject, concept.concept_id, "exceptions"),
            subject=subject,
            topic=topic,
            question=f"What are the exceptions to {concept.name}?",
            answer=exceptions_text,
            difficulty=min(concept.difficulty + 1, 5)  # Slightly harder
        )
        cards.append(card)

    # Card 4: Common Traps
    if concept.common_traps and len(concept.common_traps) > 0:
        traps_text = "\n".join([f"⚠️ {trap}" for trap in concept.common_traps])
        card = LearningCard(
            card_id=generate_card_id(subject, concept.concept_id, "traps"),
            subject=subject,
            topic=topic,
            question=f"What are common traps/mistakes with {concept.name}?",
            answer=traps_text,
            difficulty=min(concept.difficulty + 1, 5)
        )
        cards.append(card)

    # Card 5: Policy Rationales
    if concept.policy_rationales and len(concept.policy_rationales) > 0:
        policy_text = "\n".join([f"📋 {policy}" for policy in concept.policy_rationales])
        card = LearningCard(
            card_id=generate_card_id(subject, concept.concept_id, "policy"),
            subject=subject,
            topic=topic,
            question=f"What are the policy rationales behind {concept.name}?",
            answer=policy_text,
            difficulty=max(concept.difficulty - 1, 1)  # Slightly easier
        )
        cards.append(card)

    return cards


# ==================== IMPORT LOGIC ====================

def import_knowledge_base(module_name: str, db_path: str):
    """Import knowledge base from specified module into adaptive learning database"""

    print(f"Importing knowledge base from {module_name}...")
    print(f"Target database: {db_path}")
    print("=" * 60)

    # Import the module
    try:
        module = importlib.import_module(module_name)
        print(f"✓ Successfully imported module: {module_name}")
    except ImportError as e:
        print(f"✗ Error importing module {module_name}: {e}")
        sys.exit(1)

    # Get the LegalKnowledgeGraph
    try:
        knowledge_graph = module.LegalKnowledgeGraph()
        print(f"✓ Successfully initialized LegalKnowledgeGraph")
        print(f"  Total concepts in graph: {len(knowledge_graph.nodes)}")
    except Exception as e:
        print(f"✗ Error initializing LegalKnowledgeGraph: {e}")
        sys.exit(1)

    # Initialize adaptive learning system
    system = AdaptiveLearningSystem(db_path)
    print(f"✓ Successfully initialized AdaptiveLearningSystem")

    # Import concepts
    print("\nImporting concepts...")
    print("-" * 60)

    total_concepts = 0
    total_cards = 0
    cards_by_subject = {}
    skipped_cards = 0

    for concept_id, concept in knowledge_graph.nodes.items():
        total_concepts += 1

        # Generate cards from concept
        cards = generate_cards_from_concept(concept)

        # Add cards to database
        for card in cards:
            success = system.db.add_card(card)
            if success:
                total_cards += 1
                cards_by_subject[card.subject] = cards_by_subject.get(card.subject, 0) + 1
            else:
                skipped_cards += 1

        # Progress indicator
        if total_concepts % 50 == 0:
            print(f"  Processed {total_concepts} concepts, generated {total_cards} cards...")

    # Final statistics
    print("\n" + "=" * 60)
    print("IMPORT COMPLETE")
    print("=" * 60)
    print(f"Total concepts processed: {total_concepts}")
    print(f"Total cards generated: {total_cards}")
    print(f"Skipped cards (duplicates): {skipped_cards}")
    print(f"\nCards by subject:")
    for subject, count in sorted(cards_by_subject.items()):
        print(f"  {subject:30s}: {count:4d} cards")

    # Get system statistics
    print("\n" + "-" * 60)
    print("DATABASE STATISTICS")
    print("-" * 60)
    stats = system.get_statistics()
    print(f"Total cards in database: {stats['total_cards']}")
    print(f"Cards due for review: {stats['due_cards']}")
    print(f"Mastered cards: {stats['mastered_cards']}")

    # Close system
    system.close()
    print("\n✓ Import completed successfully!")


# ==================== MAIN ====================

def main():
    parser = argparse.ArgumentParser(
        description="Import knowledge base to adaptive learning system"
    )
    parser.add_argument(
        '--module',
        type=str,
        required=True,
        help='Module name containing LegalKnowledgeGraph (e.g., bar_tutor_unified)'
    )
    parser.add_argument(
        '--db',
        type=str,
        required=True,
        help='Database file path (e.g., iowa_bar_prep.db)'
    )

    args = parser.parse_args()

    import_knowledge_base(args.module, args.db)


if __name__ == "__main__":
    main()

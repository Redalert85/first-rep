#!/usr/bin/env python3
"""
Import Knowledge Base to Adaptive Learning System
Generates 5 cards per concept: rule, elements, exceptions, traps, policy
"""

import argparse
import hashlib
import importlib
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from adaptive_learning_system import (
    AdaptiveLearningDatabase,
    LearningCard,
    Subject,
    ConstitutionalLawTopic,
    EvidenceTopic
)


# ==================== TOPIC MAPPING ====================

CONSTITUTIONAL_LAW_KEYWORDS = {
    # Federal Powers
    ConstitutionalLawTopic.COMMERCE_CLAUSE: ['commerce', 'interstate', 'channels', 'instrumentalities'],
    ConstitutionalLawTopic.TAXING_SPENDING_POWER: ['tax', 'spending', 'fiscal'],
    ConstitutionalLawTopic.NECESSARY_PROPER_CLAUSE: ['necessary', 'proper', 'mcculloch'],
    ConstitutionalLawTopic.TREATY_POWER: ['treaty', 'international'],
    ConstitutionalLawTopic.WAR_POWERS: ['war', 'military', 'armed forces'],

    # Federalism
    ConstitutionalLawTopic.SUPREMACY_CLAUSE: ['supremacy', 'preempt'],
    ConstitutionalLawTopic.DORMANT_COMMERCE: ['dormant', 'discriminat'],
    ConstitutionalLawTopic.STATE_TAXATION: ['state tax'],
    ConstitutionalLawTopic.PREEMPTION: ['preempt', 'federal law', 'state law'],
    ConstitutionalLawTopic.TENTH_AMENDMENT: ['tenth', 'reserved', 'anti-commandeering'],

    # Separation of Powers
    ConstitutionalLawTopic.EXECUTIVE_POWER: ['executive', 'president', 'veto', 'pardon'],
    ConstitutionalLawTopic.LEGISLATIVE_POWER: ['legislative', 'congress', 'enumerated'],
    ConstitutionalLawTopic.JUDICIAL_POWER: ['judicial', 'justiciability', 'case or controversy'],

    # Individual Rights - Speech
    ConstitutionalLawTopic.FREE_SPEECH_GENERAL: ['free speech', 'first amendment speech'],
    ConstitutionalLawTopic.CONTENT_BASED_RESTRICTIONS: ['content-based', 'viewpoint'],
    ConstitutionalLawTopic.CONTENT_NEUTRAL_RESTRICTIONS: ['content-neutral', 'time place manner', 'tpm'],
    ConstitutionalLawTopic.PUBLIC_FORUM: ['public forum', 'traditional forum'],
    ConstitutionalLawTopic.SYMBOLIC_SPEECH: ['symbolic speech', 'expressive conduct'],
    ConstitutionalLawTopic.COMMERCIAL_SPEECH: ['commercial speech', 'advertising'],
    ConstitutionalLawTopic.OBSCENITY: ['obscenity', 'miller test'],

    # Individual Rights - Religion
    ConstitutionalLawTopic.ESTABLISHMENT_CLAUSE: ['establishment', 'religion establishment'],
    ConstitutionalLawTopic.FREE_EXERCISE: ['free exercise', 'religious freedom'],

    # Individual Rights - Other
    ConstitutionalLawTopic.DUE_PROCESS_PROCEDURAL: ['procedural due process', 'notice', 'hearing'],
    ConstitutionalLawTopic.DUE_PROCESS_SUBSTANTIVE: ['substantive due process', 'fundamental right'],
    ConstitutionalLawTopic.EQUAL_PROTECTION: ['equal protection', 'classification', 'scrutiny'],
    ConstitutionalLawTopic.TAKINGS: ['taking', 'eminent domain', 'just compensation'],
    ConstitutionalLawTopic.PRIVILEGES_IMMUNITIES: ['privileges', 'immunities'],

    # Misc
    ConstitutionalLawTopic.STATE_ACTION: ['state action', 'private action'],
    ConstitutionalLawTopic.STANDING: ['standing', 'injury', 'causation', 'redressability'],
    ConstitutionalLawTopic.MOOTNESS: ['mootness', 'moot'],
    ConstitutionalLawTopic.RIPENESS: ['ripeness', 'ripe'],
    ConstitutionalLawTopic.POLITICAL_QUESTION: ['political question'],
    ConstitutionalLawTopic.ELEVENTH_AMENDMENT: ['eleventh', 'sovereign immunity'],
    ConstitutionalLawTopic.CONGRESSIONAL_ENFORCEMENT: ['section 5', 'enforcement power'],
}

EVIDENCE_KEYWORDS = {
    # Relevance
    EvidenceTopic.RELEVANCE_GENERAL: ['relevance', 'relevant'],
    EvidenceTopic.LOGICAL_RELEVANCE: ['logical relevance', 'probative'],
    EvidenceTopic.LEGAL_RELEVANCE_403: ['403', 'unfair prejudice', 'confusion'],
    EvidenceTopic.CHARACTER_EVIDENCE: ['character evidence', 'propensity'],
    EvidenceTopic.HABIT_ROUTINE: ['habit', 'routine'],

    # Character Evidence
    EvidenceTopic.CHARACTER_CRIMINAL: ['character criminal', 'mercy rule'],
    EvidenceTopic.CHARACTER_CIVIL: ['character civil'],
    EvidenceTopic.CHARACTER_METHODS: ['reputation', 'opinion', 'specific instance'],
    EvidenceTopic.PRIOR_CRIMES_404B: ['404b', 'prior crime', 'other act', 'mimic'],
    EvidenceTopic.IMPEACHMENT_CHARACTER: ['impeachment character', 'truthfulness'],
    EvidenceTopic.REPUTATION_OPINION: ['reputation', 'opinion testimony'],

    # Hearsay
    EvidenceTopic.HEARSAY_DEFINITION: ['hearsay definition', 'out-of-court statement'],
    EvidenceTopic.HEARSAY_GENERAL: ['hearsay'],
    EvidenceTopic.PRESENT_SENSE_IMPRESSION: ['present sense', 'contemporaneous'],
    EvidenceTopic.EXCITED_UTTERANCE: ['excited utterance', 'startling event'],
    EvidenceTopic.STATE_OF_MIND: ['state of mind', 'then-existing', 'mental condition'],
    EvidenceTopic.MEDICAL_DIAGNOSIS: ['medical diagnosis', 'medical treatment'],
    EvidenceTopic.RECORDED_RECOLLECTION: ['recorded recollection', 'past recollection'],
    EvidenceTopic.BUSINESS_RECORDS: ['business record', 'regularly conducted activity'],
    EvidenceTopic.PUBLIC_RECORDS: ['public record', 'government record'],
    EvidenceTopic.ANCIENT_DOCUMENTS: ['ancient document'],
    EvidenceTopic.DYING_DECLARATION: ['dying declaration', 'belief of death'],
    EvidenceTopic.STATEMENT_AGAINST_INTEREST: ['against interest', 'pecuniary'],
    EvidenceTopic.FORFEITURE: ['forfeiture', 'wrongdoing'],
    EvidenceTopic.PRIOR_STATEMENT_WITNESS: ['prior statement', 'prior inconsistent'],
    EvidenceTopic.ADMISSION_PARTY_OPPONENT: ['admission', 'party opponent', 'opposing party'],

    # Privileges
    EvidenceTopic.ATTORNEY_CLIENT: ['attorney-client', 'lawyer-client', 'legal advice'],
    EvidenceTopic.SPOUSAL_PRIVILEGE: ['spousal', 'marital', 'husband', 'wife'],
    EvidenceTopic.PSYCHOTHERAPIST: ['psychotherapist', 'mental health'],
    EvidenceTopic.CLERGY: ['clergy', 'priest'],
    EvidenceTopic.FIFTH_AMENDMENT: ['fifth amendment', 'self-incrimination'],

    # Witnesses
    EvidenceTopic.COMPETENCE: ['competence', 'competency'],
    EvidenceTopic.PERSONAL_KNOWLEDGE: ['personal knowledge', 'firsthand'],
    EvidenceTopic.OATH_AFFIRMATION: ['oath', 'affirmation'],
    EvidenceTopic.IMPEACHMENT_GENERAL: ['impeachment'],
    EvidenceTopic.IMPEACHMENT_BIAS: ['impeachment bias', 'bias', 'interest'],
    EvidenceTopic.IMPEACHMENT_PRIOR_INCONSISTENT: ['prior inconsistent', 'prior statement'],
    EvidenceTopic.IMPEACHMENT_CONVICTION: ['impeachment conviction', 'criminal conviction'],
    EvidenceTopic.REHABILITATION: ['rehabilitation', 'rehabilitate'],

    # Expert Testimony
    EvidenceTopic.EXPERT_QUALIFICATION: ['expert qualification', 'expert witness'],
    EvidenceTopic.EXPERT_BASIS: ['expert basis', 'expert opinion'],
    EvidenceTopic.DAUBERT_STANDARD: ['daubert', 'scientific', 'reliable'],
    EvidenceTopic.EXPERT_OPINION: ['expert opinion'],

    # Authentication
    EvidenceTopic.AUTHENTICATION_GENERAL: ['authentication', 'authenticate'],
    EvidenceTopic.SELF_AUTHENTICATING: ['self-authenticating'],
    EvidenceTopic.VOICE_IDENTIFICATION: ['voice', 'identification'],
    EvidenceTopic.ANCIENT_DOCUMENTS_AUTH: ['ancient document'],

    # Best Evidence
    EvidenceTopic.ORIGINAL_DOCUMENT: ['original document', 'original writing', 'best evidence'],
    EvidenceTopic.DUPLICATES: ['duplicate', 'copy'],
    EvidenceTopic.EXCUSES_NONPRODUCTION: ['excuse', 'nonproduction'],

    # Judicial Notice
    EvidenceTopic.JUDICIAL_NOTICE_GENERAL: ['judicial notice'],
    EvidenceTopic.JUDICIAL_NOTICE_TYPES: ['adjudicative fact', 'legislative fact'],

    # Miscellaneous
    EvidenceTopic.PRESUMPTIONS: ['presumption'],
    EvidenceTopic.BURDENS: ['burden of proof', 'burden of production'],
}


# ==================== TOPIC MATCHING ====================

def match_constitutional_law_topic(concept_name: str, rule_statement: str, traps: List[str]) -> Optional[str]:
    """Match concept to Constitutional Law topic using keywords"""
    combined_text = f"{concept_name} {rule_statement} {' '.join(traps)}".lower()

    # Try to find best match
    best_match = None
    best_score = 0

    for topic, keywords in CONSTITUTIONAL_LAW_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in combined_text)
        if score > best_score:
            best_score = score
            best_match = topic.value

    return best_match if best_score > 0 else ConstitutionalLawTopic.GENERAL.value


def match_evidence_topic(concept_name: str, rule_statement: str, traps: List[str]) -> Optional[str]:
    """Match concept to Evidence topic using keywords"""
    combined_text = f"{concept_name} {rule_statement} {' '.join(traps)}".lower()

    # Try to find best match
    best_match = None
    best_score = 0

    for topic, keywords in EVIDENCE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in combined_text)
        if score > best_score:
            best_score = score
            best_match = topic.value

    return best_match if best_score > 0 else EvidenceTopic.GENERAL.value


# ==================== CARD GENERATION ====================

def generate_card_id(concept_id: str, card_type: str) -> str:
    """Generate unique card ID"""
    combined = f"{concept_id}_{card_type}"
    return hashlib.md5(combined.encode()).hexdigest()[:16]


def generate_cards_for_concept(concept, db: AdaptiveLearningDatabase) -> int:
    """Generate 5 cards for a concept: rule, elements, exceptions, traps, policy"""
    cards_created = 0

    # Determine topic for Constitutional Law and Evidence
    topic = None
    if concept.subject == "constitutional_law":
        topic = match_constitutional_law_topic(
            concept.name,
            concept.rule_statement,
            concept.common_traps
        )
    elif concept.subject == "evidence":
        topic = match_evidence_topic(
            concept.name,
            concept.rule_statement,
            concept.common_traps
        )

    # Card 1: Rule Statement
    if concept.rule_statement:
        card = LearningCard(
            card_id=generate_card_id(concept.concept_id, "rule"),
            concept_id=concept.concept_id,
            subject=concept.subject,
            topic=topic,
            card_type="rule",
            front=f"[RULE] {concept.name}",
            back=concept.rule_statement,
            difficulty=concept.difficulty
        )
        db.insert_card(card)
        cards_created += 1

    # Card 2: Elements
    if concept.elements:
        elements_text = "\n".join(f"• {elem}" for elem in concept.elements)
        card = LearningCard(
            card_id=generate_card_id(concept.concept_id, "elements"),
            concept_id=concept.concept_id,
            subject=concept.subject,
            topic=topic,
            card_type="elements",
            front=f"[ELEMENTS] What are the key elements of {concept.name}?",
            back=elements_text,
            difficulty=concept.difficulty
        )
        db.insert_card(card)
        cards_created += 1

    # Card 3: Exceptions
    if concept.exceptions:
        exceptions_text = "\n".join(f"• {exc}" for exc in concept.exceptions)
        card = LearningCard(
            card_id=generate_card_id(concept.concept_id, "exceptions"),
            concept_id=concept.concept_id,
            subject=concept.subject,
            topic=topic,
            card_type="exceptions",
            front=f"[EXCEPTIONS] What are the exceptions to {concept.name}?",
            back=exceptions_text,
            difficulty=concept.difficulty + 1 if concept.difficulty < 5 else 5
        )
        db.insert_card(card)
        cards_created += 1

    # Card 4: Common Traps
    if concept.common_traps:
        traps_text = "\n".join(f"• {trap}" for trap in concept.common_traps)
        card = LearningCard(
            card_id=generate_card_id(concept.concept_id, "traps"),
            concept_id=concept.concept_id,
            subject=concept.subject,
            topic=topic,
            card_type="traps",
            front=f"[TRAPS] What are common traps for {concept.name}?",
            back=traps_text,
            difficulty=concept.difficulty + 1 if concept.difficulty < 5 else 5
        )
        db.insert_card(card)
        cards_created += 1

    # Card 5: Policy Rationales
    if concept.policy_rationales:
        policy_text = "\n".join(f"• {policy}" for policy in concept.policy_rationales)
        card = LearningCard(
            card_id=generate_card_id(concept.concept_id, "policy"),
            concept_id=concept.concept_id,
            subject=concept.subject,
            topic=topic,
            card_type="policy",
            front=f"[POLICY] What are the policy rationales for {concept.name}?",
            back=policy_text,
            difficulty=concept.difficulty
        )
        db.insert_card(card)
        cards_created += 1

    return cards_created


# ==================== IMPORT ====================

def import_knowledge_base(module_name: str, db_path: str):
    """Import knowledge base from module and generate cards"""
    print(f"Importing knowledge base from {module_name}...")

    # Import the module
    try:
        module = importlib.import_module(module_name)
        LegalKnowledgeGraph = module.LegalKnowledgeGraph
    except Exception as e:
        print(f"Error importing module: {e}")
        return

    # Initialize knowledge graph
    print("Initializing knowledge graph...")
    kg = LegalKnowledgeGraph()

    print(f"Found {len(kg.nodes)} concepts")

    # Initialize database
    db = AdaptiveLearningDatabase(db_path)

    # Statistics
    stats = {
        'total_concepts': len(kg.nodes),
        'total_cards': 0,
        'by_subject': {},
        'by_card_type': {
            'rule': 0,
            'elements': 0,
            'exceptions': 0,
            'traps': 0,
            'policy': 0
        }
    }

    # Generate cards for each concept
    print("\nGenerating cards...")
    for concept in kg.nodes.values():
        cards_created = generate_cards_for_concept(concept, db)
        stats['total_cards'] += cards_created

        # Track by subject
        if concept.subject not in stats['by_subject']:
            stats['by_subject'][concept.subject] = {
                'concepts': 0,
                'cards': 0
            }
        stats['by_subject'][concept.subject]['concepts'] += 1
        stats['by_subject'][concept.subject]['cards'] += cards_created

    # Print detailed statistics
    print("\n" + "=" * 70)
    print("IMPORT COMPLETE")
    print("=" * 70)
    print(f"\nTotal Concepts: {stats['total_concepts']}")
    print(f"Total Cards Generated: {stats['total_cards']}")
    print(f"Average Cards per Concept: {stats['total_cards'] / stats['total_concepts']:.1f}")

    print("\n" + "-" * 70)
    print("CARDS BY SUBJECT")
    print("-" * 70)
    print(f"{'Subject':<30s} {'Concepts':>10s} {'Cards':>10s} {'Avg':>10s}")
    print("-" * 70)

    for subject in sorted(stats['by_subject'].keys()):
        data = stats['by_subject'][subject]
        avg = data['cards'] / data['concepts'] if data['concepts'] > 0 else 0
        print(f"{subject:<30s} {data['concepts']:>10d} {data['cards']:>10d} {avg:>10.1f}")

    print("-" * 70)

    # Constitutional Law and Evidence topic breakdown
    if 'constitutional_law' in stats['by_subject']:
        print("\n" + "-" * 70)
        print("CONSTITUTIONAL LAW - Top Topics")
        print("-" * 70)
        con_law_cards = db.get_cards_by_subject('constitutional_law')
        topic_counts = {}
        for card in con_law_cards:
            if card.topic:
                topic_counts[card.topic] = topic_counts.get(card.topic, 0) + 1

        for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {topic:<40s}: {count:>4d} cards")

    if 'evidence' in stats['by_subject']:
        print("\n" + "-" * 70)
        print("EVIDENCE - Top Topics")
        print("-" * 70)
        evidence_cards = db.get_cards_by_subject('evidence')
        topic_counts = {}
        for card in evidence_cards:
            if card.topic:
                topic_counts[card.topic] = topic_counts.get(card.topic, 0) + 1

        for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {topic:<40s}: {count:>4d} cards")

    db.close()

    print("\n" + "=" * 70)
    print(f"Database saved to: {db_path}")
    print("=" * 70)


# ==================== MAIN ====================

def main():
    parser = argparse.ArgumentParser(description='Import knowledge base to adaptive learning system')
    parser.add_argument('--module', type=str, default='bar_tutor_unified',
                        help='Python module to import knowledge base from')
    parser.add_argument('--db', type=str, default='iowa_bar_prep.db',
                        help='Database path')

    args = parser.parse_args()

    import_knowledge_base(args.module, args.db)


if __name__ == "__main__":
    main()

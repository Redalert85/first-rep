#!/usr/bin/env python3
"""
Import Iowa Bar concepts from bar_tutor_unified into adaptive learning database
Creates multiple flashcards per concept for comprehensive learning
"""

from adaptive_learning_system import AdaptiveLearningSystem, Card, Subject
from bar_tutor_unified import LegalKnowledgeGraph
from datetime import datetime


def import_concepts_to_database():
    """Import all concepts from LegalKnowledgeGraph into database"""

    print("=" * 70)
    print("IMPORTING IOWA BAR CONCEPTS TO DATABASE")
    print("=" * 70)
    print()

    # Initialize systems
    print("📊 Loading knowledge graph...")
    kg = LegalKnowledgeGraph()
    print(f"✓ Loaded {len(kg.nodes)} concepts")

    print("\n🗄️  Initializing database...")
    system = AdaptiveLearningSystem('iowa_bar_prep.db')

    # Clear existing data
    print("🧹 Clearing existing cards...")
    system.clear_all_cards()

    # Import concepts
    print("\n📥 Importing concepts...")
    card_count = 0

    for concept_id, concept in kg.nodes.items():
        # 1. Rule Statement Card
        if concept.rule_statement:
            card = Card(
                card_id=None,
                concept_id=f"{concept_id}_rule",
                subject=concept.subject,
                front=f"State the rule for: {concept.name}",
                back=concept.rule_statement
            )
            system.add_card(card)
            card_count += 1

        # 2. Elements Card
        if concept.elements and len(concept.elements) > 0:
            elements_text = "\n".join(f"{i}. {elem}" for i, elem in enumerate(concept.elements, 1))
            card = Card(
                card_id=None,
                concept_id=f"{concept_id}_elements",
                subject=concept.subject,
                front=f"What are the elements of {concept.name}?",
                back=elements_text
            )
            system.add_card(card)
            card_count += 1

        # 3. Common Traps Card
        if concept.common_traps and len(concept.common_traps) > 0:
            traps_text = "\n".join(f"⚠️ {trap}" for trap in concept.common_traps)
            card = Card(
                card_id=None,
                concept_id=f"{concept_id}_traps",
                subject=concept.subject,
                front=f"What are common exam traps for {concept.name}?",
                back=traps_text
            )
            system.add_card(card)
            card_count += 1

        # 4. Exceptions Card
        if hasattr(concept, 'exceptions') and concept.exceptions and len(concept.exceptions) > 0:
            exceptions_text = "\n".join(f"• {exc}" for exc in concept.exceptions)
            card = Card(
                card_id=None,
                concept_id=f"{concept_id}_exceptions",
                subject=concept.subject,
                front=f"What are the exceptions to {concept.name}?",
                back=exceptions_text
            )
            system.add_card(card)
            card_count += 1

        # 5. Policy Rationales Card
        if hasattr(concept, 'policy_rationales') and concept.policy_rationales and len(concept.policy_rationales) > 0:
            policy_text = "\n".join(f"• {policy}" for policy in concept.policy_rationales)
            card = Card(
                card_id=None,
                concept_id=f"{concept_id}_policy",
                subject=concept.subject,
                front=f"What are the policy rationales for {concept.name}?",
                back=policy_text
            )
            system.add_card(card)
            card_count += 1

        # 6. Mnemonic Card (if available)
        if hasattr(concept, 'mnemonic') and concept.mnemonic:
            card = Card(
                card_id=None,
                concept_id=f"{concept_id}_mnemonic",
                subject=concept.subject,
                front=f"What is the mnemonic for {concept.name}?",
                back=concept.mnemonic
            )
            system.add_card(card)
            card_count += 1

    print(f"✓ Imported {card_count} flashcards from {len(kg.nodes)} concepts")

    # Show statistics
    print("\n" + "=" * 70)
    print("IMPORT COMPLETE")
    print("=" * 70)

    stats = system.get_statistics()
    print(f"\n📊 Database Statistics:")
    print(f"  Total Cards: {stats['total_cards']}")
    print(f"  Total Concepts: {len(kg.nodes)}")
    print(f"  Cards per Concept: {stats['total_cards'] / len(kg.nodes):.1f}")
    print(f"  Due Today: {stats['due_cards']}")

    print(f"\n📚 Cards by Subject:")
    for subject, count in sorted(stats['cards_by_subject'].items()):
        print(f"  {subject:30} {count:4} cards")

    system.close()

    print("\n✅ Database ready at: iowa_bar_prep.db")
    print("\n🚀 Next steps:")
    print("  1. Verify import: python3 -c \"from adaptive_learning_system import ...\"")
    print("  2. Start studying: Create a study script")


if __name__ == "__main__":
    import_concepts_to_database()

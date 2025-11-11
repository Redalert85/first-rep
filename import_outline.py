#!/usr/bin/env python3
"""
Outline Importer for Iowa Bar Prep
Import bar prep outlines and automatically generate flashcards
"""

import hashlib
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

from adaptive_learning_system import AdaptiveLearningDatabase, LearningCard


# Iowa Bar subjects
SUBJECTS = [
    "contracts", "torts", "constitutional_law", "criminal_law",
    "criminal_procedure", "civil_procedure", "evidence", "real_property",
    "professional_responsibility", "corporations", "wills_trusts_estates",
    "family_law", "secured_transactions", "iowa_procedure"
]


def parse_markdown_outline(file_path: str) -> List[Dict]:
    """Parse markdown outline into structured cards"""
    cards = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Current context
    current_subject = None
    current_topic = None
    current_section = None
    current_content = []

    lines = content.split('\n')

    for line in lines:
        line = line.rstrip()

        # Subject header (## Subject)
        if line.startswith('## '):
            # Save previous section
            if current_section and current_content:
                cards.append({
                    'subject': current_subject,
                    'topic': current_topic,
                    'section': current_section,
                    'content': '\n'.join(current_content).strip()
                })
                current_content = []

            # Extract subject
            subject_text = line[3:].strip().lower()
            for s in SUBJECTS:
                if s.replace('_', ' ') in subject_text or subject_text in s:
                    current_subject = s
                    break

            current_topic = None
            current_section = None

        # Topic header (### Topic)
        elif line.startswith('### '):
            # Save previous section
            if current_section and current_content:
                cards.append({
                    'subject': current_subject,
                    'topic': current_topic,
                    'section': current_section,
                    'content': '\n'.join(current_content).strip()
                })
                current_content = []

            current_topic = line[4:].strip()
            current_section = None

        # Section header (#### Rule, #### Elements, etc.)
        elif line.startswith('#### '):
            # Save previous section
            if current_section and current_content:
                cards.append({
                    'subject': current_subject,
                    'topic': current_topic,
                    'section': current_section,
                    'content': '\n'.join(current_content).strip()
                })
                current_content = []

            current_section = line[5:].strip()

        # Content
        elif line.strip() and current_section:
            current_content.append(line)

    # Save last section
    if current_section and current_content:
        cards.append({
            'subject': current_subject,
            'topic': current_topic,
            'section': current_section,
            'content': '\n'.join(current_content).strip()
        })

    return cards


def parse_text_outline(file_path: str) -> List[Dict]:
    """Parse plain text outline with structure markers"""
    cards = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for patterns like:
    # SUBJECT: Contracts
    # TOPIC: Offer and Acceptance
    # RULE: Mailbox Rule
    # [content]

    current_subject = None
    current_topic = None
    current_section = None
    current_content = []

    for line in content.split('\n'):
        line = line.strip()

        # Subject line
        if line.upper().startswith('SUBJECT:'):
            if current_section and current_content:
                cards.append({
                    'subject': current_subject,
                    'topic': current_topic,
                    'section': current_section,
                    'content': '\n'.join(current_content).strip()
                })
                current_content = []

            subject_text = line[8:].strip().lower()
            for s in SUBJECTS:
                if s.replace('_', ' ') in subject_text:
                    current_subject = s
                    break
            current_topic = None
            current_section = None

        # Topic line
        elif line.upper().startswith('TOPIC:'):
            if current_section and current_content:
                cards.append({
                    'subject': current_subject,
                    'topic': current_topic,
                    'section': current_section,
                    'content': '\n'.join(current_content).strip()
                })
                current_content = []

            current_topic = line[6:].strip()
            current_section = None

        # Section line (RULE:, ELEMENTS:, etc.)
        elif re.match(r'^(RULE|ELEMENTS|EXCEPTIONS|TRAPS|POLICY):', line, re.IGNORECASE):
            if current_section and current_content:
                cards.append({
                    'subject': current_subject,
                    'topic': current_topic,
                    'section': current_section,
                    'content': '\n'.join(current_content).strip()
                })
                current_content = []

            match = re.match(r'^([A-Z]+):', line, re.IGNORECASE)
            current_section = match.group(1).lower()

        # Content
        elif line and current_section:
            current_content.append(line)

    # Save last section
    if current_section and current_content:
        cards.append({
            'subject': current_subject,
            'topic': current_topic,
            'section': current_section,
            'content': '\n'.join(current_content).strip()
        })

    return cards


def determine_card_type(section: str) -> str:
    """Determine card type from section name"""
    section_lower = section.lower()

    if 'rule' in section_lower or 'definition' in section_lower:
        return 'rule'
    elif 'element' in section_lower or 'factor' in section_lower or 'prong' in section_lower:
        return 'elements'
    elif 'exception' in section_lower or 'defense' in section_lower:
        return 'exceptions'
    elif 'trap' in section_lower or 'pitfall' in section_lower or 'mistake' in section_lower:
        return 'traps'
    elif 'policy' in section_lower or 'rationale' in section_lower:
        return 'policy'
    else:
        return 'rule'  # Default


def estimate_difficulty(content: str) -> int:
    """Estimate difficulty based on content complexity"""
    word_count = len(content.split())

    if word_count < 30:
        return 2  # Basic
    elif word_count < 60:
        return 3  # Intermediate
    elif word_count < 100:
        return 4  # Advanced
    else:
        return 5  # Expert


def create_flashcard(data: Dict) -> LearningCard:
    """Create a LearningCard from parsed data"""
    card_type = determine_card_type(data['section'])

    # Create front (question)
    type_label = card_type.upper()
    if data['topic']:
        front = f"[{type_label}] {data['topic']}\n\n{data['section']}"
    else:
        front = f"[{type_label}] {data['section']}"

    # Back is the content
    back = data['content']

    # Generate card ID
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    raw_id = f"{data['subject']}_{card_type}_{timestamp}_{data['topic']}"
    card_id = hashlib.md5(raw_id.encode()).hexdigest()[:16]

    # Estimate difficulty
    difficulty = estimate_difficulty(back)

    now = datetime.now()

    return LearningCard(
        card_id=card_id,
        concept_id=card_id,
        subject=data['subject'],
        topic=data['topic'],
        card_type=card_type,
        front=front,
        back=back,
        difficulty=difficulty,
        ease_factor=2.5,
        interval=1,
        repetitions=0,
        last_reviewed=None,
        next_review=None,
        times_seen=0,
        times_correct=0,
        times_incorrect=0,
        average_confidence=0.0,
        created_at=now,
        updated_at=now
    )


def preview_cards(cards: List[LearningCard], limit: int = 5):
    """Preview cards before importing"""
    print("\n" + "=" * 80)
    print(f"PREVIEW: Showing {min(limit, len(cards))} of {len(cards)} cards")
    print("=" * 80)

    for i, card in enumerate(cards[:limit], 1):
        print(f"\n--- CARD {i} ---")
        print(f"Subject: {card.subject}")
        print(f"Topic: {card.topic or '(none)'}")
        print(f"Type: {card.card_type}")
        print(f"Difficulty: {'⭐' * card.difficulty}")
        print(f"\nFront (first 100 chars):")
        print(card.front[:100] + "..." if len(card.front) > 100 else card.front)
        print(f"\nBack (first 100 chars):")
        print(card.back[:100] + "..." if len(card.back) > 100 else card.back)

    if len(cards) > limit:
        print(f"\n... and {len(cards) - limit} more cards")

    print("\n" + "=" * 80)


def get_statistics(cards: List[LearningCard]) -> Dict:
    """Get statistics about cards to import"""
    stats = {
        'total': len(cards),
        'by_subject': {},
        'by_type': {},
        'by_difficulty': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    }

    for card in cards:
        # By subject
        if card.subject not in stats['by_subject']:
            stats['by_subject'][card.subject] = 0
        stats['by_subject'][card.subject] += 1

        # By type
        if card.card_type not in stats['by_type']:
            stats['by_type'][card.card_type] = 0
        stats['by_type'][card.card_type] += 1

        # By difficulty
        stats['by_difficulty'][card.difficulty] += 1

    return stats


def display_statistics(stats: Dict):
    """Display import statistics"""
    print("\n" + "=" * 80)
    print("IMPORT STATISTICS")
    print("=" * 80)
    print(f"\nTotal cards to import: {stats['total']}")

    print(f"\nBy Subject:")
    for subject, count in sorted(stats['by_subject'].items()):
        print(f"  {subject.replace('_', ' ').title():<30} {count:>3}")

    print(f"\nBy Type:")
    for card_type, count in sorted(stats['by_type'].items()):
        print(f"  {card_type.capitalize():<30} {count:>3}")

    print(f"\nBy Difficulty:")
    for diff, count in sorted(stats['by_difficulty'].items()):
        if count > 0:
            stars = '⭐' * diff
            print(f"  {stars:<15} {count:>3}")

    print("\n" + "=" * 80)


def main():
    """Main import workflow"""
    print("\n" + "=" * 80)
    print("OUTLINE IMPORTER - Iowa Bar Prep")
    print("=" * 80)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python3 import_outline.py <file_path>")
        print("\nSupported formats:")
        print("  • Markdown (.md)")
        print("  • Plain text (.txt)")
        print("\nMarkdown format example:")
        print("  ## Contracts")
        print("  ### Offer and Acceptance")
        print("  #### Rule: Mailbox Rule")
        print("  Acceptance is effective upon dispatch...")
        print("\nText format example:")
        print("  SUBJECT: Contracts")
        print("  TOPIC: Offer and Acceptance")
        print("  RULE: Mailbox Rule")
        print("  Acceptance is effective upon dispatch...")
        print()
        return

    file_path = sys.argv[1]

    # Check file exists
    if not os.path.exists(file_path):
        print(f"\n❌ Error: File not found: {file_path}\n")
        return

    print(f"\nReading file: {file_path}")

    # Parse based on extension
    ext = Path(file_path).suffix.lower()

    if ext == '.md':
        print("Format: Markdown")
        parsed_data = parse_markdown_outline(file_path)
    elif ext in ['.txt', '.text']:
        print("Format: Plain text")
        parsed_data = parse_text_outline(file_path)
    else:
        print(f"\n❌ Unsupported file format: {ext}")
        print("Supported: .md, .txt\n")
        return

    if not parsed_data:
        print("\n⚠️  No cards found in file. Check the format.\n")
        return

    print(f"✓ Parsed {len(parsed_data)} sections")

    # Create flashcards
    print("\nGenerating flashcards...")
    cards = [create_flashcard(data) for data in parsed_data]
    print(f"✓ Created {len(cards)} flashcards")

    # Show statistics
    stats = get_statistics(cards)
    display_statistics(stats)

    # Preview
    preview_cards(cards, limit=3)

    # Confirm import
    response = input("\nImport these cards to database? (y/n): ").strip().lower()

    if response != 'y':
        print("\n❌ Import cancelled\n")
        return

    # Import to database
    print("\nImporting to database...")
    db = AdaptiveLearningDatabase("iowa_bar_prep.db")

    imported = 0
    for card in cards:
        try:
            db.insert_card(card)
            imported += 1
        except Exception as e:
            print(f"⚠️  Error importing card: {e}")

    db.close()

    print(f"\n✅ Successfully imported {imported}/{len(cards)} cards!")
    print("\nCards are now available for study:")
    print("  python3 daily_study.py")
    print("  python3 subject_study.py")
    print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
PDF Outline Importer for Iowa Bar Prep
Extract and parse bar prep outlines from PDF files
"""

import hashlib
import re
import sys
from datetime import datetime
from typing import List, Dict, Optional

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

from adaptive_learning_system import AdaptiveLearningDatabase, LearningCard


# Iowa Bar subjects
SUBJECTS = [
    "contracts", "torts", "constitutional_law", "criminal_law",
    "criminal_procedure", "civil_procedure", "evidence", "real_property",
    "professional_responsibility", "corporations", "wills_trusts_estates",
    "family_law", "secured_transactions", "iowa_procedure"
]

# Keywords that indicate subject names
SUBJECT_KEYWORDS = {
    'contracts': ['contract', 'ucc', 'sale of goods'],
    'torts': ['tort', 'negligence', 'intentional tort'],
    'constitutional_law': ['constitutional', 'first amendment', 'due process', 'equal protection', 'commerce clause'],
    'criminal_law': ['criminal law', 'homicide', 'murder', 'assault'],
    'criminal_procedure': ['criminal procedure', 'fourth amendment', 'miranda', 'search and seizure'],
    'civil_procedure': ['civil procedure', 'jurisdiction', 'pleading', 'discovery'],
    'evidence': ['evidence', 'hearsay', 'relevance', 'privilege'],
    'real_property': ['real property', 'property', 'estate', 'easement', 'covenant'],
    'professional_responsibility': ['professional responsibility', 'ethics', 'attorney', 'lawyer'],
    'corporations': ['corporation', 'business organization', 'partnership', 'llc'],
    'wills_trusts_estates': ['wills', 'trusts', 'estates', 'probate', 'intestacy'],
    'family_law': ['family law', 'divorce', 'custody', 'marriage'],
    'secured_transactions': ['secured transaction', 'article 9', 'security interest'],
    'iowa_procedure': ['iowa procedure', 'iowa civil', 'iowa code']
}


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from PDF file"""
    if not HAS_PYPDF2:
        print("\n❌ Error: PyPDF2 library not found!")
        print("Install it with: pip install PyPDF2")
        print("Or: pip3 install PyPDF2\n")
        sys.exit(1)

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""

            print(f"Extracting text from {len(pdf_reader.pages)} pages...")

            for i, page in enumerate(pdf_reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    text += page_text + "\n\n"

                    if i % 10 == 0:
                        print(f"  Processed {i}/{len(pdf_reader.pages)} pages...")
                except Exception as e:
                    print(f"  ⚠️  Warning: Could not extract page {i}: {e}")

            return text

    except Exception as e:
        print(f"\n❌ Error reading PDF: {e}\n")
        sys.exit(1)


def detect_subject(text: str, context: Optional[str] = None) -> Optional[str]:
    """Detect subject from text content"""
    text_lower = (text + " " + (context or "")).lower()

    # Count keyword matches for each subject
    matches = {}
    for subject, keywords in SUBJECT_KEYWORDS.items():
        count = sum(1 for keyword in keywords if keyword in text_lower)
        if count > 0:
            matches[subject] = count

    # Return subject with most matches
    if matches:
        return max(matches, key=matches.get)

    return None


def parse_pdf_text(text: str) -> List[Dict]:
    """Parse PDF text into structured sections"""
    cards = []
    lines = text.split('\n')

    current_subject = None
    current_topic = None
    current_section = None
    current_content = []
    context_buffer = []  # Last few lines for context

    # Patterns for section headers
    section_patterns = [
        (r'^(RULE|DEFINITION|LAW)[\s:]+(.+)', 'rule'),
        (r'^(ELEMENTS?|FACTORS?|PRONGS?|REQUIREMENTS?)[\s:]+(.+)', 'elements'),
        (r'^(EXCEPTIONS?|DEFENSES?)[\s:]+(.+)', 'exceptions'),
        (r'^(TRAPS?|PITFALLS?|COMMON\s+MISTAKES?)[\s:]+(.+)', 'traps'),
        (r'^(POLICY|RATIONALE)[\s:]+(.+)', 'policy'),
    ]

    # Roman numeral or numbered section
    topic_pattern = r'^([IVX]+\.|[0-9]+\.)\s+(.+)'

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Keep context buffer (last 5 lines for subject detection)
        context_buffer.append(line)
        if len(context_buffer) > 5:
            context_buffer.pop(0)

        # Check for topic headers (Roman numerals or numbers)
        topic_match = re.match(topic_pattern, line)
        if topic_match and len(line) < 100:  # Topics are usually short
            # Save previous section
            if current_section and current_content:
                cards.append({
                    'subject': current_subject,
                    'topic': current_topic,
                    'section': current_section,
                    'content': '\n'.join(current_content).strip()
                })
                current_content = []

            current_topic = topic_match.group(2).strip()
            current_section = None

            # Try to detect subject from topic
            if not current_subject:
                current_subject = detect_subject(current_topic, ' '.join(context_buffer))

            continue

        # Check for section headers
        matched = False
        for pattern, card_type in section_patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                # Save previous section
                if current_section and current_content:
                    cards.append({
                        'subject': current_subject,
                        'topic': current_topic,
                        'section': current_section,
                        'content': '\n'.join(current_content).strip()
                    })
                    current_content = []

                current_section = match.group(2).strip() if len(match.groups()) > 1 else match.group(1).strip()

                # Try to detect subject if not set
                if not current_subject:
                    current_subject = detect_subject(current_section, ' '.join(context_buffer))

                matched = True
                break

        if matched:
            continue

        # Check if line looks like a major heading (all caps, short)
        if line.isupper() and 10 < len(line) < 80 and not current_section:
            # Could be a subject or topic heading
            detected_subject = detect_subject(line, ' '.join(context_buffer))
            if detected_subject:
                # Save previous section
                if current_section and current_content:
                    cards.append({
                        'subject': current_subject,
                        'topic': current_topic,
                        'section': current_section,
                        'content': '\n'.join(current_content).strip()
                    })
                    current_content = []

                current_subject = detected_subject
                current_topic = line.title()
                current_section = None
            continue

        # Add to content if we have a section
        if current_section:
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


def clean_parsed_data(cards: List[Dict]) -> List[Dict]:
    """Clean and validate parsed data"""
    cleaned = []

    for card in cards:
        # Skip if no subject detected
        if not card['subject']:
            continue

        # Skip if content is too short
        if len(card['content']) < 10:
            continue

        # Skip if content is too long (might be page headers/footers)
        if len(card['content']) > 2000:
            continue

        cleaned.append(card)

    return cleaned


def determine_card_type(section: str) -> str:
    """Determine card type from section name"""
    section_lower = section.lower()

    if any(word in section_lower for word in ['rule', 'definition', 'law']):
        return 'rule'
    elif any(word in section_lower for word in ['element', 'factor', 'prong', 'requirement']):
        return 'elements'
    elif any(word in section_lower for word in ['exception', 'defense']):
        return 'exceptions'
    elif any(word in section_lower for word in ['trap', 'pitfall', 'mistake']):
        return 'traps'
    elif any(word in section_lower for word in ['policy', 'rationale']):
        return 'policy'
    else:
        return 'rule'


def estimate_difficulty(content: str) -> int:
    """Estimate difficulty based on content complexity"""
    word_count = len(content.split())

    if word_count < 30:
        return 2
    elif word_count < 60:
        return 3
    elif word_count < 100:
        return 4
    else:
        return 5


def create_flashcard(data: Dict) -> LearningCard:
    """Create a LearningCard from parsed data"""
    card_type = determine_card_type(data['section'])

    # Create front
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


def get_statistics(cards: List[LearningCard]) -> Dict:
    """Get statistics about cards"""
    stats = {
        'total': len(cards),
        'by_subject': {},
        'by_type': {},
        'by_difficulty': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    }

    for card in cards:
        stats['by_subject'][card.subject] = stats['by_subject'].get(card.subject, 0) + 1
        stats['by_type'][card.card_type] = stats['by_type'].get(card.card_type, 0) + 1
        stats['by_difficulty'][card.difficulty] += 1

    return stats


def display_statistics(stats: Dict):
    """Display statistics"""
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


def preview_cards(cards: List[LearningCard], limit: int = 3):
    """Preview cards"""
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
        print(f"\nBack (first 150 chars):")
        print(card.back[:150] + "..." if len(card.back) > 150 else card.back)

    if len(cards) > limit:
        print(f"\n... and {len(cards) - limit} more cards")

    print("\n" + "=" * 80)


def main():
    """Main PDF import workflow"""
    print("\n" + "=" * 80)
    print("PDF OUTLINE IMPORTER - Iowa Bar Prep")
    print("=" * 80)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python3 import_pdf.py <file.pdf>")
        print("\nFeatures:")
        print("  • Extracts text from PDF")
        print("  • Automatically detects subjects")
        print("  • Parses structured sections (Rule, Elements, etc.)")
        print("  • Generates flashcards")
        print("\nNote: Works best with structured outlines (not case briefs)")
        print("Requires: pip install PyPDF2\n")
        return

    pdf_path = sys.argv[1]

    # Check file exists
    import os
    if not os.path.exists(pdf_path):
        print(f"\n❌ Error: File not found: {pdf_path}\n")
        return

    if not pdf_path.lower().endswith('.pdf'):
        print(f"\n❌ Error: Not a PDF file: {pdf_path}\n")
        return

    print(f"\nProcessing PDF: {pdf_path}")

    # Extract text
    text = extract_text_from_pdf(pdf_path)
    print(f"✓ Extracted {len(text)} characters")

    # Parse text
    print("\nParsing PDF structure...")
    parsed_data = parse_pdf_text(text)
    print(f"✓ Found {len(parsed_data)} potential sections")

    # Clean data
    parsed_data = clean_parsed_data(parsed_data)
    print(f"✓ After filtering: {len(parsed_data)} valid sections")

    if not parsed_data:
        print("\n⚠️  No valid sections found.")
        print("\nTips:")
        print("  • Make sure PDF contains structured outlines")
        print("  • Look for sections labeled RULE:, ELEMENTS:, etc.")
        print("  • Try converting PDF to markdown first")
        print()
        return

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

#!/usr/bin/env python3
"""
Card Enhancement Tool for Iowa Bar Prep
Semi-automated workflow for enhancing placeholder cards with ChatGPT content
Focuses on MBE subjects only
"""

import os
import subprocess
import sys
import tempfile
from datetime import datetime
from adaptive_learning_system import AdaptiveLearningDatabase


# MBE subjects only (8 subjects tested on Multistate Bar Exam)
MBE_SUBJECTS = [
    "constitutional_law",
    "contracts",
    "criminal_law",
    "criminal_procedure",
    "civil_procedure",
    "evidence",
    "real_property",
    "torts",
]


def clear_screen():
    """Clear the terminal screen"""
    print("\033[2J\033[H", end="")


def get_mbe_subject_stats(db_path: str = "iowa_bar_prep.db"):
    """Get statistics for MBE subjects showing placeholder vs complete cards"""
    conn = db_path if hasattr(db_path, 'execute') else __import__('sqlite3').connect(db_path)

    stats = []
    for subject in MBE_SUBJECTS:
        result = conn.execute("""
            SELECT
                ? as subject,
                COUNT(*) as total,
                SUM(CASE WHEN back LIKE '%Mnemonic%'
                         OR back LIKE '%• Traps%'
                         OR back LIKE '%• Micro-Hypos%'
                    THEN 1 ELSE 0 END) as placeholders,
                COUNT(*) - SUM(CASE WHEN back LIKE '%Mnemonic%'
                                    OR back LIKE '%• Traps%'
                                    OR back LIKE '%• Micro-Hypos%'
                               THEN 1 ELSE 0 END) as complete
            FROM cards
            WHERE subject = ?
        """, (subject, subject)).fetchone()

        stats.append({
            'subject': result[0],
            'total': result[1],
            'placeholders': result[2],
            'complete': result[3]
        })

    if not hasattr(db_path, 'execute'):
        conn.close()

    return sorted(stats, key=lambda x: x['placeholders'], reverse=True)


def display_mbe_menu(stats):
    """Display menu of MBE subjects"""
    clear_screen()
    print("\n" + "=" * 80)
    print("CARD ENHANCEMENT - MBE SUBJECTS ONLY")
    print("=" * 80)
    print("\nMBE subjects ranked by placeholders needing enhancement:\n")

    print(f"{'#':<4} {'SUBJECT':<25} {'PLACEHOLDERS':<15} {'COMPLETE':<12} {'TOTAL':<8} {'%DONE'}")
    print("-" * 80)

    for i, stat in enumerate(stats, 1):
        subject = stat['subject']
        total = stat['total']
        placeholders = stat['placeholders']
        complete = stat['complete']
        pct_done = (complete / total * 100) if total > 0 else 0

        marker = "✓" if placeholders == 0 else f"[{placeholders}]"

        print(f"{i:<4} {subject:<25} {placeholders:<15} {complete:<12} {total:<8} {pct_done:>5.1f}% {marker}")

    print("\n" + "=" * 80)
    print("Focus: Enhance placeholder cards with real bar prep content")
    print("=" * 80)


def select_subject(stats):
    """Let user select a subject"""
    while True:
        try:
            print("\nEnter subject number (or 'q' to quit): ", end="")
            choice = input().strip()

            if choice.lower() == 'q':
                return None

            num = int(choice)
            if 1 <= num <= len(stats):
                return stats[num - 1]['subject']
            else:
                print(f"Please enter a number between 1 and {len(stats)}")
        except ValueError:
            print("Please enter a valid number or 'q' to quit")
        except KeyboardInterrupt:
            print("\n")
            return None


def get_placeholder_cards(db, subject):
    """Get all placeholder cards for a subject"""
    query = """
        SELECT * FROM cards
        WHERE subject = ?
        AND (back LIKE '%Mnemonic%'
             OR back LIKE '%• Traps%'
             OR back LIKE '%• Micro-Hypos%')
        ORDER BY card_type, card_id
    """

    cursor = db.conn.cursor()
    cursor.execute(query, (subject,))
    rows = cursor.fetchall()

    return [db._row_to_card(row) for row in rows]


def display_card(card, card_num, total):
    """Display card for enhancement"""
    clear_screen()
    print("\n" + "=" * 80)
    print(f"CARD {card_num} of {total} - ENHANCEMENT MODE")
    print("=" * 80)
    print(f"Card ID: {card.card_id}")
    print(f"Subject: {card.subject}")
    print(f"Topic: {card.topic or '(none)'}")
    print(f"Card Type: {card.card_type}")
    print(f"Difficulty: {'⭐' * card.difficulty}")
    print("=" * 80)

    print("\nCURRENT FRONT:")
    print("-" * 80)
    print(card.front)

    print("\n" + "-" * 80)
    print("CURRENT BACK:")
    print("-" * 80)
    print(card.back)
    print("\n" + "=" * 80)


def create_editor_template(card):
    """Create template for editor"""
    template = f"""# Card Enhancement Template
# Card ID: {card.card_id}
# Subject: {card.subject} | Type: {card.card_type} | Difficulty: {card.difficulty}
#
# Instructions:
# 1. Paste enhanced content from ChatGPT below
# 2. Use FRONT: and BACK: sections (see format below)
# 3. Save and close editor to continue
# 4. Lines starting with # are ignored
#
# Format:
# FRONT:
# [your enhanced question here]
#
# BACK:
# [your enhanced answer here]
#

FRONT:
{card.front}

BACK:
{card.back}
"""
    return template


def open_editor(template):
    """Open text editor with template"""
    # Get editor from environment or use nano as default
    editor = os.environ.get('EDITOR', 'nano')

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tf:
        tf.write(template)
        temp_path = tf.name

    try:
        # Open editor
        print(f"\nOpening {editor}... (save and close to continue)")
        subprocess.call([editor, temp_path])

        # Read edited content
        with open(temp_path, 'r') as f:
            content = f.read()

        return content
    finally:
        # Clean up
        os.unlink(temp_path)


def parse_enhanced_content(content):
    """Parse FRONT: and BACK: sections from editor content"""
    lines = content.split('\n')

    front_lines = []
    back_lines = []
    current_section = None

    for line in lines:
        # Skip comments
        if line.strip().startswith('#'):
            continue

        # Check for section headers
        if line.strip() == 'FRONT:':
            current_section = 'front'
            continue
        elif line.strip() == 'BACK:':
            current_section = 'back'
            continue

        # Add to current section
        if current_section == 'front':
            front_lines.append(line)
        elif current_section == 'back':
            back_lines.append(line)

    # Join and strip
    front = '\n'.join(front_lines).strip()
    back = '\n'.join(back_lines).strip()

    return front, back


def preview_changes(card, new_front, new_back):
    """Preview changes before saving"""
    clear_screen()
    print("\n" + "=" * 80)
    print("PREVIEW ENHANCED CARD")
    print("=" * 80)
    print(f"Card ID: {card.card_id}")
    print(f"Subject: {card.subject} | Type: {card.card_type}")
    print("=" * 80)

    # Show front comparison
    print("\nFRONT (NEW):")
    print("-" * 80)
    print(new_front)

    # Show back comparison
    print("\n" + "-" * 80)
    print("BACK (NEW):")
    print("-" * 80)
    print(new_back)

    print("\n" + "=" * 80)


def confirm(prompt):
    """Get yes/no confirmation"""
    while True:
        try:
            response = input(f"\n{prompt} (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'")
        except KeyboardInterrupt:
            print("\n")
            return False


def enhance_card_workflow(db, card, card_num, total):
    """Single card enhancement workflow"""
    # Display current card
    display_card(card, card_num, total)

    print("\nOptions:")
    print("  e - Enhance this card (open editor)")
    print("  s - Skip this card")
    print("  q - Quit enhancement session")

    while True:
        choice = input("\nChoice (e/s/q): ").strip().lower()

        if choice == 'q':
            return 'quit'
        elif choice == 's':
            return 'skip'
        elif choice == 'e':
            break
        else:
            print("Please enter 'e', 's', or 'q'")

    # Open editor with template
    template = create_editor_template(card)
    edited_content = open_editor(template)

    # Parse enhanced content
    new_front, new_back = parse_enhanced_content(edited_content)

    # Check if content was actually changed
    if new_front == card.front and new_back == card.back:
        print("\n✗ No changes detected. Card not updated.")
        input("\nPress ENTER to continue...")
        return 'skip'

    # Check if content is not empty
    if not new_front or not new_back:
        print("\n✗ Front or back is empty. Card not updated.")
        input("\nPress ENTER to continue...")
        return 'skip'

    # Preview changes
    preview_changes(card, new_front, new_back)

    # Confirm save
    if confirm("Save enhanced card?"):
        # Update card
        card.front = new_front
        card.back = new_back
        card.updated_at = datetime.now()

        # Save to database
        db.update_card(card)

        print(f"\n✓ Card enhanced and saved!")
        return 'enhanced'
    else:
        print("\n✗ Changes discarded.")
        return 'skip'


def run_enhancement_session():
    """Run card enhancement session"""
    # Get MBE subject statistics
    stats = get_mbe_subject_stats()

    if not stats:
        print("\nNo MBE subjects found in database!")
        return

    # Display menu and select subject
    display_mbe_menu(stats)
    subject = select_subject(stats)

    if not subject:
        print("\nGoodbye!")
        return

    # Open database
    db = AdaptiveLearningDatabase("iowa_bar_prep.db")

    # Get placeholder cards for subject
    cards = get_placeholder_cards(db, subject)

    if not cards:
        clear_screen()
        print(f"\n✓ No placeholder cards found in {subject.upper().replace('_', ' ')}!")
        print("All cards are complete.\n")
        db.close()
        return

    clear_screen()
    print(f"\n📝 {subject.upper().replace('_', ' ')}")
    print(f"Found {len(cards)} placeholder cards to enhance\n")

    input("Press ENTER to start enhancement session...")

    # Track progress
    enhanced_count = 0
    skipped_count = 0

    try:
        for i, card in enumerate(cards, 1):
            result = enhance_card_workflow(db, card, i, len(cards))

            if result == 'quit':
                break
            elif result == 'enhanced':
                enhanced_count += 1
            elif result == 'skip':
                skipped_count += 1

    except KeyboardInterrupt:
        print("\n\nEnhancement session interrupted!")

    finally:
        # Close database
        db.close()

        # Show summary
        clear_screen()
        print("\n" + "=" * 80)
        print("ENHANCEMENT SESSION SUMMARY")
        print("=" * 80)
        print(f"\nSubject: {subject.upper().replace('_', ' ')}")
        print(f"Cards enhanced: {enhanced_count}")
        print(f"Cards skipped: {skipped_count}")
        print(f"Total processed: {enhanced_count + skipped_count} of {len(cards)}")

        remaining = len(cards) - enhanced_count - skipped_count
        if remaining > 0:
            print(f"Remaining: {remaining}")

        print("\n" + "=" * 80)

        if enhanced_count > 0:
            print(f"\n✓ Enhanced {enhanced_count} cards!")
            print("These cards are now ready for study with daily_study.py")

        print("\n")


if __name__ == "__main__":
    run_enhancement_session()

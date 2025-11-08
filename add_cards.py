#!/usr/bin/env python3
"""
Interactive Card Creator for Iowa Bar Prep
Manually add high-quality flashcards to iowa_bar_prep.db
"""

import hashlib
import sys
from datetime import datetime
from adaptive_learning_system import AdaptiveLearningDatabase, LearningCard


# 14 Iowa Bar Exam subjects
SUBJECTS = [
    "contracts",
    "torts",
    "constitutional_law",
    "criminal_law",
    "criminal_procedure",
    "civil_procedure",
    "evidence",
    "real_property",
    "professional_responsibility",
    "corporations",
    "wills_trusts_estates",
    "family_law",
    "secured_transactions",
    "iowa_procedure",
]

CARD_TYPES = [
    "rule",
    "elements",
    "exceptions",
    "traps",
    "policy",
]


def clear_screen():
    """Clear the terminal screen"""
    print("\033[2J\033[H", end="")


def display_menu(title, items):
    """Display a numbered menu"""
    print(f"\n{title}")
    print("=" * 60)
    for i, item in enumerate(items, 1):
        print(f"{i:2}. {item}")
    print("=" * 60)


def select_from_menu(title, items):
    """Let user select from a numbered menu"""
    display_menu(title, items)

    while True:
        try:
            choice = input(f"\nSelect (1-{len(items)}): ").strip()
            num = int(choice)
            if 1 <= num <= len(items):
                return items[num - 1]
            print(f"Please enter a number between 1 and {len(items)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n")
            return None


def get_multiline_input(prompt, end_marker="@@"):
    """Get multi-line input from user"""
    print(f"\n{prompt}")
    print(f"(Enter '{end_marker}' on a new line or press ENTER twice to finish)")
    print("-" * 60)

    lines = []
    empty_count = 0

    while True:
        try:
            line = input()

            # Check for end marker
            if line.strip() == end_marker:
                break

            # Check for double empty line
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    # Remove the last empty line that was added
                    if lines and lines[-1] == "":
                        lines.pop()
                    break
                lines.append(line)
            else:
                empty_count = 0
                lines.append(line)

        except KeyboardInterrupt:
            print("\n")
            return None

    return "\n".join(lines).strip()


def generate_card_id(subject, card_type):
    """Generate unique card ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    raw_id = f"{subject}_{card_type}_{timestamp}"
    # Create a short hash for uniqueness
    hash_obj = hashlib.md5(raw_id.encode())
    return hash_obj.hexdigest()[:16]


def preview_card(card_data):
    """Display card preview"""
    clear_screen()
    print("\n" + "=" * 70)
    print("CARD PREVIEW")
    print("=" * 70)
    print(f"Subject: {card_data['subject']}")
    print(f"Topic: {card_data['topic'] or '(none)'}")
    print(f"Card Type: {card_data['card_type']}")
    print(f"Difficulty: {'⭐' * card_data['difficulty']}")
    print("=" * 70)

    print("\nFRONT:")
    print("-" * 70)
    print(card_data['front'])

    print("\n" + "-" * 70)
    print("BACK:")
    print("-" * 70)
    print(card_data['back'])
    print("\n" + "=" * 70)


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


def create_card_interactive():
    """Interactive card creation workflow"""
    clear_screen()
    print("\n" + "=" * 70)
    print("CREATE NEW FLASHCARD")
    print("=" * 70)

    # Select subject
    subject = select_from_menu("SELECT SUBJECT:", SUBJECTS)
    if not subject:
        return None

    # Enter topic (optional)
    print("\nEnter topic (optional, press ENTER to skip):")
    topic = input("> ").strip() or None

    # Select card type
    card_type = select_from_menu("SELECT CARD TYPE:", CARD_TYPES)
    if not card_type:
        return None

    # Select difficulty
    print("\nSelect difficulty (1-5):")
    print("1 = Fundamental")
    print("2 = Basic")
    print("3 = Intermediate")
    print("4 = Advanced")
    print("5 = Expert")

    while True:
        try:
            difficulty = int(input("\nDifficulty: ").strip())
            if 1 <= difficulty <= 5:
                break
            print("Please enter a number between 1 and 5")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n")
            return None

    # Get front (question)
    front = get_multiline_input("FRONT (Question):")
    if not front:
        print("\nCard creation cancelled.")
        return None

    # Get back (answer)
    back = get_multiline_input("BACK (Answer):")
    if not back:
        print("\nCard creation cancelled.")
        return None

    # Generate card ID
    card_id = generate_card_id(subject, card_type)

    # Create card data
    card_data = {
        'card_id': card_id,
        'concept_id': card_id,  # Use same as card_id
        'subject': subject,
        'topic': topic,
        'card_type': card_type,
        'front': front,
        'back': back,
        'difficulty': difficulty,
    }

    return card_data


def create_learning_card(card_data):
    """Create a LearningCard object from card data"""
    now = datetime.now()

    return LearningCard(
        card_id=card_data['card_id'],
        concept_id=card_data['concept_id'],
        subject=card_data['subject'],
        topic=card_data['topic'],
        card_type=card_data['card_type'],
        front=card_data['front'],
        back=card_data['back'],
        difficulty=card_data['difficulty'],
        ease_factor=2.5,
        interval=1,
        repetitions=0,
        last_reviewed=None,
        next_review=None,  # NULL means card is due for first review
        times_seen=0,
        times_correct=0,
        times_incorrect=0,
        average_confidence=0.0,
        created_at=now,
        updated_at=now,
    )


def main():
    """Main card creation loop"""
    clear_screen()
    print("\n" + "=" * 70)
    print("IOWA BAR PREP - FLASHCARD CREATOR")
    print("=" * 70)
    print("\nManually add high-quality flashcards to your database")
    print("\nTips:")
    print("  • Use @@  or double-ENTER to finish multi-line input")
    print("  • Preview your card before saving")
    print("  • Ctrl+C to cancel at any time")
    print("\n" + "=" * 70)

    input("\nPress ENTER to start...")

    db = AdaptiveLearningDatabase("iowa_bar_prep.db")
    cards_added = 0

    try:
        while True:
            # Create card interactively
            card_data = create_card_interactive()

            if not card_data:
                break

            # Preview the card
            preview_card(card_data)

            # Confirm save
            if confirm("Save this card?"):
                # Create LearningCard object
                card = create_learning_card(card_data)

                # Insert into database
                db.insert_card(card)
                cards_added += 1

                print(f"\n✓ Card saved! (ID: {card_data['card_id']})")
            else:
                print("\n✗ Card discarded.")

            # Ask to add another
            if not confirm("\nAdd another card?"):
                break

    except KeyboardInterrupt:
        print("\n\nCard creation interrupted!")

    finally:
        # Close database
        db.close()

        # Show summary
        clear_screen()
        print("\n" + "=" * 70)
        print("SESSION SUMMARY")
        print("=" * 70)
        print(f"\nCards added to database: {cards_added}")
        print("\n" + "=" * 70)
        print("\nYour new cards are ready for review!")
        print("Run: python3 daily_study.py")
        print("  or: python3 subject_study.py")
        print("\n")


if __name__ == "__main__":
    main()

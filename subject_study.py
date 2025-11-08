#!/usr/bin/env python3
"""
Subject-Based Study Session for Iowa Bar Prep
Filters out placeholder cards and focuses on subjects with complete content
"""

import sys
import sqlite3
from datetime import datetime
from adaptive_learning_system import AdaptiveLearningSystem, ConfidenceLevel


def clear_screen():
    """Clear the terminal screen"""
    print("\033[2J\033[H", end="")


def get_subject_statistics(db_path: str = "iowa_bar_prep.db"):
    """Get statistics for all subjects showing complete vs placeholder cards"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            subject,
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
        GROUP BY subject
        ORDER BY complete DESC
    """

    results = conn.execute(query).fetchall()
    conn.close()

    return results


def display_subject_menu(stats):
    """Display menu of subjects with their statistics"""
    clear_screen()
    print("\n" + "=" * 80)
    print("IOWA BAR PREP - SUBJECT STUDY")
    print("=" * 80)
    print("\nSubjects ranked by number of complete cards:\n")

    print(f"{'#':<4} {'SUBJECT':<30} {'COMPLETE':<12} {'PLACEHOLDERS':<15} {'TOTAL':<8} {'%COMPLETE'}")
    print("-" * 80)

    for i, stat in enumerate(stats, 1):
        subject = stat['subject']
        total = stat['total']
        complete = stat['complete']
        placeholders = stat['placeholders']
        pct_complete = (complete / total * 100) if total > 0 else 0

        # Color code by completion percentage
        if pct_complete >= 95:
            marker = "✓"
        elif pct_complete >= 80:
            marker = "~"
        else:
            marker = "!"

        print(f"{i:<4} {subject:<30} {complete:<12} {placeholders:<15} {total:<8} {pct_complete:>6.1f}% {marker}")

    print("\n" + "=" * 80)
    print("Legend: ✓ = 95%+ complete  ~ = 80%+ complete  ! = <80% complete")
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


def get_complete_cards(system: AdaptiveLearningSystem, subject: str, limit: int = 30):
    """Get cards for a subject, excluding placeholders"""
    query = """
        SELECT * FROM cards
        WHERE subject = ?
        AND back NOT LIKE '%Mnemonic%'
        AND back NOT LIKE '%• Traps%'
        AND back NOT LIKE '%• Micro-Hypos%'
        AND (next_review IS NULL OR next_review <= ?)
        ORDER BY next_review ASC
        LIMIT ?
    """

    cursor = system.db.conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(query, (subject, now, limit))

    rows = cursor.fetchall()
    return [system.db._row_to_card(row) for row in rows]


def print_header(session_num: int, total_due: int, subject: str):
    """Print session header"""
    print("=" * 70)
    print(f"SUBJECT STUDY: {subject.upper().replace('_', ' ')}")
    print("=" * 70)
    print(f"Card {session_num} of {total_due}")
    print("=" * 70)
    print()


def print_card_front(card, card_num: int):
    """Display the front of the card"""
    print(f"\n{'='*70}")
    print(f"Subject: {card.subject.upper()}")
    if card.topic:
        print(f"Topic: {card.topic}")
    print(f"Type: {card.card_type.upper()}")
    print(f"Difficulty: {'⭐' * card.difficulty}")
    print(f"{'='*70}\n")

    print(card.front)
    print()


def print_card_back(card):
    """Display the back of the card"""
    print("\n" + "─" * 70)
    print("ANSWER:")
    print("─" * 70 + "\n")
    print(card.back)
    print()


def get_confidence_rating() -> ConfidenceLevel:
    """Get confidence rating from user"""
    print("\n" + "=" * 70)
    print("How well did you know this?")
    print("=" * 70)
    print("0 - No Idea (Complete guess)")
    print("1 - Vague (Very uncertain)")
    print("2 - Uncertain (Somewhat remembered)")
    print("3 - Confident (Got it right)")
    print("4 - Mastered (Immediately knew it)")
    print("=" * 70)

    while True:
        try:
            choice = input("\nYour rating (0-4): ").strip()
            rating = int(choice)
            if 0 <= rating <= 4:
                return ConfidenceLevel(rating)
            print("Please enter a number between 0 and 4")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nStudy session interrupted!")
            sys.exit(0)


def print_review_result(card, confidence: ConfidenceLevel):
    """Show the result of the review"""
    print("\n" + "─" * 70)

    if confidence.value >= 3:
        print("✓ CORRECT - Good job!")
    else:
        print("✗ NEEDS REVIEW - Keep practicing!")

    print(f"Next review: {card.interval} day{'s' if card.interval != 1 else ''}")
    print(f"Ease factor: {card.ease_factor:.2f}")
    print(f"Accuracy: {card.calculate_accuracy():.1f}% ({card.times_correct}/{card.times_seen})")
    print("─" * 70)


def print_session_summary(subject: str, cards_reviewed: int, correct: int):
    """Print summary at end of session"""
    clear_screen()
    print("\n" + "=" * 70)
    print("SESSION COMPLETE!")
    print("=" * 70)
    print(f"\nSubject: {subject.upper().replace('_', ' ')}")
    print(f"Cards reviewed: {cards_reviewed}")
    if cards_reviewed > 0:
        print(f"Correct answers: {correct}/{cards_reviewed} ({correct/cards_reviewed*100:.1f}%)")
    print("\n" + "=" * 70)


def run_subject_study(limit: int = 30):
    """Run a subject-based study session"""
    # Get subject statistics
    stats = get_subject_statistics()

    if not stats:
        print("\nNo cards found in database!")
        return

    # Display menu and get selection
    display_subject_menu(stats)
    subject = select_subject(stats)

    if not subject:
        print("\nGoodbye!")
        return

    # Initialize system and get cards for subject
    system = AdaptiveLearningSystem("iowa_bar_prep.db")

    due_cards = get_complete_cards(system, subject, limit)

    if not due_cards:
        clear_screen()
        print(f"\n🎉 No complete cards due for review in {subject.upper().replace('_', ' ')}!")
        print("Either all cards are up to date, or this subject only has placeholder cards.\n")
        system.close()
        return

    clear_screen()
    print(f"\n📚 {subject.upper().replace('_', ' ')}")
    print(f"You have {len(due_cards)} complete cards due for review")
    print(f"Starting session with {min(limit, len(due_cards))} cards...\n")

    input("Press ENTER to begin...")

    cards_reviewed = 0
    correct_count = 0

    try:
        for i, card in enumerate(due_cards[:limit], 1):
            clear_screen()
            print_header(i, len(due_cards), subject)

            # Show front
            print_card_front(card, i)

            # Wait for user to think
            input("Press ENTER to reveal answer...")

            # Show back
            print_card_back(card)

            # Get confidence rating
            confidence = get_confidence_rating()

            # Update card using SM-2
            updated_card = system.review_card(card, confidence)

            # Show result
            print_review_result(updated_card, confidence)

            cards_reviewed += 1
            if confidence.value >= 3:
                correct_count += 1

            # Continue?
            if i < len(due_cards):
                try:
                    input("\nPress ENTER for next card (Ctrl+C to quit)...")
                except KeyboardInterrupt:
                    print("\n")
                    break

    except KeyboardInterrupt:
        print("\n\nStudy session interrupted!")

    finally:
        # Print summary
        print_session_summary(subject, cards_reviewed, correct_count)

        # Show subject stats
        subject_cards = system.db.get_cards_by_subject(subject)
        mastered = len([c for c in subject_cards if c.is_mastered()])

        print(f"\n{subject.upper().replace('_', ' ')} Progress:")
        print(f"  Total cards: {len(subject_cards)}")
        print(f"  Cards mastered: {mastered}")

        if cards_reviewed > 0:
            print(f"  Session accuracy: {correct_count/cards_reviewed*100:.1f}%")
        print()

        system.close()


if __name__ == "__main__":
    # Check for command line argument
    limit = 30
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print(f"Invalid limit: {sys.argv[1]}")
            print("Usage: python3 subject_study.py [number_of_cards]")
            sys.exit(1)

    run_subject_study(limit)

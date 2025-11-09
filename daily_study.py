#!/usr/bin/env python3
"""
Daily Study Session for Iowa Bar Prep
Works with existing 876-card database (iowa_bar_prep.db)
"""

import sys
import time
from datetime import datetime
from adaptive_learning_system import AdaptiveLearningSystem, ConfidenceLevel


def clear_screen():
    """Clear the terminal screen"""
    print("\033[2J\033[H", end="")


def print_header(session_num: int, total_due: int):
    """Print session header"""
    print("=" * 70)
    print(f"IOWA BAR PREP - DAILY STUDY SESSION")
    print("=" * 70)
    print(f"Card {session_num} of {total_due} due today")
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


def print_session_summary(cards_reviewed: int, correct: int, total: int):
    """Print summary at end of session"""
    clear_screen()
    print("\n" + "=" * 70)
    print("SESSION COMPLETE!")
    print("=" * 70)
    print(f"\nCards reviewed: {cards_reviewed}")
    print(f"Correct answers: {correct}/{cards_reviewed} ({correct/cards_reviewed*100:.1f}%)")
    print(f"Cards remaining today: {total - cards_reviewed}")
    print("\n" + "=" * 70)


def run_daily_study(limit: int = 30):
    """Run a daily study session"""
    system = AdaptiveLearningSystem("iowa_bar_prep.db")

    # Get due cards
    due_cards = system.db.get_due_cards(limit=limit)

    if not due_cards:
        print("\n🎉 No cards due for review today! Great job staying on track!\n")
        system.close()
        return

    print(f"\n📚 You have {len(due_cards)} cards due for review today")
    print(f"Starting session with {min(limit, len(due_cards))} cards...\n")

    input("Press ENTER to begin...")

    # Track session timing
    session_start_time = time.time()
    cards_reviewed = 0
    correct_count = 0
    quality_scores = []

    try:
        for i, card in enumerate(due_cards[:limit], 1):
            clear_screen()
            print_header(i, len(due_cards))

            # Track card timing
            card_start_time = time.time()

            # Show front
            print_card_front(card, i)

            # Wait for user to think
            input("Press ENTER to reveal answer...")

            # Show back
            print_card_back(card)

            # Get confidence rating
            confidence = get_confidence_rating()

            # Calculate time spent on this card
            card_time_seconds = int(time.time() - card_start_time)

            # Update card using SM-2 (this also records performance)
            updated_card = system.review_card(card, confidence)

            # Update the performance record with actual time
            # Get the last performance ID and update it
            cursor = system.db.conn.cursor()
            cursor.execute("""
                UPDATE performance
                SET time_seconds = ?
                WHERE id = (SELECT id FROM performance ORDER BY id DESC LIMIT 1)
            """, (card_time_seconds,))
            system.db.conn.commit()

            # Show result
            print_review_result(updated_card, confidence)

            cards_reviewed += 1
            quality_scores.append(confidence.value)
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
        # Calculate session duration
        session_duration_seconds = int(time.time() - session_start_time)
        session_duration_minutes = session_duration_seconds // 60

        # Save session summary if cards were reviewed
        if cards_reviewed > 0:
            avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
            system.db.insert_session(
                cards_reviewed=cards_reviewed,
                avg_quality=avg_quality,
                duration_minutes=max(1, session_duration_minutes)  # At least 1 minute
            )

        # Print summary
        print_session_summary(cards_reviewed, correct_count, len(due_cards))

        # Show session timing
        if cards_reviewed > 0:
            avg_seconds_per_card = session_duration_seconds / cards_reviewed
            print(f"\nSession Time:")
            print(f"  Duration: {session_duration_minutes} min {session_duration_seconds % 60} sec")
            print(f"  Avg per card: {avg_seconds_per_card:.1f} seconds")

        # Show overall stats
        stats = system.get_statistics()
        print(f"\nOverall Progress:")
        print(f"  Total cards: {stats['total_cards']}")
        print(f"  Cards mastered: {stats['cards_mastered']}")
        print(f"  Overall accuracy: {stats['overall_accuracy']:.1f}%")
        print(f"  Total reviews: {stats['total_reviews']}")
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
            print("Usage: python3 daily_study.py [number_of_cards]")
            sys.exit(1)

    run_daily_study(limit)

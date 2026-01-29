#!/usr/bin/env python3
"""
Bar Exam Flashcard Generator
Creates study flashcards from your 114-rule database
"""

import sys
sys.path.insert(0, 'src')
from black_letter_law import BlackLetterLawDatabase
import random

def generate_flashcards(subject=None, num_cards=10):
    """Generate random flashcards for bar exam prep"""
    db = BlackLetterLawDatabase('data/black_letter_law.json')

    if subject:
        rules = db.get_by_subject(subject)
    else:
        rules = db.rules

    # Randomly select rules
    selected = random.sample(rules, min(num_cards, len(rules)))

    print("=" * 80)
    print(f"BAR EXAM FLASHCARDS - {subject if subject else 'ALL SUBJECTS'}")
    print("=" * 80)

    for i, rule in enumerate(selected, 1):
        print(f"\n{'─' * 80}")
        print(f"CARD {i}/{len(selected)}: {rule.subject} - {rule.title}")
        print(f"{'─' * 80}")
        print("\n❓ QUESTION: What is the rule for this?")
        print("\n[Think about it...]\n")
        input("Press Enter to see answer...")

        print(f"\n✅ ANSWER:\n{rule.rule}")
        print(f"\n📋 ELEMENTS:")
        for elem in rule.elements:
            print(f"  • {elem}")

        if rule.citations:
            print(f"\n📚 CITATIONS: {', '.join(rule.citations[:2])}")

        print(f"\n{'─' * 80}")
        cont = input("\nContinue? (y/n): ")
        if cont.lower() != 'y':
            break

    print("\n✅ Study session complete!")


if __name__ == "__main__":
    print("\n🎓 BAR EXAM FLASHCARD GENERATOR")
    print("\nAvailable subjects:")
    print("  1. Constitutional Law (30 rules)")
    print("  2. Evidence (16 rules)")
    print("  3. Criminal Law (15 rules)")
    print("  4. Property (15 rules)")
    print("  5. Torts (13 rules)")
    print("  6. Contracts (13 rules)")
    print("  7. Civil Procedure (12 rules)")
    print("  8. All subjects (random)")

    choice = input("\nChoose subject (1-8): ")

    subjects = {
        '1': 'Constitutional Law',
        '2': 'Evidence',
        '3': 'Criminal Law',
        '4': 'Property',
        '5': 'Torts',
        '6': 'Contracts',
        '7': 'Civil Procedure',
        '8': None
    }

    subject = subjects.get(choice)
    num = int(input("How many flashcards? (1-20): "))

    generate_flashcards(subject, num)

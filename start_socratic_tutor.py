#!/usr/bin/env python3
"""
SOCRATIC TUTOR LAUNCHER - Real Teaching, Not Just Testing
Uses proven pedagogical techniques used by great law professors
"""

import sys
from integrated_tutor_system import IntegratedEliteTutor

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║" + " " * 20 + "SOCRATIC BAR TUTOR" + " " * 27 + "║")
    print("║" + " " * 14 + "Uses Real Teaching Methods" + " " * 25 + "║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    # Initialize the tutor
    print("🚀 Initializing Socratic tutor...")
    tutor = IntegratedEliteTutor()

    if not tutor.initialize():
        print("❌ Failed to initialize tutor")
        return

    print("✅ Socratic tutor ready!")
    print()

    # Show available subjects
    print("🎓 CHOOSE YOUR SUBJECT:")
    subjects = {
        'contracts': 'Formation, consideration, performance, breach, remedies',
        'torts': 'Negligence, intentional torts, strict liability, defamation',
        'conlaw': 'Due process, equal protection, first amendment',
        'crim': 'Mens rea, homicide, parties to crime',
        'crimpro': 'Search & seizure, Miranda, right to counsel',
        'civpro': 'Jurisdiction, pleadings, discovery',
        'evidence': 'Relevance, hearsay, character evidence',
        'property': 'Adverse possession, easements, covenants, fixtures, recording'
    }

    for i, (subject, desc) in enumerate(subjects.items(), 1):
        print(f"   {i}. {subject.title()} - {desc}")

    print()

    # Get user choice
    while True:
        choice = input("Enter subject (or 'quit'): ").strip().lower()

        if choice == 'quit':
            print("\n👋 Happy studying!")
            return

        if choice in subjects:
            print(f"\n🚀 Starting Socratic learning for {choice.upper()}...")
            print("This uses the Socratic method - expect lots of questions!")
            print("Press ENTER at each step to continue...")
            input("\nReady? Press ENTER... ")
            tutor.learn_with_me(choice, 3)
            return
        else:
            print(f"❌ '{choice}' not recognized. Try: {', '.join(subjects.keys())}")

if __name__ == "__main__":
    main()

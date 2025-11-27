#!/usr/bin/env python3
"""
Subject Summary Tool
Get complete overview of any subject with all rules

Usage:
    python3 subject_summary.py "Constitutional Law"
    python3 subject_summary.py Evidence
    python3 subject_summary.py Torts
"""

import sys
sys.path.insert(0, 'src')
from black_letter_law import BlackLetterLawDatabase

def show_subject_summary(subject_name):
    """Display all rules for a subject"""
    db = BlackLetterLawDatabase('data/black_letter_law.json')
    rules = db.get_by_subject(subject_name)

    if not rules:
        print(f"\n❌ Subject '{subject_name}' not found")
        print("\n📚 Available subjects:")
        subjects = set(rule.subject for rule in db.rules)
        for s in sorted(subjects):
            count = len(db.get_by_subject(s))
            print(f"  • {s} ({count} rules)")
        return

    # Organize by topic
    by_topic = {}
    for rule in rules:
        if rule.topic not in by_topic:
            by_topic[rule.topic] = []
        by_topic[rule.topic].append(rule)

    print("=" * 80)
    print(f"{subject_name.upper()} - COMPLETE SUMMARY")
    print("=" * 80)
    print(f"\n📊 {len(rules)} total rules across {len(by_topic)} topics\n")

    for topic in sorted(by_topic.keys()):
        print(f"\n{'▓' * 80}")
        print(f"TOPIC: {topic} ({len(by_topic[topic])} rules)")
        print(f"{'▓' * 80}")

        for i, rule in enumerate(by_topic[topic], 1):
            print(f"\n{i}. {rule.title}")
            print(f"   {rule.subtopic if rule.subtopic else ''}")
            print(f"\n   Rule: {rule.rule[:200]}{'...' if len(rule.rule) > 200 else ''}")

            if rule.elements:
                print(f"\n   Elements:")
                for elem in rule.elements[:3]:
                    print(f"     • {elem}")
                if len(rule.elements) > 3:
                    print(f"     ... ({len(rule.elements)} total)")

    print("\n" + "=" * 80)
    print(f"✅ {subject_name}: {len(rules)} rules reviewed")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        db = BlackLetterLawDatabase('data/black_letter_law.json')
        subjects = {}
        for rule in db.rules:
            subjects[rule.subject] = subjects.get(rule.subject, 0) + 1

        print("\n📚 SUBJECT SUMMARY TOOL")
        print("\nAvailable subjects:")
        for subject in sorted(subjects.keys(), key=lambda x: subjects[x], reverse=True):
            print(f"  • {subject:25s}: {subjects[subject]:2d} rules")

        print("\nUsage: python3 subject_summary.py [subject name]")
        print("\nExamples:")
        print('  python3 subject_summary.py "Constitutional Law"')
        print('  python3 subject_summary.py Evidence')
        print('  python3 subject_summary.py Torts')
        sys.exit(0)

    subject_name = ' '.join(sys.argv[1:])
    show_subject_summary(subject_name)

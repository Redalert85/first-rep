#!/usr/bin/env python3
"""
Quick Legal Lookup Tool
Search the 114-rule database instantly from command line

Usage:
    python3 quick_lookup.py hearsay
    python3 quick_lookup.py "rule against perpetuities"
    python3 quick_lookup.py negligence
"""

import sys
sys.path.insert(0, 'src')
from black_letter_law import BlackLetterLawDatabase

def quick_lookup(search_term):
    """Quick search and display results"""
    db = BlackLetterLawDatabase('data/black_letter_law.json')
    results = db.search_keyword(search_term)

    if not results:
        print(f"\n❌ No rules found for '{search_term}'")
        print("\n💡 Try searching for:")
        print("  • negligence, battery, defamation")
        print("  • hearsay, relevance, authentication")
        print("  • miranda, commerce clause, due process")
        print("  • consideration, breach, statute of frauds")
        print("  • jurisdiction, pleading, summary judgment")
        return

    print("=" * 80)
    print(f"SEARCH RESULTS: '{search_term}' ({len(results)} rules found)")
    print("=" * 80)

    for i, rule in enumerate(results, 1):
        print(f"\n{'─' * 80}")
        print(f"RESULT {i}: {rule.subject} → {rule.topic}")
        print(f"{'─' * 80}")
        print(f"\n📌 {rule.title}")
        print(f"\n{rule.rule}")

        if rule.elements:
            print(f"\n📋 Elements ({len(rule.elements)}):")
            for elem in rule.elements:
                print(f"  • {elem}")

        if rule.citations:
            print(f"\n📚 Key Citations:")
            for cite in rule.citations[:3]:
                print(f"  • {cite}")

        if rule.notes:
            print(f"\n💡 Notes: {rule.notes}")

    print("\n" + "=" * 80)
    print(f"✅ Found {len(results)} rule(s) matching '{search_term}'")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n🔍 QUICK LEGAL LOOKUP TOOL")
        print("\nUsage: python3 quick_lookup.py [search term]")
        print("\nExamples:")
        print("  python3 quick_lookup.py hearsay")
        print("  python3 quick_lookup.py 'miranda rights'")
        print("  python3 quick_lookup.py negligence")
        print("  python3 quick_lookup.py jurisdiction")
        print("\n📚 Database contains 114 rules across 7 subjects")
        sys.exit(0)

    search_term = ' '.join(sys.argv[1:])
    quick_lookup(search_term)

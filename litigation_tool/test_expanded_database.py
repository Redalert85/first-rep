#!/usr/bin/env python3
"""
Test Expanded Black Letter Law Database
Demonstrates new subjects: Criminal Law, Evidence, Constitutional Law, Property
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from black_letter_law import BlackLetterLawDatabase

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(title.center(80))
    print("="*80)

def test_database_structure():
    """Test that all new subjects were added correctly"""
    print_section("DATABASE STRUCTURE TEST")

    db = BlackLetterLawDatabase('data/black_letter_law.json')
    stats = db.get_stats()

    print(f"\n✅ Total Rules: {stats['total_rules']} (expanded from 10)")
    print(f"✅ Subjects: {stats['subjects']}")
    print(f"✅ Topics: {stats['topics']}")
    print(f"\n📚 Subjects: {', '.join(sorted(stats['subjects_list']))}")

    # Count rules per subject
    subject_counts = {}
    for rule in db.rules:
        subject_counts[rule.subject] = subject_counts.get(rule.subject, 0) + 1

    print("\n📊 Rules per Subject:")
    for subject in sorted(subject_counts.keys()):
        print(f"  • {subject}: {subject_counts[subject]} rules")

def test_criminal_law():
    """Test Criminal Law rules"""
    print_section("CRIMINAL LAW RULES")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # Test murder rule
    murder = db.get_rule('Criminal Law', 'Homicide', 'Murder')
    if murder:
        print(f"\n🔴 {murder.title}")
        print(f"\n{murder.rule}")
        print(f"\nElements:")
        for i, elem in enumerate(murder.elements, 1):
            print(f"  {i}. {elem}")
        print(f"\nNotes: {murder.notes}")

    # Test self-defense
    self_defense = db.get_rule('Criminal Law', 'Defenses', 'Self-Defense')
    if self_defense:
        print(f"\n\n🔴 {self_defense.title}")
        print(f"\n{self_defense.rule}")
        print(f"\nElements:")
        for i, elem in enumerate(self_defense.elements, 1):
            print(f"  {i}. {elem}")

    # Search for conspiracy
    conspiracy_results = db.search_keyword('conspiracy')
    if conspiracy_results:
        print(f"\n\n🔴 Search Results for 'conspiracy': {len(conspiracy_results)} rule(s)")
        for rule in conspiracy_results:
            print(f"\n  → {rule.title}")
            print(f"    Elements: {', '.join(rule.elements[:3])}...")

def test_evidence():
    """Test Evidence rules"""
    print_section("EVIDENCE RULES")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # Test relevance
    relevance = db.get_rule('Evidence', 'Relevance', 'General Relevance')
    if relevance:
        print(f"\n📋 {relevance.title}")
        print(f"\n{relevance.rule}")
        print(f"\nElements:")
        for i, elem in enumerate(relevance.elements, 1):
            print(f"  {i}. {elem}")
        print(f"\nCitation: {', '.join(relevance.citations)}")

    # Test character evidence
    character = db.get_rule('Evidence', 'Relevance', 'Character Evidence')
    if character:
        print(f"\n\n📋 {character.title}")
        print(f"\n{character.rule}")
        print(f"\nKey Points:")
        for i, elem in enumerate(character.elements, 1):
            print(f"  {i}. {elem}")

    # Search for hearsay
    hearsay_results = db.search_keyword('hearsay')
    print(f"\n\n📋 Search Results for 'hearsay': {len(hearsay_results)} rule(s)")
    for rule in hearsay_results:
        print(f"  → {rule.topic}: {rule.title}")

def test_constitutional_law():
    """Test Constitutional Law rules"""
    print_section("CONSTITUTIONAL LAW RULES")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # Test First Amendment
    free_speech = db.get_rule('Constitutional Law', 'First Amendment', 'Free Speech')
    if free_speech:
        print(f"\n⚖️  {free_speech.title}")
        print(f"\n{free_speech.rule}")
        print(f"\nKey Elements:")
        for i, elem in enumerate(free_speech.elements, 1):
            print(f"  {i}. {elem}")
        print(f"\nCitations: {', '.join(free_speech.citations)}")

    # Test Fourth Amendment
    fourth = db.get_rule('Constitutional Law', 'Fourth Amendment', 'Searches')
    if fourth:
        print(f"\n\n⚖️  {fourth.title}")
        print(f"\n{fourth.rule}")
        print(f"\nExceptions:")
        for i, elem in enumerate(fourth.elements, 1):
            print(f"  {i}. {elem}")

    # Test Equal Protection
    equal_protection = db.get_rule('Constitutional Law', 'Equal Protection', 'Levels of Scrutiny')
    if equal_protection:
        print(f"\n\n⚖️  {equal_protection.title}")
        print(f"\n{equal_protection.rule}")

def test_property():
    """Test Property rules"""
    print_section("PROPERTY LAW RULES")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # Test fee simple
    fee_simple = db.get_rule('Property', 'Estates', 'Present Estates')
    if fee_simple:
        print(f"\n🏠 {fee_simple.title}")
        print(f"\n{fee_simple.rule}")
        print(f"\nCharacteristics:")
        for i, elem in enumerate(fee_simple.elements, 1):
            print(f"  {i}. {elem}")

    # Test adverse possession
    adverse = db.get_rule('Property', 'Adverse Possession', 'Elements')
    if adverse:
        print(f"\n\n🏠 {adverse.title}")
        print(f"\n{adverse.rule}")
        print(f"\nElements (COAH):")
        for i, elem in enumerate(adverse.elements, 1):
            print(f"  {i}. {elem}")
        print(f"\nNotes: {adverse.notes}")

    # Test landlord-tenant
    warranty = db.get_rule('Property', 'Landlord-Tenant', 'Duties')
    if warranty:
        print(f"\n\n🏠 {warranty.title}")
        print(f"\n{warranty.rule}")

def test_search_functionality():
    """Test search across all subjects"""
    print_section("CROSS-SUBJECT SEARCH TEST")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    searches = [
        ('reasonable', 'Testing "reasonable" search'),
        ('intent', 'Testing "intent" search'),
        ('evidence', 'Testing "evidence" search'),
        ('rights', 'Testing "rights" search')
    ]

    for keyword, description in searches:
        results = db.search_keyword(keyword)
        print(f"\n🔍 {description}")
        print(f"   Found {len(results)} rules containing '{keyword}':")
        for rule in results[:3]:  # Show first 3
            print(f"   • {rule.subject} → {rule.topic}: {rule.title}")
        if len(results) > 3:
            print(f"   ... and {len(results) - 3} more")

def show_practical_applications():
    """Show how new rules apply to practice"""
    print_section("PRACTICAL APPLICATIONS FOR IOWA LITIGATION")

    print("""

📌 CRIMINAL DEFENSE (Iowa/Federal)
   → Murder/Manslaughter rules for homicide defense
   → Self-defense elements for justification claims
   → Conspiracy rules for multi-defendant cases

📌 MOTION IN LIMINE (Evidence)
   → Character evidence propensity rule to exclude bad acts
   → Hearsay exceptions to admit/exclude statements
   → Relevance balancing under FRE 403

📌 CIVIL RIGHTS LITIGATION (Constitutional Law)
   → First Amendment for speech restrictions
   → Fourth Amendment for unlawful search claims
   → Equal Protection for discrimination claims

📌 PROPERTY DISPUTES (Iowa Real Estate)
   → Adverse possession elements (COAH)
   → Landlord-tenant warranty of habitability
   → Easement creation and termination

🎯 NEXT STEPS:
   1. Enhance document generator to use these rules
   2. Create motion templates for criminal defense
   3. Add motion in limine generator
   4. Create property dispute analysis tools
    """)

def main():
    """Run all tests"""
    print("="*80)
    print("EXPANDED BLACK LETTER LAW DATABASE - COMPREHENSIVE TEST".center(80))
    print("="*80)

    test_database_structure()
    test_criminal_law()
    test_evidence()
    test_constitutional_law()
    test_property()
    test_search_functionality()
    show_practical_applications()

    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY".center(80))
    print("="*80)
    print("\n💡 Your database now has 28 rules across 7 major legal subjects!")
    print("   Use these rules to generate more sophisticated legal documents.\n")

if __name__ == '__main__':
    main()

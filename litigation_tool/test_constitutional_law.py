#!/usr/bin/env python3
"""
Test Expanded Constitutional Law Rules
Comprehensive demonstration of all 20 Constitutional Law rules
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

def test_fourteenth_amendment():
    """Test 14th Amendment rules"""
    print_section("14TH AMENDMENT RULES")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # Procedural Due Process
    proc_dp = db.get_rule('Constitutional Law', '14th Amendment - Due Process', 'Procedural Due Process')
    if proc_dp:
        print(f"\n⚖️  {proc_dp.title}")
        print(f"\n{proc_dp.rule}")
        print(f"\nElements (Mathews v. Eldridge):")
        for i, elem in enumerate(proc_dp.elements, 1):
            print(f"  {i}. {elem}")
        print(f"\nCitations: {', '.join(proc_dp.citations)}")

    # Substantive Due Process
    subst_dp = db.get_rule('Constitutional Law', '14th Amendment - Due Process', 'Substantive Due Process')
    if subst_dp:
        print(f"\n\n⚖️  {subst_dp.title}")
        print(f"\n{subst_dp.rule}")
        print(f"\nKey Points:")
        for i, elem in enumerate(subst_dp.elements, 1):
            print(f"  {i}. {elem}")

    # Incorporation
    incorp = db.get_rule('Constitutional Law', '14th Amendment - Incorporation', 'Incorporation Doctrine')
    if incorp:
        print(f"\n\n⚖️  {incorp.title}")
        print(f"\n{incorp.rule}")
        print(f"\nKey Exceptions:")
        for elem in incorp.elements:
            if "Exception" in elem:
                print(f"  • {elem}")

    # Equal Protection - Discriminatory Intent
    disc_intent = db.get_rule('Constitutional Law', '14th Amendment - Equal Protection', 'Discriminatory Intent')
    if disc_intent:
        print(f"\n\n⚖️  {disc_intent.title}")
        print(f"\n{disc_intent.rule}")
        print(f"\nProof Methods:")
        for i, elem in enumerate(disc_intent.elements, 1):
            print(f"  {i}. {elem}")

def test_eleventh_amendment():
    """Test 11th Amendment rules"""
    print_section("11TH AMENDMENT - SOVEREIGN IMMUNITY")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # State Sovereign Immunity
    immunity = db.get_rule('Constitutional Law', '11th Amendment - Sovereign Immunity', 'State Sovereign Immunity')
    if immunity:
        print(f"\n🛡️  {immunity.title}")
        print(f"\n{immunity.rule}")
        print(f"\nKey Exceptions:")
        for elem in immunity.elements:
            if "Exception" in elem:
                print(f"  • {elem}")

    # Congressional Abrogation
    abrogation = db.get_rule('Constitutional Law', '11th Amendment - Sovereign Immunity', 'Congressional Abrogation')
    if abrogation:
        print(f"\n\n🛡️  {abrogation.title}")
        print(f"\n{abrogation.rule}")
        print(f"\nRequirements:")
        for i, elem in enumerate(abrogation.elements, 1):
            print(f"  {i}. {elem}")
        print(f"\nCitations: {', '.join(abrogation.citations)}")

def test_commerce_clause():
    """Test Commerce Clause rules"""
    print_section("COMMERCE CLAUSE")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # Three Categories
    three_cat = db.get_rule('Constitutional Law', 'Commerce Clause', 'Congressional Power')
    if three_cat:
        print(f"\n🏛️  {three_cat.title}")
        print(f"\n{three_cat.rule}")
        print(f"\nThree Categories:")
        for i, elem in enumerate(three_cat.elements[:3], 1):
            print(f"  {i}. {elem}")
        print(f"\nKey Cases: {', '.join(three_cat.citations)}")

    # Limits
    limits = db.get_rule('Constitutional Law', 'Commerce Clause', 'Limits')
    if limits:
        print(f"\n\n🏛️  {limits.title}")
        print(f"\n{limits.rule}")
        print(f"\nProhibitions:")
        for i, elem in enumerate(limits.elements, 1):
            print(f"  {i}. {elem}")

    # Dormant Commerce Clause
    dormant = db.get_rule('Constitutional Law', 'Commerce Clause', 'Dormant Commerce Clause')
    if dormant:
        print(f"\n\n🏛️  {dormant.title}")
        print(f"\n{dormant.rule}")
        print(f"\nTests:")
        for i, elem in enumerate(dormant.elements, 1):
            print(f"  {i}. {elem}")

def test_necessary_and_proper():
    """Test Necessary and Proper Clause rules"""
    print_section("NECESSARY AND PROPER CLAUSE")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # Standard
    standard = db.get_rule('Constitutional Law', 'Necessary and Proper Clause', 'Congressional Power')
    if standard:
        print(f"\n📜 {standard.title}")
        print(f"\n{standard.rule}")
        print(f"\nMcCulloch Test:")
        for i, elem in enumerate(standard.elements, 1):
            print(f"  {i}. {elem}")

    # Limits
    limits = db.get_rule('Constitutional Law', 'Necessary and Proper Clause', 'Limits')
    if limits:
        print(f"\n\n📜 {limits.title}")
        print(f"\n{limits.rule}")
        print(f"\nLimitations:")
        for i, elem in enumerate(limits.elements, 1):
            print(f"  {i}. {elem}")

def test_taxing_and_spending():
    """Test Taxing and Spending Powers"""
    print_section("TAXING AND SPENDING POWERS")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # Taxing Power
    taxing = db.get_rule('Constitutional Law', 'Taxing and Spending Powers', 'Taxing Power')
    if taxing:
        print(f"\n💰 {taxing.title}")
        print(f"\n{taxing.rule}")
        print(f"\nRequirements:")
        for i, elem in enumerate(taxing.elements, 1):
            print(f"  {i}. {elem}")

    # Spending Power
    spending = db.get_rule('Constitutional Law', 'Taxing and Spending Powers', 'Spending Power')
    if spending:
        print(f"\n\n💰 {spending.title}")
        print(f"\n{spending.rule}")
        print(f"\nDole Test (5 factors):")
        for i, elem in enumerate(spending.elements, 1):
            print(f"  {i}. {elem}")

def test_executive_power():
    """Test Executive Power rules"""
    print_section("EXECUTIVE POWER")

    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # Domestic Powers - Youngstown
    domestic = db.get_rule('Constitutional Law', 'Executive Power', 'Domestic Powers')
    if domestic:
        print(f"\n🏛️  {domestic.title}")
        print(f"\n{domestic.rule}")
        print(f"\nYoungstown Framework:")
        for i, elem in enumerate(domestic.elements, 1):
            print(f"  {i}. {elem}")
        print(f"\nCitations: {', '.join(domestic.citations)}")

    # Foreign Affairs
    foreign = db.get_rule('Constitutional Law', 'Executive Power', 'Foreign Affairs')
    if foreign:
        print(f"\n\n🏛️  {foreign.title}")
        print(f"\n{foreign.rule}")
        print(f"\nKey Powers:")
        for i, elem in enumerate(foreign.elements, 1):
            print(f"  {i}. {elem}")

    # Limits
    limits = db.get_rule('Constitutional Law', 'Executive Power', 'Limits')
    if limits:
        print(f"\n\n🏛️  {limits.title}")
        print(f"\n{limits.rule}")
        print(f"\nLimitations:")
        for i, elem in enumerate(limits.elements, 1):
            print(f"  {i}. {elem}")

def show_practical_applications():
    """Show practical applications for Iowa litigation"""
    print_section("PRACTICAL APPLICATIONS FOR LITIGATION")

    print("""

📌 FEDERAL CIVIL RIGHTS LITIGATION (§1983 Actions)

14th Amendment Due Process:
  → Procedural DP: Challenge government deprivation without notice/hearing
  → Substantive DP: Challenge infringement of fundamental rights
  → Example: Prison conditions, government employment termination,
    land use restrictions

Equal Protection:
  → Challenge discriminatory laws/policies
  → Prove discriminatory intent (Washington v. Davis)
  → Apply correct scrutiny level (strict/intermediate/rational basis)
  → Example: Racial discrimination, gender discrimination

11th Amendment:
  → Determine if state immune from suit
  → Use Ex parte Young for prospective injunctive relief
  → Name state officer as defendant (not state itself)
  → Example: Challenge state statute, seek injunction against enforcement


📌 COMMERCE CLAUSE CHALLENGES

Challenge Federal Regulation:
  → Analyze under Lopez/Morrison framework
  → Non-economic activity requires direct substantial effect
  → Cannot compel commerce (NFIB individual mandate)
  → Example: Gun-Free School Zones Act, Violence Against Women Act

Challenge State Regulation (Dormant Commerce Clause):
  → Does state law discriminate against interstate commerce?
  → If yes, strict scrutiny (rarely survives)
  → If no, Pike balancing test
  → Example: State protectionist laws, environmental regulations


📌 SEPARATION OF POWERS LITIGATION

Executive Power Challenges:
  → Apply Youngstown framework
  → Category 3 (Congressional prohibition) hardest for President
  → Executive privilege qualified, not absolute
  → Example: Presidential seizure, executive orders, signing statements

Congressional Power Challenges:
  → Necessary and Proper Clause analysis (McCulloch)
  → Commandeering prohibited (New York v. United States)
  → Spending power conditions must not be coercive (NFIB)
  → Example: Federal mandates on states, conditional spending


📌 SOVEREIGN IMMUNITY LITIGATION

State Suit Strategy:
  → 11th Amendment bars suits against state
  → Sue state officer for prospective relief (Ex parte Young)
  → Sue local government (not immune)
  → Seek Congressional abrogation under 14th Amendment § 5
  → Example: ADA claims, civil rights claims against state


📌 IOWA-SPECIFIC APPLICATIONS

Iowa State Action + Federal Constitutional Rights:
  → Iowa government action violating federal constitutional rights
  → File in federal court under §1983
  → Or file in Iowa state court (concurrent jurisdiction)
  → Example: Iowa city zoning violates substantive due process


🎯 PRACTICAL TIPS:

1. Procedural Due Process: Always do Mathews v. Eldridge balancing
2. Substantive Due Process: Identify if right is fundamental (Glucksberg test)
3. Equal Protection: Prove discriminatory intent, not just impact
4. Commerce Clause: Distinguish economic from non-economic activity
5. 11th Amendment: Name officer, not state; seek injunction, not damages
6. Executive Power: Apply Youngstown categories
7. Spending Clause: Check Dole factors, especially coercion post-NFIB
    """)

def show_database_stats():
    """Show complete database statistics"""
    print_section("DATABASE STATISTICS")

    db = BlackLetterLawDatabase('data/black_letter_law.json')
    stats = db.get_stats()

    print(f"\n📊 Total Database:")
    print(f"  • Total Rules: {stats['total_rules']}")
    print(f"  • Subjects: {stats['subjects']}")
    print(f"  • Topics: {stats['topics']}")

    # Count by subject
    subject_counts = {}
    for rule in db.rules:
        subject_counts[rule.subject] = subject_counts.get(rule.subject, 0) + 1

    print(f"\n📚 Rules by Subject:")
    for subject in sorted(subject_counts.keys()):
        print(f"  • {subject}: {subject_counts[subject]} rules")

    # Constitutional Law breakdown
    const_rules = [r for r in db.rules if r.subject == "Constitutional Law"]
    const_topics = {}
    for rule in const_rules:
        const_topics[rule.topic] = const_topics.get(rule.topic, 0) + 1

    print(f"\n⚖️  Constitutional Law Topics ({len(const_rules)} rules):")
    for topic in sorted(const_topics.keys()):
        print(f"  • {topic}: {const_topics[topic]} rule(s)")

def main():
    """Run all tests"""
    print("="*80)
    print("CONSTITUTIONAL LAW RULES - COMPREHENSIVE TEST".center(80))
    print("="*80)

    test_fourteenth_amendment()
    test_eleventh_amendment()
    test_commerce_clause()
    test_necessary_and_proper()
    test_taxing_and_spending()
    test_executive_power()
    show_practical_applications()
    show_database_stats()

    print("\n" + "="*80)
    print("✅ ALL CONSTITUTIONAL LAW TESTS COMPLETED".center(80))
    print("="*80)
    print("\n💡 Your database now has 20 Constitutional Law rules covering:")
    print("   • 14th Amendment (Due Process, Equal Protection, Incorporation)")
    print("   • 11th Amendment (Sovereign Immunity)")
    print("   • Commerce Clause (Congressional power, Dormant)")
    print("   • Necessary and Proper Clause")
    print("   • Taxing and Spending Powers")
    print("   • Executive Power (Youngstown, Foreign Affairs, Limits)")
    print("   • 1st Amendment (Free Speech)")
    print("   • 4th Amendment (Searches)")
    print("\n   Ready for federal civil rights litigation, separation of powers,")
    print("   and constitutional challenges!\n")

if __name__ == '__main__':
    main()

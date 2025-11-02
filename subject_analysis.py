#!/usr/bin/env python3
"""
Subject Analysis & Expansion Recommendations
Analyzes current concept coverage and suggests improvements
"""

import json
from pathlib import Path

def analyze_subjects():
    """Analyze current subject coverage"""

    knowledge_file = Path(__file__).parent / 'data' / 'knowledge_849.json'
    with open(knowledge_file) as f:
        data = json.load(f)

    concepts = data['concepts']

    print("\n" + "="*80)
    print(" "*25 + "SUBJECT ANALYSIS REPORT")
    print("="*80 + "\n")

    # Bar exam importance weights (based on MBE/MEE frequency)
    importance = {
        'contracts': 10,          # High MBE + MEE frequency
        'torts': 10,              # High MBE frequency
        'constitutional_law': 9,   # High MBE frequency
        'civil_procedure': 9,      # High MBE frequency
        'evidence': 10,            # High MBE frequency + complex
        'criminal_law': 8,         # Moderate MBE frequency
        'criminal_procedure': 7,   # MEE tested
        'real_property': 9,        # High MBE frequency + complex
        'business_associations': 7, # MEE only but important
        'family_law': 6,           # MEE occasional
        'secured_transactions': 5, # MEE occasional but technical
        'trusts_estates': 7,       # MEE important
        'conflict_of_laws': 4      # MEE rare but crossover
    }

    # Complexity ratings (1-10, higher = more complex)
    complexity = {
        'evidence': 10,            # Hearsay exceptions, FRE
        'civil_procedure': 9,      # Jurisdiction, Erie, complex procedural rules
        'real_property': 9,        # Future interests, RAP, estates
        'secured_transactions': 8, # UCC Article 9 is technical
        'constitutional_law': 8,   # Multiple levels of scrutiny, complex doctrine
        'trusts_estates': 7,       # Technical rules, many exceptions
        'contracts': 7,            # UCC vs common law, many defenses
        'torts': 6,                # Straightforward but many torts
        'business_associations': 6,# Corporate law technical but logical
        'criminal_law': 5,         # Relatively straightforward
        'criminal_procedure': 6,   # Constitutional rules
        'family_law': 4,           # Policy-driven, less technical
        'conflict_of_laws': 5      # Logical frameworks
    }

    # Calculate metrics
    analysis = []
    for subject, subject_concepts in concepts.items():
        count = len(subject_concepts)
        imp = importance.get(subject, 5)
        comp = complexity.get(subject, 5)

        # Concepts with full teaching content
        with_teaching = sum(1 for c in subject_concepts
                          if c.get('teach') and c.get('question') and c.get('choices'))

        teaching_pct = (with_teaching / count * 100) if count > 0 else 0

        # Priority score (higher = more important to expand)
        # Formula: (importance * complexity) / (concepts * teaching_quality)
        priority = (imp * comp) / (count * (teaching_pct / 100 + 0.1))

        analysis.append({
            'subject': subject,
            'count': count,
            'importance': imp,
            'complexity': comp,
            'teaching_pct': teaching_pct,
            'priority': priority
        })

    # Sort by priority
    analysis.sort(key=lambda x: x['priority'], reverse=True)

    return analysis


def print_recommendations(analysis):
    """Print detailed recommendations"""

    print("📊 CURRENT COVERAGE:\n")
    print(f"{'Subject':<30} {'Concepts':<10} {'Importance':<12} {'Complexity':<12} {'Teaching %':<12} {'Priority'}")
    print("-" * 90)

    for item in analysis:
        subject = item['subject'].replace('_', ' ').title()
        print(f"{subject:<30} {item['count']:<10} {item['importance']:<12} {item['complexity']:<12} {item['teaching_pct']:<11.0f}% {item['priority']:.1f}")

    print("\n" + "="*80)
    print("🎯 EXPANSION RECOMMENDATIONS")
    print("="*80 + "\n")

    # Top 3 priorities
    top_3 = analysis[:3]

    print("TOP 3 SUBJECTS TO EXPAND:\n")
    for i, item in enumerate(top_3, 1):
        subject = item['subject']
        subject_display = subject.replace('_', ' ').title()

        print(f"{i}. {subject_display.upper()}")
        print(f"   Current: {item['count']} concepts")
        print(f"   Priority Score: {item['priority']:.1f}")

        # Specific recommendations
        if subject == 'evidence':
            print("   📈 RECOMMENDED EXPANSION: 70 → 120 concepts")
            print("   Focus Areas:")
            print("      • Hearsay exceptions (30+ variations)")
            print("      • Character evidence rules")
            print("      • Expert testimony (Daubert/Frye)")
            print("      • Privileges (attorney-client, spousal, etc.)")
            print("      • Prior statements and impeachment")
            print("      • Best evidence rule variations")

        elif subject == 'civil_procedure':
            print("   📈 RECOMMENDED EXPANSION: 60 → 100 concepts")
            print("   Focus Areas:")
            print("      • Personal jurisdiction deep dive (stream of commerce, Internet)")
            print("      • Subject matter jurisdiction edge cases")
            print("      • Erie doctrine applications")
            print("      • Discovery disputes and privileges")
            print("      • Class action certification requirements")
            print("      • Joinder and intervention scenarios")

        elif subject == 'real_property':
            print("   📈 RECOMMENDED EXPANSION: 85 → 130 concepts")
            print("   Focus Areas:")
            print("      • Future interests (30+ variations)")
            print("      • Rule Against Perpetuities applications")
            print("      • Easements (express, implied, prescriptive)")
            print("      • Covenants running with the land")
            print("      • Landlord-tenant specific issues")
            print("      • Recording acts and priority")
            print("      • Adverse possession state variations")

        elif subject == 'constitutional_law':
            print("   📈 RECOMMENDED EXPANSION: 70 → 110 concepts")
            print("   Focus Areas:")
            print("      • Free speech categories (public forum, content-based, etc.)")
            print("      • Equal protection by classification")
            print("      • Specific Bill of Rights applications")
            print("      • Takings Clause variations")
            print("      • Commerce Clause limits")
            print("      • State action doctrine edge cases")

        elif subject == 'contracts':
            print("   📈 RECOMMENDED EXPANSION: 80 → 120 concepts")
            print("   Focus Areas:")
            print("      • UCC Article 2 specific rules")
            print("      • Battle of the forms (2-207)")
            print("      • Warranties (express, implied, disclaimers)")
            print("      • Conditions vs. promises distinctions")
            print("      • Third-party beneficiary variations")
            print("      • Assignment and delegation scenarios")

        elif subject == 'secured_transactions':
            print("   📈 RECOMMENDED EXPANSION: 55 → 85 concepts")
            print("   Focus Areas:")
            print("      • Perfection methods by collateral type")
            print("      • Priority rules (PMSI, buyers, lien creditors)")
            print("      • Proceeds and after-acquired property")
            print("      • Default and remedies")
            print("      • Consumer goods special rules")

        print()

    print("\n" + "="*80)
    print("💡 STRATEGIC RECOMMENDATIONS")
    print("="*80 + "\n")

    print("OPTION A: Focus on MBE High-Impact Subjects")
    print("   Expand: Evidence, Civil Procedure, Constitutional Law")
    print("   Benefit: Maximum MBE score improvement")
    print("   Time: 3-4 weeks to add 150 concepts\n")

    print("OPTION B: Focus on Hardest Subjects")
    print("   Expand: Evidence, Real Property, Civil Procedure")
    print("   Benefit: Conquer the most complex material")
    print("   Time: 4-5 weeks to add 180 concepts\n")

    print("OPTION C: Balanced Expansion")
    print("   Expand: All subjects by 30-40% (849 → 1200 concepts)")
    print("   Benefit: Comprehensive coverage across all areas")
    print("   Time: 6-8 weeks to add 350 concepts\n")

    print("OPTION D: Deep Dive Single Subject")
    print("   Pick ONE subject and create exhaustive coverage")
    print("   Example: Evidence 70 → 200 concepts (everything tested)")
    print("   Benefit: Total mastery of one subject")
    print("   Time: 2-3 weeks for single subject\n")


def get_expansion_details(subject):
    """Get detailed expansion plan for subject"""

    expansions = {
        'evidence': {
            'current': 70,
            'target': 120,
            'new_concepts': 50,
            'breakdown': {
                'Hearsay Exceptions': 15,
                'Character Evidence': 8,
                'Expert Testimony': 6,
                'Privileges': 7,
                'Impeachment': 6,
                'Authentication': 4,
                'Best Evidence Rule': 4
            },
            'sample_concepts': [
                "Present Sense Impression Exception",
                "Excited Utterance vs. Present Sense",
                "State of Mind Exception (803(3))",
                "Business Records Foundation",
                "Public Records Exception",
                "Former Testimony Requirements",
                "Dying Declaration Elements",
                "Statement Against Interest vs. Party Admission",
                "Forfeiture by Wrongdoing",
                "Residual Exception (807)",
                "Character Evidence in Criminal Cases (Defendant)",
                "Character Evidence in Criminal Cases (Victim)",
                "Prior Bad Acts (404(b))",
                "Habit Evidence (406)",
                "Daubert Standard for Expert Testimony",
                "Frye Standard vs. Daubert",
                "Expert Opinion Based on Inadmissible Evidence",
                "Attorney-Client Privilege Elements",
                "Crime-Fraud Exception",
                "Spousal Privilege vs. Spousal Testimony"
            ]
        },
        'civil_procedure': {
            'current': 60,
            'target': 100,
            'new_concepts': 40,
            'breakdown': {
                'Personal Jurisdiction': 10,
                'Subject Matter Jurisdiction': 8,
                'Erie Doctrine': 6,
                'Pleadings': 5,
                'Discovery': 6,
                'Summary Judgment': 5
            },
            'sample_concepts': [
                "Specific Jurisdiction Requirements",
                "General Jurisdiction (Daimler Standard)",
                "Internet Jurisdiction (Zippo Sliding Scale)",
                "Stream of Commerce (Asahi/McIntyre)",
                "Federal Question Jurisdiction (Arising Under)",
                "Diversity: Complete Diversity Rule",
                "Amount in Controversy Calculation",
                "Supplemental Jurisdiction (§1367)",
                "Supplemental Jurisdiction Limits (§1367(b))",
                "Removal Jurisdiction",
                "Erie: Substantive vs. Procedural",
                "Erie: Federal Rules Analysis",
                "Erie: Unguided Erie Choice",
                "Hanna Two-Step Analysis",
                "Rule 12(b)(6) Plausibility Standard",
                "Twiqbal Pleading"
            ]
        },
        'real_property': {
            'current': 85,
            'target': 130,
            'new_concepts': 45,
            'breakdown': {
                'Future Interests': 15,
                'Rule Against Perpetuities': 5,
                'Easements': 8,
                'Covenants': 6,
                'Adverse Possession': 5,
                'Recording Acts': 6
            }
        }
    }

    return expansions.get(subject, {})


def main():
    analysis = analyze_subjects()
    print_recommendations(analysis)

    print("\n" + "="*80)
    print("🎯 NEXT STEPS")
    print("="*80 + "\n")
    print("Tell me which expansion you want:")
    print()
    print("  1. Evidence (70 → 120 concepts)")
    print("  2. Civil Procedure (60 → 100 concepts)")
    print("  3. Real Property (85 → 130 concepts)")
    print("  4. Constitutional Law (70 → 110 concepts)")
    print("  5. Contracts (80 → 120 concepts)")
    print("  6. Another subject (specify)")
    print("  7. Balanced expansion across all subjects")
    print()
    print("I'll generate detailed, exam-focused concepts with full teaching content.")
    print()


if __name__ == '__main__':
    main()

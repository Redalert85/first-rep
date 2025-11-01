#!/usr/bin/env python3
"""
Add final 3 concepts to reach exactly 331
Adding to Professional Responsibility (highest bar exam frequency)
"""

from pathlib import Path
import json

print("="*70)
print("FINAL TOUCHUP - ADDING 3 CRITICAL CONCEPTS")
print("Current: 328 → Target: 331")
print("="*70)

# Load Phase 1
with open("essay_expansion_phase1.json") as f:
    phase1 = json.load(f)

print(f"\n📖 Phase 1 currently has: {len(phase1)} concepts")

# Add 3 high-value Professional Responsibility concepts
additional_concepts = [
    {
        "concept_id": "prof_resp_client_trust_account",
        "name": "Client Trust Accounts (IOLTA)",
        "subject": "professional_responsibility",
        "category": "ESSAY",
        "difficulty": 3,
        "rule_statement": "Lawyer must maintain client funds in separate interest-bearing trust account; interest goes to state IOLTA program; strict record-keeping required; no commingling",
        "elements": ["Separate IOLTA account", "Interest to bar foundation", "Detailed records", "No commingling", "Prompt deposit"],
        "exceptions": [],
        "policy_rationales": ["Protect client funds", "Fund legal services for poor", "Prevent misappropriation"],
        "common_traps": ["Cannot use for operating expenses", "Strict accounting required", "Interest belongs to bar program not client"],
        "mnemonic": None,
        "prerequisites": [],
        "exam_frequency": "high",
        "iowa_specific": True
    },
    {
        "concept_id": "prof_resp_screening_procedures",
        "name": "Screening Procedures for Conflicts",
        "subject": "professional_responsibility",
        "category": "ESSAY",
        "difficulty": 4,
        "rule_statement": "Timely screening can cure certain conflicts: former client matters with proper procedures, former government lawyers, former judges; requires timely implementation, written notice to affected parties, and certification of compliance",
        "elements": ["Timely implementation", "Written notice to clients", "No confidential info shared", "Certification of compliance"],
        "exceptions": [],
        "policy_rationales": ["Allow lawyer mobility", "Protect client confidences", "Balance interests"],
        "common_traps": ["Cannot cure current client conflicts", "Timing is critical - must be prompt", "Documentation essential", "Former judge screening different from former government"],
        "mnemonic": "SCREEN: Separate lawyer, Certification, Records of compliance, Ethics wall, Ensure no info shared, Notice to affected parties",
        "prerequisites": [],
        "exam_frequency": "medium",
        "iowa_specific": False
    },
    {
        "concept_id": "prof_resp_lawyers_as_witnesses",
        "name": "Lawyer as Witness Rule",
        "subject": "professional_responsibility",
        "category": "ESSAY",
        "difficulty": 3,
        "rule_statement": "Lawyer shall not act as advocate in trial where lawyer likely to be necessary witness unless: testimony on uncontested matter, testimony on legal services and fees, or disqualification would cause substantial hardship to client",
        "elements": ["Advocate-witness prohibition", "Necessary witness test", "Three exceptions", "Imputation rules differ"],
        "exceptions": ["Uncontested matter", "Nature and value of legal services", "Substantial hardship to client"],
        "policy_rationales": ["Avoid jury confusion", "Prevent credibility issues", "Separate advocate and witness roles"],
        "common_traps": ["Three narrow exceptions only", "Likely to be necessary test", "Imputation does NOT apply unless personal interest conflict", "Other firm lawyers can continue"],
        "mnemonic": "UFS: Uncontested, Fees/services, Substantial hardship (exceptions)",
        "prerequisites": [],
        "exam_frequency": "medium",
        "iowa_specific": False
    }
]

print("\n✨ Adding 3 high-value concepts:")
for i, concept in enumerate(additional_concepts, 1):
    print(f"  {i}. {concept['name']}")
    print(f"     - Rule: {concept['rule_statement'][:80]}...")
    print(f"     - Frequency: {concept['exam_frequency']}")

# Append to phase 1
phase1.extend(additional_concepts)
print(f"\n📊 Updated Phase 1 to: {len(phase1)} concepts")

# Save updated phase 1
with open("essay_expansion_phase1.json", 'w') as f:
    json.dump(phase1, f, indent=2)
print("✓ Saved updated essay_expansion_phase1.json")

print("\n" + "="*70)
print("✅ FINAL 3 CONCEPTS ADDED!")
print("="*70)
print("\n🚀 Next steps:")
print("  1. Re-integrate: python3 integrate_all_complete.py")
print("  2. Verify: python3 verify_331.py")


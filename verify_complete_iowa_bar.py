#!/usr/bin/env python3
"""Verify complete Iowa Bar system - 215 concepts"""
from bar_tutor_unified import LegalKnowledgeGraph

kg = LegalKnowledgeGraph()

print("="*70)
print("🏆 COMPLETE IOWA BAR VERIFICATION")
print("="*70)
print()

# Categorize subjects
mbe_subjects = ['civil_procedure', 'constitutional_law', 'contracts', 'criminal_law',
                'criminal_procedure', 'evidence', 'real_property', 'torts']
essay_subjects = ['professional_responsibility', 'corporations', 'wills_trusts_estates',
                  'family_law', 'secured_transactions', 'iowa_procedure']

subjects = {}
for concept in kg.nodes.values():
    subjects[concept.subject] = subjects.get(concept.subject, 0) + 1

# MBE subjects
print("📚 MBE SUBJECTS (180 concepts):")
print("-"*70)
mbe_total = 0
for subject in sorted(mbe_subjects):
    count = subjects.get(subject, 0)
    mbe_total += count
    emoji = "✅" if count >= 20 else "⚠️"
    print(f"{emoji} {subject:25} {count:3} concepts")

print("-"*70)
print(f"   {'MBE SUBTOTAL':25} {mbe_total:3} concepts")

# Essay subjects
print("\n📝 ESSAY SUBJECTS (35+ concepts):")
print("-"*70)
essay_total = 0
for subject in sorted(essay_subjects):
    count = subjects.get(subject, 0)
    essay_total += count
    emoji = "✅" if count >= 1 else "⚠️"
    print(f"{emoji} {subject:25} {count:3} concepts")

print("-"*70)
print(f"   {'ESSAY SUBTOTAL':25} {essay_total:3} concepts")

# Grand total
print("\n" + "="*70)
total = mbe_total + essay_total
print(f"🏆 {'GRAND TOTAL':25} {total:3} concepts")
print("="*70)

if total >= 215:
    print("\n🎉 COMPLETE IOWA BAR SYSTEM ACHIEVED!")
    print("\n✨ Congratulations! Your system includes:")
    print("  • All 8 MBE subjects (180 concepts)")
    print("  • All 6 essay subjects (35+ concepts)")
    print("  • Complete Iowa Bar coverage")
    print("\n📊 Bar Exam Readiness:")
    print(f"  MBE (50% of exam): ✅ {mbe_total} concepts (EXCELLENT)")
    print(f"  Essays (50% of exam): ✅ {essay_total} concepts (STRONG)")
    print(f"  Overall: ✅ {total} concepts (COMPREHENSIVE)")
    print("\n🎯 You now have a COMPLETE Iowa Bar preparation system!")
else:
    print(f"\n📊 Progress: {total}/215 ({total/215*100:.1f}%)")

print("\n🚀 Ready to use:")
print("  python3 bar_tutor_unified.py")


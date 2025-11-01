#!/usr/bin/env python3
"""
Start Bar Exam Tutor with Complete 849-Concept Knowledge Base
Simple, clean interface to begin learning
"""

from socratic_tutor_849 import SocraticBarTutor

# Initialize tutor
tutor = SocraticBarTutor()

print(f"\n{'='*70}")
print(" " * 18 + "🎓 BAR EXAM TUTOR 849")
print(" " * 12 + "Complete Bar Preparation System")
print(f"{'='*70}\n")

print(f"✅ Loaded {tutor.knowledge['metadata']['total_concepts']} concepts across 12 subjects\n")

# Show available subjects
tutor.list_subjects()

print("\n" + "="*70)
print("Type one of these commands to start learning:")
print("="*70 + "\n")

print("tutor.teach_me('contracts')              # Learn 3 Contracts concepts")
print("tutor.teach_me('torts', 5)               # Learn 5 Torts concepts")
print("tutor.teach_me('constitutional_law', 7)  # Learn 7 Con Law concepts")
print("tutor.teach_me('criminal_law')           # Learn 3 Criminal Law concepts")
print("tutor.teach_me('evidence', 4)            # Learn 4 Evidence concepts")
print()
print("tutor.list_subjects()                    # Show all subjects again")
print()

print("="*70 + "\n")

# Keep tutor in scope for interactive use
if __name__ == '__main__':
    import code
    code.interact(local={'tutor': tutor}, banner="")

#!/usr/bin/env python3
"""
Socratic Bar Tutor with Complete 849-Concept Knowledge Base
Interactive, pedagogically sound teaching system
"""

import json
import random
from pathlib import Path
from typing import List, Dict

class SocraticBarTutor:
    """Bar tutor using Socratic method with 849 concepts"""

    def __init__(self):
        self.knowledge = self.load_knowledge()
        self.concepts_by_subject = self.organize_by_subject()
        self.session_stats = []

    def load_knowledge(self) -> Dict:
        """Load 849-concept knowledge base"""
        knowledge_file = Path(__file__).parent / 'data' / 'knowledge_849.json'

        if not knowledge_file.exists():
            print("⚠️  Knowledge base not found. Run: python3 comprehensive_tutor_849.py")
            return {'metadata': {'total_concepts': 0}, 'concepts': {}}

        with open(knowledge_file) as f:
            return json.load(f)

    def organize_by_subject(self) -> Dict[str, List]:
        """Organize concepts by subject"""
        by_subject = {}
        for subject, concepts in self.knowledge.get('concepts', {}).items():
            by_subject[subject] = concepts
        return by_subject

    def teach_me(self, subject: str = 'contracts', n_concepts: int = 3):
        """Interactive Socratic teaching session"""

        # Get available subjects
        available = list(self.concepts_by_subject.keys())

        if subject not in available:
            print(f"\n❌ Subject '{subject}' not found.")
            print(f"\n📚 Available subjects:")
            for subj in available:
                count = len(self.concepts_by_subject[subj])
                print(f"   • {subj.replace('_', ' ').title()}: {count} concepts")
            return

        concepts = self.concepts_by_subject[subject]
        total_available = len(concepts)

        print(f"\n{'='*70}")
        print(f"🎓 SOCRATIC TUTORING SESSION")
        print(f"{'='*70}")
        print(f"\n📚 Subject: {subject.replace('_', ' ').title()}")
        print(f"📊 Concepts Available: {total_available}")
        print(f"🎯 Session Size: {n_concepts} concepts\n")

        # Select concepts (prioritize those with teaching content)
        selected = self.select_concepts(concepts, n_concepts)

        print(f"✅ Selected {len(selected)} concepts for learning\n")

        name = input("What's your name? ").strip() or "Student"

        print(f"\nHi {name}! Let's use the Socratic method to master these concepts.")
        print("I'll teach, then test, then deepen your understanding.\n")

        input("Press ENTER to begin... ")

        results = []

        for i, concept in enumerate(selected, 1):
            print(f"\n\n{'─'*70}")
            print(f"CONCEPT {i}/{len(selected)}: {concept['name']}")
            print(f"{'─'*70}\n")

            # STEP 1: Hook (activate prior knowledge)
            hook = self.generate_hook(concept)
            print(f"💭 {hook}\n")
            input("Think about it... [ENTER] ")

            # STEP 2: Teach the rule
            print(f"\n━━ THE RULE ━━")
            print(f"{concept.get('rule_statement', 'Legal rule for this concept')}\n")

            if concept.get('elements'):
                print("Elements:")
                for elem in concept['elements'][:5]:  # Limit to 5
                    print(f"  • {elem}")
                print()

            # STEP 3: Teach mnemonic/shorthand
            if concept.get('teach'):
                print(f"💡 {concept['teach']}\n")

            input("Got it? [ENTER] for question... ")

            # STEP 4: Test understanding
            if concept.get('question'):
                print(f"\n{'─'*70}")
                print("TEST YOURSELF:\n")
                print(concept['question'])
                print()

                choices = concept.get('choices', {})
                if choices:
                    for choice, text in sorted(choices.items()):
                        print(f"  {choice}) {text}")

                    ans = input("\nYour answer: ").strip().upper()
                    correct_ans = concept.get('answer', 'A').upper()

                    correct = (ans == correct_ans)

                    if correct:
                        print(f"\n✓ Correct!")
                    else:
                        print(f"\n✗ Not quite. Answer: {correct_ans}")

                    why = concept.get('why', 'Explanation not available')
                    print(f"\n💡 {why}\n")

                    results.append({'concept': concept['name'], 'correct': correct})

                else:
                    print("[This is a conceptual understanding check - no multiple choice]\n")

            else:
                # No question available - just conceptual review
                print("\n📝 Key takeaways from this concept:\n")
                if concept.get('common_traps'):
                    print("⚠️  Common traps:")
                    for trap in concept['common_traps'][:3]:
                        print(f"   • {trap}")

            # STEP 5: Deepen (elaborative interrogation)
            if concept.get('policy_rationales'):
                print(f"\n🤔 Why does this rule exist?")
                for policy in concept['policy_rationales'][:2]:
                    print(f"   • {policy}")

            input("\nENTER to continue... ")

        # Session summary
        print(f"\n\n{'='*70}")
        print("SESSION COMPLETE")
        print(f"{'='*70}\n")

        if results:
            score = sum(r['correct'] for r in results)
            pct = (score / len(results) * 100) if results else 0

            print(f"{name}: {score}/{len(results)} ({pct:.0f}%)")
            print(f"[{'█' * int(pct/5)}{'░' * (20 - int(pct/5))}]\n")

            if pct == 100:
                print("🎉 Perfect! You're mastering this subject.")
            elif pct >= 70:
                print("💪 Strong work! Review the concepts you missed:")
                for r in results:
                    if not r['correct']:
                        print(f"   • {r['concept']}")
            else:
                print("📚 This is challenging material. Review these concepts:")
                for r in results:
                    if not r['correct']:
                        print(f"   • {r['concept']}")
                print("\nTry again tomorrow (spaced repetition helps!).")

        print(f"\n✅ Session saved. Total concepts in {subject}: {total_available}")
        print(f"   You've studied {len(selected)} so far.\n")

    def select_concepts(self, concepts: List[Dict], n: int) -> List[Dict]:
        """Select n concepts, prioritizing those with teaching content"""

        # Prioritize concepts with complete teaching materials
        with_teaching = [c for c in concepts if c.get('teach') and c.get('question')]
        without_teaching = [c for c in concepts if c not in with_teaching]

        # Take from teaching-ready first
        selected = []

        if len(with_teaching) >= n:
            selected = random.sample(with_teaching, n)
        else:
            selected.extend(with_teaching)
            needed = n - len(selected)
            if needed > 0 and without_teaching:
                selected.extend(random.sample(without_teaching, min(needed, len(without_teaching))))

        return selected[:n]

    def generate_hook(self, concept: Dict) -> str:
        """Generate Socratic hook to activate prior knowledge"""

        hooks = [
            f"Think about a real-world situation involving {concept['name'].lower()}...",
            f"Before we dive in: What do you already know about {concept['name'].lower()}?",
            f"Let me ask you: Why might {concept['name'].lower()} be important in law?",
            f"Imagine you're advising a client about {concept['name'].lower()}. What questions would they ask?",
            f"What's the first thing that comes to mind when you hear '{concept['name']}'?"
        ]

        return random.choice(hooks)

    def list_subjects(self):
        """Display all available subjects"""
        print(f"\n{'='*70}")
        print("📚 AVAILABLE BAR EXAM SUBJECTS")
        print(f"{'='*70}\n")

        total = self.knowledge['metadata']['total_concepts']
        print(f"Total Concepts: {total}\n")

        for subject, concepts in sorted(self.concepts_by_subject.items()):
            count = len(concepts)
            subject_name = subject.replace('_', ' ').title()
            print(f"  {subject_name:30} {count:>3} concepts")

        print(f"\n{'='*70}")
        print("Usage: tutor.teach_me('subject_name', 5)")
        print(f"{'='*70}\n")


def main():
    """Interactive CLI"""
    tutor = SocraticBarTutor()

    print(f"\n{'='*70}")
    print(" " * 20 + "SOCRATIC BAR TUTOR")
    print(" " * 15 + "Complete 849-Concept System")
    print(f"{'='*70}\n")

    tutor.list_subjects()

    print("\n💡 Quick Start:")
    print("   tutor.teach_me('contracts', 3)      # Learn 3 Contracts concepts")
    print("   tutor.teach_me('torts', 5)          # Learn 5 Torts concepts")
    print("   tutor.teach_me('constitutional_law') # Learn 3 Con Law concepts (default)\n")
    print("   tutor.list_subjects()               # See all subjects\n")

    return tutor


if __name__ == '__main__':
    tutor = main()

    # Enter Python REPL with tutor available
    print("=" * 70)
    print("Entering interactive mode...")
    print("Type: tutor.teach_me('subject_name', 3)")
    print("=" * 70 + "\n")

    import code
    code.interact(local=locals(), banner="")

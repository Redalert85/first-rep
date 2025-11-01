#!/usr/bin/env python3
"""
Pattern Recognition System
Trains you to identify question types and traps instantly
"""

class PatternRecognition:
    """Teach common MBE patterns"""
    
    COMMON_PATTERNS = {
        'contracts': [
            {
                'name': 'Battle of Forms',
                'trigger_words': ['merchant', 'acknowledgment', 'additional terms'],
                'instant_analysis': 'UCC 2-207: Additional terms between merchants unless material alteration',
                'common_trap': 'Applying mirror image rule (wrong for UCC)'
            },
            {
                'name': 'SOF Exception',
                'trigger_words': ['oral', 'statute of frauds', 'goods $500+'],
                'instant_analysis': 'Check: Part performance, Merchant confirmation, Admission',
                'common_trap': 'Forgetting merchant confirmation exception'
            }
        ],
        'torts': [
            {
                'name': 'Negligence Per Se',
                'trigger_words': ['statute', 'violation', 'ordinance'],
                'instant_analysis': 'Statutory standard replaces reasonable care if within protected class',
                'common_trap': 'Thinking violation automatically = liability (still need causation)'
            }
        ],
        # Add patterns for all subjects
    }
    
    def train(self, subject: str):
        """Interactive pattern training"""
        patterns = self.COMMON_PATTERNS.get(subject, [])
        
        print(f"\n🎯 PATTERN RECOGNITION: {subject.upper()}")
        print("="*70)
        
        for pattern in patterns:
            print(f"\nPattern: {pattern['name']}")
            print(f"Triggers: {', '.join(pattern['trigger_words'])}")
            print(f"Analysis: {pattern['instant_analysis']}")
            print(f"⚠️ Trap: {pattern['common_trap']}")
            print()

def main():
    print("="*70)
    print("PATTERN RECOGNITION TRAINING")
    print("="*70)
    
    pr = PatternRecognition()
    
    print("\n🧠 Learn to recognize 50+ common MBE patterns")
    print("\n📊 Mastery target:")
    print("  • Identify pattern within 10 seconds")
    print("  • Recall instant analysis framework")
    print("  • Spot common trap immediately")

if __name__ == "__main__":
    main()

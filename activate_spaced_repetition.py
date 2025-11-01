#!/usr/bin/env python3
"""
Activate spaced repetition for your 180 concepts
Uses SuperMemo SM-2 algorithm for optimal retention
"""

from datetime import datetime, timedelta
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class SpacedRepetitionCard:
    """Flashcard with SM-2 algorithm"""
    concept_id: str
    front: str
    back: str
    
    # SM-2 algorithm fields
    ease_factor: float = 2.5
    interval: int = 1  # days
    repetitions: int = 0
    next_review: str = ""
    
    def __post_init__(self):
        if not self.next_review:
            self.next_review = datetime.now().isoformat()
    
    def review(self, quality: int):
        """
        Update card based on review quality (0-5)
        0-2: Fail, 3-5: Pass
        """
        if quality < 3:
            # Failed - reset
            self.repetitions = 0
            self.interval = 1
        else:
            # Passed - calculate new interval
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
            
            self.repetitions += 1
            
            # Update ease factor
            self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        
        # Set next review date
        next_date = datetime.now() + timedelta(days=self.interval)
        self.next_review = next_date.isoformat()

class SpacedRepetitionSystem:
    """Complete SRS for 180 concepts"""
    
    def __init__(self):
        self.cards: list[SpacedRepetitionCard] = []
        self.generate_cards_from_concepts()
    
    def generate_cards_from_concepts(self):
        """Generate flashcards from your 180 concepts"""
        from bar_tutor_unified import LegalKnowledgeGraph
        
        kg = LegalKnowledgeGraph()
        
        for concept_id, concept in kg.nodes.items():
            # Create multiple cards per concept
            
            # 1. Rule statement card
            self.cards.append(SpacedRepetitionCard(
                concept_id=f"{concept_id}_rule",
                front=f"State the rule for: {concept.name}",
                back=concept.rule_statement
            ))
            
            # 2. Elements card
            if concept.elements:
                self.cards.append(SpacedRepetitionCard(
                    concept_id=f"{concept_id}_elements",
                    front=f"What are the elements of {concept.name}?",
                    back="\n".join(f"{i}. {elem}" for i, elem in enumerate(concept.elements, 1))
                ))
            
            # 3. Common traps card
            if concept.common_traps:
                self.cards.append(SpacedRepetitionCard(
                    concept_id=f"{concept_id}_traps",
                    front=f"What are common exam traps for {concept.name}?",
                    back="\n".join(f"⚠️ {trap}" for trap in concept.common_traps)
                ))
    
    def get_due_cards(self, limit: int = 20) -> list[SpacedRepetitionCard]:
        """Get cards due for review"""
        now = datetime.now()
        due = [
            card for card in self.cards
            if datetime.fromisoformat(card.next_review) <= now
        ]
        due.sort(key=lambda c: c.next_review)
        return due[:limit]
    
    def daily_review_session(self):
        """Interactive daily review"""
        due_cards = self.get_due_cards(20)
        
        if not due_cards:
            print("🎉 No cards due! You're all caught up!")
            return
        
        print(f"\n📚 Daily Review: {len(due_cards)} cards due\n")
        
        for i, card in enumerate(due_cards, 1):
            print(f"Card {i}/{len(due_cards)}")
            print(f"Q: {card.front}")
            input("Press Enter to reveal answer...")
            print(f"A: {card.back}\n")
            
            quality = int(input("Rate your recall (0-5): "))
            card.review(quality)
            print()
        
        print("✅ Review complete!")
    
    def generate_statistics(self):
        """Show retention statistics"""
        total = len(self.cards)
        reviewed = sum(1 for c in self.cards if c.repetitions > 0)
        mastered = sum(1 for c in self.cards if c.repetitions >= 5 and c.ease_factor >= 2.5)
        
        print("\n📊 SPACED REPETITION STATISTICS")
        print("="*70)
        print(f"Total Cards: {total}")
        print(f"Reviewed: {reviewed} ({reviewed/total*100:.1f}%)")
        print(f"Mastered: {mastered} ({mastered/total*100:.1f}%)")
        print(f"Due Today: {len(self.get_due_cards(999))}")

def main():
    print("="*70)
    print("SPACED REPETITION ACTIVATION")
    print("="*70)
    
    srs = SpacedRepetitionSystem()
    
    print(f"\n✅ Generated {len(srs.cards)} flashcards from 180 concepts")
    print("\n📚 Card types:")
    print("  • Rule statements")
    print("  • Elements")
    print("  • Common traps")
    
    srs.generate_statistics()
    
    print("\n🎯 To reach 100% retention:")
    print("  • Review 20-30 cards daily")
    print("  • Maintain 90%+ accuracy")
    print("  • Complete 3-4 review cycles")
    print("  • Target: 30-45 days")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from bar_tutor_unified import BarExamTutor, LegalKnowledgeGraph, InterleavedPracticeEngine

def test_knowledge_graph():
    print("Testing Knowledge Graph...")
    kg = LegalKnowledgeGraph()
    contracts = kg.get_subject_concepts("contracts")
    print(f"  Contracts: {len(contracts)} concepts")
    assert len(contracts) > 0
    print("  ✓ Working\n")

def test_interleaved():
    print("Testing Interleaved Practice...")
    kg = LegalKnowledgeGraph()
    engine = InterleavedPracticeEngine(kg)
    concepts = engine.generate_practice("contracts", 3)
    concept_ids = [c.concept_id for c in concepts]
    unique = set(concept_ids)
    print(f"  Generated: {len(concepts)}")
    print(f"  Unique: {len(unique)}")
    assert len(concepts) == len(unique), "Duplicates!"
    print("  ✓ No duplicates\n")

def test_tutor():
    print("Testing Tutor...")
    tutor = BarExamTutor()
    assert tutor.kg is not None
    print("  ✓ Initialized\n")

if __name__ == "__main__":
    print("="*50)
    print("RUNNING TESTS")
    print("="*50 + "\n")
    try:
        test_knowledge_graph()
        test_interleaved()
        test_tutor()
        print("="*50)
        print("ALL TESTS PASSED ✓")
        print("="*50)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
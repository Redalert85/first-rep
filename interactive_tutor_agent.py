#!/usr/bin/env python3
"""
Test suite for the unified bar exam tutor
Run this to verify everything works correctly
"""

from bar_tutor_unified import BarExamTutor, LegalKnowledgeGraph, InterleavedPracticeEngine

def test_knowledge_graph():
    """Test knowledge graph initialization"""
    print("Testing Knowledge Graph...")
    kg = LegalKnowledgeGraph()
    
    # Check contracts concepts
    contracts = kg.get_subject_concepts("contracts")
    print(f"  Contracts concepts: {len(contracts)}")
    assert len(contracts) > 0, "No contracts concepts found"
    
    # Check torts concepts
    torts = kg.get_subject_concepts("torts")
    print(f"  Torts concepts: {len(torts)}")
    assert len(torts) > 0, "No torts concepts found"
    
    # Check specific concept
    consideration = kg.get_concept("contracts_consideration")
    assert consideration is not None, "Consideration concept not found"
    print(f"  Found concept: {consideration.name}")
    
    print("  ✓ Knowledge graph working\n")

def test_interleaved_practice():
    """Test interleaved practice engine"""
    print("Testing Interleaved Practice...")
    kg = LegalKnowledgeGraph()
    engine = InterleavedPracticeEngine(kg)
    
    # Generate practice concepts
    concepts = engine.generate_practice("contracts", 3)
    print(f"  Generated {len(concepts)} concepts")
    
    # Check for duplicates
    concept_ids = [c.concept_id for c in concepts]
    unique_ids = set(concept_ids)
    assert len(concept_ids) == len(unique_ids), "Duplicate concepts found!"
    
    print(f"  Unique concepts: {len(unique_ids)}")
    print("  ✓ No duplicates - deduplication working\n")

def test_full_tutor():
    """Test full tutor initialization"""
    print("Testing Full Tutor...")
    tutor = BarExamTutor()
    
    assert tutor.kg is not None, "Knowledge graph not initialized"
    assert tutor.practice_engine is not None, "Practice engine not initialized"
    assert tutor.tracker is not None, "Tracker not initialized"
    assert tutor.interactive is not None, "Interactive mode not initialized"
    
    print("  ✓ All components initialized\n")

def test_interactive_mode():
    """Test interactive tutor"""
    print("Testing Interactive Mode...")
    tutor = BarExamTutor()
    
    # Start session
    welcome = tutor.interactive.start_session("contracts")
    assert "contracts" in welcome.lower(), "Subject not in welcome message"
    
    # Test help command
    help_text = tutor.interactive.process_input("help")
    assert "commands" in help_text.lower(), "Help not working"
    
    # Test explain
    explain = tutor.interactive.process_input("explain consideration")
    assert "consideration" in explain.lower() or "concept" in explain.lower(), "Explain not working"
    
    print("  ✓ Interactive mode working\n")

def run_all_tests():
    """Run all tests"""
    print("="*70)
    print("RUNNING UNIFIED BAR TUTOR TESTS")
    print("="*70 + "\n")
    
    try:
        test_knowledge_graph()
        test_interleaved_practice()
        test_full_tutor()
        test_interactive_mode()
        
        print("="*70)
        print("ALL TESTS PASSED ✓")
        print("="*70)
        print("\nThe unified tutor is working correctly!")
        print("Run: python bar_tutor_unified.py")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
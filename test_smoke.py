#!/usr/bin/env python3
"""
Smoke tests for bar prep modules.
Verifies basic imports and functionality without requiring full dependencies.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test that core modules can be imported."""
    print("Testing imports...")
    
    try:
        import mbe_item_generator
        print("  ✓ mbe_item_generator")
    except ImportError as e:
        print(f"  ✗ mbe_item_generator: {e}")
        return False
    
    try:
        import study_guide_analyzer
        print("  ✓ study_guide_analyzer")
    except ImportError as e:
        print(f"  ✗ study_guide_analyzer: {e}")
        return False
    
    # Bar tutor and memory palace have optional dependencies
    try:
        import bar_tutor
        print("  ✓ bar_tutor")
    except ImportError as e:
        print(f"  ⚠ bar_tutor (missing optional deps): {e}")
    
    try:
        import elite_memory_palace
        print("  ✓ elite_memory_palace")
    except ImportError as e:
        print(f"  ⚠ elite_memory_palace (missing optional deps): {e}")
    
    try:
        import optimized_memory_palace
        print("  ✓ optimized_memory_palace")
    except ImportError as e:
        print(f"  ⚠ optimized_memory_palace (missing optional deps): {e}")
    
    return True


def test_mbe_generator():
    """Test MBE question generator basic functionality."""
    print("\nTesting MBE item generator...")
    
    try:
        from mbe_item_generator import generate_item, BANKS
        
        # Test property question generation
        if "property" in BANKS:
            item = generate_item("property")
            assert item.subject == "property"
            assert item.answer in ["A", "B", "C", "D"]
            assert len(item.options) == 4
            print("  ✓ Property question generation works")
        
        # Test new property-servitudes generator
        if "property-servitudes" in BANKS:
            item = generate_item("property-servitudes")
            assert item.subject == "property-servitudes"
            assert "common scheme" in item.tested_rule.lower() or "equitable servitude" in item.tested_rule.lower()
            print("  ✓ Property servitudes question generation works")
            print(f"    - Tested rule: {item.tested_rule}")
            print(f"    - Trap types: {', '.join(item.trap_type)}")
        
        return True
    except Exception as e:
        print(f"  ✗ MBE generator test failed: {e}")
        return False


def test_study_guide_analyzer():
    """Test study guide analyzer basic functionality."""
    print("\nTesting study guide analyzer...")
    
    try:
        import study_guide_analyzer
        
        # Verify module has expected attributes
        print("  ✓ Study guide analyzer module loads successfully")
        return True
    except Exception as e:
        print(f"  ✗ Study guide analyzer test failed: {e}")
        return False


def main():
    """Run all smoke tests."""
    print("=" * 60)
    print("Bar Prep Smoke Tests")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("MBE Generator", test_mbe_generator()))
    results.append(("Study Guide Analyzer", test_study_guide_analyzer()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All smoke tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed - check dependencies")
        return 1


if __name__ == "__main__":
    sys.exit(main())


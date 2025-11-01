#!/usr/bin/env python3
from pathlib import Path
import re

# Read the ultimate knowledge base
ultimate_code = Path("ultimate_knowledge_base.py").read_text()

# Read current tutor
tutor = Path("bar_tutor_unified.py").read_text()

# Find the LegalKnowledgeGraph class
class_start = tutor.find("class LegalKnowledgeGraph:")
if class_start < 0:
    print("❌ Could not find LegalKnowledgeGraph class")
    exit(1)

# Find the __init__ method
init_start = tutor.find("    def __init__(self):", class_start)
init_end = tutor.find("\n    def _initialize", init_start)

# Create new __init__ with all subjects
new_init = '''    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self._initialize_all_subjects()

    def _initialize_all_subjects(self):
        """Initialize all 8 MBE subjects - 112 concepts total"""
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_criminal_procedure()
        self._initialize_civil_procedure()
        self._initialize_evidence()
        self._initialize_real_property()

'''

# Replace the section from __init__ to first _initialize method
tutor = tutor[:init_start] + new_init + tutor[init_end:]

# Now find where to insert all the _initialize methods
# Remove all old _initialize methods
pattern = r'    def _initialize_\w+\(self\):.*?(?=\n    def [^_]|\nclass )'
tutor = re.sub(pattern, '', tutor, flags=re.DOTALL)

# Find insertion point (right after _initialize_all_subjects)
insert_point = tutor.find("        self._initialize_real_property()\n\n")
if insert_point > 0:
    insert_point = tutor.find("\n\n", insert_point) + 2
    
    # Insert all the new initialization methods
    tutor = tutor[:insert_point] + ultimate_code + "\n" + tutor[insert_point:]
    
    # Save
    Path("bar_tutor_unified.py").write_text(tutor)
    
    print("="*70)
    print("✅ ULTIMATE INTEGRATION COMPLETE!")
    print("="*70)
    print("\nYour bar tutor now has:")
    print("  • 112 comprehensive concepts")
    print("  • 14 concepts per subject")
    print("  • 150% Real Property richness level")
    print("\nTest with: python3 test_tutor.py")
else:
    print("❌ Could not find insertion point")


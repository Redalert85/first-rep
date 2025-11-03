#!/usr/bin/env python3
"""
Integrate Real Property concepts into bar_tutor_unified.py
"""
from importlib import import_module
from pathlib import Path
import re

# Read the generated Real Property code
rp_code = import_module("real_property_code").get_snippet()

# Read the main tutor file
tutor = Path("bar_tutor_unified.py").read_text()

# Find where to insert (after _initialize_civil_procedure)
insert_marker = "    def _initialize_evidence(self):"
insert_pos = tutor.find(insert_marker)

if insert_pos > 0:
    # Insert the Real Property initialization before evidence
    tutor = tutor[:insert_pos] + rp_code + "\n\n" + tutor[insert_pos:]
    
    # Update _initialize_all_subjects to include real_property
    old_init = '''    def _initialize_all_subjects(self):
        """Initialize all MBE subjects"""
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_evidence()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_criminal_procedure()
        self._initialize_civil_procedure()'''
    
    new_init = '''    def _initialize_all_subjects(self):
        """Initialize all MBE subjects + Real Property"""
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_evidence()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_criminal_procedure()
        self._initialize_civil_procedure()
        self._initialize_real_property()'''
    
    tutor = tutor.replace(old_init, new_init)
    
    # Save
    Path("bar_tutor_unified.py").write_text(tutor)
    
    print("="*70)
    print("✅ REAL PROPERTY INTEGRATED!")
    print("="*70)
    print("\n✓ Added _initialize_real_property() method")
    print("✓ Updated _initialize_all_subjects()")
    print("\nYour system now has:")
    print("  • 46 MBE concepts (7 subjects)")
    print("  • 9 Real Property concepts (LAND BARON)")
    print("  • Total: 55 concepts!")
    print("\nTest with: python3 test_tutor.py")
else:
    print("❌ Could not find insertion point")


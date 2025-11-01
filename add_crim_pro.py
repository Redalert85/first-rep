#!/usr/bin/env python3
from pathlib import Path

# Read the file
content = Path("bar_tutor_unified.py").read_text()

# Find and replace the _initialize_all_subjects method
old_method = '''    def _initialize_all_subjects(self):
        """Initialize all MBE subjects"""
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_evidence()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_civil_procedure()'''

new_method = '''    def _initialize_all_subjects(self):
        """Initialize all MBE subjects"""
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_evidence()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_criminal_procedure()
        self._initialize_civil_procedure()'''

content = content.replace(old_method, new_method)

# Save
Path("bar_tutor_unified.py").write_text(content)
print("✓ Added criminal_procedure initialization")
print("\nTest again: python3 test_tutor.py")

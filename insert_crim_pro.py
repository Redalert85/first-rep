#!/usr/bin/env python3
from pathlib import Path
import re

# Read the file
content = Path("bar_tutor_unified.py").read_text()

# Read the expanded concepts to get the criminal_procedure method
expanded = Path("expanded_concepts.txt").read_text()

# Extract the criminal_procedure method
pattern = r'(    def _initialize_criminal_procedure\(self\):.*?)(?=\n    def |\n\n\n===)'
match = re.search(pattern, expanded, re.DOTALL)

if match:
    crim_pro_method = match.group(1).rstrip()
    
    # Find where to insert it (right before _initialize_civil_procedure)
    insert_point = content.find('    def _initialize_civil_procedure(self):')
    
    if insert_point > 0:
        # Insert the method
        content = content[:insert_point] + crim_pro_method + '\n\n' + content[insert_point:]
        
        # Save
        Path("bar_tutor_unified.py").write_text(content)
        print("✓ Inserted _initialize_criminal_procedure method")
        print("\nTest again: python3 test_tutor.py")
    else:
        print("❌ Could not find insertion point")
else:
    print("❌ Could not extract criminal_procedure method")

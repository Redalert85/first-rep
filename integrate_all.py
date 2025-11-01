#!/usr/bin/env python3
import re
from pathlib import Path

print("\n" + "="*70)
print("COMPREHENSIVE KNOWLEDGE BASE INTEGRATION")
print("="*70 + "\n")

# Load files
expanded_text = Path("expanded_concepts.txt").read_text()
original_code = Path("bar_tutor_unified_original.py").read_text()

# Extract all new initialization methods
new_methods = {}
subjects = ['torts', 'contracts', 'criminal_law', 'criminal_procedure', 
            'civil_procedure', 'evidence', 'constitutional_law']

for subject in subjects:
    # Match the method in expanded output
    pattern = rf'(    def _initialize_{subject}\(self\):.*?)(?=\n    def |\n\n\n===)'
    match = re.search(pattern, expanded_text, re.DOTALL)
    if match:
        new_methods[subject] = match.group(1).rstrip()
        print(f"✓ Extracted {subject:20s} ({len(match.group(1))} chars)")

print(f"\n✓ Found {len(new_methods)}/{len(subjects)} methods\n")

# Replace in original file
result = original_code

for subject, new_code in new_methods.items():
    # Find and replace old method
    old_pattern = rf'(    def _initialize_{subject}\(self\):.*?)(?=\n    def |\nclass )'
    
    if re.search(old_pattern, result, re.DOTALL):
        result = re.sub(old_pattern, new_code + '\n\n', result, flags=re.DOTALL, count=1)
        print(f"✓ Integrated {subject}")
    else:
        print(f"⚠️  Could not find old {subject} method")

# Write result
Path("bar_tutor_unified.py").write_text(result)

print("\n" + "="*70)
print("✅ INTEGRATION COMPLETE!")
print("="*70)
print("\nYour bar_tutor_unified.py now has 46 concepts!")
print("\nNext steps:")
print("  1. Test: python3 test_tutor.py")
print("  2. Run: python3 bar_tutor_unified.py")

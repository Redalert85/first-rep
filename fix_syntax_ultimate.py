#!/usr/bin/env python3
"""Fix syntax errors in the integrated file"""
from pathlib import Path

print("🔧 Fixing syntax errors...")

# Read the file
content = Path("bar_tutor_unified.py").read_text()

# Fix unterminated strings - these are from the original parsing
fixes = [
    ('"full faith and credit.\n\n#### Visuals"', '"full faith and credit"'),
    ('"work-product doctrine.\n\n#### Visuals"', '"work-product doctrine"'),
    ('"collateral source rule variations.\n\n#### Visuals"', '"collateral source rule variations"'),
    ('"confrontation Clause for testimonial hearsay.\n\n#### Visuals"', '"confrontation Clause for testimonial hearsay"'),
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"  ✓ Fixed: {new[:50]}...")

# Also fix any other unterminated strings ending with newlines
import re
# Find strings that end with .\n\n#### and close them properly
content = re.sub(r'(".*?)\n\n#### Visuals"', r'\1"', content)

# Save
Path("bar_tutor_unified.py").write_text(content)

print("\n✅ Syntax errors fixed!")
print("Test with: python3 test_tutor.py")

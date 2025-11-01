#!/usr/bin/env python3
from pathlib import Path

# Read the file
content = Path("bar_tutor_unified.py").read_text()

# Fix the broken string on line 397 (torts vicarious liability)
# The issue is an unterminated string in the traps list
content = content.replace(
    '"collateral source rule variations.\n\n#### Visuals"',
    '"collateral source rule variations"'
)

# Also fix evidence and civil procedure which have the same issue
content = content.replace(
    '"work-product doctrine.\n\n#### Visuals"',
    '"work-product doctrine"'
)

content = content.replace(
    '"full faith and credit.\n\n#### Visuals"',
    '"full faith and credit"'
)

# Save
Path("bar_tutor_unified.py").write_text(content)
print("✓ Fixed syntax errors")
print("\nTry again: python3 test_tutor.py")

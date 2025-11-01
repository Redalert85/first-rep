#!/usr/bin/env python3
"""
Expand Real Property from 14 to 25 concepts using your study guide
"""
from pathlib import Path
import re

print("="*70)
print("REAL PROPERTY EXPANSION")
print("Expanding from 14 → 25 concepts using your materials")
print("="*70)

# Parse real_property_study_guide.md
guide = Path("real_property_study_guide.md").read_text()

print("\n📖 Parsing real_property_study_guide.md...")

# Find major sections
sections = re.split(r'\n## (\d+\. .+?)\n', guide)

concepts_found = []
for i in range(1, len(sections), 2):
    if i+1 >= len(sections):
        break
    
    title = sections[i]
    content = sections[i+1]
    
    # Extract topic name
    topic_match = re.search(r'\d+\. (.+)', title)
    if topic_match:
        topic = topic_match.group(1).strip()
        concepts_found.append(topic)

print(f"✓ Found {len(concepts_found)} major topics:")
for i, concept in enumerate(concepts_found[:15], 1):
    print(f"  {i}. {concept}")

print(f"\nTotal concepts available: {len(concepts_found)}")
print("This could expand Real Property to 25+ concepts!")

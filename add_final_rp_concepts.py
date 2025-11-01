#!/usr/bin/env python3
"""Add 2 more Real Property concepts to reach 14"""
from pathlib import Path
import re

content = Path("bar_tutor_unified.py").read_text()

# Find the real_property initialization method
rp_start = content.find("    def _initialize_real_property(self):")
rp_end = content.find("\n    def _initialize", rp_start + 100)

# Add 2 more concepts
additional_concepts = '''            KnowledgeNode(
                concept_id="real_property_water_rights",
                name="Water Rights",
                subject="real_property",
                difficulty=3,
                rule_statement="Riparian rights attach to land bordering watercourse; prior appropriation follows first in time first in right",
                elements=['Riparian rights', 'Prior appropriation', 'Surface water', 'Groundwater'],
                policy_rationales=[],
                common_traps=[
                    "Mixing riparian and prior appropriation systems",
                    "Forgetting reasonable use doctrine",
                ],
            ),
            KnowledgeNode(
                concept_id="real_property_nuisance",
                name="Nuisance",
                subject="real_property",
                difficulty=3,
                rule_statement="Private nuisance is substantial unreasonable interference with use and enjoyment of land; public nuisance affects community",
                elements=['Private nuisance', 'Public nuisance', 'Coming to nuisance', 'Remedies'],
                policy_rationales=[],
                common_traps=[
                    "Confusing trespass and nuisance",
                    "Forgetting balancing test for unreasonableness",
                ],
            ),
'''

# Find where to insert (before the closing bracket)
insert_point = content.find("        ]\n        for node in concepts:\n            self.nodes[node.concept_id] = node", rp_start)

if insert_point > 0:
    content = content[:insert_point] + additional_concepts + content[insert_point:]
    Path("bar_tutor_unified.py").write_text(content)
    print("✅ Added 2 Real Property concepts!")
    print("Test with: python3 test_tutor.py")
else:
    print("❌ Could not find insertion point")

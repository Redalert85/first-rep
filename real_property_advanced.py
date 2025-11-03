"""Auto-generated snippet module.

This module is produced by tooling and exposes a helper to retrieve the raw
Python snippet needed when integrating expanded knowledge bases. Keeping the
snippet in a plain string avoids import-time syntax errors while still letting
integration scripts consume the data programmatically.
"""
from __future__ import annotations

_SNIPPET = "    def _initialize_real_property(self):\n        \"\"\"Initialize real property concepts with advanced features\"\"\"\n        concepts = [\n            KnowledgeNode(\n                concept_id=\"real_property_estates_and_future_interests\",\n                name=\"ESTATES & FUTURE INTERESTS\",\n                subject=\"real_property\",\n                difficulty=3,\n                rule_statement=\"Present possessory estates include fee simple absolute, defeasible fees, and life estates; future interests include reversions, remainders, and executory interests that must satisfy RAP.\",\n                elements=['Fee Simple Absolute', 'Life Estates', 'Defeasible Fees', 'Future Interests', 'Rule Against Perpetuities (RAP)'],\n                policy_rationales=[],\n                common_traps=[\n                    \"AUTO vs. MANUAL: Determinable = AUTOmatic (like autopilot); Condition Subsequent = MANUAL reentry (l\",\n                    \"REMAINDER RULE: Remainders are like train passengers - they wait for their turn, never jump ahead (n\",\n                    \"RAP TRAP: 21 years + lives in being = drinking age (21) + pregnancy (gestation)\",\n                ],\n                # Mnemonic (rhythmic): PREFUR\n            ),\n            KnowledgeNode(\n                concept_id=\"real_property_conveyancing_and_recording\",\n                name=\"CONVEYANCING & RECORDING\",\n                subject=\"real_property\",\n                difficulty=3,\n                rule_statement=\"Recording statutes protect bona fide purchasers; race-notice is majority rule, requiring timely recordation without notice of prior interests.\",\n                elements=['Deed Types', 'Marketable Title', 'Title Insurance', 'After-Acquired Title', 'Recording Acts'],\n                policy_rationales=[],\n                common_traps=[\n                    \"BFP = Good Faith Penny: Bona fide purchaser needs good faith + value (even $1) + no notice\",\n                    \"Chain Gang: Must examine entire chain of title, not just immediate grantor (like prison chain gang -\",\n                    \"Triple Notice Threat: Actual (you know) + Constructive (recorded) + Inquiry (should have known)\",\n                ],\n                # Mnemonic (rhythmic): RACE to the Courthouse\n            ),\n        ]\n        for node in concepts:\n            self.nodes[node.concept_id] = node\n"


def get_snippet() -> str:
    """Return the raw Python snippet for integration scripts."""
    return _SNIPPET


__all__ = ["get_snippet"]

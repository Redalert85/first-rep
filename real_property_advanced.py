    def _initialize_real_property(self):
        """Initialize real property concepts with advanced features"""
        concepts = [
            KnowledgeNode(
                concept_id="real_property_estates_and_future_interests",
                name="ESTATES & FUTURE INTERESTS",
                subject="real_property",
                difficulty=3,
                rule_statement="Present possessory estates include fee simple absolute, defeasible fees, and life estates; future interests include reversions, remainders, and executory interests that must satisfy RAP.",
                elements=['Fee Simple Absolute', 'Life Estates', 'Defeasible Fees', 'Future Interests', 'Rule Against Perpetuities (RAP)'],
                policy_rationales=[],
                common_traps=[
                    "AUTO vs. MANUAL: Determinable = AUTOmatic (like autopilot); Condition Subsequent = MANUAL reentry (l",
                    "REMAINDER RULE: Remainders are like train passengers - they wait for their turn, never jump ahead (n",
                    "RAP TRAP: 21 years + lives in being = drinking age (21) + pregnancy (gestation)",
                ],
                # Mnemonic (rhythmic): PREFUR
            ),
            KnowledgeNode(
                concept_id="real_property_conveyancing_and_recording",
                name="CONVEYANCING & RECORDING",
                subject="real_property",
                difficulty=3,
                rule_statement="Recording statutes protect bona fide purchasers; race-notice is majority rule, requiring timely recordation without notice of prior interests.",
                elements=['Deed Types', 'Marketable Title', 'Title Insurance', 'After-Acquired Title', 'Recording Acts'],
                policy_rationales=[],
                common_traps=[
                    "BFP = Good Faith Penny: Bona fide purchaser needs good faith + value (even $1) + no notice",
                    "Chain Gang: Must examine entire chain of title, not just immediate grantor (like prison chain gang -",
                    "Triple Notice Threat: Actual (you know) + Constructive (recorded) + Inquiry (should have known)",
                ],
                # Mnemonic (rhythmic): RACE to the Courthouse
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

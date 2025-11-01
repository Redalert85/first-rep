    def _initialize_real_property(self):
        """Initialize real property - LAND BARON framework (9 concepts)"""
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
                # 🏰 Mnemonic (rhythmic): PREFUR
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
                # 📜 Mnemonic (acronym): RACE to the Courthouse
            ),
            KnowledgeNode(
                concept_id="real_property_easements_servitudes_and_licenses",
                name="EASEMENTS, SERVITUDES & LICENSES",
                subject="real_property",
                difficulty=3,
                rule_statement="Easements create rights to use another's land; appurtenant easements run with land, in gross are personal; licenses are revocable permissions.",
                elements=['Appurtenant Easements', 'Easements in Gross', 'Affirmative Easements', 'Negative Easements', 'Creation Methods'],
                policy_rationales=[],
                common_traps=[],
                # 🛤️ Mnemonic (rhythmic): EASE
            ),
            KnowledgeNode(
                concept_id="real_property_concurrent_ownership",
                name="CONCURRENT OWNERSHIP",
                subject="real_property",
                difficulty=3,
                rule_statement="Joint tenancy requires four unities; tenancy in common has no survivorship; tenancy by entirety protects marital property from separate creditors.",
                elements=['Joint Tenancy', 'Tenancy in Common', 'Tenancy by Entirety', 'Severance', 'Partition'],
                policy_rationales=[],
                common_traps=[],
                # 👥 Mnemonic (acronym): TIE
            ),
            KnowledgeNode(
                concept_id="real_property_landlordtenant_law",
                name="LANDLORD-TENANT LAW",
                subject="real_property",
                difficulty=3,
                rule_statement="Landlord must maintain habitable premises; tenant must pay rent; holdover becomes periodic tenancy; self-help eviction is illegal in most states.",
                elements=['Implied Warranty of Habitability', 'Quiet Enjoyment', 'Retaliatory Evictions', 'Security Deposits', 'Assignment vs. Sublease'],
                policy_rationales=[],
                common_traps=[],
                # 🏠 Mnemonic (acronym): RENT
            ),
            KnowledgeNode(
                concept_id="real_property_mortgages_foreclosure_and_priority",
                name="MORTGAGES, FORECLOSURE & PRIORITY",
                subject="real_property",
                difficulty=3,
                rule_statement="Mortgage creates security interest; foreclosure terminates mortgagor's equity; purchase money mortgages have super-priority over later liens on same collateral.",
                elements=['Mortgage vs. Deed of Trust', 'Foreclosure Process', 'Deficiency Judgments', 'Due-on-Sale Clauses', 'Purchase Money Priority'],
                policy_rationales=[],
                common_traps=[],
                # 🏦 Mnemonic (acronym): MORT
            ),
            KnowledgeNode(
                concept_id="real_property_zoning_and_takings",
                name="ZONING & TAKINGS",
                subject="real_property",
                difficulty=3,
                rule_statement="Zoning regulates land use; takings require just compensation; variance is exception to zoning rules for hardship; exactions must be roughly proportional.",
                elements=['Zoning Ordinances', 'Variances & Special Permits', 'Physical vs. Regulatory Takings', 'Exactions', 'Inverse Condemnation'],
                policy_rationales=[],
                common_traps=[],
                # 🏛️ Mnemonic (acronym): ZONE
            ),
            KnowledgeNode(
                concept_id="real_property_adverse_possession",
                name="ADVERSE POSSESSION",
                subject="real_property",
                difficulty=3,
                rule_statement="Hostile, actual, exclusive, continuous possession for statutory period perfects title; color of title reduces period to 7 years.",
                elements=['Elements Required', 'Color of Title', 'Tacking', 'Disabilities', 'Boundary Disputes'],
                policy_rationales=[],
                common_traps=[],
                # ⚔️ Mnemonic (acronym): HATE
            ),
            KnowledgeNode(
                concept_id="real_property_fixtures",
                name="FIXTURES",
                subject="real_property",
                difficulty=3,
                rule_statement="Personal property becomes real property when permanently attached with intent to improve the realty; trade fixtures remain personal property.",
                elements=['FIX Test', 'Trade Fixtures', 'Mortgage Rights', 'Severance', 'Agricultural Fixtures'],
                policy_rationales=[],
                common_traps=[],
                # 🪑 Mnemonic (acronym): FIX
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

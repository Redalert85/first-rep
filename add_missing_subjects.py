#!/usr/bin/env python3
"""
Add missing subjects to bar_tutor_unified.py
Run this on your Mac: python3 add_missing_subjects.py
"""

import sys

# Read the file
with open('bar_tutor_unified.py', 'r') as f:
    content = f.read()

# Find the _initialize_all_subjects method and update it
old_init_all = """    def _initialize_all_subjects(self):
        \"\"\"Initialize all MBE subjects\"\"\"
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_evidence()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_civil_procedure()"""

new_init_all = """    def _initialize_all_subjects(self):
        \"\"\"Initialize all MBE and MEE subjects\"\"\"
        # MBE Subjects
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_evidence()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_criminal_procedure()
        self._initialize_civil_procedure()
        self._initialize_property()
        # MEE Subjects
        self._initialize_family_law()
        self._initialize_trusts_estates()
        self._initialize_business_associations()"""

content = content.replace(old_init_all, new_init_all)

# Add new initialization methods after civil_procedure
insert_point = """    def get_subject_concepts(self, subject: str) -> List[KnowledgeNode]:"""

new_methods = """
    def _initialize_criminal_procedure(self):
        \"\"\"Initialize criminal procedure\"\"\"
        crimpro = [
            KnowledgeNode(
                concept_id="crimpro_fourth_amendment",
                name="Fourth Amendment Search & Seizure",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="The Fourth Amendment protects against unreasonable searches and seizures",
                elements=["Reasonable expectation of privacy", "Warrant requirement", "Probable cause", "Exceptions"],
                common_traps=["Confusing reasonable suspicion with probable cause", "Missing warrant exceptions"]
            ),
            KnowledgeNode(
                concept_id="crimpro_miranda",
                name="Miranda Rights",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Police must give Miranda warnings before custodial interrogation",
                elements=["Custody", "Interrogation", "Warnings", "Waiver"],
                common_traps=["Thinking Miranda applies to all police interactions"]
            ),
            KnowledgeNode(
                concept_id="crimpro_exclusionary_rule",
                name="Exclusionary Rule",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Evidence obtained in violation of constitutional rights must be excluded",
                elements=["Constitutional violation", "Fruit of poisonous tree", "Exceptions"],
                common_traps=["Forgetting good faith exception", "Missing inevitable discovery"]
            )
        ]
        for node in crimpro:
            self.nodes[node.concept_id] = node

    def _initialize_property(self):
        \"\"\"Initialize property (real property)\"\"\"
        property_concepts = [
            KnowledgeNode(
                concept_id="property_estates",
                name="Estates in Land",
                subject="property",
                difficulty=3,
                rule_statement="Present possessory estates include fee simple absolute, defeasible fees, and life estates",
                elements=["Fee simple absolute", "Life estate", "Defeasible fees", "Future interests"],
                common_traps=["Confusing determinable vs. condition subsequent", "Forgetting RAP"]
            ),
            KnowledgeNode(
                concept_id="property_concurrent_ownership",
                name="Concurrent Ownership",
                subject="property",
                difficulty=3,
                rule_statement="Concurrent ownership includes tenancy in common, joint tenancy, and tenancy by entirety",
                elements=["Tenancy in common", "Joint tenancy (4 unities)", "Right of survivorship"],
                common_traps=["Forgetting four unities for joint tenancy"]
            ),
            KnowledgeNode(
                concept_id="property_easements",
                name="Easements",
                subject="property",
                difficulty=4,
                rule_statement="Easements grant right to use another's land, created by grant, implication, necessity, or prescription",
                elements=["Appurtenant vs. in gross", "Creation methods", "Termination"],
                common_traps=["Thinking easements in gross always run with land"]
            ),
            KnowledgeNode(
                concept_id="property_covenants",
                name="Real Covenants & Equitable Servitudes",
                subject="property",
                difficulty=4,
                rule_statement="Real covenants require writing, intent, touch and concern, notice, and privity; equitable servitudes don't require privity",
                elements=["Writing", "Intent", "Touch and concern", "Notice", "Privity (for covenants)"],
                common_traps=["Confusing covenant vs. servitude requirements"]
            ),
            KnowledgeNode(
                concept_id="property_adverse_possession",
                name="Adverse Possession",
                subject="property",
                difficulty=3,
                rule_statement="Adverse possession requires continuous, open and notorious, actual, hostile, and exclusive possession for statutory period",
                elements=["Continuous", "Open and notorious", "Actual", "Hostile", "Exclusive", "Statutory period"],
                common_traps=["Thinking permission defeats adverse possession"]
            ),
            KnowledgeNode(
                concept_id="property_recording_acts",
                name="Recording Acts",
                subject="property",
                difficulty=4,
                rule_statement="Recording acts protect subsequent purchasers: notice (last BFP wins), race (first to record wins), race-notice (first BFP to record wins)",
                elements=["Notice jurisdiction", "Race jurisdiction", "Race-notice jurisdiction", "BFP status"],
                common_traps=["Confusing three types of recording acts"]
            )
        ]
        for node in property_concepts:
            self.nodes[node.concept_id] = node

    def _initialize_family_law(self):
        \"\"\"Initialize family law (MEE subject)\"\"\"
        family = [
            KnowledgeNode(
                concept_id="family_marriage",
                name="Marriage & Marital Property",
                subject="family_law",
                difficulty=3,
                rule_statement="Marital property is divided upon divorce either equally (community property) or equitably (equitable distribution)",
                elements=["Marriage requirements", "Community vs. separate property", "Equitable distribution factors"],
                common_traps=["Forgetting to classify property as marital vs. separate"]
            ),
            KnowledgeNode(
                concept_id="family_divorce",
                name="Divorce & Separation",
                subject="family_law",
                difficulty=3,
                rule_statement="No-fault divorce available in all states; fault grounds may affect property division in some states",
                elements=["No-fault grounds", "Fault grounds", "Property division", "Spousal support"],
                common_traps=["Thinking fault always affects division"]
            ),
            KnowledgeNode(
                concept_id="family_child_custody",
                name="Child Custody & Support",
                subject="family_law",
                difficulty=3,
                rule_statement="Child custody determined by best interests of child; child support based on state guidelines",
                elements=["Legal custody", "Physical custody", "Best interests factors", "Child support calculation"],
                common_traps=["Confusing legal vs. physical custody"]
            )
        ]
        for node in family:
            self.nodes[node.concept_id] = node

    def _initialize_trusts_estates(self):
        \"\"\"Initialize trusts and estates (MEE subject)\"\"\"
        trusts = [
            KnowledgeNode(
                concept_id="trusts_creation",
                name="Trust Creation",
                subject="trusts_estates",
                difficulty=4,
                rule_statement="Valid trust requires settlor with capacity, intent, identifiable beneficiary, identifiable res, and valid trust purpose",
                elements=["Settlor capacity & intent", "Beneficiary", "Trust res (property)", "Trust purpose", "Writing (for real property)"],
                common_traps=["Forgetting Statute of Frauds for real property trusts"]
            ),
            KnowledgeNode(
                concept_id="wills_execution",
                name="Will Execution",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Valid will requires testamentary capacity, intent, signature, and attestation by witnesses",
                elements=["Testamentary capacity", "Intent", "Signature", "Witnesses", "Writing"],
                common_traps=["Forgetting witness requirements vary by state"]
            ),
            KnowledgeNode(
                concept_id="intestate_succession",
                name="Intestate Succession",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="When no valid will, property passes to heirs under intestacy statutes",
                elements=["Surviving spouse share", "Issue/descendants", "Parents", "Collateral relatives"],
                common_traps=["Forgetting spouse may not take all"]
            )
        ]
        for node in trusts:
            self.nodes[node.concept_id] = node

    def _initialize_business_associations(self):
        \"\"\"Initialize business associations (MEE subject)\"\"\"
        business = [
            KnowledgeNode(
                concept_id="biz_agency",
                name="Agency Relationships",
                subject="business_associations",
                difficulty=3,
                rule_statement="Agency created when principal manifests assent that agent act on principal's behalf and subject to control",
                elements=["Manifestation of assent", "Acting on behalf", "Subject to control", "Consent"],
                common_traps=["Confusing actual vs. apparent authority"]
            ),
            KnowledgeNode(
                concept_id="biz_partnership",
                name="General Partnerships",
                subject="business_associations",
                difficulty=3,
                rule_statement="Partnership is association of two or more persons carrying on business as co-owners for profit",
                elements=["Association of persons", "Carrying on business", "Co-owners", "For profit", "Sharing profits/losses"],
                common_traps=["Thinking formal agreement always required"]
            ),
            KnowledgeNode(
                concept_id="biz_corporation",
                name="Corporations",
                subject="business_associations",
                difficulty=4,
                rule_statement="Corporation is separate legal entity formed by filing articles with state; shareholders have limited liability",
                elements=["Articles of incorporation", "Separate legal entity", "Limited liability", "Board of directors", "Officers"],
                common_traps=["Forgetting piercing corporate veil requirements"]
            )
        ]
        for node in business:
            self.nodes[node.concept_id] = node

    def get_subject_concepts(self, subject: str) -> List[KnowledgeNode]:"""

content = content.replace(insert_point, new_methods + insert_point)

# Write the updated file
with open('bar_tutor_unified.py', 'w') as f:
    f.write(content)

print("✅ Added missing subjects:")
print("  - Criminal Procedure (3 concepts)")
print("  - Property/Real Property (6 concepts)")
print("  - Family Law (3 concepts)")
print("  - Trusts & Estates (3 concepts)")
print("  - Business Associations (3 concepts)")
print("\nTotal new concepts: 18")
print("\nNow restart the app: ./start.sh")

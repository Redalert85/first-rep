# Ultimate Expanded Knowledge Base - 112+ Concepts
# Each subject has 14+ concepts at Real Property richness level

def _initialize_civil_procedure(self):
    """Initialize civil_procedure - 14 comprehensive concepts"""
    concepts = [
        KnowledgeNode(
            concept_id="civil_procedure_jurisdiction_and_venue",
            name="Jurisdiction & Venue",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="",
            elements=['Mnemonic', 'Traps'],
            policy_rationales=[],
            common_traps=[
                "General vs specific jurisdiction",
                "minimum contacts",
                "domicile",
            ],
            # Mnemonic: PISSED
        ),
        KnowledgeNode(
            concept_id="civil_procedure_pleadings_and_motions",
            name="Pleadings & Motions",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="",
            elements=['Mnemonic', 'Traps'],
            policy_rationales=[],
            common_traps=[
                "Twiqbal plausibility",
                "relation back",
                "waiver of defenses.",
            ],
            # Mnemonic: CLAIMS
        ),
        KnowledgeNode(
            concept_id="civil_procedure_joinder_and_discovery",
            name="Joinder & Discovery",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="",
            elements=['Mnemonic', 'Traps'],
            policy_rationales=[],
            common_traps=[
                "Compulsory counterclaims",
                "indispensable parties",
                "discovery sanctions.",
            ],
            # Mnemonic: JEDI
        ),
        KnowledgeNode(
            concept_id="civil_procedure_pretrial_and_trial",
            name="Pretrial & Trial",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="",
            elements=['Mnemonic'],
            policy_rationales=[],
            common_traps=[],
            # Mnemonic: LIMES
        ),
        KnowledgeNode(
            concept_id="civil_procedure_judgments_and_preclusion",
            name="Judgments & Preclusion",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="",
            elements=['Mnemonic', 'Traps'],
            policy_rationales=[],
            common_traps=[
                "Same parties/privity",
                "mutual vs non-mutual collateral estoppel",
                "full faith and credit.

#### Visuals",
            ],
            # Mnemonic: RICE
        ),
        KnowledgeNode(
            concept_id="civil_procedure_subjectmatter_jurisdiction",
            name="SUBJECT-MATTER JURISDICTION",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="Federal courts need subject-matter jurisdiction via federal question, diversity exceeding $75,000 with complete diversity, or supplemental claims sharing common nucleus with anchor.",
            elements=['Federal Question', 'Diversity', 'Supplemental Jurisdiction', 'Removal/Remand'],
            policy_rationales=[],
            common_traps=[],
        ),
        KnowledgeNode(
            concept_id="civil_procedure_personal_jurisdiction",
            name="PERSONAL JURISDICTION",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="State court exercises personal jurisdiction where statute authorizes and Due Process satisfied through minimum contacts, purposeful availment, foreseeability, and fairness plus notice.",
            elements=['Long-Arm Statutes', 'Traditional Bases', 'Specific Jurisdiction', 'Fair Play Factors'],
            policy_rationales=[],
            common_traps=[],
        ),
        KnowledgeNode(
            concept_id="civil_procedure_subject_matter_jurisdiction__federal_question",
            name="Subject Matter Jurisdiction - Federal Question",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="Claim arises under federal law",
            elements=[],
            policy_rationales=[],
            common_traps=[],
        ),
        KnowledgeNode(
            concept_id="civil_procedure_subject_matter_jurisdiction__diversity",
            name="Subject Matter Jurisdiction - Diversity",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="Complete diversity + $75K",
            elements=[],
            policy_rationales=[],
            common_traps=[],
        ),
        KnowledgeNode(
            concept_id="civil_procedure_personal_jurisdiction__minimum_contacts",
            name="Personal Jurisdiction - Minimum Contacts",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="Purposeful availment required",
            elements=[],
            policy_rationales=[],
            common_traps=[],
        ),
        KnowledgeNode(
            concept_id="civil_procedure_personal_jurisdiction__fair_play",
            name="Personal Jurisdiction - Fair Play",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="Burden, forum interest, efficiency",
            elements=[],
            policy_rationales=[],
            common_traps=[],
        ),
        KnowledgeNode(
            concept_id="civil_procedure_service_of_process",
            name="Service of Process",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="Proper notice required for jurisdiction",
            elements=[],
            policy_rationales=[],
            common_traps=[],
        ),
        KnowledgeNode(
            concept_id="civil_procedure_pleading_standard__twombly",
            name="Pleading Standard - Twombly",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="Plausible claim, not mere possibility",
            elements=[],
            policy_rationales=[],
            common_traps=[],
        ),
        KnowledgeNode(
            concept_id="civil_procedure_summary_judgment",
            name="Summary Judgment",
            subject="civil_procedure",
            difficulty=3,
            rule_statement="No genuine dispute of material fact",
            elements=[],
            policy_rationales=[],
            common_traps=[],
        ),
    ]
    for node in concepts:
        self.nodes[node.concept_id] = node

    def _initialize_constitutional_law(self):
        """Initialize constitutional_law - 14 comprehensive concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="constitutional_law_judicial_power_and_justiciability",
                name="Judicial Power & Justiciability",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Case-or-controversy requirement demands standing (injury, causation, redressability), ripeness, and absence of mootness or political questions.",
                elements=['Rule', 'Mnemonic', 'Visual', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Taxpayer standing (usually none)",
                    "generalized grievances",
                    "mootness exceptions (e.g.",
                ],
                # Mnemonic: SCRAM
            ),
            KnowledgeNode(
                concept_id="constitutional_law_federal_legislative_power",
                name="Federal Legislative Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Congress operates within enumerated powers; Commerce Clause covers channels, instrumentalities, and substantial economic effects; Necessary & Proper clause implements enumerated powers.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Intrastate non-economic activity (Lopez)",
                    "attenuated chains under substantial-effects theory",
                    "anti-commandeering (New York v. US)",
                ],
                # Mnemonic: Can People Truly Win Now?
            ),
            KnowledgeNode(
                concept_id="constitutional_law_executive_power",
                name="Executive Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Presidential power peaks with congressional authorization, declines in twilight zones, bottomed out when defying Congress.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Executive agreements = binding without Senate",
                    "removal limits for independent agencies",
                    "pardon excludes impeachment",
                ],
                # Mnemonic: VETO PACT
            ),
            KnowledgeNode(
                concept_id="constitutional_law_federalism_and_state_power",
                name="Federalism & State Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Tenth Amendment reserves unenumerated powers; Supremacy Clause preempts conflicts; dormant Commerce Clause prevents discriminatory burdens; states cannot tax the federal government",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Facial neutrality with discriminatory effect",
                    "Article IV Privileges & Immunities limited to citizens",
                    "federal commandeering of states",
                ],
                # Mnemonic: DORM ROOM
            ),
            KnowledgeNode(
                concept_id="constitutional_law_individual_rights",
                name="Individual Rights",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Procedural DP requires notice + hearing for life/liberty/property; substantive DP protects fundamental rights via strict scrutiny, otherwise rational basis.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "At-will employment lacks property interest",
                    "stigma-plus requirement",
                    "emergency exceptions for hearings",
                ],
                # Mnemonic: MR. FIG CAP
            ),
            KnowledgeNode(
                concept_id="constitutional_law_equal_protection",
                name="Equal Protection",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Classification triggers scrutiny: suspect (strict), quasi-suspect (intermediate), others (rational basis); fundamental rights also trigger strict scrutiny.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Need discriminatory intent",
                    "federal alienage uses rational basis",
                    "affirmative action strict scrutiny",
                ],
                # Mnemonic: RAN GIL
            ),
            KnowledgeNode(
                concept_id="constitutional_law_first_amendment",
                name="First Amendment",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Content-based regulations = strict scrutiny; content-neutral TPM = intermediate; unprotected categories include incitement, obscenity, fighting words, true threats, child pornography.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Incitement requires imminence",
                    "fighting words must be face-to-face",
                    "prior restraint presumption",
                ],
                # Mnemonic: FOCI
            ),
            KnowledgeNode(
                concept_id="constitutional_law_federal_powers_and_supremacy",
                name="FEDERAL POWERS & SUPREMACY",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Congress legislates through enumerated powers, Necessary and Proper Clause, Commerce channels or substantial effects, while Supremacy Clause preempts conflicting state actions within enumerated sphere",
                elements=['Enumerated Powers', 'Commerce Authority', 'Preemption', 'Tenth Amendment Limits'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="constitutional_law_individual_rights_and_scrutiny",
                name="INDIVIDUAL RIGHTS & SCRUTINY",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Government action triggering individual rights receives strict, intermediate, or rational basis scrutiny depending on classification or burden, requiring tailored means and adequate governmental objec",
                elements=['State Action', 'Fundamental Rights', 'Equal Protection', 'Speech Regulation'],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

# (rest of file unchanged)

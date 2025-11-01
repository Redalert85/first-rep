# Generated Comprehensive Knowledge Base
# Each subject enhanced to Real Property level + 50%

    def _initialize_civil_procedure(self):
        """Initialize civil_procedure - Comprehensive expansion"""
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
                    "full faith and credit.  #### Visuals",
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
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_constitutional_law(self):
        """Initialize constitutional_law - Comprehensive expansion"""
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
                rule_statement="Tenth Amendment reserves unenumerated powers; Supremacy Clause preempts conflicts; dormant Commerce Clause prevents discriminatory burdens; states cannot tax the federal government.",
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

    def _initialize_contracts(self):
        """Initialize contracts - Comprehensive expansion"""
        concepts = [
            KnowledgeNode(
                concept_id="contracts_formation",
                name="Formation",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Advertisements (invitations)",
                    "UCC firm offers",
                    "mailbox rule twists",
                ],
                # Mnemonic: FOCI
            ),
            KnowledgeNode(
                concept_id="contracts_terms_and_interpretation",
                name="Terms & Interpretation",
                subject="contracts",
                difficulty=3,
                rule_statement="Common law mirror-image; UCC gap fillers; parol evidence.",
                elements=['Rule', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Battle of forms",
                    "parol evidence exceptions (ambiguity",
                    "fraud)",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_performance_and_breach",
                name="Performance & Breach",
                subject="contracts",
                difficulty=3,
                rule_statement="Common law substantial performance vs material breach; UCC perfect tender.",
                elements=['Rule', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Anticipatory repudiation (reasonable assurances)",
                    "divisible contracts",
                    "condition precedent vs subsequent.",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_remedies",
                name="Remedies",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Foreseeability (Hadley)",
                    "mitigation duties",
                    "liquidated damages (reasonable estimate",
                ],
                # Mnemonic: ERRS
            ),
            KnowledgeNode(
                concept_id="contracts_defenses",
                name="Defenses",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "SOF partial performance exceptions",
                    "mutual mistake vs unilateral",
                    "impossibility vs frustration.",
                ],
                # Mnemonic: STUPID
            ),
            KnowledgeNode(
                concept_id="contracts_thirdparty_rights",
                name="Third-Party Rights",
                subject="contracts",
                difficulty=3,
                rule_statement="Assignments, delegations, third-party beneficiaries.",
                elements=['Rule', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Revocation of gratuitous assignments",
                    "delegation of special skills",
                    "vesting of third-party rights.",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_ucc_delivery_title_and_risk_of_loss",
                name="UCC Delivery, Title & Risk of Loss",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Hierarchy', 'Shipment vs Destination', 'No Carrier', 'Casualty to Identified Goods', 'Entrustment & Voidable Title'],
                policy_rationales=[],
                common_traps=[
                    "Breach always keeps risk on breaching party; “FOB plant” is shipment",
                    "not destination; merchant receipt requirement.",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_acceptance_rejection_and_revocation_ucc",
                name="Acceptance, Rejection & Revocation (UCC)",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Acceptance', 'Rejection', 'Revocation of Acceptance', 'Adequate Assurances', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Using goods extensively after discovering defect can bar revocation; COD shipments limit inspection ",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_excuse_impossibility_impracticability_frustration",
                name="Excuse: Impossibility, Impracticability, Frustration",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Impossibility / Impracticability', 'Partial Impracticability', 'Frustration of Purpose', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Mere increased cost insufficient unless extreme; assuming price fluctuation risk defeats excuse.",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_modification_accord_and_satisfaction_novation",
                name="Modification, Accord & Satisfaction, Novation",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Modification', 'Accord & Satisfaction', 'Novation', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Modification of firm offer beyond three months requires fresh consideration; distinguishing novation",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_warranties_ucc_and_common",
                name="Warranties (UCC & Common)",
                subject="contracts",
                difficulty=3,
                rule_statement="",
                elements=['Express', 'Implied Warranty of Merchantability', 'Implied Warranty of Fitness', 'Disclaimers', 'Limitations'],
                policy_rationales=[],
                common_traps=[
                    "Statements of opinion/puffery not express warranties; “as is” doesn’t negate express warranties; lim",
                ],
            ),
            KnowledgeNode(
                concept_id="contracts_offer_acceptance_consideration",
                name="OFFER, ACCEPTANCE, CONSIDERATION",
                subject="contracts",
                difficulty=3,
                rule_statement="Valid contract needs offer showing commitment, acceptance mirroring material terms, and consideration or substitute reliance creating bargained-for exchange with mutual assent and capacity.",
                elements=['Offer Dynamics', 'Acceptance Mechanics', 'Consideration', 'Formation Defenses'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="contracts_performance_breach_remedies",
                name="PERFORMANCE, BREACH, REMEDIES",
                subject="contracts",
                difficulty=3,
                rule_statement="Performance judged by strict compliance for non-UCC or perfect tender under Article 2; material breach excuses; remedies include expectation, reliance, restitution, specific performance.",
                elements=['Conditions', 'Material Breach', 'UCC Obligations', 'Remedies'],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_criminal_law(self):
        """Initialize criminal_law - Comprehensive expansion"""
        concepts = [
            KnowledgeNode(
                concept_id="criminal_law_elements_of_crimes",
                name="Elements of Crimes",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Every offense needs a voluntary act (or qualifying omission), the requisite mental state, concurrence, and causation.",
                elements=['Rule', 'Actus Reus', 'Mens Rea (MPC hierarchy)', 'Concurrence', 'Causation'],
                policy_rationales=[],
                common_traps=[
                    "Specific vs general intent (intoxication defenses)",
                    "transferred intent limited to same crime",
                    "medical negligence generally foreseeable",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_law_homicide_offenses",
                name="Homicide Offenses",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Murder = unlawful killing with malice aforethought (intent to kill, intent to seriously injure, depraved heart, felony murder). Manslaughter lacks malice.",
                elements=['Rule', 'Hierarchy', 'Felony Murder', 'Mnemonics', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Instant premeditation allowed; deadly weapon inference; felony-murder merger; cooling-off defeats vo",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_law_other_crimes_against_persons",
                name="Other Crimes Against Persons",
                subject="criminal_law",
                difficulty=3,
                rule_statement="",
                elements=['Battery', 'Assault', 'Kidnapping', 'False Imprisonment', 'Rape'],
                policy_rationales=[],
                common_traps=[
                    "Battery requires only intent to touch; assault has two theories; kidnapping needs substantial moveme",
                ],
                # Mnemonic: BARK
            ),
            KnowledgeNode(
                concept_id="criminal_law_property_crimes",
                name="Property Crimes",
                subject="criminal_law",
                difficulty=3,
                rule_statement="",
                elements=['Larceny', 'Robbery', 'Embezzlement', 'False Pretenses', 'Burglary'],
                policy_rationales=[],
                common_traps=[
                    "Intent at time of taking (larceny); assaultive felonies merge; force must accompany taking for robbe",
                ],
                # Mnemonic: LREF
            ),
            KnowledgeNode(
                concept_id="criminal_law_inchoate_crimes",
                name="Inchoate Crimes",
                subject="criminal_law",
                difficulty=3,
                rule_statement="",
                elements=['Solicitation', 'Conspiracy', 'Attempt', 'Mnemonics', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Solicitation complete without acceptance; conspiracy survives completed offense; attempt always spec",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_law_accomplice_and_accessory_liability",
                name="Accomplice & Accessory Liability",
                subject="criminal_law",
                difficulty=3,
                rule_statement="",
                elements=['Accomplice', 'Accessory After the Fact', 'Principal', 'Mnemonics', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Mere presence insufficient; dual intent requirement; accomplice liability remains even if principal ",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_law_defenses",
                name="Defenses",
                subject="criminal_law",
                difficulty=3,
                rule_statement="",
                elements=['Self-Defense', 'Defense of Others/Property/Necessity', 'Duress', 'Intoxication', 'Insanity Tests'],
                policy_rationales=[],
                common_traps=[
                    "Duress unavailable for murder; voluntary intoxication limited; entrapment fails if predisposed; mist",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_law_mens_rea_and_homicide",
                name="MENS REA & HOMICIDE",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Criminal liability requires actus reus with mens rea of purpose, knowledge, recklessness, or negligence; homicide classifications depend on malice aforethought, intent, depraved heart, felony murder.",
                elements=['Mens Rea Levels', 'Murder', 'Manslaughter', 'Defenses'],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_criminal_procedure(self):
        """Initialize criminal_procedure - Comprehensive expansion"""
        concepts = [
            KnowledgeNode(
                concept_id="criminal_procedure_fourth_amendment",
                name="Fourth Amendment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Traps'],
                policy_rationales=[],
                common_traps=[
                    "Standing (expectation of privacy)",
                    "private search doctrine",
                    "warrant particularity",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_exclusionary_rule",
                name="Exclusionary Rule",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Impeachment use",
                    "Miranda violations (non-Miranda statements may be used for impeachment)",
                    "attenuation factors.",
                ],
                # Mnemonic: FISSURE
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_fifth_amendment",
                name="Fifth Amendment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Traps'],
                policy_rationales=[],
                common_traps=[
                    "Ambiguous requests",
                    "re-initiation by suspect",
                    "public-safety exception",
                ],
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_sixth_amendment",
                name="Sixth Amendment",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Offense-specific attachment",
                    "deliberate elicitation",
                    "Massiah",
                ],
                # Mnemonic: PACED
            ),
            KnowledgeNode(
                concept_id="criminal_procedure_search_seizure_statements",
                name="SEARCH, SEIZURE, STATEMENTS",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Fourth Amendment protects reasonable expectations of privacy; warrants need probable cause and particularity; exclusionary rule suppressed violations; Fifth and Sixth regulate interrogation, counsel, ",
                elements=['Standing', 'Warrant Exceptions', 'Exclusionary Limits', 'Interrogations'],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_evidence(self):
        """Initialize evidence - Comprehensive expansion"""
        concepts = [
            KnowledgeNode(
                concept_id="evidence_relevance",
                name="Relevance",
                subject="evidence",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps', 'Preliminary Questions (FRE 104)', 'Limiting Instructions (FRE 105)', 'Rule of Completeness (FRE 106)'],
                policy_rationales=[],
                common_traps=[
                    "Subsequent remedial measures",
                    "settlements",
                    "offers to pay medical expenses",
                ],
                # Mnemonic: 403 Balance
            ),
            KnowledgeNode(
                concept_id="evidence_character_evidence",
                name="Character Evidence",
                subject="evidence",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic'],
                policy_rationales=[],
                common_traps=[],
                # Mnemonic: CRIME
            ),
            KnowledgeNode(
                concept_id="evidence_hearsay",
                name="Hearsay",
                subject="evidence",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Key Exceptions', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Double hearsay",
                    "testimonial statements confronting (Crawford)",
                    "former testimony requirements.",
                ],
                # Mnemonic: HEARSAY
            ),
            KnowledgeNode(
                concept_id="evidence_witnesses_and_impeachment",
                name="Witnesses & Impeachment",
                subject="evidence",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Collateral matters",
                    "prior consistent vs inconsistent statements",
                    "confrontation Clause for testimonial hearsay.",
                ],
                # Mnemonic: PC FARMS
            ),
            KnowledgeNode(
                concept_id="evidence_privileges_and_policy",
                name="Privileges & Policy",
                subject="evidence",
                difficulty=3,
                rule_statement="",
                elements=['Mnemonic', 'Traps', 'Best Evidence Flex', 'Digital Authentication', 'Updated Prior Consistent Statements'],
                policy_rationales=[],
                common_traps=[
                    "Spousal privileges scope",
                    "waiver by presence of third parties",
                    "work-product doctrine.  #### Visuals",
                ],
                # Mnemonic: CLAPS
            ),
            KnowledgeNode(
                concept_id="evidence_relevance_and_character",
                name="RELEVANCE & CHARACTER",
                subject="evidence",
                difficulty=3,
                rule_statement="Evidence must be relevant, probative value not outweighed by unfair prejudice; character evidence limited except for habit, impeachment, or cases placing character at issue.",
                elements=['Rule 403', 'Character Evidence', 'Other Acts', 'Impeachment'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="evidence_hearsay_and_exceptions",
                name="HEARSAY & EXCEPTIONS",
                subject="evidence",
                difficulty=3,
                rule_statement="Hearsay is out-of-court statement offered for truth, inadmissible absent exemption or exception such as opposing party statements, present sense impression, excited utterance, business records.",
                elements=['Non-Hearsay Uses', 'Exemptions', 'Unavailable Declarant', 'Reliability Exceptions'],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_real_property(self):
        """Initialize real_property - Comprehensive expansion"""
        concepts = [
            KnowledgeNode(
                concept_id="real_property_estates_and_future_interests",
                name="ESTATES & FUTURE INTERESTS",
                subject="real_property",
                difficulty=3,
                rule_statement="Present estates include fee simple, life estates, and leaseholds; future interests vest in grantor or third parties subject to RAP, waste, and defeasibility doctrines.",
                elements=['Fee Estates', 'Life Estates', 'Future Interests', 'RAP Analysis'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="real_property_conveyancing_and_recording",
                name="CONVEYANCING & RECORDING",
                subject="real_property",
                difficulty=3,
                rule_statement="Valid conveyance needs competent grantor, executed deed, delivery, and acceptance; recording acts protect bona fide purchasers without notice who record first depending on statute type.",
                elements=['Deed Formalities', 'Notice Types', 'Recording Acts', 'Chain Issues'],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_torts(self):
        """Initialize torts - Comprehensive expansion"""
        concepts = [
            KnowledgeNode(
                concept_id="torts_intentional_torts",
                name="Intentional Torts",
                subject="torts",
                difficulty=3,
                rule_statement="Battery, assault, false imprisonment, IIED require volitional acts with intent or substantial certainty.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Transferred intent",
                    "consent scope",
                    "shopkeeper’s privilege limits",
                ],
                # Mnemonic: BAFI²
            ),
            KnowledgeNode(
                concept_id="torts_negligence",
                name="Negligence",
                subject="torts",
                difficulty=3,
                rule_statement="Duty, breach (reasonable person or custom), actual/ proximate cause, damages.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Duty to unforeseeable plaintiffs (Cardozo vs Andrews)",
                    "res ipsa limits",
                    "superseding vs intervening causes",
                ],
                # Mnemonic: DBCD
            ),
            KnowledgeNode(
                concept_id="torts_strict_liability_and_products",
                name="Strict Liability & Products",
                subject="torts",
                difficulty=3,
                rule_statement="Strict liability for abnormally dangerous activities, wild animals; product claims under strict, negligence, warranty theories.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Product misuse vs foreseeable misuse",
                    "learned intermediary (pharma)",
                    "design vs manufacturing defects tests.",
                ],
                # Mnemonic: ADAMS
            ),
            KnowledgeNode(
                concept_id="torts_defamation_and_privacy",
                name="Defamation & Privacy",
                subject="torts",
                difficulty=3,
                rule_statement="False statements harming reputation; public concern triggers constitutional actual-fault requirements.",
                elements=['Rule', 'Mnemonic', 'Traps', 'Micro-Hypos'],
                policy_rationales=[],
                common_traps=[
                    "Opinions vs fact",
                    "public vs private figures (actual malice vs negligence)",
                    "privacy tort distinctions (intrusion",
                ],
                # Mnemonic: PDPF
            ),
            KnowledgeNode(
                concept_id="torts_economic_and_dignitary",
                name="Economic & Dignitary",
                subject="torts",
                difficulty=3,
                rule_statement="Intentional interference, fraudulent misrepresentation, malicious prosecution.",
                elements=['Rule', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Economic harm requirements",
                    "privilege defenses",
                    "probable cause in malicious prosecution.",
                ],
            ),
            KnowledgeNode(
                concept_id="torts_vicarious_liability_and_damages",
                name="Vicarious Liability & Damages",
                subject="torts",
                difficulty=3,
                rule_statement="Employers liable for employees acting in scope; punitive damages limited; joint & several vs several depending on jurisdiction.",
                elements=['Rule', 'Traps'],
                policy_rationales=[],
                common_traps=[
                    "Frolic vs detour",
                    "independent contractor exceptions",
                    "collateral source rule variations.  #### Visuals",
                ],
            ),
            KnowledgeNode(
                concept_id="torts_negligence_elements",
                name="NEGLIGENCE ELEMENTS",
                subject="torts",
                difficulty=3,
                rule_statement="Negligence requires duty owed, breach by unreasonable conduct, actual and proximate causation, and damages; defenses include comparative fault, assumption of risk, statutes.",
                elements=['Duty', 'Breach', 'Causation', 'Defenses'],
                policy_rationales=[],
                common_traps=[],
            ),
            KnowledgeNode(
                concept_id="torts_strict_liability_and_products_liability",
                name="STRICT LIABILITY & PRODUCTS LIABILITY",
                subject="torts",
                difficulty=3,
                rule_statement="Strict liability covers abnormally dangerous activities, wild animals, and product defects proven through manufacturing, design, or warning failure where foreseeable plaintiffs suffer harm.",
                elements=['Abnormally Dangerous', 'Products Liability', 'Defenses', 'Warranties'],
                policy_rationales=[],
                common_traps=[],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


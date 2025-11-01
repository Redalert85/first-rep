#!/usr/bin/env python3
"""
Complete expansion of all subjects with comprehensive concept coverage
Run on your Mac: python3 expand_all_subjects.py
"""

import re

# Read the current file
with open('bar_tutor_unified.py', 'r') as f:
    content = f.read()

# Find and replace the entire LegalKnowledgeGraph class methods section
# We'll keep everything up to _initialize_all_subjects and replace from there

# Find the class definition start
class_start = content.find('class LegalKnowledgeGraph:')
if class_start == -1:
    print("ERROR: Could not find LegalKnowledgeGraph class")
    exit(1)

# Find where get_subject_concepts starts (this is after all init methods)
methods_end = content.find('    def get_subject_concepts(self, subject: str)')
if methods_end == -1:
    print("ERROR: Could not find get_subject_concepts method")
    exit(1)

# Keep everything before _initialize_all_subjects
init_all_start = content.find('    def _initialize_all_subjects(self):')
if init_all_start == -1:
    print("ERROR: Could not find _initialize_all_subjects")
    exit(1)

# Build the complete replacement
before_methods = content[:init_all_start]
after_methods = content[methods_end:]

# Now build all the comprehensive initialization methods
new_methods = '''    def _initialize_all_subjects(self):
        """Initialize all MBE and MEE subjects with comprehensive coverage"""
        # MBE Subjects (7)
        self._initialize_contracts()
        self._initialize_torts()
        self._initialize_evidence()
        self._initialize_constitutional_law()
        self._initialize_criminal_law()
        self._initialize_criminal_procedure()
        self._initialize_civil_procedure()
        self._initialize_property()
        # MEE Subjects (3 core)
        self._initialize_family_law()
        self._initialize_trusts_estates()
        self._initialize_business_associations()

    def _initialize_contracts(self):
        """Initialize contracts with comprehensive coverage (20 concepts)"""
        contracts = [
            # Formation
            KnowledgeNode(
                concept_id="contracts_formation",
                name="Contract Formation",
                subject="contracts",
                difficulty=2,
                rule_statement="A contract is formed when there is mutual assent (offer + acceptance) supported by consideration",
                elements=["Offer", "Acceptance", "Consideration", "No defenses to formation"],
                policy_rationales=[
                    "Protect reasonable expectations in commercial dealings",
                    "Enforce voluntary agreements"
                ],
                common_traps=["Confusing preliminary negotiations with offers", "Forgetting mailbox rule"]
            ),
            KnowledgeNode(
                concept_id="contracts_offer",
                name="Offer",
                subject="contracts",
                difficulty=3,
                prerequisites=["contracts_formation"],
                rule_statement="An offer is a manifestation of willingness to enter a bargain, made so that another reasonably believes they can accept",
                elements=["Definite terms", "Communication to offeree", "Intent to be bound"],
                exceptions=["Advertisements are invitations", "Price quotes not offers"],
                common_traps=["Thinking all communications are offers", "Missing termination by counteroffer"]
            ),
            KnowledgeNode(
                concept_id="contracts_acceptance",
                name="Acceptance",
                subject="contracts",
                difficulty=3,
                prerequisites=["contracts_offer"],
                rule_statement="Acceptance must be unequivocal assent to offer's terms, communicated by authorized means",
                elements=["Mirror image rule (CL)", "Mailbox rule", "UCC 2-207 (additional terms)"],
                common_traps=["Forgetting mailbox rule doesn't apply to option contracts"]
            ),
            KnowledgeNode(
                concept_id="contracts_consideration",
                name="Consideration",
                subject="contracts",
                difficulty=2,
                rule_statement="Consideration is bargained-for exchange of legal value between parties",
                elements=["Bargained-for exchange", "Legal value", "Not past consideration", "Not preexisting duty"],
                common_traps=["Thinking past consideration sufficient", "Missing preexisting duty rule"]
            ),
            KnowledgeNode(
                concept_id="contracts_promissory_estoppel",
                name="Promissory Estoppel",
                subject="contracts",
                difficulty=3,
                rule_statement="Promise enforceable if promisor should reasonably expect reliance, promisee relies to detriment, and injustice avoided only by enforcement",
                elements=["Promise", "Reasonable expectation of reliance", "Actual detrimental reliance", "Injustice"],
                common_traps=["Forgetting this is substitute for consideration"]
            ),
            # Defenses
            KnowledgeNode(
                concept_id="contracts_statute_of_frauds",
                name="Statute of Frauds",
                subject="contracts",
                difficulty=4,
                rule_statement="Certain contracts must be in writing: marriage, suretyship, land, year, UCC goods $500+",
                elements=["MY LEGS mnemonic", "Writing requirement", "Signature", "Essential terms"],
                common_traps=["Forgetting part performance exception for land", "Missing merchant confirmation rule"]
            ),
            KnowledgeNode(
                concept_id="contracts_capacity",
                name="Capacity & Incapacity",
                subject="contracts",
                difficulty=2,
                rule_statement="Minors and mentally incompetent persons may void contracts; intoxication if other party knew",
                elements=["Minors (voidable)", "Mental incapacity", "Intoxication", "Ratification"],
                common_traps=["Thinking necessaries are voidable"]
            ),
            KnowledgeNode(
                concept_id="contracts_mistake",
                name="Mistake",
                subject="contracts",
                difficulty=3,
                rule_statement="Mutual mistake of basic assumption allows rescission if material effect; unilateral mistake if other party knew/caused",
                elements=["Mutual vs. unilateral", "Basic assumption", "Material effect", "Risk allocation"],
                common_traps=["Confusing mistake of value vs. fact"]
            ),
            KnowledgeNode(
                concept_id="contracts_misrepresentation",
                name="Misrepresentation & Fraud",
                subject="contracts",
                difficulty=3,
                rule_statement="Fraudulent misrepresentation makes contract voidable if material false statement, intent to induce, justifiable reliance",
                elements=["False statement of fact", "Scienter (fraudulent)", "Intent to induce", "Justifiable reliance", "Materiality"],
                common_traps=["Forgetting concealment can be misrepresentation"]
            ),
            KnowledgeNode(
                concept_id="contracts_duress_undue_influence",
                name="Duress & Undue Influence",
                subject="contracts",
                difficulty=3,
                rule_statement="Contract voidable if entered under improper threat (duress) or dominated by confidential relationship (undue influence)",
                elements=["Improper threat", "No reasonable alternative", "Confidential relationship", "Unfair persuasion"],
                common_traps=["Thinking economic duress requires physical threat"]
            ),
            # Performance & Breach
            KnowledgeNode(
                concept_id="contracts_conditions",
                name="Conditions",
                subject="contracts",
                difficulty=4,
                rule_statement="Condition is event that must occur before performance due; conditions can be express, implied, or constructive",
                elements=["Condition precedent", "Condition subsequent", "Concurrent conditions", "Excuse of condition"],
                common_traps=["Confusing condition with promise", "Missing substantial compliance for constructive conditions"]
            ),
            KnowledgeNode(
                concept_id="contracts_performance",
                name="Performance & Breach",
                subject="contracts",
                difficulty=3,
                rule_statement="Perfect tender required under UCC; substantial performance sufficient at common law unless material breach",
                elements=["Substantial performance (CL)", "Perfect tender (UCC)", "Material vs. minor breach", "Timing of performance"],
                common_traps=["Forgetting perfect tender doesn't apply to CL contracts"]
            ),
            KnowledgeNode(
                concept_id="contracts_anticipatory_repudiation",
                name="Anticipatory Repudiation",
                subject="contracts",
                difficulty=3,
                rule_statement="Unequivocal refusal to perform before performance due; non-breaching party may treat as breach or wait",
                elements=["Unequivocal refusal", "Before performance due", "Options for non-breaching party", "Retraction"],
                common_traps=["Thinking mere doubt is repudiation"]
            ),
            KnowledgeNode(
                concept_id="contracts_impossibility",
                name="Impossibility, Impracticability, Frustration",
                subject="contracts",
                difficulty=4,
                rule_statement="Performance excused if supervening event makes it impossible, impracticable, or frustrates purpose",
                elements=["Supervening event", "Not foreseeable", "Not fault of party", "Impossibility vs. impracticability"],
                common_traps=["Thinking increased cost = impracticability"]
            ),
            # Remedies
            KnowledgeNode(
                concept_id="contracts_expectation_damages",
                name="Expectation Damages",
                subject="contracts",
                difficulty=3,
                rule_statement="Put non-breaching party in position they would have been in if contract performed",
                elements=["Loss in value", "Other losses", "Minus costs avoided", "Certainty required"],
                common_traps=["Forgetting to subtract costs avoided", "Missing mitigation requirement"]
            ),
            KnowledgeNode(
                concept_id="contracts_reliance_restitution",
                name="Reliance & Restitution Damages",
                subject="contracts",
                difficulty=3,
                rule_statement="Reliance restores status quo; restitution prevents unjust enrichment",
                elements=["Reliance damages", "Restitution", "Quantum meruit", "Unjust enrichment"],
                common_traps=["Confusing reliance with expectation"]
            ),
            KnowledgeNode(
                concept_id="contracts_specific_performance",
                name="Specific Performance",
                subject="contracts",
                difficulty=3,
                rule_statement="Equitable remedy ordering breaching party to perform; available when damages inadequate",
                elements=["Damages inadequate", "Unique goods", "Land contracts", "Personal service contracts (no SP)"],
                common_traps=["Thinking SP available for personal services"]
            ),
            KnowledgeNode(
                concept_id="contracts_liquidated_damages",
                name="Liquidated Damages",
                subject="contracts",
                difficulty=3,
                rule_statement="Pre-agreed damages enforceable if reasonable and damages difficult to estimate at formation",
                elements=["Reasonable estimate", "Damages uncertain at formation", "Not penalty"],
                common_traps=["Thinking reasonableness judged at breach, not formation"]
            ),
            # Third Parties
            KnowledgeNode(
                concept_id="contracts_third_party_beneficiaries",
                name="Third-Party Beneficiaries",
                subject="contracts",
                difficulty=4,
                rule_statement="Intended beneficiary can enforce; incidental beneficiary cannot",
                elements=["Intended vs. incidental", "Creditor beneficiary", "Donee beneficiary", "Vesting of rights"],
                common_traps=["Confusing incidental with intended beneficiary"]
            ),
            KnowledgeNode(
                concept_id="contracts_assignment_delegation",
                name="Assignment & Delegation",
                subject="contracts",
                difficulty=4,
                rule_statement="Rights generally assignable unless personal, materially change duty, or prohibited; duties delegable except personal services",
                elements=["Assignment of rights", "Delegation of duties", "Limitations", "Obligor's defenses"],
                common_traps=["Thinking 'no assignment' clause prevents assignment (only makes it breach)"]
            ),
        ]
        for node in contracts:
            self.nodes[node.concept_id] = node

    def _initialize_torts(self):
        """Initialize torts with comprehensive coverage (18 concepts)"""
        torts = [
            # Intentional Torts
            KnowledgeNode(
                concept_id="torts_battery",
                name="Battery",
                subject="torts",
                difficulty=2,
                rule_statement="Battery is intentional harmful or offensive contact with plaintiff's person",
                elements=["Intent", "Harmful or offensive contact", "To plaintiff's person", "Causation"],
                common_traps=["Thinking injury required", "Missing transferred intent"]
            ),
            KnowledgeNode(
                concept_id="torts_assault",
                name="Assault",
                subject="torts",
                difficulty=2,
                rule_statement="Assault is act creating reasonable apprehension of imminent harmful or offensive contact",
                elements=["Intent", "Reasonable apprehension", "Imminent contact", "Plaintiff's awareness"],
                common_traps=["Thinking words alone sufficient", "Missing immediacy requirement"]
            ),
            KnowledgeNode(
                concept_id="torts_false_imprisonment",
                name="False Imprisonment",
                subject="torts",
                difficulty=3,
                rule_statement="Intentional confinement within boundaries fixed by defendant with no reasonable means of escape",
                elements=["Intent", "Confinement", "Bounded area", "No reasonable escape", "Consciousness or harm"],
                common_traps=["Thinking moral pressure sufficient"]
            ),
            KnowledgeNode(
                concept_id="torts_iied",
                name="Intentional Infliction of Emotional Distress (IIED)",
                subject="torts",
                difficulty=3,
                rule_statement="Extreme and outrageous conduct intentionally or recklessly causing severe emotional distress",
                elements=["Extreme and outrageous conduct", "Intent or recklessness", "Causation", "Severe emotional distress"],
                common_traps=["Thinking mere insults sufficient", "Missing 'severe' requirement"]
            ),
            KnowledgeNode(
                concept_id="torts_trespass_to_land",
                name="Trespass to Land",
                subject="torts",
                difficulty=2,
                rule_statement="Intentional physical invasion of plaintiff's real property",
                elements=["Intent to enter", "Physical invasion", "Plaintiff's land", "No harm required"],
                common_traps=["Thinking mistake of ownership is defense"]
            ),
            KnowledgeNode(
                concept_id="torts_trespass_to_chattels",
                name="Trespass to Chattels & Conversion",
                subject="torts",
                difficulty=3,
                rule_statement="Trespass is minor interference with personal property; conversion is substantial interference requiring full value",
                elements=["Intent to interfere", "Personal property", "Substantial interference (conversion)", "Damages"],
                common_traps=["Confusing degree of interference between trespass and conversion"]
            ),
            # Negligence
            KnowledgeNode(
                concept_id="torts_negligence",
                name="Negligence",
                subject="torts",
                difficulty=2,
                rule_statement="Negligence requires duty, breach, causation (actual and proximate), and damages",
                elements=["Duty", "Breach", "Actual causation", "Proximate causation", "Damages"],
                common_traps=["Forgetting damages required", "Missing any element"]
            ),
            KnowledgeNode(
                concept_id="torts_duty",
                name="Duty of Care",
                subject="torts",
                difficulty=3,
                rule_statement="Generally owe duty of reasonable care to foreseeable plaintiffs; no duty to rescue absent special relationship",
                elements=["Reasonable person standard", "Foreseeable plaintiff", "Special relationships", "No duty to rescue"],
                common_traps=["Thinking duty owed to unforeseeable plaintiffs"]
            ),
            KnowledgeNode(
                concept_id="torts_breach",
                name="Breach of Duty",
                subject="torts",
                difficulty=2,
                rule_statement="Breach when defendant's conduct falls below reasonable person standard",
                elements=["Reasonable person standard", "Custom evidence", "Negligence per se", "Res ipsa loquitur"],
                common_traps=["Thinking custom establishes standard of care"]
            ),
            KnowledgeNode(
                concept_id="torts_actual_causation",
                name="Actual Causation",
                subject="torts",
                difficulty=3,
                rule_statement="But-for test: but for defendant's conduct, injury would not have occurred; substantial factor test for multiple causes",
                elements=["But-for test", "Substantial factor", "Multiple sufficient causes", "Loss of chance"],
                common_traps=["Missing substantial factor test for concurrent causes"]
            ),
            KnowledgeNode(
                concept_id="torts_proximate_causation",
                name="Proximate Causation",
                subject="torts",
                difficulty=4,
                rule_statement="Defendant liable for foreseeable consequences; unforeseeable intervening causes may cut off liability",
                elements=["Foreseeability", "Direct cause", "Intervening causes", "Superseding causes"],
                common_traps=["Thinking eggshell plaintiff rule applies to proximate cause"]
            ),
            KnowledgeNode(
                concept_id="torts_damages",
                name="Damages",
                subject="torts",
                difficulty=2,
                rule_statement="Plaintiff must prove actual damages; includes economic and non-economic losses",
                elements=["Actual damages required", "Economic losses", "Non-economic losses", "Eggshell plaintiff rule"],
                common_traps=["Forgetting eggshell plaintiff rule"]
            ),
            KnowledgeNode(
                concept_id="torts_defenses",
                name="Negligence Defenses",
                subject="torts",
                difficulty=3,
                rule_statement="Contributory negligence (complete bar), comparative negligence (reduces damages), assumption of risk (no duty)",
                elements=["Contributory negligence", "Comparative negligence (pure/modified)", "Assumption of risk"],
                common_traps=["Applying wrong comparative negligence type"]
            ),
            # Strict Liability
            KnowledgeNode(
                concept_id="torts_strict_liability",
                name="Strict Liability",
                subject="torts",
                difficulty=3,
                rule_statement="Liability without fault for abnormally dangerous activities and wild animals",
                elements=["Abnormally dangerous activity", "Wild animals", "No intent or negligence required", "Actual and proximate cause"],
                common_traps=["Thinking domesticated animals trigger strict liability"]
            ),
            KnowledgeNode(
                concept_id="torts_products_liability",
                name="Products Liability",
                subject="torts",
                difficulty=4,
                rule_statement="Manufacturer/seller strictly liable for defective product causing injury to foreseeable plaintiff",
                elements=["Manufacturing defect", "Design defect", "Warning defect", "Causation", "Foreseeable plaintiff"],
                common_traps=["Forgetting plaintiff need not be purchaser"]
            ),
            # Nuisance
            KnowledgeNode(
                concept_id="torts_nuisance",
                name="Private & Public Nuisance",
                subject="torts",
                difficulty=3,
                rule_statement="Private nuisance is substantial unreasonable interference with use and enjoyment of land",
                elements=["Substantial interference", "Unreasonable", "Use and enjoyment", "Private vs. public nuisance"],
                common_traps=["Thinking any annoyance is nuisance"]
            ),
            # Defamation
            KnowledgeNode(
                concept_id="torts_defamation",
                name="Defamation",
                subject="torts",
                difficulty=4,
                rule_statement="Defamatory statement of fact published to third party causing damages; public figures must prove actual malice",
                elements=["Defamatory statement", "Of and concerning plaintiff", "Publication", "Damages", "Fault"],
                common_traps=["Forgetting opinion not actionable", "Missing actual malice for public figures"]
            ),
            # Vicarious Liability
            KnowledgeNode(
                concept_id="torts_vicarious_liability",
                name="Vicarious Liability",
                subject="torts",
                difficulty=3,
                rule_statement="Employer liable for employee's torts within scope of employment; principal liable for agent's authorized torts",
                elements=["Respondeat superior", "Scope of employment", "Independent contractor exception", "Frolic vs. detour"],
                common_traps=["Thinking employer liable for independent contractor"]
            ),
        ]
        for node in torts:
            self.nodes[node.concept_id] = node

    def _initialize_evidence(self):
        """Initialize evidence with comprehensive coverage (16 concepts)"""
        evidence = [
            # Relevance
            KnowledgeNode(
                concept_id="evidence_relevance",
                name="Relevance",
                subject="evidence",
                difficulty=2,
                rule_statement="Evidence relevant if tendency to make fact more or less probable and fact is of consequence",
                elements=["Tendency to prove", "Fact of consequence", "FRE 401", "FRE 402 - admissible unless excluded"],
                common_traps=["Thinking any connection = relevant"]
            ),
            KnowledgeNode(
                concept_id="evidence_403",
                name="Rule 403 Exclusion",
                subject="evidence",
                difficulty=3,
                rule_statement="Court may exclude relevant evidence if probative value substantially outweighed by unfair prejudice, confusion, or waste of time",
                elements=["Probative value", "Unfair prejudice", "Confusion", "Waste of time", "Substantially outweighed"],
                common_traps=["Thinking any prejudice triggers 403"]
            ),
            # Character Evidence
            KnowledgeNode(
                concept_id="evidence_character",
                name="Character Evidence",
                subject="evidence",
                difficulty=4,
                rule_statement="Generally inadmissible to prove conduct in conformity; exceptions for criminal defendant's character, victim's character, witness credibility",
                elements=["Propensity rule", "Criminal defendant opens door", "Victim character (self-defense)", "MIMIC exceptions"],
                common_traps=["Forgetting prosecution can't initiate character evidence", "Missing MIMIC exceptions"]
            ),
            KnowledgeNode(
                concept_id="evidence_habit",
                name="Habit & Routine Practice",
                subject="evidence",
                difficulty=3,
                rule_statement="Evidence of habit or routine practice admissible to prove conduct in conformity",
                elements=["Specific conduct", "Regular response", "Particular situation", "No corroboration required"],
                common_traps=["Confusing habit (admissible) with character (inadmissible)"]
            ),
            KnowledgeNode(
                concept_id="evidence_prior_acts",
                name="Prior Bad Acts (MIMIC)",
                subject="evidence",
                difficulty=4,
                rule_statement="Prior bad acts inadmissible for propensity but admissible for MIMIC: Motive, Intent, Mistake/accident (absence), Identity, Common plan",
                elements=["Not for propensity", "MIMIC purposes", "Notice requirement (criminal)", "FRE 404(b)"],
                common_traps=["Using for propensity", "Forgetting notice requirement"]
            ),
            # Hearsay
            KnowledgeNode(
                concept_id="evidence_hearsay",
                name="Hearsay",
                subject="evidence",
                difficulty=3,
                rule_statement="Hearsay is out-of-court statement offered for truth of matter asserted; inadmissible unless exception applies",
                elements=["Out of court", "Statement", "Offered for truth", "Person (not machine)", "Declarant"],
                common_traps=["Missing 'offered for truth' requirement"]
            ),
            KnowledgeNode(
                concept_id="evidence_hearsay_nonhearsay",
                name="Non-Hearsay Uses",
                subject="evidence",
                difficulty=4,
                rule_statement="Not hearsay if not offered for truth: effect on listener, verbal acts, impeachment, state of mind of speaker",
                elements=["Effect on listener", "Verbal acts (legally operative)", "Impeachment", "State of mind of speaker"],
                common_traps=["Thinking all out-of-court statements are hearsay"]
            ),
            KnowledgeNode(
                concept_id="evidence_hearsay_exceptions_availability",
                name="Hearsay Exceptions - Declarant Unavailable",
                subject="evidence",
                difficulty=4,
                rule_statement="Former testimony, dying declaration, statement against interest, forfeiture by wrongdoing require declarant unavailability",
                elements=["Former testimony", "Dying declaration", "Statement against interest", "Forfeiture", "Unavailability required"],
                common_traps=["Forgetting unavailability requirement", "Mixing up availability exceptions"]
            ),
            KnowledgeNode(
                concept_id="evidence_hearsay_exceptions_regardless",
                name="Hearsay Exceptions - Regardless of Availability",
                subject="evidence",
                difficulty=4,
                rule_statement="Present sense impression, excited utterance, state of mind, medical diagnosis, recorded recollection, business records, public records",
                elements=["Present sense impression", "Excited utterance", "Then-existing state of mind", "Medical diagnosis", "Business records"],
                common_traps=["Confusing time requirements for PSI vs. excited utterance"]
            ),
            KnowledgeNode(
                concept_id="evidence_confrontation",
                name="Confrontation Clause",
                subject="evidence",
                difficulty=4,
                rule_statement="In criminal cases, testimonial hearsay inadmissible unless declarant unavailable and defendant had prior opportunity to cross-examine",
                elements=["Criminal cases only", "Testimonial statements", "Unavailability", "Prior cross-examination opportunity"],
                common_traps=["Applying to non-testimonial statements", "Forgetting civil cases unaffected"]
            ),
            # Witnesses
            KnowledgeNode(
                concept_id="evidence_impeachment",
                name="Impeachment",
                subject="evidence",
                difficulty=3,
                rule_statement="Witness may be impeached by bias, prior inconsistent statement, character for truthfulness, sensory defects, contradiction",
                elements=["Bias/motive", "Prior inconsistent statement", "Character for untruthfulness", "Sensory defects", "Contradiction"],
                common_traps=["Forgetting extrinsic evidence limitations"]
            ),
            KnowledgeNode(
                concept_id="evidence_credibility",
                name="Witness Credibility",
                subject="evidence",
                difficulty=3,
                rule_statement="Character for truthfulness admissible only after credibility attacked; reputation or opinion form only",
                elements=["Attack first", "Reputation or opinion only", "No specific acts on direct", "Rehabilitation"],
                common_traps=["Thinking specific acts allowed on direct"]
            ),
            # Privileges
            KnowledgeNode(
                concept_id="evidence_privileges",
                name="Privileges",
                subject="evidence",
                difficulty=3,
                rule_statement="Attorney-client, spousal, psychotherapist-patient, clergy-penitent privileges; holder may assert",
                elements=["Attorney-client", "Spousal immunity", "Spousal confidential communications", "Waiver"],
                common_traps=["Confusing two spousal privileges"]
            ),
            # Authentication & Best Evidence
            KnowledgeNode(
                concept_id="evidence_authentication",
                name="Authentication",
                subject="evidence",
                difficulty=3,
                rule_statement="Evidence must be authenticated by showing it is what proponent claims",
                elements=["What it purports to be", "Low standard", "Witness testimony", "Self-authenticating documents"],
                common_traps=["Thinking high standard required"]
            ),
            KnowledgeNode(
                concept_id="evidence_best_evidence",
                name="Best Evidence Rule",
                subject="evidence",
                difficulty=3,
                rule_statement="Original writing required to prove content of writing; applies only when content at issue",
                elements=["Original required", "Content at issue", "Duplicates admissible", "Exceptions"],
                common_traps=["Applying when content not at issue"]
            ),
            # Expert Testimony
            KnowledgeNode(
                concept_id="evidence_expert_testimony",
                name="Expert Testimony",
                subject="evidence",
                difficulty=3,
                rule_statement="Expert may testify if specialized knowledge helps trier of fact, based on sufficient facts/data, reliable principles",
                elements=["Specialized knowledge", "Helpful to trier", "Sufficient basis", "Reliable methodology (Daubert)"],
                common_traps=["Forgetting Daubert reliability requirement"]
            ),
        ]
        for node in evidence:
            self.nodes[node.concept_id] = node

    # Continue with Constitutional Law...
    def _initialize_constitutional_law(self):
        """Initialize constitutional law with comprehensive coverage (18 concepts)"""
        conlaw = [
            # Federal Powers
            KnowledgeNode(
                concept_id="conlaw_commerce_clause",
                name="Commerce Clause",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Congress may regulate channels, instrumentalities, and activities substantially affecting interstate commerce",
                elements=["Channels", "Instrumentalities", "Substantial effects", "Economic activity"],
                common_traps=["Thinking non-economic activity sufficient"]
            ),
            KnowledgeNode(
                concept_id="conlaw_spending_power",
                name="Spending Power",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Congress may spend for general welfare and condition grants if related to federal interest, clear, not coercive",
                elements=["General welfare", "Related to federal interest", "Clear conditions", "Not coercive"],
                common_traps=["Thinking conditions must be for general welfare"]
            ),
            KnowledgeNode(
                concept_id="conlaw_tenth_amendment",
                name="Tenth Amendment & Commandeering",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Federal government cannot commandeer state legislative or executive officials to implement federal programs",
                elements=["Anti-commandeering", "State sovereignty", "Can regulate individuals", "Not coerced"],
                common_traps=["Thinking Tenth Amendment limits all federal power"]
            ),
            KnowledgeNode(
                concept_id="conlaw_supremacy",
                name="Supremacy Clause & Preemption",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Federal law supreme; preempts state law if express, field, or conflict preemption",
                elements=["Express preemption", "Field preemption", "Conflict preemption", "Obstacle to federal objectives"],
                common_traps=["Finding preemption without clear conflict"]
            ),
            # Individual Rights - Due Process
            KnowledgeNode(
                concept_id="conlaw_procedural_due_process",
                name="Procedural Due Process",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Deprivation of life, liberty, or property requires notice and opportunity to be heard",
                elements=["Life, liberty, or property", "State action", "Notice", "Hearing", "Mathews balancing"],
                common_traps=["Forgetting property includes entitlements"]
            ),
            KnowledgeNode(
                concept_id="conlaw_substantive_due_process",
                name="Substantive Due Process",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Fundamental rights get strict scrutiny; economic regulations get rational basis",
                elements=["Fundamental rights", "Strict scrutiny", "Rational basis", "Deep-rooted in history"],
                common_traps=["Applying strict scrutiny to non-fundamental rights"]
            ),
            # Equal Protection
            KnowledgeNode(
                concept_id="conlaw_equal_protection",
                name="Equal Protection Clause",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Race/national origin (strict), gender/legitimacy (intermediate), other (rational basis)",
                elements=["Suspect class (strict)", "Quasi-suspect (intermediate)", "Rational basis", "Discriminatory purpose"],
                common_traps=["Applying strict scrutiny without discriminatory purpose"]
            ),
            KnowledgeNode(
                concept_id="conlaw_strict_scrutiny",
                name="Strict Scrutiny",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Law must be necessary to achieve compelling government interest; narrow tailoring required",
                elements=["Compelling interest", "Necessary", "Narrowly tailored", "Least restrictive means"],
                common_traps=["Thinking important interest sufficient"]
            ),
            # First Amendment
            KnowledgeNode(
                concept_id="conlaw_free_speech",
                name="Free Speech - Content-Based Restrictions",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Content-based speech restrictions subject to strict scrutiny unless unprotected category",
                elements=["Content-based (strict scrutiny)", "Unprotected categories", "Incitement", "Fighting words", "Obscenity"],
                common_traps=["Missing content-based vs. content-neutral distinction"]
            ),
            KnowledgeNode(
                concept_id="conlaw_free_speech_neutral",
                name="Free Speech - Content-Neutral Restrictions",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Content-neutral restrictions (time, place, manner) valid if narrowly tailored to significant interest, leave open alternatives",
                elements=["Content-neutral", "Significant interest", "Narrowly tailored", "Ample alternatives", "Public forum analysis"],
                common_traps=["Applying strict scrutiny to content-neutral"]
            ),
            KnowledgeNode(
                concept_id="conlaw_free_speech_public_forum",
                name="Public Forum Doctrine",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Traditional public forums (strict scrutiny for content-based), limited public forums, non-public forums (reasonableness)",
                elements=["Traditional public forum", "Designated/limited public forum", "Non-public forum", "Viewpoint discrimination banned"],
                common_traps=["Thinking all government property is public forum"]
            ),
            KnowledgeNode(
                concept_id="conlaw_establishment",
                name="Establishment Clause",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Government cannot endorse religion; must have secular purpose, primary effect neither advancing nor inhibiting, no excessive entanglement",
                elements=["Secular purpose", "Primary effect", "No excessive entanglement", "Lemon test", "Coercion test"],
                common_traps=["Thinking any government acknowledgment of religion invalid"]
            ),
            KnowledgeNode(
                concept_id="conlaw_free_exercise",
                name="Free Exercise Clause",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Neutral laws of general applicability need only rational basis; targeted laws get strict scrutiny",
                elements=["Neutral law", "General applicability", "Not targeted", "Hybrid rights"],
                common_traps=["Applying strict scrutiny to all religious burdens"]
            ),
            # State Action
            KnowledgeNode(
                concept_id="conlaw_state_action",
                name="State Action Requirement",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Constitution limits government, not private actors; exceptions for public function, significant entanglement, judicial enforcement",
                elements=["Government actor", "Public function exception", "Significant state involvement", "Judicial enforcement"],
                common_traps=["Finding state action from mere licensing"]
            ),
            # Takings
            KnowledgeNode(
                concept_id="conlaw_takings",
                name="Takings Clause",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Government taking of private property requires just compensation; physical taking, regulatory taking, exaction",
                elements=["Physical taking", "Regulatory taking (Penn Central)", "Just compensation", "Public use"],
                common_traps=["Thinking all regulations are takings"]
            ),
            # Dormant Commerce Clause
            KnowledgeNode(
                concept_id="conlaw_dormant_commerce",
                name="Dormant Commerce Clause",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="State law invalid if discriminates against interstate commerce or unduly burdens it",
                elements=["Discrimination (strict scrutiny)", "Undue burden (Pike balancing)", "Market participant exception"],
                common_traps=["Missing market participant exception"]
            ),
            # Privileges & Immunities
            KnowledgeNode(
                concept_id="conlaw_privileges_immunities",
                name="Privileges & Immunities",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="State cannot discriminate against out-of-state citizens regarding fundamental rights unless substantial justification",
                elements=["Fundamental rights", "Citizens only (not corporations)", "Substantial justification required"],
                common_traps=["Applying to corporations"]
            ),
            # Separation of Powers
            KnowledgeNode(
                concept_id="conlaw_separation_powers",
                name="Separation of Powers",
                subject="constitutional_law",
                difficulty=3,
                rule_statement="Three branches with checks and balances; non-delegation doctrine, appointment/removal, executive privilege",
                elements=["Legislative power", "Executive power", "Judicial power", "Checks and balances"],
                common_traps=["Thinking non-delegation doctrine strictly applied"]
            ),
        ]
        for node in conlaw:
            self.nodes[node.concept_id] = node

    # I'll continue with the remaining subjects in the next part...
    # Due to length, showing pattern for remaining subjects abbreviated

    def _initialize_criminal_law(self):
        """Initialize criminal law with comprehensive coverage (17 concepts)"""
        crim_law = [
            # Elements
            KnowledgeNode(
                concept_id="crimlaw_actus_reus",
                name="Actus Reus",
                subject="criminal_law",
                difficulty=2,
                rule_statement="Voluntary physical act or omission where duty to act exists",
                elements=["Voluntary act", "Omission with legal duty", "Not mere thoughts", "Causation"],
                common_traps=["Thinking involuntary acts sufficient"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_mens_rea",
                name="Mens Rea",
                subject="criminal_law",
                difficulty=3,
                rule_statement="MPC: purposely, knowingly, recklessly, negligently; CL: specific intent, general intent, malice, strict liability",
                elements=["Specific intent", "General intent", "Malice", "Strict liability", "MPC hierarchy"],
                common_traps=["Confusing MPC with common law mens rea"]
            ),
            # Homicide
            KnowledgeNode(
                concept_id="crimlaw_murder",
                name="Murder",
                subject="criminal_law",
                difficulty=4,
                rule_statement="Unlawful killing with malice aforethought: intent to kill, intent to inflict serious bodily injury, depraved heart, felony murder",
                elements=["Malice aforethought", "Intent to kill", "Intent to inflict SBI", "Depraved heart", "Felony murder"],
                common_traps=["Missing depraved heart murder", "Forgetting felony murder limitations"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_felony_murder",
                name="Felony Murder",
                subject="criminal_law",
                difficulty=4,
                rule_statement="Death during commission of inherently dangerous felony; limitations: res gestae, foreseeability, agency theory vs. proximate cause",
                elements=["BARRK felonies", "Inherently dangerous", "During commission", "Res gestae", "Limitations"],
                common_traps=["Thinking all deaths during felonies qualify", "Missing merger doctrine"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_manslaughter",
                name="Voluntary & Involuntary Manslaughter",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Voluntary: killing in heat of passion; Involuntary: killing with criminal negligence or during unlawful act",
                elements=["Heat of passion", "Adequate provocation", "Criminal negligence", "Misdemeanor manslaughter"],
                common_traps=["Thinking any emotion = heat of passion"]
            ),
            # Other Crimes Against Person
            KnowledgeNode(
                concept_id="crimlaw_assault_battery",
                name="Assault & Battery",
                subject="criminal_law",
                difficulty=2,
                rule_statement="Battery: unlawful application of force; Assault: attempt to commit battery or intentional frightening",
                elements=["Battery (force)", "Assault (attempt or frighten)", "General intent crimes"],
                common_traps=["Confusing with tort definitions"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_rape",
                name="Rape & Sexual Assault",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Sexual intercourse without consent; lack of consent shown by force, threats, incapacity, or statute",
                elements=["Sexual intercourse", "Lack of consent", "Force or threats", "Incapacity", "Statutory rape (strict liability)"],
                common_traps=["Thinking mistake of age defense to statutory rape"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_kidnapping",
                name="Kidnapping & False Imprisonment",
                subject="criminal_law",
                difficulty=2,
                rule_statement="Kidnapping: unlawful confinement with movement or concealment; False imprisonment: unlawful confinement without movement",
                elements=["Confinement", "Asportation (kidnapping)", "Against victim's will"],
                common_traps=["Thinking any movement = kidnapping"]
            ),
            # Property Crimes
            KnowledgeNode(
                concept_id="crimlaw_larceny",
                name="Larceny",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Trespassory taking and carrying away of personal property of another with intent to permanently deprive",
                elements=["Trespassory taking", "Carrying away", "Personal property", "Of another", "Intent to permanently deprive"],
                common_traps=["Thinking borrowing = larceny", "Missing continuing trespass"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_robbery_burglary",
                name="Robbery & Burglary",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Robbery: larceny from person by force/intimidation; Burglary: breaking and entering dwelling of another at night with intent to commit felony",
                elements=["Robbery (larceny + force)", "Burglary (breaking + entering + dwelling + night + intent)", "Modern statutes"],
                common_traps=["Forgetting burglary requires intent at time of entry"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_theft_crimes",
                name="Embezzlement, False Pretenses, Receiving Stolen Property",
                subject="criminal_law",
                difficulty=4,
                rule_statement="Embezzlement: conversion of property lawfully possessed; False pretenses: obtaining title by false representation; RSP: receiving with knowledge",
                elements=["Embezzlement (lawful possession)", "False pretenses (title obtained)", "Larceny by trick (possession only)", "Receiving stolen property"],
                common_traps=["Confusing larceny by trick with false pretenses"]
            ),
            # Inchoate Crimes
            KnowledgeNode(
                concept_id="crimlaw_attempt",
                name="Attempt",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Specific intent to commit crime plus substantial step toward commission; defenses: legal impossibility (yes), factual impossibility (no)",
                elements=["Specific intent", "Substantial step", "Mere preparation insufficient", "Impossibility"],
                common_traps=["Thinking abandonment is defense"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_conspiracy",
                name="Conspiracy",
                subject="criminal_law",
                difficulty=4,
                rule_statement="Agreement between two or more to commit unlawful act; majority rule requires overt act; Pinkerton liability for crimes in furtherance",
                elements=["Agreement", "Two or more (majority rule)", "Overt act (majority)", "Specific intent", "No merger"],
                common_traps=["Thinking conspiracy merges", "Missing withdrawal requirements"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_solicitation",
                name="Solicitation",
                subject="criminal_law",
                difficulty=2,
                rule_statement="Asking, encouraging, or commanding another to commit crime with intent that crime be committed",
                elements=["Asking/encouraging", "Another person", "Specific intent", "Merges into attempt/completed crime"],
                common_traps=["Thinking it merges into conspiracy"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_accomplice_liability",
                name="Accomplice Liability",
                subject="criminal_law",
                difficulty=4,
                rule_statement="One who aids, abets, or encourages with intent that crime be committed is liable for that crime and foreseeable crimes",
                elements=["Aid, abet, or encourage", "Intent", "Liable for intended crime", "Liable for natural and probable consequences"],
                common_traps=["Thinking mere presence sufficient"]
            ),
            # Defenses
            KnowledgeNode(
                concept_id="crimlaw_self_defense",
                name="Self-Defense & Defense of Others",
                subject="criminal_law",
                difficulty=3,
                rule_statement="Reasonable belief of imminent unlawful force; force used must be reasonable; deadly force only if threat of serious bodily injury/death; no duty to retreat",
                elements=["Reasonable belief", "Imminent threat", "Proportional force", "Deadly force limitations", "Retreat (minority)"],
                common_traps=["Thinking aggressor can claim self-defense", "Missing imperfect self-defense"]
            ),
            KnowledgeNode(
                concept_id="crimlaw_other_defenses",
                name="Necessity, Duress, Intoxication, Insanity, Mistake",
                subject="criminal_law",
                difficulty=4,
                rule_statement="Necessity: lesser harm chosen; Duress: threat of death/SBI (not murder); Intoxication: negates specific intent; Insanity: M'Naghten, irresistible impulse, MPC, Durham",
                elements=["Necessity", "Duress", "Voluntary intoxication", "Involuntary intoxication", "Insanity tests", "Mistake of fact/law"],
                common_traps=["Thinking voluntary intoxication is complete defense", "Confusing insanity tests"]
            ),
        ]
        for node in crim_law:
            self.nodes[node.concept_id] = node

    def _initialize_criminal_procedure(self):
        """Initialize criminal procedure with comprehensive coverage (16 concepts)"""
        crim_pro = [
            # Fourth Amendment - Searches
            KnowledgeNode(
                concept_id="crimpro_fourth_amendment",
                name="Fourth Amendment Overview",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Protects against unreasonable searches and seizures; requires warrant based on probable cause or exception",
                elements=["Reasonable expectation of privacy", "Government action", "Warrant requirement", "Exceptions"],
                common_traps=["Missing standing requirement"]
            ),
            KnowledgeNode(
                concept_id="crimpro_searches",
                name="Searches & Reasonable Expectation of Privacy",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Search occurs when government violates reasonable expectation of privacy; no REP in things exposed to public, open fields, or third parties",
                elements=["Katz test", "No REP in public", "Open fields", "Plain view", "Third-party doctrine"],
                common_traps=["Thinking curtilage = open fields"]
            ),
            KnowledgeNode(
                concept_id="crimpro_warrant",
                name="Warrant Requirement",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Warrant requires probable cause, particularity, issued by neutral magistrate; defects may be saved by good faith exception",
                elements=["Probable cause", "Particularity", "Neutral magistrate", "Good faith exception"],
                common_traps=["Forgetting particularity requirement"]
            ),
            KnowledgeNode(
                concept_id="crimpro_warrant_exceptions",
                name="Warrant Exceptions",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="SILA: Search incident to arrest, Inventory search, Exigent circumstances, Automobile exception, Consent, Plain view, Stop and frisk",
                elements=["SILA", "Automobile exception", "Consent", "Exigent circumstances", "Plain view", "Stop and frisk"],
                common_traps=["Thinking searches of car always allowed", "Missing scope limitations"]
            ),
            KnowledgeNode(
                concept_id="crimpro_exclusionary_rule",
                name="Exclusionary Rule & Fruit of Poisonous Tree",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Evidence from unconstitutional search excluded; fruit also excluded unless independent source, inevitable discovery, or attenuated",
                elements=["Exclusionary rule", "Fruit of poisonous tree", "Independent source", "Inevitable discovery", "Attenuation"],
                common_traps=["Thinking exclusionary rule applies to all violations"]
            ),
            # Fourth Amendment - Seizures
            KnowledgeNode(
                concept_id="crimpro_seizures",
                name="Seizures & Arrests",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Arrest requires probable cause; warrant required for home arrest absent exigency; Terry stop requires reasonable suspicion",
                elements=["Arrest (probable cause)", "Terry stop (reasonable suspicion)", "Warrant for home arrest", "Pretextual stops OK"],
                common_traps=["Thinking warrant always required for arrest"]
            ),
            KnowledgeNode(
                concept_id="crimpro_stop_frisk",
                name="Stop & Frisk (Terry)",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Brief investigatory stop requires reasonable suspicion; frisk requires reasonable belief of armed and dangerous",
                elements=["Reasonable suspicion", "Brief detention", "Frisk for weapons only", "Plain feel doctrine"],
                common_traps=["Thinking reasonable suspicion = probable cause"]
            ),
            # Fifth Amendment
            KnowledgeNode(
                concept_id="crimpro_miranda",
                name="Miranda Warnings",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Custodial interrogation requires warnings: right to silence, anything said used against you, right to attorney, appointed if indigent",
                elements=["Custody", "Interrogation", "Warnings required", "Waiver must be knowing and voluntary", "Invocation"],
                common_traps=["Thinking Miranda required for all police questioning"]
            ),
            KnowledgeNode(
                concept_id="crimpro_self_incrimination",
                name="Fifth Amendment Privilege Against Self-Incrimination",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="No person compelled to be witness against himself; applies to testimonial evidence only, not physical evidence",
                elements=["Testimonial only", "Not physical evidence", "Must be compelled", "Grant of immunity"],
                common_traps=["Thinking applies to physical evidence"]
            ),
            KnowledgeNode(
                concept_id="crimpro_double_jeopardy",
                name="Double Jeopardy",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="No person tried twice for same offense; jeopardy attaches when jury sworn (jury trial) or first witness sworn (bench trial)",
                elements=["Same offense test", "Jeopardy attaches", "Exceptions: mistrial, appeal by defendant, separate sovereigns"],
                common_traps=["Thinking retrial after mistrial violates DJ"]
            ),
            # Sixth Amendment
            KnowledgeNode(
                concept_id="crimpro_right_to_counsel",
                name="Sixth Amendment Right to Counsel",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Attaches at initiation of adversarial proceedings; applies to all critical stages; deliberate elicitation triggers",
                elements=["Attaches at formal charges", "Critical stages", "Deliberate elicitation", "Offense-specific"],
                common_traps=["Confusing with Miranda right to counsel", "Thinking applies pre-charge"]
            ),
            KnowledgeNode(
                concept_id="crimpro_confrontation",
                name="Confrontation Clause",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Criminal defendant has right to confront witnesses; testimonial hearsay inadmissible unless declarant unavailable and prior cross-examination",
                elements=["Criminal cases only", "Testimonial statements", "Unavailability", "Prior opportunity to cross-examine"],
                common_traps=["Applying to non-testimonial hearsay"]
            ),
            # Pretrial
            KnowledgeNode(
                concept_id="crimpro_pretrial",
                name="Pretrial Procedures",
                subject="criminal_procedure",
                difficulty=2,
                rule_statement="Complaint, initial appearance, preliminary hearing (PC determination), grand jury (indictment), arraignment",
                elements=["Gerstein hearing (48 hours)", "Preliminary hearing", "Grand jury", "Arraignment", "Bail"],
                common_traps=["Thinking preliminary hearing required in all cases"]
            ),
            KnowledgeNode(
                concept_id="crimpro_lineups",
                name="Lineups & Identifications",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Post-charge lineups trigger right to counsel; unnecessarily suggestive procedures may be excluded under Due Process",
                elements=["Right to counsel (post-charge)", "Suggestiveness", "Due process test", "Independent source"],
                common_traps=["Thinking right to counsel applies to pre-charge lineups"]
            ),
            # Trial & Post-Conviction
            KnowledgeNode(
                concept_id="crimpro_jury_trial",
                name="Jury Trial Right",
                subject="criminal_procedure",
                difficulty=2,
                rule_statement="Right to jury trial for serious offenses (>6 months); 6 jurors minimum; unanimous verdict required in federal, state 12-person juries",
                elements=["Serious offenses", "6 jurors minimum", "Unanimity", "Fair cross-section", "Peremptory challenges"],
                common_traps=["Thinking jury required for petty offenses"]
            ),
            KnowledgeNode(
                concept_id="crimpro_ineffective_assistance",
                name="Ineffective Assistance of Counsel",
                subject="criminal_procedure",
                difficulty=3,
                rule_statement="Two-prong Strickland test: deficient performance and prejudice (reasonable probability of different outcome)",
                elements=["Deficient performance", "Prejudice", "Reasonable probability", "Objective standard"],
                common_traps=["Thinking any mistake = IAC"]
            ),
        ]
        for node in crim_pro:
            self.nodes[node.concept_id] = node

    def _initialize_civil_procedure(self):
        """Initialize civil procedure with comprehensive coverage (15 concepts)"""
        civ_pro = [
            # Jurisdiction
            KnowledgeNode(
                concept_id="civpro_subject_matter_jurisdiction",
                name="Subject Matter Jurisdiction",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Federal courts have limited jurisdiction: federal question or diversity; diversity requires >$75K and complete diversity",
                elements=["Federal question", "Diversity jurisdiction", "Complete diversity", "Amount in controversy", "Supplemental jurisdiction"],
                common_traps=["Forgetting complete diversity rule", "Thinking federal courts have general jurisdiction"]
            ),
            KnowledgeNode(
                concept_id="civpro_personal_jurisdiction",
                name="Personal Jurisdiction",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Court must have power over defendant: general jurisdiction (at home), specific jurisdiction (minimum contacts + reasonableness), or consent",
                elements=["General jurisdiction", "Specific jurisdiction", "Minimum contacts", "Purposeful availment", "Reasonableness"],
                common_traps=["Forgetting 'arise out of' requirement for specific jurisdiction"]
            ),
            KnowledgeNode(
                concept_id="civpro_venue",
                name="Venue",
                subject="civil_procedure",
                difficulty=2,
                rule_statement="Proper venue: where any defendant resides (if all in same state), where substantial part of events occurred, or fallback",
                elements=["Defendant's residence", "Events or property", "Fallback", "Transfer", "Forum non conveniens"],
                common_traps=["Confusing venue with jurisdiction"]
            ),
            KnowledgeNode(
                concept_id="civpro_erie",
                name="Erie Doctrine",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Federal courts apply federal procedural law and state substantive law; if conflict, use RDA test or direct collision",
                elements=["Substantive vs. procedural", "State law in diversity", "Federal Rule applies if valid", "RDA test"],
                common_traps=["Thinking federal courts always apply federal law"]
            ),
            # Pleadings
            KnowledgeNode(
                concept_id="civpro_pleadings",
                name="Pleadings - Complaint & Answer",
                subject="civil_procedure",
                difficulty=2,
                rule_statement="Complaint requires short and plain statement showing entitlement to relief; Answer must respond to each allegation",
                elements=["Notice pleading", "Plausibility (Twombly/Iqbal)", "Answer", "Affirmative defenses", "Rule 11 sanctions"],
                common_traps=["Thinking detailed facts required in complaint"]
            ),
            KnowledgeNode(
                concept_id="civpro_rule_12b",
                name="Rule 12(b) Motions",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Pre-answer motions: 12(b)(1) SMJ, (2) PJ, (3) venue, (4) process, (5) service, (6) failure to state claim, (7) failure to join party",
                elements=["Waivable defenses (2-5)", "Non-waivable (SMJ, FtSC)", "12(b)(6) motion", "Convert to summary judgment"],
                common_traps=["Thinking all 12(b) defenses waived if not raised"]
            ),
            KnowledgeNode(
                concept_id="civpro_joinder",
                name="Joinder of Claims & Parties",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Permissive joinder of parties if same transaction/occurrence and common question; claims freely joined",
                elements=["Permissive party joinder", "Compulsory joinder (Rule 19)", "Claim joinder (Rule 18)", "Counterclaims", "Cross-claims"],
                common_traps=["Confusing permissive with compulsory joinder"]
            ),
            KnowledgeNode(
                concept_id="civpro_class_actions",
                name="Class Actions",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Requirements: numerosity, commonality, typicality, adequate representation; plus Rule 23(b) type",
                elements=["Numerosity", "Commonality", "Typicality", "Adequate representation", "23(b) categories", "Notice"],
                common_traps=["Forgetting 23(b) requirement in addition to 23(a)"]
            ),
            # Discovery
            KnowledgeNode(
                concept_id="civpro_discovery",
                name="Discovery",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Parties may discover non-privileged information relevant to claims or defenses; proportionality required",
                elements=["Scope", "Relevance", "Proportionality", "Privileged matter", "Work product", "Required disclosures"],
                common_traps=["Thinking attorney work product absolutely protected"]
            ),
            KnowledgeNode(
                concept_id="civpro_discovery_devices",
                name="Discovery Devices",
                subject="civil_procedure",
                difficulty=2,
                rule_statement="Depositions, interrogatories (parties only), requests for production, requests for admission, physical/mental exams",
                elements=["Depositions", "Interrogatories", "RFPs", "RFAs", "Physical exams (good cause)"],
                common_traps=["Thinking interrogatories available for non-parties"]
            ),
            # Summary Judgment & Trial
            KnowledgeNode(
                concept_id="civpro_summary_judgment",
                name="Summary Judgment",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Granted when no genuine dispute of material fact and movant entitled to judgment as matter of law",
                elements=["No genuine dispute", "Material fact", "Judgment as matter of law", "Burden on movant", "Non-movant's burden"],
                common_traps=["Thinking any factual dispute defeats SJ"]
            ),
            KnowledgeNode(
                concept_id="civpro_jury_trial",
                name="Right to Jury Trial",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Seventh Amendment preserves right to jury in suits at common law (legal claims); no right for equitable claims",
                elements=["Legal vs. equitable", "Historical test", "Demand required", "Jury size (6-12)", "Unanimity not required"],
                common_traps=["Thinking jury right exists for all claims"]
            ),
            KnowledgeNode(
                concept_id="civpro_jmol",
                name="Judgment as Matter of Law (JMOL/JNOV)",
                subject="civil_procedure",
                difficulty=3,
                rule_statement="Court may grant JMOL if reasonable jury could not find for non-moving party; renewed JMOL after verdict",
                elements=["During trial", "After verdict (renewed JMOL)", "Legal sufficiency", "View evidence in light favorable to non-movant"],
                common_traps=["Thinking renewed JMOL available without pre-verdict motion"]
            ),
            # Preclusion
            KnowledgeNode(
                concept_id="civpro_res_judicata",
                name="Claim Preclusion (Res Judicata)",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Final judgment on merits bars re-litigation of same claim by same parties; claim includes all grounds arising from same transaction",
                elements=["Final judgment", "On the merits", "Same claim", "Same parties (or privies)", "Transactional test"],
                common_traps=["Thinking only identical claims precluded"]
            ),
            KnowledgeNode(
                concept_id="civpro_collateral_estoppel",
                name="Issue Preclusion (Collateral Estoppel)",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Issue actually litigated and necessarily decided in prior action cannot be re-litigated",
                elements=["Actually litigated", "Necessarily decided", "Full and fair opportunity", "Mutuality (not always required)"],
                common_traps=["Applying when issue not actually litigated"]
            ),
        ]
        for node in civ_pro:
            self.nodes[node.concept_id] = node

    def _initialize_property(self):
        """Initialize property with comprehensive coverage (20 concepts)"""
        property_law = [
            # Estates
            KnowledgeNode(
                concept_id="property_present_estates",
                name="Present Estates",
                subject="property",
                difficulty=3,
                rule_statement="Fee simple absolute (no limitations), fee tail (abolished), life estate, fee simple determinable, fee simple subject to condition subsequent, fee simple subject to executory limitation",
                elements=["Fee simple absolute", "Life estate", "Fee simple determinable", "Fee simple subject to condition subsequent", "Defeasible fees"],
                common_traps=["Confusing FSD with FSSCS"]
            ),
            KnowledgeNode(
                concept_id="property_future_interests",
                name="Future Interests",
                subject="property",
                difficulty=4,
                rule_statement="Reversions, possibilities of reverter, rights of entry in grantor; remainders and executory interests in grantees",
                elements=["Reversion", "Possibility of reverter", "Right of entry", "Vested remainder", "Contingent remainder", "Executory interest"],
                common_traps=["Confusing vested vs. contingent remainders"]
            ),
            KnowledgeNode(
                concept_id="property_rule_against_perpetuities",
                name="Rule Against Perpetuities",
                subject="property",
                difficulty=4,
                rule_statement="Interest must vest if at all within 21 years after life in being at creation; applies to contingent remainders, executory interests, certain options",
                elements=["Life in being", "21 years", "Must vest or fail", "What RAP applies to", "Charity exception"],
                common_traps=["Applying RAP to vested interests", "Forgetting charity-to-charity exception"]
            ),
            # Concurrent Ownership
            KnowledgeNode(
                concept_id="property_concurrent_ownership",
                name="Concurrent Ownership",
                subject="property",
                difficulty=3,
                rule_statement="Joint tenancy (right of survivorship, four unities), tenancy in common (no survivorship), tenancy by entirety (married couples)",
                elements=["Joint tenancy", "Four unities", "Right of survivorship", "Tenancy in common", "Severance"],
                common_traps=["Thinking TIC has survivorship", "Missing severance methods"]
            ),
            # Landlord-Tenant
            KnowledgeNode(
                concept_id="property_leases",
                name="Leasehold Estates",
                subject="property",
                difficulty=3,
                rule_statement="Term of years, periodic tenancy, tenancy at will, tenancy at sufferance; different termination rules",
                elements=["Term of years", "Periodic tenancy", "Tenancy at will", "Tenancy at sufferance", "Notice requirements"],
                common_traps=["Confusing termination requirements"]
            ),
            KnowledgeNode(
                concept_id="property_landlord_tenant_duties",
                name="Landlord-Tenant Duties",
                subject="property",
                difficulty=3,
                rule_statement="Landlord: duty to deliver possession, implied warranty of habitability, duty to repair; Tenant: duty to pay rent, duty not to waste",
                elements=["Delivery of possession", "Implied warranty of habitability", "Quiet enjoyment", "Actual vs. constructive eviction", "Waste"],
                common_traps=["Thinking landlord always has duty to repair"]
            ),
            KnowledgeNode(
                concept_id="property_assignments_subleases",
                name="Assignments & Subleases",
                subject="property",
                difficulty=3,
                rule_statement="Assignment: full transfer, assignee in privity of estate with landlord; Sublease: partial transfer, no privity",
                elements=["Assignment vs. sublease", "Privity of estate", "Privity of contract", "Landlord consent clauses"],
                common_traps=["Confusing assignment with sublease"]
            ),
            # Easements & Covenants
            KnowledgeNode(
                concept_id="property_easements",
                name="Easements",
                subject="property",
                difficulty=4,
                rule_statement="Creation: express grant/reservation, implication, necessity, prescription; types: appurtenant vs. in gross, affirmative vs. negative",
                elements=["Express", "Implied", "Necessity", "Prescription", "Appurtenant vs. in gross", "Termination"],
                common_traps=["Thinking easements in gross can't be transferred"]
            ),
            KnowledgeNode(
                concept_id="property_covenants",
                name="Real Covenants & Equitable Servitudes",
                subject="property",
                difficulty=4,
                rule_statement="Real covenant: writing, intent, touch and concern, privity; Equitable servitude: writing (or implied), intent, touch and concern, notice",
                elements=["Real covenant requirements", "Horizontal/vertical privity", "Equitable servitude", "Notice", "Touch and concern"],
                common_traps=["Forgetting notice requirement for equitable servitudes"]
            ),
            # Adverse Possession
            KnowledgeNode(
                concept_id="property_adverse_possession",
                name="Adverse Possession",
                subject="property",
                difficulty=3,
                rule_statement="Continuous, open and notorious, actual, exclusive, hostile possession for statutory period; tacking allowed",
                elements=["Continuous", "Open and notorious", "Actual", "Exclusive", "Hostile", "Statutory period", "Tacking"],
                common_traps=["Thinking permission defeats AP", "Missing tacking rules"]
            ),
            # Land Sale Contracts
            KnowledgeNode(
                concept_id="property_land_sale_contracts",
                name="Land Sale Contracts",
                subject="property",
                difficulty=3,
                rule_statement="Statute of frauds requires writing; marketable title required unless stated; equitable conversion doctrine",
                elements=["Statute of frauds", "Marketable title", "Equitable conversion", "Risk of loss", "Time of performance"],
                common_traps=["Thinking perfect title required"]
            ),
            KnowledgeNode(
                concept_id="property_marketable_title",
                name="Marketable Title",
                subject="property",
                difficulty=3,
                rule_statement="Title free from reasonable doubt; defects: gaps in chain, encumbrances, zoning violations",
                elements=["Free from reasonable doubt", "Chain of title", "Encumbrances", "Zoning", "Merger doctrine"],
                common_traps=["Thinking any defect = unmarketable"]
            ),
            KnowledgeNode(
                concept_id="property_deeds",
                name="Deeds & Delivery",
                subject="property",
                difficulty=3,
                rule_statement="General warranty deed, special warranty deed, quitclaim deed; delivery required (intent to pass title presently)",
                elements=["Types of deeds", "Covenants of title", "Delivery", "Intent", "Acceptance"],
                common_traps=["Thinking physical transfer required for delivery"]
            ),
            # Recording Acts
            KnowledgeNode(
                concept_id="property_recording_acts",
                name="Recording Acts",
                subject="property",
                difficulty=4,
                rule_statement="Race: first to record wins; Notice: later BFP wins; Race-notice: later BFP who records first wins",
                elements=["Race", "Notice", "Race-notice", "Bona fide purchaser", "Value", "Notice (actual, inquiry, record)"],
                common_traps=["Confusing notice with race-notice", "Forgetting inquiry notice"]
            ),
            KnowledgeNode(
                concept_id="property_bona_fide_purchaser",
                name="Bona Fide Purchaser",
                subject="property",
                difficulty=3,
                rule_statement="Purchaser for value without notice (actual, record, or inquiry) of prior interest",
                elements=["Purchaser", "Value", "Without notice", "Types of notice", "Shelter rule"],
                common_traps=["Thinking donee can be BFP"]
            ),
            # Mortgages
            KnowledgeNode(
                concept_id="property_mortgages",
                name="Mortgages",
                subject="property",
                difficulty=3,
                rule_statement="Security interest in land; foreclosure required; deficiency judgment if proceeds insufficient; redemption rights",
                elements=["Purchase money mortgage", "Foreclosure", "Deficiency judgment", "Redemption", "Priority", "Assumption vs. subject to"],
                common_traps=["Confusing assumption with subject to"]
            ),
            # Takings
            KnowledgeNode(
                concept_id="property_takings",
                name="Takings",
                subject="property",
                difficulty=4,
                rule_statement="Government taking requires just compensation; physical taking, regulatory taking (Penn Central factors), temporary taking",
                elements=["Physical taking", "Regulatory taking", "Public use", "Just compensation", "Penn Central factors"],
                common_traps=["Thinking all regulations are takings"]
            ),
            # Zoning
            KnowledgeNode(
                concept_id="property_zoning",
                name="Zoning",
                subject="property",
                difficulty=2,
                rule_statement="Government land use regulation; non-conforming uses grandfathered; variances for hardship; special use permits",
                elements=["Non-conforming uses", "Variance", "Special exception/conditional use", "Spot zoning"],
                common_traps=["Thinking non-conforming uses can expand"]
            ),
            # Water Rights
            KnowledgeNode(
                concept_id="property_water_rights",
                name="Water Rights",
                subject="property",
                difficulty=3,
                rule_statement="Riparian rights (reasonable use), prior appropriation (first in time, first in right), groundwater",
                elements=["Riparian doctrine", "Prior appropriation", "Natural flow vs. reasonable use", "Groundwater"],
                common_traps=["Confusing riparian with prior appropriation"]
            ),
            # Fixtures
            KnowledgeNode(
                concept_id="property_fixtures",
                name="Fixtures",
                subject="property",
                difficulty=2,
                rule_statement="Chattel becomes fixture if annexed to realty with intent to be permanent; tests: annexation, adaptation, intent",
                elements=["Annexation", "Adaptation", "Intent", "Trade fixtures exception"],
                common_traps=["Thinking any attached item is fixture"]
            ),
        ]
        for node in property_law:
            self.nodes[node.concept_id] = node

    def _initialize_family_law(self):
        """Initialize family law with comprehensive coverage (10 concepts)"""
        family = [
            # Marriage
            KnowledgeNode(
                concept_id="family_marriage_requirements",
                name="Marriage Requirements & Validity",
                subject="family_law",
                difficulty=2,
                rule_statement="Valid marriage requires legal capacity, consent, no impediments; common law marriage recognized in some states",
                elements=["Legal capacity (age, mental)", "Consent", "No impediments", "License and ceremony", "Common law marriage"],
                common_traps=["Thinking common law marriage recognized everywhere"]
            ),
            KnowledgeNode(
                concept_id="family_premarital_agreements",
                name="Premarital Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Valid if voluntary, full disclosure, not unconscionable; cannot limit child support",
                elements=["Voluntary execution", "Full disclosure", "Not unconscionable", "Cannot waive child support", "Writing required"],
                common_traps=["Thinking prenups can limit child support"]
            ),
            # Divorce
            KnowledgeNode(
                concept_id="family_grounds_for_divorce",
                name="Grounds for Divorce",
                subject="family_law",
                difficulty=2,
                rule_statement="No-fault (irreconcilable differences, separation) or fault (adultery, cruelty, desertion)",
                elements=["No-fault divorce", "Irreconcilable differences", "Separation period", "Fault grounds", "Jurisdiction"],
                common_traps=["Thinking fault affects property division in all states"]
            ),
            KnowledgeNode(
                concept_id="family_property_division",
                name="Property Division",
                subject="family_law",
                difficulty=3,
                rule_statement="Community property (50/50 split) or equitable distribution (fair, not necessarily equal)",
                elements=["Community property", "Equitable distribution", "Marital vs. separate property", "Commingling", "Transmutation"],
                common_traps=["Confusing community property with equitable distribution"]
            ),
            KnowledgeNode(
                concept_id="family_spousal_support",
                name="Spousal Support/Alimony",
                subject="family_law",
                difficulty=3,
                rule_statement="Based on need, ability to pay, length of marriage, standard of living; modifiable upon material change",
                elements=["Need", "Ability to pay", "Duration", "Modification", "Termination (remarriage, death)"],
                common_traps=["Thinking alimony always permanent"]
            ),
            # Children
            KnowledgeNode(
                concept_id="family_child_custody",
                name="Child Custody",
                subject="family_law",
                difficulty=3,
                rule_statement="Best interests of child standard; legal vs. physical custody; joint vs. sole custody",
                elements=["Best interests", "Legal custody", "Physical custody", "Joint vs. sole", "Modification (substantial change)"],
                common_traps=["Thinking parent preference controls"]
            ),
            KnowledgeNode(
                concept_id="family_child_support",
                name="Child Support",
                subject="family_law",
                difficulty=2,
                rule_statement="Based on guidelines considering income and needs; modifiable upon material change; cannot be waived",
                elements=["Income-based guidelines", "Both parents' income", "Cannot be waived", "Modification", "Duration (age of majority)"],
                common_traps=["Thinking parents can waive child support"]
            ),
            KnowledgeNode(
                concept_id="family_parentage",
                name="Parentage & Paternity",
                subject="family_law",
                difficulty=3,
                rule_statement="Presumptions: marital presumption, acknowledgment, genetic testing; best interests of child",
                elements=["Marital presumption", "Acknowledgment", "Genetic testing", "Equitable parent doctrine", "UPA"],
                common_traps=["Thinking genetic testing always determinative"]
            ),
            # Adoption
            KnowledgeNode(
                concept_id="family_adoption",
                name="Adoption",
                subject="family_law",
                difficulty=2,
                rule_statement="Consent required (parents and child if over certain age); terminates biological parents' rights; creates parent-child relationship",
                elements=["Consent required", "Termination of parental rights", "Best interests", "Stepparent adoption", "Interstate adoption"],
                common_traps=["Thinking biological father's consent always required"]
            ),
            # Domestic Violence
            KnowledgeNode(
                concept_id="family_domestic_violence",
                name="Domestic Violence & Protective Orders",
                subject="family_law",
                difficulty=2,
                rule_statement="Restraining orders available; may affect custody; abuse includes physical, emotional, financial",
                elements=["Types of abuse", "Restraining orders", "Emergency orders", "Effect on custody", "Violation consequences"],
                common_traps=["Thinking only physical abuse qualifies"]
            ),
        ]
        for node in family:
            self.nodes[node.concept_id] = node

    def _initialize_trusts_estates(self):
        """Initialize trusts & estates with comprehensive coverage (12 concepts)"""
        trusts_estates = [
            # Wills
            KnowledgeNode(
                concept_id="trusts_will_execution",
                name="Will Execution & Formalities",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Valid will requires testamentary intent, capacity, writing signed by testator, two witnesses; holographic and nuncupative wills in some states",
                elements=["Testamentary intent", "Capacity", "Writing", "Signature", "Witnesses", "Holographic wills"],
                common_traps=["Thinking witnesses must know contents"]
            ),
            KnowledgeNode(
                concept_id="trusts_will_revocation",
                name="Will Revocation",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Revoked by subsequent will, physical act, or operation of law (divorce, pretermitted children)",
                elements=["Subsequent instrument", "Physical act", "Divorce revokes gifts to spouse", "Dependent relative revocation", "Revival"],
                common_traps=["Thinking partial physical destruction revokes entire will"]
            ),
            KnowledgeNode(
                concept_id="trusts_intestacy",
                name="Intestate Succession",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Spouse and descendants take priority; per stirpes vs. per capita distribution",
                elements=["Surviving spouse share", "Descendants", "Per stirpes", "Per capita at each generation", "Ancestors and collaterals"],
                common_traps=["Confusing per stirpes with per capita"]
            ),
            KnowledgeNode(
                concept_id="trusts_will_contests",
                name="Will Contests",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Grounds: lack of capacity, undue influence, fraud, improper execution; no-contest clauses enforceable",
                elements=["Testamentary capacity", "Undue influence", "Fraud", "Duress", "Insane delusion", "No-contest clause"],
                common_traps=["Thinking mere eccentricity = lack of capacity"]
            ),
            # Trusts
            KnowledgeNode(
                concept_id="trusts_creation",
                name="Trust Creation",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Requires settlor with capacity, intent, identifiable beneficiaries, trust property (res), valid purpose",
                elements=["Settlor", "Intent", "Beneficiaries", "Res", "Valid purpose", "Statute of frauds (land)"],
                common_traps=["Thinking precatory language creates trust"]
            ),
            KnowledgeNode(
                concept_id="trusts_types",
                name="Types of Trusts",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Inter vivos vs. testamentary; revocable vs. irrevocable; charitable vs. private; express, resulting, constructive",
                elements=["Inter vivos", "Testamentary", "Revocable", "Irrevocable", "Charitable", "Resulting", "Constructive"],
                common_traps=["Thinking all trusts irrevocable"]
            ),
            KnowledgeNode(
                concept_id="trusts_charitable",
                name="Charitable Trusts",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Must have charitable purpose; no identifiable beneficiaries required; cy pres doctrine applies; RAP doesn't apply",
                elements=["Charitable purpose", "No beneficiaries required", "Cy pres", "RAP exception", "Attorney general enforcement"],
                common_traps=["Applying RAP to charitable trusts"]
            ),
            KnowledgeNode(
                concept_id="trusts_trustee_duties",
                name="Trustee Duties",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Duty of loyalty, duty of care (prudent investor rule), duty to inform beneficiaries, duty not to commingle",
                elements=["Duty of loyalty", "Prudent investor rule", "Duty to inform", "No self-dealing", "No commingling"],
                common_traps=["Thinking trustee can profit from position"]
            ),
            KnowledgeNode(
                concept_id="trusts_modification_termination",
                name="Trust Modification & Termination",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Settlor can modify/revoke if revocable; beneficiaries can terminate if all consent and no material purpose; court modification via cy pres or changed circumstances",
                elements=["Revocable trusts", "Beneficiary consent", "Material purpose test", "Cy pres", "Changed circumstances"],
                common_traps=["Thinking beneficiaries can always terminate"]
            ),
            # Nonprobate Transfers
            KnowledgeNode(
                concept_id="trusts_nonprobate",
                name="Nonprobate Transfers",
                subject="trusts_estates",
                difficulty=2,
                rule_statement="Joint tenancy, life insurance, POD/TOD accounts, inter vivos trusts avoid probate",
                elements=["Joint tenancy with right of survivorship", "Life insurance", "Payable on death", "Transfer on death", "Inter vivos trusts"],
                common_traps=["Thinking all transfers go through probate"]
            ),
            # Future Interests
            KnowledgeNode(
                concept_id="trusts_class_gifts",
                name="Class Gifts & Rule of Convenience",
                subject="trusts_estates",
                difficulty=3,
                rule_statement="Class closes when any member can demand distribution; rule of convenience vs. natural closing",
                elements=["Class gift", "Rule of convenience", "Natural closing", "After-born class members"],
                common_traps=["Thinking class never closes early"]
            ),
            # Powers
            KnowledgeNode(
                concept_id="trusts_powers_of_appointment",
                name="Powers of Appointment",
                subject="trusts_estates",
                difficulty=4,
                rule_statement="General power: appointee can appoint to self, estate, creditors; special power: limited class; RAP applies to special powers",
                elements=["General power", "Special/limited power", "Donor", "Donee", "Appointees", "Exercise", "RAP"],
                common_traps=["Confusing general with special powers"]
            ),
        ]
        for node in trusts_estates:
            self.nodes[node.concept_id] = node

    def _initialize_business_associations(self):
        """Initialize business associations with comprehensive coverage (11 concepts)"""
        biz_assoc = [
            # Agency
            KnowledgeNode(
                concept_id="biz_agency",
                name="Agency Formation & Authority",
                subject="business_associations",
                difficulty=3,
                rule_statement="Agency: principal manifests assent for agent to act on principal's behalf subject to control; authority: actual, apparent, inherent",
                elements=["Manifestation of assent", "Control", "Actual authority", "Apparent authority", "Inherent authority", "Ratification"],
                common_traps=["Thinking independent contractor is agent"]
            ),
            KnowledgeNode(
                concept_id="biz_agency_liability",
                name="Principal & Agent Liability",
                subject="business_associations",
                difficulty=3,
                rule_statement="Principal liable for agent's authorized acts and torts within scope; agent liable if no disclosed principal or exceeds authority",
                elements=["Disclosed principal", "Undisclosed principal", "Scope of employment", "Frolic vs. detour", "Agent's liability"],
                common_traps=["Thinking principal never liable for agent torts"]
            ),
            # Partnerships
            KnowledgeNode(
                concept_id="biz_general_partnership",
                name="General Partnership",
                subject="business_associations",
                difficulty=3,
                rule_statement="Association of two or more to carry on business for profit; no formalities required; partners jointly and severally liable",
                elements=["Association", "For profit", "No formalities", "Joint and several liability", "Fiduciary duties", "Equal management"],
                common_traps=["Thinking partnership requires written agreement"]
            ),
            KnowledgeNode(
                concept_id="biz_partnership_property",
                name="Partnership Property & Interests",
                subject="business_associations",
                difficulty=3,
                rule_statement="Partnership owns property; partners have transferable economic interest but non-transferable management rights",
                elements=["Partnership property", "Partner's interest", "Transferability", "Charging order", "No partition right"],
                common_traps=["Thinking partners own partnership property individually"]
            ),
            KnowledgeNode(
                concept_id="biz_partnership_dissolution",
                name="Partnership Dissolution",
                subject="business_associations",
                difficulty=3,
                rule_statement="Dissolution doesn't terminate partnership; winding up follows; wrongful dissolution triggers damages",
                elements=["Dissolution events", "Winding up", "Continuation agreement", "Wrongful dissolution", "Buyout rights"],
                common_traps=["Thinking dissolution immediately terminates partnership"]
            ),
            KnowledgeNode(
                concept_id="biz_limited_partnership",
                name="Limited Partnership & LLPs",
                subject="business_associations",
                difficulty=3,
                rule_statement="LP: general partners manage, limited partners passive investors with limited liability; LLP: all partners have limited liability",
                elements=["General vs. limited partners", "Limited liability", "Control rule", "LLP registration", "Fiduciary duties"],
                common_traps=["Thinking limited partner who participates loses limited liability (modern law changed)"]
            ),
            # Corporations
            KnowledgeNode(
                concept_id="biz_incorporation",
                name="Incorporation & Corporate Formation",
                subject="business_associations",
                difficulty=2,
                rule_statement="Corporation formed by filing articles; de facto corporation and corporation by estoppel doctrines; promoter liability for pre-incorporation contracts",
                elements=["Articles of incorporation", "De jure corporation", "De facto corporation", "Corporation by estoppel", "Promoter liability"],
                common_traps=["Thinking corporation exists without filing"]
            ),
            KnowledgeNode(
                concept_id="biz_piercing_veil",
                name="Piercing the Corporate Veil",
                subject="business_associations",
                difficulty=3,
                rule_statement="Courts disregard separate entity if inadequate capitalization, failure to observe formalities, fraud, or alter ego",
                elements=["Inadequate capitalization", "Formalities not observed", "Commingling", "Fraud", "Alter ego"],
                common_traps=["Thinking sole shareholder automatically means piercing"]
            ),
            KnowledgeNode(
                concept_id="biz_shareholder_rights",
                name="Shareholder Rights & Voting",
                subject="business_associations",
                difficulty=3,
                rule_statement="Shareholders elect directors, approve fundamental changes; voting agreements and voting trusts allowed; preemptive rights unless denied",
                elements=["Voting rights", "Voting agreements", "Voting trusts", "Proxies", "Preemptive rights", "Inspection rights"],
                common_traps=["Thinking shareholders manage corporation"]
            ),
            KnowledgeNode(
                concept_id="biz_director_duties",
                name="Director & Officer Duties",
                subject="business_associations",
                difficulty=4,
                rule_statement="Duty of care (business judgment rule) and duty of loyalty (self-dealing, corporate opportunity); BJR protects informed, good faith decisions",
                elements=["Duty of care", "Business judgment rule", "Duty of loyalty", "Self-dealing", "Corporate opportunity doctrine"],
                common_traps=["Thinking business judgment rule protects all decisions"]
            ),
            KnowledgeNode(
                concept_id="biz_derivative_suits",
                name="Shareholder Derivative Suits",
                subject="business_associations",
                difficulty=3,
                rule_statement="Shareholder sues on behalf of corporation; must make demand on board unless futile; recovery goes to corporation",
                elements=["Standing requirements", "Contemporaneous ownership", "Demand requirement", "Futility", "Recovery to corporation"],
                common_traps=["Thinking shareholder keeps recovery in derivative suit"]
            ),
        ]
        for node in biz_assoc:
            self.nodes[node.concept_id] = node

    def get_subject_concepts(self, subject: str) -> List[KnowledgeNode]:'''

# Combine the pieces
new_content = before_methods + new_methods + after_methods

# Write the file
with open('bar_tutor_unified.py', 'w') as f:
    f.write(new_content)

print("✅ Successfully expanded all subjects with comprehensive coverage!")
print("\n📚 MBE Subjects (8):")
print("   - Contracts: 20 concepts")
print("   - Torts: 18 concepts")
print("   - Evidence: 16 concepts")
print("   - Constitutional Law: 18 concepts")
print("   - Criminal Law: 17 concepts")
print("   - Criminal Procedure: 16 concepts")
print("   - Civil Procedure: 15 concepts")
print("   - Property: 20 concepts")
print("\n📝 MEE Subjects (3):")
print("   - Family Law: 10 concepts")
print("   - Trusts & Estates: 12 concepts")
print("   - Business Associations: 11 concepts")
print("\n🎯 Total: 173 comprehensive concepts across all 11 subjects!")
print("\n✨ Next step: Restart the web app to see all subjects and concepts:")
print("   cd web && ./start.sh")

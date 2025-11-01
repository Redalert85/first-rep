#!/usr/bin/env python3
"""
Full MBE Expansion - Complete NCBE Coverage
Target: 170-210 total concepts (21-26 per subject)
"""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict

@dataclass
class ExpandedConcept:
    """Full MBE concept with all details"""
    concept_id: str
    name: str
    subject: str
    difficulty: int = 3
    rule_statement: str = ""
    elements: List[str] = field(default_factory=list)
    policy_rationales: List[str] = field(default_factory=list)
    common_traps: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    mnemonic: str = ""

class FullMBEExpander:
    """Expand all MBE subjects to complete NCBE coverage"""
    
    def __init__(self):
        self.new_concepts = {
            'civil_procedure': [],
            'constitutional_law': [],
            'contracts': [],
            'criminal_law': [],
            'criminal_procedure': [],
            'evidence': [],
            'real_property': [],
            'torts': []
        }
    
    def generate_civil_procedure_concepts(self):
        """Add 7-11 Civil Procedure concepts (14 → 21-25)"""
        concepts = [
            ExpandedConcept(
                concept_id="civil_procedure_venue",
                name="Venue & Transfer",
                subject="civil_procedure",
                rule_statement="Venue proper where defendant resides, events occurred, or property located; transfer for convenience or interest of justice",
                elements=["Proper venue", "§1404(a) transfer", "§1406 improper venue transfer", "Forum non conveniens"],
                common_traps=[
                    "Confusing venue with personal jurisdiction",
                    "Forgetting §1404(a) requires proper venue initially",
                    "Missing that transferee court applies transferor's choice of law"
                ],
                mnemonic="VET: Venue, Events, Transfer"
            ),
            ExpandedConcept(
                concept_id="civil_procedure_joinder_claims",
                name="Joinder of Claims",
                subject="civil_procedure",
                rule_statement="Party may join as many claims as they have against opposing party under Rule 18; no need for relation",
                elements=["Permissive joinder", "Rule 18 - unlimited", "Subject matter jurisdiction required", "Supplemental jurisdiction"],
                common_traps=[
                    "Thinking claims must be related (they don't under Rule 18)",
                    "Forgetting each claim needs independent SMJ or supplemental",
                    "Confusing claim joinder with party joinder"
                ]
            ),
            ExpandedConcept(
                concept_id="civil_procedure_counterclaims",
                name="Counterclaims & Cross-claims",
                subject="civil_procedure",
                rule_statement="Compulsory counterclaim arises from same transaction; permissive does not; cross-claims must arise from same transaction",
                elements=["Compulsory counterclaim", "Permissive counterclaim", "Cross-claims", "Same transaction test"],
                common_traps=[
                    "Missing that compulsory counterclaim is waived if not asserted",
                    "Forgetting cross-claims are always permissive",
                    "Confusing counterclaim with setoff"
                ],
                mnemonic="CCC: Compulsory, Cross, Claims"
            ),
            ExpandedConcept(
                concept_id="civil_procedure_class_actions",
                name="Class Actions",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Class action requires numerosity, commonality, typicality, adequate representation, plus Rule 23(b) category",
                elements=["Numerosity", "Commonality", "Typicality", "Adequate representation", "Rule 23(b) types"],
                common_traps=[
                    "Forgetting notice required for Rule 23(b)(3) damages classes",
                    "Missing that class members can opt out only in (b)(3)",
                    "Confusing certification with merits determination"
                ],
                mnemonic="NCTA: Numerosity, Commonality, Typicality, Adequate rep"
            ),
            ExpandedConcept(
                concept_id="civil_procedure_res_judicata_detailed",
                name="Res Judicata (Claim Preclusion)",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Valid final judgment on merits precludes same parties from relitigating same claim or any part that could have been litigated",
                elements=["Valid judgment", "Final on merits", "Same claim", "Same parties or in privity"],
                policy_rationales=[
                    "Finality and repose",
                    "Prevent harassment",
                    "Judicial efficiency"
                ],
                common_traps=[
                    "Forgetting dismissal for lack of jurisdiction is not on merits",
                    "Missing that voluntary dismissal without prejudice is not preclusive",
                    "Applying res judicata when issue preclusion should apply"
                ]
            ),
            ExpandedConcept(
                concept_id="civil_procedure_discovery_sanctions",
                name="Discovery Sanctions",
                subject="civil_procedure",
                rule_statement="Court may impose sanctions for discovery violations, from costs to dismissal or default judgment",
                elements=["Rule 37 sanctions", "Good faith requirement", "Proportionality", "Protective orders"],
                common_traps=[
                    "Forgetting meet-and-confer requirement before motion",
                    "Missing that dismissal/default are harsh sanctions requiring willfulness",
                    "Not considering less severe sanctions first"
                ]
            ),
            ExpandedConcept(
                concept_id="civil_procedure_erie_doctrine",
                name="Erie Doctrine Applications",
                subject="civil_procedure",
                difficulty=4,
                rule_statement="Federal courts in diversity apply state substantive law but federal procedural law; outcome determinative if no valid FRCP",
                elements=["Substantive vs procedural", "Outcome determinative test", "Rules Enabling Act", "Twin aims of Erie"],
                common_traps=[
                    "Assuming all procedural issues are federal",
                    "Forgetting valid FRCP trumps conflicting state law",
                    "Missing that statute of limitations is substantive"
                ],
                mnemonic="SOAP: Substantive vs Outcome vs Act vs Procedural"
            ),
        ]
        self.new_concepts['civil_procedure'] = concepts
        return len(concepts)
    
    def generate_constitutional_law_concepts(self):
        """Add 7-11 Constitutional Law concepts (14 → 21-25)"""
        concepts = [
            ExpandedConcept(
                concept_id="constitutional_law_state_action",
                name="State Action Doctrine",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Constitutional rights apply only to government action; private conduct becomes state action through public function, entanglement, or encouragement",
                elements=["Public function test", "Entanglement", "Nexus/encouragement", "Exclusive public function"],
                common_traps=[
                    "Thinking all constitutional rights apply to private parties",
                    "Missing that public function must be traditionally exclusively governmental",
                    "Forgetting mere government regulation ≠ state action"
                ],
                policy_rationales=["Protect individual liberty from government overreach", "Preserve private autonomy"]
            ),
            ExpandedConcept(
                concept_id="constitutional_law_dormant_commerce_clause",
                name="Dormant Commerce Clause",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="States cannot discriminate against or unduly burden interstate commerce; discrimination gets strict scrutiny, burden gets balancing",
                elements=["Discrimination analysis", "Pike balancing test", "Market participant exception", "Congressional authorization"],
                common_traps=[
                    "Applying dormant commerce clause when Congress has acted",
                    "Forgetting market participant exception",
                    "Missing that facially neutral laws can discriminate in effect"
                ],
                mnemonic="DCC: Discriminate, Congress can override, Clause"
            ),
            ExpandedConcept(
                concept_id="constitutional_law_privileges_immunities_art4",
                name="Privileges & Immunities Clause (Art IV)",
                subject="constitutional_law",
                rule_statement="State cannot discriminate against out-of-state citizens regarding fundamental rights unless substantial justification and no less restrictive means",
                elements=["Fundamental rights", "Substantial justification", "Discrimination against non-residents", "Least restrictive means"],
                common_traps=[
                    "Confusing Art IV P&I with 14th Amendment P&I",
                    "Applying to corporations (only applies to citizens)",
                    "Forgetting recreational activities not fundamental"
                ]
            ),
            ExpandedConcept(
                concept_id="constitutional_law_contracts_clause",
                name="Contracts Clause",
                subject="constitutional_law",
                rule_statement="States cannot substantially impair contracts unless reasonable and necessary to serve important public purpose",
                elements=["Substantial impairment", "Public vs private contracts", "Strict scrutiny for public", "Intermediate for private"],
                common_traps=[
                    "Not applying stricter scrutiny when state impairs its own contracts",
                    "Forgetting reasonable expectations matter",
                    "Missing prospective vs retroactive distinction"
                ]
            ),
            ExpandedConcept(
                concept_id="constitutional_law_ex_post_facto",
                name="Ex Post Facto & Bills of Attainder",
                subject="constitutional_law",
                rule_statement="Ex post facto criminalizes past conduct or increases punishment retroactively; bills of attainder legislatively punish without trial",
                elements=["Retroactive criminalization", "Retroactive penalty increase", "Legislative punishment", "Criminal only"],
                common_traps=[
                    "Applying ex post facto to civil laws (criminal only)",
                    "Missing that increased sentencing guidelines can violate",
                    "Forgetting bills of attainder require specific identification"
                ]
            ),
            ExpandedConcept(
                concept_id="constitutional_law_executive_powers",
                name="Executive Powers",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="President has inherent powers over foreign affairs; domestic power greatest with Congressional approval, weakest when contrary to Congress",
                elements=["Youngstown framework", "Foreign affairs power", "Commander in Chief", "Pardon power"],
                common_traps=[
                    "Giving president unlimited domestic emergency powers",
                    "Forgetting treaty power shared with Senate",
                    "Missing limits on pardon power (impeachment, state crimes)"
                ],
                mnemonic="YES: Youngstown, Executive, Senate (for treaties)"
            ),
            ExpandedConcept(
                concept_id="constitutional_law_justiciability",
                name="Justiciability - Standing, Mootness, Ripeness",
                subject="constitutional_law",
                difficulty=4,
                rule_statement="Standing requires injury, causation, redressability; mootness requires live controversy; ripeness requires matured harm",
                elements=["Standing elements", "Mootness exceptions", "Ripeness test", "Third-party standing"],
                common_traps=[
                    "Forgetting generalized grievances lack standing",
                    "Missing capable of repetition yet evading review exception",
                    "Not applying ripeness to pre-enforcement challenges"
                ],
                mnemonic="SMR: Standing, Mootness, Ripeness"
            ),
        ]
        self.new_concepts['constitutional_law'] = concepts
        return len(concepts)
    
    def generate_contracts_concepts(self):
        """Add 11-16 Contracts concepts (14 → 25-30)"""
        concepts = [
            ExpandedConcept(
                concept_id="contracts_offer_termination",
                name="Offer Termination",
                subject="contracts",
                rule_statement="Offer terminates by rejection, counteroffer, lapse, revocation, death/incapacity, or destruction of subject matter",
                elements=["Rejection", "Counteroffer as rejection", "Lapse of time", "Revocation", "Death of offeror"],
                common_traps=[
                    "Thinking inquiry is rejection (it's not)",
                    "Missing that counteroffer rejects but not if merchant under UCC 2-207",
                    "Forgetting irrevocable offers (option, firm offer, reliance)"
                ],
                mnemonic="RRLD: Rejection, Revocation, Lapse, Death"
            ),
            ExpandedConcept(
                concept_id="contracts_battle_of_forms_detailed",
                name="UCC §2-207 Battle of Forms",
                subject="contracts",
                difficulty=4,
                rule_statement="Definite expression of acceptance forms contract even with additional terms; between merchants, additional terms included unless material alteration, expressly limited, or objection",
                elements=["Definite expression", "Additional vs different terms", "Material alteration test", "Merchant status"],
                common_traps=[
                    "Applying mirror image rule under UCC (wrong!)",
                    "Forgetting expressly conditional acceptance is counteroffer",
                    "Missing that different terms knocked out, additional terms analyzed"
                ],
                policy_rationales=["Facilitate modern commerce", "Avoid technical knockout rule"]
            ),
            ExpandedConcept(
                concept_id="contracts_mailbox_rule",
                name="Mailbox Rule & Exceptions",
                subject="contracts",
                rule_statement="Acceptance effective upon dispatch unless option contract, offeror specifies receipt, or rejection sent first",
                elements=["Dispatch rule", "Receipt rule exceptions", "Option contracts", "Overtaking rule"],
                common_traps=[
                    "Applying mailbox to revocations (need receipt)",
                    "Missing that sending rejection first voids mailbox rule",
                    "Forgetting improper dispatch doesn't get mailbox protection"
                ]
            ),
            ExpandedConcept(
                concept_id="contracts_statute_of_frauds",
                name="Statute of Frauds",
                subject="contracts",
                difficulty=4,
                rule_statement="MYLEGS contracts must be in writing: Marriage, Year, Land, Executor, Goods $500+, Surety",
                elements=["MYLEGS categories", "Writing requirements", "Part performance exception", "Merchant confirmation"],
                common_traps=[
                    "Forgetting one-year is from making, not performance",
                    "Missing that services completable within year don't need writing",
                    "Not applying merchant confirmation rule (UCC)"
                ],
                mnemonic="MYLEGS"
            ),
            ExpandedConcept(
                concept_id="contracts_parol_evidence_detailed",
                name="Parol Evidence Rule Applications",
                subject="contracts",
                difficulty=4,
                rule_statement="Completely integrated writing bars prior or contemporaneous contradictory or supplementary terms; partial integration bars only contradictory",
                elements=["Integration", "Four corners vs contextual", "Exceptions", "Merger clause"],
                common_traps=[
                    "Thinking PER bars all extrinsic evidence (wrong - only prior/contemporaneous)",
                    "Missing exceptions for condition precedent, fraud, mistake",
                    "Not distinguishing complete vs partial integration"
                ],
                policy_rationales=["Protect integrity of written agreements", "Certainty in contracting"]
            ),
            ExpandedConcept(
                concept_id="contracts_mistake",
                name="Mistake (Mutual vs Unilateral)",
                subject="contracts",
                rule_statement="Mutual mistake as to basic assumption allows rescission; unilateral mistake allows rescission only if known/should be known by other party",
                elements=["Mutual mistake", "Basic assumption", "Material effect", "Unilateral mistake limits"],
                common_traps=[
                    "Allowing rescission for mistake in value (usually no)",
                    "Forgetting party bearing risk can't claim mistake",
                    "Missing that negligent mistake may still count if extreme"
                ]
            ),
            ExpandedConcept(
                concept_id="contracts_misrepresentation",
                name="Misrepresentation & Fraud",
                subject="contracts",
                rule_statement="Fraudulent misrepresentation makes contract voidable; requires false assertion of fact, scienter, intent to induce, justifiable reliance, harm",
                elements=["False assertion", "Material fact", "Scienter", "Justifiable reliance", "Damages"],
                common_traps=[
                    "Applying fraud to mere opinions (usually not actionable)",
                    "Forgetting fraud in the inducement makes voidable, fraud in execution void",
                    "Missing that non-disclosure can be misrepresentation if duty to speak"
                ]
            ),
            ExpandedConcept(
                concept_id="contracts_duress",
                name="Duress & Undue Influence",
                subject="contracts",
                rule_statement="Duress by improper threat leaves no reasonable alternative; undue influence unfairly persuades party in confidential relationship",
                elements=["Improper threat", "No reasonable alternative", "Economic duress", "Undue influence factors"],
                common_traps=[
                    "Confusing duress with hard bargaining",
                    "Forgetting threat must be improper (not just pressure)",
                    "Missing undue influence requires confidential relationship usually"
                ]
            ),
            ExpandedConcept(
                concept_id="contracts_impossibility_impracticability",
                name="Impossibility vs Impracticability",
                subject="contracts",
                difficulty=4,
                rule_statement="Impossibility excuses if objectively impossible; impracticability excuses if extreme unforeseen difficulty makes performance unreasonably expensive",
                elements=["Objective impossibility", "Subjective impossibility", "Commercial impracticability", "Foreseeability"],
                common_traps=[
                    "Excusing for subjective impossibility (e.g., bankruptcy)",
                    "Applying impracticability when just more expensive (need extreme)",
                    "Forgetting party assuming risk cannot claim impossibility"
                ],
                mnemonic="PIF: Possible, Impractical, Frustrated"
            ),
            ExpandedConcept(
                concept_id="contracts_frustration_purpose",
                name="Frustration of Purpose",
                subject="contracts",
                rule_statement="Frustration excuses if supervening event destroys principal purpose and party did not assume risk",
                elements=["Principal purpose destroyed", "Supervening event", "Not assumed risk", "Foreseeability"],
                common_traps=[
                    "Applying when purpose merely difficult (need destroyed)",
                    "Using when performance impossible (that's impossibility, not frustration)",
                    "Forgetting both parties must have known purpose"
                ]
            ),
            ExpandedConcept(
                concept_id="contracts_assignment_delegation",
                name="Assignment vs Delegation",
                subject="contracts",
                difficulty=3,
                rule_statement="Rights can be assigned unless personal, materially change duty, or prohibited; duties can be delegated unless personal services or prohibited",
                elements=["Assignment of rights", "Delegation of duties", "Prohibition clauses", "Personal services exception"],
                common_traps=[
                    "Thinking all contract rights assignable (personal services exception)",
                    "Missing that delegation doesn't release delegator (still liable)",
                    "Confusing assignment language with delegation"
                ],
                mnemonic="AD: Assignment (rights), Delegation (duties)"
            ),
            ExpandedConcept(
                concept_id="contracts_third_party_beneficiaries",
                name="Third-Party Beneficiaries",
                subject="contracts",
                difficulty=4,
                rule_statement="Intended beneficiary can enforce; incidental beneficiary cannot; test is whether party intended to benefit third party",
                elements=["Intended vs incidental", "Creditor beneficiary", "Donee beneficiary", "Vesting of rights"],
                common_traps=[
                    "Letting incidental beneficiary sue (cannot)",
                    "Missing that rights vest when beneficiary learns and relies",
                    "Forgetting government contracts presumed not to benefit third parties"
                ]
            ),
        ]
        self.new_concepts['contracts'] = concepts
        return len(concepts)
    
    def generate_criminal_law_concepts(self):
        """Add 7-11 Criminal Law concepts (14 → 21-25)"""
        concepts = [
            ExpandedConcept(
                concept_id="criminal_law_robbery",
                name="Robbery",
                subject="criminal_law",
                rule_statement="Robbery is larceny from person or presence by force or intimidation",
                elements=["Larceny elements", "From person or presence", "Force or fear", "Intent to permanently deprive"],
                common_traps=[
                    "Missing that force must be used to obtain property or escape",
                    "Forgetting presence means within victim's control",
                    "Confusing robbery with extortion (future threat)"
                ],
                prerequisites=["criminal_law_larceny"]
            ),
            ExpandedConcept(
                concept_id="criminal_law_burglary",
                name="Burglary",
                subject="criminal_law",
                rule_statement="Common law burglary: breaking and entering dwelling of another at nighttime with intent to commit felony therein",
                elements=["Breaking", "Entering", "Dwelling", "Of another", "Nighttime", "Intent to commit felony"],
                common_traps=[
                    "Applying modern statutes (many drop nighttime, dwelling requirements)",
                    "Missing that intent must exist at time of entry",
                    "Forgetting slight force counts as breaking (turning doorknob)"
                ],
                mnemonic="BEDINF: Breaking, Entering, Dwelling, Intent, Nighttime, Felony"
            ),
            ExpandedConcept(
                concept_id="criminal_law_arson",
                name="Arson",
                subject="criminal_law",
                rule_statement="Common law arson: malicious burning of dwelling of another",
                elements=["Malicious", "Burning", "Dwelling", "Of another"],
                common_traps=[
                    "Thinking any burning suffices (need material wasting/charring)",
                    "Missing that burning own property for insurance is arson if endangers others",
                    "Confusing arson with criminal mischief"
                ]
            ),
            ExpandedConcept(
                concept_id="criminal_law_conspiracy",
                name="Conspiracy",
                subject="criminal_law",
                difficulty=4,
                rule_statement="Agreement between two or more to commit crime plus overt act in furtherance (majority); common law no overt act needed",
                elements=["Agreement", "Two or more parties", "Intent", "Overt act", "Withdrawal"],
                common_traps=[
                    "Forgetting Wharton's Rule (crime requiring two can't be conspiracy with only two)",
                    "Missing that withdrawal doesn't excuse conspiracy liability (only subsequent crimes)",
                    "Applying unilateral conspiracy where bilateral required"
                ],
                mnemonic="AIM: Agreement, Intent, Mens rea"
            ),
            ExpandedConcept(
                concept_id="criminal_law_solicitation",
                name="Solicitation",
                subject="criminal_law",
                rule_statement="Solicitation is asking, encouraging, or commanding another to commit crime with intent that crime be committed",
                elements=["Asking/encouraging", "Another person", "Commit crime", "Intent crime be committed"],
                common_traps=[
                    "Thinking target crime must occur (solicitation complete upon asking)",
                    "Missing that renunciation generally not a defense",
                    "Confusing solicitation with attempt"
                ]
            ),
            ExpandedConcept(
                concept_id="criminal_law_accomplice_liability",
                name="Accomplice Liability",
                subject="criminal_law",
                difficulty=4,
                rule_statement="Accomplice liable for crimes they aid, abet, or encourage with intent to assist and intent that crime be committed",
                elements=["Aid/abet/encourage", "Intent to assist", "Intent crime be committed", "Principal commits crime"],
                common_traps=[
                    "Imposing liability for mere presence (need assistance)",
                    "Missing that accomplice liable for foreseeable crimes in furtherance",
                    "Confusing accomplice with accessory after fact (who aids after crime)"
                ],
                policy_rationales=["Deter assistance to criminals", "Hold helpers accountable"]
            ),
            ExpandedConcept(
                concept_id="criminal_law_entrapment",
                name="Entrapment",
                subject="criminal_law",
                rule_statement="Entrapment defense if government induces crime in person not predisposed; objective test focuses on government conduct",
                elements=["Government inducement", "Lack of predisposition", "Subjective test", "Objective test"],
                common_traps=[
                    "Applying entrapment to private party inducement (must be government)",
                    "Forgetting predisposition defeats defense under subjective test",
                    "Missing that providing opportunity is not inducement"
                ]
            ),
        ]
        self.new_concepts['criminal_law'] = concepts
        return len(concepts)
    
    def generate_criminal_procedure_concepts(self):
        """Add 7-11 Criminal Procedure concepts (14 → 21-25)"""
        concepts = [
            ExpandedConcept(
                concept_id="criminal_procedure_fruit_poisonous_tree",
                name="Fruit of Poisonous Tree",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Evidence derived from illegal search/seizure excluded unless independent source, inevitable discovery, or attenuation",
                elements=["Derivative evidence", "Independent source", "Inevitable discovery", "Attenuation doctrine"],
                common_traps=[
                    "Missing that Miranda violations don't trigger fruit doctrine fully",
                    "Forgetting live testimony attenuates more easily than physical evidence",
                    "Not applying inevitable discovery when would have found anyway"
                ],
                mnemonic="IIA: Independent source, Inevitable discovery, Attenuation"
            ),
            ExpandedConcept(
                concept_id="criminal_procedure_terry_stops",
                name="Terry Stops (Stop & Frisk)",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Officer may briefly detain for investigation with reasonable suspicion of criminal activity; may frisk if reasonable belief armed and dangerous",
                elements=["Reasonable suspicion", "Brief detention", "Armed and dangerous", "Plain feel doctrine"],
                common_traps=[
                    "Requiring probable cause for Terry stop (reasonable suspicion suffices)",
                    "Allowing frisk without safety concern",
                    "Missing that anonymous tip alone insufficient without corroboration"
                ],
                prerequisites=["criminal_procedure_search_incident"]
            ),
            ExpandedConcept(
                concept_id="criminal_procedure_arrests",
                name="Arrests (With & Without Warrant)",
                subject="criminal_procedure",
                rule_statement="Arrest requires probable cause; warrant required for home arrest absent exigency; public arrest no warrant needed",
                elements=["Probable cause", "Warrant for home", "Exigent circumstances", "Public place exception"],
                common_traps=[
                    "Requiring warrant for all arrests (public arrests don't need warrant)",
                    "Missing that arrest in third party home needs search warrant",
                    "Forgetting hot pursuit is exigency excusing warrant"
                ]
            ),
            ExpandedConcept(
                concept_id="criminal_procedure_exigent_circumstances",
                name="Exigent Circumstances",
                subject="criminal_procedure",
                rule_statement="Warrantless entry justified by hot pursuit, imminent destruction of evidence, emergency aid, or preventing escape",
                elements=["Hot pursuit", "Destruction of evidence", "Emergency aid", "Prevent escape"],
                common_traps=[
                    "Applying when police created exigency by bad faith",
                    "Missing that mere possibility of destruction insufficient",
                    "Forgetting exigency must be immediate, not speculative"
                ]
            ),
            ExpandedConcept(
                concept_id="criminal_procedure_inventory_searches",
                name="Inventory Searches",
                subject="criminal_procedure",
                rule_statement="Police may inventory lawfully impounded vehicle or arrested person's belongings following standardized procedures",
                elements=["Lawful impoundment", "Standardized procedure", "Administrative purpose", "No investigative pretext"],
                common_traps=[
                    "Allowing when done for investigative purposes (must be administrative)",
                    "Missing that warrantless search of closed containers OK in inventory",
                    "Forgetting need for established policy/procedure"
                ]
            ),
            ExpandedConcept(
                concept_id="criminal_procedure_lineups",
                name="Lineups & Identifications",
                subject="criminal_procedure",
                difficulty=4,
                rule_statement="Post-charge lineup requires counsel; suggestive pre-trial identification excluded if unreliable; in-court ID evaluated for reliability",
                elements=["Right to counsel at lineup", "Suggestiveness test", "Reliability factors", "Independent source"],
                common_traps=[
                    "Requiring counsel at pre-charge lineups (not required)",
                    "Missing that photo arrays don't require counsel",
                    "Forgetting independent source exception for tainted ID"
                ]
            ),
            ExpandedConcept(
                concept_id="criminal_procedure_plea_bargaining",
                name="Plea Bargaining",
                subject="criminal_procedure",
                rule_statement="Guilty plea must be voluntary, intelligent, with understanding of charges and consequences; breach of plea deal allows withdrawal",
                elements=["Voluntary", "Intelligent", "Understanding", "Breach remedies"],
                common_traps=[
                    "Missing that defendant must understand deportation consequences",
                    "Forgetting ineffective assistance can invalidate plea",
                    "Not knowing that judge not bound by sentencing recommendation"
                ]
            ),
        ]
        self.new_concepts['criminal_procedure'] = concepts
        return len(concepts)
    
    def generate_evidence_concepts(self):
        """Add 7-11 Evidence concepts (14 → 21-25)"""
        concepts = [
            ExpandedConcept(
                concept_id="evidence_subsequent_remedial_measures",
                name="Subsequent Remedial Measures",
                subject="evidence",
                rule_statement="Evidence of repairs or safety measures after injury inadmissible to prove negligence or defect, but admissible for impeachment, ownership, or feasibility",
                elements=["Inadmissible for negligence", "Admissible for impeachment", "Ownership", "Feasibility if disputed"],
                common_traps=[
                    "Excluding when offered for permissible purpose",
                    "Missing that rule doesn't apply to strict liability cases in some jurisdictions",
                    "Forgetting rule encourages safety improvements"
                ],
                policy_rationales=["Encourage repairs", "Prevent deterring safety measures"]
            ),
            ExpandedConcept(
                concept_id="evidence_compromise_settlement",
                name="Compromise & Settlement Offers",
                subject="evidence",
                rule_statement="Statements made during settlement negotiations inadmissible to prove liability or amount; admissible for other purposes like bias",
                elements=["Dispute exists", "Settlement statements", "Not if no dispute", "Admissions of fact admissible if not hypothetical"],
                common_traps=[
                    "Excluding factual admissions made during negotiations (may be admissible)",
                    "Applying rule when no dispute existed at time",
                    "Missing that Rule 408 doesn't apply to criminal cases"
                ]
            ),
            ExpandedConcept(
                concept_id="evidence_habit",
                name="Habit Evidence",
                subject="evidence",
                rule_statement="Evidence of habit or routine practice admissible to prove conduct on particular occasion; more specific and automatic than character",
                elements=["Specificity", "Frequency", "Automatic response", "Routine practice"],
                common_traps=[
                    "Confusing habit with character (habit is specific routine)",
                    "Missing that habit doesn't require corroboration or eyewitness",
                    "Thinking single instance can establish habit (need pattern)"
                ]
            ),
            ExpandedConcept(
                concept_id="evidence_rape_shield",
                name="Rape Shield Rule",
                subject="evidence",
                difficulty=4,
                rule_statement="Evidence of victim's sexual behavior generally inadmissible except to prove alternative source of semen/injury or past acts with defendant",
                elements=["General exclusion", "Alternative source exception", "Prior acts with defendant", "Constitutional rights"],
                common_traps=[
                    "Missing that constitutional right to present defense may override",
                    "Applying rule to exclude reputation for untruthfulness (wrong - character for truthfulness allowed)",
                    "Forgetting criminal vs civil distinctions"
                ],
                policy_rationales=["Protect victim privacy", "Prevent victim-blaming", "Encourage reporting"]
            ),
            ExpandedConcept(
                concept_id="evidence_best_evidence_rule",
                name="Best Evidence Rule (Original Document Rule)",
                subject="evidence",
                rule_statement="To prove content of writing, recording, or photo, must produce original or explain absence; doesn't apply if not proving contents",
                elements=["Content being proved", "Original required", "Duplicate admissible", "Excuses for absence"],
                common_traps=[
                    "Applying when content not being proved (e.g., event witnessed)",
                    "Thinking duplicates inadmissible (they're treated as originals)",
                    "Missing that photos of writings are duplicates"
                ]
            ),
            ExpandedConcept(
                concept_id="evidence_witness_competency",
                name="Witness Competency",
                subject="evidence",
                rule_statement="All persons competent to testify unless cannot perceive, remember, communicate, or understand oath; judge determines competency",
                elements=["Perception", "Memory", "Communication", "Oath understanding"],
                common_traps=[
                    "Thinking children automatically incompetent (competency presumed)",
                    "Confusing competency with credibility",
                    "Missing that personal knowledge is separate requirement"
                ]
            ),
            ExpandedConcept(
                concept_id="evidence_recorded_recollection",
                name="Recorded Recollection vs Refreshing Memory",
                subject="evidence",
                difficulty=4,
                rule_statement="Refreshing recollection: witness looks at writing, then testifies from refreshed memory; recorded recollection: can't remember even after viewing, read into evidence",
                elements=["Present recollection refreshed", "Past recollection recorded", "Foundation requirements", "Hearsay exception"],
                common_traps=[
                    "Confusing the two doctrines",
                    "Missing that refreshing document not admitted, recorded recollection is",
                    "Forgetting that recorded recollection requires inability to remember even after viewing"
                ]
            ),
            ExpandedConcept(
                concept_id="evidence_learned_treatises",
                name="Learned Treatises",
                subject="evidence",
                rule_statement="Statements from reliable treatises admissible on direct or cross if established as reliable authority and expert on stand",
                elements=["Reliable authority", "Expert on stand", "Read to jury", "Not admitted as exhibit"],
                common_traps=[
                    "Admitting treatise itself (only read into evidence)",
                    "Using without expert on stand",
                    "Missing that can be used on direct, not just cross"
                ]
            ),
            ExpandedConcept(
                concept_id="evidence_judicial_notice",
                name="Judicial Notice",
                subject="evidence",
                rule_statement="Court may take judicial notice of facts generally known in jurisdiction or accurately and readily determinable from reliable sources",
                elements=["Generally known", "Accurately determinable", "Mandatory if requested", "Instructing jury"],
                common_traps=[
                    "Taking notice of disputed facts (must be indisputable)",
                    "Missing that criminal jury cannot be instructed to accept noticed fact as conclusive",
                    "Forgetting party must be heard before judicial notice"
                ]
            ),
        ]
        self.new_concepts['evidence'] = concepts
        return len(concepts)
    
    def generate_real_property_concepts(self):
        """Add 11-16 Real Property concepts (14 → 25-30)"""
        concepts = [
            ExpandedConcept(
                concept_id="real_property_easement_by_implication",
                name="Easement by Implication",
                subject="real_property",
                difficulty=4,
                rule_statement="Easement implied from prior use if use was apparent, continuous, reasonably necessary, and parties expected it to continue",
                elements=["Prior use", "Apparent", "Continuous", "Reasonably necessary", "Common grantor"],
                common_traps=[
                    "Confusing with easement by necessity (necessity must be absolute)",
                    "Missing that strict necessity only required for necessity, not implication",
                    "Forgetting quasi-easement requires unity of ownership before severance"
                ],
                prerequisites=["real_property_easements_servitudes_and_licenses"]
            ),
            ExpandedConcept(
                concept_id="real_property_easement_by_prescription",
                name="Easement by Prescription",
                subject="real_property",
                rule_statement="Easement acquired by open, notorious, continuous, adverse use for statutory period (similar to adverse possession)",
                elements=["Open and notorious", "Continuous", "Adverse/hostile", "Statutory period", "No exclusive use"],
                common_traps=[
                    "Requiring exclusive use (not required for prescriptive easement)",
                    "Missing that permissive use cannot ripen into prescriptive easement",
                    "Forgetting that prescription creates easement, not ownership"
                ],
                prerequisites=["real_property_adverse_possession"]
            ),
            ExpandedConcept(
                concept_id="real_property_profit_a_prendre",
                name="Profit à Prendre",
                subject="real_property",
                rule_statement="Right to enter land and remove resources like minerals, timber, or fish; similar to easement but includes right to take",
                elements=["Right to take", "Created like easements", "Alienable", "Divisible"],
                common_traps=[
                    "Confusing profit with easement (profit includes taking)",
                    "Missing that profit holder may imply easement to access",
                    "Not distinguishing profit in gross vs appurtenant"
                ]
            ),
            ExpandedConcept(
                concept_id="real_property_real_covenants_detailed",
                name="Real Covenants Running with Land",
                subject="real_property",
                difficulty=4,
                rule_statement="Covenant runs at law if writing, intent, touch and concern, notice, and horizontal/vertical privity; damages remedy",
                elements=["Writing", "Intent to run", "Touch and concern", "Notice", "Horizontal privity", "Vertical privity"],
                common_traps=[
                    "Missing horizontal privity requirement (not needed for equitable servitudes)",
                    "Confusing real covenant (damages) with equitable servitude (injunction)",
                    "Forgetting burden runs at law only if horizontal privity exists"
                ],
                mnemonic="WRITNHV: Writing, Run intent, Interest (T&C), Touch concern, Notice, Horizontal, Vertical"
            ),
            ExpandedConcept(
                concept_id="real_property_equitable_servitudes",
                name="Equitable Servitudes",
                subject="real_property",
                difficulty=4,
                rule_statement="Equitable servitude enforced in equity if writing (or common scheme), intent, touch and concern, and notice; injunction remedy",
                elements=["Writing or common scheme", "Intent", "Touch and concern", "Notice", "No privity required"],
                common_traps=[
                    "Requiring privity for equitable servitudes (not needed)",
                    "Missing that equitable servitudes remedy is injunction, not damages",
                    "Forgetting notice can be actual, record, or inquiry"
                ],
                policy_rationales=["Allow flexible land use restrictions", "Protect purchaser expectations"]
            ),
            ExpandedConcept(
                concept_id="real_property_assignment_vs_sublease_detailed",
                name="Assignment vs Sublease",
                subject="real_property",
                difficulty=4,
                rule_statement="Assignment transfers entire remaining term; sublease retains any part; assignee in privity with landlord, sublessee not",
                elements=["Entire term test", "Privity of estate", "Privity of contract", "Landlord-tenant relationships"],
                common_traps=[
                    "Missing that retaining one day makes it sublease",
                    "Forgetting assignee liable on covenants that run with land",
                    "Confusing when original tenant remains liable (always in contract)"
                ],
                mnemonic="APES: Assignment = Privity Estate; Sublease = no privity"
            ),
            ExpandedConcept(
                concept_id="real_property_constructive_eviction",
                name="Constructive Eviction",
                subject="real_property",
                rule_statement="Landlord's breach of duty makes premises uninhabitable; tenant must notify, give chance to repair, and vacate within reasonable time",
                elements=["Substantial interference", "Tenant vacates", "Reasonable time", "Landlord's fault"],
                common_traps=[
                    "Missing that tenant must actually vacate (if stay, waives claim)",
                    "Forgetting to give landlord notice and opportunity to cure",
                    "Confusing with actual eviction (which is physical exclusion)"
                ],
                prerequisites=["real_property_landlordtenant_law"]
            ),
            ExpandedConcept(
                concept_id="real_property_security_deposits",
                name="Security Deposits",
                subject="real_property",
                rule_statement="Landlord may retain deposit for unpaid rent or damage beyond normal wear and tear; must return within statutory period with itemization",
                elements=["Permissible deductions", "Normal wear and tear", "Statutory return period", "Itemization requirement"],
                common_traps=[
                    "Allowing deduction for normal wear and tear (not permitted)",
                    "Missing statutory interest requirements in some states",
                    "Forgetting landlord burden to prove deductions proper"
                ]
            ),
            ExpandedConcept(
                concept_id="real_property_mortgage_assumption",
                name="Mortgage Assumption vs Subject To",
                subject="real_property",
                difficulty=4,
                rule_statement="Assumption: buyer personally liable; subject to: buyer not personally liable but property at risk; original borrower remains liable unless novation",
                elements=["Assumption agreement", "Personal liability", "Subject to purchase", "Novation requirement"],
                common_traps=[
                    "Thinking original borrower released automatically (need novation/release)",
                    "Confusing assumption with subject to liability",
                    "Missing that due-on-sale clause may prevent transfer"
                ]
            ),
            ExpandedConcept(
                concept_id="real_property_due_on_sale",
                name="Due-on-Sale Clauses",
                subject="real_property",
                rule_statement="Clause allowing lender to accelerate loan upon transfer; generally enforceable; Garn-St. Germain Act exempts certain transfers",
                elements=["Acceleration right", "Transfer restrictions", "Federal preemption", "Exempt transfers"],
                common_traps=[
                    "Missing Garn-St. Germain exemptions (transfers to spouse, children, etc.)",
                    "Thinking all transfers trigger clause (exempt transfers exist)",
                    "Forgetting lender must act timely to enforce"
                ]
            ),
            ExpandedConcept(
                concept_id="real_property_redemption",
                name="Redemption (Equitable vs Statutory)",
                subject="real_property",
                difficulty=4,
                rule_statement="Equitable redemption: pay full debt before foreclosure sale; statutory redemption: buy back property after sale within statutory period",
                elements=["Equitable redemption timing", "Statutory redemption period", "Amount required", "Priority of redemptioners"],
                common_traps=[
                    "Confusing timing of equitable (before sale) vs statutory (after sale)",
                    "Missing that statutory redemption not available in all states",
                    "Forgetting strict foreclosure eliminates redemption"
                ]
            ),
            ExpandedConcept(
                concept_id="real_property_deed_types",
                name="Deed Types & Requirements",
                subject="real_property",
                difficulty=3,
                rule_statement="General warranty deed: grantor warrants title against all defects; special warranty: only during grantor's ownership; quitclaim: no warranties",
                elements=["General warranty deed", "Special warranty deed", "Quitclaim deed", "Six covenants"],
                common_traps=[
                    "Missing that quitclaim transfers whatever interest grantor has, if any",
                    "Confusing present covenants (breached at closing) vs future (breached later)",
                    "Forgetting delivery required for deed effectiveness"
                ],
                mnemonic="GSQ: General, Special, Quitclaim"
            ),
        ]
        self.new_concepts['real_property'] = concepts
        return len(concepts)
    
    def generate_torts_concepts(self):
        """Add 7-11 Torts concepts (14 → 21-25)"""
        concepts = [
            ExpandedConcept(
                concept_id="torts_false_imprisonment",
                name="False Imprisonment",
                subject="torts",
                rule_statement="False imprisonment: intentional confinement within bounded area with plaintiff's awareness or harm",
                elements=["Intent to confine", "Actual confinement", "No reasonable means of escape", "Awareness or harm"],
                common_traps=[
                    "Missing that threat of force suffices for confinement",
                    "Requiring physical barriers (words or threat can confine)",
                    "Forgetting that failure to release when duty exists is confinement"
                ]
            ),
            ExpandedConcept(
                concept_id="torts_iied",
                name="Intentional Infliction of Emotional Distress",
                subject="torts",
                difficulty=4,
                rule_statement="IIED requires extreme and outrageous conduct, intent or recklessness, causing severe emotional distress",
                elements=["Extreme and outrageous", "Intent or recklessness", "Causation", "Severe distress"],
                common_traps=[
                    "Finding liability for mere insults (must be extreme)",
                    "Missing common carrier/innkeeper exception (lower threshold)",
                    "Forgetting physical manifestation not required"
                ],
                policy_rationales=["Protect emotional wellbeing", "Limit frivolous claims"]
            ),
            ExpandedConcept(
                concept_id="torts_trespass_to_land",
                name="Trespass to Land",
                subject="torts",
                rule_statement="Trespass requires intentional physical invasion of plaintiff's land; mistake no defense",
                elements=["Intent to enter", "Physical invasion", "Plaintiff's land", "No mistake defense"],
                common_traps=[
                    "Requiring knowledge of trespass (intent to enter land suffices)",
                    "Missing that remaining after consent expires is trespass",
                    "Confusing trespass with nuisance (trespass is physical invasion)"
                ]
            ),
            ExpandedConcept(
                concept_id="torts_conversion",
                name="Conversion",
                subject="torts",
                rule_statement="Conversion: intentional serious interference with plaintiff's chattel so serious as to require defendant to pay full value",
                elements=["Intent to exercise dominion", "Serious interference", "Plaintiff's possessory interest", "Full value damages"],
                common_traps=[
                    "Confusing conversion with trespass to chattels (conversion more serious)",
                    "Missing that good faith no defense to conversion",
                    "Forgetting that plaintiff can elect between replevin and conversion"
                ]
            ),
            ExpandedConcept(
                concept_id="torts_defamation",
                name="Defamation (Libel vs Slander)",
                subject="torts",
                difficulty=4,
                rule_statement="Defamation: false defamatory statement communicated to third party causing harm; public figures must prove actual malice",
                elements=["Defamatory statement", "Of and concerning plaintiff", "Publication", "Damages", "Fault"],
                common_traps=[
                    "Missing slander per se categories (damages presumed)",
                    "Forgetting actual malice standard for public figures/matters",
                    "Not distinguishing libel (written) from slander (spoken)"
                ],
                mnemonic="SLANDER per se: Sexual misconduct, Loathsome disease, Adversely affects business, Notion of crime"
            ),
            ExpandedConcept(
                concept_id="torts_privacy_torts",
                name="Privacy Torts (Four Types)",
                subject="torts",
                difficulty=4,
                rule_statement="Four privacy torts: appropriation of name/likeness, intrusion upon seclusion, public disclosure of private facts, false light",
                elements=["Appropriation", "Intrusion", "Public disclosure", "False light"],
                common_traps=[
                    "Confusing false light (privacy) with defamation (reputation)",
                    "Missing that truth is defense to false light but not public disclosure",
                    "Forgetting newsworthiness is defense to public disclosure"
                ],
                mnemonic="AIPF: Appropriation, Intrusion, Public disclosure, False light"
            ),
            ExpandedConcept(
                concept_id="torts_misrepresentation",
                name="Misrepresentation (Fraudulent, Negligent, Innocent)",
                subject="torts",
                difficulty=4,
                rule_statement="Fraudulent: knowingly false material representation with intent to induce reliance causing damages; negligent: should have known false",
                elements=["False representation", "Material fact", "Scienter (fraud)", "Intent to induce", "Justifiable reliance", "Damages"],
                common_traps=[
                    "Applying fraud to opinions (usually not actionable unless expert)",
                    "Missing that negligent misrep requires special relationship often",
                    "Confusing tort fraud with contract misrepresentation"
                ]
            ),
            ExpandedConcept(
                concept_id="torts_vicarious_liability",
                name="Vicarious Liability",
                subject="torts",
                difficulty=4,
                rule_statement="Employer liable for employee torts within scope of employment; not liable for independent contractors except non-delegable duties",
                elements=["Employee vs independent contractor", "Scope of employment", "Frolic vs detour", "Non-delegable duties"],
                common_traps=[
                    "Missing that employer liable even if prohibited employee conduct",
                    "Applying vicarious liability to independent contractors generally",
                    "Forgetting intentional torts can be within scope if job-related"
                ],
                policy_rationales=["Deep pocket", "Risk distribution", "Employer control"]
            ),
            ExpandedConcept(
                concept_id="torts_joint_several_liability",
                name="Joint & Several Liability",
                subject="torts",
                difficulty=3,
                rule_statement="Multiple defendants jointly and severally liable; plaintiff can collect full amount from any defendant; contribution and indemnity available",
                elements=["Joint liability", "Several liability", "Contribution", "Indemnity", "Comparative fault rules"],
                common_traps=[
                    "Missing that many states modified joint and several with comparative fault",
                    "Confusing contribution (pro rata share) with indemnity (full shifting)",
                    "Forgetting intentional tortfeasors cannot get contribution"
                ]
            ),
        ]
        self.new_concepts['torts'] = concepts
        return len(concepts)
    
    def generate_all_concepts(self):
        """Generate all new concepts"""
        print("="*70)
        print("FULL MBE EXPANSION")
        print("Generating 58-98 new concepts for complete NCBE coverage")
        print("="*70)
        print()
        
        counts = {}
        counts['civil_procedure'] = self.generate_civil_procedure_concepts()
        counts['constitutional_law'] = self.generate_constitutional_law_concepts()
        counts['contracts'] = self.generate_contracts_concepts()
        counts['criminal_law'] = self.generate_criminal_law_concepts()
        counts['criminal_procedure'] = self.generate_criminal_procedure_concepts()
        counts['evidence'] = self.generate_evidence_concepts()
        counts['real_property'] = self.generate_real_property_concepts()
        counts['torts'] = self.generate_torts_concepts()
        
        print("\n📊 New Concepts Generated:")
        total_new = 0
        for subject, count in sorted(counts.items()):
            total_new += count
            print(f"  ✅ {subject:25} +{count:2} concepts")
        
        print(f"\n🎯 Total new concepts: {total_new}")
        print(f"🏆 Target total: 112 + {total_new} = {112 + total_new}")
        
        return total_new
    
    def export_to_python(self) -> str:
        """Export all new concepts as Python code"""
        code = "# Full MBE Expansion - Additional Concepts\n"
        code += "# Adds 58-98 concepts for complete NCBE coverage\n\n"
        
        for subject in sorted(self.new_concepts.keys()):
            concepts = self.new_concepts[subject]
            if not concepts:
                continue
            
            code += f"    def _add_{subject}_expansion(self):\n"
            code += f'        """Add {len(concepts)} additional {subject} concepts"""\n'
            code += "        concepts = [\n"
            
            for concept in concepts:
                code += "            KnowledgeNode(\n"
                code += f"                concept_id=\"{concept.concept_id}\",\n"
                code += f"                name=\"{concept.name}\",\n"
                code += f"                subject=\"{concept.subject}\",\n"
                code += f"                difficulty={concept.difficulty},\n"
                
                rule_escaped = concept.rule_statement.replace('"', '\\"').replace('\n', ' ')
                code += f"                rule_statement=\"{rule_escaped}\",\n"
                
                code += f"                elements={concept.elements},\n"
                code += f"                policy_rationales={concept.policy_rationales},\n"
                code += f"                common_traps={concept.common_traps},\n"
                
                if concept.prerequisites:
                    code += f"                prerequisites={concept.prerequisites},\n"
                
                if concept.mnemonic:
                    code += f"                # Mnemonic: {concept.mnemonic}\n"
                
                code += "            ),\n"
            
            code += "        ]\n"
            code += "        for node in concepts:\n"
            code += "            self.nodes[node.concept_id] = node\n\n"
        
        return code
    
    def save_expansion(self, filepath: Path):
        """Save all concepts to JSON"""
        all_concepts = []
        for subject, concepts in self.new_concepts.items():
            all_concepts.extend([asdict(c) for c in concepts])
        
        with filepath.open('w') as f:
            json.dump(all_concepts, f, indent=2)

def main():
    expander = FullMBEExpander()
    
    # Generate all concepts
    total_new = expander.generate_all_concepts()
    
    # Export Python code
    print("\n💾 Exporting Python code...")
    python_code = expander.export_to_python()
    Path("mbe_full_expansion.py").write_text(python_code)
    print("✓ Saved to: mbe_full_expansion.py")
    
    # Export JSON
    print("💾 Exporting JSON...")
    expander.save_expansion(Path("mbe_full_expansion.json"))
    print("✓ Saved to: mbe_full_expansion.json")
    
    print("\n" + "="*70)
    print("✅ FULL MBE EXPANSION COMPLETE!")
    print("="*70)
    print(f"\n📊 Summary:")
    print(f"  • Generated: {total_new} new concepts")
    print(f"  • Current: 112 concepts")
    print(f"  • New Total: {112 + total_new} concepts")
    print(f"  • Target: 170-210 concepts")
    print(f"  • Completion: {(112 + total_new)/190*100:.1f}%")
    print("\nNext step:")
    print("  python3 integrate_mbe_expansion.py")

if __name__ == "__main__":
    main()

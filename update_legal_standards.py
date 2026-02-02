#!/usr/bin/env python3
"""
Script to add substantive legal standards to knowledge base concepts.
Updates concepts with empty or minimal rule_statements with comprehensive legal rules.
"""

import json
from pathlib import Path

# Comprehensive legal standards to add to concepts
LEGAL_STANDARDS = {
    # CIVIL PROCEDURE
    "civil_procedure_jurisdiction_and_venue": {
        "rule_statement": "Federal courts require subject-matter jurisdiction (federal question under 28 USC 1331 or diversity under 28 USC 1332 with complete diversity and >$75,000). Personal jurisdiction requires minimum contacts satisfying due process (International Shoe) through general jurisdiction (at home) or specific jurisdiction (arise from contacts). Venue proper where defendant resides, events occurred, or property located (28 USC 1391).",
        "elements": ["Subject-Matter Jurisdiction", "Personal Jurisdiction", "Minimum Contacts Test", "General vs. Specific Jurisdiction", "Venue", "Forum Non Conveniens"],
    },
    "civil_procedure_pleadings_and_motions": {
        "rule_statement": "Complaint must contain short plain statement showing entitlement to relief with factual allegations plausibly suggesting liability (Twombly/Iqbal). Answer admits, denies, or claims insufficient knowledge within 21 days. Rule 12(b) motions (jurisdiction, venue, service, failure to state claim) must be raised in first responsive pleading or waived. Amendments freely allowed when justice requires (Rule 15).",
        "elements": ["Complaint Requirements", "Twombly/Iqbal Plausibility", "Answer", "Rule 12 Motions", "Amendments", "Relation Back"],
    },
    "civil_procedure_joinder_and_discovery": {
        "rule_statement": "Permissive joinder allows parties with claims arising from same transaction with common questions (Rule 20). Compulsory counterclaims arise from same transaction as claim (Rule 13(a)). Indispensable parties whose absence prevents complete relief must be joined if feasible (Rule 19). Discovery scope: nonprivileged matter relevant to claims/defenses proportional to needs (Rule 26(b)).",
        "elements": ["Permissive Joinder", "Compulsory Counterclaims", "Required Parties (Rule 19)", "Interpleader", "Discovery Scope", "Privilege", "Work Product"],
    },
    "civil_procedure_pretrial_and_trial": {
        "rule_statement": "Summary judgment granted when no genuine dispute of material fact exists and movant entitled to judgment as law (Rule 56). Burden: movant must show absence of dispute; nonmovant must present specific facts showing genuine issue. JMOL (Rule 50) appropriate when reasonable jury could only find one way. New trial (Rule 59) for errors affecting substantial rights.",
        "elements": ["Summary Judgment Standard", "Burden Shifting", "JMOL", "New Trial", "Jury Instructions", "Judgment as Matter of Law"],
    },
    "civil_procedure_judgments_and_preclusion": {
        "rule_statement": "Claim preclusion (res judicata) bars relitigation of claims that were or could have been raised in prior action between same parties with valid final judgment on merits. Issue preclusion (collateral estoppel) bars relitigation of issues actually litigated and necessarily decided. Mutuality not required for defensive non-mutual collateral estoppel (Blonder-Tongue).",
        "elements": ["Claim Preclusion Elements", "Issue Preclusion Elements", "Same Parties/Privity", "Final Judgment on Merits", "Mutuality", "Full Faith and Credit"],
    },

    # CRIMINAL LAW
    "criminal_law_other_crimes_against_persons": {
        "rule_statement": "Battery: unlawful application of force causing harmful or offensive contact. Assault: (1) attempted battery, or (2) intentional creation of reasonable apprehension of imminent harmful contact. Kidnapping: unlawful confinement with movement (asportation) or concealment. False imprisonment: unlawful restraint of freedom of movement. Rape: unlawful sexual intercourse without consent through force, threat, or incapacity.",
        "elements": ["Battery Elements", "Assault (Two Theories)", "Kidnapping", "False Imprisonment", "Rape", "Statutory Rape"],
    },
    "criminal_law_property_crimes": {
        "rule_statement": "Larceny: trespassory taking and carrying away of personal property of another with intent to permanently deprive. Embezzlement: fraudulent conversion of property by one in lawful possession. False pretenses: obtaining title through false representation of material present or past fact. Robbery: larceny from person by force or threat of immediate force. Burglary: breaking and entering dwelling of another at night with intent to commit felony therein (common law).",
        "elements": ["Larceny", "Embezzlement", "False Pretenses", "Robbery", "Burglary", "Receiving Stolen Property", "Arson"],
    },
    "criminal_law_inchoate_crimes": {
        "rule_statement": "Solicitation: asking another to commit a crime with intent that crime be committed (complete upon asking). Conspiracy: agreement between two or more persons to commit unlawful act plus overt act (majority rule); no withdrawal from conspiracy itself, only from liability for future crimes. Attempt: specific intent to commit crime plus substantial step toward completion beyond mere preparation.",
        "elements": ["Solicitation", "Conspiracy", "Overt Act Requirement", "Pinkerton Liability", "Attempt", "Abandonment Defense"],
    },
    "criminal_law_accomplice_and_accessory_liability": {
        "rule_statement": "Accomplice liability: one who aids, abets, counsels, or encourages principal with intent that crime be committed is liable for crime and all foreseeable crimes in furtherance. Accessory after fact: one who assists felon after crime completion knowing of felony status; separate lesser offense. Mere presence or knowledge insufficient; must have purpose to assist.",
        "elements": ["Accomplice Elements", "Dual Intent Requirement", "Natural and Probable Consequences", "Accessory After Fact", "Withdrawal"],
    },
    "criminal_law_defenses": {
        "rule_statement": "Self-defense: non-aggressor may use reasonable force when reasonably believing imminent unlawful force threatened; deadly force only against deadly force. Duress: threat of imminent death or serious bodily harm with no reasonable escape (not defense to murder). Insanity: M'Naghten (didn't know nature/quality or wrongfulness), MPC (lacked substantial capacity to appreciate criminality or conform conduct). Intoxication: voluntary negates specific intent only; involuntary is full defense.",
        "elements": ["Self-Defense", "Defense of Others", "Necessity", "Duress", "Insanity Tests", "Intoxication", "Mistake of Fact", "Entrapment"],
    },

    # CRIMINAL PROCEDURE
    "criminal_procedure_fourth_amendment": {
        "rule_statement": "Fourth Amendment prohibits unreasonable searches and seizures. Search requires government action invading reasonable expectation of privacy (Katz). Warrant required unless exception applies: consent, search incident to arrest, automobile, plain view, hot pursuit, exigent circumstances, stop and frisk (Terry). Probable cause: fair probability contraband or evidence will be found.",
        "elements": ["Reasonable Expectation of Privacy", "Government Action", "Warrant Requirements", "Probable Cause", "Warrant Exceptions", "Stop and Frisk"],
    },
    "criminal_procedure_exclusionary_rule": {
        "rule_statement": "Evidence obtained in violation of Fourth, Fifth, or Sixth Amendment excluded from prosecution's case-in-chief. Fruit of poisonous tree doctrine extends to derivative evidence. Exceptions: independent source, inevitable discovery, attenuation (time, intervening acts, flagrancy). Good faith exception for reasonable reliance on facially valid warrant (Leon). Does not apply to grand jury, civil proceedings, or impeachment.",
        "elements": ["Exclusionary Rule", "Fruit of Poisonous Tree", "Independent Source", "Inevitable Discovery", "Attenuation", "Good Faith Exception"],
    },
    "criminal_procedure_fifth_amendment": {
        "rule_statement": "Fifth Amendment privilege against self-incrimination applies to testimonial evidence compelled by government. Miranda warnings required for custodial interrogation: right to silence, statements used against you, right to attorney, appointed if indigent. Invocation must be clear and unambiguous. Waiver must be knowing, intelligent, and voluntary. Public safety exception allows questioning without Miranda when immediate threat.",
        "elements": ["Self-Incrimination Privilege", "Custody", "Interrogation", "Miranda Warnings", "Invocation", "Waiver", "Public Safety Exception"],
    },
    "criminal_procedure_sixth_amendment": {
        "rule_statement": "Sixth Amendment right to counsel attaches at initiation of formal adversarial proceedings (indictment, arraignment). Offense-specific: applies only to charged offense. Massiah: government may not deliberately elicit statements about charged offense without counsel present. Confrontation Clause: testimonial hearsay inadmissible unless declarant unavailable and prior cross-examination opportunity (Crawford).",
        "elements": ["Attachment", "Offense-Specific", "Deliberate Elicitation", "Ineffective Assistance (Strickland)", "Confrontation Clause", "Speedy Trial"],
    },

    # EVIDENCE
    "evidence_relevance": {
        "rule_statement": "Evidence is relevant if it has any tendency to make a fact of consequence more or less probable (FRE 401). Relevant evidence admissible unless excluded by rule (FRE 402). Court may exclude if probative value substantially outweighed by unfair prejudice, confusion, or waste of time (FRE 403). Policy exclusions: subsequent remedial measures, compromise offers, medical payment offers, plea discussions.",
        "elements": ["Logical Relevance (401)", "Legal Relevance (402)", "Rule 403 Balancing", "Subsequent Remedial Measures (407)", "Compromise Offers (408)", "Medical Payments (409)"],
    },
    "evidence_character_evidence": {
        "rule_statement": "Character evidence generally inadmissible to prove action in conformity (FRE 404(a)). Criminal defendant may offer pertinent trait; prosecution may rebut. Victim's character: defendant may offer in self-defense or homicide cases. Other acts (FRE 404(b)) admissible for MIMIC: motive, intent, absence of mistake, identity, common plan. Sexual assault cases: victim's past behavior generally inadmissible (FRE 412); defendant's prior acts admissible (FRE 413-415).",
        "elements": ["Character in Civil Cases", "Criminal Defendant's Character", "Victim's Character", "Other Acts (MIMIC)", "Habit (FRE 406)", "Rape Shield (FRE 412)"],
    },
    "evidence_hearsay": {
        "rule_statement": "Hearsay: out-of-court statement offered to prove truth of matter asserted; inadmissible unless exemption or exception (FRE 801-807). Non-hearsay: verbal acts, effect on listener, state of mind of speaker. Exemptions: prior statements under oath, opposing party statements. Exceptions regardless of availability: present sense impression, excited utterance, state of mind, medical diagnosis, business records, public records. Unavailability required: former testimony, dying declaration, statement against interest.",
        "elements": ["Hearsay Definition", "Non-Hearsay Uses", "Prior Statements", "Opposing Party Statements", "Present Sense Impression", "Excited Utterance", "Business Records", "Dying Declaration"],
    },
    "evidence_witnesses_and_impeachment": {
        "rule_statement": "Witnesses must have personal knowledge (FRE 602) and be competent. Impeachment methods: prior inconsistent statement, bias, sensory deficiency, character for untruthfulness (opinion/reputation), prior conviction (FRE 609), specific instances of conduct (FRE 608(b)). Prior consistent statements admissible to rebut fabrication charge. Extrinsic evidence barred for collateral matters. Bolstering only after attack.",
        "elements": ["Competency", "Personal Knowledge", "Impeachment Methods", "Prior Inconsistent Statements", "Bias", "Prior Convictions (FRE 609)", "Rehabilitation"],
    },
    "evidence_privileges_and_policy": {
        "rule_statement": "Attorney-client privilege: confidential communications between attorney and client for legal advice. Work product: attorney's mental impressions and legal theories; qualified protection. Spousal testimonial privilege: spouse cannot be compelled to testify (criminal only, holder is witness-spouse). Marital communications: confidential communications during marriage (either spouse holds). Physician-patient privilege exists in most states but not federal common law.",
        "elements": ["Attorney-Client Privilege", "Work Product Doctrine", "Spousal Testimonial Privilege", "Marital Communications", "Physician-Patient", "Waiver"],
    },

    # CONTRACTS
    "contracts_formation": {
        "rule_statement": "Contract formation requires offer, acceptance, and consideration. Offer: manifestation of willingness to enter bargain creating power of acceptance. Acceptance: unequivocal assent to terms (mirror image rule for common law; UCC 2-207 allows additional terms). Consideration: bargained-for exchange of legal value. Promissory estoppel substitutes when reasonable reliance on promise causes detriment.",
        "elements": ["Offer", "Acceptance", "Mirror Image Rule", "UCC 2-207 Battle of Forms", "Consideration", "Promissory Estoppel", "Option Contracts"],
    },
    "contracts_remedies": {
        "rule_statement": "Expectation damages: put non-breaching party in position had contract been performed (benefit of bargain). Consequential damages recoverable if foreseeable at formation (Hadley v. Baxendale). Reliance damages: put party in pre-contract position. Restitution: restore benefit conferred. Specific performance: when legal remedy inadequate (unique goods, real property). Liquidated damages enforceable if reasonable forecast and actual damages difficult to calculate.",
        "elements": ["Expectation Damages", "Consequential Damages", "Hadley Foreseeability", "Reliance Damages", "Restitution", "Specific Performance", "Liquidated Damages", "Mitigation Duty"],
    },
    "contracts_defenses": {
        "rule_statement": "Statute of Frauds requires writing for: marriage contracts, contracts not performable within one year, land interests, executor promises, goods over $500 (UCC). Mutual mistake of material fact makes contract voidable. Impossibility: performance objectively impossible. Impracticability: extreme and unreasonable difficulty (UCC 2-615). Frustration of purpose: principal purpose substantially frustrated by supervening event.",
        "elements": ["Statute of Frauds (MY LEGS)", "Mutual Mistake", "Unilateral Mistake", "Impossibility", "Impracticability", "Frustration of Purpose", "Unconscionability"],
    },
    "contracts_ucc_delivery_title_and_risk_of_loss": {
        "rule_statement": "Risk of loss passes per agreement; absent agreement, for shipment contract (FOB seller's location) risk passes on delivery to carrier; for destination contract (FOB buyer's location) risk passes on tender at destination. Breach: risk remains on breaching party regardless of delivery terms. Title passes when seller completes physical delivery. Good faith purchaser from merchant with voidable title takes good title.",
        "elements": ["Shipment Contract", "Destination Contract", "Risk During Breach", "Title Passage", "Entrustment", "Good Faith Purchaser"],
    },
    "contracts_acceptance_rejection_and_revocation_ucc": {
        "rule_statement": "Buyer may inspect goods before acceptance. Acceptance occurs by: signifying goods conform, failing to reject after reasonable time, or doing act inconsistent with seller's ownership. Rejection: must occur within reasonable time with specification of defects. Revocation of acceptance: substantial impairment of value, accepted on reasonable assumption nonconformity would be cured or without discovery of defect.",
        "elements": ["Right to Inspect", "Acceptance Methods", "Effective Rejection", "Revocation of Acceptance", "Adequate Assurances (UCC 2-609)", "Anticipatory Repudiation"],
    },

    # CONSTITUTIONAL LAW (Adding some key concepts)
    "constitutional_law_equal_protection": {
        "rule_statement": "Equal Protection (14th Amendment, 5th Amendment for federal): government classifications must satisfy appropriate scrutiny. Strict scrutiny (race, national origin, alienage by state): necessary to compelling interest, narrowly tailored. Intermediate scrutiny (gender, legitimacy): substantially related to important government interest. Rational basis (economic, social): rationally related to legitimate government interest. Burden on government for strict/intermediate; on challenger for rational basis.",
        "elements": ["Strict Scrutiny", "Intermediate Scrutiny", "Rational Basis", "Suspect Classifications", "Fundamental Rights", "Affirmative Action"],
    },
    "constitutional_law_due_process": {
        "rule_statement": "Procedural due process: when government deprives life, liberty, or property, must provide notice and meaningful opportunity to be heard. Balancing test (Mathews v. Eldridge): private interest, risk of error, government interest. Substantive due process: fundamental rights (privacy, marriage, procreation, family) require strict scrutiny; non-fundamental rights require rational basis.",
        "elements": ["Property Interest", "Liberty Interest", "Mathews Balancing", "Fundamental Rights", "Privacy Right", "Right to Marry"],
    },
    "constitutional_law_first_amendment_speech": {
        "rule_statement": "First Amendment protects speech from government abridgment. Content-based restrictions: strict scrutiny (compelling interest, narrowly tailored). Content-neutral restrictions: intermediate scrutiny (significant interest, narrowly tailored, alternative channels). Unprotected speech: incitement (Brandenburg), fighting words, true threats, obscenity (Miller test), child pornography. Public forum: government cannot ban based on viewpoint; can impose reasonable time, place, manner restrictions.",
        "elements": ["Content-Based vs. Content-Neutral", "Public Forum Doctrine", "Symbolic Speech", "Commercial Speech", "Unprotected Categories", "Prior Restraints"],
    },
}


def update_knowledge_base():
    """Update the knowledge base with substantive legal standards."""
    kb_path = Path("ultimate_knowledge_base.json")

    if not kb_path.exists():
        print(f"Error: {kb_path} not found")
        return

    with open(kb_path, "r", encoding="utf-8") as f:
        knowledge_base = json.load(f)

    updates_made = 0
    concepts_updated = []

    for concept in knowledge_base:
        concept_id = concept.get("concept_id", "")

        if concept_id in LEGAL_STANDARDS:
            update = LEGAL_STANDARDS[concept_id]

            # Update rule_statement if provided and current is empty or minimal
            if "rule_statement" in update:
                current = concept.get("rule_statement", "")
                if not current or len(current) < 50:  # Update if empty or very short
                    concept["rule_statement"] = update["rule_statement"]
                    updates_made += 1
                    concepts_updated.append(concept_id)

            # Update elements if provided
            if "elements" in update and not concept.get("elements"):
                concept["elements"] = update["elements"]

    # Write updated knowledge base
    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)

    print(f"Updated {updates_made} concepts with substantive legal standards:")
    for concept_id in concepts_updated:
        print(f"  - {concept_id}")

    return updates_made


if __name__ == "__main__":
    update_knowledge_base()

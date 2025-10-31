#!/usr/bin/env python3
"""
Expand Black Letter Law Database - Add Criminal Law, Evidence, Constitutional Law, Property
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from black_letter_law import BlackLetterLawDatabase, LegalRule

def add_criminal_law_rules(db: BlackLetterLawDatabase):
    """Add Criminal Law black letter rules"""

    # CRIMINAL LAW - Homicide
    db.add_rule(LegalRule(
        subject="Criminal Law",
        topic="Homicide",
        subtopic="Murder",
        title="Common Law Murder Elements",
        rule="Murder is the unlawful killing of another human being with malice aforethought. Malice aforethought includes: (1) intent to kill; (2) intent to inflict serious bodily injury; (3) depraved heart (reckless indifference to human life); or (4) felony murder.",
        elements=["Unlawful killing", "Of another human being", "With malice aforethought", "Causation"],
        citations=["Common Law"],
        notes="Malice can be express (intent to kill) or implied (depraved heart, felony murder). First degree murder typically requires premeditation and deliberation."
    ))

    db.add_rule(LegalRule(
        subject="Criminal Law",
        topic="Homicide",
        subtopic="Manslaughter",
        title="Voluntary Manslaughter",
        rule="Voluntary manslaughter is an intentional killing committed in the heat of passion upon adequate provocation. Requires: (1) adequate provocation; (2) actual passion; (3) no reasonable cooling off time; and (4) defendant did not actually cool off.",
        elements=["Adequate provocation", "Actual passion", "No reasonable cooling off time", "Defendant did not cool off"],
        citations=["Common Law", "MPC § 210.3"],
        notes="Adequate provocation: traditionally requires serious battery, mutual combat, illegal arrest, or witnessing adultery. MPC uses 'extreme mental or emotional disturbance.'"
    ))

    # CRIMINAL LAW - Inchoate Crimes
    db.add_rule(LegalRule(
        subject="Criminal Law",
        topic="Inchoate Crimes",
        subtopic="Attempt",
        title="Criminal Attempt Elements",
        rule="Attempt requires: (1) specific intent to commit the target crime; and (2) a substantial step beyond mere preparation toward commission of that crime. Impossibility is generally not a defense.",
        elements=["Specific intent to commit target crime", "Substantial step beyond mere preparation", "Does not complete the crime"],
        citations=["MPC § 5.01", "Common Law"],
        notes="Mere preparation is not enough. Modern rule: substantial step test. Common law: dangerous proximity test. Legal impossibility is a defense, factual impossibility is not."
    ))

    db.add_rule(LegalRule(
        subject="Criminal Law",
        topic="Inchoate Crimes",
        subtopic="Conspiracy",
        title="Conspiracy Elements",
        rule="Conspiracy requires: (1) an agreement between two or more persons; (2) intent to enter into the agreement; and (3) intent to achieve the objective of the agreement. Under modern/MPC rule, only one party needs genuine criminal intent (unilateral approach). Majority rule also requires an overt act in furtherance.",
        elements=["Agreement between two or more persons", "Intent to agree", "Intent to achieve criminal objective", "Overt act (majority rule)"],
        citations=["MPC § 5.03", "Federal: 18 U.S.C. § 371"],
        notes="Common law: bilateral approach (both must have criminal intent). MPC: unilateral approach (one genuine party sufficient). Conspirators are liable for crimes of co-conspirators in furtherance of conspiracy (Pinkerton liability)."
    ))

    # CRIMINAL LAW - Defenses
    db.add_rule(LegalRule(
        subject="Criminal Law",
        topic="Defenses",
        subtopic="Self-Defense",
        title="Self-Defense Requirements",
        rule="A person may use reasonable force to defend against an imminent, unlawful attack. Deadly force is justified only if: (1) defendant reasonably believes they face imminent threat of death or serious bodily injury; (2) defendant was not the aggressor; and (3) no obligation to retreat (majority rule) or retreat not safely possible (minority rule).",
        elements=["Reasonable belief of imminent threat", "Threat of death or serious bodily injury", "Not the aggressor", "No safe retreat available (if duty to retreat jurisdiction)"],
        citations=["Common Law", "MPC § 3.04"],
        notes="Stand your ground: majority rule, no duty to retreat. Minority/MPC: duty to retreat if safely possible before using deadly force, except in own home (castle doctrine)."
    ))

def add_evidence_rules(db: BlackLetterLawDatabase):
    """Add Evidence black letter rules"""

    # EVIDENCE - Relevance
    db.add_rule(LegalRule(
        subject="Evidence",
        topic="Relevance",
        subtopic="General Relevance",
        title="Relevance Standard - FRE 401",
        rule="Evidence is relevant if: (1) it has any tendency to make a fact more or less probable than it would be without the evidence; and (2) the fact is of consequence in determining the action.",
        elements=["Tendency to make fact more/less probable", "Fact is of consequence to the case"],
        citations=["FRE 401"],
        notes="Very low threshold - 'any tendency' is enough. Nearly all evidence is relevant. FRE 403 balancing test excludes if probative value substantially outweighed by unfair prejudice."
    ))

    db.add_rule(LegalRule(
        subject="Evidence",
        topic="Relevance",
        subtopic="Character Evidence",
        title="Character Evidence Propensity Rule",
        rule="Evidence of a person's character or character trait is not admissible to prove that on a particular occasion the person acted in accordance with the character or trait (propensity evidence). Exceptions: criminal defendant may introduce pertinent character trait, which opens door for prosecution rebuttal.",
        elements=["General rule: no character for propensity", "Exception: defendant's pertinent trait in criminal case", "Exception: victim's character in homicide/assault", "Exception: witness credibility"],
        citations=["FRE 404(a)", "FRE 404(b)"],
        notes="FRE 404(b): evidence of other crimes/wrongs/acts may be admissible for non-propensity purposes (MIMIC: Motive, Intent, Mistake/absence, Identity, Common plan). Still subject to FRE 403 balancing."
    ))

    # EVIDENCE - Hearsay Exceptions
    db.add_rule(LegalRule(
        subject="Evidence",
        topic="Hearsay",
        subtopic="Exceptions",
        title="Excited Utterance Exception",
        rule="A statement relating to a startling event or condition, made while the declarant was under the stress of excitement that it caused, is admissible as an exception to the hearsay rule. Does not require that statement be contemporaneous, only that declarant still under stress.",
        elements=["Startling event occurred", "Statement relates to startling event", "Made while under stress of excitement"],
        citations=["FRE 803(2)"],
        notes="Distinguished from present sense impression (803(1)), which requires contemporaneity but not necessarily startling event. Excited utterance requires stress, not timing."
    ))

    db.add_rule(LegalRule(
        subject="Evidence",
        topic="Hearsay",
        subtopic="Exceptions",
        title="Statement Against Interest",
        rule="A statement that a reasonable person in declarant's position would have made only if believing it to be true because it was so contrary to declarant's proprietary, pecuniary, penal, or civil interests. Declarant must be unavailable. If statement exposes declarant to criminal liability and is offered to exculpate accused, corroborating circumstances must indicate trustworthiness.",
        elements=["Statement against interest when made", "Declarant unavailable", "Corroboration if exculpatory in criminal case"],
        citations=["FRE 804(b)(3)"],
        notes="Distinguished from party admission (not hearsay, FRE 801(d)(2)). Statement against interest requires unavailability and that reasonable person wouldn't have made statement unless true."
    ))

def add_constitutional_law_rules(db: BlackLetterLawDatabase):
    """Add Constitutional Law black letter rules"""

    # CONSTITUTIONAL LAW - First Amendment
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="First Amendment",
        subtopic="Free Speech",
        title="Content-Based Speech Restrictions",
        rule="Content-based restrictions on speech are presumptively unconstitutional and subject to strict scrutiny: government must prove the restriction is necessary to achieve a compelling government interest and is narrowly tailored. Content-neutral restrictions (time, place, manner) receive intermediate scrutiny.",
        elements=["Content-based = strict scrutiny", "Compelling government interest", "Narrowly tailored means", "Content-neutral = intermediate scrutiny"],
        citations=["Reed v. Town of Gilbert, 576 U.S. 155 (2015)", "Ward v. Rock Against Racism, 491 U.S. 781 (1989)"],
        notes="Content-based: regulates speech based on subject matter or viewpoint. Content-neutral: regulates without regard to content (e.g., noise ordinance). Public forum analysis also relevant."
    ))

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="First Amendment",
        subtopic="Unprotected Speech",
        title="Categories of Unprotected Speech",
        rule="Certain categories of speech receive no First Amendment protection: (1) incitement to imminent lawless action; (2) obscenity; (3) defamation; (4) fighting words; (5) true threats; and (6) child pornography. Government may regulate these categories without strict scrutiny.",
        elements=["Incitement (Brandenburg test)", "Obscenity (Miller test)", "Defamation", "Fighting words", "True threats", "Child pornography"],
        citations=["Brandenburg v. Ohio, 395 U.S. 444 (1969)", "Miller v. California, 413 U.S. 15 (1973)"],
        notes="Incitement requires: (1) intent to incite, (2) imminence, (3) likelihood of lawless action. Obscenity (Miller test): appeals to prurient interest, patently offensive, lacks serious value (SLAPS test)."
    ))

    # CONSTITUTIONAL LAW - Equal Protection
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Equal Protection",
        subtopic="Levels of Scrutiny",
        title="Equal Protection Scrutiny Levels",
        rule="Equal protection analysis applies different levels of scrutiny based on classification: (1) Strict scrutiny for suspect classifications (race, national origin, alienage in some contexts) - must be necessary to compelling interest; (2) Intermediate scrutiny for quasi-suspect classifications (gender, legitimacy) - must be substantially related to important interest; (3) Rational basis for all others - must be rationally related to legitimate interest.",
        elements=["Strict scrutiny: race, national origin", "Intermediate: gender, legitimacy", "Rational basis: all other classifications"],
        citations=["Loving v. Virginia, 388 U.S. 1 (1967)", "Craig v. Boren, 429 U.S. 190 (1976)", "City of Cleburne v. Cleburne Living Center, 473 U.S. 432 (1985)"],
        notes="Strict scrutiny: compelling interest + necessary (no less restrictive alternative). Intermediate: important interest + substantially related. Rational basis: legitimate interest + rationally related (very deferential)."
    ))

    # CONSTITUTIONAL LAW - Fourth Amendment
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Fourth Amendment",
        subtopic="Searches",
        title="Warrantless Search Exceptions",
        rule="Warrantless searches are presumptively unreasonable. Exceptions: (1) search incident to lawful arrest (SILA); (2) automobile exception; (3) plain view; (4) consent; (5) stop and frisk; (6) hot pursuit/exigent circumstances; (7) administrative/special needs searches.",
        elements=["Lawful arrest allows search of person and wingspan", "Automobile: probable cause of evidence in car", "Plain view: lawful vantage + inadvertent discovery + immediately apparent contraband", "Valid consent", "Terry stop: reasonable suspicion", "Exigent circumstances"],
        citations=["Chimel v. California, 395 U.S. 752 (1969)", "Carroll v. United States, 267 U.S. 132 (1925)", "Terry v. Ohio, 392 U.S. 1 (1968)"],
        notes="SILA: wingspan rule from Chimel. Automobile exception does not require exigency (inherently mobile). Plain view requires lawful presence. Consent must be voluntary."
    ))

def add_property_law_rules(db: BlackLetterLawDatabase):
    """Add Property Law black letter rules"""

    # PROPERTY - Estates
    db.add_rule(LegalRule(
        subject="Property",
        topic="Estates",
        subtopic="Present Estates",
        title="Fee Simple Absolute",
        rule="Fee simple absolute is the largest estate in land, with unlimited duration and freely alienable, devisable, and descendible. Created by grant 'to A' or 'to A and his heirs.' Modern rule presumes fee simple absent contrary intent.",
        elements=["Unlimited duration", "Freely transferable", "No conditions or limitations"],
        citations=["Common Law"],
        notes="Magic words 'and his heirs' required at common law but not under modern rule. Most comprehensive estate possible."
    ))

    db.add_rule(LegalRule(
        subject="Property",
        topic="Estates",
        subtopic="Defeasible Fees",
        title="Fee Simple Determinable vs. Fee Simple Subject to Condition Subsequent",
        rule="Fee simple determinable: estate automatically terminates upon occurrence of stated event (durational language: 'so long as,' 'while,' 'during,' 'until'). Grantor retains possibility of reverter. Fee simple subject to condition subsequent: grantor has right to terminate upon occurrence of event (conditional language: 'but if,' 'provided that,' 'on condition that'). Grantor retains right of entry/power of termination.",
        elements=["FS Determinable: automatic termination", "FS Subj to Condition: right to terminate", "Durational vs. conditional language", "Possibility of reverter vs. right of entry"],
        citations=["Restatement (First) of Property § 23"],
        notes="Key difference: determinable ends automatically, condition subsequent requires grantor to exercise right of re-entry. Determinable uses durational language, condition subsequent uses conditional language."
    ))

    # PROPERTY - Adverse Possession
    db.add_rule(LegalRule(
        subject="Property",
        topic="Adverse Possession",
        subtopic="Elements",
        title="Adverse Possession Requirements (COAH)",
        rule="To acquire title by adverse possession, possessor must prove: (1) Continuous possession for statutory period (typically 10-20 years); (2) Open and notorious possession; (3) Actual possession; and (4) Hostile/adverse possession (without owner's permission). Some states also require claim of right or payment of taxes.",
        elements=["Continuous for statutory period", "Open and notorious", "Actual", "Hostile/adverse"],
        citations=["Common Law"],
        notes="COAH mnemonic. Tacking: successive adverse possessors can combine their periods if in privity. Disabilities: statutory period may be tolled if true owner is under disability (minority, insanity) when adverse possession begins."
    ))

    # PROPERTY - Landlord-Tenant
    db.add_rule(LegalRule(
        subject="Property",
        topic="Landlord-Tenant",
        subtopic="Duties",
        title="Implied Warranty of Habitability",
        rule="In residential leases, landlord impliedly warrants that premises are suitable for human habitation and will remain so during tenancy. Applies to latent defects that materially affect habitability (e.g., no heat, water, severe rodent infestation). Breach gives tenant remedies: (1) move out and terminate; (2) repair and deduct; (3) withhold rent; or (4) damages.",
        elements=["Residential lease only", "Latent defects affecting habitability", "Cannot be waived", "Tenant remedies: terminate, repair/deduct, withhold rent, damages"],
        citations=["Javins v. First National Realty Corp., 428 F.2d 1071 (D.C. Cir. 1970)"],
        notes="Modern rule - does not apply to commercial leases. Distinguished from covenant of quiet enjoyment (protects from interference with possession). Tenant must provide notice to landlord and reasonable time to repair."
    ))

    # PROPERTY - Easements
    db.add_rule(LegalRule(
        subject="Property",
        topic="Easements",
        subtopic="Creation",
        title="Easement by Necessity vs. Easement by Implication",
        rule="Easement by necessity: arises when land is subdivided and parcel becomes landlocked with no access to public road. Ends when necessity ends. Easement by implication (quasi-easement): arises from prior use when: (1) common ownership; (2) apparent and continuous use before severance; (3) use reasonably necessary to enjoyment; and (4) parties intended use to continue. Permanent unless stated otherwise.",
        elements=["Necessity: landlocked parcel, strict necessity", "Implication: prior use, apparent, continuous, reasonably necessary, intent", "Necessity is temporary, implication is permanent"],
        citations=["Restatement (Third) of Property (Servitudes) § 2.15"],
        notes="Necessity requires strict necessity (no alternative access). Implication requires only reasonable necessity. Both arise from severance of previously united parcels."
    ))

def main():
    """Expand the black letter law database"""

    print("="*80)
    print("EXPANDING BLACK LETTER LAW DATABASE")
    print("="*80)

    # Load existing database
    db_path = Path(__file__).parent / 'data' / 'black_letter_law.json'
    db = BlackLetterLawDatabase(str(db_path))

    print(f"\nCurrent database: {len(db.rules)} rules")

    # Add new subjects
    print("\n" + "="*80)
    print("ADDING NEW RULES")
    print("="*80)

    print("\nAdding Criminal Law rules...")
    add_criminal_law_rules(db)

    print("Adding Evidence rules...")
    add_evidence_rules(db)

    print("Adding Constitutional Law rules...")
    add_constitutional_law_rules(db)

    print("Adding Property Law rules...")
    add_property_law_rules(db)

    # Save updated database
    db.save_to_file(str(db_path))

    # Show statistics
    stats = db.get_stats()

    print("\n" + "="*80)
    print("UPDATED DATABASE STATISTICS")
    print("="*80)
    print(f"\nTotal Rules: {stats['total_rules']}")
    print(f"Subjects: {stats['subjects']}")
    print(f"Topics: {stats['topics']}")
    print(f"\nSubjects: {', '.join(stats['subjects_list'])}")

    # Show sample rules from each new subject
    print("\n" + "="*80)
    print("SAMPLE RULES FROM NEW SUBJECTS")
    print("="*80)

    # Criminal Law
    murder = db.get_rule('Criminal Law', 'Homicide', 'Murder')
    if murder:
        print(f"\n{'='*80}")
        print(f"CRIMINAL LAW - {murder.title}")
        print(f"{'='*80}")
        print(f"Rule: {murder.rule}")
        print(f"\nElements:")
        for i, elem in enumerate(murder.elements, 1):
            print(f"  ({i}) {elem}")

    # Evidence
    relevance = db.get_rule('Evidence', 'Relevance', 'General Relevance')
    if relevance:
        print(f"\n{'='*80}")
        print(f"EVIDENCE - {relevance.title}")
        print(f"{'='*80}")
        print(f"Rule: {relevance.rule}")
        print(f"\nElements:")
        for i, elem in enumerate(relevance.elements, 1):
            print(f"  ({i}) {elem}")

    # Constitutional Law
    free_speech = db.get_rule('Constitutional Law', 'First Amendment', 'Free Speech')
    if free_speech:
        print(f"\n{'='*80}")
        print(f"CONSTITUTIONAL LAW - {free_speech.title}")
        print(f"{'='*80}")
        print(f"Rule: {free_speech.rule}")
        print(f"\nElements:")
        for i, elem in enumerate(free_speech.elements, 1):
            print(f"  ({i}) {elem}")

    # Property
    fee_simple = db.get_rule('Property', 'Estates', 'Present Estates')
    if fee_simple:
        print(f"\n{'='*80}")
        print(f"PROPERTY - {fee_simple.title}")
        print(f"{'='*80}")
        print(f"Rule: {fee_simple.rule}")
        print(f"\nElements:")
        for i, elem in enumerate(fee_simple.elements, 1):
            print(f"  ({i}) {elem}")

    print("\n" + "="*80)
    print(f"✅ Database expanded and saved to: {db_path}")
    print("="*80)

    # Show all subjects and topics
    print("\n" + "="*80)
    print("COMPLETE DATABASE STRUCTURE")
    print("="*80)

    subjects_dict = {}
    for rule in db.rules:
        if rule.subject not in subjects_dict:
            subjects_dict[rule.subject] = set()
        subjects_dict[rule.subject].add(rule.topic)

    for subject in sorted(subjects_dict.keys()):
        print(f"\n{subject}:")
        for topic in sorted(subjects_dict[subject]):
            topic_rules = [r for r in db.rules if r.subject == subject and r.topic == topic]
            print(f"  • {topic} ({len(topic_rules)} rules)")

if __name__ == '__main__':
    main()

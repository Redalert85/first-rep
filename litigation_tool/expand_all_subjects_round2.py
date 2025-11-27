#!/usr/bin/env python3
"""
Second Round Expansion: Add 5 More Rules to Each Subject
This expands the database from 79 rules to 114 rules (35 new rules)

Expansion breakdown:
- Constitutional Law: 25 → 30 rules
- Evidence: 11 → 16 rules
- Criminal Law: 10 → 15 rules
- Property: 10 → 15 rules
- Torts: 8 → 13 rules
- Contracts: 8 → 13 rules
- Civil Procedure: 7 → 12 rules
"""

import sys
sys.path.insert(0, 'src')
from black_letter_law import BlackLetterLawDatabase, LegalRule

def add_constitutional_law_rules(db: BlackLetterLawDatabase):
    """Add 5 more Constitutional Law rules (25 → 30)"""

    rules = [
        LegalRule(
            subject="Constitutional Law",
            topic="1st Amendment - Freedom of Speech",
            subtopic="Content Regulation",
            title="Content-Based vs Content-Neutral Speech Restrictions",
            rule="Content-based restrictions regulate speech based on subject matter or viewpoint; subject to strict scrutiny (compelling interest + narrowly tailored). Content-neutral restrictions regulate time/place/manner; subject to intermediate scrutiny (significant government interest + narrowly tailored + ample alternative channels). Prior restraints strongly disfavored. Symbolic speech protected if intended to convey message and likely to be understood. Commercial speech: intermediate scrutiny.",
            elements=[
                "Content-based: strict scrutiny (compelling interest + narrowly tailored)",
                "Content-neutral: intermediate scrutiny (significant interest + narrowly tailored + alternatives)",
                "Prior restraints strongly disfavored (heavy presumption against validity)",
                "Symbolic speech: intent to convey message + likelihood of understanding",
                "Commercial speech: intermediate scrutiny (substantial interest + direct advancement + reasonable fit)",
                "Public forum analysis: traditional, designated, limited, non-public"
            ],
            citations=[
                "Reed v. Town of Gilbert, 576 U.S. 155 (2015)",
                "Ward v. Rock Against Racism, 491 U.S. 781 (1989)",
                "Texas v. Johnson, 491 U.S. 397 (1989)",
                "Central Hudson Gas & Elec. v. PSC, 447 U.S. 557 (1980)"
            ],
            notes="Three-tier scrutiny: strict (content-based), intermediate (content-neutral/commercial), rational basis. Time/place/manner must be content-neutral."
        ),

        LegalRule(
            subject="Constitutional Law",
            topic="1st Amendment - Freedom of Press",
            subtopic="Press Rights and Restrictions",
            title="Freedom of the Press - No Special Rights Beyond Speech",
            rule="Press has no greater First Amendment rights than general public. Prior restraints on publication presumptively unconstitutional (Near v. Minnesota). Government cannot compel press to publish (Miami Herald). Press can be required to reveal confidential sources in grand jury proceedings (no reporter's privilege). Broadcast media subject to greater regulation than print (scarcity rationale). No right of access to government information beyond public access.",
            elements=[
                "No special press rights beyond general First Amendment rights",
                "Prior restraints presumptively unconstitutional",
                "Cannot compel publication (editorial discretion protected)",
                "No reporter's privilege from grand jury subpoenas",
                "Broadcast media: greater regulation (scarcity, pervasiveness)",
                "No constitutional right of access to government information"
            ],
            citations=[
                "Near v. Minnesota, 283 U.S. 697 (1931)",
                "New York Times Co. v. United States, 403 U.S. 713 (1971)",
                "Miami Herald Pub. Co. v. Tornillo, 418 U.S. 241 (1974)",
                "Branzburg v. Hayes, 408 U.S. 665 (1972)"
            ],
            notes="Pentagon Papers case: prior restraint rejected even for national security. Press and public treated equally for access purposes."
        ),

        LegalRule(
            subject="Constitutional Law",
            topic="1st Amendment - Assembly and Petition",
            subtopic="Rights to Assemble",
            title="Freedom of Assembly and Petition",
            rule="Right to peaceably assemble protected. Government may impose reasonable time/place/manner restrictions (content-neutral, narrowly tailored, ample alternatives). Permit requirements constitutional if clear standards (no unfettered discretion). Right of association implicit in First Amendment (freedom of expressive association). Government cannot compel disclosure of membership that would chill association. Right to petition includes right to sue government.",
            elements=[
                "Right to peaceably assemble (includes expressive association)",
                "Time/place/manner restrictions: content-neutral + narrowly tailored + alternatives",
                "Permit requirements: clear standards required (no unfettered discretion)",
                "Freedom of association protected from compelled disclosure",
                "Government cannot condition benefits on relinquishing assembly rights",
                "Right to petition: includes right to sue, lobby, communicate with officials"
            ],
            citations=[
                "De Jonge v. Oregon, 299 U.S. 353 (1937)",
                "NAACP v. Alabama, 357 U.S. 449 (1958)",
                "NAACP v. Button, 371 U.S. 415 (1963)",
                "Boy Scouts of America v. Dale, 530 U.S. 640 (2000)"
            ],
            notes="Assembly and petition often overlap with speech. Expressive association protects groups from forced inclusion that would affect message."
        ),

        LegalRule(
            subject="Constitutional Law",
            topic="4th Amendment - Searches and Seizures",
            subtopic="Reasonable Expectation of Privacy",
            title="Reasonable Expectation of Privacy - Katz Test",
            rule="Fourth Amendment protects against unreasonable searches and seizures. Search occurs when government violates reasonable expectation of privacy: (1) subjective expectation of privacy; AND (2) expectation society recognizes as reasonable. No REP in: open fields, curtilage protected, aerial surveillance (public navigable airspace), garbage left for collection, pen registers, GPS tracking long-term may require warrant, third-party doctrine (info voluntarily given to third parties).",
            elements=[
                "Katz test: (1) subjective expectation + (2) objectively reasonable",
                "No REP in open fields (Oliver)",
                "Curtilage protected (area immediately surrounding home)",
                "Third-party doctrine: no REP in info given to third parties",
                "Garbage: no REP once placed for collection",
                "Technology: thermal imaging (Kyllo), GPS long-term (Jones), cell-site data (Carpenter)"
            ],
            citations=[
                "Katz v. United States, 389 U.S. 347 (1967)",
                "Oliver v. United States, 466 U.S. 170 (1984)",
                "California v. Greenwood, 486 U.S. 35 (1988)",
                "United States v. Jones, 565 U.S. 400 (2012)",
                "Carpenter v. United States, 138 S. Ct. 2206 (2018)"
            ],
            notes="Modern technology cases expanding privacy protections: Kyllo (thermal imaging), Jones (GPS), Riley (cell phones), Carpenter (CSLI)."
        ),

        LegalRule(
            subject="Constitutional Law",
            topic="5th Amendment - Double Jeopardy",
            subtopic="Protection Against Multiple Prosecutions",
            title="Double Jeopardy Clause",
            rule="No person shall be twice put in jeopardy for same offense. Three protections: (1) no re-prosecution after acquittal; (2) no re-prosecution after conviction; (3) no multiple punishments for same offense. Jeopardy attaches: jury trial when jury sworn; bench trial when first witness sworn. Same offense: Blockburger test (each statute requires proof of element other does not). Exceptions: hung jury, mistrial for manifest necessity, successful appeal, separate sovereigns.",
            elements=[
                "Three protections: no second prosecution after acquittal/conviction; no multiple punishments",
                "Jeopardy attaches: jury sworn (jury trial) or first witness (bench trial)",
                "Blockburger test: same offense if each statute doesn't require unique element",
                "Acquittal bars re-prosecution even if legally erroneous",
                "Conviction bars re-prosecution for same offense",
                "Exceptions: hung jury, manifest necessity, defendant's appeal, separate sovereigns"
            ],
            citations=[
                "Blockburger v. United States, 284 U.S. 299 (1932)",
                "Benton v. Maryland, 395 U.S. 784 (1969)",
                "Ashe v. Swenson, 397 U.S. 436 (1970)",
                "United States v. Dixon, 509 U.S. 688 (1993)"
            ],
            notes="Separate sovereigns: state and federal governments can each prosecute. Collateral estoppel applies (issue preclusion). Lesser included offenses implicitly acquitted."
        )
    ]

    for rule in rules:
        db.add_rule(rule)
    print(f"✓ Added 5 Constitutional Law rules (25 → 30)")


def add_evidence_rules(db: BlackLetterLawDatabase):
    """Add 5 more Evidence rules (11 → 16)"""

    rules = [
        LegalRule(
            subject="Evidence",
            topic="Hearsay Exceptions",
            subtopic="Present Sense Impression",
            title="Hearsay Exception - Present Sense Impression (FRE 803(1))",
            rule="Statement describing or explaining event or condition, made while or immediately after declarant perceived it. No time for reflection or fabrication. Requirements: (1) statement describes event; (2) made while perceiving or immediately thereafter; (3) no time for reflective thought. Personal knowledge required. No unavailability requirement.",
            elements=[
                "Statement describes/explains event or condition",
                "Made while perceiving OR immediately after",
                "Contemporaneous (no time for fabrication)",
                "Personal knowledge required",
                "Declarant availability irrelevant (803 exception)",
                "Corroboration often required (independent evidence event occurred)"
            ],
            citations=[
                "FRE 803(1)",
                "United States v. Mitchell, 145 F.3d 572 (3d Cir. 1998)"
            ],
            notes="Distinguished from excited utterance: no stress required but must be truly contemporaneous. Often used for 911 calls if immediate."
        ),

        LegalRule(
            subject="Evidence",
            topic="Hearsay Exceptions",
            subtopic="Excited Utterance",
            title="Hearsay Exception - Excited Utterance (FRE 803(2))",
            rule="Statement relating to startling event, made while declarant under stress of excitement caused by event. Requirements: (1) startling event; (2) statement relates to event; (3) made while under stress of excitement (no time for reflective thought). Time lapse flexible if excitement continues. More leeway than present sense impression.",
            elements=[
                "Startling event or condition",
                "Statement relates to startling event",
                "Made while under stress of excitement",
                "No opportunity for reflective thought",
                "Time lapse flexible (depends on nature of event)",
                "Declarant availability irrelevant"
            ],
            citations=[
                "FRE 803(2)",
                "United States v. Napier, 518 F.2d 316 (9th Cir. 1975)"
            ],
            notes="Focus on declarant's state of mind (excited/stressed), not timing. Serious events may excuse longer delays. Common in domestic violence cases."
        ),

        LegalRule(
            subject="Evidence",
            topic="Hearsay Exceptions",
            subtopic="Then-Existing Condition",
            title="Then-Existing Mental, Emotional, or Physical Condition (FRE 803(3))",
            rule="Statement of declarant's then-existing state of mind (intent, motive, plan), emotion, sensation, or physical condition. Admissible for declarant's then-existing condition or to prove future conduct in accordance with stated intent. NOT admissible for memory or belief to prove past fact. Exception: will cases (testator's state of mind re: will execution).",
            elements=[
                "Statement of then-existing mental/emotional/physical condition",
                "Admissible to show declarant's state of mind at that time",
                "Forward-looking: proves future conduct per stated intent (Hillmon)",
                "NOT backward-looking: excludes memory/belief of past facts",
                "Exception: will cases (testator's mental state)",
                "No unavailability requirement"
            ],
            citations=[
                "FRE 803(3)",
                "Mutual Life Ins. Co. v. Hillmon, 145 U.S. 285 (1892)",
                "Shepard v. United States, 290 U.S. 96 (1933)"
            ],
            notes="'I intend to go to Kansas' admissible to prove went to Kansas. 'I went to Kansas' NOT admissible under 803(3). Doctor testimony re: patient statements of pain."
        ),

        LegalRule(
            subject="Evidence",
            topic="Hearsay Exceptions",
            subtopic="Medical Diagnosis",
            title="Statement for Medical Diagnosis or Treatment (FRE 803(4))",
            rule="Statement made for medical diagnosis or treatment, describing medical history, symptoms, pain, sensation, inception/cause if reasonably pertinent to treatment. Requirements: (1) made for medical diagnosis/treatment; (2) reasonably pertinent to diagnosis/treatment; (3) declarant has motive to be truthful. Includes statements to doctors, nurses, EMTs, family relaying to doctors. Cause admissible if pertinent to treatment.",
            elements=[
                "Made for medical diagnosis or treatment",
                "Reasonably pertinent to diagnosis/treatment",
                "Includes: history, symptoms, pain, inception, cause",
                "Declarant motivated to be truthful (self-interest in treatment)",
                "Identity of perpetrator admissible if pertinent (abuse cases)",
                "Includes statements to any medical personnel"
            ],
            citations=[
                "FRE 803(4)",
                "United States v. Renville, 779 F.2d 430 (8th Cir. 1985)"
            ],
            notes="Fault admissible if relevant to treatment (e.g., type of blow in abuse). Child abuse cases: identity may be pertinent to treatment for psychological trauma."
        ),

        LegalRule(
            subject="Evidence",
            topic="Hearsay Exceptions",
            subtopic="Recorded Recollection",
            title="Past Recollection Recorded (FRE 803(5))",
            rule="Record on matter witness once knew but now cannot recall well enough to testify fully and accurately. Requirements: (1) insufficient memory at trial; (2) record made/adopted when fresh in memory; (3) record accurately reflects knowledge; (4) witness can verify accuracy. If admitted, READ to jury but NOT received as exhibit unless offered by opponent. Distinguished from refreshing recollection (FRE 612).",
            elements=[
                "Insufficient memory at trial (present recollection failure)",
                "Record made when matter fresh in memory",
                "Record accurately reflects witness's knowledge",
                "Witness can verify/adopt record's accuracy",
                "If admitted: read to jury, NOT received as exhibit",
                "Opponent may offer as exhibit"
            ],
            citations=[
                "FRE 803(5)",
                "United States v. Williams, 571 F.2d 344 (6th Cir. 1978)"
            ],
            notes="Distinguished from FRE 612 (refreshing): 803(5) requires insufficient memory; witness need not have made record personally if adopted it. Record stays out of jury room."
        )
    ]

    for rule in rules:
        db.add_rule(rule)
    print(f"✓ Added 5 Evidence rules (11 → 16)")


def add_criminal_law_rules(db: BlackLetterLawDatabase):
    """Add 5 more Criminal Law rules (10 → 15)"""

    rules = [
        LegalRule(
            subject="Criminal Law",
            topic="Inchoate Crimes",
            subtopic="Attempt",
            title="Attempt Elements and Defenses",
            rule="Attempt requires: (1) specific intent to commit target crime; AND (2) substantial step toward commission beyond mere preparation. Defenses: legal impossibility (act if completed would not be crime); factual impossibility NOT a defense; abandonment (MPC: complete and voluntary renunciation before crime committed). Merger: attempt merges into completed crime.",
            elements=[
                "Specific intent to commit target crime (even if target crime is general intent)",
                "Substantial step toward commission (beyond mere preparation)",
                "Proximity test vs. substantial step test (MPC more lenient)",
                "Legal impossibility: defense (act not criminal)",
                "Factual impossibility: NOT defense (if facts as believed, would be crime)",
                "Abandonment: complete and voluntary (MPC)",
                "Merger: attempt merges into completed crime"
            ],
            citations=[
                "MPC § 5.01",
                "United States v. Jackson, 560 F.2d 112 (2d Cir. 1977)"
            ],
            notes="Substantial step requires conduct strongly corroborative of criminal purpose. Lying in wait, searching for victim, possessing materials at scene qualify."
        ),

        LegalRule(
            subject="Criminal Law",
            topic="Inchoate Crimes",
            subtopic="Solicitation",
            title="Solicitation Elements",
            rule="Solicitation: (1) asking, encouraging, or commanding another person; (2) to commit a crime; (3) with intent that crime be committed. Crime complete when request made (no agreement required). Defenses: renunciation (MPC: complete and voluntary, prevents crime). Merger: solicitation merges into conspiracy if other party agrees; merges into completed crime.",
            elements=[
                "Asking, encouraging, requesting, or commanding",
                "Another person to commit crime",
                "Specific intent that crime be committed",
                "Complete when request made (no acceptance required)",
                "Cannot solicit lawful act",
                "Renunciation defense (MPC): complete, voluntary, prevents commission",
                "Merger: into conspiracy (if agreement) and completed crime"
            ],
            citations=[
                "MPC § 5.02"
            ],
            notes="Solicitation is first step toward inchoate liability. Merges into conspiracy or target crime but not attempt."
        ),

        LegalRule(
            subject="Criminal Law",
            topic="Inchoate Crimes",
            subtopic="Conspiracy",
            title="Conspiracy Elements and Liability",
            rule="Conspiracy: (1) agreement between two or more persons; (2) intent to agree; (3) intent to achieve unlawful objective. Common law: bilateral (two guilty minds). MPC: unilateral (one person with intent suffices). Overt act required (federal/MPC) unless crime of violence. Co-conspirator liability: liable for all crimes in furtherance committed by co-conspirators. Withdrawal: not defense to conspiracy but cuts off liability for future crimes (communicate to all members OR notify authorities).",
            elements=[
                "Agreement between two or more persons",
                "Intent to agree",
                "Intent to achieve unlawful objective",
                "Overt act required (federal/MPC) unless violent crime",
                "Bilateral vs. unilateral approach (MPC)",
                "Wharton Rule: crime requiring two persons (no conspiracy unless more parties)",
                "Pinkerton liability: liable for foreseeable crimes in furtherance",
                "Withdrawal: communicate renunciation to all OR notify police"
            ],
            citations=[
                "Pinkerton v. United States, 328 U.S. 640 (1946)",
                "MPC § 5.03"
            ],
            notes="Conspiracy does NOT merge into completed crime. Each conspirator liable for all co-conspirators' crimes in furtherance if foreseeable. Wheel vs. chain conspiracies."
        ),

        LegalRule(
            subject="Criminal Law",
            topic="Crimes Against the Person",
            subtopic="Assault",
            title="Assault (Criminal)",
            rule="Assault defined as: (1) attempt to commit battery (attempted battery assault); OR (2) intentional creation of reasonable apprehension of imminent harmful/offensive contact (fear assault). Requirements vary by jurisdiction. Words alone generally insufficient (must be accompanied by conduct). Conditional threat ('your money or your life') may suffice. Aggravated assault: with deadly weapon, intent to rape/rob/kill, or causes serious bodily injury.",
            elements=[
                "Attempted battery: intent + substantial step toward battery",
                "OR Apprehension: intent to create fear + reasonable apprehension + imminent",
                "No actual contact required (distinguishes from battery)",
                "Words alone generally insufficient (conduct required)",
                "Victim awareness required (for apprehension type)",
                "Aggravating factors: deadly weapon, intent for felony, serious injury"
            ],
            citations=[
                "MPC § 211.1"
            ],
            notes="Two types: attempted battery (closer to attempt) and apprehension (distinct crime). Modern statutes often combine. Mens rea: specific intent."
        ),

        LegalRule(
            subject="Criminal Law",
            topic="Theft Crimes",
            subtopic="False Pretenses",
            title="False Pretenses vs. Larceny by Trick",
            rule="False pretenses: (1) obtaining title to property; (2) by false representation of material past/present fact; (3) with intent to defraud; (4) victim relies and passes title. Distinguished from larceny by trick: false pretenses passes TITLE; larceny by trick passes only POSSESSION. Must be factual misrepresentation (not opinion/puffery). Future promises insufficient unless no intent to perform.",
            elements=[
                "False representation of material past or present fact",
                "Knowledge of falsity (scienter)",
                "Intent to defraud (obtain title)",
                "Victim relies on misrepresentation",
                "Victim passes TITLE to property (not just possession)",
                "Factual misrepresentation (not opinion, prediction, or puffery)"
            ],
            citations=[
                "MPC § 223.3"
            ],
            notes="Title vs. Possession: false pretenses (title), larceny by trick (possession), embezzlement (lawful possession → conversion). Modern theft statutes consolidate."
        )
    ]

    for rule in rules:
        db.add_rule(rule)
    print(f"✓ Added 5 Criminal Law rules (10 → 15)")


def add_property_rules(db: BlackLetterLawDatabase):
    """Add 5 more Property rules (10 → 15)"""

    rules = [
        LegalRule(
            subject="Property",
            topic="Future Interests",
            subtopic="Rule Against Perpetuities",
            title="Rule Against Perpetuities (RAP)",
            rule="No interest is good unless it must vest, if at all, not later than 21 years after some life in being at creation of interest. Applies to: contingent remainders, executory interests, vested remainders subject to open (class gifts). Does NOT apply to: reversion, possibility of reverter, right of entry, vested remainders. Test: might interest vest too remotely? If yes, strike interest. Charity-to-charity and options in gross may have special rules.",
            elements=[
                "Must vest if at all within lives in being plus 21 years",
                "Applies to: contingent remainders, executory interests, class gifts",
                "NOT applicable to: reversions, possibilities of reverter, rights of entry",
                "Measured from creation: will (death), deed (delivery), irrevocable trust (creation)",
                "What-might-happen test (not what actually happens)",
                "Common pitfalls: fertile octogenarian, unborn widow, administrative contingency",
                "Reforms: wait-and-see, cy pres, USRAP (90 years)"
            ],
            citations=[
                "Duke of Norfolk's Case (1681)",
                "Uniform Statutory Rule Against Perpetuities (USRAP)"
            ],
            notes="Classic traps: gift to children who reach 25 (void - could vest beyond 21 years after lives in being). RAP invalidates only offending interest."
        ),

        LegalRule(
            subject="Property",
            topic="Easements",
            subtopic="Creation",
            title="Creation of Easements",
            rule="Easement: non-possessory right to use another's land. Created by: (1) express grant/reservation (writing required - Statute of Frauds); (2) implied from prior use (quasi-easement: apparent, continuous, reasonably necessary); (3) implied by necessity (strict necessity, landlocked); (4) prescription (adverse use: open, notorious, continuous, hostile, for statutory period). Appurtenant: benefits land (runs with land). In gross: benefits person (generally non-transferable unless commercial).",
            elements=[
                "Express: writing required (SOF), clear intent, properly described",
                "Implied from prior use: common owner, apparent, continuous, reasonably necessary",
                "Necessity: strict necessity, landlocked, unity of ownership then severance",
                "Prescription: COHAN (Continuous, Open, Hostile, Actual, Notorious) for statutory period",
                "Appurtenant: benefits dominant tenement, burdens servient",
                "In gross: personal to holder (non-transferable unless commercial)"
            ],
            citations=[
                "Van Sandt v. Royster, 83 P.2d 698 (Kan. 1938)"
            ],
            notes="Easement by necessity: strict necessity (landlocked). Implied from prior use: reasonable necessity (less than strict). Prescription: like adverse possession but use, not possession."
        ),

        LegalRule(
            subject="Property",
            topic="Easements",
            subtopic="Termination",
            title="Termination of Easements",
            rule="Easements terminated by: (1) expiration (stated term); (2) merger (unity of ownership of dominant/servient); (3) release (writing from dominant to servient); (4) abandonment (intent to abandon + physical act); (5) estoppel (servient owner reasonably relies on cessation); (6) prescription (servient owner adversely interferes for statutory period); (7) condemnation; (8) changed conditions (neighborhood change makes easement obsolete). Mere non-use insufficient for abandonment.",
            elements=[
                "Expiration: stated time period ends",
                "Merger: same owner acquires dominant and servient estates",
                "Release: writing required (dominant releases to servient)",
                "Abandonment: intent + physical act (non-use alone insufficient)",
                "Estoppel: servient relies on representations of abandonment",
                "Prescription: servient adversely interferes for statutory period",
                "Changed conditions: renders easement obsolete (difficult)",
                "Condemnation: government takes servient estate"
            ],
            citations=[
                "Preseault v. United States, 100 F.3d 1525 (Fed. Cir. 1996)"
            ],
            notes="Most common: merger and release. Abandonment requires more than non-use (need intent + act inconsistent with easement). Prescription to terminate mirrors prescription to create."
        ),

        LegalRule(
            subject="Property",
            topic="Landlord-Tenant",
            subtopic="Types of Tenancies",
            title="Types of Leasehold Estates",
            rule="Four types: (1) Term of Years: fixed period, no notice to terminate, ends automatically; (2) Periodic Tenancy: continuous periods (month-to-month), auto-renews, notice to terminate (common law: 6 months for year-to-year, period for others); (3) Tenancy at Will: no fixed duration, terminable by either party (reasonable notice), ends at death of party; (4) Tenancy at Sufferance: holdover tenant (not trespasser but not valid tenant), landlord may evict or hold to new term.",
            elements=[
                "Term of Years: fixed start and end, automatic termination, SOF if >1 year",
                "Periodic: continuous auto-renewing periods, notice required to terminate",
                "At Will: terminable anytime, reasonable notice, death terminates",
                "At Sufferance: holdover tenant (wrongful possession), landlord's options",
                "Notice to terminate periodic: common law 6 months (year-to-year), equal to period (others)",
                "Statute of Frauds: leases >1 year must be in writing"
            ],
            citations=[
                "Restatement (Second) of Property: Landlord and Tenant"
            ],
            notes="Holdover: landlord may evict OR hold to another term (usually periodic). Option to hold may be limited by statute. Residential: often periodic (month-to-month)."
        ),

        LegalRule(
            subject="Property",
            topic="Landlord-Tenant",
            subtopic="Duties and Remedies",
            title="Landlord and Tenant Duties and Remedies",
            rule="Landlord duties: (1) deliver possession (majority: actual; minority: legal); (2) covenant of quiet enjoyment (no interference); (3) implied warranty of habitability (residential: safe, sanitary, fit for living - not waivable). Tenant remedies: breach of IWH: repair/deduct, withhold rent, terminate, damages. Tenant duties: pay rent, avoid waste (voluntary, permissive, ameliorative). Constructive eviction: substantial interference + notice + vacate.",
            elements=[
                "Deliver possession: majority (English rule) requires actual; minority (American) legal only",
                "Quiet enjoyment: no interference by landlord (actual or constructive eviction)",
                "Implied warranty of habitability: residential only, not waivable, serious defects",
                "IWH remedies: move out, repair/deduct, withhold rent, terminate, damages",
                "Constructive eviction: substantial interference + notice + tenant vacates",
                "Tenant duties: pay rent, avoid waste, return possession",
                "Assignment vs. sublease: assignment (full term/privity), sublease (less than full)"
            ],
            citations=[
                "Javins v. First Nat'l Realty Corp., 428 F.2d 1071 (D.C. Cir. 1970)",
                "Reste Realty Corp. v. Cooper, 251 A.2d 268 (N.J. 1969)"
            ],
            notes="IWH revolution: tenant not required to vacate for breach (unlike constructive eviction). Remedies cumulative. Applies residential only (some jurisdictions commercial too)."
        )
    ]

    for rule in rules:
        db.add_rule(rule)
    print(f"✓ Added 5 Property rules (10 → 15)")


def add_torts_rules(db: BlackLetterLawDatabase):
    """Add 5 more Torts rules (8 → 13)"""

    rules = [
        LegalRule(
            subject="Torts",
            topic="Intentional Torts",
            subtopic="Trespass to Land",
            title="Trespass to Land Elements",
            rule="Trespass to land: (1) act by defendant; (2) intent to enter land (or cause object/person to enter); (3) physical invasion of plaintiff's real property; (4) causation. Intent to trespass NOT required (only intent to enter); mistake of fact (boundary) no defense. Entitled to nominal damages without proof of actual harm. Above/below surface included (reasonable height/depth).",
            elements=[
                "Volitional act",
                "Intent to enter (or cause entry) - NOT intent to trespass",
                "Physical invasion of land (defendant or object/third person)",
                "Plaintiff has possessory interest in land",
                "Mistake no defense",
                "Nominal damages available (no actual harm required)"
            ],
            citations=[
                "Dougherty v. Stepp, 18 N.C. 371 (1835)",
                "Restatement (Second) of Torts § 158"
            ],
            notes="Distinguished from nuisance (interference with use/enjoyment). Includes entry by object, person, or particles. Airspace: reasonable altitude. Subterranean: reasonable depth."
        ),

        LegalRule(
            subject="Torts",
            topic="Intentional Torts",
            subtopic="Trespass to Chattels",
            title="Trespass to Chattels vs. Conversion",
            rule="Trespass to chattels: (1) act by defendant; (2) intent to interfere with plaintiff's chattel; (3) interference (intermeddling or dispossession); (4) causation; (5) actual damages required. Distinguished from conversion: trespass = minor interference; conversion = serious interference (requires full value). Factors: extent/duration of interference, harm, inconvenience, intent to assert right, good faith.",
            elements=[
                "Volitional act",
                "Intent to interfere with chattel",
                "Interference: intermeddling (physical contact) or dispossession",
                "Causation",
                "Actual damages required (unlike conversion)",
                "Temporary interference or minor damage"
            ],
            citations=[
                "CompuServe Inc. v. Cyber Promotions, Inc., 962 F. Supp. 1015 (S.D. Ohio 1997)",
                "Restatement (Second) of Torts § 217"
            ],
            notes="Modern: applies to electronic data (spam, computer trespass). Remedy: actual damages. If serious enough, becomes conversion (liable for full value)."
        ),

        LegalRule(
            subject="Torts",
            topic="Intentional Torts",
            subtopic="Conversion",
            title="Conversion Elements and Remedy",
            rule="Conversion: (1) act by defendant; (2) intent to exercise dominion/control over chattel; (3) serious interference with plaintiff's possessory rights; (4) causation. Seriousness factors: extent/duration, harm, inconvenience, intent, good faith. Remedy: forced sale - defendant liable for full fair market value. Defendant may keep chattel. Mistake no defense. Includes: taking, destruction, use, refusing to return.",
            elements=[
                "Volitional act",
                "Intent to exercise dominion/control",
                "Serious interference with possessory rights",
                "Plaintiff entitled to possession",
                "Causation",
                "Remedy: forced sale (full FMV)"
            ],
            citations=[
                "Pearson v. Dodd, 410 F.2d 701 (D.C. Cir. 1969)",
                "Restatement (Second) of Torts § 222A"
            ],
            notes="Conversion = serious interference; trespass to chattels = minor. Good faith irrelevant. Purchasing stolen goods = conversion. Bailment: failure to return on demand."
        ),

        LegalRule(
            subject="Torts",
            topic="Dignitary Torts",
            subtopic="Defamation",
            title="Defamation - Libel and Slander Elements",
            rule="Defamation: (1) defamatory statement (harms reputation); (2) of and concerning plaintiff; (3) publication (communication to third party); (4) damages; (5) fault (negligence for private figure, actual malice for public figure/matter). Libel: written, broadcast (presumed damages). Slander: spoken (actual damages required unless slander per se). Slander per se: crime, loathsome disease, business/profession, sexual misconduct. Constitutional requirements: public figure/matter requires actual malice (knowledge of falsity or reckless disregard).",
            elements=[
                "Defamatory statement (lowers reputation in community)",
                "Of and concerning plaintiff (identifies plaintiff)",
                "Publication to third party (intent or negligence)",
                "Damages: libel (presumed), slander (actual unless per se)",
                "Fault: private figure (negligence), public (actual malice)",
                "Truth is absolute defense (CL/modern)"
            ],
            citations=[
                "New York Times Co. v. Sullivan, 376 U.S. 254 (1964)",
                "Gertz v. Robert Welch, Inc., 418 U.S. 323 (1974)",
                "Restatement (Second) of Torts § 558"
            ],
            notes="Public figure: actual malice (knowledge of falsity or reckless disregard). Opinion protected if no implied false facts. Privileges: absolute (judicial, legislative), qualified (interest)."
        ),

        LegalRule(
            subject="Torts",
            topic="Dignitary Torts",
            subtopic="Privacy",
            title="Invasion of Privacy - Four Torts",
            rule="Four privacy torts: (1) Intrusion upon seclusion: intentional intrusion (physical/otherwise) into private affairs, offensive to reasonable person; (2) Appropriation: use of name/likeness for commercial benefit without consent; (3) False light: publicity placing plaintiff in false light, highly offensive, actual malice if public figure; (4) Public disclosure of private facts: public disclosure of private matters, highly offensive, not newsworthy. No privacy for deceased.",
            elements=[
                "Intrusion: physical/electronic invasion, private place, highly offensive",
                "Appropriation: name/likeness, commercial use, without consent",
                "False light: public portrayal, false impression, highly offensive, actual malice (public)",
                "Private facts: public disclosure, private matter, not newsworthy, highly offensive",
                "Generally: no liability for deceased's privacy",
                "Truth not defense (for private facts)"
            ],
            citations=[
                "Restatement (Second) of Torts § 652A-E",
                "Prosser, Privacy, 48 Cal. L. Rev. 383 (1960)"
            ],
            notes="Intrusion: paparazzi, wiretapping, peeping. Appropriation: right of publicity (commercial). False light: overlaps defamation but broader. Private facts: truth no defense; newsworthiness defense."
        )
    ]

    for rule in rules:
        db.add_rule(rule)
    print(f"✓ Added 5 Torts rules (8 → 13)")


def add_contracts_rules(db: BlackLetterLawDatabase):
    """Add 5 more Contracts rules (8 → 13)"""

    rules = [
        LegalRule(
            subject="Contracts",
            topic="Contract Formation",
            subtopic="Offer and Acceptance",
            title="Offer and Acceptance - Mutual Assent",
            rule="Offer: manifestation of willingness to enter bargain, creates power of acceptance. Requirements: (1) expression of promise/commitment; (2) certainty of terms; (3) communication to offeree. Terminates by: rejection, counteroffer, lapse of time, revocation, death/incapacity. Acceptance: (1) manifestation of assent; (2) by offeree; (3) according to terms of offer. Mailbox rule: acceptance effective upon dispatch (not receipt); revocation effective upon receipt.",
            elements=[
                "Offer: promise + certainty + communication",
                "Definite terms: parties, subject matter, price, quantity (UCC: quantity only)",
                "Termination: rejection, counteroffer, lapse, revocation, death",
                "Acceptance: assent + by offeree + per offer terms",
                "Mailbox rule: acceptance upon dispatch; revocation upon receipt",
                "Mirror image (CL) vs. additional terms (UCC 2-207)"
            ],
            citations=[
                "Restatement (Second) of Contracts § 24, 50",
                "UCC § 2-206, 2-207"
            ],
            notes="Advertisements: generally invitations to offer (not offers). Option contracts: irrevocable if supported by consideration. Firm offer (UCC): merchant, writing, signed, max 3 months."
        ),

        LegalRule(
            subject="Contracts",
            topic="Contract Formation",
            subtopic="Consideration",
            title="Consideration and Its Substitutes",
            rule="Consideration: (1) bargained-for exchange; (2) legal detriment to promisee OR benefit to promisor. Requirements: something of legal value + induces promise + promise induces it. Adequacy irrelevant (courts won't inquire into sufficiency). Illusory promise: no consideration (no commitment). Past consideration: not consideration. Pre-existing duty rule: performance of existing duty not consideration (exceptions: new/different consideration, unforeseen circumstances, UCC modification in good faith).",
            elements=[
                "Bargained-for exchange",
                "Legal detriment to promisee OR benefit to promisor",
                "Inducement (mutual: each induces other)",
                "Adequacy irrelevant (sufficiency required)",
                "Illusory promise: not consideration",
                "Past consideration: not consideration",
                "Pre-existing duty: not consideration (unless modification exception)"
            ],
            citations=[
                "Restatement (Second) of Contracts § 71",
                "Hamer v. Sidway, 124 N.Y. 538 (1891)"
            ],
            notes="Substitutes for consideration: promissory estoppel (detrimental reliance), seal (some jurisdictions), moral obligation + material benefit. UCC: modification needs no consideration if good faith."
        ),

        LegalRule(
            subject="Contracts",
            topic="Contract Modification",
            subtopic="Common Law vs UCC",
            title="Contract Modification - Common Law vs. UCC",
            rule="Common law: modification requires new consideration (pre-existing duty rule applies). Exceptions: unforeseen circumstances, additional duties, rescission and new contract. UCC § 2-209: modification needs NO consideration if (1) good faith; AND (2) not violating SOF if modified contract within SOF. Bad faith modification: economic duress, no consideration. No-oral-modification clause: UCC requires written modification if clause present (unless waived).",
            elements=[
                "Common law: new consideration required for modification",
                "Exceptions: unforeseen circumstances, additional/different duties",
                "UCC: no consideration required if good faith",
                "Bad faith: economic duress renders modification voidable",
                "SOF: modified contract must comply if within SOF",
                "No-oral-modification clause: UCC enforces (absent waiver)"
            ],
            citations=[
                "Restatement (Second) of Contracts § 89",
                "UCC § 2-209"
            ],
            notes="Pre-existing duty rule: strict common law. UCC more flexible: good faith required. Economic duress: improper threat + no reasonable alternative. Waiver: conduct inconsistent with clause."
        ),

        LegalRule(
            subject="Contracts",
            topic="Third Party Rights",
            subtopic="Third Party Beneficiaries",
            title="Third Party Beneficiary Rights",
            rule="Third party beneficiary (TPB) may enforce contract if (1) parties intended to benefit TPB; AND (2) enforcement necessary to satisfy obligee's duty. Intended beneficiary: creditor beneficiary (obligee owes debt to TPB) or donee beneficiary (obligee intends gift to TPB). Incidental beneficiary: no rights. TPB rights vest when: (1) manifests assent; (2) materially changes position; OR (3) files suit. After vesting, parties cannot modify without TPB consent.",
            elements=[
                "Intended beneficiary: parties intended to benefit (creditor or donee)",
                "Creditor beneficiary: obligee owes duty to TPB",
                "Donee beneficiary: obligee intends gift to TPB",
                "Incidental beneficiary: no enforcement rights",
                "Vesting: assent, detrimental reliance, or filing suit",
                "After vesting: cannot modify without TPB consent"
            ],
            citations=[
                "Restatement (Second) of Contracts § 302, 311",
                "Lawrence v. Fox, 20 N.Y. 268 (1859)"
            ],
            notes="Test: did parties intend to benefit TPB at time of contracting? Government contracts: typically no TPB rights (citizens incidental). Vesting locks in rights."
        ),

        LegalRule(
            subject="Contracts",
            topic="Third Party Rights",
            subtopic="Assignment and Delegation",
            title="Assignment and Delegation of Contract Rights",
            rule="Assignment: transfer of rights (benefits) to assignee. Delegation: transfer of duties (obligations) to delegatee. Assignment requirements: (1) manifest intent to transfer; (2) no consideration required; (3) writing not required unless SOF applies. Rights assignable unless: (1) substantially changes obligor's duty/risk; (2) personal services; (3) contract prohibits (UCC: prohibition ineffective for payment rights). Delegation: duties delegable unless personal services or contract prohibits. Delegator remains liable.",
            elements=[
                "Assignment: transfers rights; no consideration required",
                "Delegation: transfers duties; delegator remains liable",
                "Non-assignable: material change to obligor duty/risk, personal services, prohibition",
                "UCC: prohibition on assignment of payment rights ineffective",
                "Notice to obligor: required for assignment (prevents paying assignor)",
                "Revocability: gratuitous assignment revocable (until performance/token/writing)",
                "Delegation: prohibited if personal services or contract bars"
            ],
            citations=[
                "Restatement (Second) of Contracts § 317, 318",
                "UCC § 2-210"
            ],
            notes="'All my rights under the contract' = assignment only. 'All my rights and delegates duties' = assignment + delegation. Delegatee not liable unless assumes (promise to delegator)."
        )
    ]

    for rule in rules:
        db.add_rule(rule)
    print(f"✓ Added 5 Contracts rules (8 → 13)")


def add_civil_procedure_rules(db: BlackLetterLawDatabase):
    """Add 5 more Civil Procedure rules (7 → 12)"""

    rules = [
        LegalRule(
            subject="Civil Procedure",
            topic="Pleadings",
            subtopic="Rule 8 Requirements",
            title="Pleading Requirements - FRCP Rule 8",
            rule="Rule 8(a) complaint requires: (1) jurisdictional statement; (2) short and plain statement showing entitlement to relief; (3) demand for judgment/relief. Plausibility standard (Twombly/Iqbal): factual allegations must plausibly suggest claim (more than possible, less than probable). Notice pleading: labels and conclusions insufficient; must plead facts. Fraud, mistake, special damages: particularity required (Rule 9).",
            elements=[
                "Jurisdictional statement (subject matter jurisdiction basis)",
                "Short and plain statement of claim showing entitlement to relief",
                "Demand for judgment/relief sought",
                "Plausibility: factual allegations plausibly suggest claim (Twombly/Iqbal)",
                "Conclusory statements insufficient",
                "Rule 9(b): fraud/mistake require particularity (who, what, when, where)",
                "Rule 9(g): special damages require specificity"
            ],
            citations=[
                "FRCP Rule 8, 9",
                "Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)",
                "Ashcroft v. Iqbal, 556 U.S. 662 (2009)"
            ],
            notes="Twombly/Iqbal two-step: (1) identify conclusory allegations (disregard); (2) accept remaining factual allegations, determine plausibility. Heightened pleading for fraud/mistake only."
        ),

        LegalRule(
            subject="Civil Procedure",
            topic="Pleadings",
            subtopic="Rule 11 Sanctions",
            title="Rule 11 Sanctions for Frivolous Filings",
            rule="Rule 11: attorney/party certifies that (1) not for improper purpose (harassment, delay); (2) legal contentions warranted by law or nonfrivolous argument for change; (3) factual contentions have evidentiary support or likely after investigation; (4) denials warranted. Violation: court may impose sanctions (reasonable attorney's fees). Safe harbor: 21-day notice before filing motion (except dismissals). Sanctions: deterrence, not compensation.",
            elements=[
                "Certification by signing: reasonable inquiry into facts and law",
                "Not for improper purpose (harassment, delay, increase costs)",
                "Legal contentions: warranted by law or nonfrivolous extension/change",
                "Factual contentions: evidentiary support or likely after investigation",
                "Denials: warranted on evidence or reasonably based on lack of info",
                "Safe harbor: 21 days to withdraw/correct before sanctions motion filed",
                "Sanctions: deterrent purpose (may include attorney's fees)"
            ],
            citations=[
                "FRCP Rule 11",
                "Business Guides, Inc. v. Chromatic Commc'ns Enters., 498 U.S. 533 (1991)"
            ],
            notes="Objective standard: reasonable attorney in circumstances. Cannot sanction for legal arguments (even if lose). Must serve motion but not file for 21 days (safe harbor)."
        ),

        LegalRule(
            subject="Civil Procedure",
            topic="Joinder",
            subtopic="Joinder of Claims and Parties",
            title="Permissive and Compulsory Joinder",
            rule="Permissive party joinder (Rule 20): (1) claims arise from same transaction/occurrence; AND (2) common question of law/fact. Compulsory party joinder (Rule 19): person is necessary if (1) complete relief cannot be accorded without them; OR (2) disposition may impair their interest or create inconsistent obligations. If necessary, must join if feasible. If not feasible, determine if indispensable (dismiss if yes). Claim joinder (Rule 18): party may join as many claims as have.",
            elements=[
                "Rule 20: permissive party joinder (same T/O + common question)",
                "Rule 19(a): necessary party (complete relief OR impair interest)",
                "Rule 19(b): indispensable party (equity factors)",
                "Rule 18: unlimited claim joinder by plaintiff (no relationship required)",
                "Rule 13: counterclaims (compulsory if same T/O; permissive otherwise)",
                "Supplemental jurisdiction: likely needed for claims lacking independent basis"
            ],
            citations=[
                "FRCP Rule 18, 19, 20",
                "Temple v. Synthes Corp., 498 U.S. 5 (1990)"
            ],
            notes="Necessary but not indispensable: proceed without party. Indispensable: must dismiss. Factors: prejudice, adequacy, judgment, alternative forum. SMJ required for each claim."
        ),

        LegalRule(
            subject="Civil Procedure",
            topic="Pleadings",
            subtopic="Counterclaims and Cross-claims",
            title="Counterclaims, Cross-claims, and Third-Party Practice",
            rule="Counterclaim (Rule 13): claim against opposing party. Compulsory: arises from same transaction/occurrence (waived if not asserted). Permissive: any other claim (not waived). Cross-claim (Rule 13(g)): claim against co-party (same side); permissive only; must arise from same T/O or involve same property. Third-party claim (Rule 14): defendant may implead third-party defendant who is/may be liable for defendant's liability (derivative liability only).",
            elements=[
                "Compulsory counterclaim: same T/O as opposing party's claim (waived if not asserted)",
                "Permissive counterclaim: any claim against opposing party (not waived)",
                "Cross-claim: against co-party, must arise from same T/O, always permissive",
                "Third-party practice (impleader): derivative liability (may be liable to defendant)",
                "Supplemental jurisdiction: typically available for compulsory, cross-claims, impleader",
                "Independent SMJ basis: required for permissive counterclaims (unless diversity)"
            ],
            citations=[
                "FRCP Rule 13, 14",
                "United States v. Heyward-Robinson Co., 430 F.2d 1077 (2d Cir. 1970)"
            ],
            notes="Compulsory: logical relationship test. Waived if not asserted. Permissive: not waived. Impleader limited to derivative liability (TPD liable if defendant liable)."
        ),

        LegalRule(
            subject="Civil Procedure",
            topic="Former Adjudication",
            subtopic="Res Judicata",
            title="Res Judicata - Claim Preclusion",
            rule="Claim preclusion (res judicata): bars re-litigation of claims. Requirements: (1) same claimant against same defendant; (2) valid final judgment on merits; (3) same claim/cause of action. Defines claim broadly: transactional test (all claims arising from same T/O). Bars not only what was litigated but what could have been litigated. Exceptions: lack of jurisdiction, fraud, change in law/facts, agreement.",
            elements=[
                "Valid final judgment on merits",
                "Same claimant vs. same defendant",
                "Same claim/cause of action (transactional approach)",
                "Bars claims litigated AND claims that could have been litigated",
                "Transactional test: all rights arising from same T/O",
                "Judgment must be final (all appeals exhausted or time expired)"
            ],
            citations=[
                "Restatement (Second) of Judgments § 24",
                "Taylor v. Sturgell, 553 U.S. 880 (2008)"
            ],
            notes="Broad claim definition: modern transactional approach. Bars splitting claims. Dismissals: with prejudice (on merits); without prejudice (not on merits). Non-mutual preclusion limited."
        )
    ]

    for rule in rules:
        db.add_rule(rule)
    print(f"✓ Added 5 Civil Procedure rules (7 → 12)")


def main():
    """Execute second round expansion"""
    print("=" * 80)
    print("BLACK LETTER LAW DATABASE - SECOND ROUND EXPANSION")
    print("=" * 80)
    print("\nExpanding from 79 rules to 114 rules (35 new rules)")
    print("Adding 5 rules to each of 7 subjects\n")

    # Load database
    db = BlackLetterLawDatabase('data/black_letter_law.json')

    # Show current state
    current = db.get_stats()
    print(f"Current: {current['total_rules']} rules across {current['subjects']} subjects\n")

    # Add rules
    print("Adding new rules:")
    print("-" * 80)
    add_constitutional_law_rules(db)
    add_evidence_rules(db)
    add_criminal_law_rules(db)
    add_property_rules(db)
    add_torts_rules(db)
    add_contracts_rules(db)
    add_civil_procedure_rules(db)

    # Save database
    db.save_to_file('data/black_letter_law.json')
    print("\n" + "=" * 80)
    print("✅ DATABASE SAVED")
    print("=" * 80)

    # Show final state
    final = db.get_stats()
    print(f"\nFinal: {final['total_rules']} rules across {final['subjects']} subjects")
    print(f"Growth: +{final['total_rules'] - current['total_rules']} rules ({((final['total_rules'] - current['total_rules']) / current['total_rules'] * 100):.0f}% increase)")

    # Count by subject
    subject_counts = {}
    for rule in db.rules:
        subject_counts[rule.subject] = subject_counts.get(rule.subject, 0) + 1

    print("\n" + "=" * 80)
    print("FINAL BREAKDOWN BY SUBJECT")
    print("=" * 80)
    for subject in sorted(subject_counts.keys()):
        print(f"  {subject:25s}: {subject_counts[subject]:2d} rules")

    print("\n" + "=" * 80)
    print("✅ SECOND ROUND EXPANSION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()

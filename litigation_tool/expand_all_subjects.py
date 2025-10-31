#!/usr/bin/env python3
"""
Comprehensive Database Expansion - Add 5 Rules to All 7 Subjects
Expands database from 44 to 79 rules (35 new rules)
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from black_letter_law import BlackLetterLawDatabase, LegalRule

def add_constitutional_law_rules(db: BlackLetterLawDatabase):
    """Add 5 more Constitutional Law rules"""

    # 5th Amendment - Self-Incrimination
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="5th Amendment",
        subtopic="Self-Incrimination",
        title="Miranda Rights and Self-Incrimination",
        rule="5th Amendment privilege against self-incrimination protects against compelled testimonial communications. Miranda v. Arizona requires police to warn suspects in custody before interrogation: (1) right to remain silent; (2) statements can be used against them; (3) right to attorney; (4) attorney appointed if indigent. Failure to give Miranda warnings makes statements inadmissible (but can be used for impeachment if voluntary).",
        elements=["Custody", "Interrogation", "Miranda warnings required", "Right to remain silent", "Right to attorney", "Voluntary waiver required"],
        citations=["Miranda v. Arizona, 384 U.S. 436 (1966)", "Dickerson v. United States, 530 U.S. 428 (2000)", "5th Amendment"],
        notes="Custody = reasonable person would not feel free to leave. Interrogation = words/actions likely to elicit incriminating response. Public safety exception (New York v. Quarles). Can invoke right to silence or counsel; invocation must be unambiguous (Berghuis v. Thompkins). Violation = exclusion of statements."
    ))

    # 5th Amendment - Takings Clause
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="5th Amendment",
        subtopic="Takings Clause",
        title="Regulatory Takings and Just Compensation",
        rule="5th Amendment Takings Clause requires just compensation when government takes private property for public use. Per se takings: (1) physical occupation (Loretto); (2) total economic deprivation (Lucas). Penn Central balancing test for regulatory takings: (a) economic impact; (b) interference with investment-backed expectations; (c) character of government action. Temporary takings also compensable.",
        elements=["Per se taking: physical occupation", "Per se taking: total economic deprivation", "Penn Central balancing for regulatory takings", "Just compensation required", "Public use (rational basis review)"],
        citations=["Penn Central Transp. Co. v. New York City, 438 U.S. 104 (1978)", "Lucas v. South Carolina Coastal Council, 505 U.S. 1003 (1992)", "Loretto v. Teleprompter Manhattan CATV Corp., 458 U.S. 419 (1982)", "Kelo v. City of New London, 545 U.S. 469 (2005)"],
        notes="Physical occupation = per se taking even if minimal (Loretto - cable box). Total deprivation = Lucas (all economically viable use destroyed). Penn Central: most regulatory takings analyzed under balancing test. Public use = very deferential (Kelo - economic development sufficient). Just compensation = fair market value."
    ))

    # 6th Amendment - Right to Counsel
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="6th Amendment",
        subtopic="Right to Counsel",
        title="Right to Counsel at Critical Stages",
        rule="6th Amendment guarantees right to counsel at all critical stages of criminal prosecution after adversarial proceedings begin (formal charge, arraignment, indictment). Critical stages include: arraignment, plea negotiations, trial, sentencing, first appeal as of right. States must provide appointed counsel to indigent defendants in felony cases (Gideon) and misdemeanors with actual imprisonment (Argersinger).",
        elements=["Attaches at initiation of adversarial proceedings", "All critical stages", "Appointed counsel for indigent if imprisonment possible", "Effective assistance required (Strickland)", "Waiver must be knowing and voluntary"],
        citations=["Gideon v. Wainwright, 372 U.S. 335 (1963)", "Massiah v. United States, 377 U.S. 201 (1964)", "Strickland v. Washington, 466 U.S. 668 (1984)", "6th Amendment"],
        notes="Massiah: 6th Amendment violated when government deliberately elicits statements from charged defendant without counsel. Strickland ineffective assistance test: (1) deficient performance; (2) prejudice (reasonable probability of different result). Photo lineup pre-charge not critical stage. Post-charge lineup is critical stage."
    ))

    # 6th Amendment - Confrontation Clause
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="6th Amendment",
        subtopic="Confrontation Clause",
        title="Confrontation Clause - Crawford Test",
        rule="6th Amendment Confrontation Clause bars admission of testimonial hearsay unless: (1) declarant is unavailable; AND (2) defendant had prior opportunity to cross-examine. Crawford v. Washington: testimonial statements require confrontation; non-testimonial statements analyzed under hearsay rules. Testimonial = formal statements to government for prosecution (police interrogations, affidavits, depositions, prior testimony). Confrontation satisfied if witness testifies at trial subject to cross.",
        elements=["Testimonial hearsay requires confrontation", "Declarant unavailable", "Prior opportunity to cross-examine", "Or witness testifies at trial", "Non-testimonial = hearsay rules apply"],
        citations=["Crawford v. Washington, 541 U.S. 36 (2004)", "Davis v. Washington, 547 U.S. 813 (2006)", "6th Amendment"],
        notes="Crawford replaced Ohio v. Roberts reliability test. Davis: 911 calls seeking help = non-testimonial; statements to police for prosecution = testimonial. Lab reports testimonial (Melendez-Diaz). Business records generally non-testimonial. Dying declarations exception even if testimonial (dictum in Crawford)."
    ))

    # Religion Clauses
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="1st Amendment",
        subtopic="Religion Clauses",
        title="Establishment Clause and Free Exercise",
        rule="Establishment Clause prohibits government from establishing religion or excessively entangling with religion. Lemon test (declining use): (1) secular purpose; (2) primary effect neither advances nor inhibits religion; (3) no excessive entanglement. Modern approach: history and tradition (Kennedy v. Bremerton). Free Exercise: generally applicable neutral laws valid even if burden religion (Smith); religious exemptions discretionary. Strict scrutiny if law targets religion or not generally applicable.",
        elements=["Establishment: no government endorsement of religion", "Lemon test (declining)", "History and tradition test (Kennedy)", "Free Exercise: neutral laws of general applicability valid (Smith)", "Strict scrutiny if targets religion"],
        citations=["Lemon v. Kurtzman, 403 U.S. 602 (1971)", "Employment Division v. Smith, 494 U.S. 872 (1990)", "Kennedy v. Bremerton School Dist., 142 S. Ct. 2407 (2022)", "1st Amendment"],
        notes="Kennedy overruled Lemon's endorsement test, emphasized history/tradition. Smith: no religious exemption from neutral laws (peyote). But strict scrutiny if law targets religion (Church of Lukumi Babalu Aye - animal sacrifice ban). RFRA provides statutory protection for federal laws. State RFRAs vary."
    ))

def add_evidence_rules(db: BlackLetterLawDatabase):
    """Add 5 more Evidence rules"""

    # Impeachment - Prior Inconsistent Statements
    db.add_rule(LegalRule(
        subject="Evidence",
        topic="Impeachment",
        subtopic="Prior Inconsistent Statements",
        title="Impeachment by Prior Inconsistent Statement",
        rule="A witness may be impeached by prior inconsistent statement. Under FRE 613, extrinsic evidence of prior inconsistent statement admissible only if: (1) witness given opportunity to explain or deny; AND (2) adverse party given opportunity to examine about it. Prior inconsistent statement made under oath at proceeding is non-hearsay (FRE 801(d)(1)(A)) and admissible for truth. Collateral matter rule: no extrinsic evidence on collateral matters.",
        elements=["Witness may be impeached by prior inconsistent statement", "Foundation required for extrinsic evidence", "Witness must have opportunity to explain", "Under oath at proceeding = non-hearsay (substantive)", "Not under oath = impeachment only"],
        citations=["FRE 613", "FRE 801(d)(1)(A)"],
        notes="FRE 613 eliminates common law requirement to confront witness before extrinsic evidence. Prior inconsistent statement under oath (deposition, trial, hearing) admissible as substantive evidence, not just impeachment. Collateral matter: if only relevant to impeach credibility, no extrinsic evidence allowed."
    ))

    # Habit Evidence
    db.add_rule(LegalRule(
        subject="Evidence",
        topic="Character Evidence",
        subtopic="Habit",
        title="Habit Evidence - FRE 406",
        rule="Evidence of habit or routine practice is admissible to prove conduct on particular occasion. Habit = regular response to repeated specific situation (more specific than character). No corroboration or eyewitness required. Routine practice of organization also admissible. Distinguished from character evidence (inadmissible for propensity under FRE 404).",
        elements=["Habit admissible to prove conforming conduct", "Must be regular response to repeated situation", "More specific than character", "No corroboration required", "Organizational routine practice admissible"],
        citations=["FRE 406"],
        notes="Habit vs. character: habit is specific (always stops at stop sign), character is general (careful person). Frequency + specificity = habit. Examples: always mailing letters same day, always checking brakes before driving. Business routine: regular practice of organization (e.g., always sending invoices on 1st of month)."
    ))

    # Subsequent Remedial Measures
    db.add_rule(LegalRule(
        subject="Evidence",
        topic="Relevance",
        subtopic="Policy Exclusions",
        title="Subsequent Remedial Measures - FRE 407",
        rule="Evidence of subsequent remedial measures (repairs, design changes, safety measures after accident) inadmissible to prove negligence, culpable conduct, design defect, or need for warning. Admissible for other purposes: impeachment, ownership/control (if disputed), feasibility (if disputed). Policy: encourage safety improvements without fear of liability.",
        elements=["Repairs/safety measures after accident", "Inadmissible for negligence, defect, need for warning", "Admissible: impeachment, ownership (if disputed), feasibility (if disputed)", "Must be after incident"],
        citations=["FRE 407"],
        notes="Applies only to measures taken after incident. 2011 amendment: applies to product liability (design defect, failure to warn). Feasibility: only if defendant contests feasibility. Impeachment: if witness claims product was safest possible. Third-party repairs not excluded (only defendant's repairs)."
    ))

    # Compromise and Settlement Offers
    db.add_rule(LegalRule(
        subject="Evidence",
        topic="Relevance",
        subtopic="Policy Exclusions",
        title="Compromise Offers and Statements - FRE 408",
        rule="Offers to compromise disputed claims and statements made during settlement negotiations inadmissible to prove or disprove validity or amount of claim. Admissible for other purposes: proving bias, negating contention of undue delay, proving effort to obstruct investigation. Claim must be disputed as to validity or amount. Statements to government agencies in civil enforcement not protected.",
        elements=["Compromise offers inadmissible", "Statements during settlement negotiations inadmissible", "Claim must be disputed", "Admissible: bias, undue delay, obstruction", "Government civil enforcement statements not protected"],
        citations=["FRE 408"],
        notes="'Disputed claim' = actual dispute or difference of opinion about validity/amount. Pre-dispute statements not protected (must be offer to compromise pending/imminent claim). 2006 amendment: statements to government agencies in civil regulatory/enforcement matters not protected by 408 but may be protected by 410 (plea discussions)."
    ))

    # Authentication
    db.add_rule(LegalRule(
        subject="Evidence",
        topic="Authentication",
        subtopic="General Requirement",
        title="Authentication Requirement - FRE 901",
        rule="To be admissible, evidence must be authenticated by showing it is what proponent claims. Proponent must produce evidence sufficient to support finding of authenticity. Methods include: (1) testimony of witness with knowledge; (2) lay opinion on handwriting; (3) expert comparison; (4) distinctive characteristics; (5) voice identification; (6) phone conversations; (7) ancient documents (20+ years); (8) reply doctrine; (9) self-authenticating documents (FRE 902). Standard: jury could reasonably find item authentic.",
        elements=["Must authenticate before admitting", "Prima facie showing of authenticity", "Many methods available", "Self-authenticating documents need no extrinsic evidence", "Standard: sufficient to support jury finding"],
        citations=["FRE 901", "FRE 902"],
        notes="Low bar - just enough to support jury finding. Self-authenticating (FRE 902): public documents with seals, certified copies, newspapers, trade inscriptions, acknowledged documents, commercial paper, business records with affidavit. Email/texts: testimony about sender + reply doctrine + distinctive characteristics. Ancient documents: 20+ years old, proper custody, unblemished."
    ))

def add_criminal_law_rules(db: BlackLetterLawDatabase):
    """Add 5 more Criminal Law rules"""

    # Felony Murder
    db.add_rule(LegalRule(
        subject="Criminal Law",
        topic="Homicide",
        subtopic="Felony Murder",
        title="Felony Murder Rule",
        rule="Killing during commission of inherently dangerous felony constitutes murder even without intent to kill. Common law: BARRK felonies (Burglary, Arson, Rape, Robbery, Kidnapping). Requirements: (1) underlying felony; (2) death caused during commission or immediate flight; (3) death foreseeable result of felony. Limitations: merger doctrine (felony must be independent of killing), agency theory (felon or accomplice must cause death), res gestae (must be during felony, not after safe escape).",
        elements=["Inherently dangerous felony (BARRK)", "Death during commission or immediate flight", "Causation (foreseeability)", "No merger (felony independent of killing)", "Agency theory (some states)"],
        citations=["Common Law", "MPC § 210.2"],
        notes="Inherently dangerous: BARRK traditionally; modern expanded to any dangerous felony. Merger: assault/battery cannot be underlying felony (would merge with killing). Agency theory: defendant/accomplice must cause death (not victim/police/third party). Res gestae: immediate flight included; safe escape ends. Redline limitation: felon not liable if co-felon killed by victim/police."
    ))

    # Burglary
    db.add_rule(LegalRule(
        subject="Criminal Law",
        topic="Property Crimes",
        subtopic="Burglary",
        title="Burglary Elements",
        rule="Common law burglary: (1) breaking and entering; (2) of dwelling; (3) of another; (4) at nighttime; (5) with intent to commit felony inside. Modern statutes eliminate 'breaking,' 'nighttime,' expand 'dwelling' to any building/structure. Intent to commit felony (or theft) must exist at time of entry. Remaining inside after permission expires can be 'entry.'",
        elements=["Breaking and entering (common law)", "Of dwelling/building", "Of another", "Intent to commit felony inside", "Intent at time of entry"],
        citations=["Common Law", "MPC § 221.1"],
        notes="Breaking: creating/enlarging opening (pushing open door, breaking window). Entry: any part of body or instrument. Dwelling: common law limited to residence; modern includes any building. Intent: must have intent to commit felony at time of entry (if forms intent after entry, not burglary). Constructive entry: use of tool/instrument. Modern: often includes cars, vending machines."
    ))

    # Robbery
    db.add_rule(LegalRule(
        subject="Criminal Law",
        topic="Property Crimes",
        subtopic="Robbery",
        title="Robbery - Larceny by Force or Fear",
        rule="Robbery is larceny plus force or intimidation. Elements: (1) taking and carrying away; (2) of personal property of another; (3) from person or presence; (4) by force or intimidation; (5) with intent to permanently deprive. Force/intimidation must be used to obtain property or retain possession immediately after taking. Threat of immediate harm required (not future harm).",
        elements=["Taking and carrying away (larceny)", "Personal property of another", "From person or presence", "By force or intimidation", "Intent to permanently deprive"],
        citations=["Common Law", "MPC § 222.1"],
        notes="From person or presence: property on person or area within victim's control. Force: enough to overcome resistance (snatching sufficient if victim resists). Intimidation: threat of immediate physical harm to victim, family, or property. Timing: force must be during or immediately after taking (force to escape = robbery). Armed robbery: enhanced penalty."
    ))

    # Larceny
    db.add_rule(LegalRule(
        subject="Criminal Law",
        topic="Property Crimes",
        subtopic="Larceny/Theft",
        title="Larceny Elements",
        rule="Larceny is (1) trespassory taking (caption); (2) and carrying away (asportation); (3) of personal property; (4) of another; (5) with intent to permanently deprive. Taking must be without consent (trespassory). Asportation: any movement, however slight. Intent must exist at time of taking. Larceny by trick: obtaining possession by fraud/deception.",
        elements=["Trespassory taking", "Carrying away (asportation)", "Personal property", "Of another", "Intent to permanently deprive at time of taking"],
        citations=["Common Law", "MPC § 223.2"],
        notes="Trespassory: without consent or exceeding scope of consent. Asportation: slight movement sufficient. Personal property: tangible property, not real estate. Of another: someone else has superior possessory right. Intent: must intend permanent deprivation (borrowing not larceny unless unreasonable time/substantial risk). Continuing trespass: if took without intent but later forms intent while still possessing = larceny."
    ))

    # Accomplice Liability
    db.add_rule(LegalRule(
        subject="Criminal Law",
        topic="Parties to Crime",
        subtopic="Accomplice Liability",
        title="Accomplice Liability - Aiding and Abetting",
        rule="Person liable as accomplice if: (1) aids, abets, encourages, or assists; AND (2) with intent that crime be committed. Accomplice liable for crime committed and all foreseeable crimes in furtherance of criminal objective. Mere presence insufficient; must affirmative act. Withdrawal possible before crime if: (a) repudiate encouragement; (b) neutralize assistance; OR (c) notify police.",
        elements=["Aids, abets, encourages, assists (actus reus)", "Intent that crime be committed (mens rea)", "Liable for target crime and foreseeable crimes", "Withdrawal: repudiate, neutralize, or notify police"],
        citations=["Common Law", "MPC § 2.06"],
        notes="Actus reus: encouragement, assistance, or presence plus intent to assist. Mens rea: intent that principal commit crime (purpose standard under MPC). Natural and probable consequences doctrine: liable for foreseeable crimes (some states abolished). Withdrawal: must occur before crime committed and must neutralize assistance. Accessory after fact: separate crime (not accomplice)."
    ))

def add_property_rules(db: BlackLetterLawDatabase):
    """Add 5 more Property rules"""

    # Recording Acts
    db.add_rule(LegalRule(
        subject="Property",
        topic="Conveyancing",
        subtopic="Recording Acts",
        title="Notice, Race, and Race-Notice Recording Acts",
        rule="Recording acts protect subsequent purchasers from prior unrecorded interests. Three types: (1) Notice: subsequent bona fide purchaser (BFP) for value without notice wins over prior unrecorded interest; (2) Race: first to record wins (notice irrelevant); (3) Race-Notice: BFP without notice who records first wins. BFP requires: payment of valuable consideration + no actual, inquiry, or constructive notice. Shelter rule: BFP's transferee protected even with notice.",
        elements=["Notice jurisdiction: BFP without notice wins", "Race jurisdiction: first to record wins", "Race-Notice: BFP without notice who records first", "BFP: value + no notice (actual, inquiry, constructive)", "Shelter rule protects BFP's transferees"],
        citations=["Common Law"],
        notes="Notice states (minority): last BFP wins even if doesn't record. Race states (rare): first to record wins regardless of knowledge. Race-notice (majority): BFP must record first. Notice types: actual (knew), inquiry (suspicious circumstances), constructive (recorded documents in chain of title). Shelter: BFP's donee protected. Quitclaim grantee can be BFP if pays value and lacks notice."
    ))

    # Marketable Title
    db.add_rule(LegalRule(
        subject="Property",
        topic="Conveyancing",
        subtopic="Title Quality",
        title="Marketable Title Doctrine",
        rule="Seller has implied duty to deliver marketable title at closing unless contract says otherwise. Marketable title = title reasonably free from doubt, title buyer can resell or mortgage without risk. Defects: (1) adverse possession not quieted; (2) encumbrances (mortgages, easements, covenants not excepted in contract); (3) significant variation in description; (4) existing violation of zoning. Buyer must notify seller and give reasonable time to cure before closing.",
        elements=["Implied duty to deliver marketable title", "Free from reasonable doubt", "Defects: adverse possession, encumbrances, description errors, zoning violations", "Time to cure before closing", "Merger: contract merges into deed (unless fraud/mistake)"],
        citations=["Common Law"],
        notes="Marketable ≠ perfect (minor defects OK if won't affect value/use). Encumbrances: easements, mortgages, covenants make title unmarketable unless accepted in contract. Quitclaim deed doesn't guarantee marketable title. Merger doctrine: after closing, contract obligations merge into deed; can't sue on contract (only deed warranties). Time to cure: reasonable time before closing. Specific performance denied if title unmarketable and not curable."
    ))

    # Equitable Servitudes
    db.add_rule(LegalRule(
        subject="Property",
        topic="Servitudes",
        subtopic="Equitable Servitudes",
        title="Equitable Servitudes - Creation and Enforcement",
        rule="Equitable servitude is covenant enforceable in equity (injunction). Requirements: (1) writing satisfying Statute of Frauds (or implied from common scheme); (2) intent to bind successors; (3) touches and concerns land; (4) notice to subsequent purchasers (actual, inquiry, or constructive). Negative covenants (restrictions) more readily enforced than affirmative. Common scheme implied if: (a) subdivision recorded plan; OR (b) uniform restrictions shown by deeds/conduct.",
        elements=["Writing or implied from common scheme", "Intent to bind successors", "Touch and concern land", "Notice to subsequent purchasers", "Enforceable by injunction"],
        citations=["Restatement (Third) of Property (Servitudes)"],
        notes="Equity enforces even if real covenant requirements not met. Common scheme: developer's general plan for subdivision binds all lots even if restriction not in deed, if notice (inquiry from uniform development). Notice: actual (knew), inquiry (uniform restrictions), constructive (recorded). Touch and concern: affects use/value of land. Defenses: laches, acquiescence, unclean hands, changed conditions. Remedy: injunction (not damages)."
    ))

    # Real Covenants
    db.add_rule(LegalRule(
        subject="Property",
        topic="Servitudes",
        subtopic="Real Covenants",
        title="Real Covenants Running with Land",
        rule="Real covenant runs with land if: (1) writing; (2) intent to run with land; (3) touches and concerns land; (4) horizontal privity (original parties); (5) vertical privity (successors). Horizontal privity: mutual/successive interests in land (grantor-grantee, landlord-tenant). Vertical privity: successor holds entire estate. Burden and benefit analyzed separately. Remedy: damages at law.",
        elements=["Writing (Statute of Frauds)", "Intent to run", "Touch and concern", "Horizontal privity (original parties)", "Vertical privity (successors)"],
        citations=["Common Law", "Restatement (Third) of Property (Servitudes)"],
        notes="Burden runs: all 5 requirements. Benefit runs: writing, intent, touch and concern (no privity required). Horizontal privity: grantor-grantee, landlord-tenant, mortgagor-mortgagee (NOT neighbors). Vertical privity for burden: successor must take entire estate (not adverse possessor). Equitable servitude easier to enforce (no privity). Touch and concern: affects use/value as landowner (not personal)."
    ))

    # Fixtures
    db.add_rule(LegalRule(
        subject="Property",
        topic="Personal vs. Real Property",
        subtopic="Fixtures",
        title="Fixtures - Personal Property Becoming Real Property",
        rule="Fixture is personal property that becomes part of real property. Tests: (1) annexation (physically attached); (2) adaptation (custom-made for property); (3) intent (objective intent to make permanent). Factors: degree of attachment, injury to property if removed, relationship of parties. Trade fixtures: tenant's business equipment removable at end of lease if: (a) installed for trade/business; (b) removed without substantial damage.",
        elements=["Annexation test (physical attachment)", "Adaptation test (custom-made)", "Intent test (permanent)", "Default: conveys with land unless reserved", "Trade fixtures: tenant may remove"],
        citations=["Common Law"],
        notes="Intent most important, determined objectively from circumstances. Examples of fixtures: built-in appliances, heating systems, custom storm windows. NOT fixtures: area rugs, curtains, movable appliances. Trade fixtures: tenant's business equipment (shelves, counters, specialized equipment) removable even if attached. Must remove by end of lease or becomes landlord's. Seller may reserve in contract."
    ))

def add_torts_rules(db: BlackLetterLawDatabase):
    """Add 5 more Torts rules"""

    # Battery
    db.add_rule(LegalRule(
        subject="Torts",
        topic="Intentional Torts",
        subtopic="Battery",
        title="Battery Elements",
        rule="Battery requires: (1) act by defendant; (2) intent to cause contact or apprehension of contact; (3) harmful or offensive contact; (4) to plaintiff or something closely connected to plaintiff; (5) causation. Intent: purpose or substantial certainty (transferred intent applies). Offensive = would offend reasonable person's sense of dignity. No harm/damages required; nominal damages available.",
        elements=["Volitional act", "Intent (purpose or substantial certainty)", "Harmful or offensive contact", "To plaintiff's person", "Causation"],
        citations=["Restatement (Second) of Torts § 13"],
        notes="Intent: need not intend harm, only contact. Substantial certainty sufficient (kick chair knowing person sitting). Transferred intent: intent to battery A, actually battery B = liable. Offensive: unwanted touching offensive to reasonable dignity (no actual harm needed). Contact with clothing, object closely associated, or something held = battery. Single intent vs. dual intent: jurisdictions split."
    ))

    # Assault
    db.add_rule(LegalRule(
        subject="Torts",
        topic="Intentional Torts",
        subtopic="Assault",
        title="Assault Elements",
        rule="Assault requires: (1) act by defendant; (2) intent to cause apprehension of imminent harmful or offensive contact; (3) reasonable apprehension in plaintiff; (4) of imminent contact. No actual contact required (if contact, battery). Apparent ability sufficient; actual ability not required. Words alone generally insufficient; require overt act. Apprehension ≠ fear (just awareness of contact).",
        elements=["Volitional act", "Intent to cause apprehension", "Reasonable apprehension", "Of imminent harmful or offensive contact", "No contact required"],
        citations=["Restatement (Second) of Torts § 21"],
        notes="Apprehension = awareness/expectation of contact (not fear). Imminent: immediate, without significant delay. Future threats not assault ('I'll get you next week'). Apparent ability sufficient (unloaded gun if plaintiff doesn't know). Words can negate assault ('I'd hit you but I won't'). Transferred intent applies. Common with battery but can exist alone."
    ))

    # False Imprisonment
    db.add_rule(LegalRule(
        subject="Torts",
        topic="Intentional Torts",
        subtopic="False Imprisonment",
        title="False Imprisonment Elements",
        rule="False imprisonment requires: (1) act by defendant; (2) intent to confine; (3) actual confinement; (4) plaintiff's awareness of confinement or harm. Confinement: bounded area with no reasonable means of escape. Physical barriers, force, threats of force, invalid assertion of legal authority. Moral pressure or future threats insufficient. Shopkeeper's privilege: reasonable detention on reasonable suspicion of shoplifting.",
        elements=["Volitional act", "Intent to confine", "Actual confinement in bounded area", "No reasonable means of escape", "Awareness or harm"],
        citations=["Restatement (Second) of Torts § 35"],
        notes="Confinement: must be bounded in all directions (blocked street not confined if can go back). Means of escape: unreasonable if unknown, dangerous, humiliating, or involves harm to property. Duration: any time sufficient (brief OK). Awareness: must know confined at time OR suffer actual harm. Shopkeeper's privilege: reasonable manner, time, suspicion. Invalid arrest = false imprisonment."
    ))

    # IIED (Intentional Infliction of Emotional Distress)
    db.add_rule(LegalRule(
        subject="Torts",
        topic="Intentional Torts",
        subtopic="IIED",
        title="Intentional Infliction of Emotional Distress",
        rule="IIED (outrage) requires: (1) extreme and outrageous conduct; (2) intent to cause severe emotional distress OR recklessness; (3) causation; (4) severe emotional distress. Extreme and outrageous: exceeds all bounds of decency, atrocious, utterly intolerable in civilized society. Mere insults, indignities, annoyances insufficient. Common carriers and innkeepers held to higher standard. Third party recovery: present family member may recover if defendant knew present.",
        elements=["Extreme and outrageous conduct", "Intent or recklessness", "Causation", "Severe emotional distress", "More than mere insults/indignities"],
        citations=["Restatement (Second) of Torts § 46"],
        notes="High bar: must be truly outrageous. Factors: abuse of power/authority, knowledge of special sensitivity, continuous/repeated conduct. Examples: mishandling corpse, fake death notification, extreme debt collection. NOT IIED: simple insults, mean behavior, firing. Severe distress: medically significant (physical manifestations helpful). Recklessness sufficient. Third party: family member present can recover if defendant knew."
    ))

    # Strict Liability - Abnormally Dangerous Activities
    db.add_rule(LegalRule(
        subject="Torts",
        topic="Strict Liability",
        subtopic="Abnormally Dangerous Activities",
        title="Strict Liability for Abnormally Dangerous Activities",
        rule="Strict liability (no fault) for abnormally dangerous activities. Factors: (1) high degree of risk of harm; (2) likelihood harm will be great; (3) inability to eliminate risk with reasonable care; (4) activity not common; (5) inappropriate for location; (6) value to community outweighed by risk. Common examples: blasting, storing explosives, toxic chemicals. Defenses: assumption of risk, comparative negligence (jurisdictions split), unforeseeable intervening cause.",
        elements=["Abnormally dangerous activity (6 factor test)", "No need to prove negligence", "Causation", "Damages", "Defenses: assumption of risk, possibly comparative fault"],
        citations=["Restatement (Second) of Torts § 519-520"],
        notes="All 6 factors considered; not all required. Examples: dynamite blasting, storing explosive gases, crop dusting, oil well operations. NOT strict liability: construction, airplane flights (common). Liability only for harm from risk that makes activity abnormally dangerous (blast damages building = liable; blast frightens cow who kicks plaintiff = negligence only). Modern trend: some states allow comparative fault defense."
    ))

def add_contracts_rules(db: BlackLetterLawDatabase):
    """Add 5 more Contracts rules"""

    # Statute of Frauds
    db.add_rule(LegalRule(
        subject="Contracts",
        topic="Contract Formation",
        subtopic="Statute of Frauds",
        title="Statute of Frauds Requirements",
        rule="Certain contracts must be in writing: (1) Marriage (in consideration of marriage); (2) Year (not performable within one year from formation); (3) Land (sale or transfer of land/interests); (4) Executor (executor's promise to pay estate debt from own funds); (5) Goods $500+ (UCC); (6) Surety (guarantee another's debt). Writing must contain: essential terms and signature of party to be charged. Part performance exception for land (2 of 3: payment, possession, improvements).",
        elements=["MY LEGS: Marriage, Year, Land, Executor, Goods, Surety", "Writing required", "Essential terms and signature", "Part performance exception (land)", "Merchant's confirmatory memo (UCC)"],
        citations=["Restatement (Second) of Contracts § 110", "UCC § 2-201"],
        notes="One year: if possibly performable in year, no writing needed (lifetime employment OK - death within year possible). Land: includes leases >1 year, easements, mortgages. UCC goods: writing needed if $500+; exceptions: specially manufactured, admitted in testimony, accepted/paid goods. Merchant's confirmatory memo: binds both if not objected to in 10 days. Part performance takes out of statute."
    ))

    # Parol Evidence Rule
    db.add_rule(LegalRule(
        subject="Contracts",
        topic="Contract Interpretation",
        subtopic="Parol Evidence Rule",
        title="Parol Evidence Rule",
        rule="Parol evidence rule bars evidence of prior or contemporaneous agreements/negotiations that contradict or add to integrated written contract. Partial integration: bars contradictory evidence. Complete integration: bars contradictory AND supplementary evidence. Evidence always admissible to: (1) show formation defects (fraud, duress, mistake, incapacity); (2) interpret ambiguous terms; (3) show condition precedent to effectiveness; (4) show subsequent modification; (5) collateral agreements.",
        elements=["Bars prior/contemporaneous agreements contradicting integrated writing", "Partial integration: no contradiction", "Complete integration: no contradiction or supplement", "Exceptions: formation defects, ambiguity, conditions, modifications, collateral"],
        citations=["Restatement (Second) of Contracts § 213"],
        notes="Integration: parties intended writing as final expression. Four corners test vs. contextual approach for determining integration. Merger clause indicates complete integration. Parol evidence: testimony, oral agreements, written agreements before final contract. Doesn't bar subsequent agreements (can always modify). Collateral agreement: separate consideration, doesn't contradict, wouldn't ordinarily be in main contract."
    ))

    # Breach of Contract
    db.add_rule(LegalRule(
        subject="Contracts",
        topic="Performance and Breach",
        subtopic="Breach",
        title="Material Breach vs. Minor Breach",
        rule="Material breach: significant failure to perform allowing non-breaching party to: (1) withhold own performance; AND (2) sue for damages. Minor breach: non-breaching party must still perform but may recover damages. Factors for materiality: (a) degree of benefit received; (b) adequacy of compensation; (c) forfeiture to breaching party; (d) likelihood of cure; (e) good faith. Anticipatory repudiation: unequivocal refusal to perform before performance due.",
        elements=["Material breach: withhold performance + damages", "Minor breach: must perform but recover damages", "Factors: benefit, compensation, forfeiture, cure, good faith", "Anticipatory repudiation: immediate cause of action"],
        citations=["Restatement (Second) of Contracts § 241", "UCC § 2-612"],
        notes="Material = substantial performance not rendered. Perfect tender rule (UCC): buyer may reject if goods/tender fail in any respect (exceptions: installment contracts, cure, revocation of acceptance). Substantial performance: minor breach, breaching party can enforce (recover contract price minus damages). Divisible contract: each part separate. Anticipatory repudiation: may await performance or sue immediately; retraction possible until relied upon."
    ))

    # Expectation Damages
    db.add_rule(LegalRule(
        subject="Contracts",
        topic="Remedies",
        subtopic="Damages",
        title="Expectation Damages",
        rule="Expectation damages put non-breaching party in position as if contract performed. Formula: Loss in Value + Other Loss - Cost Avoided - Loss Avoided. Consequential damages: foreseeable losses (Hadley v. Baxendale). Incidental damages: costs of dealing with breach. Limitations: (1) certainty (damages not too speculative); (2) foreseeability (Hadley); (3) avoidable consequences (mitigation); (4) no emotional distress (exceptions: contract for emotion, physical injury).",
        elements=["Loss in value + other loss - cost avoided - loss avoided", "Consequential damages if foreseeable", "Incidental damages", "Certainty required", "Mitigation required"],
        citations=["Restatement (Second) of Contracts § 347", "Hadley v. Baxendale"],
        notes="Expectation = benefit of bargain. Consequential: Hadley test - foreseeable at time of contracting or communicated. Lost profits: allowed if established with reasonable certainty (new business harder). Incidental: costs of cover, arranging substitute. Duty to mitigate: reasonable efforts to avoid loss (but don't have to sacrifice dignity/reputation). UCC: buyer gets difference + consequential + incidental - expenses saved."
    ))

    # Promissory Estoppel
    db.add_rule(LegalRule(
        subject="Contracts",
        topic="Contract Formation",
        subtopic="Consideration Substitutes",
        title="Promissory Estoppel (Reliance)",
        rule="Promissory estoppel enforces promise without consideration if: (1) promise; (2) promisor should reasonably expect reliance; (3) actual reliance; (4) reliance was reasonable and detrimental; AND (5) injustice can only be avoided by enforcement. Remedy: expectation damages OR reliance damages as justice requires. Common in charitable subscriptions, family promises, employment offers.",
        elements=["Promise", "Foreseeable reliance", "Actual reliance", "Reasonable and detrimental reliance", "Injustice requires enforcement"],
        citations=["Restatement (Second) of Contracts § 90"],
        notes="Consideration substitute when no bargain but fairness requires enforcement. Reliance: must be induced by promise and reasonable under circumstances. Damages: courts may limit to reliance (out-of-pocket losses) rather than expectation (benefit of bargain). Charitable subscriptions: reliance presumed. Employment: pre-employment reliance if offer definite and relied on (moved for job). Flexibility: enforcement 'as justice requires.'"
    ))

def add_civil_procedure_rules(db: BlackLetterLawDatabase):
    """Add 5 more Civil Procedure rules"""

    # Personal Jurisdiction
    db.add_rule(LegalRule(
        subject="Civil Procedure",
        topic="Jurisdiction",
        subtopic="Personal Jurisdiction",
        title="Personal Jurisdiction - Minimum Contacts",
        rule="Court has personal jurisdiction over defendant if: (1) defendant has minimum contacts with forum state; (2) exercise of jurisdiction does not offend traditional notions of fair play and substantial justice; AND (3) authorized by state long-arm statute. Specific jurisdiction: contacts relate to claim (purposeful availment + foreseeability + reasonableness). General jurisdiction: continuous and systematic contacts (essentially at home - domicile for individuals, incorporation/principal place for corporations).",
        elements=["Minimum contacts with forum state", "Fair play and substantial justice", "Specific jurisdiction: claim arises from contacts", "General jurisdiction: at home (continuous and systematic)", "Long-arm statute authorization"],
        citations=["International Shoe Co. v. Washington, 326 U.S. 310 (1945)", "Daimler AG v. Bauman, 571 U.S. 117 (2014)", "Bristol-Myers Squibb v. Superior Court, 137 S. Ct. 1773 (2017)"],
        notes="Specific: purposeful availment (purposefully directed toward forum), foreseeability (reasonable anticipation of suit), reasonableness (fair play test). Stream of commerce insufficient without 'plus' (Asahi). General: post-Daimler, essentially at home test very narrow (corporations at home at incorporation + principal place of business). Physical presence = traditional basis. Consent, long-arm statute limits may apply."
    ))

    # Subject Matter Jurisdiction
    db.add_rule(LegalRule(
        subject="Civil Procedure",
        topic="Jurisdiction",
        subtopic="Subject Matter Jurisdiction",
        title="Federal Subject Matter Jurisdiction",
        rule="Federal courts have limited subject matter jurisdiction: (1) Federal question: arises under Constitution, federal law, or treaties (28 USC 1331); (2) Diversity: citizens of different states + amount in controversy exceeds $75,000 (28 USC 1332); (3) Supplemental jurisdiction: related claims (same case or controversy); (4) Removal: defendant may remove diversity or federal question cases. Complete diversity required: no plaintiff from same state as any defendant. Amount determined from plaintiff's good faith claim.",
        elements=["Federal question (arises under federal law)", "Diversity (complete diversity + $75,000+)", "Supplemental jurisdiction (same case/controversy)", "Removal by defendant", "Subject matter jurisdiction cannot be waived"],
        citations=["28 U.S.C. § 1331", "28 U.S.C. § 1332", "28 U.S.C. § 1367"],
        notes="Federal question: claim must arise under federal law (well-pleaded complaint rule - complaint, not anticipated defense). Diversity: citizenship at filing (individual = domicile, corporation = incorporation + principal place). Amount: aggregation for single plaintiff vs. defendant; not across multiple plaintiffs. Supplemental: common nucleus of operative fact (same transaction/occurrence). Removal: within 30 days of service; diversity cases only removable if no defendant from forum state."
    ))

    # Summary Judgment
    db.add_rule(LegalRule(
        subject="Civil Procedure",
        topic="Pretrial Procedure",
        subtopic="Summary Judgment",
        title="Summary Judgment Standard - FRCP 56",
        rule="Court grants summary judgment if movant shows: (1) no genuine dispute as to any material fact; AND (2) movant entitled to judgment as a matter of law. Material fact: affects outcome under governing law. Genuine dispute: reasonable jury could return verdict for non-movant. Burden: movant bears burden of showing no genuine dispute; non-movant must show specific facts establishing genuine dispute (can't rely on pleadings). View evidence in light most favorable to non-movant.",
        elements=["No genuine dispute of material fact", "Entitled to judgment as a matter of law", "Material fact affects outcome", "Genuine = reasonable jury could differ", "All inferences to non-movant"],
        citations=["FRCP 56", "Celotex Corp. v. Catrett, 477 U.S. 317 (1986)", "Anderson v. Liberty Lobby, Inc., 477 U.S. 242 (1986)", "Matsushita Elec. Indus. Co. v. Zenith Radio Corp., 475 U.S. 574 (1986)"],
        notes="Movant's burden: show absence of genuine dispute (can point to lack of evidence on essential element). Non-movant must go beyond pleadings - affidavits, depositions, documents. Inferences: draw all reasonable inferences in favor of non-movant. Credibility: can't weigh credibility or evidence (jury function). Partial summary judgment: some issues/claims. Summary judgment differs from Iowa practice (Iowa uses summary judgment less frequently, more liberal notice pleading)."
    ))

    # Discovery Scope
    db.add_rule(LegalRule(
        subject="Civil Procedure",
        topic="Discovery",
        subtopic="Scope",
        title="Discovery Scope - FRCP 26",
        rule="Parties may discover any nonprivileged matter relevant to any party's claim or defense and proportional to needs of case. Proportionality factors: (a) importance; (b) amount in controversy; (c) parties' resources; (d) importance of discovery; (e) burden vs. benefit. Privileged materials not discoverable. Work product: trial preparation materials protected unless substantial need + undue hardship. Expert witnesses: testifying experts discoverable, non-testifying protected.",
        elements=["Relevant to claim or defense", "Proportional to needs of case", "Nonprivileged", "Work product protected (substantial need exception)", "Testifying experts discoverable"],
        citations=["FRCP 26", "Hickman v. Taylor, 329 U.S. 495 (1947)"],
        notes="2015 Amendment: proportionality limit, eliminated 'reasonably calculated to lead to admissible evidence.' Privileged: attorney-client, work product, spousal, doctor-patient (state law), 5th Amendment. Work product: trial prep materials (fact work product: substantial need + undue hardship; opinion work product: near absolute protection). Expert: testifying expert report + deposition; consulting expert generally protected. ESI: electronically stored information - proportionality critical. Iowa R. Civ. P. 1.503: similar scope."
    ))

    # Class Actions
    db.add_rule(LegalRule(
        subject="Civil Procedure",
        topic="Joinder",
        subtopic="Class Actions",
        title="Class Action Requirements - FRCP 23",
        rule="Class action allowed if: Prerequisites (FRCP 23(a)): (1) numerosity (too many for joinder); (2) commonality (common questions); (3) typicality (representative's claims typical); (4) adequacy (representative adequately protects class); AND FRCP 23(b) type: (b)(1) inconsistent adjudications, (b)(2) injunctive/declaratory relief, OR (b)(3) common questions predominate + class action superior (requires notice + opt-out). Court must certify class. Binding on all class members.",
        elements=["Numerosity, commonality, typicality, adequacy (23(a))", "23(b) type: (b)(1) inconsistent, (b)(2) injunctive, (b)(3) predominance + superiority", "Court certification required", "(b)(3): notice + opt-out", "Binding on class members"],
        citations=["FRCP 23", "Wal-Mart Stores, Inc. v. Dukes, 564 U.S. 338 (2011)"],
        notes="Numerosity: no magic number (40+ usually sufficient). Commonality: common question (not identical facts). Typicality: representative's claims arise from same event/practice. Adequacy: competent counsel, no conflicts. (b)(1): risk of inconsistent results. (b)(2): defendant acted same toward class (civil rights, employment discrimination). (b)(3): damages classes, requires predominance (common issues > individual) + superiority + notice + opt-out right. Settlement class actions require approval."
    ))

def main():
    """Comprehensive expansion of all subjects"""

    print("="*80)
    print("COMPREHENSIVE DATABASE EXPANSION - ALL 7 SUBJECTS")
    print("Adding 5 Rules to Each Subject (35 New Rules)")
    print("="*80)

    # Load existing database
    db_path = Path(__file__).parent / 'data' / 'black_letter_law.json'
    db = BlackLetterLawDatabase(str(db_path))

    # Count before
    before_total = len(db.rules)
    before_by_subject = {}
    for rule in db.rules:
        before_by_subject[rule.subject] = before_by_subject.get(rule.subject, 0) + 1

    print(f"\n📊 Current Database: {before_total} rules")
    print("\nRules by Subject (Before):")
    for subject in sorted(before_by_subject.keys()):
        print(f"  • {subject}: {before_by_subject[subject]} rules")

    # Add rules
    print("\n" + "="*80)
    print("ADDING RULES")
    print("="*80)

    print("\n📜 Adding 5 Constitutional Law rules...")
    add_constitutional_law_rules(db)

    print("📋 Adding 5 Evidence rules...")
    add_evidence_rules(db)

    print("🔴 Adding 5 Criminal Law rules...")
    add_criminal_law_rules(db)

    print("🏠 Adding 5 Property rules...")
    add_property_rules(db)

    print("⚖️  Adding 5 Torts rules...")
    add_torts_rules(db)

    print("📝 Adding 5 Contracts rules...")
    add_contracts_rules(db)

    print("🏛️  Adding 5 Civil Procedure rules...")
    add_civil_procedure_rules(db)

    # Save
    db.save_to_file(str(db_path))

    # Count after
    after_total = len(db.rules)
    after_by_subject = {}
    for rule in db.rules:
        after_by_subject[rule.subject] = after_by_subject.get(rule.subject, 0) + 1

    # Display results
    print("\n" + "="*80)
    print("EXPANSION COMPLETE")
    print("="*80)

    print(f"\n📊 Updated Database: {after_total} rules (was {before_total})")
    print(f"   Rules Added: {after_total - before_total}")

    print("\n📈 Growth by Subject:")
    for subject in sorted(after_by_subject.keys()):
        before = before_by_subject.get(subject, 0)
        after = after_by_subject[subject]
        growth = after - before
        print(f"  • {subject}: {before} → {after} (+{growth} rules)")

    # Show all topics
    print("\n" + "="*80)
    print("COMPLETE TOPIC COVERAGE")
    print("="*80)

    for subject in sorted(after_by_subject.keys()):
        rules_for_subject = [r for r in db.rules if r.subject == subject]
        topics = {}
        for rule in rules_for_subject:
            if rule.topic not in topics:
                topics[rule.topic] = []
            topics[rule.topic].append(rule)

        print(f"\n{subject} ({len(rules_for_subject)} rules):")
        for topic in sorted(topics.keys()):
            print(f"  • {topic} ({len(topics[topic])} rules)")

    print("\n" + "="*80)
    print(f"✅ Database saved to: {db_path}")
    print("="*80)
    print(f"\n🎉 SUCCESS! Database expanded from {before_total} to {after_total} rules")
    print("   Ready for comprehensive legal practice across all major subjects!\n")

if __name__ == '__main__':
    main()

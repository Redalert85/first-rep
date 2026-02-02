#!/usr/bin/env python3
"""
Add micro-hypos and policy rationales to knowledge base concepts.
Target: At least 20% of concepts (23+ of 112).
"""

import json
from pathlib import Path

# Micro-hypos and policy rationales for 25+ concepts
ENHANCEMENTS = {
    # CIVIL PROCEDURE (5 concepts)
    "civil_procedure_jurisdiction_and_venue": {
        "policy_rationales": [
            "Subject-matter jurisdiction ensures federal courts only hear cases within constitutional and statutory limits",
            "Venue rules promote convenience and fairness by locating trials near relevant events and witnesses",
            "Forum non conveniens allows courts to decline jurisdiction when another forum is clearly more appropriate"
        ],
        "micro_hypos": [
            "Plaintiff (citizen of NY) sues Defendant (citizen of NJ) for $100K breach of contract. RESULT: Diversity jurisdiction exists—complete diversity and amount exceeds $75K.",
            "Plaintiff sues under federal civil rights statute for $5K. RESULT: Federal question jurisdiction exists regardless of amount—federal law on face of complaint.",
            "Plaintiff and Defendant both from California. State law claim for $200K. RESULT: No diversity—same state citizens. Must use state court."
        ]
    },
    "civil_procedure_personal_jurisdiction": {
        "policy_rationales": [
            "Due process protects defendants from being sued in distant, inconvenient forums with no connection to them",
            "Minimum contacts doctrine balances plaintiff's interest in convenient forum with defendant's liberty interest",
            "Promotes fairness by requiring defendants to reasonably anticipate being haled into court based on their conduct"
        ],
        "micro_hypos": [
            "A website operator in Maine sells products to customers in all 50 states. A California customer sues in California. RESULT: Likely specific jurisdiction—purposeful availment through systematic sales to California market.",
            "A tourist from Ohio causes a car accident while vacationing in Florida. Victim sues in Ohio. RESULT: No jurisdiction—Ohio has no connection to the accident; Florida is proper forum.",
            "A company's only contact with Texas is one contract with a Texas company. Suit arises from that contract. RESULT: Specific jurisdiction exists—claim arises from the Texas contact.",
            "A corporation is incorporated in Delaware, headquartered in New York, with no offices in California. RESULT: General jurisdiction only in Delaware and New York (where 'at home'); not California."
        ]
    },
    "civil_procedure_subject_matter_jurisdiction": {
        "policy_rationales": [
            "Federal question jurisdiction ensures uniform interpretation of federal law across states",
            "Diversity jurisdiction protects out-of-state parties from potential local bias in state courts",
            "Amount-in-controversy requirement prevents trivial cases from burdening federal courts"
        ],
        "micro_hypos": [
            "Plaintiff from Texas sues defendant from Texas for $100K breach of contract. RESULT: No diversity—same state citizens; no federal question. State court only.",
            "Plaintiff from New York sues defendant from California for $50K tort. RESULT: No diversity—amount doesn't exceed $75K. State court only.",
            "Plaintiff sues under federal securities law for $10K. RESULT: Federal question jurisdiction exists regardless of amount—federal law on face of complaint."
        ]
    },
    "civil_procedure_summary_judgment": {
        "policy_rationales": [
            "Eliminates need for trial when no genuine factual disputes exist—saves judicial resources",
            "Protects parties from cost of unnecessary trials when outcome is legally certain",
            "Balances efficiency with right to jury trial by allowing trial when facts are genuinely disputed"
        ],
        "micro_hypos": [
            "Plaintiff claims breach of contract. Defendant produces unsigned contract. Plaintiff produces nothing showing signature. RESULT: Summary judgment for defendant—no evidence of contract formation.",
            "Both parties submit conflicting affidavits about whether light was red or green. RESULT: Summary judgment denied—genuine dispute of material fact for jury.",
            "Defendant admits all facts but argues law doesn't support liability. RESULT: Summary judgment appropriate—legal question for court, no factual dispute."
        ]
    },
    "civil_procedure_claim_preclusion": {
        "policy_rationales": [
            "Prevents harassment through repetitive litigation over same dispute",
            "Promotes finality—parties should have one opportunity to litigate claims",
            "Conserves judicial resources by avoiding relitigation of decided matters",
            "Encourages parties to bring all related claims in single action"
        ],
        "micro_hypos": [
            "P sues D for breach of contract and wins. P later sues D for fraud arising from same transaction. RESULT: Barred—fraud claim could have been raised in first suit.",
            "P1 sues D and loses. P2, not a party to first suit, sues D for same conduct. RESULT: Not barred—P2 wasn't party to first suit; no privity.",
            "P sues D in small claims court (limit $5K) for $5K. Actual damages were $50K. P later sues for remaining $45K. RESULT: Barred—P chose to split claim; could have sued in higher court."
        ]
    },
    "civil_procedure_issue_preclusion": {
        "policy_rationales": [
            "Prevents relitigation of identical issues already decided",
            "Promotes consistency in adjudication of same factual/legal issues",
            "Relies on incentive to fully litigate issues the first time"
        ],
        "micro_hypos": [
            "D found negligent in suit by P1. P2 sues D for same accident. RESULT: Offensive non-mutual collateral estoppel may apply—D already litigated negligence and lost.",
            "D wins negligence case against P1. P2 sues D for same accident. RESULT: No preclusion against P2—P2 had no opportunity to litigate the issue.",
            "Jury finds D negligent but also finds P1 50% negligent. P2 sues D. RESULT: D's negligence finding preclusive; P1's comparative negligence isn't binding on P2."
        ]
    },
    "civil_procedure_pleadings_and_motions": {
        "policy_rationales": [
            "Twombly/Iqbal plausibility standard prevents fishing expeditions through discovery",
            "Liberal amendment policy promotes resolution on merits rather than procedural technicalities",
            "Rule 12 motions allow early dismissal of meritless claims, saving resources"
        ],
        "micro_hypos": [
            "Complaint alleges 'D was negligent.' No specific facts. RESULT: Dismiss under 12(b)(6)—conclusory allegations without factual support.",
            "Plaintiff discovers new theory of liability during discovery. Wants to amend. RESULT: Amendment freely granted when justice requires (Rule 15).",
            "D fails to raise personal jurisdiction defense in answer. Raises it later. RESULT: Waived—Rule 12(h) requires certain defenses in first response."
        ]
    },
    "civil_procedure_joinder_and_discovery": {
        "policy_rationales": [
            "Liberal joinder promotes efficiency by resolving related claims in single action",
            "Compulsory counterclaims prevent piecemeal litigation of related disputes",
            "Broad discovery ensures parties have access to relevant information for fair adjudication"
        ],
        "micro_hypos": [
            "A sues B for breach of contract. B has tort claim against A from same transaction. RESULT: Compulsory counterclaim—must raise or waive.",
            "P wants to join D2 as defendant. D2 is from same state as P. RESULT: Permissive joinder allowed if same transaction; supplemental jurisdiction may apply.",
            "P requests 'all documents about product safety.' D objects as overbroad. RESULT: Court may limit—discovery must be proportional to needs of case."
        ]
    },
    "civil_procedure_pretrial_and_trial": {
        "policy_rationales": [
            "Summary judgment promotes efficiency when no genuine factual disputes exist",
            "JMOL prevents verdicts unsupported by evidence",
            "New trial corrects errors affecting substantial rights while respecting jury findings"
        ],
        "micro_hypos": [
            "P presents circumstantial evidence of negligence. D moves for SJ arguing evidence is weak. RESULT: Denied—court cannot weigh evidence; jury must assess.",
            "After P's case, D moves for JMOL. No reasonable jury could find for P. RESULT: Granted—JMOL appropriate when evidence permits only one conclusion.",
            "Juror misconduct discovered after verdict. D moves for new trial. RESULT: Granted if misconduct prejudiced substantial rights."
        ]
    },

    # CRIMINAL LAW (5 concepts)
    "criminal_law_elements_of_crimes": {
        "policy_rationales": [
            "Actus reus requirement ensures punishment for conduct, not thoughts alone",
            "Mens rea requirement reflects moral culpability—intentional harm more blameworthy than accidental",
            "Concurrence doctrine ensures mental state accompanies the criminal act"
        ],
        "micro_hypos": [
            "D has seizure, arms flail, strikes V. Charged with battery. RESULT: Not guilty—no voluntary act; seizure is involuntary.",
            "D plans murder. Before acting, D is arrested. RESULT: No crime—guilty mind alone without guilty act is not punishable.",
            "D borrows car intending to return. Later decides to keep it. RESULT: Not larceny—intent to steal must exist at time of taking."
        ]
    },
    "criminal_law_homicide_offenses": {
        "policy_rationales": [
            "Gradations of homicide reflect moral culpability—premeditated killing more blameworthy than heat-of-passion",
            "Malice aforethought requirement ensures only intentional or reckless killings receive harshest punishment",
            "Voluntary manslaughter recognizes human frailty while still condemning the killing"
        ],
        "micro_hypos": [
            "D spends two weeks planning to kill V, purchases gun, and executes plan. RESULT: First-degree murder—clear premeditation and deliberation.",
            "D finds spouse in bed with V, immediately grabs lamp and kills V. RESULT: Voluntary manslaughter—adequate provocation, heat of passion, no cooling time.",
            "D drives 90mph through school zone, killing child. RESULT: Depraved heart murder—conscious disregard of extreme risk to human life.",
            "D punches V once in bar fight; V falls, hits head, dies. RESULT: Involuntary manslaughter—criminal negligence but no intent to kill or seriously injure."
        ]
    },
    "criminal_law_felony_murder": {
        "policy_rationales": [
            "Deters dangerous felonies by imposing murder liability for resulting deaths",
            "Holds felons responsible for foreseeable consequences of their criminal conduct",
            "Reflects judgment that inherently dangerous felonies demonstrate disregard for human life"
        ],
        "micro_hypos": [
            "D robs bank; security guard has heart attack and dies from stress. RESULT: Felony murder—death during inherently dangerous felony.",
            "D commits arson; firefighter dies fighting fire. RESULT: Felony murder—arson is inherently dangerous; firefighter death foreseeable.",
            "D commits felony tax evasion; accountant dies in car accident driving to testify. RESULT: No felony murder—tax evasion not inherently dangerous.",
            "During robbery, store clerk shoots co-felon. Under agency theory: RESULT: Surviving felon not liable—clerk is not felon's agent."
        ]
    },
    "criminal_law_self_defense": {
        "policy_rationales": [
            "Recognizes natural right to protect oneself from unlawful aggression",
            "Proportionality requirement prevents excessive violence beyond what's necessary",
            "Reasonable belief standard accounts for split-second decisions in dangerous situations"
        ],
        "micro_hypos": [
            "V punches D once. D shoots V dead. RESULT: No self-defense—deadly force against non-deadly force is disproportionate.",
            "V threatens D with knife. D shoots V. RESULT: Valid self-defense—deadly force against deadly threat.",
            "D starts fight with V. V pulls knife. D retreats, V pursues. D shoots V. RESULT: Self-defense may apply—initial aggressor regained right by withdrawing.",
            "D unreasonably believes V has a gun (V is unarmed). D shoots V. RESULT: No self-defense at common law—belief must be objectively reasonable."
        ]
    },
    "criminal_law_conspiracy": {
        "policy_rationales": [
            "Targets group criminality, which is more dangerous than individual criminal action",
            "Allows intervention before crime is completed—preventive function",
            "Reflects increased likelihood that agreed-upon crimes will be carried out"
        ],
        "micro_hypos": [
            "A and B agree to rob bank. A buys ski masks. RESULT: Conspiracy complete—agreement plus overt act (buying masks).",
            "A and B agree to rob bank. Before any overt act, A tells police. RESULT: No conspiracy in jurisdictions requiring overt act; complete in others.",
            "A tells undercover cop 'let's rob the bank.' Cop 'agrees.' RESULT: No conspiracy—no meeting of guilty minds; cop never intended to commit crime.",
            "A, B conspire to rob bank. During robbery, B kills guard. RESULT: A liable for murder under Pinkerton—reasonably foreseeable."
        ]
    },
    "criminal_law_attempt": {
        "policy_rationales": [
            "Punishes dangerous conduct even when crime isn't completed",
            "Allows police intervention before harm occurs",
            "Specific intent requirement ensures we punish those who truly intended to commit crime"
        ],
        "micro_hypos": [
            "D buys gun and conducts surveillance of V's home, intending to kill V. Arrested before approaching house. RESULT: Attempt—substantial steps strongly corroborative of intent.",
            "D picks up gun, thinks about shooting V, puts gun down. RESULT: No attempt—mere preparation, no substantial step.",
            "D shoots at V intending to kill. Bullet misses. RESULT: Attempted murder—specific intent plus substantial step (shooting).",
            "D tries to pick empty pocket, not knowing it's empty. RESULT: Attempted larceny—factual impossibility is not a defense."
        ]
    },

    # CRIMINAL PROCEDURE (5 concepts)
    "criminal_procedure_fourth_amendment": {
        "policy_rationales": [
            "Protects individual privacy from arbitrary government intrusion",
            "Warrant requirement ensures neutral magistrate reviews police actions",
            "Probable cause standard balances law enforcement needs with privacy rights"
        ],
        "micro_hypos": [
            "Police search home without warrant based on anonymous tip. RESULT: Unconstitutional—home searches require warrant absent exigency.",
            "Police fly over backyard at legal altitude, observe marijuana. RESULT: Constitutional—no reasonable expectation of privacy from lawful aerial observation.",
            "Police use thermal imaging on home to detect heat lamps for growing marijuana. RESULT: Unconstitutional—sense-enhancing technology on home requires warrant (Kyllo).",
            "Police search car based on smell of marijuana. RESULT: Constitutional—automobile exception with probable cause."
        ]
    },
    "criminal_procedure_miranda": {
        "policy_rationales": [
            "Protects Fifth Amendment right against compelled self-incrimination",
            "Counteracts inherently coercive nature of custodial interrogation",
            "Ensures suspects know their rights before making statements to police"
        ],
        "micro_hypos": [
            "D is arrested, taken to station, questioned without warnings. Confesses. RESULT: Confession suppressed—custodial interrogation without Miranda.",
            "D comes to station voluntarily, told free to leave. Confesses without warnings. RESULT: Admissible—not in custody because free to leave.",
            "D is read Miranda rights, says 'maybe I want a lawyer.' Police continue questioning. D confesses. RESULT: Admissible—invocation was ambiguous.",
            "D invokes right to counsel. Police stop. Next day, D initiates conversation. RESULT: Admissible if D knowingly waived rights after initiating."
        ]
    },
    "criminal_procedure_exclusionary_rule": {
        "policy_rationales": [
            "Deters police misconduct by removing incentive for illegal searches",
            "Preserves judicial integrity by refusing to sanction illegal police conduct",
            "Protects Fourth Amendment rights by providing meaningful remedy"
        ],
        "micro_hypos": [
            "Illegal search finds drugs. D charged. RESULT: Drugs excluded from prosecution's case-in-chief.",
            "Illegal search finds drugs. D testifies he never saw drugs before. RESULT: Drugs admissible to impeach D's testimony.",
            "Police illegally arrest D. During search, discover valid outstanding warrant. D confesses. RESULT: Confession admissible—warrant attenuates taint (Strieff).",
            "Police conduct illegal search. D's gun found. Later, informant independently tells police about gun. RESULT: Gun admissible—independent source doctrine."
        ]
    },
    "criminal_procedure_sixth_amendment": {
        "policy_rationales": [
            "Guarantees effective legal representation during critical stages of prosecution",
            "Offense-specific attachment balances defendant rights with legitimate investigative needs",
            "Preserves adversarial system by preventing government from circumventing counsel"
        ],
        "micro_hypos": [
            "D indicted for robbery. Police question about uncharged burglary without counsel. RESULT: Statement admissible—Sixth Amendment is offense-specific; no charges for burglary.",
            "D indicted. Informant placed in cell. Informant asks about charged crime. D confesses. RESULT: Suppressed—deliberate elicitation after attachment.",
            "D charged with DUI. Blood test taken without D's attorney present. RESULT: Admissible—blood test is not testimonial; no Sixth Amendment violation.",
            "D's lawyer sleeps through trial. D convicted. RESULT: Ineffective assistance—prejudicial if outcome would likely differ."
        ]
    },
    "criminal_procedure_confrontation_clause": {
        "policy_rationales": [
            "Ensures reliability through cross-examination of accusers",
            "Protects against conviction based on accusations defendant cannot challenge",
            "Crawford rule distinguishes testimonial statements (require cross-examination) from non-testimonial"
        ],
        "micro_hypos": [
            "V gives statement to police describing crime. V dies before trial. RESULT: Statement inadmissible unless D had prior cross-examination opportunity.",
            "V tells friend 'D attacked me' immediately after attack. Friend testifies. RESULT: Admissible—non-testimonial (not made to police for investigation).",
            "Lab analyst writes report. Different analyst testifies about report. RESULT: May violate Confrontation Clause—D has right to cross-examine analyst who did testing.",
            "911 call describing ongoing emergency. Caller unavailable at trial. RESULT: Likely admissible—primary purpose was addressing emergency, not proving past facts."
        ]
    },

    # EVIDENCE (5 concepts)
    "evidence_hearsay": {
        "policy_rationales": [
            "Cross-examination tests accuracy and truthfulness of declarant",
            "Exceptions exist when circumstances provide reliability equivalent to cross-examination",
            "Jury should observe demeanor of witness to assess credibility"
        ],
        "micro_hypos": [
            "W testifies 'D told me he robbed the bank.' Offered to prove D committed robbery. RESULT: Hearsay—out-of-court statement offered for truth.",
            "W testifies 'D said I'll kill you' in assault case to prove threat was made. RESULT: Not hearsay—verbal act (legally operative words), not offered for truth of matter asserted.",
            "Contract case. W testifies 'Buyer said I accept.' Offered to prove acceptance. RESULT: Not hearsay—verbal act constituting acceptance.",
            "W testifies V said 'I'm feeling great' day before claimed injury. Offered to show V's state of mind. RESULT: State of mind exception applies if relevant to issue."
        ]
    },
    "evidence_character_evidence": {
        "policy_rationales": [
            "Propensity evidence risks unfair prejudice—jury may convict for bad character, not evidence of crime",
            "MIMIC purposes (motive, intent, identity, etc.) offer relevant non-propensity uses",
            "Criminal defendant may open door to character evidence as shield"
        ],
        "micro_hypos": [
            "Prosecution offers D's prior assault conviction to show D is violent person. RESULT: Inadmissible—propensity use of character evidence.",
            "D claims self-defense. Prosecution offers evidence D started previous fights. RESULT: Inadmissible unless D first offers evidence of peacefulness.",
            "D charged with fraud. Prosecution offers prior fraud conviction to show modus operandi. RESULT: Admissible under 404(b) for identity if distinctive pattern.",
            "Civil case. Plaintiff tries to introduce D's prior similar acts. RESULT: Generally inadmissible in civil cases except for MIMIC purposes."
        ]
    },
    "evidence_relevance": {
        "policy_rationales": [
            "Relevance is threshold requirement—irrelevant evidence wastes time and confuses issues",
            "Rule 403 balancing protects against unfair prejudice even when evidence is relevant",
            "Policy exclusions (subsequent remedial measures, settlement offers) encourage socially beneficial conduct"
        ],
        "micro_hypos": [
            "Personal injury case. Defendant's subsequent repair of stairway. RESULT: Inadmissible to prove negligence; admissible to prove ownership/control if disputed.",
            "Settlement offer: 'I'll pay $10K because you'd win anyway.' RESULT: Inadmissible to prove liability or damage amount.",
            "Gruesome photos of murder victim. Defense objects as prejudicial. RESULT: Court balances probative value against unfair prejudice; may limit or exclude.",
            "Evidence of unrelated crime. Prosecutor offers to show D is 'bad person.' RESULT: Inadmissible—irrelevant and highly prejudicial."
        ]
    },
    "evidence_privileges": {
        "policy_rationales": [
            "Attorney-client privilege promotes full disclosure to counsel for effective legal advice",
            "Spousal privileges protect marital harmony and intimacy",
            "Privileges exclude reliable evidence—accepted cost to protect important relationships"
        ],
        "micro_hypos": [
            "Client tells lawyer 'I robbed the bank' seeking defense advice. RESULT: Privileged—confidential communication for legal advice.",
            "Client tells lawyer 'I'm planning to rob a bank tomorrow.' RESULT: Crime-fraud exception—future crime disclosure not privileged.",
            "Wife is only witness to husband's crime. Prosecution subpoenas wife. RESULT: Spousal testimonial privilege—wife cannot be compelled to testify (criminal case).",
            "Husband tells wife 'I embezzled money' during marriage. They later divorce. RESULT: Still privileged—marital communications privilege survives divorce."
        ]
    },
    "evidence_witnesses": {
        "policy_rationales": [
            "Impeachment tests witness credibility to help jury evaluate testimony",
            "Prior inconsistent statements suggest witness may be unreliable",
            "Character for truthfulness evidence limited to reputation/opinion to avoid mini-trials on collateral issues"
        ],
        "micro_hypos": [
            "W testifies D was at scene. Cross-examiner asks about prior statement 'I didn't see D there.' RESULT: Proper impeachment with prior inconsistent statement.",
            "W is prosecution witness. Defense asks about W's pending drug charges (bias). RESULT: Admissible—pending charges show potential bias/motive to cooperate.",
            "W testifies for D. Prosecutor asks 'Didn't you lie on your tax return?' RESULT: Improper unless allowed under 608(b)—specific acts require good faith basis.",
            "W has felony conviction for theft 8 years ago. Offered to impeach. RESULT: Admissible under 609—crime of dishonesty, within 10 years."
        ]
    },

    # CONTRACTS (5 concepts)
    "contracts_formation": {
        "policy_rationales": [
            "Mutual assent ensures both parties voluntarily agreed to same terms",
            "Consideration doctrine distinguishes enforceable promises from gratuitous ones",
            "Mirror image rule provides certainty about when contract is formed"
        ],
        "micro_hypos": [
            "A offers to sell car for $10K. B says 'I'll take it for $9K.' RESULT: Counteroffer—mirror image rule rejects offer; B's statement is new offer.",
            "A promises to give B $1,000 as a gift. A changes mind. RESULT: Unenforceable—no consideration; gift promises not binding.",
            "A promises $1,000 if B quits smoking. B quits. RESULT: Enforceable—B's detriment (giving up legal right) is consideration.",
            "A offers to sell house. B mails acceptance Monday. A revokes by phone Tuesday. RESULT: Contract formed—mailbox rule; acceptance effective when sent."
        ]
    },
    "contracts_consideration": {
        "policy_rationales": [
            "Bargained-for exchange ensures reciprocity—both parties give something up",
            "Past consideration rule prevents enforcement of obligations for already-completed acts",
            "Pre-existing duty rule prevents extortion through modification demands"
        ],
        "micro_hypos": [
            "A promises to pay B $100 for mowing lawn last week. RESULT: Unenforceable—past consideration is not consideration.",
            "A owes B $10K. A offers $5K in full settlement. B accepts. RESULT: Traditionally no consideration for paying less than owed; modern view may enforce.",
            "Employer promises bonus if employee stays one more year. Employee stays. RESULT: Enforceable—employee's continued service is consideration.",
            "A contracts to build house for $100K. Midway, A demands $120K or will stop. B agrees. RESULT: Modification may be unenforceable—pre-existing duty; no new consideration."
        ]
    },
    "contracts_breach": {
        "policy_rationales": [
            "Material breach doctrine allows injured party to treat obligations as discharged",
            "Substantial performance protects against forfeiture for minor deviations",
            "Anticipatory repudiation allows immediate suit when breach is certain"
        ],
        "micro_hypos": [
            "Builder completes house but uses wrong brand of pipes (equally good). Owner refuses to pay. RESULT: Substantial performance—minor breach doesn't excuse payment; owner gets damages for difference.",
            "Builder abandons project 10% complete. Owner hires replacement at higher cost. RESULT: Material breach—owner can treat contract as discharged and sue for damages.",
            "Seller of goods says 'I won't deliver' before delivery date. Buyer finds replacement. RESULT: Anticipatory repudiation—buyer can immediately treat as breach.",
            "UCC sale: goods arrive with minor defect. RESULT: Perfect tender rule—buyer may reject any goods failing to conform in any respect."
        ]
    },
    "contracts_remedies": {
        "policy_rationales": [
            "Expectation damages put non-breaching party in position performance would have achieved",
            "Foreseeability limits liability to what parties could reasonably anticipate",
            "Specific performance reserved for situations where money damages are inadequate"
        ],
        "micro_hypos": [
            "Seller breaches contract to sell machine for $10K. Buyer finds replacement for $12K. RESULT: Expectation damages = $2K (difference in price).",
            "Carrier loses package causing buyer to miss $1M deal. Carrier didn't know about deal. RESULT: Consequential damages likely denied—loss not foreseeable by carrier.",
            "Seller breaches contract to sell unique painting. RESULT: Specific performance appropriate—painting is unique; money damages inadequate.",
            "Contract has liquidated damages clause of $10K. Actual damages are $500. RESULT: Clause may be unenforceable as penalty if amount is unreasonable."
        ]
    },
    "contracts_statute_of_frauds": {
        "policy_rationales": [
            "Writing requirement prevents fraudulent claims of oral agreements for important transactions",
            "Exceptions for part performance protect parties who rely on oral agreements",
            "UCC relaxes requirements for merchant confirmations to reflect commercial reality"
        ],
        "micro_hypos": [
            "Oral agreement to sell land. Buyer pays full price, takes possession, makes improvements. RESULT: Enforceable despite SOF—part performance exception.",
            "Oral 2-year employment contract. Employee works 6 months, is fired. RESULT: Unenforceable—cannot be performed within one year.",
            "Oral agreement to sell goods for $600. Buyer pays $200 down. RESULT: Enforceable to extent of $200 payment; SOF satisfied for paid portion.",
            "Merchant sends written confirmation of oral deal. Other merchant doesn't object within 10 days. RESULT: SOF satisfied by merchant confirmation rule."
        ]
    },
    "contracts_defenses": {
        "policy_rationales": [
            "Mutual mistake doctrine protects parties from agreements based on shared false assumptions",
            "Impossibility excuses performance when circumstances make it objectively impossible",
            "Unconscionability protects weaker parties from oppressive contract terms"
        ],
        "micro_hypos": [
            "Both parties believe painting is by famous artist. It's a copy. RESULT: Voidable for mutual mistake—basic assumption, material effect.",
            "Building burns down before contractor can renovate. RESULT: Impossibility—performance is objectively impossible; contractor excused.",
            "Consumer signs contract with hidden 50% interest rate in fine print. RESULT: May be unconscionable—procedural (hidden) and substantive (oppressive) elements."
        ]
    },

    # REAL PROPERTY (5 concepts)
    "real_property_estates_and_future_interests": {
        "policy_rationales": [
            "Estate system balances property owners' desires with societal interest in marketable land",
            "Future interests doctrine allows planning for generational wealth transfer",
            "RAP prevents dead hand control by limiting how long future interests can remain contingent"
        ],
        "micro_hypos": [
            "'To A for life, then to B.' RESULT: A has life estate; B has vested remainder in fee simple.",
            "'To A so long as used for school.' RESULT: A has fee simple determinable; grantor has possibility of reverter.",
            "'To A, but if liquor sold, to B.' RESULT: A has fee simple subject to executory limitation; B has executory interest."
        ]
    },
    "real_property_conveyancing_and_recording": {
        "policy_rationales": [
            "Recording acts protect good faith purchasers who rely on public records",
            "Race-notice jurisdictions balance recording diligence with protection from fraud",
            "Title examination promotes certainty in real property transactions"
        ],
        "micro_hypos": [
            "O sells to A (doesn't record). O sells to B (knows of A's deed). B records first. RESULT: In race-notice, A wins—B had notice.",
            "O sells to A (doesn't record). O sells to B (no knowledge of A). B records. RESULT: B wins in notice or race-notice jurisdiction.",
            "Wild deed in chain of title. Subsequent purchaser fails to find it. RESULT: May have constructive notice depending on reasonable search scope."
        ]
    },
    "real_property_adverse_possession": {
        "policy_rationales": [
            "Rewards productive use of land and punishes owners who sleep on rights",
            "Quiets title and promotes certainty in land ownership",
            "Statute of limitations provides finality and prevents stale claims"
        ],
        "micro_hypos": [
            "A uses neighbor's land openly for 12 years (10-year statute). Neighbor sues for trespass. RESULT: A owns by adverse possession—all elements met.",
            "A uses land with owner's permission. Uses for 15 years. RESULT: No adverse possession—permissive use is not hostile.",
            "A uses land hostilely for 6 years, sells to B. B uses for 5 years. RESULT: B can tack A's period—privity through sale. 11 years > 10."
        ]
    },
    "real_property_landlordtenant_law": {
        "policy_rationales": [
            "Implied warranty of habitability protects residential tenants from substandard housing",
            "Quiet enjoyment covenant ensures tenant's peaceful possession",
            "Anti-retaliation rules protect tenants who assert legal rights"
        ],
        "micro_hypos": [
            "Landlord fails to repair heating in winter despite notice. RESULT: Breach of implied warranty of habitability—tenant may withhold rent.",
            "Landlord rents apartment above, new tenant plays loud music at 3 AM. RESULT: May breach quiet enjoyment if landlord controls/causes interference.",
            "Tenant reports code violations. Landlord raises rent 50% next month. RESULT: Retaliatory—may be prohibited; rent increase voidable."
        ]
    },
    "real_property_easements_servitudes_and_licenses": {
        "policy_rationales": [
            "Easements allow beneficial use of land while respecting ownership boundaries",
            "Distinction between appurtenant and in gross affects transferability",
            "Methods of creation (express, implied, prescriptive) serve different policy goals"
        ],
        "micro_hypos": [
            "Deed grants 'right to cross Blackacre to reach highway.' A owns Whiteacre. RESULT: Easement appurtenant—benefits Whiteacre, burdens Blackacre.",
            "Utility company has power line across property. RESULT: Easement in gross—benefits company personally, not other land.",
            "A openly crosses B's land for 20 years without permission (15-year period). RESULT: Prescriptive easement—like adverse possession but for use, not title."
        ]
    },

    # TORTS (3 concepts)
    "torts_negligence": {
        "policy_rationales": [
            "Reasonable person standard provides objective measure of required care",
            "Proximate cause limits liability to foreseeable consequences",
            "Comparative fault allocates damages based on relative responsibility"
        ],
        "micro_hypos": [
            "D drives carefully but hits P who suddenly runs into street. RESULT: No breach—D acted as reasonable person; P's conduct may be superseding.",
            "D negligently starts fire. Fire spreads to P's house 2 miles away. RESULT: Proximate cause analysis—was spread foreseeable given conditions?",
            "P 30% at fault. Damages $100K. Pure comparative fault state. RESULT: P recovers $70K."
        ]
    },
    "torts_intentional_torts": {
        "policy_rationales": [
            "Intent requirement distinguishes intentional from negligent conduct",
            "Transferred intent holds wrongdoers liable even when different harm occurs",
            "Consent and privilege defenses balance protection with autonomy"
        ],
        "micro_hypos": [
            "D intends to scare P but causes harmful contact. RESULT: Battery—intent to cause apprehension transferred to harmful contact.",
            "D throws rock at A, hits B. RESULT: Transferred intent—D liable for battery to B.",
            "P consents to boxing match. D punches P. RESULT: No battery—consent to contact within scope of game."
        ]
    },
    "torts_strict_liability_and_products": {
        "policy_rationales": [
            "Strict liability for dangerous activities places loss on party best able to prevent harm",
            "Products liability ensures manufacturers internalize costs of defective products",
            "Consumer expectations test focuses on reasonable consumer's safety assumptions"
        ],
        "micro_hypos": [
            "D keeps lion as pet. Lion escapes, bites P. RESULT: Strict liability—wild animals; no negligence required.",
            "Blender blade breaks during normal use, cutting P. RESULT: Manufacturing defect—product deviated from intended design.",
            "Car lacks possible safety feature. P injured in crash. RESULT: Design defect claim—must show reasonable alternative design existed."
        ]
    }
}


def update_knowledge_base():
    """Update knowledge base with micro-hypos and policy rationales."""
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

        if concept_id in ENHANCEMENTS:
            enhancement = ENHANCEMENTS[concept_id]

            # Add policy rationales
            if "policy_rationales" in enhancement:
                existing = concept.get("policy_rationales", [])
                if not existing or len(existing) == 0:
                    concept["policy_rationales"] = enhancement["policy_rationales"]

            # Add micro-hypos
            if "micro_hypos" in enhancement:
                existing = concept.get("micro_hypos", [])
                if not existing or len(existing) == 0:
                    concept["micro_hypos"] = enhancement["micro_hypos"]

            updates_made += 1
            concepts_updated.append(concept_id)

    # Write updated knowledge base
    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)

    print(f"Updated {updates_made} concepts with micro-hypos and policy rationales:")
    for concept_id in concepts_updated:
        print(f"  - {concept_id}")

    print(f"\n{updates_made}/112 = {updates_made/112*100:.1f}% of concepts enhanced")

    return updates_made


if __name__ == "__main__":
    update_knowledge_base()

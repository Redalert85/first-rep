/**
 * Comprehensive Flashcard Database for Bar Exam Preparation
 * Covers all MBE subjects with difficulty ratings
 */

export const flashcardDatabase = [
  // ===== EVIDENCE =====
  {
    id: 1,
    subject: "Evidence",
    topic: "Hearsay Exceptions",
    question: "Excited Utterance vs. Present Sense Impression",
    answer: "Excited Utterance (803(2)): Statement relating to startling event made while under stress of excitement. Present Sense Impression (803(1)): Statement describing event made while perceiving it or immediately thereafter. Key difference: EU requires startling event + emotional stress; PSI requires contemporaneous observation.",
    subtext: "Time gap and emotional state distinguish these exceptions",
    difficulty: "Hard",
    tags: ["hearsay", "FRE 803", "exceptions"]
  },
  {
    id: 2,
    subject: "Evidence",
    topic: "Character Evidence",
    question: "Propensity Rule and MIMIC Exceptions",
    answer: "General Rule (404(a)): Character evidence inadmissible to prove conforming conduct. MIMIC Exceptions (404(b)): Evidence of other crimes/acts admissible for Motive, Intent, absence of Mistake, Identity, Common plan/scheme. Must satisfy 403 balancing test.",
    subtext: "Mnemonic: MIMIC - most tested evidence concept on MBE",
    difficulty: "Hard",
    tags: ["character", "FRE 404", "MIMIC"]
  },
  {
    id: 3,
    subject: "Evidence",
    topic: "Witness Competency",
    question: "Dead Man's Statute",
    answer: "In civil case concerning transaction with deceased, interested party cannot testify about communications/transactions with deceased unless: (1) Representative of estate waives, (2) Adverse party testifies, or (3) Other exception applies. Modern trend: Many jurisdictions have abolished this rule.",
    subtext: "Only applies in jurisdictions that adopt it - check local rules",
    difficulty: "Medium",
    tags: ["witnesses", "competency", "state law"]
  },
  {
    id: 4,
    subject: "Evidence",
    topic: "Authentication",
    question: "Self-Authenticating Documents (FRE 902)",
    answer: "No extrinsic evidence needed for: (1) Public documents with seal, (2) Certified copies of public records, (3) Newspapers/periodicals, (4) Trade inscriptions, (5) Acknowledged documents, (6) Commercial paper, (7) Business records certified by custodian.",
    subtext: "Save time on exam by recognizing self-authenticating docs",
    difficulty: "Medium",
    tags: ["authentication", "FRE 902", "documents"]
  },
  {
    id: 5,
    subject: "Evidence",
    topic: "Privileges",
    question: "Attorney-Client Privilege Elements",
    answer: "Protects confidential communications between attorney and client made for purpose of seeking/providing legal advice. Elements: (1) Communication, (2) Between attorney and client, (3) In confidence, (4) For purpose of legal advice. Exceptions: Crime-fraud, dispute between attorney-client, joint client exception.",
    subtext: "Privilege belongs to client, not attorney",
    difficulty: "Easy",
    tags: ["privileges", "attorney-client"]
  },

  // ===== CRIMINAL PROCEDURE =====
  {
    id: 6,
    subject: "Criminal Procedure",
    topic: "Search & Seizure",
    question: "Search Incident to Lawful Arrest (SILA)",
    answer: "Police may search arrestee's person and areas within immediate control (wingspan) without warrant. Justifications: officer safety and preserve evidence. For vehicles: May search passenger compartment if (1) arrestee unsecured and could access vehicle, OR (2) reasonable belief evidence of offense of arrest is in vehicle (Arizona v. Gant).",
    subtext: "Chimel v. California established wingspan doctrine",
    difficulty: "Medium",
    tags: ["Fourth Amendment", "search", "arrest"]
  },
  {
    id: 7,
    subject: "Criminal Procedure",
    topic: "Fourth Amendment",
    question: "Automobile Exception to Warrant Requirement",
    answer: "Police may search vehicle without warrant if probable cause to believe it contains contraband/evidence. Rationale: Mobility + reduced expectation of privacy. Scope: Entire vehicle including trunk and containers that could hold evidence. Unlike SILA, arrestee need not be present.",
    subtext: "Carroll doctrine - one of most important exceptions",
    difficulty: "Medium",
    tags: ["Fourth Amendment", "automobiles", "warrantless search"]
  },
  {
    id: 8,
    subject: "Criminal Procedure",
    topic: "Miranda Rights",
    question: "When Miranda Warnings Required",
    answer: "Required before custodial interrogation. Custody: Reasonable person would not feel free to leave. Interrogation: Express questioning OR conduct reasonably likely to elicit incriminating response. Warnings: Right to remain silent, statements can be used against you, right to attorney, appointed if indigent.",
    subtext: "Both custody AND interrogation required - test each separately",
    difficulty: "Medium",
    tags: ["Fifth Amendment", "Miranda", "confessions"]
  },
  {
    id: 9,
    subject: "Criminal Procedure",
    topic: "Exclusionary Rule",
    question: "Exceptions to Exclusionary Rule",
    answer: "Evidence obtained in violation of 4th/5th/6th Amendment generally excluded. Exceptions: (1) Independent source, (2) Inevitable discovery, (3) Attenuation (break in chain), (4) Good faith (reasonable reliance on warrant/law), (5) Knock-and-announce violations, (6) Impeachment use.",
    subtext: "Good faith exception does NOT apply to warrantless searches",
    difficulty: "Hard",
    tags: ["Fourth Amendment", "exclusionary rule", "exceptions"]
  },
  {
    id: 10,
    subject: "Criminal Procedure",
    topic: "Sixth Amendment",
    question: "Right to Counsel - Critical Stages",
    answer: "Attaches at initiation of adversarial proceedings (arraignment, indictment). Critical stages requiring counsel: post-indictment lineups, preliminary hearings, arraignments, plea negotiations, trial, sentencing, first appeal. NOT critical: pre-charge investigations, blood draws, handwriting samples.",
    subtext: "Offense-specific right unlike Miranda",
    difficulty: "Hard",
    tags: ["Sixth Amendment", "counsel", "critical stages"]
  },

  // ===== CRIMINAL LAW =====
  {
    id: 11,
    subject: "Criminal Law",
    topic: "Homicide",
    question: "Murder vs. Manslaughter Distinctions",
    answer: "Murder: Unlawful killing with malice aforethought - (1) Intent to kill, (2) Intent to cause serious bodily harm, (3) Depraved heart (reckless indifference), (4) Felony murder. Voluntary Manslaughter: Intentional killing with adequate provocation (heat of passion). Involuntary: Unintentional from criminal negligence or unlawful act.",
    subtext: "Cooling off period defeats heat of passion defense",
    difficulty: "Medium",
    tags: ["homicide", "murder", "manslaughter"]
  },
  {
    id: 12,
    subject: "Criminal Law",
    topic: "Felony Murder",
    question: "Felony Murder Rule and Limitations",
    answer: "Killing during commission of inherently dangerous felony = murder. BARRK felonies: Burglary, Arson, Rape, Robbery, Kidnapping. Limitations: (1) Res gestae (during felony/immediate flight), (2) Defendant must be guilty of underlying felony, (3) Death must be foreseeable, (4) Merger doctrine (felony can't be assault that caused death).",
    subtext: "Agency approach (majority): D only liable for deaths caused by D or co-felon",
    difficulty: "Hard",
    tags: ["felony murder", "BARRK", "homicide"]
  },
  {
    id: 13,
    subject: "Criminal Law",
    topic: "Inchoate Crimes",
    question: "Attempt vs. Preparation",
    answer: "Attempt requires: (1) Specific intent to commit crime, (2) Substantial step beyond mere preparation. Tests for substantial step: Proximity test (how close to completion), Equivocality test (unambiguous conduct), MPC test (strongly corroborative of intent). Legal impossibility is defense; factual impossibility is NOT.",
    subtext: "Abandonment generally NOT a defense unless statute provides",
    difficulty: "Hard",
    tags: ["attempt", "inchoate", "mens rea"]
  },
  {
    id: 14,
    subject: "Criminal Law",
    topic: "Defenses",
    question: "Self-Defense Requirements",
    answer: "Elements: (1) Reasonable belief of imminent unlawful force, (2) Force used is necessary, (3) Force is proportional. Deadly force: Only if facing death/serious bodily harm. No duty to retreat except in minority of jurisdictions (castle doctrine exception). Initial aggressor loses right unless complete withdrawal communicated.",
    subtext: "Imperfect self-defense may reduce murder to voluntary manslaughter",
    difficulty: "Medium",
    tags: ["defenses", "self-defense", "justification"]
  },
  {
    id: 15,
    subject: "Criminal Law",
    topic: "Mental State",
    question: "MPC Mental States Hierarchy",
    answer: "Purposely (conscious objective), Knowingly (aware of near certainty), Recklessly (conscious disregard of substantial risk), Negligently (should have been aware of substantial risk). Key: Each level can satisfy lower levels but not higher. If statute silent, recklessness is default.",
    subtext: "MPC approach differs from common law malice/specific intent",
    difficulty: "Medium",
    tags: ["mens rea", "MPC", "intent"]
  },

  // ===== CONTRACTS =====
  {
    id: 16,
    subject: "Contracts",
    topic: "Formation",
    question: "Battle of the Forms - UCC §2-207",
    answer: "Between merchants: (1) Definite expression of acceptance forms contract despite additional terms, (2) Additional terms become part of contract unless: material alteration, offer expressly limits acceptance, or offeror objects within reasonable time, (3) Different terms: knock-out rule applies (conflicting terms cancel, fill gap with UCC default).",
    subtext: "Critical MBE issue - memorize the three exceptions",
    difficulty: "Hard",
    tags: ["UCC", "formation", "battle of forms"]
  },
  {
    id: 17,
    subject: "Contracts",
    topic: "Consideration",
    question: "Past Consideration vs. Moral Obligation",
    answer: "Past consideration is NOT valid consideration (act already performed before promise). Exceptions: (1) Material benefit rule (promise to pay for prior benefit if just), (2) Promise to pay debt barred by statute of limitations, (3) Promise to pay debt discharged in bankruptcy. Moral obligation alone insufficient.",
    subtext: "Distinguish from pre-existing duty rule",
    difficulty: "Medium",
    tags: ["consideration", "bargain", "formation"]
  },
  {
    id: 18,
    subject: "Contracts",
    topic: "Statute of Frauds",
    question: "MY LEGS - Contracts Requiring Writing",
    answer: "Marriage (in consideration of), Year (can't perform within one year), Land (interests in), Executor (answer for estate debt), Goods ($500+ UCC, now $5000+ under amendments), Surety (answer for debt of another). Writing must contain: parties, subject matter, essential terms, signature of party to be charged.",
    subtext: "Part performance exception for land and goods",
    difficulty: "Easy",
    tags: ["statute of frauds", "MY LEGS", "writing requirement"]
  },
  {
    id: 19,
    subject: "Contracts",
    topic: "Remedies",
    question: "Expectation Damages Formula",
    answer: "Put non-breaching party in position if contract performed. Formula: Loss in Value + Other Loss (incidental/consequential) - Cost Avoided - Loss Avoided. Consequential damages must be: (1) Foreseeable at contract formation, (2) Proven with reasonable certainty. Mitigation duty: Cannot recover avoidable losses.",
    subtext: "Hadley v. Baxendale foreseeability standard",
    difficulty: "Medium",
    tags: ["remedies", "damages", "breach"]
  },
  {
    id: 20,
    subject: "Contracts",
    topic: "Third Party Beneficiaries",
    question: "Intended vs. Incidental Beneficiary",
    answer: "Intended beneficiary: Party intended to benefit from contract, has rights to enforce. Two types: (1) Creditor beneficiary (performance satisfies promisee's debt to beneficiary), (2) Donee beneficiary (promisee's intent to make gift). Incidental beneficiary: Unintended benefit, NO enforcement rights. Vesting: Rights vest when beneficiary (1) learns and assents, (2) relies, or (3) sues.",
    subtext: "Test: Would reasonable person believe promisor assumed duty to beneficiary?",
    difficulty: "Hard",
    tags: ["third party", "beneficiary", "privity"]
  },

  // ===== TORTS =====
  {
    id: 21,
    subject: "Torts",
    topic: "Negligence",
    question: "Res Ipsa Loquitur Inference",
    answer: "Allows negligence inference when direct evidence unavailable. Elements: (1) Accident normally doesn't occur without negligence, (2) Instrumentality under defendant's exclusive control, (3) Plaintiff didn't contribute to accident. Effect: Creates permissible inference, shifts burden of production (not persuasion) to defendant. Avoids directed verdict.",
    subtext: "Classic examples: falling objects, surgical instruments left in body",
    difficulty: "Easy",
    tags: ["negligence", "res ipsa", "breach"]
  },
  {
    id: 22,
    subject: "Torts",
    topic: "Products Liability",
    question: "Strict Liability for Defective Products",
    answer: "Elements: (1) Defendant is commercial seller in distribution chain, (2) Product defective when left D's control (manufacturing, design, or warning defect), (3) Plaintiff was foreseeable user, (4) Defect caused injury. No privity required. Design defect tests: Consumer expectation OR risk-utility (safer alternative feasible).",
    subtext: "Learned intermediary rule for prescription drugs",
    difficulty: "Medium",
    tags: ["products liability", "strict liability", "defects"]
  },
  {
    id: 23,
    subject: "Torts",
    topic: "Intentional Torts",
    question: "Battery vs. Assault",
    answer: "Battery: (1) Intent to cause harmful/offensive contact or imminent apprehension thereof, (2) Harmful/offensive contact with plaintiff or something closely connected to plaintiff. Assault: (1) Intent to cause apprehension of imminent harmful/offensive contact, (2) Plaintiff reasonably apprehends such contact. Words alone insufficient for assault; mere contact insufficient for battery without offensiveness.",
    subtext: "Intent can be transferred between torts and victims",
    difficulty: "Easy",
    tags: ["intentional torts", "battery", "assault"]
  },
  {
    id: 24,
    subject: "Torts",
    topic: "Defamation",
    question: "Public Figure vs. Private Figure Standard",
    answer: "Public Figure/Official: Plaintiff must prove actual malice (knowledge of falsity OR reckless disregard for truth). Private Figure + Public Concern: States set standard but must require at least negligence; actual malice for punitive damages. Private Figure + Private Concern: States set standard, no constitutional restrictions. Special damages required for slander unless per se.",
    subtext: "New York Times v. Sullivan - actual malice standard",
    difficulty: "Hard",
    tags: ["defamation", "First Amendment", "public figure"]
  },
  {
    id: 25,
    subject: "Torts",
    topic: "Nuisance",
    question: "Private vs. Public Nuisance",
    answer: "Private Nuisance: Substantial and unreasonable interference with another's use/enjoyment of land. Balancing test: gravity of harm vs. utility of conduct. Remedies: injunction or damages. Public Nuisance: Unreasonable interference with right common to general public. Private plaintiff must show special injury different in kind, not just degree.",
    subtext: "Coming to the nuisance generally not a complete defense",
    difficulty: "Medium",
    tags: ["nuisance", "property", "interference"]
  },

  // ===== REAL PROPERTY =====
  {
    id: 26,
    subject: "Real Property",
    topic: "Adverse Possession",
    question: "Elements of Adverse Possession (COAH)",
    answer: "Possession must be: (1) Continuous for statutory period (typically 10-20 years), (2) Open & Notorious (visible, obvious to true owner), (3) Actual & Exclusive (not shared with owner/public), (4) Hostile (without owner's permission). Tacking allowed if privity between successive possessors. Adverse possessor gets title equal to what they possessed.",
    subtext: "Disability tolls statute if existing when AP begins",
    difficulty: "Medium",
    tags: ["adverse possession", "COAH", "title"]
  },
  {
    id: 27,
    subject: "Real Property",
    topic: "Future Interests",
    question: "Remainders: Vested vs. Contingent",
    answer: "Vested Remainder: Created in ascertained person, no conditions precedent except natural end of prior estate. Types: absolutely vested, vested subject to open (class gift), vested subject to complete defeasance. Contingent Remainder: Created in unascertained person OR subject to condition precedent. Preference for vested construction resolves ambiguity.",
    subtext: "Rule Against Perpetuities only applies to contingent remainders",
    difficulty: "Hard",
    tags: ["future interests", "remainders", "estates"]
  },
  {
    id: 28,
    subject: "Real Property",
    topic: "Covenants Running with Land",
    answer: "Real Covenant (damages): (1) Writing, (2) Intent to run, (3) Touch and concern land, (4) Horizontal privity (original parties in land transaction) + Vertical privity (succession). Equitable Servitude (injunction): (1) Writing (or inquiry notice), (2) Intent, (3) Touch and concern, (4) Notice to subsequent purchaser. No privity required for ES.",
    subtext: "Modern trend: Touch and concern test replaced by reasonableness",
    difficulty: "Hard",
    tags: ["covenants", "servitudes", "privity"]
  },
  {
    id: 29,
    subject: "Real Property",
    topic: "Recording Acts",
    question: "Notice vs. Race-Notice vs. Race",
    answer: "Notice: Subsequent BFP (bona fide purchaser) without notice wins, even if they don't record. Race-Notice: Subsequent BFP without notice who records FIRST wins. Race: First to record wins regardless of notice (rare). BFP requires: (1) Purchase for value (not gift/heir), (2) Without actual, constructive (record), or inquiry (visible) notice. Shelter rule: Those who take from BFP protected.",
    subtext: "Identify jurisdiction type before applying rule",
    difficulty: "Medium",
    tags: ["recording acts", "BFP", "priority"]
  },
  {
    id: 30,
    subject: "Real Property",
    topic: "Landlord-Tenant",
    question: "Implied Warranty of Habitability",
    answer: "Modern trend: Landlord must maintain residential premises in habitable condition. Breached by substantial defects (heat, water, electricity, sanitation). Tenant remedies: (1) Move out and terminate, (2) Repair and deduct, (3) Withhold rent (may need escrow), (4) Damages. Waiver generally unenforceable. Applies only to residential, not commercial leases.",
    subtext: "Separate from covenant of quiet enjoyment",
    difficulty: "Medium",
    tags: ["landlord-tenant", "habitability", "residential"]
  },

  // ===== CONSTITUTIONAL LAW =====
  {
    id: 31,
    subject: "Constitutional Law",
    topic: "Equal Protection",
    question: "Three Levels of Scrutiny",
    answer: "Strict Scrutiny: Suspect class (race, national origin, alienage*) OR fundamental right - law must be narrowly tailored to compelling government interest. Intermediate: Quasi-suspect (gender, legitimacy) - substantially related to important interest. Rational Basis: All others - rationally related to legitimate interest. *State alienage classifications get strict; federal get rational basis.",
    subtext: "Most laws survive rational basis; most fail strict scrutiny",
    difficulty: "Medium",
    tags: ["equal protection", "scrutiny", "14th Amendment"]
  },
  {
    id: 32,
    subject: "Constitutional Law",
    topic: "Dormant Commerce Clause",
    question: "State Regulation of Interstate Commerce",
    answer: "State law burdening interstate commerce violates DCC unless: (1) Legitimate local interest, (2) No less discriminatory alternative, (3) Benefits outweigh burdens (balancing test). Discriminatory laws (facial or in effect): Virtually per se invalid unless necessary for important state interest. Market participant exception: State can favor its own citizens when acting as buyer/seller.",
    subtext: "Congressional authorization can permit state discrimination",
    difficulty: "Hard",
    tags: ["commerce clause", "federalism", "state power"]
  },
  {
    id: 33,
    subject: "Constitutional Law",
    topic: "First Amendment",
    question: "Content-Based vs. Content-Neutral Speech Restrictions",
    answer: "Content-Based: Strict scrutiny - narrowly tailored to compelling interest. Includes viewpoint and subject matter restrictions. Content-Neutral: Intermediate scrutiny - narrowly tailored to significant interest with ample alternative channels. Time, place, manner restrictions in public forum must be content-neutral. Categories outside protection: obscenity, incitement, fighting words, true threats, defamation.",
    subtext: "Government can't regulate speech based on message",
    difficulty: "Hard",
    tags: ["First Amendment", "speech", "scrutiny"]
  },
  {
    id: 34,
    subject: "Constitutional Law",
    topic: "Takings Clause",
    question: "When Does Regulation Constitute Taking?",
    answer: "Physical taking: Any permanent physical occupation = taking (Loretto). Regulatory taking: (Penn Central factors): (1) Economic impact, (2) Interference with reasonable investment-backed expectations, (3) Character of regulation. Per se taking if: (1) Regulation denies ALL economic value (Lucas), (2) Permanent physical invasion. Exactions must have nexus and rough proportionality (Nollan/Dolan).",
    subtext: "Just compensation = fair market value at time of taking",
    difficulty: "Hard",
    tags: ["Fifth Amendment", "takings", "property"]
  },
  {
    id: 35,
    subject: "Constitutional Law",
    topic: "Justiciability",
    question: "Standing Requirements",
    answer: "Constitutional standing: (1) Injury in fact (concrete and particularized, actual or imminent), (2) Causation (fairly traceable to defendant's conduct), (3) Redressability (favorable decision likely to remedy injury). Prudential standing: (1) No generalized grievances, (2) Assert own rights not third parties (exceptions: close relationship + hindrance, or First Amendment overbreadth), (3) Within zone of interests. Organizations: Members have standing OR direct injury to organization.",
    subtext: "Standing assessed at time suit is filed",
    difficulty: "Hard",
    tags: ["justiciability", "standing", "Article III"]
  },

  // ===== CIVIL PROCEDURE =====
  {
    id: 36,
    subject: "Civil Procedure",
    topic: "Personal Jurisdiction",
    question: "Minimum Contacts Test",
    answer: "Due process requires defendant have minimum contacts with forum such that maintenance of suit doesn't offend traditional notions of fair play and substantial justice. Specific jurisdiction: Purposeful availment + claim arises from contacts. General jurisdiction: Continuous and systematic contacts (essentially at home - incorporation/principal place for corporations). Reasonableness factors: burden, forum interest, plaintiff interest, efficiency, policy interests.",
    subtext: "International Shoe v. Washington framework",
    difficulty: "Hard",
    tags: ["jurisdiction", "due process", "minimum contacts"]
  },
  {
    id: 37,
    subject: "Civil Procedure",
    topic: "Subject Matter Jurisdiction",
    question: "Diversity Jurisdiction Requirements",
    answer: "28 U.S.C. §1332: (1) Complete diversity (no plaintiff shares citizenship with any defendant), (2) Amount in controversy exceeds $75,000. Citizenship: Individuals - domicile (residence + intent to remain); Corporations - incorporation AND principal place of business (nerve center); Unincorporated associations - citizenship of all members. Determined at filing; subsequent events don't destroy.",
    subtext: "Aggregation allowed for single P v. single D; not for multiple Ds",
    difficulty: "Medium",
    tags: ["SMJ", "diversity", "federal courts"]
  },
  {
    id: 38,
    subject: "Civil Procedure",
    topic: "Erie Doctrine",
    question: "Federal Courts Applying State Law",
    answer: "Federal courts exercising diversity jurisdiction must apply: (1) State substantive law (Erie), (2) Federal procedural law (Hanna). Analysis: If Federal Rule on point and valid (REA + Constitutional), apply Federal Rule (Hanna). If no Federal Rule, outcome determinative test + balance interests (York/Byrd). State law governs: SOL, choice of law, elements of claim/defense. Federal law: Pleading, discovery, jury instructions (form not content).",
    subtext: "Goal: Prevent forum shopping and inequitable administration",
    difficulty: "Hard",
    tags: ["Erie", "federalism", "choice of law"]
  },
  {
    id: 39,
    subject: "Civil Procedure",
    topic: "Class Actions",
    question: "Rule 23 Requirements",
    answer: "Prerequisites (23(a)): (1) Numerosity, (2) Commonality, (3) Typicality, (4) Adequacy of representation. Plus one type: (b)(1) - risk of inconsistent obligations or impair absent members' interests; (b)(2) - injunctive/declaratory relief appropriate for class; (b)(3) - common questions predominate + class action superior (opt-out available). Court approval required for settlement. Notice required for (b)(3).",
    subtext: "Diversity jurisdiction requires minimal diversity only",
    difficulty: "Hard",
    tags: ["class actions", "Rule 23", "procedure"]
  },
  {
    id: 40,
    subject: "Civil Procedure",
    topic: "Summary Judgment",
    question: "Rule 56 Standard",
    answer: "Court must grant if movant shows no genuine dispute of material fact and entitled to judgment as matter of law. Burden: Movant bears initial burden to identify lack of evidence. Then non-movant must show genuine factual dispute. Court views evidence in light most favorable to non-movant. Issue of fact is 'genuine' if reasonable jury could return verdict for non-movant. Credibility determinations inappropriate.",
    subtext: "Distinguish from Rule 12(b)(6) - different standard",
    difficulty: "Medium",
    tags: ["summary judgment", "Rule 56", "procedure"]
  }
];

// Subject categories for filtering
export const subjects = [
  "All",
  "Evidence",
  "Criminal Procedure",
  "Criminal Law",
  "Contracts",
  "Torts",
  "Real Property",
  "Constitutional Law",
  "Civil Procedure"
];

// Difficulty levels
export const difficulties = ["Easy", "Medium", "Hard"];

// Utility functions
export const getCardsBySubject = (subject) => {
  if (subject === "All") return flashcardDatabase;
  return flashcardDatabase.filter(card => card.subject === subject);
};

export const getCardsByDifficulty = (difficulty) => {
  return flashcardDatabase.filter(card => card.difficulty === difficulty);
};

export const getCardsByTag = (tag) => {
  return flashcardDatabase.filter(card => card.tags && card.tags.includes(tag));
};

export const getRandomCard = (subject = "All") => {
  const cards = getCardsBySubject(subject);
  return cards[Math.floor(Math.random() * cards.length)];
};

export const searchCards = (query) => {
  const lowerQuery = query.toLowerCase();
  return flashcardDatabase.filter(card =>
    card.question.toLowerCase().includes(lowerQuery) ||
    card.answer.toLowerCase().includes(lowerQuery) ||
    card.topic.toLowerCase().includes(lowerQuery) ||
    card.subject.toLowerCase().includes(lowerQuery)
  );
};

// Statistics
export const getSubjectDistribution = () => {
  const distribution = {};
  flashcardDatabase.forEach(card => {
    distribution[card.subject] = (distribution[card.subject] || 0) + 1;
  });
  return distribution;
};

export const getDifficultyDistribution = () => {
  const distribution = {};
  flashcardDatabase.forEach(card => {
    distribution[card.difficulty] = (distribution[card.difficulty] || 0) + 1;
  });
  return distribution;
};

export default flashcardDatabase;

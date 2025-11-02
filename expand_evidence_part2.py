#!/usr/bin/env python3
"""
Evidence Subject Expansion Part 2: Final 27 Concepts
Adds Privileges, Expert Testimony, Impeachment, and Miscellaneous Evidence
Completes expansion to 120 total Evidence concepts
"""

import json
from pathlib import Path

def create_final_evidence_concepts():
    """Create final 27 Evidence concepts"""

    new_concepts = []

    # ========== PRIVILEGES (7 concepts) ==========

    privilege_concepts = [
        {
            'concept_id': 'evidence_privilege_attorney_client',
            'name': 'Attorney-Client Privilege',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Confidential communications between attorney and client for legal advice privileged',
            'elements': ['Attorney-client relationship', 'Communication', 'Made in confidence', 'For purpose of legal advice'],
            'exceptions': ['Crime-fraud exception', 'Future crime/fraud', 'Waiver', 'Joint clients against each other'],
            'policy_rationales': ['Encourage full disclosure to attorney', 'Effective legal representation', 'Fundamental to adversary system'],
            'common_traps': ['Thinking covers facts', 'Missing crime-fraud exception', 'Forgetting waiver by disclosure to third party'],
            'teach': 'ATTORNEY-CLIENT = Confidential communications for legal advice. NOT facts, NOT future crimes.',
            'question': 'Client tells lawyer "I plan to commit tax fraud." Privileged?',
            'choices': {'A': 'Yes-privileged', 'B': 'Yes-confidential', 'C': 'No-crime-fraud', 'D': 'No-not legal advice'},
            'answer': 'C',
            'why': 'Crime-fraud exception: communications in furtherance of future crime/fraud not privileged.',
            'source': 'expanded',
            'exam_frequency': 'very high'
        },
        {
            'concept_id': 'evidence_privilege_work_product',
            'name': 'Work Product Doctrine',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Attorney\'s trial preparation materials protected from discovery absent substantial need',
            'elements': ['Prepared in anticipation of litigation', 'By attorney or representative', 'Core work product (mental impressions) strongly protected'],
            'exceptions': ['Substantial need + undue hardship to obtain equivalent', 'Core work product almost never discoverable'],
            'policy_rationales': ['Protect attorney\'s thought process', 'Prevent adversary free-riding', 'Zealous advocacy'],
            'common_traps': ['Confusing with attorney-client privilege', 'Thinking it\'s absolute', 'Missing "anticipation of litigation"'],
            'teach': 'WORK PRODUCT = Attorney trial prep protected. Core mental impressions = super protected.',
            'question': 'Attorney\'s notes analyzing case strategy. Discoverable if opponent shows substantial need?',
            'choices': {'A': 'Yes-substantial need', 'B': 'Yes-work product', 'C': 'No-core work product', 'D': 'No-privileged'},
            'answer': 'C',
            'why': 'Core work product (mental impressions, strategies) protected even with substantial need.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_privilege_spousal_immunity',
            'name': 'Spousal Immunity (Testimonial Privilege)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Married person may refuse to testify against spouse in criminal case',
            'elements': ['Valid marriage at time of trial', 'Criminal case', 'Witness spouse holds privilege'],
            'exceptions': ['Crimes against spouse or children', 'Federal: witness spouse decides', 'Majority: defendant spouse decides'],
            'policy_rationales': ['Preserve marital harmony', 'Prevent forcing testimony against spouse', 'Family unit protection'],
            'common_traps': ['Applying to civil cases', 'Who holds privilege varies by jurisdiction', 'Forgetting "at time of trial" rule'],
            'teach': 'SPOUSAL IMMUNITY = Married now? Can refuse to testify against spouse (criminal only). Witness holds privilege.',
            'question': 'Husband charged with tax fraud. Wife witness to fraud. Must wife testify?',
            'choices': {'A': 'Yes-relevant', 'B': 'Yes-no privilege', 'C': 'No-spousal immunity', 'D': 'No-if choose not to'},
            'answer': 'D',
            'why': 'Spousal immunity (testimonial privilege): witness spouse may refuse to testify in criminal case.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_privilege_marital_communications',
            'name': 'Marital Communications Privilege',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Confidential communications between spouses during valid marriage privileged',
            'elements': ['Confidential communication', 'During valid marriage', 'Both spouses hold privilege', 'Survives divorce'],
            'exceptions': ['Crimes against spouse/children', 'Not confidential if third party present'],
            'policy_rationales': ['Encourage marital communications', 'Protect intimacy', 'Preserve family unit'],
            'common_traps': ['Confusing with spousal immunity', 'Missing "during marriage" timing', 'Forgetting survives divorce'],
            'teach': 'MARITAL COMMUNICATIONS = Said during marriage in confidence? Privileged forever. Both spouses hold it.',
            'question': 'Husband told wife "I committed fraud" during marriage. Now divorced. Wife can testify?',
            'choices': {'A': 'Yes-divorced', 'B': 'Yes-crime', 'C': 'No-marital privilege', 'D': 'No-unless wife waives'},
            'answer': 'C',
            'why': 'Marital communications privilege survives divorce. Communication during marriage protected.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_privilege_psychotherapist',
            'name': 'Psychotherapist-Patient Privilege',
            'subject': 'evidence',
            'difficulty': 3,
            'rule_statement': 'Confidential communications to licensed psychotherapist for diagnosis/treatment privileged',
            'elements': ['Licensed psychotherapist', 'Confidential communication', 'For diagnosis/treatment', 'Patient holds privilege'],
            'exceptions': ['Patient-litigant exception', 'Dangerous patient', 'Court-ordered examination'],
            'policy_rationales': ['Effective mental health treatment', 'Encourage full disclosure', 'Protect privacy'],
            'common_traps': ['Applying to non-licensed counselors', 'Missing dangerous patient exception', 'Forgetting patient-litigant exception'],
            'teach': 'PSYCHOTHERAPIST = Mental health treatment confidential. Patient holds privilege.',
            'question': 'Patient sues for emotional distress, putting mental state at issue. Therapy communications privileged?',
            'choices': {'A': 'Yes-privileged', 'B': 'Yes-unless waived', 'C': 'No-patient-litigant exception', 'D': 'No-in suit'},
            'answer': 'C',
            'why': 'Patient-litigant exception: by putting mental state at issue, patient waives psychotherapist privilege.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        },
        {
            'concept_id': 'evidence_privilege_physician_patient',
            'name': 'Physician-Patient Privilege',
            'subject': 'evidence',
            'difficulty': 3,
            'rule_statement': 'In some states, communications to physician for treatment privileged (not in federal law)',
            'elements': ['State privilege only (no federal)', 'Communication for treatment', 'Patient holds privilege'],
            'exceptions': ['Patient-litigant exception', 'Court-ordered examination', 'Many states don\'t recognize'],
            'policy_rationales': ['Encourage seeking treatment', 'Medical privacy', 'Effective healthcare'],
            'common_traps': ['Thinking exists in federal court', 'Confusing with psychotherapist privilege', 'Missing patient-litigant exception'],
            'teach': 'PHYSICIAN-PATIENT = State privilege only (NO federal privilege). Patient-litigant exception common.',
            'question': 'Federal court diversity case. State has physician-patient privilege. Applies in federal court?',
            'choices': {'A': 'Yes-state privilege', 'B': 'Yes-Erie', 'C': 'No-federal rules', 'D': 'Depends on 501'},
            'answer': 'D',
            'why': 'FRE 501: state law privileges apply in diversity cases. Federal common law in federal question cases.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        },
        {
            'concept_id': 'evidence_privilege_waiver',
            'name': 'Privilege Waiver',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Privilege waived by voluntary disclosure or by putting privileged matter at issue',
            'elements': ['Voluntary disclosure to third party', 'Putting matter at issue (patient-litigant)', 'Failure to claim privilege'],
            'exceptions': ['Inadvertent disclosure (may not waive if steps taken)', 'Partial disclosure may waive all on topic'],
            'policy_rationales': ['Cannot use privilege as shield and sword', 'Fairness', 'Prevent selective disclosure'],
            'common_traps': ['Thinking inadvertent disclosure always waives', 'Missing partial disclosure rule', 'Forgetting topic waiver'],
            'teach': 'PRIVILEGE WAIVER = Disclose to third party OR put at issue = lose privilege. Can\'t have it both ways.',
            'question': 'Client tells friend what lawyer said. Attorney-client privilege waived?',
            'choices': {'A': 'Yes-disclosed', 'B': 'Yes-third party', 'C': 'No-friend not party', 'D': 'No-still confidential'},
            'answer': 'A',
            'why': 'Voluntary disclosure to third party waives attorney-client privilege. No longer confidential.',
            'source': 'expanded',
            'exam_frequency': 'high'
        }
    ]

    new_concepts.extend(privilege_concepts)

    # ========== EXPERT TESTIMONY (6 concepts) ==========

    expert_concepts = [
        {
            'concept_id': 'evidence_expert_daubert',
            'name': 'Daubert Standard for Expert Testimony',
            'subject': 'evidence',
            'difficulty': 5,
            'rule_statement': 'Expert testimony admissible if scientific knowledge will help trier of fact and reliable methodology',
            'elements': ['Qualified expert', 'Scientific/technical knowledge', 'Reliable methodology (Daubert factors)', 'Relevant/helpful to fact-finder'],
            'exceptions': ['Daubert factors not exclusive checklist', 'Judge has discretion'],
            'policy_rationales': ['Screen junk science', 'Ensure reliability', 'Help jury with complex matters'],
            'common_traps': ['Applying Frye in federal court', 'Thinking Daubert factors mandatory', 'Missing gatekeeper role'],
            'teach': 'DAUBERT = Federal standard. Reliable methodology + helpful = admissible. Judge is gatekeeper.',
            'question': 'Expert uses novel scientific method not peer-reviewed. Admissible under Daubert?',
            'choices': {'A': 'Yes-if qualified', 'B': 'Yes-novel OK', 'C': 'No-need peer review', 'D': 'Maybe-judge decides'},
            'answer': 'D',
            'why': 'Peer review is one Daubert factor, not requirement. Judge has discretion as gatekeeper.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_expert_frye',
            'name': 'Frye Standard (General Acceptance)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Scientific evidence admissible if methodology generally accepted in relevant scientific community',
            'elements': ['Scientific method', 'General acceptance in field', 'Relevant scientific community'],
            'exceptions': ['Some states still use Frye', 'Federal courts use Daubert'],
            'policy_rationales': ['Conservative approach', 'Rely on scientific consensus', 'Avoid novel methods'],
            'common_traps': ['Using in federal court (Daubert superseded)', 'Missing "general acceptance" requirement', 'Confusing with Daubert'],
            'teach': 'FRYE = Old standard. Generally accepted in scientific community? Some states still use.',
            'question': 'State court using Frye. Novel but reliable scientific method. Admissible?',
            'choices': {'A': 'Yes-reliable', 'B': 'Yes-Daubert', 'C': 'No-not generally accepted', 'D': 'No-novel'},
            'answer': 'C',
            'why': 'Under Frye, must be generally accepted in scientific community. Novel = not accepted yet.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        },
        {
            'concept_id': 'evidence_expert_702',
            'name': 'Expert Testimony Requirements (FRE 702)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Expert may testify if qualified and testimony based on sufficient facts/data and reliable principles reliably applied',
            'elements': ['Expert qualified by knowledge/skill/experience/training/education', 'Help trier of fact', 'Sufficient facts/data', 'Reliable principles', 'Reliably applied'],
            'policy_rationales': ['Ensure expertise', 'Screen unreliable opinions', 'Help fact-finder'],
            'common_traps': ['Missing "reliably applied" requirement', 'Thinking qualification alone sufficient', 'Forgetting sufficient basis'],
            'teach': 'FRE 702 = Qualified + reliable principles reliably applied + helpful = admissible expert testimony.',
            'question': 'Doctor uses reliable medical principles but applies them incorrectly. Admissible under 702?',
            'choices': {'A': 'Yes-qualified', 'B': 'Yes-reliable principles', 'C': 'No-not reliably applied', 'D': 'No-not expert'},
            'answer': 'C',
            'why': 'Must reliably APPLY principles, not just use reliable principles. Application matters.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_expert_703',
            'name': 'Bases of Expert Opinion (FRE 703)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Expert may base opinion on facts/data reasonably relied upon by experts in field, even if inadmissible',
            'elements': ['Facts reasonably relied upon in field', 'May be inadmissible evidence', 'Probative value vs. prejudice (if disclosed to jury)'],
            'policy_rationales': ['Experts work with all information', 'Practical reality', 'Still protect jury from prejudice'],
            'common_traps': ['Thinking expert can only use admissible evidence', 'Admitting basis without 403 analysis', 'Missing disclosure limitations'],
            'teach': 'FRE 703 = Expert can use inadmissible evidence as basis if reasonably relied upon in field.',
            'question': 'Expert bases opinion on hearsay report. Can expert testify to opinion?',
            'choices': {'A': 'Yes-if reliable', 'B': 'Yes-if reasonably relied upon', 'C': 'No-hearsay inadmissible', 'D': 'No-need exception'},
            'answer': 'B',
            'why': 'Expert can base opinion on inadmissible evidence if reasonably relied upon by experts in field.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_expert_704',
            'name': 'Opinion on Ultimate Issue (FRE 704)',
            'subject': 'evidence',
            'difficulty': 3,
            'rule_statement': 'Expert may opine on ultimate issue except in criminal cases regarding defendant\'s mental state',
            'elements': ['Ultimate issue testimony allowed', 'Exception: criminal defendant mental state', 'Still must be helpful'],
            'exceptions': ['Cannot testify defendant had/lacked mental state in criminal case'],
            'policy_rationales': ['Help jury', 'Modern approach', 'But protect criminal defendants from dispositive expert testimony'],
            'common_traps': ['Thinking ultimate issue always barred', 'Missing criminal mental state exception', 'Confusing with 701'],
            'teach': 'FRE 704 = Expert CAN opine on ultimate issue (except criminal defendant mental state).',
            'question': 'Civil case. Can expert testify "Defendant was negligent"?',
            'choices': {'A': 'Yes-ultimate issue OK', 'B': 'Yes-helpful', 'C': 'No-ultimate issue', 'D': 'No-jury decides'},
            'answer': 'A',
            'why': 'Ultimate issue testimony permitted under 704. Expert may opine on negligence in civil case.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        },
        {
            'concept_id': 'evidence_expert_lay_opinion',
            'name': 'Lay vs. Expert Opinion (FRE 701 vs. 702)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Lay opinion admissible if rationally based on perception and helpful; expert opinion for specialized knowledge',
            'elements': ['Lay (701): perception-based, not specialized knowledge', 'Expert (702): specialized knowledge needed', 'Lay: cannot be based on scientific/technical knowledge'],
            'policy_rationales': ['Allow common sense observations', 'Distinguish from expert testimony', 'Prevent disguised expert testimony'],
            'common_traps': ['Allowing lay witnesses to give expert opinions', 'Missing perception requirement for lay', 'Using 701 for specialized knowledge'],
            'teach': 'LAY OPINION (701) = What you saw/experienced. EXPERT (702) = Specialized knowledge needed.',
            'question': 'Lay witness: "Car was going 70 mph." Admissible as lay opinion?',
            'choices': {'A': 'Yes-lay opinion', 'B': 'Yes-perception', 'C': 'No-need expert', 'D': 'No-speculation'},
            'answer': 'A',
            'why': 'Speed estimation from observation = lay opinion (701). Rationally based on perception.',
            'source': 'expanded',
            'exam_frequency': 'high'
        }
    ]

    new_concepts.extend(expert_concepts)

    # ========== IMPEACHMENT (6 concepts) ==========

    impeachment_concepts = [
        {
            'concept_id': 'evidence_impeachment_prior_inconsistent',
            'name': 'Prior Inconsistent Statement (613)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Witness may be impeached by showing prior inconsistent statement if given opportunity to explain',
            'elements': ['Prior statement', 'Inconsistent with trial testimony', 'Witness given opportunity to explain', 'Extrinsic evidence allowed if opportunity given'],
            'exceptions': ['May use without opportunity if witness still available', 'Collateral matters - no extrinsic evidence'],
            'policy_rationales': ['Test credibility', 'Show witness unreliable', 'Fairness'],
            'common_traps': ['Thinking must confront before using', 'Using extrinsic evidence on collateral matters', 'Missing explain/deny opportunity'],
            'teach': 'PRIOR INCONSISTENT = Said X before, Y now? Shows unreliable. Give chance to explain.',
            'question': 'Impeach with prior statement. Must confront witness with statement first?',
            'choices': {'A': 'Yes-always', 'B': 'Yes-before extrinsic', 'C': 'No-if opportunity given', 'D': 'No-never required'},
            'answer': 'C',
            'why': 'Need opportunity to explain but can give at any time. Modern rule allows extrinsic evidence if opportunity given.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_impeachment_bias',
            'name': 'Impeachment by Bias',
            'subject': 'evidence',
            'difficulty': 3,
            'rule_statement': 'Witness may be impeached by showing bias, prejudice, or motive to lie',
            'elements': ['Bias/prejudice/motive', 'Always relevant to credibility', 'Extrinsic evidence allowed'],
            'policy_rationales': ['Central to credibility', 'Always probative', 'Constitutional right (Confrontation Clause)'],
            'common_traps': ['Thinking collateral matter rule applies to bias', 'Missing that bias always admissible', 'Confusing with character'],
            'teach': 'BIAS = Always relevant to impeach. NOT collateral. Can use extrinsic evidence.',
            'question': 'Witness is plaintiff\'s brother. Can cross-examine about relationship to show bias?',
            'choices': {'A': 'Yes-bias relevant', 'B': 'Yes-credibility', 'C': 'No-collateral', 'D': 'No-unfair'},
            'answer': 'A',
            'why': 'Bias always relevant to credibility. Family relationship shows potential bias/motive.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_impeachment_sensory_deficiency',
            'name': 'Impeachment by Sensory/Mental Deficiency',
            'subject': 'evidence',
            'difficulty': 3,
            'rule_statement': 'Witness may be impeached by showing deficiency in capacity to observe, remember, or relate',
            'elements': ['Sensory deficiency (sight, hearing)', 'Memory problems', 'Mental capacity', 'Drug/alcohol impairment'],
            'policy_rationales': ['Test ability to perceive and relate', 'Credibility fundamental', 'Jury needs to know limitations'],
            'common_traps': ['Thinking it attacks character', 'Missing specific vs. general capacity', 'Not distinguishing from bias'],
            'teach': 'SENSORY/MENTAL = Could witness see/hear/remember? Affects ability to testify accurately.',
            'question': 'Witness was drunk at time of observation. Can cross-examine about intoxication?',
            'choices': {'A': 'Yes-affects perception', 'B': 'Yes-credibility', 'C': 'No-character', 'D': 'No-unfair'},
            'answer': 'A',
            'why': 'Intoxication at time of observation affects ability to perceive. Relevant to impeach.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        },
        {
            'concept_id': 'evidence_impeachment_contradiction',
            'name': 'Impeachment by Contradiction',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Witness may be impeached by showing testimony contradicted by other evidence',
            'elements': ['Testimony contradicted', 'May use extrinsic evidence if not collateral', 'Collateral matters - no extrinsic evidence'],
            'exceptions': ['Bias always non-collateral', 'Conviction always non-collateral'],
            'policy_rationales': ['Show witness unreliable', 'Test credibility', 'Jury weighs evidence'],
            'common_traps': ['Using extrinsic evidence on collateral matters', 'Missing collateral matter rule', 'Confusing with prior inconsistent'],
            'teach': 'CONTRADICTION = Witness wrong about something? If not collateral, can prove up. If collateral, stuck with answer.',
            'question': 'Cross: "Didn\'t you wear blue shirt?" Witness: "No, red." Can call second witness to prove blue shirt?',
            'choices': {'A': 'Yes-contradiction', 'B': 'Yes-extrinsic', 'C': 'No-collateral', 'D': 'No-irrelevant'},
            'answer': 'C',
            'why': 'Shirt color = collateral matter (not relevant to case). Cannot use extrinsic evidence. Stuck with answer.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_impeachment_rehabilitation',
            'name': 'Rehabilitation of Witness',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'After credibility attacked, witness may be rehabilitated by prior consistent statement or character for truthfulness',
            'elements': ['Credibility must be attacked first', 'Prior consistent statement if charge of recent fabrication/improper motive', 'Character for truthfulness if character attacked'],
            'exceptions': ['Cannot bolster before attack', 'Prior consistent must predate motive to fabricate'],
            'policy_rationales': ['Fair response to attack', 'Prevent preemptive bolstering', 'Allow correction of false impressions'],
            'common_traps': ['Bolstering before attack', 'Using prior consistent without fabrication charge', 'Missing predate requirement'],
            'teach': 'REHABILITATION = Credibility attacked? Can rehabilitate with prior consistent (if motive charged) or character.',
            'question': 'Witness impeached by prior inconsistent statement. Can rehabilitate with character evidence?',
            'choices': {'A': 'Yes-impeached', 'B': 'Yes-rehabilitate', 'C': 'No-not character attack', 'D': 'Depends'},
            'answer': 'D',
            'why': 'Character for truthfulness only if character attacked. Prior inconsistent may not be character attack.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        },
        {
            'concept_id': 'evidence_impeachment_religious_beliefs',
            'name': 'Religious Beliefs Inadmissible for Credibility (610)',
            'subject': 'evidence',
            'difficulty': 2,
            'rule_statement': 'Cannot impeach or support credibility by evidence of religious beliefs or opinions',
            'elements': ['Religious beliefs', 'Cannot attack or support credibility', 'Absolute rule'],
            'exceptions': ['May show bias/interest if religion relevant to bias'],
            'policy_rationales': ['First Amendment', 'Religious freedom', 'Prevent prejudice'],
            'common_traps': ['Using religion to attack credibility', 'Confusing with bias exception', 'Thinking shows truthfulness'],
            'teach': 'RELIGIOUS BELIEFS = Cannot impeach or support credibility. Off limits under 610.',
            'question': 'Cross-examination: "You\'re an atheist, correct?" to attack credibility. Permissible?',
            'choices': {'A': 'Yes-credibility', 'B': 'Yes-relevant', 'C': 'No-610 bars', 'D': 'No-unless bias'},
            'answer': 'C',
            'why': 'FRE 610 prohibits using religious beliefs (or lack thereof) to attack credibility.',
            'source': 'expanded',
            'exam_frequency': 'low'
        }
    ]

    new_concepts.extend(impeachment_concepts)

    # ========== MISCELLANEOUS EVIDENCE (8 concepts) ==========

    misc_concepts = [
        {
            'concept_id': 'evidence_relevance_401',
            'name': 'Relevance Definition (FRE 401)',
            'subject': 'evidence',
            'difficulty': 2,
            'rule_statement': 'Evidence relevant if it has any tendency to make fact more or less probable',
            'elements': ['Tendency to make fact more/less probable', 'Fact of consequence', 'Very low threshold'],
            'policy_rationales': ['Broad standard', 'Let all probative evidence in', '403 screens prejudice'],
            'common_traps': ['Requiring high probative value', 'Confusing with 403', 'Thinking must prove fact'],
            'teach': 'RELEVANCE = ANY tendency to make fact more/less probable. Very low bar.',
            'question': 'Evidence makes fact 1% more probable. Relevant under 401?',
            'choices': {'A': 'Yes-any tendency', 'B': 'Yes-probative', 'C': 'No-too little', 'D': 'No-not significant'},
            'answer': 'A',
            'why': 'ANY tendency sufficient for relevance. Even 1% probability increase = relevant under 401.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_403_balancing',
            'name': 'Exclusion for Unfair Prejudice (FRE 403)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Court may exclude relevant evidence if probative value substantially outweighed by unfair prejudice',
            'elements': ['Evidence must be relevant', 'Unfair prejudice (not just damaging)', 'Substantially outweighs (high bar)', 'Confusion, waste of time also considered'],
            'policy_rationales': ['Balance probative vs. prejudicial', 'Ensure fair trial', 'Judicial efficiency'],
            'common_traps': ['Thinking "substantially" favors exclusion (it favors admission)', 'Confusing harmful with unfairly prejudicial', 'Missing discretionary nature'],
            'teach': 'FRE 403 = Probative value SUBSTANTIALLY outweighed by unfair prejudice? High bar to exclude.',
            'question': 'Gruesome photo relevant to injury. Prejudicial to defendant. Admissible?',
            'choices': {'A': 'Yes-unless substantially outweighed', 'B': 'Yes-relevant', 'C': 'No-prejudicial', 'D': 'No-gruesome'},
            'answer': 'A',
            'why': 'High bar for 403 exclusion. Probative value must be SUBSTANTIALLY outweighed. Damaging ≠ unfairly prejudicial.',
            'source': 'expanded',
            'exam_frequency': 'very high'
        },
        {
            'concept_id': 'evidence_authentication_901',
            'name': 'Authentication (FRE 901)',
            'subject': 'evidence',
            'difficulty': 3,
            'rule_statement': 'Evidence must be authenticated by showing it is what proponent claims',
            'elements': ['Proponent shows what claimed', 'Sufficient evidence for jury to find authentic', 'Low threshold'],
            'exceptions': ['Self-authenticating documents (902)', 'Stipulation'],
            'policy_rationales': ['Ensure genuine', 'Foundation requirement', 'Prevent fraud'],
            'common_traps': ['Requiring absolute proof', 'Missing low threshold', 'Confusing with best evidence rule'],
            'teach': 'AUTHENTICATION = Show it\'s what you claim. Low bar - enough for jury to find authentic.',
            'question': 'Letter claimed written by defendant. How authenticate?',
            'choices': {'A': 'Handwriting expert only', 'B': 'Defendant admission only', 'C': 'Any sufficient evidence', 'D': 'Original required'},
            'answer': 'C',
            'why': 'Authentication: any evidence sufficient to support finding it\'s what claimed. Multiple methods OK.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_best_evidence',
            'name': 'Best Evidence Rule (FRE 1002)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Original document required to prove contents of writing, recording, or photograph',
            'elements': ['Proving contents', 'Writing, recording, or photograph', 'Original or duplicate unless excuse'],
            'exceptions': ['Duplicate admissible unless genuine question', 'Excuses: lost, destroyed, in opponent possession', 'Not needed if not proving contents'],
            'policy_rationales': ['Prevent fraud', 'Ensure accuracy', 'Incentivize preservation'],
            'common_traps': ['Applying when not proving contents', 'Thinking always need original (duplicate OK)', 'Missing exceptions'],
            'teach': 'BEST EVIDENCE = Proving contents of document? Need original or duplicate (unless excused).',
            'question': 'Witness testifies to what he saw at event. Event was photographed. Need photo?',
            'choices': {'A': 'Yes-best evidence', 'B': 'Yes-photo exists', 'C': 'No-not proving contents', 'D': 'No-witness enough'},
            'answer': 'C',
            'why': 'Best evidence rule only applies when proving CONTENTS. Witness testifying to observation, not photo contents.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_subsequent_remedial',
            'name': 'Subsequent Remedial Measures (FRE 407)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Evidence of repairs/changes after event inadmissible to prove negligence/defect but admissible for other purposes',
            'elements': ['Subsequent to event', 'Remedial measure', 'Inadmissible for negligence/defect', 'Admissible for: ownership, control, feasibility, impeachment'],
            'policy_rationales': ['Encourage repairs', 'Don\'t punish safety improvements', 'Public policy'],
            'common_traps': ['Thinking always inadmissible', 'Missing other purposes exceptions', 'Applying to strict liability'],
            'teach': 'SUBSEQUENT REMEDIAL = Fixed it after? Can\'t prove negligence/defect. BUT can prove control, feasibility, impeach.',
            'question': 'After accident, defendant fixed stairs. Admissible to prove owned stairs?',
            'choices': {'A': 'Yes-ownership', 'B': 'Yes-relevant', 'C': 'No-subsequent remedial', 'D': 'No-407 bars'},
            'answer': 'A',
            'why': 'Subsequent remedial inadmissible for negligence/defect but admissible to prove ownership/control.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_settlement_negotiations',
            'name': 'Settlement Negotiations (FRE 408)',
            'subject': 'evidence',
            'difficulty': 3,
            'rule_statement': 'Settlement offers and negotiations inadmissible to prove/disprove validity or amount of claim',
            'elements': ['Claim disputed', 'Settlement offer or negotiation', 'Inadmissible for liability/amount', 'Admissible for bias, undue delay, obstruction'],
            'exceptions': ['Can use for other purposes (bias, etc.)', 'Statements to government agencies not protected', 'Criminal cases: statements not protected'],
            'policy_rationales': ['Encourage settlement', 'Promote compromise', 'Free discussion'],
            'common_traps': ['Thinking statements protected in criminal cases', 'Missing "disputed claim" requirement', 'Forgetting bias exception'],
            'teach': 'SETTLEMENT = Can\'t use offers to prove liability/amount. Encourage compromise. Criminal ≠ protected.',
            'question': 'Settlement offer in civil case. Admissible in later criminal case?',
            'choices': {'A': 'Yes-different case', 'B': 'Yes-not protected', 'C': 'No-408 bars', 'D': 'No-settlement'},
            'answer': 'B',
            'why': '408 protection only in case being compromised. Later criminal case = no protection.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_pleas',
            'name': 'Pleas and Plea Discussions (FRE 410)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Withdrawn guilty pleas, nolo contendere pleas, and plea discussions inadmissible',
            'elements': ['Withdrawn guilty plea', 'Nolo contendere plea', 'Statements during plea discussions', 'Inadmissible against defendant'],
            'exceptions': ['Defendant may use own plea statements', 'Perjury/false statement prosecution', 'Fairness exception'],
            'policy_rationales': ['Encourage plea negotiations', 'Protect defendants', 'Promote resolution'],
            'common_traps': ['Thinking accepted guilty plea protected (it\'s not)', 'Missing prosecutor must be involved', 'Forgetting exceptions'],
            'teach': 'PLEA DISCUSSIONS = Withdrawn pleas + nolo + plea talks = inadmissible. Encourage negotiation.',
            'question': 'Defendant withdrew guilty plea. Can prosecution use plea in trial?',
            'choices': {'A': 'Yes-admission', 'B': 'Yes-relevant', 'C': 'No-410 bars', 'D': 'No-withdrawn'},
            'answer': 'C',
            'why': 'FRE 410: withdrawn guilty pleas inadmissible. Encourage plea negotiations.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        },
        {
            'concept_id': 'evidence_liability_insurance',
            'name': 'Liability Insurance (FRE 411)',
            'subject': 'evidence',
            'difficulty': 3,
            'rule_statement': 'Evidence of liability insurance inadmissible to prove negligence or ability to pay but admissible for other purposes',
            'elements': ['Liability insurance', 'Inadmissible for negligence or ability to pay', 'Admissible for bias, ownership, control'],
            'policy_rationales': ['Encourage insurance', 'Prevent prejudice', 'Don\'t penalize responsible actors'],
            'common_traps': ['Thinking always inadmissible', 'Missing bias exception', 'Confusing with other policy exclusions'],
            'teach': 'LIABILITY INSURANCE = Can\'t prove negligence. BUT can prove bias, ownership, control.',
            'question': 'Witness works for defendant\'s insurer. Can cross-examine about employment to show bias?',
            'choices': {'A': 'Yes-bias', 'B': 'Yes-impeach', 'C': 'No-411 bars', 'D': 'No-insurance'},
            'answer': 'A',
            'why': 'Liability insurance inadmissible for negligence but admissible to show bias of witness.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        }
    ]

    new_concepts.extend(misc_concepts)

    return new_concepts


def main():
    """Complete Evidence expansion to 120 concepts"""

    print("\n" + "="*70)
    print("🔨 COMPLETING EVIDENCE EXPANSION TO 120 CONCEPTS")
    print("="*70 + "\n")

    # Load current knowledge base
    kb_file = Path(__file__).parent / 'data' / 'knowledge_849.json'
    with open(kb_file) as f:
        knowledge = json.load(f)

    current_evidence = knowledge['concepts']['evidence']
    print(f"Current Evidence concepts: {len(current_evidence)}")

    # Create final 27 concepts
    new_concepts = create_final_evidence_concepts()
    print(f"Generated new concepts: {len(new_concepts)}")

    # Add to evidence
    current_evidence.extend(new_concepts)
    total_evidence = len(current_evidence)

    print(f"Total Evidence concepts now: {total_evidence}")

    # Update metadata
    all_concepts_count = sum(len(concepts) for concepts in knowledge['concepts'].values())
    knowledge['metadata']['total_concepts'] = all_concepts_count

    # Save
    with open(kb_file, 'w') as f:
        json.dump(knowledge, f, indent=2)

    print(f"\n✅ Updated knowledge base: {all_concepts_count} total concepts")
    print(f"   Evidence: {total_evidence} concepts")
    print(f"\n🎉 TARGET REACHED: {total_evidence}/120 Evidence concepts!")

    print("\n" + "="*70)
    print("Part 2 concepts added:")
    print("  ✓ Privileges (7): Attorney-client, work product, spousal immunity,")
    print("    marital communications, psychotherapist, physician-patient, waiver")
    print("  ✓ Expert Testimony (6): Daubert, Frye, FRE 702-704, lay vs. expert")
    print("  ✓ Impeachment (6): Prior inconsistent, bias, sensory/mental,")
    print("    contradiction, rehabilitation, religious beliefs")
    print("  ✓ Miscellaneous (8): Relevance, 403 balancing, authentication,")
    print("    best evidence, subsequent remedial, settlement, pleas, insurance")
    print("="*70)

    print("\n📊 COMPLETE EVIDENCE BREAKDOWN (120 concepts):")
    print("   • Hearsay exceptions: 15 concepts")
    print("   • Character evidence: 8 concepts")
    print("   • Privileges: 7 concepts")
    print("   • Expert testimony: 6 concepts")
    print("   • Impeachment: 6 concepts")
    print("   • Miscellaneous: 8 concepts")
    print("   • Original base: 70 concepts")
    print("   TOTAL: 120 concepts\n")


if __name__ == '__main__':
    main()

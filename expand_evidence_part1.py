#!/usr/bin/env python3
"""
Evidence Subject Expansion: 70 → 120 Concepts
Adds 50 detailed Evidence concepts with full Socratic teaching content
Focus: Hearsay, Character Evidence, Privileges, Expert Testimony, Impeachment
"""

import json
from pathlib import Path

def create_expanded_evidence_concepts():
    """Create 50 new detailed Evidence concepts"""

    new_concepts = []

    # ========== HEARSAY EXCEPTIONS (15 concepts) ==========

    hearsay_concepts = [
        {
            'concept_id': 'evidence_hearsay_present_sense',
            'name': 'Present Sense Impression (803(1))',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Statement describing event made while declarant perceiving event or immediately thereafter',
            'elements': ['Describing event', 'While perceiving or immediately after', 'No time for fabrication'],
            'policy_rationales': ['No time to fabricate', 'Corroborated by event itself', 'Contemporaneous observation'],
            'common_traps': ['Confusing with excited utterance', 'Missing "immediately" requirement', 'Thinking any description qualifies'],
            'teach': 'PRESENT SENSE = Describing what you see RIGHT NOW. No time to lie.',
            'question': 'Witness testifies: "As car ran red light, passenger said \'That car just ran the light!\'" Hearsay exception?',
            'choices': {'A': 'Yes-present sense', 'B': 'Yes-excited utterance', 'C': 'No-hearsay', 'D': 'No-no exception'},
            'answer': 'A',
            'why': 'Statement describing event while/immediately after perceiving = present sense impression (803(1))',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_hearsay_excited_utterance',
            'name': 'Excited Utterance (803(2))',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Statement relating to startling event made while under stress of excitement caused by event',
            'elements': ['Startling event', 'Statement relates to event', 'Made while under stress of excitement'],
            'policy_rationales': ['Stress prevents fabrication', 'Spontaneous reaction', 'Trustworthy due to emotional state'],
            'common_traps': ['Requiring immediate statement (can be later if still excited)', 'Confusing with present sense', 'Missing startling event requirement'],
            'teach': 'EXCITED UTTERANCE = Startling event + still excited when speaking. Adrenaline = no lying.',
            'question': '2 hours after accident, victim (still shaking/crying) says "He ran the light!" Exception?',
            'choices': {'A': 'Yes-still excited', 'B': 'Yes-present sense', 'C': 'No-too late', 'D': 'No-not startling'},
            'answer': 'A',
            'why': 'Time doesn\'t matter if still under stress of excitement. Still shaking = still excited.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_hearsay_state_of_mind',
            'name': 'State of Mind Exception (803(3))',
            'subject': 'evidence',
            'difficulty': 5,
            'rule_statement': 'Statement of declarant\'s then-existing mental/emotional/physical condition',
            'elements': ['Then-existing condition', 'Not memory/belief about past', 'Declarant\'s own state'],
            'exceptions': ['Cannot prove fact remembered/believed (Hillmon doctrine limits)'],
            'policy_rationales': ['People know their own mental state', 'Hard to fake emotions', 'Necessity'],
            'common_traps': ['Using past statements about mental state', 'Thinking it proves past acts', 'Missing "then-existing" requirement'],
            'teach': 'STATE OF MIND = "I feel X right now" OK. "I felt X yesterday" NOT OK.',
            'question': 'Will contest. Statement "I intend to leave all to charity" admissible for intent?',
            'choices': {'A': 'Yes-then-existing intent', 'B': 'Yes-state of mind', 'C': 'No-hearsay', 'D': 'No-past belief'},
            'answer': 'A',
            'why': 'Then-existing intent admissible under 803(3). Intent to do future act = state of mind.',
            'source': 'expanded',
            'exam_frequency': 'very high'
        },
        {
            'concept_id': 'evidence_hearsay_medical_diagnosis',
            'name': 'Statements for Medical Diagnosis (803(4))',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Statements made for medical diagnosis/treatment describing symptoms, cause, or source',
            'elements': ['Made for medical diagnosis/treatment', 'Reasonably pertinent to diagnosis/treatment', 'Declarant believes for treatment'],
            'policy_rationales': ['People don\'t lie to their doctors', 'Necessity for treatment', 'Reliable motivation'],
            'common_traps': ['Including fault statements (inadmissible)', 'Missing treatment purpose', 'Thinking any statement to doctor qualifies'],
            'teach': 'MEDICAL STATEMENTS = To get treated right, you tell truth. But NOT fault/blame.',
            'question': 'Patient tells doctor: "My husband hit me." Admissible for medical diagnosis?',
            'choices': {'A': 'Yes-all statements', 'B': 'Yes-if pertinent', 'C': 'No-fault', 'D': 'No-hearsay'},
            'answer': 'B',
            'why': 'Source of injury pertinent to diagnosis/treatment. "Who" matters for domestic violence treatment.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_hearsay_business_records',
            'name': 'Business Records Exception (803(6))',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Record of regularly conducted activity, made at/near time by person with knowledge, kept in regular course',
            'elements': ['Record of act/event/condition', 'Made at/near time', 'By person with knowledge', 'Regular business practice', 'Foundation testimony'],
            'exceptions': ['Opponent can show untrustworthiness', 'Prepared for litigation may be excluded'],
            'policy_rationales': ['Business relies on accuracy', 'Regular practice ensures reliability', 'Necessity'],
            'common_traps': ['Missing foundation witness', 'Including opinions beyond business scope', 'Forgetting litigation exclusion'],
            'teach': 'BUSINESS RECORDS = Regular + routine + reliable. Need foundation witness.',
            'question': 'Hospital record of patient vitals. Nurse who recorded it unavailable. Admissible?',
            'choices': {'A': 'Yes-business record', 'B': 'Yes-if foundation', 'C': 'No-hearsay', 'D': 'No-nurse unavailable'},
            'answer': 'B',
            'why': 'Business record if foundation laid (custodian can testify about regular practice). Recorder need not testify.',
            'source': 'expanded',
            'exam_frequency': 'very high'
        },
        {
            'concept_id': 'evidence_hearsay_public_records',
            'name': 'Public Records Exception (803(8))',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Public office record of activities, matters observed if duty to report, or factual findings',
            'elements': ['Public office record', 'Activities OR observations OR factual findings', 'If observations: duty to report'],
            'exceptions': ['Police reports in criminal cases against defendant', 'Untrustworthy records excluded'],
            'policy_rationales': ['Public officials presumed reliable', 'Duty to report accurately', 'Necessity'],
            'common_traps': ['Using police reports against criminal defendant', 'Missing duty to report', 'Confusing with business records'],
            'teach': 'PUBLIC RECORDS = Government records reliable. BUT not police reports vs. criminal defendant.',
            'question': 'Prosecutor offers police report in criminal case. Admissible as public record?',
            'choices': {'A': 'Yes-public record', 'B': 'Yes-reliable', 'C': 'No-803(8) bars', 'D': 'No-hearsay'},
            'answer': 'C',
            'why': '803(8) specifically excludes law enforcement observations in criminal cases against defendant.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_hearsay_former_testimony',
            'name': 'Former Testimony (804(b)(1))',
            'subject': 'evidence',
            'difficulty': 5,
            'rule_statement': 'Prior testimony given as witness, declarant unavailable, party had opportunity to cross-examine',
            'elements': ['Declarant unavailable (804(a))', 'Given as witness under oath', 'Prior proceeding', 'Party had opportunity/similar motive to cross-examine'],
            'policy_rationales': ['Oath ensures truthfulness', 'Cross-examination tested credibility', 'Necessity due to unavailability'],
            'common_traps': ['Missing unavailability requirement', 'Different party (need privity)', 'Missing similar motive to develop'],
            'teach': 'FORMER TESTIMONY = Previous sworn testimony + similar motive to cross. Need unavailability.',
            'question': 'Witness testified at preliminary hearing. Now unavailable. Admissible in trial?',
            'choices': {'A': 'Yes-if similar motive', 'B': 'Yes-prior testimony', 'C': 'No-different proceeding', 'D': 'No-hearsay'},
            'answer': 'A',
            'why': 'Former testimony admissible if party (or predecessor) had similar motive to develop testimony.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        },
        {
            'concept_id': 'evidence_hearsay_dying_declaration',
            'name': 'Dying Declaration (804(b)(2))',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Statement under belief of imminent death concerning cause/circumstances of death',
            'elements': ['Declarant unavailable', 'Belief death imminent', 'Concerning cause/circumstances of death', 'Homicide case OR civil case'],
            'exceptions': ['Criminal cases: only homicide', 'Declarant need not actually die'],
            'policy_rationales': ['No one lies on deathbed', 'Person about to meet Maker tells truth', 'Necessity'],
            'common_traps': ['Thinking declarant must die', 'Using in non-homicide criminal cases', 'Missing imminent death belief'],
            'teach': 'DYING DECLARATION = "I\'m about to die, here\'s who killed me." Homicide or civil only.',
            'question': 'Shooting victim believes he\'s dying, says "Joe shot me." Survives. Admissible in Joe\'s assault trial?',
            'choices': {'A': 'Yes-dying declaration', 'B': 'Yes-excited utterance', 'C': 'No-not homicide', 'D': 'No-survived'},
            'answer': 'C',
            'why': 'Dying declaration only admissible in homicide prosecutions (or civil). Assault = not homicide.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_hearsay_statement_against_interest',
            'name': 'Statement Against Interest (804(b)(3))',
            'subject': 'evidence',
            'difficulty': 5,
            'rule_statement': 'Statement against declarant\'s interest when made, declarant unavailable, reasonable person would not have made unless true',
            'elements': ['Declarant unavailable', 'Against interest when made (pecuniary/proprietary/penal)', 'Reasonable person wouldn\'t say unless true'],
            'exceptions': ['Statement exposing declarant to criminal liability needs corroboration'],
            'policy_rationales': ['People don\'t say things against their interest unless true', 'Reliability from self-damaging nature'],
            'common_traps': ['Confusing with party admission (no unavailability needed for admission)', 'Missing "when made" timing', 'Forgetting corroboration for criminal'],
            'teach': 'AGAINST INTEREST = "This hurts me, but it\'s true." Need unavailability (unlike party admission).',
            'question': 'Unavailable declarant said "I robbed the bank, not defendant." Admissible for defendant?',
            'choices': {'A': 'Yes-if corroborated', 'B': 'Yes-against interest', 'C': 'No-hearsay', 'D': 'No-self-serving'},
            'answer': 'A',
            'why': 'Statement exposing declarant to criminal liability admissible if corroborating circumstances show trustworthiness.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_hearsay_forfeiture',
            'name': 'Forfeiture by Wrongdoing (804(b)(6))',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Party forfeits hearsay objection if wrongfully caused declarant\'s unavailability to prevent testimony',
            'elements': ['Declarant unavailable', 'Party\'s wrongdoing caused unavailability', 'Intent to prevent testimony'],
            'policy_rationales': ['Prevent party from benefiting from wrongdoing', 'Equity principle', 'Ensure justice'],
            'common_traps': ['Missing intent requirement', 'Thinking any unavailability works', 'Not recognizing as exception'],
            'teach': 'FORFEITURE = You killed witness to shut them up? You lose hearsay objection.',
            'question': 'Defendant murders witness to prevent testimony. Witness\'s prior statements admissible?',
            'choices': {'A': 'Yes-forfeiture', 'B': 'Yes-dying declaration', 'C': 'No-hearsay', 'D': 'No-still need exception'},
            'answer': 'A',
            'why': 'Forfeiture by wrongdoing: party loses hearsay objection by wrongfully causing unavailability.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        },
        {
            'concept_id': 'evidence_hearsay_residual',
            'name': 'Residual Exception (807)',
            'subject': 'evidence',
            'difficulty': 5,
            'rule_statement': 'Hearsay with equivalent guarantees of trustworthiness, material to issue, best available evidence, notice given',
            'elements': ['Equivalent trustworthiness guarantees', 'More probative than other evidence', 'Justice best served', 'Notice to adverse party'],
            'policy_rationales': ['Catchall for reliable hearsay', 'Flexibility for unforeseen situations', 'Justice over technicality'],
            'common_traps': ['Using as first resort (it\'s last resort)', 'Missing notice requirement', 'Not showing equivalent trustworthiness'],
            'teach': 'RESIDUAL = Catchall for reliable hearsay not fitting other exceptions. Last resort only.',
            'question': 'Reliable hearsay not fitting 803/804. Can use residual exception without notice?',
            'choices': {'A': 'Yes-if reliable', 'B': 'Yes-catchall', 'C': 'No-need notice', 'D': 'No-never'},
            'answer': 'C',
            'why': 'Residual exception requires pretrial notice to adverse party (or showing good cause for non-notice).',
            'source': 'expanded',
            'exam_frequency': 'low'
        },
        {
            'concept_id': 'evidence_hearsay_party_admission',
            'name': 'Party Admission (801(d)(2))',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Statement by party-opponent offered against that party (not hearsay by definition)',
            'elements': ['Statement by party', 'Offered against that party', 'No unavailability required'],
            'exceptions': ['Not hearsay, so no need for unavailability'],
            'policy_rationales': ['Party cannot complain about own statement', 'Adversarial system allows use against party'],
            'common_traps': ['Thinking it\'s an exception (it\'s not hearsay)', 'Confusing with statement against interest', 'Missing no unavailability needed'],
            'teach': 'PARTY ADMISSION = NOT hearsay. Your own words used against you. No unavailability needed.',
            'question': 'Plaintiff offers defendant\'s prior statement against defendant. Hearsay exception needed?',
            'choices': {'A': 'Yes-admission exception', 'B': 'Yes-against interest', 'C': 'No-not hearsay', 'D': 'No-unavailable'},
            'answer': 'C',
            'why': 'Party admission is NOT hearsay by definition under 801(d)(2). No exception needed.',
            'source': 'expanded',
            'exam_frequency': 'very high'
        },
        {
            'concept_id': 'evidence_hearsay_coconspirator',
            'name': 'Co-Conspirator Statement (801(d)(2)(E))',
            'subject': 'evidence',
            'difficulty': 5,
            'rule_statement': 'Statement by co-conspirator during and in furtherance of conspiracy',
            'elements': ['Statement by co-conspirator', 'During conspiracy', 'In furtherance of conspiracy', 'Party was member'],
            'policy_rationales': ['Conspirators act as agents', 'Statements part of criminal enterprise', 'Necessity in conspiracy cases'],
            'common_traps': ['Using statements after conspiracy ends', 'Casual conversations not "in furtherance"', 'Missing temporal requirement'],
            'teach': 'CO-CONSPIRATOR = During + in furtherance of conspiracy. NOT casual chit-chat.',
            'question': 'After arrest, co-conspirator says "We robbed the bank." Admissible against defendant?',
            'choices': {'A': 'Yes-co-conspirator', 'B': 'Yes-admission', 'C': 'No-after arrest', 'D': 'No-hearsay'},
            'answer': 'C',
            'why': 'After arrest = conspiracy ended. Must be during conspiracy and in furtherance.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_hearsay_ancient_documents',
            'name': 'Ancient Documents (803(16))',
            'subject': 'evidence',
            'difficulty': 3,
            'rule_statement': 'Statement in document 20+ years old, authentic, in place expected if authentic',
            'elements': ['Document 20+ years old', 'Authentic on face', 'Found in place expected'],
            'policy_rationales': ['Old documents presumed reliable', 'Difficulty getting witnesses after 20 years', 'Practical necessity'],
            'common_traps': ['Thinking any old document qualifies', 'Missing authentication requirement', 'Not checking age'],
            'teach': 'ANCIENT DOCUMENTS = 20+ years old + looks real + found right place = reliable.',
            'question': '25-year-old deed found in courthouse records. Admissible without foundation?',
            'choices': {'A': 'Yes-ancient document', 'B': 'Yes-public record', 'C': 'No-need witness', 'D': 'No-hearsay'},
            'answer': 'A',
            'why': '20+ years old, authentic on face, proper place = ancient document exception.',
            'source': 'expanded',
            'exam_frequency': 'low'
        },
        {
            'concept_id': 'evidence_hearsay_refreshing_recollection',
            'name': 'Refreshing Recollection vs. Recorded Recollection',
            'subject': 'evidence',
            'difficulty': 5,
            'rule_statement': 'Refreshing: witness uses anything to jog memory. Recorded recollection: 803(5) exception for past recording',
            'elements': ['Refreshing: witness testifies from refreshed memory', 'Recorded: document admitted when witness still can\'t remember'],
            'exceptions': ['Refreshing: document not admitted, just used', 'Recorded: requires foundation (made when fresh, accurate, now can\'t remember)'],
            'policy_rationales': ['Allow witnesses to testify accurately', 'Recognize memory limitations', 'Preserve accurate contemporaneous records'],
            'common_traps': ['Confusing the two concepts', 'Thinking refreshing document comes in as evidence', 'Missing foundation for recorded recollection'],
            'teach': 'REFRESHING = Jog memory, doc stays out. RECORDED RECOLLECTION = Can\'t remember even after, doc comes in (803(5)).',
            'question': 'Witness looks at notes, now remembers. Notes admissible as evidence?',
            'choices': {'A': 'Yes-recorded recollection', 'B': 'Yes-refreshing', 'C': 'No-just refreshing', 'D': 'No-hearsay'},
            'answer': 'C',
            'why': 'Refreshing recollection: witness testifies from memory, document not admitted.',
            'source': 'expanded',
            'exam_frequency': 'high'
        }
    ]

    new_concepts.extend(hearsay_concepts)

    # ========== CHARACTER EVIDENCE (8 concepts) ==========

    character_concepts = [
        {
            'concept_id': 'evidence_character_defendant_criminal',
            'name': 'Character Evidence - Criminal Defendant',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Defendant may offer evidence of pertinent good character trait; prosecution may rebut',
            'elements': ['Defendant opens door', 'Pertinent trait only', 'Reputation or opinion testimony', 'Prosecution may rebut'],
            'policy_rationales': ['Defendant needs protection', 'Relevant to propensity', 'Fair rebuttal for prosecution'],
            'common_traps': ['Thinking prosecution can start with character', 'Missing pertinent trait requirement', 'Allowing specific acts on direct'],
            'teach': 'DEFENDANT CHARACTER = Defendant opens door with good character. Prosecution can rebut. Reputation/opinion only.',
            'question': 'Can prosecution start case by proving defendant\'s bad character for violence?',
            'choices': {'A': 'Yes-propensity', 'B': 'Yes-relevant', 'C': 'No-defendant opens door', 'D': 'No-never allowed'},
            'answer': 'C',
            'why': 'Prosecution cannot initiate character evidence. Defendant must open door first (404(a)(2)(A)).',
            'source': 'expanded',
            'exam_frequency': 'very high'
        },
        {
            'concept_id': 'evidence_character_victim_criminal',
            'name': 'Character Evidence - Victim in Criminal Case',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Defendant may offer victim\'s pertinent character; prosecution may rebut and offer defendant\'s same trait',
            'elements': ['Defendant may offer victim character', 'Pertinent trait', 'Prosecution rebounds with defendant\'s same trait', 'Homicide: victim\'s peacefulness'],
            'policy_rationales': ['Self-defense claims need victim aggression evidence', 'Fair rebuttal for prosecution', 'Protect victims'],
            'common_traps': ['Missing "same trait" requirement for prosecution rebuttal', 'Forgetting homicide special rule', 'Allowing any trait'],
            'teach': 'VICTIM CHARACTER = Defense offers victim aggression → Prosecution offers defendant aggression (same trait).',
            'question': 'Self-defense case. Defense offers victim\'s violent character. Prosecution can offer defendant\'s what?',
            'choices': {'A': 'Any bad character', 'B': 'Violent character', 'C': 'Nothing', 'D': 'Dishonesty'},
            'answer': 'B',
            'why': 'Prosecution may rebut with defendant\'s character for SAME TRAIT (violence here).',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_character_404b',
            'name': 'Prior Bad Acts (404(b))',
            'subject': 'evidence',
            'difficulty': 5,
            'rule_statement': 'Evidence of other crimes/wrongs inadmissible to prove propensity but admissible for MIMIC purposes',
            'elements': ['Not for propensity/character', 'MIMIC: Motive, Intent, Mistake (absence), Identity, Common plan'],
            'exceptions': ['Sexual assault/child molestation cases (414-415)', 'Notice requirement in criminal cases'],
            'policy_rationales': ['Propensity reasoning unfairly prejudicial', 'But other purposes probative', 'Balance probative vs. prejudicial'],
            'common_traps': ['Thinking prior acts always inadmissible', 'Missing MIMIC exceptions', 'Forgetting notice requirement'],
            'teach': 'PRIOR BAD ACTS = NO for propensity. YES for MIMIC (Motive Intent Mistake Identity Common plan).',
            'question': 'Prosecution offers defendant\'s prior robbery to show he\'s a robber in current robbery case. Admissible?',
            'choices': {'A': 'Yes-relevant', 'B': 'Yes-MIMIC', 'C': 'No-propensity', 'D': 'No-prejudicial'},
            'answer': 'C',
            'why': 'To show "he\'s a robber" = propensity use. Inadmissible under 404(b).',
            'source': 'expanded',
            'exam_frequency': 'very high'
        },
        {
            'concept_id': 'evidence_character_methods',
            'name': 'Methods of Proving Character (405)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Character proved by reputation/opinion; specific acts allowed on cross or if character is essential element',
            'elements': ['Reputation or opinion testimony', 'Specific acts on cross-examination only', 'Specific acts if essential element of claim'],
            'policy_rationales': ['Reputation/opinion less prejudicial', 'Specific acts too time-consuming', 'Cross needs testing grounds'],
            'common_traps': ['Allowing specific acts on direct (except essential element)', 'Confusing methods', 'Missing good faith basis for cross'],
            'teach': 'CHARACTER METHODS = Reputation/opinion on direct. Specific acts ONLY on cross (or if essential element).',
            'question': 'Direct examination of character witness. Can ask about specific good acts?',
            'choices': {'A': 'Yes-if probative', 'B': 'Yes-specific acts', 'C': 'No-reputation/opinion only', 'D': 'No-cross only'},
            'answer': 'C',
            'why': 'Direct examination: reputation or opinion only. Specific acts allowed only on cross.',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_character_habit',
            'name': 'Habit Evidence (406)',
            'subject': 'evidence',
            'difficulty': 3,
            'rule_statement': 'Evidence of habit or routine practice admissible to prove conformity',
            'elements': ['Habit = specific response to repeated situation', 'Frequency and particularity', 'Admissible without corroboration'],
            'policy_rationales': ['Habits more reliable than character', 'Specific and regular', 'Probative value high'],
            'common_traps': ['Confusing habit with character', 'Not enough frequency', 'Thinking corroboration needed'],
            'teach': 'HABIT = Specific + regular + automatic. "Always do X in situation Y." Admissible to prove conduct.',
            'question': '"Plaintiff always stops at that stop sign" - admissible to show stopped on day in question?',
            'choices': {'A': 'Yes-habit', 'B': 'Yes-character', 'C': 'No-propensity', 'D': 'No-specific'},
            'answer': 'A',
            'why': 'Specific regular behavior (always stops at same sign) = habit. Admissible under 406.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        },
        {
            'concept_id': 'evidence_character_truthfulness_608',
            'name': 'Character for Truthfulness (608)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'Witness credibility may be attacked/supported by testimony about character for truthfulness',
            'elements': ['Reputation or opinion about truthfulness', 'Only after credibility attacked for support', 'Specific acts on cross with good faith basis'],
            'policy_rationales': ['Assess witness credibility', 'Reputation for lying matters', 'Limit to truthfulness trait'],
            'common_traps': ['Bolstering before attack', 'Using specific acts on direct', 'Missing good faith basis requirement'],
            'teach': 'TRUTHFULNESS = Attack credibility anytime. Support ONLY after attack. Reputation/opinion; specific acts on cross only.',
            'question': 'Can plaintiff support own witness\'s truthfulness before any attack?',
            'choices': {'A': 'Yes-always', 'B': 'Yes-if relevant', 'C': 'No-only after attack', 'D': 'No-never'},
            'answer': 'C',
            'why': 'Cannot bolster witness credibility before credibility attacked (608(a)).',
            'source': 'expanded',
            'exam_frequency': 'high'
        },
        {
            'concept_id': 'evidence_character_conviction_609',
            'name': 'Impeachment by Conviction (609)',
            'subject': 'evidence',
            'difficulty': 5,
            'rule_statement': 'Prior conviction admissible for impeachment if crime of dishonesty OR felony passing 403 balance',
            'elements': ['Crime of dishonesty: automatically admissible', 'Felony: balance probative vs. prejudicial (403)', 'Criminal defendant: reverse 403', '10-year limit unless probative value substantially outweighs prejudice'],
            'exceptions': ['Pardon based on innocence', 'Juvenile convictions (limited)', 'Appeals pending (may use)'],
            'policy_rationales': ['Criminals less credible', 'Dishonesty crimes directly relevant', 'Balance prejudice to defendants'],
            'common_traps': ['Auto-admitting all felonies', 'Missing 10-year rule', 'Wrong 403 balance for criminal defendant'],
            'teach': 'CONVICTION IMPEACHMENT = Dishonesty crimes always. Felonies if pass 403 (reverse for crim defendant). 10-year limit.',
            'question': 'Criminal defendant testifies. 12-year-old felony conviction. Admissible to impeach?',
            'choices': {'A': 'Yes-felony', 'B': 'Yes-if probative', 'C': 'No-10 year limit', 'D': 'No-unless outweighs'},
            'answer': 'D',
            'why': 'Convictions 10+ years old admissible ONLY if probative value substantially outweighs prejudice.',
            'source': 'expanded',
            'exam_frequency': 'very high'
        },
        {
            'concept_id': 'evidence_character_sexual_assault',
            'name': 'Character Evidence in Sexual Assault Cases (413-415)',
            'subject': 'evidence',
            'difficulty': 4,
            'rule_statement': 'In sexual assault/child molestation cases, defendant\'s prior similar acts admissible for any purpose including propensity',
            'elements': ['Sexual assault or child molestation case', 'Prior offense of similar nature', 'Admissible for propensity', 'Notice requirement'],
            'exceptions': ['Special rules only for sexual offenses', 'Still subject to 403 balancing'],
            'policy_rationales': ['Pattern of sexual offenses highly probative', 'Protect victims', 'Recidivism rates high'],
            'common_traps': ['Applying to non-sexual crimes', 'Missing notice requirement', 'Forgetting still need 403 balance'],
            'teach': 'SEXUAL ASSAULT = Special rule. Prior similar acts admissible for propensity. Exception to general 404(b) rule.',
            'question': 'Rape prosecution. Evidence of defendant\'s prior rape 5 years ago. Admissible for propensity?',
            'choices': {'A': 'Yes-413', 'B': 'Yes-MIMIC', 'C': 'No-404(b)', 'D': 'No-too old'},
            'answer': 'A',
            'why': 'Rule 413: prior sexual assault admissible for any purpose including propensity in sexual assault cases.',
            'source': 'expanded',
            'exam_frequency': 'medium'
        }
    ]

    new_concepts.extend(character_concepts)

    return new_concepts


def main():
    """Add new Evidence concepts to knowledge base"""

    print("\n" + "="*70)
    print("🔨 EXPANDING EVIDENCE: 70 → 120 CONCEPTS")
    print("="*70 + "\n")

    # Load current knowledge base
    kb_file = Path(__file__).parent / 'data' / 'knowledge_849.json'
    with open(kb_file) as f:
        knowledge = json.load(f)

    current_evidence = knowledge['concepts']['evidence']
    print(f"Current Evidence concepts: {len(current_evidence)}")

    # Create new concepts (first batch: 23 hearsay + character concepts)
    new_concepts = create_expanded_evidence_concepts()
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
    print(f"\n📊 Progress: {total_evidence}/120 Evidence concepts")
    print(f"   Remaining: {120 - total_evidence} concepts needed\n")

    print("="*70)
    print("Concepts added:")
    print("  ✓ Hearsay exceptions (15): Present sense, excited utterance, state of mind, medical,")
    print("    business records, public records, former testimony, dying declaration,")
    print("    against interest, forfeiture, residual, party admission, co-conspirator,")
    print("    ancient documents, refreshing/recorded recollection")
    print("  ✓ Character evidence (8): Defendant, victim, 404(b), methods, habit,")
    print("    truthfulness (608), conviction (609), sexual assault (413-415)")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()

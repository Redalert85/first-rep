"""Interactive Bar Prep Tutor with adaptive session summary and rule refreshers.

This lightweight tutor is intended as an approachable on-ramp to the
more advanced study systems that live elsewhere in the repository. It
now includes:

* Subject filtering so learners can focus on weak areas
* Confidence tracking for each prompt
* Rich session analytics with subject-level breakdowns and review cues
* Structured representation of questions (MCQ + essay)
* Optional rule refreshers that surface core black-letter concepts per subject

The script remains terminal-friendly and does not require network
access or API keys, making it ideal for quick study bursts.
"""

from __future__ import annotations

import random
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field
from statistics import mean
from typing import Dict, Iterable, List, Optional, Sequence


# ---------------------------------------------------------------------------
# Data model


@dataclass
class Question:
    """Representation of a study prompt."""

    id: str
    subject: str
    type: str  # "mcq" or "essay"
    prompt: str
    explanation: str
    choices: List[str] = field(default_factory=list)
    answer: Optional[int] = None
    grading_keywords: List[str] = field(default_factory=list)

    @property
    def is_mcq(self) -> bool:
        return self.type == "mcq"

    @property
    def is_essay(self) -> bool:
        return self.type == "essay"


# Raw question database.  This intentionally stays small so that the
# interactive experience is quick, but the structure mirrors the larger
# knowledge bases in the project.
_QUESTIONS_RAW: Sequence[Dict] = [
    {
        "subject": "Contracts",
        "type": "mcq",
        "prompt": "A offers to sell his car to B for $5,000. B accepts. What is the legal status of their agreement?",
        "choices": [
            "A valid contract exists.",
            "No contract exists because there is no consideration.",
            "No contract exists because the price is too low.",
            "No contract exists because the parties did not sign anything.",
        ],
        "answer": 0,
        "explanation": "A valid contract exists because there was an offer, acceptance, and consideration (the price).",
    },
    {
        "subject": "Torts",
        "type": "mcq",
        "prompt": "Which of the following is a defense to battery?",
        "choices": ["Consent", "Negligence", "Duress", "Strict liability"],
        "answer": 0,
        "explanation": "Consent is a classic defense to intentional torts like battery. It negates the wrongful touching element.",
    },
    {
        "subject": "Criminal Law",
        "type": "essay",
        "prompt": "Discuss whether a defendant who accidentally kills someone during a lawful act is guilty of homicide.",
        "grading_keywords": [
            "mens rea",
            "actus reus",
            "lawful act",
            "criminal negligence",
            "involuntary manslaughter",
        ],
        "explanation": textwrap.dedent(
            """
            For homicide, the prosecution must prove that the defendant caused the death of another human being. Mens rea
            (criminal intent) is required for most homicides. If the killing was truly accidental during a lawful act and not
            due to criminal negligence, the defendant may not be guilty of homicide. However, if their actions were reckless
            or grossly negligent, they could be guilty of involuntary manslaughter.
            """
        ).strip(),
    },
    {
        "subject": "Constitutional Law",
        "type": "mcq",
        "prompt": "Which amendment protects against unreasonable searches and seizures?",
        "choices": ["First Amendment", "Fourth Amendment", "Fifth Amendment", "Eighth Amendment"],
        "answer": 1,
        "explanation": "The Fourth Amendment protects against unreasonable searches and seizures.",
    },
    {
        "subject": "Property",
        "type": "mcq",
        "prompt": "Which of the following is a future interest?",
        "choices": ["Life estate", "Fee simple absolute", "Remainder", "Tenancy in common"],
        "answer": 2,
        "explanation": "A remainder is a future interest that becomes possessory upon the natural termination of the prior estate.",
    },
    {
        "subject": "Evidence",
        "type": "essay",
        "prompt": "Explain the hearsay rule and its exceptions.",
        "grading_keywords": [
            "hearsay",
            "out of court statement",
            "truth of the matter",
            "exceptions",
            "declarant",
            "admissible",
        ],
        "explanation": textwrap.dedent(
            """
            Hearsay is an out-of-court statement offered to prove the truth of the matter asserted. Hearsay is generally
            inadmissible unless it falls within an exception (e.g., present sense impression, excited utterance, business
            records). The rationale is that such statements are unreliable unless certain conditions are met.
            """
        ).strip(),
    },
    {
        "subject": "Civil Procedure",
        "type": "mcq",
        "prompt": "Which of the following motions can dispose of a case before trial?",
        "choices": [
            "Motion to dismiss",
            "Motion for summary judgment",
            "Motion to compel discovery",
            "Motion for directed verdict",
        ],
        "answer": 1,
        "explanation": "A motion for summary judgment can dispose of a case before trial if there is no genuine issue of material fact.",
    },
    {
        "subject": "Evidence",
        "type": "mcq",
        "prompt": "For character evidence in a criminal trial, when may the prosecution offer evidence of the defendant's character?",
        "choices": [
            "In its case-in-chief whenever relevant",
            "Only after the defendant opens the door",
            "Only during cross-examination of the defendant",
            "Never; character evidence is always inadmissible",
        ],
        "answer": 1,
        "explanation": "The prosecution may generally rebut the defendant's character evidence but cannot initiate it in the case-in-chief.",
    },
    {
        "subject": "Criminal Procedure",
        "type": "mcq",
        "prompt": "When must police administer Miranda warnings during a custodial interrogation?",
        "choices": [
            "Whenever the suspect is questioned, regardless of custody",
            "Only when the suspect is in custody and subject to interrogation",
            "Only for felony investigations",
            "Only if the suspect specifically requests an attorney",
        ],
        "answer": 1,
        "explanation": "Miranda warnings are required when a suspect is both in custody and subject to interrogation by law enforcement.",
    },
    {
        "subject": "Contracts",
        "type": "essay",
        "prompt": "A written contract contains a clause stating it is the final agreement. The buyer later seeks to introduce prior oral negotiations to add a term. Discuss the admissibility of the oral evidence.",
        "grading_keywords": [
            "parol evidence rule",
            "integration",
            "partial integration",
            "exceptions",
            "ambiguity",
        ],
        "explanation": textwrap.dedent(
            """
            The parol evidence rule bars evidence of prior or contemporaneous agreements that contradict a fully integrated
            writing. If the contract is fully integrated, additional terms are excluded unless an exception applies (e.g.,
            ambiguity, fraud). For a partially integrated agreement, consistent additional terms may be admissible. The
            integration clause suggests a total integration, but courts examine intent and context.
            """
        ).strip(),
    },
    {
        "subject": "Real Property",
        "type": "mcq",
        "prompt": "Which of the following is NOT a required element for adverse possession?",
        "choices": [
            "Open and notorious",
            "Exclusive",
            "Good faith belief of ownership",
            "Continuous for the statutory period",
        ],
        "answer": 2,
        "explanation": "Most jurisdictions do not require a good faith belief; some even require hostility, which can include knowing trespass.",
    },
    {
        "subject": "Torts",
        "type": "essay",
        "prompt": "Analyze whether a store owner is liable when a patron slips on a freshly mopped floor that lacked warning signs.",
        "grading_keywords": [
            "duty",
            "breach",
            "invitee",
            "reasonable care",
            "comparative negligence",
            "notice",
        ],
        "explanation": textwrap.dedent(
            """
            Business owners owe invitees a duty of reasonable care to maintain safe premises. Leaving a wet floor without
            signage can constitute breach if the danger was foreseeable and easily preventable. Liability depends on causation
            and defenses such as comparative negligence if the patron disregarded obvious warnings.
            """
        ).strip(),
    },
    {
        "subject": "Remedies",
        "type": "mcq",
        "prompt": "Specific performance is most appropriate when:",
        "choices": [
            "The contract involves fungible goods",
            "Money damages are adequate",
            "The subject matter is unique and enforceable",
            "The plaintiff has unclean hands",
        ],
        "answer": 2,
        "explanation": "Specific performance is an equitable remedy used when money damages are inadequate, typically for unique items like real property.",
    },
    {
        "subject": "Professional Responsibility",
        "type": "mcq",
        "prompt": "A lawyer learns a current client intends to commit substantial financial fraud. What is the lawyer's best ethical course?",
        "choices": [
            "Immediately inform authorities regardless of client wishes",
            "Do nothing because of confidentiality",
            "Counsel the client to refrain and, if necessary, withdraw, revealing only to the extent permitted to prevent the crime",
            "Disclose the information to opposing counsel",
        ],
        "answer": 2,
        "explanation": "Model Rule 1.6 permits disclosure to prevent certain financial crimes, but the lawyer should first counsel the client and withdraw if the client persists.",
    },
    {
        "subject": "Civil Procedure",
        "type": "essay",
        "prompt": "Discuss personal jurisdiction over an out-of-state manufacturer whose products are sold in the forum through an online marketplace.",
        "grading_keywords": [
            "personal jurisdiction",
            "minimum contacts",
            "purposeful availment",
            "specific jurisdiction",
            "stream of commerce",
            "fair play and substantial justice",
        ],
        "explanation": textwrap.dedent(
            """
            Personal jurisdiction requires minimum contacts such that maintenance of the suit does not offend traditional
            notions of fair play and substantial justice. Courts analyze whether the defendant purposefully availed itself of
            the forum, including targeted sales or marketing. Mere placement into the stream of commerce may be insufficient
            without additional conduct directed at the forum.
            """
        ).strip(),
    },
    {
        "subject": "Evidence",
        "type": "mcq",
        "prompt": "Under the Federal Rules, prior inconsistent statements are admissible substantively when:",
        "choices": [
            "They were made under oath at a prior proceeding",
            "They relate to bias",
            "They are used only to impeach",
            "They were made to police shortly after the event",
        ],
        "answer": 0,
        "explanation": "A prior inconsistent statement is non-hearsay when made under oath at a prior proceeding; otherwise it is limited to impeachment.",
    },
    {
        "subject": "Trusts & Estates",
        "type": "essay",
        "prompt": "Explain how a charitable trust can be modified when its specific purpose becomes impossible to carry out.",
        "grading_keywords": [
            "charitable trust",
            "cy pres",
            "general charitable intent",
            "impracticable",
            "trust modification",
        ],
        "explanation": textwrap.dedent(
            """
            When a charitable trust's purpose becomes impossible or impracticable, courts may apply cy pres to modify the
            trust in a manner consistent with the settlor's general charitable intent. The trustee or attorney general usually
            petitions the court to redirect funds to a similar charitable purpose.
            """
        ).strip(),
    },
    {
        "subject": "Secured Transactions",
        "type": "mcq",
        "prompt": "Attachment of a security interest requires:",
        "choices": [
            "Value given, debtor has rights in the collateral, and an authenticated security agreement",
            "Filing a financing statement",
            "Notifying other creditors",
            "Possession by the secured party",
        ],
        "answer": 0,
        "explanation": "Attachment requires value, rights in the collateral, and an authenticated security agreement (or possession/control depending on collateral).",
    },
    {
        "subject": "Constitutional Law",
        "type": "essay",
        "prompt": "A state imposes a tax on goods imported from other states. Analyze the constitutional issues raised.",
        "grading_keywords": [
            "Dormant Commerce Clause",
            "discrimination",
            "market participant",
            "balancing test",
            "Privileges and Immunities",
        ],
        "explanation": textwrap.dedent(
            """
            The Dormant Commerce Clause prohibits states from discriminating against or unduly burdening interstate commerce.
            A facially discriminatory tax is presumptively invalid unless the state can show it advances a legitimate local
            purpose that cannot be served by nondiscriminatory means. The state may also rely on the market-participant
            exception if it is acting as a buyer or seller rather than a regulator.
            """
        ).strip(),
    },
    {
        "subject": "Family Law",
        "type": "mcq",
        "prompt": "In an equitable distribution jurisdiction, marital property generally includes:",
        "choices": [
            "Property acquired before marriage only",
            "Property acquired during marriage regardless of title",
            "Only income earned by the higher-earning spouse",
            "Separate property gifts",
        ],
        "answer": 1,
        "explanation": "Marital property typically includes assets acquired during the marriage by either spouse, regardless of how title is held.",
    },
    {
        "subject": "Criminal Law",
        "type": "mcq",
        "prompt": "Felony murder liability generally requires:",
        "choices": [
            "Any death that occurs during a felony, regardless of cause",
            "A death proximately caused during the commission of an inherently dangerous felony",
            "Only intentional killings",
            "Proof that the defendant personally killed the victim",
        ],
        "answer": 1,
        "explanation": "Felony murder attaches when a death is proximately caused during the commission of an inherently dangerous felony by the defendant or a co-felon.",
    },
    {
        "subject": "Evidence",
        "type": "essay",
        "prompt": "Police entered a home without a warrant after hearing screams. Discuss admissibility of statements made inside under the hearsay rule and any confrontation issues.",
        "grading_keywords": [
            "excited utterance",
            "present sense impression",
            "public safety",
            "testimonial",
            "confrontation clause",
        ],
        "explanation": textwrap.dedent(
            """
            Statements made during an ongoing emergency can fall under the excited utterance or present sense impression
            exceptions and may be deemed non-testimonial for Confrontation Clause purposes. Once the emergency ends, statements
            become testimonial and require confrontation unless the declarant is unavailable and there was a prior opportunity
            for cross-examination.
            """
        ).strip(),
    },
]

QUESTIONS: List[Question] = [
    Question(
        id=f"q{index:03d}",
        subject=data["subject"],
        type=data["type"],
        prompt=data["prompt"],
        explanation=data["explanation"],
        choices=list(data.get("choices", [])),
        answer=data.get("answer"),
        grading_keywords=list(data.get("grading_keywords", [])),
    )
    for index, data in enumerate(_QUESTIONS_RAW, start=1)
]


CONCEPT_SNIPPETS: Dict[str, List[str]] = {
    "Contracts": [
        "Offer + acceptance + consideration create a contract unless barred by defenses.",
        "The parol evidence rule limits extrinsic evidence that contradicts a final written integration.",
        "Anticipatory repudiation allows the non-breaching party to treat the breach as immediate and seek damages or assurances.",
    ],
    "Torts": [
        "Negligence requires duty, breach, causation, and damages.",
        "Invitees receive the highest duty of care on premises liability questions.",
        "Comparative negligence reduces but does not bar recovery unless jurisdiction follows pure contributory negligence.",
    ],
    "Criminal Law": [
        "Felony murder extends malice when a killing occurs during an inherently dangerous felony.",
        "Mens rea terms: purposely, knowingly, recklessly, negligently (MPC).",
        "Defenses like self-defense require reasonable belief in imminent unlawful force.",
    ],
    "Criminal Procedure": [
        "Miranda warnings are triggered by custodial interrogation.",
        "The exclusionary rule suppresses evidence obtained in violation of the Fourth Amendment, subject to good-faith exceptions.",
        "The Sixth Amendment right to counsel is offense specific and attaches at critical stages after formal proceedings begin.",
    ],
    "Evidence": [
        "Hearsay is an out-of-court statement offered for its truth; assess exclusions and exceptions before admitting.",
        "Character evidence is limited: prosecution cannot open the door to propensity evidence in criminal cases.",
        "Prior inconsistent statements under oath at prior proceedings are substantive non-hearsay under Rule 801(d)(1).",
    ],
    "Civil Procedure": [
        "Personal jurisdiction hinges on minimum contacts plus fairness.",
        "Subject-matter jurisdiction cannot be waived and includes federal question and diversity.",
        "Summary judgment is proper when no genuine dispute of material fact exists.",
    ],
    "Constitutional Law": [
        "Apply strict scrutiny to content-based speech restrictions.",
        "Dormant Commerce Clause forbids states from discriminating against interstate commerce without strong justification.",
        "Equal Protection analysis depends on classification: suspect, quasi-suspect, or rational basis.",
    ],
    "Real Property": [
        "Adverse possession needs actual, open, notorious, exclusive, hostile, and continuous use.",
        "A remainder becomes possessory upon natural termination of the prior estate.",
        "Landlord-tenant duties include habitability and delivery of possession.",
    ],
    "Remedies": [
        "Equitable remedies like specific performance require no adequate remedy at law and clean hands.",
        "Expectation damages put the plaintiff in the position as if the contract were performed.",
        "Injunctions require showing likelihood of irreparable harm and balance of hardships in the plaintiff's favor.",
    ],
    "Professional Responsibility": [
        "Duty of confidentiality is broad but allows disclosure to prevent reasonably certain death or substantial financial harm.",
        "Conflicts of interest require informed consent confirmed in writing.",
        "Competence demands legal knowledge, skill, thoroughness, and preparation reasonably necessary for representation.",
    ],
    "Trusts & Estates": [
        "Testamentary capacity requires knowledge of the nature of the property, natural objects of bounty, and plan of disposition.",
        "Cy pres modifies charitable trusts to effectuate general intent when specific purpose fails.",
        "Anti-lapse statutes save gifts to certain relatives who predecease the testator, substituting descendants.",
    ],
    "Secured Transactions": [
        "Attachment requires value, rights in the collateral, and an authenticated security agreement.",
        "Perfection is often achieved by filing a financing statement or taking possession/control.",
        "Priority disputes pit perfected secured parties ahead of lien creditors and later-perfected interests.",
    ],
    "Family Law": [
        "Equitable distribution divides marital property acquired during marriage.",
        "Best interests of the child govern custody determinations.",
        "Prenuptial agreements require voluntary execution and full disclosure or fair waiver.",
    ],
}


# ---------------------------------------------------------------------------
# Session tracking


class StudySession:
    """Track performance for a learning session."""

    def __init__(self) -> None:
        self.responses: List[Dict] = []

    def record(
        self,
        question: Question,
        correct: bool,
        confidence: int,
        score: float,
        details: Optional[Dict] = None,
    ) -> None:
        payload = {
            "id": question.id,
            "subject": question.subject,
            "type": question.type,
            "correct": bool(correct),
            "confidence": confidence,
            "score": score,
        }
        if details:
            payload["details"] = details
        self.responses.append(payload)

    # --- derived metrics -------------------------------------------------

    def _group_by_subject(self) -> Dict[str, List[Dict]]:
        grouped: Dict[str, List[Dict]] = defaultdict(list)
        for response in self.responses:
            grouped[response["subject"]].append(response)
        return dict(grouped)

    def mcq_accuracy(self) -> Optional[float]:
        mcq = [r for r in self.responses if r["type"] == "mcq"]
        if not mcq:
            return None
        return sum(1 for r in mcq if r["correct"]) / len(mcq)

    def essay_coverage(self) -> Optional[float]:
        essays = [r for r in self.responses if r["type"] == "essay"]
        if not essays:
            return None
        return sum(r["score"] for r in essays) / len(essays)

    def average_confidence(self) -> Optional[float]:
        if not self.responses:
            return None
        return sum(r["confidence"] for r in self.responses) / len(self.responses)

    def flagged_items(self) -> List[Dict]:
        flagged: List[Dict] = []
        for response in self.responses:
            low_confidence = response["confidence"] <= 2
            incorrect_mcq = response["type"] == "mcq" and not response["correct"]
            weak_essay = response["type"] == "essay" and response["score"] < 0.6
            if low_confidence or incorrect_mcq or weak_essay:
                flagged.append(response)
        return flagged

    def print_summary(self) -> None:
        print("\n" + "=" * 60)
        print("SESSION SUMMARY")
        print("=" * 60)

        total_questions = len(self.responses)
        print(f"Questions attempted: {total_questions}")

        mcq_accuracy = self.mcq_accuracy()
        if mcq_accuracy is not None:
            print(f"MCQ accuracy: {mcq_accuracy * 100:.1f}%")

        essay_cov = self.essay_coverage()
        if essay_cov is not None:
            print(f"Essay coverage (keywords hit): {essay_cov * 100:.1f}%")

        avg_conf = self.average_confidence()
        if avg_conf is not None:
            print(f"Average confidence: {avg_conf:.2f} / 5")

        print("\nSubject breakdown:")
        for subject, entries in sorted(self._group_by_subject().items()):
            subject_mcq = [r for r in entries if r["type"] == "mcq"]
            subject_essay = [r for r in entries if r["type"] == "essay"]

            line_parts = [f"- {subject}"]

            if subject_mcq:
                accuracy = sum(1 for r in subject_mcq if r["correct"]) / len(subject_mcq)
                line_parts.append(f"MCQ {accuracy * 100:.0f}%")

            if subject_essay:
                coverage = mean(r["score"] for r in subject_essay)
                line_parts.append(f"Essay {coverage * 100:.0f}% keywords")

            conf = sum(r["confidence"] for r in entries) / len(entries)
            line_parts.append(f"Confidence {conf:.1f}/5")

            print("  " + " | ".join(line_parts))

        flagged = self.flagged_items()
        if flagged:
            print("\nFocus these for review:")
            for item in flagged:
                summary = f"{item['subject']} ({item['type']})"
                if item["type"] == "mcq":
                    status = "incorrect" if not item["correct"] else "low confidence"
                else:
                    status = f"{item['score'] * 100:.0f}% keyword coverage"
                print(f"  - {summary}: {status}, confidence {item['confidence']}/5")
        else:
            print("\nGreat work! Nothing is currently flagged for urgent review.")

        print("=" * 60)


# ---------------------------------------------------------------------------
# Interactive helpers


def prompt_confidence() -> int:
    """Prompt the learner for a 1-5 confidence rating."""

    while True:
        raw = input("Confidence (1-5, default 3): ").strip()
        if not raw:
            return 3
        if raw.isdigit():
            value = int(raw)
            if 1 <= value <= 5:
                return value
        print("Please enter a number between 1 and 5.")


def grade_essay(answer: str, keywords: Sequence[str]) -> Dict:
    answer_lower = answer.lower()
    matched = [kw for kw in keywords if kw.lower() in answer_lower]
    missing = [kw for kw in keywords if kw.lower() not in answer_lower]
    coverage = (len(matched) / len(keywords)) if keywords else 0.0
    return {
        "matched": matched,
        "missing": missing,
        "coverage": coverage,
    }


def maybe_offer_concept_review(subject: str) -> None:
    """Offer a quick subject-specific rules refresher."""

    snippets = CONCEPT_SNIPPETS.get(subject)
    if not snippets:
        return

    choice = input(f"Would you like a quick {subject} rule refresher? (y/N): ").strip().lower()
    if choice not in {"y", "yes"}:
        return

    print("\nKey black-letter concepts:")
    for bullet in snippets:
        print(f"  • {bullet}")
    print()


def ask_mcq(question: Question, session: StudySession) -> None:
    print(f"\nSubject: {question.subject}\n{question.prompt}")
    for i, choice in enumerate(question.choices, start=1):
        print(f"{i}. {choice}")

    user_ans = input("Your answer (number): ").strip()
    correct = False
    if user_ans.isdigit():
        choice_index = int(user_ans) - 1
        correct = choice_index == question.answer

    if correct:
        print("✅ Correct!")
    else:
        correct_choice = question.choices[question.answer] if question.answer is not None else "(n/a)"
        print(f"❌ Incorrect. The correct answer is: {correct_choice}")

    print("Explanation:")
    print(textwrap.fill(question.explanation, width=80))

    maybe_offer_concept_review(question.subject)

    confidence = prompt_confidence()
    session.record(question, correct=correct, confidence=confidence, score=1.0 if correct else 0.0)


def ask_essay(question: Question, session: StudySession) -> None:
    print(f"\nSubject: {question.subject}\nEssay Prompt:\n{question.prompt}")
    response = input("\nType your answer (or hit Enter to skip): ")

    if response.strip():
        evaluation = grade_essay(response, question.grading_keywords)
        matched = ", ".join(evaluation["matched"]) or "(none)"
        missing = ", ".join(evaluation["missing"]) or "(none)"
        print(f"\nKeywords covered: {matched}")
        print(f"Keywords to review: {missing}")
        print(f"Coverage score: {evaluation['coverage'] * 100:.0f}%")
        score = evaluation["coverage"]
        correct = score >= 0.6
    else:
        print("No answer provided. Try outlining even a quick response for retrieval practice!")
        score = 0.0
        correct = False

    print("\nTeaching Explanation:")
    print(textwrap.fill(question.explanation, width=80))

    maybe_offer_concept_review(question.subject)

    confidence = prompt_confidence()
    session.record(
        question,
        correct=correct,
        confidence=confidence,
        score=score,
        details={"coverage": score},
    )


def select_subjects(questions: Iterable[Question]) -> List[str]:
    subjects = sorted({q.subject for q in questions})
    print("\nAvailable subjects:")
    for idx, subject in enumerate(subjects, start=1):
        print(f"  {idx}. {subject}")
    print("Press Enter to study all subjects or provide a comma-separated list (e.g., 1,3).")

    while True:
        choice = input("Subjects to include: ").strip()
        if not choice:
            return subjects

        indices = {token.strip() for token in choice.split(",") if token.strip()}
        try:
            selected = [subjects[int(index) - 1] for index in indices]
        except (ValueError, IndexError):
            print("Please choose valid subject numbers (e.g., 1,2).")
            continue
        if selected:
            return selected
        print("No valid subjects selected.")


def select_question_types() -> List[str]:
    options = {"1": "mcq", "2": "essay", "3": "mixed"}
    print("\nSelect question format:")
    print("  1. Multiple Choice")
    print("  2. Essay/Issue Spotting")
    print("  3. Mixed session")

    while True:
        choice = input("Choice (default 3): ").strip() or "3"
        if choice not in options:
            print("Please enter 1, 2, or 3.")
            continue
        if options[choice] == "mixed":
            return ["mcq", "essay"]
        return [options[choice]]


def choose_number_of_questions(maximum: int) -> int:
    prompt = f"How many questions would you like to answer today? (1-{maximum}): "
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            value = int(raw)
            if 1 <= value <= maximum:
                return value
        print(f"Please enter a number between 1 and {maximum}.")


def main() -> None:
    print("Welcome to the Bar Prep Tutor Agent!")

    subjects = select_subjects(QUESTIONS)
    question_types = select_question_types()

    filtered = [q for q in QUESTIONS if q.subject in subjects and q.type in question_types]
    if not filtered:
        print("No questions available for the chosen filters. Try expanding your selection.")
        return

    num_questions = choose_number_of_questions(len(filtered))
    questions = random.sample(filtered, k=num_questions)

    session = StudySession()

    for question in questions:
        if question.is_mcq:
            ask_mcq(question, session)
        else:
            ask_essay(question, session)
        print("\n" + "-" * 40)

    session.print_summary()
    print("Session complete. Keep studying for success!")


if __name__ == "__main__":
    main()

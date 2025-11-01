import json
import os
import random
import textwrap

# Filenames for questions and progress tracking
QUESTIONS_FILE = "questions.json"
PROGRESS_FILE = "progress.json"

# Example questions for initial setup (expand as needed)
DEFAULT_QUESTIONS = [
    {
        "subject": "Contracts",
        "type": "mcq",
        "question": "A offers to sell his car to B for $5,000. B accepts. What is the legal status of their agreement?",
        "choices": [
            "A valid contract exists.",
            "No contract exists because there is no consideration.",
            "No contract exists because the price is too low.",
            "No contract exists because the parties did not sign anything."
        ],
        "answer": 0,
        "feedback": [
            "Correct! All contract elements are present: offer, acceptance, and consideration.",
            "Incorrect. Consideration is present—the price is the consideration.",
            "Incorrect. The law doesn't require a minimum price for a contract.",
            "Incorrect. Contracts can be valid even if nothing is signed, unless required by the Statute of Frauds."
        ],
        "explanation": "A valid contract exists because there was an offer, acceptance, and consideration (the price)."
    },
    {
        "subject": "Torts",
        "type": "mcq",
        "question": "Which of the following is a defense to battery?",
        "choices": [
            "Consent",
            "Negligence",
            "Duress",
            "Strict liability"
        ],
        "answer": 0,
        "feedback": [
            "Correct! Consent is a recognized defense to battery.",
            "Incorrect. Negligence is not a defense to battery.",
            "Incorrect. Duress can be a defense to criminal liability, not battery.",
            "Incorrect. Strict liability is not a defense; it's a liability standard."
        ],
        "explanation": "Consent is a defense to battery."
    },
    {
        "subject": "Criminal Law",
        "type": "essay",
        "question": "Discuss whether a defendant who accidentally kills someone during a lawful act is guilty of homicide.",
        "grading_keywords": ["mens rea", "actus reus", "lawful act", "criminal negligence", "involuntary manslaughter"],
        "explanation": textwrap.dedent("""
            For homicide, the prosecution must prove that the defendant caused the death of another human being. 
            Mens rea (criminal intent) is required for most homicides. If the killing was truly accidental during a lawful act 
            and not due to criminal negligence, the defendant may not be guilty of homicide. However, if their actions were 
            reckless or grossly negligent, they could be guilty of involuntary manslaughter.
        """),
        "sample_answer": textwrap.dedent("""
            A defendant who accidentally kills during a lawful act may not be guilty of homicide unless their actions involved criminal negligence. 
            To be convicted, there must be both actus reus (the act of killing) and mens rea (intent or recklessness). If the act was lawful 
            and not reckless, the defendant is not criminally liable. If the act was lawful but reckless or grossly negligent, involuntary manslaughter may apply.
        """)
    },
    {
        "subject": "Constitutional Law",
        "type": "mcq",
        "question": "Which amendment protects against unreasonable searches and seizures?",
        "choices": [
            "First Amendment",
            "Fourth Amendment",
            "Fifth Amendment",
            "Eighth Amendment"
        ],
        "answer": 1,
        "feedback": [
            "Incorrect. The First Amendment covers speech, religion, and assembly.",
            "Correct! The Fourth Amendment protects against unreasonable searches and seizures.",
            "Incorrect. The Fifth Amendment covers due process and self-incrimination.",
            "Incorrect. The Eighth Amendment covers cruel and unusual punishment."
        ],
        "explanation": "The Fourth Amendment protects against unreasonable searches and seizures."
    },
    {
        "subject": "Evidence",
        "type": "essay",
        "question": "Explain the hearsay rule and its exceptions.",
        "grading_keywords": ["hearsay", "out of court statement", "truth of the matter", "exceptions", "declarant", "admissible"],
        "explanation": textwrap.dedent("""
            Hearsay is an out of court statement offered to prove the truth of the matter asserted. 
            Hearsay is generally inadmissible unless it falls within an exception (e.g., present sense impression, 
            excited utterance, business records). The rationale is that such statements are unreliable unless 
            certain conditions are met.
        """),
        "sample_answer": textwrap.dedent("""
            The hearsay rule excludes out of court statements offered for the truth of the matter asserted, unless an exception applies. 
            Common exceptions include present sense impression, excited utterance, and business records. Statements by a declarant 
            in court are generally admissible, while those made outside are not unless an exception applies.
        """)
    }
]

def ensure_questions_file():
    if not os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "w") as f:
            json.dump(DEFAULT_QUESTIONS, f, indent=2)

def load_questions():
    with open(QUESTIONS_FILE, "r") as f:
        return json.load(f)

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def update_progress(progress, subject, qtype, correct):
    if subject not in progress:
        progress[subject] = {"mcq_correct": 0, "mcq_total": 0, "essay_total": 0}
    if qtype == "mcq":
        if correct:
            progress[subject]["mcq_correct"] += 1
        progress[subject]["mcq_total"] += 1
    elif qtype == "essay":
        progress[subject]["essay_total"] += 1

def show_summary(progress):
    print("\nProgress Summary:")
    for subject, stats in progress.items():
        mcq_percent = (stats["mcq_correct"] / stats["mcq_total"] * 100) if stats["mcq_total"] > 0 else 0
        print(f"- {subject}:")
        print(f"    MCQ: {stats['mcq_correct']}/{stats['mcq_total']} correct ({mcq_percent:.1f}%)")
        print(f"    Essay questions attempted: {stats['essay_total']}")

def select_subjects(questions):
    subjects = sorted(set(q["subject"] for q in questions))
    print("Available subjects:")
    for idx, subj in enumerate(subjects):
        print(f"{idx+1}. {subj}")
    selection = input("Enter the numbers of subjects you want (comma-separated, blank for all): ")
    if not selection.strip():
        return subjects
    indexes = [int(x)-1 for x in selection.split(",") if x.strip().isdigit() and 0 < int(x) <= len(subjects)]
    return [subjects[i] for i in indexes if i < len(subjects)]

def ask_mcq(q):
    print(f"\nSubject: {q['subject']}\n{q['question']}")
    choices = list(enumerate(q['choices']))
    random.shuffle(choices)
    for i, choice in choices:
        print(f"{choices.index((i, choice))+1}. {choice}")
    user_ans = input("Your answer (number): ")
    try:
        user_idx = int(user_ans) - 1
        ans_idx = choices[user_idx][0]
        print(q['feedback'][ans_idx])
        correct = ans_idx == q['answer']
    except (ValueError, IndexError):
        print("Invalid input.")
        correct = False
    print(f"Explanation: {q['explanation']}")
    return correct

def ask_essay(q):
    print(f"\nSubject: {q['subject']}\nEssay Question:\n{q['question']}")
    user_ans = input("\nType your answer (or hit Enter to skip): ")
    if user_ans.strip():
        score = grade_essay(user_ans, q['grading_keywords'])
        print(f"\nYour essay covers {score}/{len(q['grading_keywords'])} key points.")
    else:
        print("No answer provided.")
        score = 0
    print("\nTeaching Explanation:\n" + textwrap.fill(q['explanation'], width=80))
    print("\nSample High-scoring Answer:\n" + textwrap.fill(q.get('sample_answer', 'N/A'), width=80))
    return True

def grade_essay(answer, keywords):
    answer_lower = answer.lower()
    score = sum(1 for kw in keywords if kw.lower() in answer_lower)
    return score

def main():
    ensure_questions_file()
    questions = load_questions()
    print("Welcome to the Bar Prep Tutor Agent!")
    progress = load_progress()

    # Subject selection
    selected_subjects = select_subjects(questions)
    filtered_questions = [q for q in questions if q["subject"] in selected_subjects]

    if not filtered_questions:
        print("No questions for selected subjects. Exiting.")
        return

    # Type selection
    print("Which question types do you want?")
    print("1. Multiple Choice only")
    print("2. Essays only")
    print("3. Both")
    qtype_choice = input("Type the number: ").strip()
    if qtype_choice == "1":
        filtered_questions = [q for q in filtered_questions if q["type"] == "mcq"]
    elif qtype_choice == "2":
        filtered_questions = [q for q in filtered_questions if q["type"] == "essay"]
    # else leave both types

    num_questions = input("How many questions would you like to answer today? (1-20): ")
    try:
        num_questions = int(num_questions)
    except ValueError:
        num_questions = 5
    session_questions = random.sample(filtered_questions, k=min(num_questions, len(filtered_questions)))

    for q in session_questions:
        if q["type"] == "mcq":
            correct = ask_mcq(q)
            update_progress(progress, q["subject"], "mcq", correct)
        elif q["type"] == "essay":
            ask_essay(q)
            update_progress(progress, q["subject"], "essay", True)
        print("\n" + "-"*40)

    save_progress(progress)
    show_summary(progress)
    print("Session complete. Keep studying for success!")

if __name__ == "__main__":
    main()

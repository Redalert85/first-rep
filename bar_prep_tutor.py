import random
import textwrap

# Sample questions database
QUESTIONS = [
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
        "explanation": "The Fourth Amendment protects against unreasonable searches and seizures."
    },
    {
        "subject": "Property",
        "type": "mcq",
        "question": "Which of the following is a future interest?",
        "choices": [
            "Life estate",
            "Fee simple absolute",
            "Remainder",
            "Tenancy in common"
        ],
        "answer": 2,
        "explanation": "A remainder is a future interest."
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
        """)
    },
    {
        "subject": "Civil Procedure",
        "type": "mcq",
        "question": "Which of the following motions can dispose of a case before trial?",
        "choices": [
            "Motion to dismiss",
            "Motion for summary judgment",
            "Motion to compel discovery",
            "Motion for directed verdict"
        ],
        "answer": 1,
        "explanation": "A motion for summary judgment can dispose of a case before trial if there is no genuine issue of material fact."
    }
]

def ask_mcq(q):
    print(f"\nSubject: {q['subject']}\n{q['question']}")
    for i, choice in enumerate(q['choices']):
        print(f"{i+1}. {choice}")
    user_ans = input("Your answer (number): ")
    try:
        user_ans = int(user_ans) - 1
        correct = user_ans == q['answer']
    except ValueError:
        correct = False
    if correct:
        print("Correct!")
    else:
        print(f"Incorrect. The correct answer is: {q['choices'][q['answer']]}")
    print(f"Explanation: {q['explanation']}")

def ask_essay(q):
    print(f"\nSubject: {q['subject']}\nEssay Question:\n{q['question']}")
    user_ans = input("\nType your answer (or hit Enter to skip): ")
    if user_ans.strip():
        score = grade_essay(user_ans, q['grading_keywords'])
        print(f"\nYour essay covers {score}/{len(q['grading_keywords'])} key points.")
    else:
        print("No answer provided.")
    print("Teaching Explanation:\n" + textwrap.fill(q['explanation'], width=80))

def grade_essay(answer, keywords):
    answer_lower = answer.lower()
    score = sum(1 for kw in keywords if kw in answer_lower)
    return score

def main():
    print("Welcome to the Bar Prep Tutor Agent!")
    num_questions = int(input("How many questions would you like to answer today? (1-10): "))
    questions = random.sample(QUESTIONS, k=min(num_questions, len(QUESTIONS)))
    for q in questions:
        if q['type'] == "mcq":
            ask_mcq(q)
        elif q['type'] == "essay":
            ask_essay(q)
        print("\n" + "-"*40)
    print("Session complete. Keep studying for success!")

if __name__ == "__main__":
    main()

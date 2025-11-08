#!/usr/bin/env python3
"""
Adaptive Learning System with SQLite database for Iowa Bar Prep
Implements SM-2 spaced repetition algorithm with performance tracking
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Card:
    """Represents a flashcard in the spaced repetition system"""
    card_id: int
    subject: str
    topic: str
    concept_id: str
    front: str
    back: str
    ease_factor: float
    interval_days: int
    repetitions: int
    due_date: str
    created_at: str
    last_reviewed: Optional[str] = None

@dataclass
class Performance:
    """Represents a review performance record"""
    review_id: int
    card_id: int
    review_date: str
    quality: int
    time_spent_seconds: int

class AdaptiveLearningSystem:
    """Manages the spaced repetition database and analytics"""

    def __init__(self, db_path: str = "iowa_bar_prep.db"):
        self.db_path = db_path
        self.conn = None
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()

        # Cards table - stores flashcards with spaced repetition metadata
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                card_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                concept_id TEXT NOT NULL,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                ease_factor REAL DEFAULT 2.5,
                interval_days INTEGER DEFAULT 1,
                repetitions INTEGER DEFAULT 0,
                due_date TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_reviewed TEXT
            )
        """)

        # Performance table - tracks review history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id INTEGER NOT NULL,
                review_date TEXT DEFAULT CURRENT_TIMESTAMP,
                quality INTEGER NOT NULL CHECK(quality >= 0 AND quality <= 5),
                time_spent_seconds INTEGER DEFAULT 0,
                FOREIGN KEY (card_id) REFERENCES cards(card_id)
            )
        """)

        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cards_due_date ON cards(due_date)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cards_subject ON cards(subject)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_performance_card_id ON performance(card_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_performance_review_date ON performance(review_date)
        """)

        self.conn.commit()

    def add_card(self, subject: str, topic: str, concept_id: str,
                 front: str, back: str) -> int:
        """Add a new card to the database"""
        cursor = self.conn.cursor()
        due_date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO cards (subject, topic, concept_id, front, back, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (subject, topic, concept_id, front, back, due_date))

        self.conn.commit()
        return cursor.lastrowid

    def review_card(self, card_id: int, quality: int, time_spent: int = 0):
        """
        Review a card and update using SM-2 algorithm
        Quality: 0-5 (0=complete blackout, 5=perfect response)
        """
        cursor = self.conn.cursor()

        # Get current card data
        cursor.execute("""
            SELECT ease_factor, interval_days, repetitions
            FROM cards WHERE card_id = ?
        """, (card_id,))
        row = cursor.fetchone()

        if not row:
            raise ValueError(f"Card {card_id} not found")

        ease_factor = row['ease_factor']
        interval_days = row['interval_days']
        repetitions = row['repetitions']

        # SM-2 Algorithm
        if quality < 3:
            # Failed - reset
            repetitions = 0
            interval_days = 1
        else:
            # Passed - calculate new interval
            if repetitions == 0:
                interval_days = 1
            elif repetitions == 1:
                interval_days = 6
            else:
                interval_days = int(interval_days * ease_factor)

            repetitions += 1

        # Update ease factor
        ease_factor = max(1.3, ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        # Calculate next due date
        next_due = (datetime.now() + timedelta(days=interval_days)).strftime("%Y-%m-%d")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update card
        cursor.execute("""
            UPDATE cards
            SET ease_factor = ?, interval_days = ?, repetitions = ?,
                due_date = ?, last_reviewed = ?
            WHERE card_id = ?
        """, (ease_factor, interval_days, repetitions, next_due, now, card_id))

        # Record performance
        cursor.execute("""
            INSERT INTO performance (card_id, quality, time_spent_seconds)
            VALUES (?, ?, ?)
        """, (card_id, quality, time_spent))

        self.conn.commit()

    def get_due_cards(self, limit: int = 20) -> List[Card]:
        """Get cards due for review"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM cards
            WHERE date(due_date) <= date('now')
            ORDER BY due_date, card_id
            LIMIT ?
        """, (limit,))

        return [Card(**dict(row)) for row in cursor.fetchall()]

    def get_card_count(self) -> int:
        """Get total number of cards"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM cards")
        return cursor.fetchone()['count']

    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Execute a custom query and return results"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def populate_from_bar_tutor():
    """Populate database from existing bar tutor concepts"""
    try:
        # Suppress dotenv import error
        import sys
        import io
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()

        from bar_tutor_unified import LegalKnowledgeGraph

        sys.stderr = old_stderr
    except Exception as e:
        print(f"Error loading bar tutor: {e}")
        print("Falling back to manual initialization...")
        populate_manually()
        return

    system = AdaptiveLearningSystem()
    kg = LegalKnowledgeGraph()

    print("Loading concepts from bar tutor...")

    for concept_id, concept in kg.nodes.items():
        # Create multiple cards per concept

        # 1. Rule statement card
        if concept.rule_statement:
            system.add_card(
                subject=concept.subject,
                topic=concept.name,
                concept_id=f"{concept_id}_rule",
                front=f"State the rule for: {concept.name}",
                back=concept.rule_statement
            )

        # 2. Elements card
        if concept.elements:
            system.add_card(
                subject=concept.subject,
                topic=concept.name,
                concept_id=f"{concept_id}_elements",
                front=f"What are the elements of {concept.name}?",
                back="\n".join(f"{i}. {elem}" for i, elem in enumerate(concept.elements, 1))
            )

        # 3. Common traps card
        if hasattr(concept, 'common_traps') and concept.common_traps:
            system.add_card(
                subject=concept.subject,
                topic=concept.name,
                concept_id=f"{concept_id}_traps",
                front=f"What are common exam traps for {concept.name}?",
                back="\n".join(f"⚠️ {trap}" for trap in concept.common_traps)
            )

    card_count = system.get_card_count()
    print(f"✅ Created {card_count} flashcards in database")
    system.close()

def populate_manually():
    """Manually populate database with sample Iowa Bar concepts"""
    system = AdaptiveLearningSystem()

    print("Initializing database with Iowa Bar concepts...")

    # Sample comprehensive concepts across all subjects
    concepts = [
        # Constitutional Law (MBE)
        ("Constitutional Law", "Judicial Review", "judicial_review",
         "What is the doctrine of judicial review?",
         "The power of federal courts to review the constitutionality of government actions. Established in Marbury v. Madison."),
        ("Constitutional Law", "Commerce Clause", "commerce_clause",
         "What is the scope of Congress's commerce power?",
         "Congress may regulate: 1) channels of interstate commerce, 2) instrumentalities of interstate commerce, 3) activities substantially affecting interstate commerce"),
        ("Constitutional Law", "Equal Protection", "equal_protection",
         "What are the three levels of Equal Protection scrutiny?",
         "1) Strict Scrutiny (race, national origin, fundamental rights)\n2) Intermediate (gender, legitimacy)\n3) Rational Basis (all others)"),
        ("Constitutional Law", "Due Process", "due_process",
         "What are the requirements for procedural due process?",
         "1) Notice must be reasonably calculated to inform\n2) Opportunity to be heard\n3) Neutral decision-maker"),
        ("Constitutional Law", "First Amendment", "first_amendment",
         "What is the test for content-based speech restrictions?",
         "Strict scrutiny: Must be narrowly tailored to achieve a compelling government interest"),

        # Evidence (MBE)
        ("Evidence", "Hearsay", "hearsay_definition",
         "What is hearsay?",
         "An out-of-court statement offered to prove the truth of the matter asserted"),
        ("Evidence", "Hearsay Exceptions", "hearsay_803",
         "Name 5 hearsay exceptions that don't require unavailability",
         "1) Present sense impression\n2) Excited utterance\n3) State of mind\n4) Medical diagnosis/treatment\n5) Business records"),
        ("Evidence", "Character Evidence", "character_evidence",
         "When is character evidence admissible in a criminal case?",
         "Defendant may introduce evidence of pertinent good character trait; prosecution may rebut. Victim's character admissible if relevant to defense."),
        ("Evidence", "Authentication", "authentication",
         "What must be shown to authenticate a document?",
         "Evidence sufficient to support a finding that the item is what the proponent claims it to be"),
        ("Evidence", "Expert Testimony", "expert_testimony",
         "What are the requirements for expert testimony under Daubert?",
         "1) Reliable methodology\n2) Relevant to case\n3) Applied reliably to facts"),

        # Contracts (MBE)
        ("Contracts", "Offer and Acceptance", "offer_acceptance",
         "What are the elements of a valid offer?",
         "1) Intent to contract\n2) Definite and certain terms\n3) Communication to offeree"),
        ("Contracts", "Consideration", "consideration",
         "What constitutes valid consideration?",
         "A bargained-for exchange of legal value: benefit to promisor OR detriment to promisee"),
        ("Contracts", "Statute of Frauds", "statute_of_frauds",
         "What contracts must be in writing under the Statute of Frauds?",
         "MY LEGS: Marriage, Year, Land, Executor, Goods $500+, Surety"),
        ("Contracts", "Parol Evidence Rule", "parol_evidence",
         "When does the parol evidence rule bar extrinsic evidence?",
         "Bars evidence of prior or contemporaneous agreements that contradict a complete and final written contract"),
        ("Contracts", "Breach and Remedies", "breach_remedies",
         "What is the standard measure of damages for breach?",
         "Expectation damages: put non-breaching party in position they would have been in if contract performed"),

        # Torts (MBE)
        ("Torts", "Negligence", "negligence_elements",
         "What are the elements of negligence?",
         "1) Duty\n2) Breach\n3) Causation (actual and proximate)\n4) Damages"),
        ("Torts", "Duty of Care", "duty_of_care",
         "What is the general standard of care?",
         "Reasonable person under the circumstances"),
        ("Torts", "Intentional Torts", "battery",
         "What are the elements of battery?",
         "1) Intent to cause harmful or offensive contact\n2) Harmful or offensive contact with person\n3) Causation"),
        ("Torts", "Strict Liability", "strict_liability",
         "What activities are subject to strict liability?",
         "1) Abnormally dangerous activities\n2) Wild animals\n3) Defective products"),
        ("Torts", "Products Liability", "products_liability",
         "What are the three theories of products liability?",
         "1) Manufacturing defect\n2) Design defect\n3) Failure to warn"),

        # Criminal Law (MBE)
        ("Criminal Law", "Homicide", "murder_elements",
         "What is the mens rea for common law murder?",
         "Malice aforethought: intent to kill, intent to cause serious bodily harm, depraved heart, or felony murder"),
        ("Criminal Law", "Felony Murder", "felony_murder",
         "What is the felony murder rule?",
         "A killing during the commission of an inherently dangerous felony is murder. BARRK: Burglary, Arson, Robbery, Rape, Kidnapping"),
        ("Criminal Law", "Accomplice Liability", "accomplice_liability",
         "When is someone liable as an accomplice?",
         "Intent to assist AND intent that principal commit the crime, with assistance given"),
        ("Criminal Law", "Defenses", "self_defense",
         "What are the requirements for self-defense?",
         "1) Reasonable belief of imminent unlawful force\n2) Proportional force\n3) No duty to retreat (unless aggressor)"),
        ("Criminal Law", "Inchoate Crimes", "attempt",
         "What are the elements of attempt?",
         "1) Specific intent to commit the crime\n2) Substantial step beyond mere preparation"),

        # Criminal Procedure (MBE)
        ("Criminal Procedure", "Fourth Amendment", "search_seizure",
         "When is a warrant required for a search?",
         "When there is a reasonable expectation of privacy, unless an exception applies"),
        ("Criminal Procedure", "Search Exceptions", "search_exceptions",
         "Name 6 exceptions to the warrant requirement",
         "ESCAPES: Exigent circumstances, Search incident to arrest, Consent, Automobile, Plain view, Emergency, Stop & frisk"),
        ("Criminal Procedure", "Miranda Rights", "miranda",
         "When must Miranda warnings be given?",
         "Before custodial interrogation by police"),
        ("Criminal Procedure", "Exclusionary Rule", "exclusionary_rule",
         "What evidence is excluded under the exclusionary rule?",
         "Evidence obtained in violation of Fourth, Fifth, or Sixth Amendment (and fruit of the poisonous tree)"),
        ("Criminal Procedure", "Right to Counsel", "right_to_counsel",
         "When does the Sixth Amendment right to counsel attach?",
         "At all critical stages after formal charging (indictment, information, arraignment, etc.)"),

        # Civil Procedure (MBE)
        ("Civil Procedure", "Subject Matter Jurisdiction", "smj",
         "What are the two types of federal subject matter jurisdiction?",
         "1) Federal question (arising under federal law)\n2) Diversity (complete diversity + amount > $75,000)"),
        ("Civil Procedure", "Personal Jurisdiction", "personal_jurisdiction",
         "What is required for personal jurisdiction?",
         "1) Minimum contacts with forum state\n2) Exercise of jurisdiction must be fair and reasonable"),
        ("Civil Procedure", "Pleadings", "pleadings",
         "What must a complaint contain under Rule 8?",
         "1) Short and plain statement of grounds for jurisdiction\n2) Claim showing entitlement to relief\n3) Demand for judgment"),
        ("Civil Procedure", "Joinder", "joinder",
         "When is a counterclaim compulsory?",
         "When it arises out of the same transaction or occurrence as the plaintiff's claim"),
        ("Civil Procedure", "Summary Judgment", "summary_judgment",
         "What is the standard for summary judgment?",
         "No genuine dispute as to any material fact, and movant is entitled to judgment as a matter of law"),

        # Real Property (MBE)
        ("Real Property", "Estates", "fee_simple",
         "What is a fee simple absolute?",
         "Absolute ownership with infinite duration, freely transferable and inheritable"),
        ("Real Property", "Concurrent Estates", "joint_tenancy",
         "What are the four unities required for joint tenancy?",
         "TTIP: Time, Title, Interest, Possession"),
        ("Real Property", "Easements", "easement_types",
         "What are the four types of easements?",
         "1) Express (grant or reservation)\n2) Implied (prior use or necessity)\n3) Prescription (adverse use)\n4) Estoppel"),
        ("Real Property", "Adverse Possession", "adverse_possession",
         "What are the elements of adverse possession?",
         "OCEAN: Open and notorious, Continuous, Exclusive, Actual, Non-permissive (hostile)"),
        ("Real Property", "Recording Acts", "recording_acts",
         "What are the three types of recording acts?",
         "1) Race: first to record wins\n2) Notice: last BFP wins\n3) Race-Notice: first BFP to record wins"),

        # Professional Responsibility (Essay)
        ("Professional Responsibility", "Conflicts of Interest", "conflicts",
         "When can a lawyer represent clients with conflicting interests?",
         "1) Lawyer reasonably believes can provide competent/diligent representation\n2) Not prohibited by law\n3) Not same litigation\n4) Each client gives informed written consent"),
        ("Professional Responsibility", "Confidentiality", "confidentiality",
         "When may a lawyer reveal confidential information?",
         "1) Client consent\n2) Prevent death/substantial bodily harm\n3) Prevent/rectify financial fraud\n4) Comply with law/court order\n5) Establish claim/defense"),
        ("Professional Responsibility", "Competence", "competence",
         "What does the duty of competence require?",
         "Legal knowledge, skill, thoroughness, and preparation reasonably necessary for representation"),

        # Corporations (Essay)
        ("Corporations", "Formation", "formation",
         "What are the requirements to form a corporation?",
         "1) File articles of incorporation\n2) Pay fees\n3) Hold organizational meeting\n4) Adopt bylaws"),
        ("Corporations", "Fiduciary Duties", "fiduciary_duties",
         "What are the two fiduciary duties of directors?",
         "1) Duty of Care: act with care of ordinarily prudent person\n2) Duty of Loyalty: act in good faith in corporation's best interest"),
        ("Corporations", "Piercing the Veil", "piercing_veil",
         "When will courts pierce the corporate veil?",
         "1) Failure to follow formalities\n2) Undercapitalization\n3) Fraud or injustice\n4) Alter ego"),

        # Wills, Trusts & Estates (Essay)
        ("Wills, Trusts & Estates", "Will Execution", "will_execution",
         "What are the requirements for a valid will?",
         "1) Testamentary capacity\n2) Testamentary intent\n3) Writing\n4) Signed by testator\n5) Two witnesses"),
        ("Wills, Trusts & Estates", "Trust Creation", "trust_creation",
         "What are the elements of a valid trust?",
         "1) Intent\n2) Identifiable trust property\n3) Ascertainable beneficiaries\n4) Proper purpose\n5) Trustee duties"),
        ("Wills, Trusts & Estates", "Intestate Succession", "intestacy",
         "Who inherits under intestate succession?",
         "Surviving spouse and descendants first, then parents, then siblings, then more remote relatives"),

        # Family Law (Essay)
        ("Family Law", "Marriage", "marriage_requirements",
         "What are the requirements for a valid marriage?",
         "1) Legal capacity (age, mental capacity)\n2) Consent\n3) No legal impediment\n4) License\n5) Ceremony"),
        ("Family Law", "Divorce", "divorce_grounds",
         "What are the grounds for divorce?",
         "Most states: no-fault (irreconcilable differences, irretrievable breakdown)"),
        ("Family Law", "Property Division", "property_division",
         "How is marital property divided in divorce?",
         "Community property states: 50/50. Equitable distribution states: fair and equitable division"),
        ("Family Law", "Child Custody", "child_custody",
         "What is the standard for child custody decisions?",
         "Best interests of the child"),

        # Secured Transactions (Essay)
        ("Secured Transactions", "Attachment", "attachment",
         "What are the requirements for attachment of a security interest?",
         "1) Value given\n2) Debtor has rights in collateral\n3) Security agreement (authenticated record describing collateral)"),
        ("Secured Transactions", "Perfection", "perfection",
         "How is a security interest perfected?",
         "1) Filing financing statement\n2) Possession\n3) Control\n4) Automatic (PMSI in consumer goods)"),
        ("Secured Transactions", "Priority", "priority",
         "What is the general priority rule for security interests?",
         "First to file or perfect wins"),

        # Iowa Procedure (Essay)
        ("Iowa Procedure", "Jurisdiction", "iowa_jurisdiction",
         "What is the jurisdictional amount for Iowa small claims?",
         "$6,500 or less"),
        ("Iowa Procedure", "Service", "iowa_service",
         "How is service of process made in Iowa?",
         "Personal service, certified mail, publication, or as court orders"),
    ]

    print(f"Adding {len(concepts)} flashcards...")

    for subject, topic, concept_id, front, back in concepts:
        system.add_card(
            subject=subject,
            topic=topic,
            concept_id=concept_id,
            front=front,
            back=back
        )

    card_count = system.get_card_count()
    print(f"✅ Created {card_count} flashcards in database")
    system.close()

if __name__ == "__main__":
    print("Initializing Adaptive Learning System...")
    system = AdaptiveLearningSystem()
    print(f"Database initialized: {system.db_path}")
    print(f"Total cards: {system.get_card_count()}")
    system.close()

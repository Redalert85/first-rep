#!/usr/bin/env python3
"""
Black Letter Law Database - Structured legal rules organized by subject
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class LegalRule:
    """Represents a single legal rule with elements and citations"""
    subject: str  # e.g., "Torts", "Contracts"
    topic: str    # e.g., "Negligence", "Contract Formation"
    subtopic: str  # e.g., "Elements", "Defenses"
    title: str    # Brief title
    rule: str     # Complete rule statement
    elements: List[str]  # List of elements (if applicable)
    citations: List[str]  # Case/statute citations
    notes: str    # Additional notes or context


class BlackLetterLawDatabase:
    """Searchable database of black letter law rules"""

    def __init__(self, db_file: Optional[str] = None):
        """
        Initialize database from JSON file or create new

        Args:
            db_file: Path to JSON database file
        """
        self.rules: List[LegalRule] = []
        self.db_file = db_file

        if db_file:
            try:
                self.load_from_file(db_file)
            except FileNotFoundError:
                print(f"Database file {db_file} not found. Creating new database.")
                self._populate_initial_rules()
                self.save_to_file(db_file)
        else:
            self._populate_initial_rules()

    def _populate_initial_rules(self):
        """Populate with initial black letter law rules"""

        # TORTS - Negligence
        self.add_rule(LegalRule(
            subject="Torts",
            topic="Negligence",
            subtopic="Elements",
            title="Elements of Negligence",
            rule="To establish negligence, plaintiff must prove: (1) defendant owed plaintiff a duty of care; (2) defendant breached that duty; (3) the breach was the actual and proximate cause of plaintiff's injuries; and (4) plaintiff suffered damages.",
            elements=["Duty", "Breach", "Causation (actual and proximate)", "Damages"],
            citations=["Restatement (Second) of Torts § 281"],
            notes="This is the standard negligence prima facie case. All four elements must be established."
        ))

        self.add_rule(LegalRule(
            subject="Torts",
            topic="Negligence",
            subtopic="Duty",
            title="Duty of Reasonable Care",
            rule="All persons owe a duty to act as a reasonably prudent person under the circumstances. The standard is objective and does not account for the defendant's individual characteristics (except for children, professionals, and those with physical disabilities).",
            elements=["Reasonably prudent person standard", "Objective test", "Under the circumstances"],
            citations=["Restatement (Second) of Torts § 283"],
            notes="Exceptions: Children held to standard of child of similar age, intelligence, experience. Professionals held to standard of professionals in their field."
        ))

        self.add_rule(LegalRule(
            subject="Torts",
            topic="Negligence",
            subtopic="Causation",
            title="Causation - Actual and Proximate",
            rule="Plaintiff must prove both actual cause (but-for causation) and proximate cause (legal cause/foreseeability). But-for test: But for defendant's conduct, would the injury have occurred? Proximate cause: Was the type of injury foreseeable?",
            elements=["Actual cause (but-for test)", "Proximate cause (foreseeability)", "No superseding intervening cause"],
            citations=["Restatement (Second) of Torts § 431", "Palsgraf v. Long Island R.R."],
            notes="Both types of causation required. Proximate cause limits liability to foreseeable consequences."
        ))

        # CONTRACTS - Formation
        self.add_rule(LegalRule(
            subject="Contracts",
            topic="Contract Formation",
            subtopic="Elements",
            title="Elements of Contract",
            rule="A valid contract requires: (1) offer; (2) acceptance; (3) consideration; (4) no defenses to formation (e.g., incapacity, illegality, statute of frauds).",
            elements=["Offer", "Acceptance", "Consideration", "No defenses"],
            citations=["Restatement (Second) of Contracts § 17"],
            notes="Mutual assent (offer + acceptance) = meeting of the minds. Some contracts also require writing under statute of frauds."
        ))

        self.add_rule(LegalRule(
            subject="Contracts",
            topic="Contract Formation",
            subtopic="Offer",
            title="Valid Offer",
            rule="An offer is a manifestation of willingness to enter into a bargain, made in such a way that another person is justified in understanding that their assent will conclude the bargain. Must contain definite and certain terms.",
            elements=["Manifestation of willingness", "Definite terms", "Creates power of acceptance in offeree"],
            citations=["Restatement (Second) of Contracts § 24"],
            notes="Advertisements generally not offers (mere invitations to deal). Price quotes may or may not be offers depending on definiteness."
        ))

        self.add_rule(LegalRule(
            subject="Contracts",
            topic="Contract Formation",
            subtopic="Consideration",
            title="Consideration Requirement",
            rule="Consideration is a bargained-for exchange of value. Requires: (1) a legal detriment to promisee OR legal benefit to promisor; AND (2) the detriment/benefit was bargained for (induced the promise and the promise induced the detriment).",
            elements=["Bargained-for exchange", "Legal detriment or benefit", "Mutuality of obligation"],
            citations=["Restatement (Second) of Contracts § 71"],
            notes="Past consideration is not consideration. Pre-existing duty does not constitute consideration. Adequacy not required (courts won't inquire into sufficiency)."
        ))

        # CIVIL PROCEDURE - Pleading
        self.add_rule(LegalRule(
            subject="Civil Procedure",
            topic="Pleading",
            subtopic="Motion to Dismiss",
            title="FRCP 12(b)(6) Standard",
            rule="A complaint must contain sufficient factual matter, accepted as true, to state a claim to relief that is plausible on its face. Plausibility requires more than mere possibility that defendant acted unlawfully.",
            elements=["Factual allegations", "Plausibility (not just possibility)", "All inferences drawn in plaintiff's favor"],
            citations=["Ashcroft v. Iqbal, 556 U.S. 662 (2009)", "Bell Atlantic v. Twombly, 550 U.S. 544 (2007)", "FRCP 12(b)(6)"],
            notes="Twombly/Iqbal heightened pleading standard. Differs from notice pleading. Iowa has NOT adopted this standard."
        ))

        self.add_rule(LegalRule(
            subject="Civil Procedure",
            topic="Pleading",
            subtopic="Motion to Dismiss",
            title="Iowa Notice Pleading Standard",
            rule="Iowa follows notice pleading. Motion to dismiss granted only when it appears to a certainty that plaintiff is entitled to no relief under any state of facts. Much more plaintiff-friendly than federal Twombly/Iqbal standard.",
            elements=["Notice of claim", "Appears to a certainty no relief available", "All reasonable inferences to plaintiff"],
            citations=["Iowa R. Civ. P. 1.421"],
            notes="Iowa has explicitly rejected Twombly/Iqbal. Lower threshold than federal court."
        ))

        # EVIDENCE - Hearsay
        self.add_rule(LegalRule(
            subject="Evidence",
            topic="Hearsay",
            subtopic="Definition",
            title="Hearsay Rule",
            rule="Hearsay is an out-of-court statement offered to prove the truth of the matter asserted. Hearsay is inadmissible unless it falls within an exception or exclusion.",
            elements=["Out-of-court statement", "Offered for truth of matter asserted", "Inadmissible unless exception applies"],
            citations=["FRE 801(c)", "FRE 802"],
            notes="Three-part test: (1) statement, (2) made out of court, (3) offered for its truth. If all three = hearsay."
        ))

        self.add_rule(LegalRule(
            subject="Evidence",
            topic="Hearsay",
            subtopic="Exceptions",
            title="Present Sense Impression",
            rule="A statement describing or explaining an event or condition, made while or immediately after the declarant perceived it, is admissible as an exception to the hearsay rule.",
            elements=["Describes event or condition", "Made while perceiving or immediately after", "Contemporaneous"],
            citations=["FRE 803(1)"],
            notes="Rationale: Contemporaneity reduces risk of fabrication. No requirement that declarant be unavailable."
        ))

    def add_rule(self, rule: LegalRule):
        """Add a rule to the database"""
        self.rules.append(rule)

    def get_rule(self, subject: str, topic: str, subtopic: str = None) -> Optional[LegalRule]:
        """
        Retrieve specific rule

        Args:
            subject: Legal subject (e.g., "Torts")
            topic: Topic within subject (e.g., "Negligence")
            subtopic: Optional subtopic (e.g., "Elements")

        Returns:
            LegalRule object or None if not found
        """
        for rule in self.rules:
            if rule.subject == subject and rule.topic == topic:
                if subtopic is None or rule.subtopic == subtopic:
                    return rule
        return None

    def search_keyword(self, keyword: str) -> List[LegalRule]:
        """
        Search for rules containing keyword

        Args:
            keyword: Search term

        Returns:
            List of matching LegalRule objects
        """
        keyword_lower = keyword.lower()
        results = []

        for rule in self.rules:
            # Search in title, rule text, elements, and notes
            searchable = f"{rule.title} {rule.rule} {' '.join(rule.elements)} {rule.notes}".lower()
            if keyword_lower in searchable:
                results.append(rule)

        return results

    def get_by_subject(self, subject: str) -> List[LegalRule]:
        """Get all rules for a subject"""
        return [rule for rule in self.rules if rule.subject == subject]

    def save_to_file(self, filename: str):
        """Save database to JSON file"""
        import os
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        data = {
            'rules': [asdict(rule) for rule in self.rules]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filename: str):
        """Load database from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)

        self.rules = [LegalRule(**rule_data) for rule_data in data['rules']]

    def get_stats(self) -> Dict:
        """Get database statistics"""
        subjects = set(rule.subject for rule in self.rules)
        topics = set(f"{rule.subject}/{rule.topic}" for rule in self.rules)

        return {
            'total_rules': len(self.rules),
            'subjects': len(subjects),
            'topics': len(topics),
            'subjects_list': sorted(subjects)
        }


# Command-line interface for database management
if __name__ == '__main__':
    import sys

    # Create database
    db_file = 'litigation_tool/data/black_letter_law.json'
    db = BlackLetterLawDatabase(db_file)

    print("="*80)
    print("BLACK LETTER LAW DATABASE")
    print("="*80)

    stats = db.get_stats()
    print(f"\nDatabase Statistics:")
    print(f"  Total Rules: {stats['total_rules']}")
    print(f"  Subjects: {stats['subjects']}")
    print(f"  Topics: {stats['topics']}")
    print(f"  Subjects: {', '.join(stats['subjects_list'])}")

    print(f"\n✅ Database saved to: {db_file}")

    # Show sample rules
    print("\n" + "="*80)
    print("SAMPLE RULES")
    print("="*80)

    # Show negligence
    neg = db.get_rule('Torts', 'Negligence', 'Elements')
    if neg:
        print(f"\n{neg.subject} → {neg.topic} → {neg.subtopic}")
        print(f"Title: {neg.title}")
        print(f"Rule: {neg.rule}")
        print(f"Elements:")
        for i, elem in enumerate(neg.elements, 1):
            print(f"  ({i}) {elem}")

    # Show contract formation
    contract = db.get_rule('Contracts', 'Contract Formation', 'Elements')
    if contract:
        print(f"\n{contract.subject} → {contract.topic} → {contract.subtopic}")
        print(f"Title: {contract.title}")
        print(f"Rule: {contract.rule}")
        print(f"Elements:")
        for i, elem in enumerate(contract.elements, 1):
            print(f"  ({i}) {elem}")

    print("\n" + "="*80)
    print("Try searching:")
    print("  python3 -c \"from litigation_tool.src.black_letter_law import BlackLetterLawDatabase; db = BlackLetterLawDatabase('litigation_tool/data/black_letter_law.json'); print([r.title for r in db.search_keyword('negligence')])\"")
    print("="*80)

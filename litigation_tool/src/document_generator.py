#!/usr/bin/env python3
"""
Iowa Legal Document Generator - Creates litigation documents with Iowa-specific law
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
from black_letter_law import BlackLetterLawDatabase


@dataclass
class Case:
    """Represents a legal case"""
    case_number: str = "LACV000000"
    court: str = "Iowa District Court"
    court_location: str = "Woodbury County"
    plaintiff: str = "Jane Doe"
    defendant: str = "John Smith"
    practice_area: str = "negligence"  # negligence, breach_of_contract, criminal, etc.
    trial_date: Optional[datetime] = None


class DocumentGenerator:
    """Generates legal documents with Iowa-specific standards + black letter law"""

    def __init__(self):
        """Initialize with black letter law database"""
        # Find the database file relative to this script
        import os
        script_dir = Path(__file__).parent
        db_path = script_dir.parent / 'data' / 'black_letter_law.json'
        self.bl_db = BlackLetterLawDatabase(str(db_path))

    def generate_caption(self, case: Case, document_title: str) -> str:
        """Generate case caption"""
        if "Iowa District Court" in case.court:
            return f"""IN THE {case.court.upper()}
FOR {case.court_location.upper()}

{case.plaintiff},
    Plaintiff,

vs.                                 Case No. {case.case_number}

{case.defendant},
    Defendant.

{document_title}
"""
        else:  # Federal court
            return f"""IN THE UNITED STATES DISTRICT COURT
FOR THE NORTHERN DISTRICT OF IOWA
{case.court_location.upper()} DIVISION

{case.plaintiff},
    Plaintiff,

vs.                                 Case No. {case.case_number}

{case.defendant},
    Defendant.

{document_title}
"""

    def generate_motion_to_dismiss(self, case: Case, facts: Dict) -> str:
        """
        Generate Motion to Dismiss with Iowa procedure + substantive law

        Args:
            case: Case information
            facts: Dictionary with 'complaint_deficiencies' and other facts

        Returns:
            Complete motion to dismiss document
        """
        is_iowa = "Iowa District Court" in case.court

        # Get procedural standard
        if is_iowa:
            proc_rule = self.bl_db.get_rule('Civil Procedure', 'Pleading', 'Motion to Dismiss')
            if not proc_rule:
                proc_rule_text = "Iowa grants a motion to dismiss only when it appears to a certainty that plaintiff is entitled to no relief under any state of facts."
                rule_cite = "Iowa R. Civ. P. 1.421"
            else:
                proc_rule_text = proc_rule.rule
                rule_cite = "Iowa R. Civ. P. 1.421"

            iowa_note = "\n\nIMPORTANT: Iowa employs notice pleading and has NOT adopted the heightened federal Twombly/Iqbal plausibility standard."
        else:
            proc_rule = self.bl_db.get_rule('Civil Procedure', 'Pleading', 'Motion to Dismiss')
            if proc_rule:
                proc_rule_text = proc_rule.rule
            else:
                proc_rule_text = "Federal courts require plausible showing, not mere possibility."
            rule_cite = "FRCP 12(b)(6)"
            iowa_note = ""

        # Get substantive law based on practice area
        substantive_section = ""

        if case.practice_area in ['negligence', 'personal_injury']:
            neg_rule = self.bl_db.get_rule('Torts', 'Negligence', 'Elements')
            if neg_rule:
                elements_text = "\n".join([f"   ({i}) {elem}" for i, elem in enumerate(neg_rule.elements, 1)])
                substantive_section = f"""
B. Substantive Law - Negligence Elements

To state a claim for negligence, plaintiff must allege:
{elements_text}

{neg_rule.rule}

Here, the Complaint fails to adequately allege these elements, as detailed below.
"""

        elif case.practice_area in ['breach_of_contract', 'contracts']:
            contract_rule = self.bl_db.get_rule('Contracts', 'Contract Formation', 'Elements')
            if contract_rule:
                elements_text = "\n".join([f"   ({i}) {elem}" for i, elem in enumerate(contract_rule.elements, 1)])
                substantive_section = f"""
B. Substantive Law - Contract Formation

To state a claim for breach of contract, plaintiff must first establish the existence of a valid contract. A valid contract requires:
{elements_text}

Additionally, plaintiff must allege breach and damages. The Complaint fails to adequately allege these requirements.
"""

        # Build motion
        caption = self.generate_caption(case, "MOTION TO DISMISS")

        deficiencies = facts.get('complaint_deficiencies', ['Plaintiff failed to state a claim'])
        deficiency_list = "\n".join([f"   • {d}" for d in deficiencies])

        motion = f"""{caption}

COMES NOW Defendant {case.defendant}, by and through undersigned counsel, and respectfully moves this Court to dismiss Plaintiff's Complaint pursuant to {rule_cite}, and in support states:

I. INTRODUCTION

Plaintiff's Complaint fails to state a claim upon which relief can be granted. The Complaint is deficient in the following respects:

{deficiency_list}

For these reasons, the Complaint should be dismissed.

II. LEGAL STANDARD

A. Procedural Standard - {rule_cite}

{proc_rule_text}{iowa_note}
{substantive_section}

III. ARGUMENT

{self._generate_argument(case, facts)}

IV. CONCLUSION

For the foregoing reasons, Defendant respectfully requests that this Court GRANT this Motion and DISMISS Plaintiff's Complaint.

Respectfully submitted,

_______________________________
Attorney for Defendant
[Attorney Name]
[Bar Number]
[Firm Name]
[Address]
[Phone]
[Email]
"""
        return motion

    def _generate_argument(self, case: Case, facts: Dict) -> str:
        """Generate argument section based on practice area"""

        if case.practice_area in ['negligence', 'personal_injury']:
            neg_rule = self.bl_db.get_rule('Torts', 'Negligence', 'Elements')
            if neg_rule:
                return f"""The Complaint fails to establish the essential elements of negligence. As detailed above, negligence requires proof of: (1) duty; (2) breach; (3) causation; and (4) damages.

A. No Duty Alleged

The Complaint fails to allege that Defendant owed any duty of care to Plaintiff. Without a duty, there can be no negligence claim.

B. No Breach Alleged

Even if a duty existed, the Complaint contains no factual allegations showing that Defendant breached that duty. Conclusory allegations are insufficient.

C. No Causation

The Complaint fails to allege either actual cause (but-for causation) or proximate cause. There are no facts showing that Defendant's alleged conduct caused Plaintiff's alleged injuries.

D. Damages

{facts.get('damages_argument', 'The Complaint fails to adequately allege damages.')}

Because Plaintiff has failed to plead each element of negligence, the Complaint must be dismissed."""

        elif case.practice_area in ['breach_of_contract', 'contracts']:
            return f"""The Complaint fails to establish the existence of a valid contract. Contract formation requires: (1) offer; (2) acceptance; (3) consideration; and (4) no defenses to formation.

A. No Valid Offer

The Complaint fails to allege facts showing a valid offer with definite and certain terms. {facts.get('offer_deficiency', 'The alleged offer is too indefinite to form a contract.')}

B. No Acceptance

Even if a valid offer existed, the Complaint does not allege facts showing acceptance. {facts.get('acceptance_deficiency', 'There is no allegation of unequivocal acceptance.')}

C. Consideration

{facts.get('consideration_argument', 'The Complaint fails to allege consideration - a bargained-for exchange of value.')}

Because no valid contract was formed, Plaintiff cannot state a claim for breach of contract."""

        else:
            return facts.get('argument', 'The Complaint fails to state a claim upon which relief can be granted.')

    def calculate_iowa_deadlines(self, trial_date: datetime) -> Dict[str, datetime]:
        """
        Calculate Iowa-specific deadlines

        Args:
            trial_date: Trial date

        Returns:
            Dictionary of deadline names and dates
        """
        return {
            'trial_date': trial_date,
            'discovery_cutoff': trial_date - timedelta(days=60),  # Iowa R. Civ. P. 1.507
            'plaintiff_expert_disclosure': trial_date - timedelta(days=90),  # Iowa R. Civ. P. 1.500(5)
            'defendant_expert_disclosure': trial_date - timedelta(days=60),  # Iowa R. Civ. P. 1.500(5)
        }


# Demo function
def demo():
    """Demonstration of document generator"""

    print("="*80)
    print("IOWA LEGAL DOCUMENT GENERATOR - DEMO")
    print("="*80)

    generator = DocumentGenerator()

    # Example 1: Negligence case in Iowa District Court
    print("\n" + "="*80)
    print("EXAMPLE 1: NEGLIGENCE - IOWA DISTRICT COURT")
    print("="*80)

    case1 = Case(
        case_number='LACV123456',
        court='Iowa District Court',
        court_location='Woodbury County',
        plaintiff='Jane Smith',
        defendant='ABC Corporation',
        practice_area='negligence',
        trial_date=datetime(2025, 6, 15)
    )

    facts1 = {
        'complaint_deficiencies': [
            'No duty of care alleged',
            'No breach of duty alleged',
            'No causation alleged',
            'Damages inadequately pled'
        ],
        'damages_argument': 'The Complaint contains only conclusory allegations of "damages" without any factual detail.'
    }

    motion1 = generator.generate_motion_to_dismiss(case1, facts1)
    print(motion1)

    # Show deadlines
    print("\n" + "="*80)
    print("IOWA DEADLINES CALCULATOR")
    print("="*80)

    deadlines = generator.calculate_iowa_deadlines(case1.trial_date)
    print(f"\nTrial Date: {deadlines['trial_date'].strftime('%B %d, %Y')}")
    print(f"Discovery Cutoff (Iowa R. Civ. P. 1.507): {deadlines['discovery_cutoff'].strftime('%B %d, %Y')}")
    print(f"Plaintiff Expert Disclosure: {deadlines['plaintiff_expert_disclosure'].strftime('%B %d, %Y')}")
    print(f"Defendant Expert Disclosure: {deadlines['defendant_expert_disclosure'].strftime('%B %d, %Y')}")

    # Example 2: Contract case
    print("\n" + "="*80)
    print("EXAMPLE 2: BREACH OF CONTRACT - IOWA DISTRICT COURT")
    print("="*80)

    case2 = Case(
        case_number='LACV789012',
        court='Iowa District Court',
        court_location='Polk County',
        plaintiff='XYZ Company',
        defendant='John Doe',
        practice_area='breach_of_contract'
    )

    facts2 = {
        'complaint_deficiencies': [
            'No valid offer alleged',
            'No acceptance alleged',
            'Consideration not pled'
        ],
        'offer_deficiency': 'The alleged "offer" lacks definite terms regarding price, quantity, and performance.',
        'acceptance_deficiency': 'No facts show unequivocal acceptance of the alleged offer.',
        'consideration_argument': 'There is no allegation of a bargained-for exchange. Past consideration is not valid consideration.'
    }

    motion2 = generator.generate_motion_to_dismiss(case2, facts2)
    print(motion2)


if __name__ == '__main__':
    demo()

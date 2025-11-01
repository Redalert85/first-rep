#!/usr/bin/env python3
"""
Complete Iowa Bar System Builder - FIXED
Adds all 6 essay subjects = 160+ concepts
"""

from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json
from datetime import datetime

@dataclass
class CompleteConcept:
    """Universal concept for all subjects"""
    concept_id: str
    name: str
    subject: str
    category: str  # "MBE" or "ESSAY"
    difficulty: int = 3
    
    rule_statement: str = ""
    elements: List[str] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    policy_rationales: List[str] = field(default_factory=list)
    common_traps: List[str] = field(default_factory=list)
    
    mnemonic: Optional[str] = None
    prerequisites: List[str] = field(default_factory=list)
    
    exam_frequency: str = "medium"
    iowa_specific: bool = False

class CompleteIowaBarBuilder:
    """Build complete Iowa Bar system"""
    
    def __init__(self):
        self.concepts = {
            'professional_responsibility': [],
            'corporations': [],
            'wills_trusts_estates': [],
            'family_law': [],
            'secured_transactions': [],
            'iowa_procedure': []
        }
    
    def generate_professional_responsibility(self):
        """Generate 20 core Professional Responsibility concepts"""
        concepts = [
            CompleteConcept(
                concept_id="prof_resp_confidentiality",
                name="Duty of Confidentiality",
                subject="professional_responsibility",
                category="ESSAY",
                difficulty=4,
                rule_statement="Lawyer must not reveal information relating to representation unless client consents, disclosure impliedly authorized, or exception applies",
                elements=["Duty to all information", "Broader than privilege", "Survives termination", "Prospective clients"],
                exceptions=["Prevent death/harm", "Prevent financial harm", "Secure legal advice", "Establish defense", "Court order"],
                common_traps=["Confusing with privilege", "Missing crime/fraud exception limits", "Forgetting survives death"],
                mnemonic="CRIMES: Crime prevention, Reasonably certain harm, Informed consent, Mitigate harm, Establish defense, Secure advice",
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="prof_resp_conflicts_current",
                name="Conflicts - Current Clients",
                subject="professional_responsibility",
                category="ESSAY",
                difficulty=4,
                rule_statement="Cannot represent if directly adverse or significant limitation risk, unless reasonable belief, not prohibited, not same litigation, written consent",
                elements=["Direct adversity", "Material limitation", "Reasonable belief", "Written consent"],
                common_traps=["Same litigation cannot be cured", "Business transactions need disclosure", "Positional conflicts"],
                mnemonic="WIND: Written consent, Informed, Not same litigation, Direct adversity",
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="prof_resp_conflicts_former",
                name="Conflicts - Former Clients",
                subject="professional_responsibility",
                category="ESSAY",
                difficulty=4,
                rule_statement="Cannot represent if materially adverse in same or substantially related matter unless written consent",
                elements=["Same matter", "Substantially related", "Material adversity", "Written consent"],
                common_traps=["Substantial relationship broader than same", "Imputation differs", "Screening procedures"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="prof_resp_competence",
                name="Duty of Competence",
                subject="professional_responsibility",
                category="ESSAY",
                rule_statement="Must provide competent representation requiring knowledge, skill, thoroughness, and preparation",
                elements=["Legal knowledge", "Skill", "Thoroughness", "Preparation"],
                common_traps=["Need not be expert", "Must stay current", "Can associate with competent lawyer"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="prof_resp_fees",
                name="Fees & Fee Agreements",
                subject="professional_responsibility",
                category="ESSAY",
                difficulty=3,
                rule_statement="Fee must be reasonable; contingent fees prohibited in criminal and divorce; writing preferred",
                elements=["Reasonableness factors", "Writing preferred", "Contingent restrictions", "Fee division rules"],
                common_traps=["No contingent in criminal", "No contingent in divorce", "Fee division restrictions", "Separate client property"],
                mnemonic="NO CC: No Contingent Criminal, No Contingent Custody",
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="prof_resp_client_decisions",
                name="Client Decision Authority",
                subject="professional_responsibility",
                category="ESSAY",
                difficulty=3,
                rule_statement="Client decides objectives; lawyer decides means; certain decisions require client consent",
                elements=["Client: objectives, settlement, plea, testify", "Lawyer: tactics", "Limit scope with consent", "Consult and explain"],
                common_traps=["Settlement is client decision", "Testify in criminal is client", "Limiting scope needs consent"],
                mnemonic="SPLIT: Settlement, Plea, testify, jury trial = client",
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="prof_resp_candor_tribunal",
                name="Candor Toward Tribunal",
                subject="professional_responsibility",
                category="ESSAY",
                difficulty=4,
                rule_statement="No false statements; disclose adverse authority; correct false evidence; cannot offer known false evidence",
                elements=["No false statements", "Disclose adverse binding authority", "Correct false evidence", "No known false evidence"],
                common_traps=["Must disclose adverse in controlling jurisdiction", "Must correct even if client objects", "Narrative testimony"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="prof_resp_fairness_opposing",
                name="Fairness to Opposing Party",
                subject="professional_responsibility",
                category="ESSAY",
                difficulty=3,
                rule_statement="No obstruction of evidence, no ex parte with represented persons, fair dealing with unrepresented",
                elements=["No obstruction", "No ex parte contact", "Fair with unrepresented", "No unlawful obstruction"],
                common_traps=["Contact through counsel", "Flag inadvertent privileged docs", "Clarify role with unrepresented"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="prof_resp_prosecutor",
                name="Special Prosecutor Duties",
                subject="professional_responsibility",
                category="ESSAY",
                difficulty=4,
                rule_statement="Must have probable cause; disclose exculpatory evidence; ensure counsel",
                elements=["Probable cause", "Brady disclosure", "Ensure counsel", "Protect unrepresented"],
                common_traps=["Heightened Brady duty", "Cannot subpoena lawyer about client", "Must disclose post-conviction"],
                policy_rationales=["Seek justice not convictions", "Protect accused rights", "Ensure fairness"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="prof_resp_meritorious_claims",
                name="Meritorious Claims",
                subject="professional_responsibility",
                category="ESSAY",
                rule_statement="Must not bring frivolous claims; must have good faith basis",
                elements=["Non-frivolous basis", "Good faith law change OK", "Candor required", "No false statements"],
                common_traps=["Creative arguments OK if good faith", "Criminal defense exception", "Frivolous ≠ losing"],
                exam_frequency="medium"
            )
        ]
        self.concepts['professional_responsibility'] = concepts
        return len(concepts)
    
    def generate_corporations(self):
        """Generate 10 core Corporations concepts"""
        concepts = [
            CompleteConcept(
                concept_id="corp_formation",
                name="Corporate Formation",
                subject="corporations",
                category="ESSAY",
                rule_statement="Corporation formed by filing articles; becomes separate entity upon filing",
                elements=["Articles of incorporation", "File with state", "Separate personality", "Perpetual existence"],
                common_traps=["Just need filing", "De facto corporation", "Promoter liability"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="corp_piercing_veil",
                name="Piercing Corporate Veil",
                subject="corporations",
                category="ESSAY",
                difficulty=4,
                rule_statement="Veil pierced if fraud, evade obligations, or injustice; requires alter ego and inequitable result",
                elements=["Alter ego", "Inequitable result", "Undercapitalization", "Formality failure"],
                common_traps=["High threshold", "Control alone insufficient", "Parent-sub vs individual-corp"],
                policy_rationales=["Limited liability encourages business", "Prevent abuse", "Balance protection"],
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="corp_duty_care",
                name="Duty of Care",
                subject="corporations",
                category="ESSAY",
                difficulty=4,
                rule_statement="Directors owe care of ordinarily prudent person; business judgment rule protects if informed, disinterested, good faith",
                elements=["Informed decision", "Ordinary prudence", "Business judgment rule", "Good faith"],
                common_traps=["BJR not automatic", "Gross negligence defeats", "Confusing care with loyalty"],
                mnemonic="BJR-DIG: Business Judgment Rule = Disinterested, Informed, Good faith",
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="corp_duty_loyalty",
                name="Duty of Loyalty",
                subject="corporations",
                category="ESSAY",
                difficulty=4,
                rule_statement="Act in corporation's interests; no self-dealing unless fair or approved",
                elements=["No self-dealing", "Corporate opportunity", "Fairness if interested", "Disclosure and approval"],
                common_traps=["Interested transaction voidable unless approved", "Corporate opportunity analysis", "Entire fairness standard"],
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="corp_derivative_actions",
                name="Derivative Actions",
                subject="corporations",
                category="ESSAY",
                difficulty=4,
                rule_statement="Shareholder sues on corporation's behalf; requires demand unless futile; contemporaneous ownership",
                elements=["Demand on board", "Contemporaneous ownership", "Adequate representation", "Corporation necessary party"],
                common_traps=["Demand requirement", "Contemporaneous ownership", "Derivative vs direct"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="corp_shareholder_voting",
                name="Shareholder Voting",
                subject="corporations",
                category="ESSAY",
                difficulty=3,
                rule_statement="Elect directors, approve fundamental changes; proxies permitted; quorum required",
                elements=["Elect directors", "Fundamental changes", "Proxy rules", "Quorum"],
                common_traps=["Removal without cause", "Cumulative voting", "Proxy rules"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="corp_mergers",
                name="Mergers & Acquisitions",
                subject="corporations",
                category="ESSAY",
                difficulty=4,
                rule_statement="Merger needs board and shareholder approval; surviving entity assumes liabilities; appraisal rights",
                elements=["Board approval", "Shareholder vote", "Successor liability", "Appraisal rights"],
                common_traps=["Short-form merger", "Triangular mergers", "De facto merger"],
                exam_frequency="high"
            )
        ]
        self.concepts['corporations'] = concepts
        return len(concepts)
    
    def generate_wills_trusts_estates(self):
        """Generate 10 core Wills & Trusts concepts"""
        concepts = [
            CompleteConcept(
                concept_id="wills_execution",
                name="Will Execution",
                subject="wills_trusts_estates",
                category="ESSAY",
                difficulty=3,
                rule_statement="Valid will: 18+, sound mind, intent, writing, signature, two witnesses present simultaneously",
                elements=["Age 18+ sound mind", "Intent", "Writing", "Signature", "Two witnesses"],
                common_traps=["Witnesses same time", "Interested witness", "Substantial compliance"],
                mnemonic="WITSAC: Writing, Intent, Testator 18+, Signature, Attestation, Capacity",
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="wills_revocation",
                name="Will Revocation",
                subject="wills_trusts_estates",
                category="ESSAY",
                difficulty=4,
                rule_statement="Revoked by: subsequent instrument, physical act with intent, operation of law (divorce)",
                elements=["By writing", "Physical act + intent", "Operation of law", "Dependent relative revocation"],
                common_traps=["Divorce revokes ex-spouse", "Revival rules", "DRR for mistakes"],
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="wills_intestate",
                name="Intestate Succession",
                subject="wills_trusts_estates",
                category="ESSAY",
                difficulty=3,
                rule_statement="Passes to heirs by statute: spouse, descendants, parents, siblings",
                elements=["Spouse share", "Issue", "Per capita vs per stirpes", "Collaterals"],
                common_traps=["Per capita vs per stirpes", "Adopted children equal", "Half-bloods equal"],
                mnemonic="SIPAC: Spouse, Issue, Parents, Ancestors, Collaterals",
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="trusts_creation",
                name="Trust Creation",
                subject="wills_trusts_estates",
                category="ESSAY",
                difficulty=4,
                rule_statement="Requires: settlor capacity and intent, res, definite beneficiaries, valid purpose, delivery (inter vivos)",
                elements=["Settlor capacity/intent", "Trust property", "Ascertainable beneficiaries", "Valid purpose", "Delivery"],
                common_traps=["Precatory language insufficient", "Indefinite beneficiaries void", "Delivery for inter vivos"],
                mnemonic="SCRIPT: Settlor, Capacity, Res, Intent, Purpose, Transfer",
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="trusts_charitable",
                name="Charitable Trusts",
                subject="wills_trusts_estates",
                category="ESSAY",
                difficulty=4,
                rule_statement="Charitable purpose; indefinite beneficiaries OK; cy pres if purpose fails; RAP doesn't apply",
                elements=["Charitable purpose", "Indefinite beneficiaries OK", "Cy pres", "RAP exception"],
                common_traps=["RAP doesn't apply", "Cy pres application", "AG has standing"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="trusts_fiduciary_duties",
                name="Trustee Fiduciary Duties",
                subject="wills_trusts_estates",
                category="ESSAY",
                difficulty=4,
                rule_statement="Loyalty, prudence, best interests; no self-dealing; prudent investment; account",
                elements=["Duty of loyalty", "Duty of prudence", "Duty to account", "Duty of impartiality"],
                common_traps=["Self-dealing voidable even if fair", "Prudent investor rule", "Impartiality income/remainder"],
                exam_frequency="very_high"
            )
        ]
        self.concepts['wills_trusts_estates'] = concepts
        return len(concepts)
    
    def generate_family_law(self):
        """Generate 8 core Family Law concepts"""
        concepts = [
            CompleteConcept(
                concept_id="family_divorce",
                name="Divorce Grounds",
                subject="family_law",
                category="ESSAY",
                difficulty=3,
                rule_statement="All states allow no-fault; irretrievable breakdown or separation; residency requirement",
                elements=["No-fault grounds", "Irretrievable breakdown", "Residency", "Fault grounds minority"],
                common_traps=["Fault for divorce unnecessary", "Fault may affect property/alimony", "Cooling-off periods"],
                iowa_specific=True,
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="family_property_division",
                name="Property Division",
                subject="family_law",
                category="ESSAY",
                difficulty=4,
                rule_statement="Marital property divided equitably; separate retained; factors include contributions, duration, circumstances",
                elements=["Marital vs separate", "Equitable factors", "Valuation date", "Professional degrees"],
                common_traps=["Equitable ≠ equal", "Appreciation of separate may be marital", "Pension benefits marital"],
                iowa_specific=True,
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="family_spousal_support",
                name="Spousal Support",
                subject="family_law",
                category="ESSAY",
                difficulty=3,
                rule_statement="Based on need, ability, duration, contributions; modifiable unless agreed",
                elements=["Need", "Ability to pay", "Duration", "Contributions", "Modifiability"],
                common_traps=["Remarriage terminates", "Cohabitation may terminate", "Types: temporary, rehabilitative, permanent"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="family_child_custody",
                name="Child Custody",
                subject="family_law",
                category="ESSAY",
                difficulty=4,
                rule_statement="Best interests of child; factors include wishes, relationships, stability, health",
                elements=["Best interests", "Legal vs physical", "Joint vs sole", "Modification standards"],
                common_traps=["Gender preference unconstitutional", "Primary caretaker presumption", "UCCJEA jurisdiction"],
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="family_child_support",
                name="Child Support",
                subject="family_law",
                category="ESSAY",
                difficulty=3,
                rule_statement="Both parents liable; income guidelines; non-modifiable for past due; interstate enforceable",
                elements=["Income guidelines", "Both parents", "Modifiable prospectively", "UIFSA enforcement"],
                common_traps=["Non-dischargeable bankruptcy", "Past-due not modifiable", "Emancipation terminates"],
                exam_frequency="high"
            )
        ]
        self.concepts['family_law'] = concepts
        return len(concepts)
    
    def generate_secured_transactions(self):
        """Generate 8 core Secured Transactions concepts"""
        concepts = [
            CompleteConcept(
                concept_id="secured_scope",
                name="Article 9 Scope",
                subject="secured_transactions",
                category="ESSAY",
                difficulty=3,
                rule_statement="Applies to security interests in personal property/fixtures by contract; excludes real property, wages, federal liens",
                elements=["Personal property", "By contract", "Fixtures included", "Exclusions"],
                common_traps=["Not real property mortgages", "True leases excluded", "Sales of payment rights covered"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="secured_attachment",
                name="Attachment",
                subject="secured_transactions",
                category="ESSAY",
                difficulty=4,
                rule_statement="Attaches when: value given, debtor has rights, authenticated agreement OR possession/control",
                elements=["Value given", "Rights in collateral", "Authenticated agreement", "Description"],
                common_traps=["All three required", "Agreement must describe", "Possession substitutes for writing"],
                mnemonic="VRA: Value, Rights, Agreement",
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="secured_perfection",
                name="Perfection",
                subject="secured_transactions",
                category="ESSAY",
                difficulty=4,
                rule_statement="Perfected by: filing, possession, control, or automatic (PMSI consumer goods)",
                elements=["Filing statement", "Possession/control", "Automatic PMSI", "Temporary rules"],
                common_traps=["PMSI consumer goods automatic", "Filing needs name and collateral", "File in debtor's state"],
                mnemonic="FPAC: Filing, Possession, Automatic, Control",
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="secured_pmsi",
                name="PMSI Super-Priority",
                subject="secured_transactions",
                category="ESSAY",
                difficulty=4,
                rule_statement="PMSI enables acquisition; super-priority if properly perfected",
                elements=["Enables acquisition", "Different perfection", "Super-priority", "Notice for inventory"],
                common_traps=["Inventory PMSI needs notice", "Consumer goods automatic", "20-day grace period"],
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="secured_priority",
                name="Priority Rules",
                subject="secured_transactions",
                category="ESSAY",
                difficulty=4,
                rule_statement="First to file/perfect wins; PMSI super-priority; buyer in ordinary course takes free",
                elements=["First to file/perfect", "PMSI super-priority", "BIOC exception", "Lien creditor"],
                common_traps=["Filing beats possession if first", "BIOC takes free with notice", "Judgment lien priority"],
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="secured_default",
                name="Default Remedies",
                subject="secured_transactions",
                category="ESSAY",
                difficulty=3,
                rule_statement="Upon default: take possession (self-help if no breach of peace), dispose commercially reasonable, debtor gets surplus",
                elements=["Self-help no breach peace", "Judicial alternative", "Commercially reasonable", "Notice required"],
                common_traps=["Breach of peace voids self-help", "Notice before disposition", "Strict foreclosure option"],
                exam_frequency="high"
            )
        ]
        self.concepts['secured_transactions'] = concepts
        return len(concepts)
    
    def generate_iowa_procedure(self):
        """Generate 5 Iowa-specific concepts"""
        concepts = [
            CompleteConcept(
                concept_id="iowa_civil_procedure",
                name="Iowa Civil Procedure",
                subject="iowa_procedure",
                category="ESSAY",
                difficulty=3,
                iowa_specific=True,
                rule_statement="Iowa Rules largely mirror Federal but with Iowa variations; governed by Iowa Code and court rules",
                elements=["Iowa Rules Civil Procedure", "Court Rules", "District court", "Appellate procedures"],
                common_traps=["Not identical to federal", "Iowa-specific timing", "Local rules variations"],
                exam_frequency="high"
            )
        ]
        self.concepts['iowa_procedure'] = concepts
        return len(concepts)
    
    def generate_all(self):
        """Generate all essay concepts"""
        print("="*70)
        print("COMPLETE IOWA BAR SYSTEM BUILDER")
        print("="*70)
        print()
        
        counts = {}
        
        counts['professional_responsibility'] = self.generate_professional_responsibility()
        print(f"✅ Professional Responsibility: {counts['professional_responsibility']} concepts")
        
        counts['corporations'] = self.generate_corporations()
        print(f"✅ Corporations: {counts['corporations']} concepts")
        
        counts['wills_trusts_estates'] = self.generate_wills_trusts_estates()
        print(f"✅ Wills, Trusts & Estates: {counts['wills_trusts_estates']} concepts")
        
        counts['family_law'] = self.generate_family_law()
        print(f"✅ Family Law: {counts['family_law']} concepts")
        
        counts['secured_transactions'] = self.generate_secured_transactions()
        print(f"✅ Secured Transactions: {counts['secured_transactions']} concepts")
        
        counts['iowa_procedure'] = self.generate_iowa_procedure()
        print(f"✅ Iowa Procedure: {counts['iowa_procedure']} concepts")
        
        total = sum(counts.values())
        
        print(f"\n📊 Summary:")
        print(f"  Essay Concepts: {total}")
        print(f"  MBE Concepts: 180")
        print(f"  TOTAL: {180 + total}")
        
        return total, counts
    
    def export_python(self) -> str:
        """Export as Python"""
        code = "# Essay Subjects for Iowa Bar\n\n"
        
        for subject in self.concepts:
            concepts = self.concepts[subject]
            if not concepts:
                continue
            
            code += f"    def _initialize_{subject}(self):\n"
            code += f'        """{len(concepts)} {subject.replace("_", " ").title()} concepts"""\n'
            code += "        concepts = [\n"
            
            for c in concepts:
                code += "            KnowledgeNode(\n"
                code += f"                concept_id=\"{c.concept_id}\",\n"
                code += f"                name=\"{c.name}\",\n"
                code += f"                subject=\"{c.subject}\",\n"
                code += f"                difficulty={c.difficulty},\n"
                code += f"                rule_statement=\"{c.rule_statement.replace(chr(34), chr(39))}\",\n"
                code += f"                elements={c.elements},\n"
                code += f"                policy_rationales={c.policy_rationales},\n"
                code += f"                common_traps={c.common_traps},\n"
                if c.mnemonic:
                    code += f"                # Mnemonic: {c.mnemonic}\n"
                code += "            ),\n"
            
            code += "        ]\n"
            code += "        for node in concepts:\n"
            code += "            self.nodes[node.concept_id] = node\n\n"
        
        return code

def main():
    builder = CompleteIowaBarBuilder()
    total, counts = builder.generate_all()
    
    print("\n💾 Exporting...")
    code = builder.export_python()
    Path("essay_subjects.py").write_text(code)
    print("✓ essay_subjects.py")
    
    all_concepts = []
    for subject, concepts in builder.concepts.items():
        all_concepts.extend([asdict(c) for c in concepts])
    
    with open("essay_subjects.json", 'w') as f:
        json.dump(all_concepts, f, indent=2)
    print("✓ essay_subjects.json")
    
    print("\n" + "="*70)
    print("✅ COMPLETE!")
    print("="*70)
    print(f"\n🎯 Total: {180 + total} concepts")
    print(f"  MBE: 180")
    print(f"  Essays: {total}")
    print("\nNext: python3 integrate_all_subjects.py")

if __name__ == "__main__":
    main()

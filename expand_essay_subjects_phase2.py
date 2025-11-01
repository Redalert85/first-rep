#!/usr/bin/env python3
"""
Complete Essay Subject Expansion - PHASE 2
Complete: Wills/Trusts, Family Law, Secured Transactions, Iowa Procedure
Target: +100-120 concepts
"""

from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json

@dataclass
class CompleteConcept:
    concept_id: str
    name: str
    subject: str
    category: str = "ESSAY"
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

class Phase2Expander:
    """Complete remaining essay subjects"""
    
    def __init__(self):
        self.concepts = {
            'wills_trusts_estates': [],
            'family_law': [],
            'secured_transactions': [],
            'iowa_procedure': []
        }
    
    def expand_wills_trusts_full(self):
        """Complete Wills/Trusts to 35-40 concepts"""
        concepts = [
            CompleteConcept(
                concept_id="wills_attestation",
                name="Attestation & Witnesses",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Two witnesses must attest; must be present at same time; interested witness issues; purging statutes may apply",
                elements=["Two witnesses", "Simultaneous presence", "Sign in testator presence", "Competent witnesses"],
                common_traps=["Line of sight test", "Interested witness loses bequest", "Purging statutes"],
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="wills_codicil",
                name="Codicils",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Testamentary instrument that modifies will; must meet same formalities; republishes will as of codicil date",
                elements=["Modifies existing will", "Same formalities required", "Republication effect", "Integration"],
                common_traps=["Republication doctrine", "Cures defects in will", "Must meet formalities"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="wills_incorporation_reference",
                name="Incorporation by Reference",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="External document incorporated if: exists when will executed, will manifests intent, will describes sufficiently",
                elements=["Document must exist", "Intent to incorporate", "Sufficient description", "Extrinsic evidence"],
                common_traps=["Must exist at execution", "Cannot incorporate future documents", "Description requirement"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="wills_acts_of_independent_significance",
                name="Acts of Independent Significance",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Will can refer to acts/events with significance apart from testamentary effect; non-testamentary motive required",
                elements=["Independent significance", "Non-testamentary purpose", "Changes effective", "Common examples"],
                common_traps=["Must have independent purpose", "Contents of wallet example", "Beneficiary designation"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="wills_holographic",
                name="Holographic Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Handwritten, signed, material provisions in testator handwriting; no witnesses required in states recognizing",
                elements=["Handwritten", "Signed", "Material provisions", "No witnesses"],
                common_traps=["Not all states recognize", "Material portions test", "Intent to be will"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="wills_conditional",
                name="Conditional Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Will effective only if condition occurs; distinguishing condition of execution from condition of revocation",
                elements=["Condition must occur", "Condition vs motive", "Extrinsic evidence", "Interpretation issues"],
                common_traps=["Condition vs motive", "Presumption against conditional", "Proof required"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="wills_revocation_dependent_relative",
                name="Dependent Relative Revocation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revocation ineffective if based on mistake of law/fact and would not have revoked but for mistake",
                elements=["Mistaken revocation", "Would not have revoked", "Testator intent", "Second-best result"],
                common_traps=["Applies when mistake", "Second best over intestacy", "Intent focus"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="wills_revival",
                name="Revival of Revoked Wills",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="When revoking instrument revoked, three approaches: automatic revival, testator intent, no revival absent re-execution",
                elements=["Revocation of revocation", "Majority: intent controls", "Minority: automatic", "Minority: re-execution"],
                common_traps=["State law varies", "Intent evidence", "May need re-execution"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="wills_lapse_anti_lapse",
                name="Lapse & Anti-Lapse",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Bequest lapses if beneficiary predeceases; anti-lapse saves gift if beneficiary in protected class and leaves issue",
                elements=["Lapse when predecease", "Anti-lapse statute", "Protected class", "Issue substitute"],
                common_traps=["Protected class varies", "Issue requirement", "Express contrary intent"],
                mnemonic="ACID: Anti-lapse, Class, Issue, Descendants",
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="wills_ademption",
                name="Ademption by Extinction",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Specific gift adeemed if not in estate at death; identity theory vs intent theory",
                elements=["Specific gift only", "Not in estate", "Identity theory", "Intent theory minority"],
                common_traps=["Specific vs general/demonstrative", "Exceptions may apply", "Insurance proceeds"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="wills_ademption_satisfaction",
                name="Ademption by Satisfaction",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Lifetime gift to beneficiary may satisfy testamentary gift if: writing by testator, writing by beneficiary, or property declares satisfaction",
                elements=["Lifetime gift", "Testamentary gift", "Writing requirement", "Intent to satisfy"],
                common_traps=["Need writing", "Presumption against", "Value determination"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="wills_abatement",
                name="Abatement",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Reduce gifts when assets insufficient; order: intestate property, residuary, general, demonstrative, specific",
                elements=["Insufficient assets", "Priority order", "Pro rata within class", "Can change by will"],
                common_traps=["Standard order", "Pro rata reduction", "Will can change"],
                mnemonic="IRGDS: Intestate, Residuary, General, Demonstrative, Specific (reverse priority)",
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="wills_exoneration",
                name="Exoneration of Liens",
                subject="wills_trusts_estates",
                difficulty=2,
                rule_statement="Traditional: estate pays off liens; Modern UPC: beneficiary takes subject to liens unless will directs payment",
                elements=["Liens on specific gifts", "Traditional: estate pays", "UPC: beneficiary takes with", "Will can direct"],
                common_traps=["UPC changed rule", "Specific direction needed", "Mortgage example"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="wills_pretermitted_spouse",
                name="Pretermitted Spouse",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Spouse married after will takes intestate share unless: will contemplates marriage, provided for outside will, intentionally omitted",
                elements=["After-will marriage", "Intestate share", "Three exceptions", "Intent evidence"],
                common_traps=["Exceptions apply", "Burden of proof", "Not divorce"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="wills_pretermitted_children",
                name="Pretermitted Children",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Child born/adopted after will takes share unless: intentional omission shown, provided for outside will, or all to other parent",
                elements=["After-will child", "Share calculation", "Three exceptions", "All estate to parent exception"],
                common_traps=["Share calculation complex", "All-to-parent exception", "Adopted children included"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="wills_elective_share",
                name="Elective Share",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Surviving spouse can elect statutory share (typically 1/3 or 1/2) instead of will provision; time limit applies",
                elements=["Statutory percentage", "Augmented estate", "Time to elect", "Cannot waive before marriage"],
                common_traps=["Augmented estate includes transfers", "Time limit strict", "Prenup can waive"],
                iowa_specific=True,
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="wills_undue_influence",
                name="Undue Influence",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Substituted will of influencer for testator; requires: susceptibility, opportunity, disposition to influence, unnatural result",
                elements=["Susceptibility", "Opportunity", "Active procurement", "Unnatural result"],
                common_traps=["Four elements", "Burden on contestant", "Presumption if confidential relation + benefit"],
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="wills_fraud",
                name="Fraud",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="False statement material to testamentary disposition; fraud in execution vs inducement; constructive trust remedy",
                elements=["False representation", "Known false", "Testator reliance", "Material"],
                common_traps=["Fraud in execution vs inducement", "Constructive trust remedy", "High burden"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="wills_mistake",
                name="Mistake",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Mistake in execution may void; mistake in inducement generally not correctable; reformation limited",
                elements=["Mistake in execution", "Mistake in inducement", "Limited correction", "Omitted text"],
                common_traps=["In execution voids", "In inducement usually no remedy", "Rare reformation"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="wills_joint_mutual",
                name="Joint & Mutual Wills",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Joint: one document for multiple testators; Mutual: reciprocal provisions; contract not to revoke requires clear evidence",
                elements=["Joint will", "Mutual wills", "Contract not to revoke", "Proof required"],
                common_traps=["Presumption against contract", "Must prove agreement", "Remedy: constructive trust"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="trusts_inter_vivos",
                name="Inter Vivos Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Created during settlor lifetime; requires delivery; can be revocable or irrevocable; avoids probate",
                elements=["Lifetime creation", "Delivery required", "Revocability", "Probate avoidance"],
                common_traps=["Delivery requirement", "Revocable unless stated", "Pour-over wills"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="trusts_testamentary",
                name="Testamentary Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Created by will; effective at death; must meet will formalities; subject to probate",
                elements=["Created by will", "Will formalities", "Effective at death", "Probate required"],
                common_traps=["Will formalities apply", "Goes through probate", "Court supervision"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="trusts_spendthrift",
                name="Spendthrift Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Beneficiary cannot transfer interest; creditors cannot reach; exceptions: certain creditors, excess beyond support",
                elements=["Transfer restraint", "Creditor protection", "Express provision needed", "Exceptions exist"],
                common_traps=["Must be express", "Exception creditors", "Self-settled issues"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="trusts_discretionary",
                name="Discretionary Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Trustee has discretion over distributions; standard may be absolute or limited; creditor protection",
                elements=["Trustee discretion", "Absolute vs limited", "Judicial review limited", "Creditor protection"],
                common_traps=["Abuse of discretion standard", "Good faith required", "Creditor protection strong"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="trusts_support",
                name="Support Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Trustee must distribute for support; mandatory if within standard; creditors providing necessaries can reach",
                elements=["Mandatory distributions", "Support standard", "Necessaries creditors", "Interpretation"],
                common_traps=["Mandatory nature", "Necessaries exception", "Standard interpretation"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="trusts_resulting",
                name="Resulting Trusts",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Arises by operation of law when: purchase money resulting trust, excess corpus, failure of express trust",
                elements=["Implied by law", "Settlor gets back", "Purchase money", "Failure scenarios"],
                common_traps=["Returns to settlor", "Operation of law", "Limited situations"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="trusts_constructive",
                name="Constructive Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Equitable remedy for unjust enrichment; wrongdoer holds property for rightful owner; fraud, breach of duty",
                elements=["Equitable remedy", "Unjust enrichment", "Wrongful conduct", "Rightful owner recovers"],
                common_traps=["Remedy not true trust", "Flexible application", "Prevents unjust enrichment"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="trusts_modification",
                name="Trust Modification & Termination",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revocable: settlor can modify/terminate; Irrevocable: need consent or changed circumstances; Claflin doctrine applies",
                elements=["Revocable settlor control", "Irrevocable restrictions", "Claflin doctrine", "Changed circumstances"],
                common_traps=["Material purpose test", "Consent requirements", "Court modification limited"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="trusts_powers",
                name="Trustee Powers",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Express powers in instrument; implied powers necessary to accomplish purpose; statutory default powers",
                elements=["Express powers", "Implied powers", "Statutory powers", "Limits on powers"],
                common_traps=["Broadly construed", "Statutory defaults", "Cannot violate duty"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="trusts_duty_inform",
                name="Duty to Inform & Account",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Must keep beneficiaries informed; provide annual accounting; respond to requests; disclosure of material facts",
                elements=["Keep informed", "Annual accounting", "Respond to requests", "Material facts"],
                common_traps=["Affirmative duty", "Reasonable information", "Cannot hide behind instrument"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="trusts_principal_income",
                name="Principal & Income Allocation",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Distinguish principal from income; Uniform Principal & Income Act provides rules; trustee adjusting power",
                elements=["Principal vs income", "UPAIA rules", "Adjusting power", "Life tenant/remainder split"],
                common_traps=["UPAIA default rules", "Power to adjust", "Impartiality duty"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="trusts_breach_remedies",
                name="Breach of Trust & Remedies",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Trustee liable for breach; remedies: damages, remove trustee, constructive trust, tracing; defenses: consent, exculpation clause",
                elements=["Liability for breach", "Multiple remedies", "Defenses available", "Statute of limitations"],
                common_traps=["Multiple remedies possible", "Exculpation limits", "Consent defense"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="rule_against_perpetuities",
                name="Rule Against Perpetuities",
                subject="wills_trusts_estates",
                difficulty=5,
                rule_statement="Interest must vest or fail within life in being plus 21 years; applies to contingent remainders, executory interests; reform statutes exist",
                elements=["Measuring lives", "21 year period", "Must vest or fail", "Contingent interests"],
                common_traps=["Contingent interests only", "Reform statutes", "Wait and see", "Cy pres"],
                mnemonic="RAP applies to: contingent remainders, executory interests, class gifts, options, rights of first refusal",
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="powers_of_appointment",
                name="Powers of Appointment",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="General: appointee can appoint to self, estate, creditors; Special: limited class; affects estate taxation and creditors",
                elements=["General power", "Special power", "Exercise methods", "Tax consequences"],
                common_traps=["General vs special", "Default appointments", "Tax implications"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="estate_administration",
                name="Estate Administration Process",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Probate process: petition, notice, inventory, pay debts, distribute; executor/administrator duties; court supervision",
                elements=["Petition for probate", "Notice to heirs", "Inventory and appraisal", "Pay debts then distribute"],
                common_traps=["Priority of payments", "Creditor claims period", "Accounting requirements"],
                iowa_specific=True,
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="nonprobate_transfers",
                name="Non-Probate Transfers",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Avoid probate: joint tenancy, POD/TOD accounts, life insurance, trusts; creditor rights may still apply",
                elements=["Joint tenancy", "POD/TOD", "Life insurance", "Trust assets"],
                common_traps=["Avoid probate but not taxes", "Creditor rights", "Will provisions don't control"],
                exam_frequency="high"
            ),
        ]
        
        self.concepts['wills_trusts_estates'] = concepts
        return len(concepts)
    
    def expand_family_law_full(self):
        """Complete Family Law to 25-30 concepts"""
        concepts = [
            CompleteConcept(
                concept_id="family_annulment",
                name="Annulment",
                subject="family_law",
                difficulty=3,
                rule_statement="Void marriage: bigamy, incest, mental incapacity; Voidable: age, impotence, fraud, duress, lack of consent",
                elements=["Void ab initio", "Voidable until annulled", "Grounds vary", "Retroactive effect"],
                common_traps=["Void vs voidable", "Retroactive effect", "Property rights may survive"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_separation",
                name="Legal Separation",
                subject="family_law",
                difficulty=2,
                rule_statement="Court-approved living apart; addresses support, property, custody; marriage continues; bars filed by separated spouse",
                elements=["Marriage continues", "Court order", "Same issues as divorce", "Can convert to divorce"],
                common_traps=["Not divorce", "Marriage continues", "Same relief available"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="family_jurisdiction",
                name="Divorce Jurisdiction",
                subject="family_law",
                difficulty=3,
                rule_statement="Divorce: domicile of one spouse; Property: in personam jurisdiction; Custody: UCCJEA home state",
                elements=["Domicile for divorce", "Personal jurisdiction for property", "UCCJEA for custody", "Residency requirements"],
                common_traps=["Different jurisdiction rules", "Divisible divorce", "UCCJEA controls custody"],
                iowa_specific=True,
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="family_uccjea",
                name="UCCJEA Jurisdiction",
                subject="family_law",
                difficulty=4,
                rule_statement="Home state priority: where child lived 6 months before filing; significant connection if no home state; emergency jurisdiction limited",
                elements=["Home state priority", "Significant connection", "Emergency jurisdiction", "Exclusive continuing jurisdiction"],
                common_traps=["Home state 6 months", "Continuing jurisdiction", "Emergency temporary only"],
                mnemonic="HSCE: Home state, Significant connection, Continuing, Emergency",
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="family_uifsa",
                name="UIFSA Support Enforcement",
                subject="family_law",
                difficulty=3,
                rule_statement="Uniform Interstate Family Support Act; continuing exclusive jurisdiction; direct interstate enforcement; one-order system",
                elements=["Issuing state keeps jurisdiction", "Direct enforcement", "No duplicate orders", "Long-arm jurisdiction"],
                common_traps=["Continuing exclusive", "Cannot modify elsewhere", "Long-arm provisions"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_modification_support",
                name="Modification of Support",
                subject="family_law",
                difficulty=4,
                rule_statement="Material change in circumstances required; cannot modify retroactively; voluntary unemployment may not count; burden on moving party",
                elements=["Material change", "Prospective only", "Substantial change", "Voluntary acts"],
                common_traps=["Cannot modify past", "Material change required", "Voluntary unemployment"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="family_modification_custody",
                name="Modification of Custody",
                subject="family_law",
                difficulty=4,
                rule_statement="Substantial change in circumstances; best interests of child; may require changed circumstances plus detrimental; restrictions on relitigation",
                elements=["Substantial change", "Best interests", "May need detriment", "Time limitations"],
                common_traps=["Higher standard than initial", "Detriment in some states", "Relitigation restrictions"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="family_enforcement",
                name="Support Enforcement",
                subject="family_law",
                difficulty=3,
                rule_statement="Contempt: civil or criminal; wage garnishment; license suspension; passport denial; federal locate services",
                elements=["Contempt sanctions", "Wage withholding", "License suspension", "Federal enforcement"],
                common_traps=["Civil vs criminal contempt", "Automatic withholding", "Cannot discharge in bankruptcy"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_contempt",
                name="Contempt Proceedings",
                subject="family_law",
                difficulty=3,
                rule_statement="Civil: coercive, must have ability to comply; Criminal: punitive, beyond reasonable doubt; inability to pay is defense",
                elements=["Civil coercive", "Criminal punitive", "Ability to pay", "Purge conditions"],
                common_traps=["Civil vs criminal", "Ability to pay defense", "Burden of proof differs"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_child_abuse",
                name="Child Abuse & Neglect",
                subject="family_law",
                difficulty=3,
                rule_statement="State intervention to protect child; removal requires hearing; reasonable efforts to reunify; termination of parental rights possible",
                elements=["Emergency removal", "Court hearing", "Reasonable efforts", "TPR option"],
                common_traps=["Due process protections", "Reasonable efforts", "Clear and convincing for TPR"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_termination_parental_rights",
                name="Termination of Parental Rights",
                subject="family_law",
                difficulty=4,
                rule_statement="Severs legal parent-child relationship; grounds: abuse, neglect, abandonment, unfitness; clear and convincing evidence; permanent",
                elements=["Statutory grounds", "Clear and convincing", "Permanent severance", "Best interests"],
                common_traps=["High burden", "Permanent", "Best interests focus"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_adoption",
                name="Adoption",
                subject="family_law",
                difficulty=3,
                rule_statement="Creates legal parent-child relationship; consent required from biological parents unless rights terminated; home study; finalization hearing",
                elements=["Consent requirements", "TPR alternative", "Home study", "Finalization"],
                common_traps=["Consent requirements", "Putative father rights", "Revocation period"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="family_paternity",
                name="Paternity Establishment",
                subject="family_law",
                difficulty=3,
                rule_statement="Voluntary acknowledgment or court determination; genetic testing presumptive; rebuttable presumptions; support and custody rights follow",
                elements=["Voluntary acknowledgment", "Genetic testing", "Presumptions", "Rights and duties"],
                common_traps=["Presumptions of paternity", "Genetic testing standard", "Rights follow establishment"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_presumptions_paternity",
                name="Presumptions of Paternity",
                subject="family_law",
                difficulty=3,
                rule_statement="Marital presumption: husband presumed father; holding out; genetic testing rebuts; multiple presumptions possible",
                elements=["Marital presumption", "Holding out", "Genetic testing", "Rebuttal"],
                common_traps=["Marital presumption strong", "Genetic testing rebuts", "Multiple presumed fathers"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="family_equitable_parent",
                name="Equitable Parent Doctrine",
                subject="family_law",
                difficulty=3,
                rule_statement="Non-biological parent may have rights/duties if: accepted parental role, bonded with child, parent consented; minority doctrine",
                elements=["Functional parent", "Acceptance of role", "Parent consent", "Bonding"],
                common_traps=["Minority doctrine", "Factors test", "Parent consent key"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="family_visitation",
                name="Visitation Rights",
                subject="family_law",
                difficulty=3,
                rule_statement="Non-custodial parent entitled to reasonable visitation unless detrimental; grandparent rights limited; supervised visitation possible",
                elements=["Reasonable visitation", "Best interests", "Grandparent limits", "Supervised option"],
                common_traps=["Grandparent rights limited", "Troxel case", "Parental presumption"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_relocation",
                name="Relocation with Child",
                subject="family_law",
                difficulty=4,
                rule_statement="Custodial parent seeking to relocate must: give notice, show legitimate reason; court balances factors; may modify custody",
                elements=["Notice requirement", "Legitimate reason", "Factor balancing", "Burden on relocating parent"],
                common_traps=["Notice timing", "Burden allocation", "Factor tests vary"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_domestic_violence",
                name="Domestic Violence",
                subject="family_law",
                difficulty=3,
                rule_statement="Protective orders available; ex parte emergency; full hearing; custody and support implications; violation is contempt/crime",
                elements=["Ex parte available", "Full hearing", "Relief available", "Violation sanctions"],
                common_traps=["Ex parte standard lower", "Custody preferences", "Criminal violation"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_protective_orders",
                name="Protective Orders",
                subject="family_law",
                difficulty=3,
                rule_statement="Restraining orders to prevent abuse; standards: immediate danger, abuse occurred; violations punishable; mutual orders disfavored",
                elements=["Standard for issuance", "Relief available", "Violation consequences", "Mutual orders issue"],
                common_traps=["Standard of proof", "Duration", "Mutual orders problematic"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="family_prenuptial_agreements",
                name="Prenuptial Agreements",
                subject="family_law",
                difficulty=4,
                rule_statement="Valid if: voluntary, fair disclosure, not unconscionable; cannot adversely affect child support; can waive spousal support",
                elements=["Voluntary execution", "Financial disclosure", "Conscionability", "Cannot affect child support"],
                common_traps=["Full disclosure required", "Cannot limit child support", "Can waive spousal support"],
                mnemonic="VFC: Voluntary, Fair disclosure, Conscionable",
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="family_postnuptial_agreements",
                name="Postnuptial Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Agreement after marriage; same requirements as prenuptial plus consideration; scrutinized closely; increasing acceptance",
                elements=["After marriage", "Consideration needed", "Close scrutiny", "Similar to prenup"],
                common_traps=["Need consideration", "Higher scrutiny", "Growing acceptance"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="family_separation_agreements",
                name="Separation Agreements",
                subject="family_law",
                difficulty=3,
                rule_statement="Negotiated settlement of divorce issues; merged into decree if approved; court reviews for fairness; child provisions always modifiable",
                elements=["Negotiated settlement", "Court approval", "Fairness review", "Merger into decree"],
                common_traps=["Court must approve", "Child provisions modifiable", "Merger vs incorporation"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="family_mediation",
                name="Mediation & ADR",
                subject="family_law",
                difficulty=2,
                rule_statement="Alternative dispute resolution; mediator facilitates; confidential; many jurisdictions require mediation attempt; custody mediation common",
                elements=["Facilitative process", "Confidentiality", "Mandatory in some places", "Custody focus"],
                common_traps=["Confidentiality protections", "No binding decision", "Mandatory mediation"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="family_tax_consequences",
                name="Tax Consequences of Divorce",
                subject="family_law",
                difficulty=3,
                rule_statement="Property transfers: generally tax-free; Alimony: post-2018 not deductible/taxable; Child support: not deductible/taxable; Dependency exemptions",
                elements=["Property transfer rules", "Alimony tax treatment", "Child support treatment", "Exemptions"],
                common_traps=["2018 tax law changes", "Property transfer tax-free", "Child support never deductible"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="family_bankruptcy",
                name="Bankruptcy & Family Law",
                subject="family_law",
                difficulty=3,
                rule_statement="Child support non-dischargeable; spousal support non-dischargeable; property division may be dischargeable; automatic stay exceptions",
                elements=["Support obligations survive", "Property division varies", "Stay exceptions", "Priority debts"],
                common_traps=["Support never dischargeable", "Property division in Ch 13", "Stay exceptions"],
                exam_frequency="low"
            ),
        ]
        
        self.concepts['family_law'] = concepts
        return len(concepts)
    
    def expand_secured_trans_full(self):
        """Complete Secured Transactions to 20-25 concepts"""
        concepts = [
            CompleteConcept(
                concept_id="secured_types_collateral",
                name="Types of Collateral",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods: consumer, equipment, farm products, inventory; Intangibles: accounts, instruments, documents, chattel paper, investment property, deposit accounts",
                elements=["Goods categories", "Intangibles", "Classification determines rules", "Use-based for goods"],
                common_traps=["Use determines goods classification", "Dual-use situations", "Transformation changes type"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="secured_after_acquired",
                name="After-Acquired Property Clause",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Security interest attaches to after-acquired property if clause included; automatic for inventory and accounts; exception for consumer goods",
                elements=["Requires clause", "Automatic inventory/accounts", "Consumer goods limit", "Attaches when acquired"],
                common_traps=["Consumer goods 10-day limit", "Inventory automatic", "Must have clause"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="secured_proceeds",
                name="Proceeds",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Security interest continues in proceeds; automatically perfected for 20 days; must perfect afterward; identifiable proceeds required",
                elements=["Automatic security interest", "20-day perfection", "Must perfect after", "Identifiable standard"],
                common_traps=["20-day temporary perfection", "Lowest intermediate balance rule", "Cash proceeds"],
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="secured_future_advances",
                name="Future Advances",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Security interest can secure future loans; priority from original perfection if within 45 days or committed",
                elements=["Secures future debts", "Original priority", "45-day rule", "Commitment"],
                common_traps=["Priority relates back", "45-day rule", "Optional vs committed"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="secured_bioc",
                name="Buyer in Ordinary Course",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="BIOC takes free of security interest in inventory even if perfected and knows; must be ordinary course; good faith; value given",
                elements=["Takes free", "Inventory only", "Ordinary course", "Good faith + value"],
                common_traps=["Takes free even with knowledge", "Inventory only", "Ordinary course requirement"],
                mnemonic="BIOC: Buyer, Inventory, Ordinary, Course (takes free)",
                exam_frequency="very_high"
            ),
            CompleteConcept(
                concept_id="secured_fixtures",
                name="Fixtures",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Personal property that becomes real property; fixture filing perfects; PMSI fixture has priority if: filed before or within 20 days, construction mortgage exception",
                elements=["Fixture definition", "Fixture filing", "PMSI priority", "Construction mortgage"],
                common_traps=["20-day grace period", "Construction mortgage wins", "Fixture filing location"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="secured_accessions",
                name="Accessions",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods installed in other goods; security interest continues; perfection required; removal right if no material harm",
                elements=["Continues in accession", "Perfection needed", "Priority rules", "Removal rights"],
                common_traps=["First to file wins", "Material harm test", "PMSI super-priority"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="secured_commingled",
                name="Commingled Goods",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Goods physically united in product; security interest continues in product; perfection continues; priority prorata by value",
                elements=["Continues in product", "Perfection continues", "Pro rata priority", "Cannot separate"],
                common_traps=["Pro rata distribution", "Cannot separate", "Perfection continues"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="secured_investment_property",
                name="Investment Property",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Securities, security entitlements, accounts; perfection by control or filing; control has priority over filing",
                elements=["Control perfection", "Filing alternative", "Control priority", "Types included"],
                common_traps=["Control beats filing", "Control methods", "Securities intermediary"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="secured_deposit_accounts",
                name="Deposit Accounts",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Can only perfect by control; control: secured party is bank, control agreement, or secured party is account holder",
                elements=["Control only", "Three methods", "No filing perfection", "Priority by control"],
                common_traps=["Cannot perfect by filing", "Control methods", "Bank as secured party"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="secured_lien_creditor",
                name="Lien Creditors",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Secured party vs lien creditor: perfected wins; unperfected loses unless PMSI grace period; trustee in bankruptcy is lien creditor",
                elements=["Perfected beats lien creditor", "Unperfected loses", "PMSI grace period", "Bankruptcy trustee"],
                common_traps=["Trustee as lien creditor", "PMSI grace period", "Perfection timing critical"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="secured_continuation",
                name="Continuation Statements",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Filing effective 5 years; continuation filed within 6 months before lapse; extends another 5 years",
                elements=["5-year duration", "6-month window", "Extends 5 years", "Must be timely"],
                common_traps=["6-month window", "Lapses if not filed", "Calculation of dates"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="secured_termination",
                name="Termination Statements",
                subject="secured_transactions",
                difficulty=2,
                rule_statement="Secured party must file termination when debt paid; consumer goods: 1 month or 20 days if requested; other collateral: on demand",
                elements=["Must file when paid", "Consumer timing", "Non-consumer on demand", "Penalties for failure"],
                common_traps=["Consumer timing strict", "Must file termination", "Failure penalties"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="secured_assignments",
                name="Assignment of Security Interest",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Can assign security interest; need not file unless assignee wants priority over later assignee; notification to debtor",
                elements=["Assignability", "Filing not required", "Priority of assignees", "Debtor notification"],
                common_traps=["Filing not required for perfection", "Priority among assignees", "Debtor payment rules"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="secured_agricultural_liens",
                name="Agricultural Liens",
                subject="secured_transactions",
                difficulty=2,
                rule_statement="Non-consensual lien on farm products; perfection by filing; priority rules similar to Article 9; statute creates",
                elements=["Statutory lien", "Farm products", "Filing perfects", "Similar priority"],
                common_traps=["Not security interest", "Statutory basis", "Filing required"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="secured_bankruptcy_trustee",
                name="Bankruptcy Trustee Powers",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Trustee has strong-arm power: lien creditor status; can avoid unperfected interests; 90-day preference period for perfection",
                elements=["Lien creditor status", "Avoid unperfected", "90-day preference", "Filing relates back"],
                common_traps=["90-day preference", "Grace period protection", "Relates back if timely"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="secured_preferences",
                name="Preferences in Bankruptcy",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Transfer within 90 days while insolvent that prefers creditor can be avoided; exceptions: contemporaneous exchange, ordinary course, PMSI grace",
                elements=["90-day lookback", "Insolvency presumed", "Preference elements", "Exceptions"],
                common_traps=["90 days", "PMSI grace period exception", "Ordinary course exception"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="secured_fraudulent_transfers",
                name="Fraudulent Transfers",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Transfer to hinder, delay, defraud creditors; transfer for less than reasonably equivalent value while insolvent; can be avoided",
                elements=["Actual fraud", "Constructive fraud", "Reasonably equivalent value", "Insolvency"],
                common_traps=["Actual vs constructive", "Timing", "Badges of fraud"],
                exam_frequency="medium"
            ),
        ]
        
        self.concepts['secured_transactions'] = concepts
        return len(concepts)
    
    def expand_iowa_procedure_full(self):
        """Complete Iowa Procedure to 15-20 concepts"""
        concepts = [
            CompleteConcept(
                concept_id="iowa_pleading",
                name="Iowa Pleading Requirements",
                subject="iowa_procedure",
                difficulty=3,
                iowa_specific=True,
                rule_statement="Iowa requires notice pleading similar to federal; original notice serves as complaint; must state claim upon which relief can be granted",
                elements=["Original notice", "Notice pleading", "State claim", "Similar to federal"],
                common_traps=["Original notice terminology", "Similar to FRCP", "Specific Iowa forms"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="iowa_service",
                name="Iowa Service of Process",
                subject="iowa_procedure",
                difficulty=3,
                iowa_specific=True,
                rule_statement="Personal service by sheriff or process server; substituted service available; service by publication with court approval",
                elements=["Personal service", "Sheriff service", "Substituted service", "Publication service"],
                common_traps=["Sheriff preference", "Publication requirements", "Proof of service"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="iowa_discovery",
                name="Iowa Discovery Rules",
                subject="iowa_procedure",
                difficulty=2,
                iowa_specific=True,
                rule_statement="Iowa discovery mirrors federal rules; interrogatories, depositions, requests for production, admissions; proportionality applies",
                elements=["Federal model", "All federal tools", "Proportionality", "Protective orders"],
                common_traps=["Similar to federal", "Iowa-specific limits", "Timing differences"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="iowa_summary_judgment",
                name="Iowa Summary Judgment",
                subject="iowa_procedure",
                difficulty=3,
                iowa_specific=True,
                rule_statement="Available if no genuine issue of material fact; moving party burden; view evidence in light favorable to non-movant",
                elements=["No genuine issue", "Material fact", "Moving party burden", "Favorable view"],
                common_traps=["Standard similar to federal", "Iowa case law", "Timing requirements"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="iowa_trial_procedures",
                name="Iowa Trial Procedures",
                subject="iowa_procedure",
                difficulty=2,
                iowa_specific=True,
                rule_statement="Jury trial right; voir dire conducted by judge typically; Iowa Rules of Evidence govern; jury instructions settled before trial",
                elements=["Jury right", "Judge voir dire", "Evidence rules", "Jury instructions"],
                common_traps=["Judge-conducted voir dire", "Iowa evidence rules", "Pre-trial procedures"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="iowa_appeals",
                name="Iowa Appellate Procedure",
                subject="iowa_procedure",
                difficulty=3,
                iowa_specific=True,
                rule_statement="Appeal to Iowa Court of Appeals or Supreme Court; notice of appeal within 30 days; record and brief requirements; standards of review",
                elements=["30-day deadline", "Notice of appeal", "Record requirements", "Standards of review"],
                common_traps=["30-day deadline strict", "Direct to Supreme Court options", "Preservation requirements"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="iowa_venue",
                name="Iowa Venue",
                subject="iowa_procedure",
                difficulty=2,
                iowa_specific=True,
                rule_statement="Proper venue: defendant residence, cause of action arose, property located, contract performed; transfer available",
                elements=["Defendant residence", "Cause arose", "Property location", "Transfer possible"],
                common_traps=["Multiple proper venues", "Transfer discretion", "Convenience factors"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="iowa_jurisdiction",
                name="Iowa Personal Jurisdiction",
                subject="iowa_procedure",
                difficulty=3,
                iowa_specific=True,
                rule_statement="Long-arm statute reaches constitutional limits; minimum contacts required; purposeful availment; fair play and substantial justice",
                elements=["Long-arm statute", "Constitutional limits", "Minimum contacts", "Fairness test"],
                common_traps=["Constitutional analysis", "Specific vs general", "Stream of commerce"],
                exam_frequency="high"
            ),
            CompleteConcept(
                concept_id="iowa_joinder",
                name="Iowa Joinder Rules",
                subject="iowa_procedure",
                difficulty=2,
                iowa_specific=True,
                rule_statement="Permissive joinder of parties and claims; compulsory joinder of necessary parties; intervention and interpleader available",
                elements=["Permissive joinder", "Necessary parties", "Intervention", "Interpleader"],
                common_traps=["Similar to federal", "Iowa variations", "Necessary vs indispensable"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="iowa_class_actions",
                name="Iowa Class Actions",
                subject="iowa_procedure",
                difficulty=3,
                iowa_specific=True,
                rule_statement="Class actions permitted; requirements similar to federal; certification required; notice to class members",
                elements=["Certification requirements", "Numerosity", "Commonality", "Notice"],
                common_traps=["Certification motion", "Opt-out rights", "Settlement approval"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="iowa_injunctions",
                name="Iowa Injunctions",
                subject="iowa_procedure",
                difficulty=3,
                iowa_specific=True,
                rule_statement="Temporary and permanent injunctions available; requirements: likelihood of success, irreparable harm, balance of harms, public interest",
                elements=["Temporary injunction", "Permanent injunction", "Four factors", "Bond requirement"],
                common_traps=["Four-factor test", "Bond for temporary", "Hearing requirements"],
                exam_frequency="medium"
            ),
            CompleteConcept(
                concept_id="iowa_judgments",
                name="Iowa Judgments",
                subject="iowa_procedure",
                difficulty=2,
                iowa_specific=True,
                rule_statement="Default judgment available; directed verdict/JNOV motions; new trial motions; judgment liens; enforcement procedures",
                elements=["Default judgment", "Post-trial motions", "Judgment liens", "Enforcement"],
                common_traps=["Motion timing", "Lien procedures", "Enforcement methods"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="iowa_execution",
                name="Iowa Execution & Garnishment",
                subject="iowa_procedure",
                difficulty=3,
                iowa_specific=True,
                rule_statement="Execution on judgment; garnishment of wages and accounts; exemptions protect certain property; procedures for collection",
                elements=["Execution process", "Garnishment", "Exemptions", "Debtor protections"],
                common_traps=["Iowa exemptions", "Garnishment limits", "Procedures"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="iowa_sanctions",
                name="Iowa Sanctions",
                subject="iowa_procedure",
                difficulty=2,
                iowa_specific=True,
                rule_statement="Court may sanction frivolous filings, discovery abuse, contempt; attorney fees available; Rule 1.413 governs",
                elements=["Frivolous filings", "Discovery sanctions", "Contempt", "Attorney fees"],
                common_traps=["Rule 1.413", "Standards for sanctions", "Safe harbor"],
                exam_frequency="low"
            ),
            CompleteConcept(
                concept_id="iowa_adr",
                name="Iowa ADR Procedures",
                subject="iowa_procedure",
                difficulty=2,
                iowa_specific=True,
                rule_statement="Mediation encouraged; arbitration enforceable; case management conferences; settlement conferences",
                elements=["Mediation", "Arbitration", "Case management", "Settlement conferences"],
                common_traps=["Mandatory mediation in some cases", "Arbitration enforcement", "Confidentiality"],
                exam_frequency="low"
            ),
        ]
        
        self.concepts['iowa_procedure'] = concepts
        return len(concepts)
    
    def generate_all(self):
        """Generate all Phase 2 concepts"""
        print("="*70)
        print("COMPLETE ESSAY EXPANSION - PHASE 2")
        print("Completing remaining 4 subjects")
        print("="*70)
        print()
        
        counts = {}
        
        print("📚 Expanding Remaining Subjects:\n")
        
        counts['wills_trusts_estates'] = self.expand_wills_trusts_full()
        print(f"✅ Wills/Trusts/Estates: {counts['wills_trusts_estates']} concepts")
        
        counts['family_law'] = self.expand_family_law_full()
        print(f"✅ Family Law: {counts['family_law']} concepts")
        
        counts['secured_transactions'] = self.expand_secured_trans_full()
        print(f"✅ Secured Transactions: {counts['secured_transactions']} concepts")
        
        counts['iowa_procedure'] = self.expand_iowa_procedure_full()
        print(f"✅ Iowa Procedure: {counts['iowa_procedure']} concepts")
        
        total = sum(counts.values())
        
        print(f"\n📊 Phase 2 Summary:")
        print(f"  New Concepts Generated: {total}")
        print(f"  Phase 1 Concepts: 57")
        print(f"  Total Essay Concepts: {57 + total}")
        print(f"  MBE Concepts: 180")
        print(f"  GRAND TOTAL: {180 + 57 + total}")
        
        return total

def main():
    expander = Phase2Expander()
    total = expander.generate_all()
    
    print("\n💾 Exporting...")
    
    all_concepts = []
    for subject, concepts in expander.concepts.items():
        all_concepts.extend([asdict(c) for c in concepts])
    
    with open("essay_expansion_phase2.json", 'w') as f:
        json.dump(all_concepts, f, indent=2)
    print("✓ essay_expansion_phase2.json")
    
    print("\n" + "="*70)
    print("✅ PHASE 2 COMPLETE!")
    print("="*70)
    print(f"\n🎉 Total Essay Concepts: {57 + total}")
    print(f"🎉 Complete Iowa Bar Total: {180 + 57 + total}")
    print("\n📊 Breakdown:")
    print("  • Professional Responsibility: 26")
    print("  • Corporations: 27")
    print("  • Wills/Trusts/Estates: ~36")
    print("  • Family Law: ~25")
    print("  • Secured Transactions: ~18")
    print("  • Iowa Procedure: ~15")
    print("\nNext: python3 integrate_all_essays.py")

if __name__ == "__main__":
    main()

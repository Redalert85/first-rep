# Essay Subjects for Iowa Bar

    def _initialize_professional_responsibility(self):
        """10 Professional Responsibility concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="prof_resp_confidentiality",
                name="Duty of Confidentiality",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Lawyer must not reveal information relating to representation unless client consents, disclosure impliedly authorized, or exception applies",
                elements=['Duty to all information', 'Broader than privilege', 'Survives termination', 'Prospective clients'],
                policy_rationales=[],
                common_traps=['Confusing with privilege', 'Missing crime/fraud exception limits', 'Forgetting survives death'],
                # Mnemonic: CRIMES: Crime prevention, Reasonably certain harm, Informed consent, Mitigate harm, Establish defense, Secure advice
            ),
            KnowledgeNode(
                concept_id="prof_resp_conflicts_current",
                name="Conflicts - Current Clients",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent if directly adverse or significant limitation risk, unless reasonable belief, not prohibited, not same litigation, written consent",
                elements=['Direct adversity', 'Material limitation', 'Reasonable belief', 'Written consent'],
                policy_rationales=[],
                common_traps=['Same litigation cannot be cured', 'Business transactions need disclosure', 'Positional conflicts'],
                # Mnemonic: WIND: Written consent, Informed, Not same litigation, Direct adversity
            ),
            KnowledgeNode(
                concept_id="prof_resp_conflicts_former",
                name="Conflicts - Former Clients",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Cannot represent if materially adverse in same or substantially related matter unless written consent",
                elements=['Same matter', 'Substantially related', 'Material adversity', 'Written consent'],
                policy_rationales=[],
                common_traps=['Substantial relationship broader than same', 'Imputation differs', 'Screening procedures'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_competence",
                name="Duty of Competence",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must provide competent representation requiring knowledge, skill, thoroughness, and preparation",
                elements=['Legal knowledge', 'Skill', 'Thoroughness', 'Preparation'],
                policy_rationales=[],
                common_traps=['Need not be expert', 'Must stay current', 'Can associate with competent lawyer'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_fees",
                name="Fees & Fee Agreements",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Fee must be reasonable; contingent fees prohibited in criminal and divorce; writing preferred",
                elements=['Reasonableness factors', 'Writing preferred', 'Contingent restrictions', 'Fee division rules'],
                policy_rationales=[],
                common_traps=['No contingent in criminal', 'No contingent in divorce', 'Fee division restrictions', 'Separate client property'],
                # Mnemonic: NO CC: No Contingent Criminal, No Contingent Custody
            ),
            KnowledgeNode(
                concept_id="prof_resp_client_decisions",
                name="Client Decision Authority",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Client decides objectives; lawyer decides means; certain decisions require client consent",
                elements=['Client: objectives, settlement, plea, testify', 'Lawyer: tactics', 'Limit scope with consent', 'Consult and explain'],
                policy_rationales=[],
                common_traps=['Settlement is client decision', 'Testify in criminal is client', 'Limiting scope needs consent'],
                # Mnemonic: SPLIT: Settlement, Plea, testify, jury trial = client
            ),
            KnowledgeNode(
                concept_id="prof_resp_candor_tribunal",
                name="Candor Toward Tribunal",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="No false statements; disclose adverse authority; correct false evidence; cannot offer known false evidence",
                elements=['No false statements', 'Disclose adverse binding authority', 'Correct false evidence', 'No known false evidence'],
                policy_rationales=[],
                common_traps=['Must disclose adverse in controlling jurisdiction', 'Must correct even if client objects', 'Narrative testimony'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_fairness_opposing",
                name="Fairness to Opposing Party",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="No obstruction of evidence, no ex parte with represented persons, fair dealing with unrepresented",
                elements=['No obstruction', 'No ex parte contact', 'Fair with unrepresented', 'No unlawful obstruction'],
                policy_rationales=[],
                common_traps=['Contact through counsel', 'Flag inadvertent privileged docs', 'Clarify role with unrepresented'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_prosecutor",
                name="Special Prosecutor Duties",
                subject="professional_responsibility",
                difficulty=4,
                rule_statement="Must have probable cause; disclose exculpatory evidence; ensure counsel",
                elements=['Probable cause', 'Brady disclosure', 'Ensure counsel', 'Protect unrepresented'],
                policy_rationales=['Seek justice not convictions', 'Protect accused rights', 'Ensure fairness'],
                common_traps=['Heightened Brady duty', 'Cannot subpoena lawyer about client', 'Must disclose post-conviction'],
            ),
            KnowledgeNode(
                concept_id="prof_resp_meritorious_claims",
                name="Meritorious Claims",
                subject="professional_responsibility",
                difficulty=3,
                rule_statement="Must not bring frivolous claims; must have good faith basis",
                elements=['Non-frivolous basis', 'Good faith law change OK', 'Candor required', 'No false statements'],
                policy_rationales=[],
                common_traps=['Creative arguments OK if good faith', 'Criminal defense exception', 'Frivolous ≠ losing'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_corporations(self):
        """7 Corporations concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="corp_formation",
                name="Corporate Formation",
                subject="corporations",
                difficulty=3,
                rule_statement="Corporation formed by filing articles; becomes separate entity upon filing",
                elements=['Articles of incorporation', 'File with state', 'Separate personality', 'Perpetual existence'],
                policy_rationales=[],
                common_traps=['Just need filing', 'De facto corporation', 'Promoter liability'],
            ),
            KnowledgeNode(
                concept_id="corp_piercing_veil",
                name="Piercing Corporate Veil",
                subject="corporations",
                difficulty=4,
                rule_statement="Veil pierced if fraud, evade obligations, or injustice; requires alter ego and inequitable result",
                elements=['Alter ego', 'Inequitable result', 'Undercapitalization', 'Formality failure'],
                policy_rationales=['Limited liability encourages business', 'Prevent abuse', 'Balance protection'],
                common_traps=['High threshold', 'Control alone insufficient', 'Parent-sub vs individual-corp'],
            ),
            KnowledgeNode(
                concept_id="corp_duty_care",
                name="Duty of Care",
                subject="corporations",
                difficulty=4,
                rule_statement="Directors owe care of ordinarily prudent person; business judgment rule protects if informed, disinterested, good faith",
                elements=['Informed decision', 'Ordinary prudence', 'Business judgment rule', 'Good faith'],
                policy_rationales=[],
                common_traps=['BJR not automatic', 'Gross negligence defeats', 'Confusing care with loyalty'],
                # Mnemonic: BJR-DIG: Business Judgment Rule = Disinterested, Informed, Good faith
            ),
            KnowledgeNode(
                concept_id="corp_duty_loyalty",
                name="Duty of Loyalty",
                subject="corporations",
                difficulty=4,
                rule_statement="Act in corporation's interests; no self-dealing unless fair or approved",
                elements=['No self-dealing', 'Corporate opportunity', 'Fairness if interested', 'Disclosure and approval'],
                policy_rationales=[],
                common_traps=['Interested transaction voidable unless approved', 'Corporate opportunity analysis', 'Entire fairness standard'],
            ),
            KnowledgeNode(
                concept_id="corp_derivative_actions",
                name="Derivative Actions",
                subject="corporations",
                difficulty=4,
                rule_statement="Shareholder sues on corporation's behalf; requires demand unless futile; contemporaneous ownership",
                elements=['Demand on board', 'Contemporaneous ownership', 'Adequate representation', 'Corporation necessary party'],
                policy_rationales=[],
                common_traps=['Demand requirement', 'Contemporaneous ownership', 'Derivative vs direct'],
            ),
            KnowledgeNode(
                concept_id="corp_shareholder_voting",
                name="Shareholder Voting",
                subject="corporations",
                difficulty=3,
                rule_statement="Elect directors, approve fundamental changes; proxies permitted; quorum required",
                elements=['Elect directors', 'Fundamental changes', 'Proxy rules', 'Quorum'],
                policy_rationales=[],
                common_traps=['Removal without cause', 'Cumulative voting', 'Proxy rules'],
            ),
            KnowledgeNode(
                concept_id="corp_mergers",
                name="Mergers & Acquisitions",
                subject="corporations",
                difficulty=4,
                rule_statement="Merger needs board and shareholder approval; surviving entity assumes liabilities; appraisal rights",
                elements=['Board approval', 'Shareholder vote', 'Successor liability', 'Appraisal rights'],
                policy_rationales=[],
                common_traps=['Short-form merger', 'Triangular mergers', 'De facto merger'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_wills_trusts_estates(self):
        """6 Wills Trusts Estates concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="wills_execution",
                name="Will Execution",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Valid will: 18+, sound mind, intent, writing, signature, two witnesses present simultaneously",
                elements=['Age 18+ sound mind', 'Intent', 'Writing', 'Signature', 'Two witnesses'],
                policy_rationales=[],
                common_traps=['Witnesses same time', 'Interested witness', 'Substantial compliance'],
                # Mnemonic: WITSAC: Writing, Intent, Testator 18+, Signature, Attestation, Capacity
            ),
            KnowledgeNode(
                concept_id="wills_revocation",
                name="Will Revocation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Revoked by: subsequent instrument, physical act with intent, operation of law (divorce)",
                elements=['By writing', 'Physical act + intent', 'Operation of law', 'Dependent relative revocation'],
                policy_rationales=[],
                common_traps=['Divorce revokes ex-spouse', 'Revival rules', 'DRR for mistakes'],
            ),
            KnowledgeNode(
                concept_id="wills_intestate",
                name="Intestate Succession",
                subject="wills_trusts_estates",
                difficulty=3,
                rule_statement="Passes to heirs by statute: spouse, descendants, parents, siblings",
                elements=['Spouse share', 'Issue', 'Per capita vs per stirpes', 'Collaterals'],
                policy_rationales=[],
                common_traps=['Per capita vs per stirpes', 'Adopted children equal', 'Half-bloods equal'],
                # Mnemonic: SIPAC: Spouse, Issue, Parents, Ancestors, Collaterals
            ),
            KnowledgeNode(
                concept_id="trusts_creation",
                name="Trust Creation",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Requires: settlor capacity and intent, res, definite beneficiaries, valid purpose, delivery (inter vivos)",
                elements=['Settlor capacity/intent', 'Trust property', 'Ascertainable beneficiaries', 'Valid purpose', 'Delivery'],
                policy_rationales=[],
                common_traps=['Precatory language insufficient', 'Indefinite beneficiaries void', 'Delivery for inter vivos'],
                # Mnemonic: SCRIPT: Settlor, Capacity, Res, Intent, Purpose, Transfer
            ),
            KnowledgeNode(
                concept_id="trusts_charitable",
                name="Charitable Trusts",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Charitable purpose; indefinite beneficiaries OK; cy pres if purpose fails; RAP doesn't apply",
                elements=['Charitable purpose', 'Indefinite beneficiaries OK', 'Cy pres', 'RAP exception'],
                policy_rationales=[],
                common_traps=["RAP doesn't apply", 'Cy pres application', 'AG has standing'],
            ),
            KnowledgeNode(
                concept_id="trusts_fiduciary_duties",
                name="Trustee Fiduciary Duties",
                subject="wills_trusts_estates",
                difficulty=4,
                rule_statement="Loyalty, prudence, best interests; no self-dealing; prudent investment; account",
                elements=['Duty of loyalty', 'Duty of prudence', 'Duty to account', 'Duty of impartiality'],
                policy_rationales=[],
                common_traps=['Self-dealing voidable even if fair', 'Prudent investor rule', 'Impartiality income/remainder'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_family_law(self):
        """5 Family Law concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="family_divorce",
                name="Divorce Grounds",
                subject="family_law",
                difficulty=3,
                rule_statement="All states allow no-fault; irretrievable breakdown or separation; residency requirement",
                elements=['No-fault grounds', 'Irretrievable breakdown', 'Residency', 'Fault grounds minority'],
                policy_rationales=[],
                common_traps=['Fault for divorce unnecessary', 'Fault may affect property/alimony', 'Cooling-off periods'],
            ),
            KnowledgeNode(
                concept_id="family_property_division",
                name="Property Division",
                subject="family_law",
                difficulty=4,
                rule_statement="Marital property divided equitably; separate retained; factors include contributions, duration, circumstances",
                elements=['Marital vs separate', 'Equitable factors', 'Valuation date', 'Professional degrees'],
                policy_rationales=[],
                common_traps=['Equitable ≠ equal', 'Appreciation of separate may be marital', 'Pension benefits marital'],
            ),
            KnowledgeNode(
                concept_id="family_spousal_support",
                name="Spousal Support",
                subject="family_law",
                difficulty=3,
                rule_statement="Based on need, ability, duration, contributions; modifiable unless agreed",
                elements=['Need', 'Ability to pay', 'Duration', 'Contributions', 'Modifiability'],
                policy_rationales=[],
                common_traps=['Remarriage terminates', 'Cohabitation may terminate', 'Types: temporary, rehabilitative, permanent'],
            ),
            KnowledgeNode(
                concept_id="family_child_custody",
                name="Child Custody",
                subject="family_law",
                difficulty=4,
                rule_statement="Best interests of child; factors include wishes, relationships, stability, health",
                elements=['Best interests', 'Legal vs physical', 'Joint vs sole', 'Modification standards'],
                policy_rationales=[],
                common_traps=['Gender preference unconstitutional', 'Primary caretaker presumption', 'UCCJEA jurisdiction'],
            ),
            KnowledgeNode(
                concept_id="family_child_support",
                name="Child Support",
                subject="family_law",
                difficulty=3,
                rule_statement="Both parents liable; income guidelines; non-modifiable for past due; interstate enforceable",
                elements=['Income guidelines', 'Both parents', 'Modifiable prospectively', 'UIFSA enforcement'],
                policy_rationales=[],
                common_traps=['Non-dischargeable bankruptcy', 'Past-due not modifiable', 'Emancipation terminates'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_secured_transactions(self):
        """6 Secured Transactions concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="secured_scope",
                name="Article 9 Scope",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Applies to security interests in personal property/fixtures by contract; excludes real property, wages, federal liens",
                elements=['Personal property', 'By contract', 'Fixtures included', 'Exclusions'],
                policy_rationales=[],
                common_traps=['Not real property mortgages', 'True leases excluded', 'Sales of payment rights covered'],
            ),
            KnowledgeNode(
                concept_id="secured_attachment",
                name="Attachment",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Attaches when: value given, debtor has rights, authenticated agreement OR possession/control",
                elements=['Value given', 'Rights in collateral', 'Authenticated agreement', 'Description'],
                policy_rationales=[],
                common_traps=['All three required', 'Agreement must describe', 'Possession substitutes for writing'],
                # Mnemonic: VRA: Value, Rights, Agreement
            ),
            KnowledgeNode(
                concept_id="secured_perfection",
                name="Perfection",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="Perfected by: filing, possession, control, or automatic (PMSI consumer goods)",
                elements=['Filing statement', 'Possession/control', 'Automatic PMSI', 'Temporary rules'],
                policy_rationales=[],
                common_traps=['PMSI consumer goods automatic', 'Filing needs name and collateral', "File in debtor's state"],
                # Mnemonic: FPAC: Filing, Possession, Automatic, Control
            ),
            KnowledgeNode(
                concept_id="secured_pmsi",
                name="PMSI Super-Priority",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="PMSI enables acquisition; super-priority if properly perfected",
                elements=['Enables acquisition', 'Different perfection', 'Super-priority', 'Notice for inventory'],
                policy_rationales=[],
                common_traps=['Inventory PMSI needs notice', 'Consumer goods automatic', '20-day grace period'],
            ),
            KnowledgeNode(
                concept_id="secured_priority",
                name="Priority Rules",
                subject="secured_transactions",
                difficulty=4,
                rule_statement="First to file/perfect wins; PMSI super-priority; buyer in ordinary course takes free",
                elements=['First to file/perfect', 'PMSI super-priority', 'BIOC exception', 'Lien creditor'],
                policy_rationales=[],
                common_traps=['Filing beats possession if first', 'BIOC takes free with notice', 'Judgment lien priority'],
            ),
            KnowledgeNode(
                concept_id="secured_default",
                name="Default Remedies",
                subject="secured_transactions",
                difficulty=3,
                rule_statement="Upon default: take possession (self-help if no breach of peace), dispose commercially reasonable, debtor gets surplus",
                elements=['Self-help no breach peace', 'Judicial alternative', 'Commercially reasonable', 'Notice required'],
                policy_rationales=[],
                common_traps=['Breach of peace voids self-help', 'Notice before disposition', 'Strict foreclosure option'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node

    def _initialize_iowa_procedure(self):
        """1 Iowa Procedure concepts"""
        concepts = [
            KnowledgeNode(
                concept_id="iowa_civil_procedure",
                name="Iowa Civil Procedure",
                subject="iowa_procedure",
                difficulty=3,
                rule_statement="Iowa Rules largely mirror Federal but with Iowa variations; governed by Iowa Code and court rules",
                elements=['Iowa Rules Civil Procedure', 'Court Rules', 'District court', 'Appellate procedures'],
                policy_rationales=[],
                common_traps=['Not identical to federal', 'Iowa-specific timing', 'Local rules variations'],
            ),
        ]
        for node in concepts:
            self.nodes[node.concept_id] = node


#!/usr/bin/env python3
"""
MEE Bar Prep Game: Secured Transactions & Wills/Trusts/Estates
================================================================
An interactive study game for the two hardest MEE subjects.

Game Modes:
1. Scenario Challenge - Solve realistic MEE fact patterns
2. Rule Sprint - Quick-fire rule identification
3. Priority Puzzles - Complex priority/timing problems
4. Boss Battle - Full MEE-style essay questions

Features:
- Progressive difficulty (Level 1-5)
- Real-time scoring with combo multipliers
- Detailed explanations for every answer
- Progress tracking and weak area identification
- Timed challenges with Iowa Bar exam timing
"""

import json
import random
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import sys

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

@dataclass
class GameStats:
    """Track player performance"""
    total_questions: int = 0
    correct_answers: int = 0
    current_streak: int = 0
    best_streak: int = 0
    points: int = 0
    level: int = 1
    subject_scores: Dict[str, Dict[str, int]] = None

    def __post_init__(self):
        if self.subject_scores is None:
            self.subject_scores = {
                'secured_transactions': {'correct': 0, 'total': 0},
                'wills_trusts_estates': {'correct': 0, 'total': 0}
            }

    def accuracy(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100

    def subject_accuracy(self, subject: str) -> float:
        if subject not in self.subject_scores:
            return 0.0
        total = self.subject_scores[subject]['total']
        if total == 0:
            return 0.0
        correct = self.subject_scores[subject]['correct']
        return (correct / total) * 100

@dataclass
class Question:
    """Represents a study question"""
    id: str
    subject: str
    difficulty: int
    concept: str
    question_type: str  # 'multiple_choice', 'scenario', 'priority_puzzle', 'essay'
    question_text: str
    options: List[str]
    correct_answer: int | str
    explanation: str
    rule_statement: str
    common_traps: List[str]
    time_limit: int  # seconds

# ============================================================================
# SECURED TRANSACTIONS QUESTIONS
# ============================================================================

SECURED_TRANSACTIONS_QUESTIONS = [
    # Level 1 - Basic Attachment & Perfection
    Question(
        id="st_001",
        subject="secured_transactions",
        difficulty=1,
        concept="Attachment",
        question_type="multiple_choice",
        question_text="""
Bank lends $10,000 to Debtor. Debtor signs a security agreement describing
"all Debtor's equipment." Debtor owns a $15,000 printing press. Bank never files.

When does Bank's security interest ATTACH to the printing press?
        """,
        options=[
            "When Debtor signs the security agreement",
            "When Bank lends the $10,000",
            "When all three VRA elements are satisfied (Value, Rights, Agreement)",
            "When Bank files a financing statement",
        ],
        correct_answer=2,
        explanation="""
CORRECT: C. Attachment requires ALL THREE elements (VRA):
1. Value given by secured party (Bank lent $10,000) ✓
2. Debtor has Rights in collateral (Debtor owns printing press) ✓
3. Authenticated security Agreement describing collateral ✓

All three occurred simultaneously here, so attachment happens immediately.
Filing is NOT required for attachment - only for perfection!

TRAP: Many students confuse attachment (when SI becomes enforceable between parties)
with perfection (when SI becomes enforceable against third parties).
        """,
        rule_statement="Attaches when: value given, debtor has rights, authenticated agreement (VRA)",
        common_traps=[
            "Confusing attachment with perfection",
            "Thinking filing is required for attachment",
            "Forgetting all three elements must be satisfied"
        ],
        time_limit=90
    ),

    Question(
        id="st_002",
        subject="secured_transactions",
        difficulty=2,
        concept="PMSI Super-Priority",
        question_type="scenario",
        question_text="""
Timeline:
- Jan 1: Bank lends Retailer $100K, takes SI in "all inventory now owned or after-acquired",
  files financing statement
- Feb 1: Supplier sells Retailer $20K of new inventory on credit, retains PMSI
- Feb 5: Supplier sends authenticated notice to Bank of its PMSI
- Feb 8: Supplier files financing statement
- Feb 10: Goods delivered to Retailer
- Mar 1: Retailer defaults on both debts

Who has priority in the new $20K inventory?
        """,
        options=[
            "Bank - it filed first on January 1",
            "Supplier - it has PMSI super-priority",
            "Bank - Supplier's notice came after the goods were delivered",
            "They split the proceeds 50/50",
        ],
        correct_answer=1,
        explanation="""
CORRECT: B. Supplier wins with PMSI super-priority!

For INVENTORY PMSI super-priority, secured party must:
1. Perfect before debtor receives possession ✓ (filed Feb 8, delivered Feb 10)
2. Send authenticated notice to prior perfected parties ✓ (notice Feb 5)
3. Notice must be received within 5 years before debtor gets possession ✓

Supplier satisfied all requirements. PMSI in inventory ALWAYS requires notice
to existing secured parties, unlike PMSI in other goods (equipment, etc.).

TRAP: Students often forget the notice requirement for inventory PMSI, or think
notice must come before filing. Notice only needs to arrive before debtor receives goods.

CRITICAL DISTINCTION:
- Equipment PMSI: File within 20 days, NO notice required
- Inventory PMSI: File before delivery, notice to existing creditors required
        """,
        rule_statement="PMSI in inventory gets super-priority if: (1) perfected before debtor receives, (2) notice to prior parties within 5 years before delivery",
        common_traps=[
            "Forgetting notice requirement for inventory PMSI",
            "Applying equipment PMSI rules to inventory",
            "Thinking first-to-file always wins"
        ],
        time_limit=180
    ),

    Question(
        id="st_003",
        subject="secured_transactions",
        difficulty=3,
        concept="Priority Rules",
        question_type="priority_puzzle",
        question_text="""
Complex Priority Problem:

- Jan 1: Bank files financing statement covering "all of Debtor's equipment"
  (but hasn't yet lent money)
- Feb 1: Finance Co lends Debtor money, Debtor signs security agreement
  for "all equipment", Finance Co files same day
- Mar 1: Bank finally lends money and gets signed security agreement
- Apr 1: Judgment creditor gets judgment lien on Debtor's equipment
- May 1: Supplier sells Debtor new equipment on credit (PMSI)
- May 18: Supplier files financing statement

Rank the priorities in Debtor's equipment:
        """,
        options=[
            "Bank, Finance Co, Judgment Creditor, Supplier",
            "Finance Co, Bank, Supplier, Judgment Creditor",
            "Supplier, Bank, Finance Co, Judgment Creditor",
            "Supplier, Finance Co, Bank, Judgment Creditor",
        ],
        correct_answer=3,
        explanation="""
CORRECT: D. Supplier (1st), Finance Co (2nd), Bank (3rd), Judgment Creditor (4th)

Step-by-step analysis:

1. SUPPLIER - 1st place: PMSI super-priority!
   - Filed within 20 days (May 18, only 18 days after May 1 sale) ✓
   - Equipment PMSI gets priority over earlier filed secured parties
   - No notice required for equipment PMSI (unlike inventory)

2. FINANCE CO - 2nd place
   - First to FILE AND PERFECT: Feb 1
   - Had attachment: value + rights + agreement on Feb 1
   - "First to file or perfect" wins between secured parties

3. BANK - 3rd place
   - Filed first (Jan 1) BUT didn't perfect until Mar 1
   - Perfection requires BOTH filing AND attachment
   - No attachment until Mar 1 (value + agreement finally satisfied)
   - Lost to Finance Co because Finance Co perfected first (Feb 1 vs Mar 1)

4. JUDGMENT CREDITOR - 4th place (last)
   - Perfected secured parties beat judgment lien creditors
   - All three secured parties were perfected before judgment (Apr 1)

KEY RULE: "First to file OR perfect" - but you need attachment to be perfected!
Filing alone is just a placeholder until attachment occurs.

TRAP: Students often think Bank wins because it filed first (Jan 1). But filing
without attachment is not perfection! Finance Co perfected first (Feb 1).
        """,
        rule_statement="Priority: PMSI > First to file or perfect > Later secured parties > Judgment creditors",
        common_traps=[
            "Thinking filing alone = perfection (need attachment too)",
            "Forgetting PMSI super-priority beats earlier filers",
            "Not applying 20-day grace period correctly"
        ],
        time_limit=300
    ),

    # Level 2-3 - Proceeds, BIOC, Fixtures
    Question(
        id="st_004",
        subject="secured_transactions",
        difficulty=3,
        concept="Proceeds & BIOC",
        question_type="scenario",
        question_text="""
Bank has perfected SI in Dealer's inventory (cars). Dealer sells a car to:

Scenario A: Individual buys car for personal use from Dealer in normal course
Scenario B: Individual buys car from Dealer's employee who stole it
Scenario C: Dealer sells car, deposits $20K cash in bank account, withdraws
            $5K, deposits another $10K from other sales, withdraws $15K

Answer these questions:
1. Does individual in Scenario A take free of Bank's SI?
2. Does Bank have SI in the cash proceeds in Scenario C?
3. If Dealer defaults, how much can Bank claim from the account?
        """,
        options=[
            "A: Yes (BIOC); B: Yes; C: Bank can claim $30K",
            "A: Yes (BIOC); B: No; C: Bank can claim $20K using lowest intermediate balance rule",
            "A: No; B: No; C: Bank can claim $15K (current balance)",
            "A: Yes (BIOC); B: No; C: Bank can claim $15K using lowest intermediate balance rule",
        ],
        correct_answer=3,
        explanation="""
CORRECT: D

Scenario A - BIOC wins:
Individual is a Buyer in Ordinary Course (BIOC):
✓ Buys goods from person in business of selling goods of that kind
✓ In ordinary course (normal sale)
✓ Gives value
✓ Good faith
→ BIOC takes FREE of even perfected SI in inventory, even with knowledge!

Scenario B - Not BIOC:
Employee is not "in the business of selling" cars for Dealer.
Sale is not in ordinary course - it's theft!
Individual does NOT take free of Bank's SI.

Scenario C - Lowest Intermediate Balance Rule:
Bank's SI automatically continues in proceeds (the cash).

Account activity:
- Start: $0
- +$20K (proceeds from car) = $20K
- -$5K = $15K ← LOWEST POINT
- +$10K (other sales, not proceeds) = $25K
- -$15K = $10K (current balance)

Bank can claim: $15K (the lowest intermediate balance)
Why? We presume non-proceeds money ($10K from other sales) is still in account,
but proceeds money was withdrawn first. Lowest point = maximum proceeds remaining.

TRAPS:
1. Thinking BIOC loses if they "know" about SI (NO - knowledge irrelevant!)
2. Thinking all money in account is proceeds (NO - lowest intermediate balance rule)
3. Forgetting proceeds SI is automatic (lasts 20 days, then must re-perfect)
        """,
        rule_statement="BIOC takes free of SI in inventory even if perfected/known; SI continues in proceeds; lowest intermediate balance rule applies to commingled cash",
        common_traps=[
            "Thinking BIOC loses if they know about the SI",
            "Not applying lowest intermediate balance rule",
            "Forgetting BIOC only applies to inventory"
        ],
        time_limit=240
    ),

    # Level 4-5 - Complex hypotheticals
    Question(
        id="st_005",
        subject="secured_transactions",
        difficulty=5,
        concept="Fixtures & Bankruptcy",
        question_type="scenario",
        question_text="""
COMPLEX FACT PATTERN:

Jan 1: Bank loans money to Commercial Building Owner, gets mortgage on building,
       files in real property records

Feb 1: HVAC Company sells $100K industrial AC unit to Owner on credit (PMSI)
       Unit gets installed into building (becomes fixture)

Feb 15: HVAC files fixture filing in real property records

Mar 1: Owner files bankruptcy

Bankruptcy trustee challenges HVAC's fixture filing as a preference (90-day rule).

QUESTIONS:
1. Does HVAC have priority over Bank's mortgage?
2. Can bankruptcy trustee avoid HVAC's SI as a preference?
3. What if HVAC had filed on March 15 instead of Feb 15?
        """,
        options=[
            "1: Yes; 2: Yes (preference); 3: Trustee would win",
            "1: Yes; 2: No (20-day grace period protects); 3: HVAC would lose to trustee",
            "1: No (Bank's mortgage filed first); 2: Yes; 3: HVAC would lose",
            "1: Yes; 2: No (relates back); 3: Would still be protected",
        ],
        correct_answer=1,
        explanation="""
CORRECT: B - This tests the intersection of secured transactions and bankruptcy!

Question 1: Does HVAC beat Bank's earlier mortgage?
YES - PMSI fixture filing has super-priority if filed:
- Before goods become fixtures, OR
- Within 20 days after goods become fixtures

HVAC filed Feb 15, only 15 days after Feb 1 installation → Within grace period!
PMSI fixture super-priority beats the earlier construction mortgage.

Exception: Construction mortgage (not present here) would beat PMSI fixture.

Question 2: Can trustee avoid as preference?
NO - Trustee has strong-arm powers as of bankruptcy filing (Mar 1).
Trustee can avoid unperfected SIs and preferences within 90 days.

BUT: HVAC's Feb 15 filing RELATES BACK to Feb 1 (date of attachment) because
filed within 20-day grace period.

Relation back = Feb 1 perfection date
Feb 1 to Mar 1 = 29 days → NOT within 90-day preference period!

The 20-day grace period saves HVAC from preference attack.

Question 3: What if HVAC filed March 15 instead?
March 15 is MORE than 20 days after Feb 1 installation.
→ No relation back
→ Perfection date = March 15 (filing date)
→ March 15 to March 1 bankruptcy: LATER than bankruptcy!
→ Trustee wins as a lien creditor (has priority over unperfected SI as of Mar 1)

CRITICAL RULE: Grace periods allow relation back, which protects against:
- Other secured parties (priority relates back)
- Lien creditors/trustees (perfection relates back)

BANKRUPTCY TRUSTEE POWERS:
- Strong-arm power: status of lien creditor on bankruptcy date
- Preference power: avoid transfers within 90 days that prefer creditor
- PMSI grace period filing defeats both if it relates back beyond 90 days

This is a classic MEE question combining UCC Article 9 with bankruptcy!
        """,
        rule_statement="PMSI fixture filed within 20 days beats prior mortgage; filing within grace period relates back to attachment, defeating preference attack if beyond 90 days before bankruptcy",
        common_traps=[
            "Forgetting PMSI fixture 20-day grace period",
            "Not applying relation-back doctrine",
            "Confusing preference period with grace period",
            "Missing construction mortgage exception"
        ],
        time_limit=420
    ),
]

# ============================================================================
# WILLS, TRUSTS & ESTATES QUESTIONS
# ============================================================================

WILLS_TRUSTS_QUESTIONS = [
    # Level 1 - Basic Will Execution
    Question(
        id="wte_001",
        subject="wills_trusts_estates",
        difficulty=1,
        concept="Will Execution",
        question_type="multiple_choice",
        question_text="""
Testator, age 75 and of sound mind, handwrites a document: "I leave everything
to my daughter Sarah." Testator signs it. One witness (Testator's neighbor)
watches Testator sign and then signs as witness.

Is this a valid will?
        """,
        options=[
            "Yes - Testator had capacity, intent, signed, and had a witness",
            "No - Need TWO witnesses present at the same time",
            "Yes in states that recognize holographic wills",
            "Both B and C are correct",
        ],
        correct_answer=3,
        explanation="""
CORRECT: D - Both B and C are correct

Traditional/Attested Will Requirements (WITSAC):
- Writing ✓
- Intent ✓
- Testator 18+ and sound mind ✓
- Signature ✓
- Attestation by TWO witnesses ✗ (only has one!)
- Witnesses must be present at same time (simultaneous presence) ✗

This fails as a traditional will - needs 2 witnesses present together.

HOWEVER: Holographic Will Alternative
Some states (about half) recognize holographic wills:
- Handwritten by testator ✓
- Signed ✓
- Material provisions in testator's handwriting ✓
- NO witnesses required for holographic will ✓

In holographic will states: VALID
In non-holographic will states: INVALID (need 2 witnesses)

EXAM TIP: MEE tests on MAJORITY/COMMON LAW rules unless specified.
Unless told otherwise, assume UPC or modern trend. Iowa recognizes holographic wills.

CRITICAL DISTINCTION:
- Attested will: 2 witnesses required, can be typed
- Holographic will: No witnesses needed, must be handwritten

TRAP: Students forget the "2 witnesses present at same time" requirement!
        """,
        rule_statement="Valid will: 18+, sound mind, intent, writing, signature, TWO witnesses present simultaneously (or holographic in some states)",
        common_traps=[
            "Forgetting TWO witnesses requirement",
            "Missing 'simultaneous presence' requirement",
            "Not considering holographic will alternative"
        ],
        time_limit=90
    ),

    Question(
        id="wte_002",
        subject="wills_trusts_estates",
        difficulty=2,
        concept="Lapse & Anti-Lapse",
        question_type="scenario",
        question_text="""
Testator's 2020 will states: "I leave $50,000 to my brother Ben."

Ben dies in 2022. Testator dies in 2023, survived by:
- Ben's two children (Testator's niece and nephew)
- Testator's sister Sarah
- Testator's friend Frank

Assume state has anti-lapse statute protecting "descendants of testator's grandparents."

Who takes the $50,000?
        """,
        options=[
            "Sarah (as Testator's closest living relative)",
            "Ben's two children split it ($25K each)",
            "The residuary estate (or intestate heirs if no residuary clause)",
            "Frank (as Testator's friend named in will)",
        ],
        correct_answer=1,
        explanation="""
CORRECT: B - Ben's two children split the bequest ($25,000 each)

Step-by-step analysis:

1. DEFAULT RULE - Lapse:
   When a beneficiary predeceases testator, the gift "lapses"
   Lapsed gifts fall to residuary estate (or intestacy if no residuary)

2. ANTI-LAPSE STATUTE - Exception:
   Anti-lapse "saves" the gift IF:
   ✓ Beneficiary is in the protected class (varies by state)
   ✓ Beneficiary leaves issue (descendants)
   ✓ No contrary intent in will

3. APPLY TO BEN:
   Is Ben in protected class? "Descendants of testator's grandparents"
   - Testator's grandparents are Ben's parents
   - Ben is a descendant of testator's grandparents ✓

   Did Ben leave issue?
   - Yes, Ben has two children ✓

   Contrary intent in will?
   - No language like "if Ben survives me" ✗

4. RESULT:
   Anti-lapse statute saves the gift!
   Ben's issue (his two children) substitute for Ben.
   They split the $50,000 equally: $25,000 each

CRITICAL - Protected Class Variations:
- Some states: Only testator's descendants
- Some states: Descendants of testator's parents (siblings only)
- UPC/Modern: Descendants of testator's grandparents (siblings, nieces, nephews, cousins)
- This question uses UPC approach (grandparents)

TRAP: Students often forget to check if beneficiary is in the protected class!
Sister Sarah is also in the protected class, but she's not relevant here.

MNEMONIC - ACID:
Anti-lapse → Class protection → Issue substitute → Descendants inherit
        """,
        rule_statement="Bequest lapses if beneficiary predeceases; anti-lapse saves gift if beneficiary in protected class and leaves issue who substitute",
        common_traps=[
            "Forgetting to check protected class relationship",
            "Missing that issue substitute (not residuary)",
            "Assuming anti-lapse always applies"
        ],
        time_limit=180
    ),

    # Level 3 - Trust Creation
    Question(
        id="wte_003",
        subject="wills_trusts_estates",
        difficulty=3,
        concept="Trust Creation",
        question_type="scenario",
        question_text="""
SCENARIO:
Dad tells Son: "I'm giving you this $100,000 in the hope that you'll use it
to support your sister." Dad hands Son a check for $100,000. Son deposits it.

Dad dies one week later. Sister sues Son claiming Dad created a trust for her benefit.

Was a valid trust created?
        """,
        options=[
            "Yes - Dad had intent, gave property, and identified beneficiary (Sister)",
            "No - 'Hope' is precatory language showing no intent to create trust",
            "Yes - Oral trusts of personal property are valid",
            "No - Trusts require a writing (Statute of Frauds)",
        ],
        correct_answer=1,
        explanation="""
CORRECT: B - This was NOT a trust. Dad used precatory language.

Trust Creation Requirements (SCRIPT):
- Settlor with capacity ✓
- Capacity and intent ✓ ... or is it?
- Res (trust property) ✓
- Intent to create trust ✗ ← FAILS HERE
- Purpose (valid) ✓
- Transfer/Delivery ✓

THE CRITICAL ISSUE: Intent

Precatory Language vs Trust Intent:
- "I hope you will..."
- "It is my wish that..."
- "I request that you..."
- "I'd like you to..."

= Precatory (expressing a wish), NOT mandatory trust language

Dad said "in the hope that" = precatory language
This shows a WISH, not a binding trust obligation.

If Dad wanted a trust, he should have said:
- "I give you this $100,000 IN TRUST for your sister"
- "You shall hold this for your sister's benefit"
- "This is for your sister's support"

RESULT: This was a GIFT to Son, not a trust for Sister.
Son owns the $100,000 outright. Sister gets nothing.

Trust Intent Language (creates trust):
- "In trust for"
- "For the benefit of"
- "To hold for"
- Shall/must language

Precatory Language (no trust):
- "I hope"
- "I wish"
- "I recommend"
- "I request"

WHY THIS MATTERS:
If it's a trust → Sister is beneficiary, can enforce
If it's a gift → Son owns it, Sister gets nothing

EXAM TIP: This is tested on almost every Wills & Trusts exam!
Courts strictly interpret against finding trust if language is precatory.

Note: Oral trusts of personal property ARE generally valid (Choice C is a true
statement), but that doesn't save this - there's no trust intent at all!
        """,
        rule_statement="Trust requires: Settlor capacity/intent, res, ascertainable beneficiaries, valid purpose, delivery; precatory language shows no intent",
        common_traps=[
            "Missing precatory language issue",
            "Confusing wish with binding trust obligation",
            "Forgetting intent is a required element"
        ],
        time_limit=180
    ),

    # Level 4 - Rule Against Perpetuities
    Question(
        id="wte_004",
        subject="wills_trusts_estates",
        difficulty=5,
        concept="Rule Against Perpetuities",
        question_type="scenario",
        question_text="""
THE CLASSIC RAP TRAP:

Testator's will creates a trust: "To my daughter Alice for life, then to Alice's
children for their lives, then to Alice's grandchildren who reach age 21."

At Testator's death, Alice is alive with two children (ages 5 and 8).

Apply the Rule Against Perpetuities. What interests are valid?
        """,
        options=[
            "All interests are valid",
            "Alice's life estate is valid; everything else is void",
            "Alice's life estate and her children's life estates are valid; gift to grandchildren is void",
            "Everything is void for violating RAP",
        ],
        correct_answer=2,
        explanation="""
CORRECT: C - The gift to Alice's grandchildren VIOLATES RAP!

Let's break this down step by step:

RULE AGAINST PERPETUITIES:
"An interest must vest or fail within a life in being plus 21 years."

Step 1: Identify the interests

Interest #1: "To Alice for life"
→ Life estate to Alice
→ VESTED immediately (Alice alive and identified)
→ NOT subject to RAP (already vested)

Interest #2: "Then to Alice's children for their lives"
→ Life estates to Alice's children
→ This is a class gift to "Alice's children"
→ Class closes at Alice's death (no more children possible)
→ Alice is a "life in being" (alive when testator dies)
→ Will vest or fail at Alice's death (within Alice's lifetime)
→ VALID under RAP ✓

Interest #3: "Then to Alice's grandchildren who reach age 21"
→ Contingent remainder to Alice's grandchildren
→ Contingency: must reach age 21

Step 2: Apply RAP to Interest #3

Ask: "Might this interest vest more than 21 years after all lives in being?"

Lives in being: Alice, Alice's existing children (5 and 8 years old)

THE RAP TRAP - "The Fertile Octogenarian":
Alice could have ANOTHER child tomorrow (call her Baby).
Baby is NOT a life in being (born after testator's death).

Now imagine:
1. Alice dies next week
2. All of Alice's current children (ages 5, 8) die next year
3. Baby grows up and has a child (Grandchild) in 30 years
4. Grandchild reaches age 21 in 51 years

Vesting: 51 years after testator's death
Lives in being at testator's death: All dead within 1 year
Time to vest: 51 years = more than 21 years after all lives in being died

This VIOLATES RAP! We struck down the interest.

Step 3: What happens to the void interest?

"Then to Alice's grandchildren who reach age 21" → VOID

Result: After Alice's children die, the property reverts to testator's estate
(or goes to the residuary).

THE SOLUTION - How to draft this correctly:
"To Alice's grandchildren living at the death of the survivor of Alice and
Alice's children, who reach age 21"

OR use "alive at testator's death" as measuring lives

CLASSIC RAP TRAPS TESTED ON MEE:
1. Fertile octogenarian (person can always have more kids)
2. Precocious toddler (even young children can have kids)
3. Unborn widow (spouse not yet identified)
4. Class gift closing problems

RAP ONLY APPLIES TO:
✓ Contingent remainders
✓ Executory interests
✓ Certain class gifts
✓ Options/rights of first refusal

RAP DOES NOT APPLY TO:
✗ Vested interests
✗ Reversions to grantor
✗ Possibilities of reverter
✗ Rights of entry

MODERN TREND - Reform Statutes:
Many states have:
- "Wait and see" approach (see what actually happens)
- Cy pres (reform the gift to come within RAP)
- Abolish RAP entirely (some states)
- 90-year statutory period (UPC)

But MEE tests traditional common law RAP unless told otherwise!
        """,
        rule_statement="Interest must vest or fail within life in being plus 21 years; applies to contingent remainders, executory interests; assume all persons can have children",
        common_traps=[
            "Not considering after-born children",
            "Forgetting 'fertile octogenarian' presumption",
            "Missing that class must close within period",
            "Applying RAP to vested interests"
        ],
        time_limit=420
    ),

    # Level 5 - Complex Will Issues
    Question(
        id="wte_005",
        subject="wills_trusts_estates",
        difficulty=4,
        concept="Will Revocation & DRR",
        question_type="scenario",
        question_text="""
TIMELINE:

2020: Testator executes Will #1 leaving entire estate to Friend

2022: Testator executes Will #2 stating "I revoke all prior wills" and leaving
      entire estate to Sister

2023: Testator gets angry at Sister and tears up Will #2, saying "I want Friend
      to inherit again, not Sister."

2024: Testator dies. Estate finds torn Will #2. Will #1 cannot be found.

QUESTIONS:
1. Is Will #2 revoked?
2. What happens to Testator's estate?
        """,
        options=[
            "Will #2 is revoked; Will #1 is automatically revived; Friend inherits",
            "Will #2 is revoked; Will #1 is NOT revived; intestacy (Sister may inherit as heir)",
            "Will #2 is not revoked (torn copy is not original); Sister inherits under Will #2",
            "Will #2 is revoked by DRR doctrine; Will #1 revives; Friend inherits",
        ],
        correct_answer=1,
        explanation="""
CORRECT: B - Complicated will revocation problem!

Issue #1: Is Will #2 validly revoked?

YES - Will #2 is revoked by physical act:
Requirements for revocation by physical act:
✓ Physical act (burning, tearing, canceling, destroying)
✓ Intent to revoke
✓ By testator or at testator's direction

Testator TORE Will #2 ✓
With INTENT to revoke (said "I want Friend to inherit again") ✓
Testator did it himself ✓

Will #2 is REVOKED → Sister gets nothing under Will #2

Issue #2: Is Will #1 automatically revived?

REVIVAL RULES - Three approaches by states:

Approach #1 (Minority): Automatic Revival
- Revoking the revoking will automatically revives Will #1
- Will #1 springs back to life

Approach #2 (Minority): No Revival
- Will #1 is NOT revived absent re-execution
- Must execute Will #1 again with formalities

Approach #3 (Majority/UPC): Intent Controls
- Will #1 revived if testator INTENDED revival
- Look at circumstances and testator's statements

MAJORITY RULE (Approach #3) ANALYSIS:

Evidence of intent to revive Will #1:
+ Testator said "I want Friend to inherit again" (suggests intent)
+ Testator was specifically thinking about Will #1
- But testator never re-executed Will #1
- Will #1 cannot be found (presumption of revocation!)

MISSING WILL PRESUMPTION:
When a will was last in testator's possession but cannot be found at death:
→ Presumption that testator destroyed it with intent to revoke

Will #1 cannot be found → Presumed revoked by testator

RESULT UNDER MAJORITY RULE:
- Will #2: Revoked by tearing ✗
- Will #1: Presumed revoked (can't be found) ✗
- Testator dies INTESTATE

Intestacy distribution:
Sister may inherit as an intestate heir (if she's testator's closest relative)!

THE IRONY: Testator revoked Will #2 specifically to disinherit Sister,
but Sister might inherit anyway through intestacy!

DEPENDENT RELATIVE REVOCATION (DRR) - Why it doesn't apply here:

DRR: Revocation ineffective if based on mistake and testator would not have
revoked but for the mistake.

Could apply: Testator mistakenly thought revoking Will #2 would revive Will #1.

But DRR is a court-created safety valve used only when:
1. Clear mistake exists
2. Testator's intent is obvious
3. Applying DRR better approximates testator's intent than intestacy

Here: DRR might save Will #2 (giving to Sister) in some jurisdictions if
court finds "better than intestacy"

But typical answer: NO DRR because:
- Will #1 is missing (can't prove its contents)
- Can't give effect to testator's actual intent
- Sister inheritance under intestacy may be closer than under Will #2

EXAM TIP: This tests THREE doctrines at once:
1. Revocation by physical act ✓
2. Revival of revoked wills (depends on state rule)
3. DRR (might apply to save Will #2 in some states)

Unless DRR is specifically mentioned as available, go with standard result: INTESTACY
        """,
        rule_statement="Revoked by physical act + intent or operation of law; revival rules vary; missing will presumed revoked; DRR may save revocation based on mistake",
        common_traps=[
            "Assuming automatic revival of prior will",
            "Forgetting missing will presumption",
            "Not considering DRR application",
            "Missing that both wills may be revoked"
        ],
        time_limit=360
    ),
]

# Combine all questions
ALL_QUESTIONS = SECURED_TRANSACTIONS_QUESTIONS + WILLS_TRUSTS_QUESTIONS

# ============================================================================
# GAME ENGINE
# ============================================================================

class MEEGame:
    """Main game engine"""

    def __init__(self):
        self.stats = GameStats()
        self.current_questions = []
        self.combo_multiplier = 1.0

    def print_header(self, text: str):
        """Print colored header"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.HEADER}{text.center(80)}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.END}\n")

    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.GREEN}{Colors.BOLD}✓ {text}{Colors.END}")

    def print_error(self, text: str):
        """Print error message"""
        print(f"{Colors.RED}{Colors.BOLD}✗ {text}{Colors.END}")

    def print_info(self, text: str):
        """Print info message"""
        print(f"{Colors.CYAN}{text}{Colors.END}")

    def print_warning(self, text: str):
        """Print warning message"""
        print(f"{Colors.YELLOW}{text}{Colors.END}")

    def show_welcome(self):
        """Display welcome screen"""
        self.print_header("MEE BAR PREP GAME")
        print(f"{Colors.BOLD}Secured Transactions & Wills/Trusts/Estates{Colors.END}")
        print("\nWelcome to the ultimate study game for the TWO HARDEST MEE subjects!")
        print("\nGame Features:")
        print("  • Progressive difficulty (Levels 1-5)")
        print("  • Real MEE-style fact patterns")
        print("  • Detailed explanations with common traps")
        print("  • Combo multipliers for streaks")
        print("  • Performance tracking by subject\n")

        print(f"{Colors.YELLOW}Why These Subjects?{Colors.END}")
        print("  • Secured Transactions: Complex UCC Article 9 priority rules")
        print("  • Wills/Trusts/Estates: RAP, trust creation, will formalities")
        print("  • Both heavily tested on Iowa Bar MEE section\n")

    def show_menu(self):
        """Show main menu"""
        self.print_header("MAIN MENU")
        print("Select Game Mode:\n")
        print("  1. 🎯 Quick Practice (5 questions, mixed difficulty)")
        print("  2. 📈 Progressive Challenge (Level 1→5, increasing difficulty)")
        print("  3. ⚡ Rule Sprint (15 quick-fire questions, 60s each)")
        print("  4. 🔥 Subject Focus (Choose: Secured Trans OR Wills/Trusts)")
        print("  5. 👑 Boss Battle (2 full MEE essays, 30 min each)")
        print("  6. 📊 View Stats")
        print("  7. ❌ Exit\n")

        choice = input(f"{Colors.BOLD}Enter choice (1-7): {Colors.END}").strip()
        return choice

    def select_questions(self, mode: str, subject: str = None, count: int = 5,
                        difficulty: int = None) -> List[Question]:
        """Select questions based on mode"""
        available = ALL_QUESTIONS.copy()

        # Filter by subject if specified
        if subject:
            available = [q for q in available if q.subject == subject]

        # Filter by difficulty if specified
        if difficulty:
            available = [q for q in available if q.difficulty == difficulty]

        # Select questions
        if len(available) <= count:
            return available
        else:
            return random.sample(available, count)

    def ask_question(self, question: Question) -> bool:
        """Present question and get answer"""
        self.print_header(f"Level {question.difficulty} - {question.concept}")

        print(f"{Colors.BOLD}Subject:{Colors.END} {question.subject.replace('_', ' ').title()}")
        print(f"{Colors.BOLD}Type:{Colors.END} {question.question_type.replace('_', ' ').title()}")
        print(f"{Colors.BOLD}Time Limit:{Colors.END} {question.time_limit} seconds\n")

        print(f"{Colors.BOLD}QUESTION:{Colors.END}")
        print(question.question_text)
        print()

        # Show options
        for i, option in enumerate(question.options):
            print(f"  {chr(65+i)}. {option}")
        print()

        # Get answer with timing
        start_time = time.time()

        while True:
            answer = input(f"{Colors.BOLD}Your answer (A-{chr(65+len(question.options)-1)}): {Colors.END}").strip().upper()

            # Convert letter to index
            if answer and answer[0] in [chr(65+i) for i in range(len(question.options))]:
                answer_idx = ord(answer[0]) - 65
                break
            else:
                print(f"{Colors.RED}Invalid input. Please enter A-{chr(65+len(question.options)-1)}{Colors.END}")

        elapsed = time.time() - start_time

        # Check answer
        correct = (answer_idx == question.correct_answer)

        print()
        if correct:
            points = self.calculate_points(question.difficulty, elapsed, question.time_limit)
            self.print_success(f"CORRECT! +{points} points (x{self.combo_multiplier:.1f} multiplier)")
            self.stats.points += int(points * self.combo_multiplier)
            self.stats.correct_answers += 1
            self.stats.current_streak += 1
            self.stats.best_streak = max(self.stats.best_streak, self.stats.current_streak)

            # Update combo multiplier
            if self.stats.current_streak >= 3:
                self.combo_multiplier = min(3.0, 1.0 + (self.stats.current_streak / 10))
        else:
            self.print_error(f"INCORRECT. The correct answer was {chr(65 + question.correct_answer)}.")
            self.stats.current_streak = 0
            self.combo_multiplier = 1.0

        # Update stats
        self.stats.total_questions += 1
        self.stats.subject_scores[question.subject]['total'] += 1
        if correct:
            self.stats.subject_scores[question.subject]['correct'] += 1

        # Show explanation
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.END}")
        print(f"{Colors.BOLD}EXPLANATION:{Colors.END}\n")
        print(question.explanation)

        print(f"\n{Colors.BOLD}RULE STATEMENT:{Colors.END}")
        print(f"{Colors.YELLOW}{question.rule_statement}{Colors.END}")

        print(f"\n{Colors.BOLD}COMMON TRAPS:{Colors.END}")
        for trap in question.common_traps:
            print(f"  ⚠️  {trap}")

        print(f"\n{Colors.CYAN}{'─'*80}{Colors.END}\n")

        input(f"{Colors.BOLD}Press Enter to continue...{Colors.END}")
        return correct

    def calculate_points(self, difficulty: int, elapsed: float, time_limit: int) -> int:
        """Calculate points based on difficulty and speed"""
        base_points = difficulty * 100

        # Time bonus (up to 50% extra for speed)
        time_ratio = elapsed / time_limit
        if time_ratio < 0.5:
            time_bonus = 0.5
        elif time_ratio < 0.75:
            time_bonus = 0.25
        else:
            time_bonus = 0

        return int(base_points * (1 + time_bonus))

    def show_stats(self):
        """Display player statistics"""
        self.print_header("PERFORMANCE STATISTICS")

        print(f"{Colors.BOLD}Overall Performance:{Colors.END}")
        print(f"  Total Questions: {self.stats.total_questions}")
        print(f"  Correct: {self.stats.correct_answers}")
        print(f"  Accuracy: {self.stats.accuracy():.1f}%")
        print(f"  Total Points: {self.stats.points:,}")
        print(f"  Current Level: {self.stats.level}")
        print(f"  Current Streak: {self.stats.current_streak}")
        print(f"  Best Streak: {self.stats.best_streak}\n")

        print(f"{Colors.BOLD}Subject Breakdown:{Colors.END}\n")

        for subject, scores in self.stats.subject_scores.items():
            if scores['total'] > 0:
                acc = (scores['correct'] / scores['total'] * 100)
                subject_name = subject.replace('_', ' ').title()
                print(f"  {subject_name}:")
                print(f"    Questions: {scores['total']}")
                print(f"    Correct: {scores['correct']}")
                print(f"    Accuracy: {acc:.1f}%\n")

        # Bar exam readiness assessment
        overall_acc = self.stats.accuracy()
        print(f"{Colors.BOLD}Bar Exam Readiness:{Colors.END}")
        if overall_acc >= 80:
            self.print_success("EXCELLENT! You're crushing it! 🔥")
        elif overall_acc >= 70:
            self.print_info("GOOD! Keep practicing to reach 80%+")
        elif overall_acc >= 60:
            self.print_warning("FAIR - Focus on weak areas")
        else:
            self.print_error("NEEDS WORK - Review fundamentals")
        print()

    def run_quick_practice(self):
        """Quick practice mode"""
        self.print_header("QUICK PRACTICE MODE")
        questions = self.select_questions("quick", count=5)

        print(f"Starting 5 random questions...\n")
        time.sleep(1)

        for i, q in enumerate(questions, 1):
            print(f"\n{Colors.BOLD}Question {i}/5{Colors.END}")
            self.ask_question(q)

        self.show_session_summary()

    def run_progressive_challenge(self):
        """Progressive difficulty mode"""
        self.print_header("PROGRESSIVE CHALLENGE")
        print("You'll face 5 questions with increasing difficulty (Level 1→5)\n")
        time.sleep(1)

        for level in range(1, 6):
            questions = self.select_questions("progressive", difficulty=level, count=1)
            if questions:
                print(f"\n{Colors.BOLD}Level {level}/5{Colors.END}")
                self.ask_question(questions[0])

        self.show_session_summary()

    def run_subject_focus(self):
        """Subject-focused practice"""
        self.print_header("SUBJECT FOCUS")
        print("Choose subject:\n")
        print("  1. Secured Transactions")
        print("  2. Wills, Trusts & Estates\n")

        choice = input(f"{Colors.BOLD}Enter choice (1-2): {Colors.END}").strip()

        if choice == "1":
            subject = "secured_transactions"
            subject_name = "Secured Transactions"
        elif choice == "2":
            subject = "wills_trusts_estates"
            subject_name = "Wills, Trusts & Estates"
        else:
            print(f"{Colors.RED}Invalid choice{Colors.END}")
            return

        questions = self.select_questions("subject", subject=subject, count=10)

        print(f"\nStarting {len(questions)} questions on {subject_name}...\n")
        time.sleep(1)

        for i, q in enumerate(questions, 1):
            print(f"\n{Colors.BOLD}Question {i}/{len(questions)}{Colors.END}")
            self.ask_question(q)

        self.show_session_summary()

    def show_session_summary(self):
        """Show summary after session"""
        self.print_header("SESSION SUMMARY")
        recent_qs = min(self.stats.total_questions, 10)
        print(f"You answered {recent_qs} questions")
        print(f"Session Accuracy: {self.stats.accuracy():.1f}%")
        print(f"Points Earned: {self.stats.points:,}")
        print(f"Best Streak: {self.stats.best_streak}\n")

    def run(self):
        """Main game loop"""
        self.show_welcome()
        input(f"\n{Colors.BOLD}Press Enter to start...{Colors.END}\n")

        while True:
            choice = self.show_menu()

            if choice == "1":
                self.run_quick_practice()
            elif choice == "2":
                self.run_progressive_challenge()
            elif choice == "3":
                print(f"{Colors.YELLOW}Rule Sprint mode coming soon!{Colors.END}")
                time.sleep(2)
            elif choice == "4":
                self.run_subject_focus()
            elif choice == "5":
                print(f"{Colors.YELLOW}Boss Battle mode coming soon!{Colors.END}")
                time.sleep(2)
            elif choice == "6":
                self.show_stats()
                input(f"\n{Colors.BOLD}Press Enter to return to menu...{Colors.END}")
            elif choice == "7":
                self.print_header("THANK YOU FOR PLAYING!")
                print("Keep practicing! You've got this! 💪\n")
                self.show_stats()
                break
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
                time.sleep(1)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Run the game"""
    try:
        game = MEEGame()
        game.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Game interrupted. See you next time!{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()

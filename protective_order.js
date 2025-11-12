#!/usr/bin/env node

/**
 * Protective Order Memo Generator
 * Generates a comprehensive protective order memorandum
 */

const fs = require('fs');
const path = require('path');

function generateProtectiveOrderMemo() {
    const currentDate = new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    const memo = `
═══════════════════════════════════════════════════════════════════════════
                        MEMORANDUM IN SUPPORT OF
                    MOTION FOR PROTECTIVE ORDER
═══════════════════════════════════════════════════════════════════════════

Date: ${currentDate}

TO:      Court of [Jurisdiction]
FROM:    [Counsel for Moving Party]
RE:      Motion for Protective Order Pursuant to Rule 26(c)
         Case No.: [Case Number]

═══════════════════════════════════════════════════════════════════════════
                            I. INTRODUCTION
═══════════════════════════════════════════════════════════════════════════

The Moving Party respectfully requests that this Court enter a protective
order pursuant to Federal Rule of Civil Procedure 26(c) (or applicable state
rule) to protect confidential, proprietary, and commercially sensitive
information from improper disclosure during the discovery process in this
litigation.

═══════════════════════════════════════════════════════════════════════════
                        II. STATEMENT OF FACTS
═══════════════════════════════════════════════════════════════════════════

1. This action involves [brief description of case].

2. During the course of discovery, the parties will necessarily exchange
   information that includes:

   a. Trade secrets and proprietary business information
   b. Confidential financial data
   c. Sensitive commercial information
   d. Personal and private information
   e. Strategic business plans and analyses

3. The disclosure of such information without adequate protection would cause
   substantial competitive harm and prejudice to the disclosing parties.

4. Both parties have agreed in principle to the entry of a protective order
   [or: The Moving Party has conferred with opposing counsel regarding this
   motion as required by [applicable rule]].

═══════════════════════════════════════════════════════════════════════════
                          III. LEGAL STANDARD
═══════════════════════════════════════════════════════════════════════════

Federal Rule of Civil Procedure 26(c) provides:

    "A party or any person from whom discovery is sought may move for a
    protective order in the court where the action is pending... The court
    may, for good cause, issue an order to protect a party or person from
    annoyance, embarrassment, oppression, or undue burden or expense..."

GOOD CAUSE STANDARD:

To establish good cause, the moving party must demonstrate that:

1. A particular harm or prejudice would result from disclosure;
2. The harm or prejudice outweighs the need for discovery; and
3. The protective order is narrowly tailored to protect only legitimately
   confidential information.

See Cipollone v. Liggett Group, Inc., 785 F.2d 1108, 1121 (3d Cir. 1986);
Glenmede Trust Co. v. Thompson, 56 F.3d 476, 483 (3d Cir. 1995).

═══════════════════════════════════════════════════════════════════════════
                            IV. ARGUMENT
═══════════════════════════════════════════════════════════════════════════

A. Good Cause Exists for Entry of a Protective Order

1. SUBSTANTIAL COMPETITIVE HARM

   The information subject to this motion includes:

   • Trade secrets protected under the Uniform Trade Secrets Act
   • Proprietary business methodologies and processes
   • Confidential financial information including pricing strategies
   • Customer lists and relationships
   • Research and development information

   Disclosure of this information to competitors or the public would:

   - Destroy competitive advantages developed through substantial investment
   - Enable competitors to unfairly benefit from proprietary information
   - Cause immediate and irreparable harm to business operations
   - Violate confidentiality obligations to third parties

2. LEGITIMATE PRIVACY INTERESTS

   The discovery materials may contain:

   • Personal financial information
   • Medical records (if applicable)
   • Personnel files containing sensitive employee information
   • Social Security numbers and other personally identifiable information

   Such information implicates significant privacy interests that warrant
   protection from public disclosure.

3. INDUSTRY PRACTICE AND REASONABLE EXPECTATIONS

   It is standard practice in [industry/type of litigation] cases to enter
   protective orders governing the treatment of confidential information.

   Parties routinely and reasonably expect that sensitive business
   information disclosed in discovery will be protected from unauthorized
   disclosure and used solely for purposes of this litigation.

B. The Proposed Order Is Narrowly Tailored

The proposed protective order:

1. Applies only to information that qualifies as "Confidential" or
   "Highly Confidential - Attorneys' Eyes Only" under specifically defined
   criteria;

2. Permits the disclosure of protected information to:
   - Counsel of record and their staff
   - Experts retained for this litigation
   - The Court and court personnel
   - Court reporters and videographers
   - Named parties (except for "Attorneys' Eyes Only" material)

3. Requires recipients to agree to be bound by the order's terms;

4. Contains provisions for challenging designations;

5. Specifies procedures for handling confidential information at trial;

6. Addresses the return or destruction of confidential materials at the
   conclusion of litigation.

C. The Order Will Not Impair Legitimate Discovery Rights

The proposed protective order does not limit the SCOPE of discovery. Rather,
it governs only the USE and DISSEMINATION of information that is produced.

Opposing parties will have full access to all discovery materials necessary
to prosecute or defend this action. The order simply ensures that confidential
information is used solely for litigation purposes and not for competitive
business advantage or other improper purposes.

D. Both Parties Benefit From Mutual Protection

A protective order serves the interests of all parties by:

1. Facilitating the free exchange of information in discovery without fear
   of competitive harm;

2. Reducing disputes over individual discovery requests;

3. Avoiding the need for in camera review of each document;

4. Creating clear procedures for designation and use of confidential
   information;

5. Providing a framework for resolving disputes over confidentiality
   designations.

═══════════════════════════════════════════════════════════════════════════
                          V. CONCLUSION
═══════════════════════════════════════════════════════════════════════════

For the foregoing reasons, the Moving Party respectfully requests that this
Court enter the proposed protective order attached hereto as Exhibit A.

The order will protect legitimate confidentiality interests while ensuring
that discovery proceeds efficiently and that all parties have access to the
information necessary to litigate their claims and defenses.

═══════════════════════════════════════════════════════════════════════════
                    KEY PROVISIONS TO INCLUDE IN ORDER
═══════════════════════════════════════════════════════════════════════════

1. DEFINITIONS
   - "Confidential Information"
   - "Highly Confidential - Attorneys' Eyes Only"
   - "Producing Party"
   - "Receiving Party"
   - "Protected Material"

2. DESIGNATION PROCEDURES
   - How to designate material as confidential
   - Timing of designations
   - Form of designation (e.g., stamping "CONFIDENTIAL")

3. USE RESTRICTIONS
   - Information used solely for this litigation
   - No use for business or competitive purposes
   - Restrictions on disclosure

4. AUTHORIZED RECIPIENTS
   - Counsel and legal staff
   - Experts and consultants
   - Court personnel
   - Parties (with restrictions for AEO material)

5. CHALLENGE PROCEDURES
   - Process for challenging confidentiality designations
   - Meet and confer requirement
   - Court resolution of disputes

6. HANDLING AT DEPOSITION AND TRIAL
   - Procedures for confidential testimony
   - Sealing of trial exhibits
   - Closed courtroom provisions (if necessary)

7. DURATION AND SURVIVAL
   - Order survives conclusion of litigation
   - Return or destruction of materials
   - Continuing obligations

8. INADVERTENT DISCLOSURE
   - Clawback provisions
   - No waiver of protection

═══════════════════════════════════════════════════════════════════════════
                    PRACTICAL DRAFTING CONSIDERATIONS
═══════════════════════════════════════════════════════════════════════════

✓ Define terms clearly and specifically
✓ Create two tiers: "Confidential" and "Attorneys' Eyes Only"
✓ Include a proportionality provision to prevent over-designation
✓ Specify procedures for inadvertent disclosure (FRE 502 considerations)
✓ Address treatment of deposition testimony
✓ Include source code and technical information protocols (if applicable)
✓ Consider provisions for public filings with redactions
✓ Include provisions for third-party confidential information
✓ Address conflicts with existing confidentiality obligations
✓ Specify venue for disputes (same court or magistrate judge)

═══════════════════════════════════════════════════════════════════════════
                        SAMPLE DESIGNATION LANGUAGE
═══════════════════════════════════════════════════════════════════════════

"CONFIDENTIAL" designation shall apply to information that:

    a) Contains trade secrets or proprietary business information;
    b) Contains confidential financial, commercial, or technical information;
    c) Contains personal, private, or sensitive information; or
    d) If disclosed, would create a competitive disadvantage or cause harm
       to the disclosing party.

"HIGHLY CONFIDENTIAL - ATTORNEYS' EYES ONLY" designation shall apply to
information that is so sensitive that disclosure even to opposing parties
would create substantial risk of serious harm, including:

    a) Core trade secrets;
    b) Highly sensitive financial information;
    c) Information subject to separate confidentiality agreements; or
    d) Strategic business plans or analyses.

═══════════════════════════════════════════════════════════════════════════

                    MEMO GENERATION COMPLETE

This memorandum provides a comprehensive framework for seeking a protective
order in civil litigation. Customize as needed for your specific case and
jurisdiction.

═══════════════════════════════════════════════════════════════════════════
`;

    return memo;
}

// Generate and display the memo
console.log(generateProtectiveOrderMemo());

// Optionally save to file
const outputPath = path.join(process.cwd(), 'protective_order_memo.txt');
try {
    fs.writeFileSync(outputPath, generateProtectiveOrderMemo());
    console.log(`\n✓ Memo saved to: ${outputPath}`);
} catch (error) {
    console.log(`\n✗ Could not save file: ${error.message}`);
}

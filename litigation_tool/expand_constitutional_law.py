#!/usr/bin/env python3
"""
Expand Constitutional Law - Add 14th Amendment, 11th Amendment,
Necessary and Proper Clause, Commerce Clause, Taxing/Spending Powers, Executive Powers
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from black_letter_law import BlackLetterLawDatabase, LegalRule

def add_fourteenth_amendment_rules(db: BlackLetterLawDatabase):
    """Add 14th Amendment rules - Due Process and Equal Protection"""

    # Due Process - Procedural
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="14th Amendment - Due Process",
        subtopic="Procedural Due Process",
        title="Procedural Due Process Requirements",
        rule="When government deprives a person of life, liberty, or property, procedural due process requires: (1) notice reasonably calculated to inform; (2) meaningful opportunity to be heard; and (3) impartial decision-maker. The amount of process due depends on balancing: (a) private interest affected; (b) risk of erroneous deprivation and value of additional safeguards; and (c) government's interest including fiscal/administrative burdens.",
        elements=["Notice", "Opportunity to be heard", "Impartial decision-maker", "Mathews v. Eldridge balancing test"],
        citations=["Mathews v. Eldridge, 424 U.S. 319 (1975)", "Goldberg v. Kelly, 397 U.S. 254 (1970)", "14th Amendment"],
        notes="Threshold question: Is there a protected liberty or property interest? Liberty includes physical freedom, fundamental rights. Property requires legitimate claim of entitlement (not mere expectation). Pre-deprivation hearing generally required unless post-deprivation remedy sufficient."
    ))

    # Due Process - Substantive
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="14th Amendment - Due Process",
        subtopic="Substantive Due Process",
        title="Substantive Due Process - Fundamental Rights",
        rule="Substantive due process protects fundamental rights from government interference. Fundamental rights include: (1) rights enumerated in Constitution (e.g., 1st Amendment); (2) fundamental privacy rights (marriage, procreation, contraception, family relationships, child rearing); (3) right to refuse medical treatment. Government infringement on fundamental right triggers strict scrutiny. Non-fundamental rights (economic/social) receive only rational basis review.",
        elements=["Fundamental rights identified", "Strict scrutiny for fundamental rights", "Rational basis for non-fundamental rights", "Must be narrowly tailored to compelling interest"],
        citations=["Griswold v. Connecticut, 381 U.S. 479 (1965)", "Roe v. Wade, 410 U.S. 113 (1973)", "Washington v. Glucksberg, 521 U.S. 702 (1997)", "Dobbs v. Jackson Women's Health, 142 S. Ct. 2228 (2022)"],
        notes="Fundamental rights must be 'deeply rooted in Nation's history and tradition' or 'implicit in concept of ordered liberty' (Glucksberg test). Economic regulations receive only rational basis review (Lochner era rejected). Abortion right overturned in Dobbs (2022)."
    ))

    # 14th Amendment - Incorporation
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="14th Amendment - Incorporation",
        subtopic="Incorporation Doctrine",
        title="Selective Incorporation of Bill of Rights",
        rule="The 14th Amendment Due Process Clause incorporates most Bill of Rights protections against the states. Nearly all amendments are incorporated except: (1) 3rd Amendment (quartering soldiers); (2) 5th Amendment grand jury requirement; (3) 7th Amendment civil jury trial; and (4) 8th Amendment excessive fines. 2nd Amendment incorporated in McDonald v. Chicago (2010).",
        elements=["Due Process Clause incorporates fundamental rights", "Almost all Bill of Rights apply to states", "Exceptions: 3rd, 5th grand jury, 7th, 8th excessive fines"],
        citations=["Duncan v. Louisiana, 391 U.S. 145 (1968)", "McDonald v. Chicago, 561 U.S. 742 (2010)", "14th Amendment § 1"],
        notes="Incorporation doctrine developed through 20th century. Originally, Bill of Rights applied only to federal government (Barron v. Baltimore). Selective incorporation asks if right is 'fundamental to our scheme of ordered liberty.' Total incorporation never adopted."
    ))

    # Equal Protection - already added in previous expansion, but add more specific rule
    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="14th Amendment - Equal Protection",
        subtopic="Discriminatory Intent",
        title="Proving Discriminatory Intent",
        rule="To establish Equal Protection violation, plaintiff must prove: (1) discriminatory intent/purpose (not merely disparate impact); AND (2) law/action treats similarly situated people differently. Discriminatory intent can be shown through: (a) facial discrimination (law explicitly classifies); (b) discriminatory application of facially neutral law; or (c) facially neutral law with discriminatory motive (requires proof beyond disparate impact).",
        elements=["Discriminatory intent required", "Disparate impact alone insufficient", "Facial discrimination, discriminatory application, or discriminatory motive", "Similarly situated people treated differently"],
        citations=["Washington v. Davis, 426 U.S. 229 (1976)", "Village of Arlington Heights v. Metropolitan Housing Dev. Corp., 429 U.S. 252 (1977)", "14th Amendment § 1"],
        notes="Arlington Heights factors for discriminatory intent: (1) disparate impact; (2) historical background; (3) sequence of events leading to decision; (4) departures from normal procedures; (5) legislative/administrative history. Facial discrimination (e.g., 'white only') shows intent automatically."
    ))

def add_eleventh_amendment_rules(db: BlackLetterLawDatabase):
    """Add 11th Amendment - Sovereign Immunity rules"""

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="11th Amendment - Sovereign Immunity",
        subtopic="State Sovereign Immunity",
        title="State Sovereign Immunity from Suit",
        rule="The 11th Amendment bars federal court suits against states by: (1) citizens of another state; (2) citizens of defendant state; and (3) foreign citizens. Bars suits for both legal and equitable relief. Exceptions: (a) state consent; (b) Ex parte Young suits for prospective injunctive relief against state officers; (c) Congress abrogates pursuant to 14th Amendment § 5; (d) suits against local governments (not immune); (e) bankruptcy proceedings.",
        elements=["States immune from federal court suits", "Bars suits by own citizens and others", "Exception: state consent", "Exception: Ex parte Young (prospective relief only)", "Exception: Congressional abrogation under 14th Amendment", "Local governments NOT immune"],
        citations=["Hans v. Louisiana, 134 U.S. 1 (1890)", "Ex parte Young, 209 U.S. 123 (1908)", "Seminole Tribe v. Florida, 517 U.S. 44 (1996)", "11th Amendment"],
        notes="11th Amendment bars suits for money damages from state treasury. Ex parte Young allows prospective injunctions against state officers in their official capacity (fiction: officer violating federal law 'stripped' of state authority). Congress can abrogate only via 14th Amendment § 5, not Article I powers. Local governments (cities, counties) are not states and have no sovereign immunity."
    ))

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="11th Amendment - Sovereign Immunity",
        subtopic="Congressional Abrogation",
        title="Congressional Abrogation of State Immunity",
        rule="Congress can abrogate state sovereign immunity only when: (1) acting pursuant to 14th Amendment Section 5 (not Article I powers); (2) Congress's intent to abrogate is unmistakably clear; AND (3) the statute is congruent and proportional to remedying 14th Amendment violations. Congress cannot abrogate via Commerce Clause, Patent Clause, or other Article I powers.",
        elements=["Only 14th Amendment § 5 allows abrogation", "Clear Congressional intent required", "Must be congruent and proportional", "Article I powers cannot abrogate"],
        citations=["Seminole Tribe v. Florida, 517 U.S. 44 (1996)", "City of Boerne v. Flores, 521 U.S. 507 (1997)", "Florida Prepaid v. College Savings Bank, 527 U.S. 627 (1999)"],
        notes="Seminole Tribe held Indian Commerce Clause cannot abrogate. Congruent and proportional test: Congress must identify actual constitutional violations and tailor remedies to prevent/remedy those violations. RFRA struck down as not congruent/proportional. ADA Title I (employment) invalidated as applied to states."
    ))

def add_necessary_and_proper_clause_rules(db: BlackLetterLawDatabase):
    """Add Necessary and Proper Clause rules"""

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Necessary and Proper Clause",
        subtopic="Congressional Power",
        title="Necessary and Proper Clause Standard",
        rule="Congress may exercise powers not enumerated in Constitution if: (1) the end is legitimate (within scope of Constitution); (2) the means are appropriate and plainly adapted to that end; AND (3) the means are not prohibited by Constitution and are consistent with its letter and spirit. 'Necessary' means convenient, useful, or conducive to enumerated power - not absolutely necessary.",
        elements=["Legitimate end (enumerated power)", "Appropriate means", "Plainly adapted to the end", "Not prohibited by Constitution", "'Necessary' = useful/convenient, not essential"],
        citations=["McCulloch v. Maryland, 17 U.S. 316 (1819)", "United States v. Comstock, 560 U.S. 126 (2010)", "Art. I, § 8, cl. 18"],
        notes="McCulloch established broad construction: 'Let the end be legitimate...and all means which are appropriate...are constitutional.' Rejected narrow 'absolutely necessary' interpretation. Congress has broad discretion to choose means. Combine with enumerated power (e.g., Commerce Clause + N&P = broad regulatory power)."
    ))

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Necessary and Proper Clause",
        subtopic="Limits",
        title="Limits on Necessary and Proper Clause",
        rule="Necessary and Proper Clause does not grant independent power - must be coupled with enumerated power. Cannot use N&P to: (1) commandeer state legislatures or executives (anti-commandeering); (2) exceed scope of enumerated power it supplements; or (3) violate individual rights (e.g., Bill of Rights). NFIB v. Sebelius: cannot use N&P to create new powers, only implement existing ones.",
        elements=["No independent power - requires enumerated power", "Cannot commandeer states", "Cannot exceed enumerated power scope", "Cannot violate individual rights", "Cannot create new powers (NFIB)"],
        citations=["New York v. United States, 505 U.S. 144 (1992)", "Printz v. United States, 521 U.S. 898 (1997)", "NFIB v. Sebelius, 567 U.S. 519 (2012)"],
        notes="Anti-commandeering: Congress cannot compel states to enact/enforce federal regulatory programs. NFIB: individual mandate not valid under N&P because it created new power (compel commerce), didn't implement existing Commerce Clause power. Can condition federal funds but cannot coerce states (unconstitutional coercion in NFIB Medicaid expansion)."
    ))

def add_commerce_clause_rules(db: BlackLetterLawDatabase):
    """Add Commerce Clause rules"""

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Commerce Clause",
        subtopic="Congressional Power",
        title="Commerce Clause - Three Categories of Regulation",
        rule="Congress may regulate: (1) channels of interstate commerce (highways, waterways, internet); (2) instrumentalities of interstate commerce and persons/things in interstate commerce (cars, planes, goods, people moving interstate); AND (3) activities that substantially affect interstate commerce (economic activity, aggregated if necessary). For category 3, if non-economic intrastate activity, must show direct substantial effect (no aggregation).",
        elements=["Channels of interstate commerce", "Instrumentalities and persons/things in interstate commerce", "Activities substantially affecting interstate commerce", "Economic activity can be aggregated", "Non-economic requires direct substantial effect"],
        citations=["United States v. Lopez, 514 U.S. 549 (1995)", "United States v. Morrison, 529 U.S. 598 (2000)", "Gonzales v. Raich, 545 U.S. 1 (2005)", "Art. I, § 8, cl. 3"],
        notes="Lopez: Gun-Free School Zones Act invalid - non-economic activity without substantial effect. Morrison: Violence Against Women Act invalid - gender-motivated violence non-economic. Raich: homegrown marijuana valid target - economic activity (drug market), aggregation permitted. Post-1937 to 1995, nearly unlimited; post-Lopez, non-economic intrastate activity harder to regulate."
    ))

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Commerce Clause",
        subtopic="Limits",
        title="Commerce Clause Limits - Inactivity and Commandeering",
        rule="Commerce Clause does not permit: (1) regulating inactivity (cannot compel commerce - NFIB individual mandate invalid as Commerce Clause regulation); (2) commandeering state legislatures to enact federal programs; or (3) commandeering state executives to enforce federal law. Commerce power is broad but not unlimited - cannot regulate non-economic activity without substantial interstate effect.",
        elements=["Cannot compel commerce (regulate inactivity)", "Cannot commandeer state legislatures", "Cannot commandeer state executives", "Non-economic activity requires substantial interstate effect"],
        citations=["NFIB v. Sebelius, 567 U.S. 519 (2012)", "New York v. United States, 505 U.S. 144 (1992)", "Printz v. United States, 521 U.S. 898 (1997)"],
        notes="NFIB: individual mandate to buy health insurance exceeded Commerce Clause because it compelled commerce rather than regulated existing commerce. Upheld as tax instead. New York: cannot commandeer states to regulate radioactive waste. Printz: cannot commandeer sheriffs to conduct background checks. Congress can incentivize (spending power) but not compel states."
    ))

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Commerce Clause",
        subtopic="Dormant Commerce Clause",
        title="Dormant Commerce Clause - State Regulation Limits",
        rule="States may not: (1) discriminate against interstate commerce (strict scrutiny - must be necessary to important/compelling state interest with no less discriminatory means); or (2) impose undue burden on interstate commerce (Pike balancing - burden must not be excessive compared to putative local benefits). Exceptions: (a) market participant exception (state acting as buyer/seller); (b) Congressional authorization.",
        elements=["No discrimination against interstate commerce (strict scrutiny)", "No undue burden on interstate commerce (Pike balancing)", "Exception: market participant", "Exception: Congressional authorization"],
        citations=["City of Philadelphia v. New Jersey, 437 U.S. 617 (1978)", "Pike v. Bruce Church, Inc., 397 U.S. 137 (1970)", "South-Central Timber Dev. v. Wunnicke, 467 U.S. 82 (1984)"],
        notes="Discrimination: facial (law treats in-state and out-of-state differently), discriminatory purpose, or discriminatory effect. Strict scrutiny rarely satisfied. Pike balancing: weigh burden on interstate commerce against local benefits. Market participant: state buying/selling in market can favor own citizens (e.g., state selling timber to in-state mills). Cannot attach conditions to goods after sale (Wunnicke)."
    ))

def add_taxing_and_spending_rules(db: BlackLetterLawDatabase):
    """Add Taxing and Spending Powers rules"""

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Taxing and Spending Powers",
        subtopic="Taxing Power",
        title="Congressional Taxing Power",
        rule="Congress has broad power to tax for general welfare. Tax is valid if: (1) it raises revenue (even if minimal) OR has regulatory effect with some revenue; AND (2) not a penalty (must be a 'tax' not punishment). Courts highly deferential - will uphold tax if any revenue purpose. After NFIB v. Sebelius, functional analysis: if functions like tax (revenue to Treasury, enforced by IRS, amount not prohibitive), upheld as tax even if called 'penalty.'",
        elements=["Broad power to tax for general welfare", "Must raise some revenue OR have revenue potential", "Not a pure penalty", "NFIB functional analysis: revenue, IRS enforcement, not prohibitive"],
        citations=["United States v. Kahriger, 345 U.S. 22 (1953)", "NFIB v. Sebelius, 567 U.S. 519 (2012)", "Art. I, § 8, cl. 1"],
        notes="Pre-1937, Court struck down Child Labor Tax as penalty. Post-1937, highly deferential. NFIB: individual mandate upheld as tax - goes to Treasury via IRS, amount not prohibitive, revenue-raising function. Courts won't inquire into motive if revenue raised. Penalty vs. tax: penalty punishes unlawful conduct; tax raises revenue from lawful/unlawful conduct."
    ))

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Taxing and Spending Powers",
        subtopic="Spending Power",
        title="Conditional Spending - Dole Test",
        rule="Congress may attach conditions to federal funds granted to states if: (1) spending for general welfare; (2) condition stated unambiguously; (3) condition relates to federal interest in funding program; (4) condition does not violate other constitutional provisions; AND (5) financial inducement not so coercive as to be compulsion (NFIB). Conditions must be germane to funded program.",
        elements=["General welfare purpose", "Unambiguous condition", "Germane to federal interest", "No violation of other constitutional rights", "Not coercive (NFIB test)"],
        citations=["South Dakota v. Dole, 483 U.S. 203 (1987)", "NFIB v. Sebelius, 567 U.S. 519 (2012)", "Art. I, § 8, cl. 1"],
        notes="Dole: Congress can condition highway funds on state raising drinking age to 21. NFIB: Medicaid expansion condition coercive - threatened loss of all Medicaid funds (over 10% state budgets) = unconstitutional coercion, not mere inducement. Germaneness: condition must relate to purpose of funds. Coercion test new in NFIB - percentage of state budget relevant factor."
    ))

def add_executive_powers_rules(db: BlackLetterLawDatabase):
    """Add Executive Powers and Limits rules"""

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Executive Power",
        subtopic="Domestic Powers",
        title="Presidential Domestic Powers - Youngstown Framework",
        rule="Presidential power varies with Congressional support. Three categories (Youngstown): (1) Express/implied Congressional authorization - President's authority at maximum (includes Congressional acquiescence); (2) Congressional silence - President relies on independent powers, zone of twilight; (3) Congressional prohibition - President's power at lowest, can only rely on exclusive constitutional powers. Category 3 rarely upheld.",
        elements=["Category 1: Congressional authorization - maximum power", "Category 2: Congressional silence - twilight zone", "Category 3: Congressional prohibition - lowest power", "Must rely on exclusive constitutional power in Category 3"],
        citations=["Youngstown Sheet & Tube Co. v. Sawyer, 343 U.S. 579 (1952)", "Dames & Moore v. Regan, 453 U.S. 654 (1981)", "Medellin v. Texas, 552 U.S. 491 (2008)"],
        notes="Youngstown: Truman seizure of steel mills invalid - Congress prohibited seizure (Category 3), no exclusive Presidential power. Category 1: very broad (e.g., war powers with Congressional authorization). Category 2: Congressional acquiescence/historical practice may authorize (Dames & Moore - Iranian assets). President has no domestic lawmaking power - cannot make laws, only execute them."
    ))

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Executive Power",
        subtopic="Foreign Affairs",
        title="Executive Power in Foreign Affairs",
        rule="President has significant authority in foreign affairs: (1) sole organ of federal government in international relations; (2) power to recognize foreign governments; (3) executive agreements (not treaties - no Senate approval needed); (4) commander-in-chief of armed forces. Treaties require 2/3 Senate consent. War Powers Resolution: President must notify Congress within 48 hours of deploying troops; forces must withdraw in 60-90 days without Congressional authorization.",
        elements=["Exclusive power to recognize foreign governments", "Can make executive agreements (no Senate approval)", "Commander-in-chief power", "Treaties need 2/3 Senate consent", "War Powers Resolution: 48-hour notice, 60-90 day limit"],
        citations=["United States v. Curtiss-Wright Export Corp., 299 U.S. 304 (1936)", "Zivotofsky v. Kerry, 576 U.S. 1 (2015)", "War Powers Resolution, 50 U.S.C. §§ 1541-48"],
        notes="Curtiss-Wright: President has inherent foreign affairs powers beyond domestic powers. Zivotofsky: President's recognition power exclusive - Congress cannot require State Dept. to list 'Israel' as birthplace for Jerusalem-born. Executive agreements have force of law but don't supersede conflicting federal statutes or Constitution. War Powers Resolution constitutionality disputed but followed in practice."
    ))

    db.add_rule(LegalRule(
        subject="Constitutional Law",
        topic="Executive Power",
        subtopic="Limits",
        title="Limits on Executive Power - Separation of Powers",
        rule="Presidential power limited by: (1) cannot make laws (only execute) - line-item veto unconstitutional; (2) cannot impound appropriated funds; (3) executive privilege limited (not absolute, must yield to criminal proceedings); (4) appointment power requires Senate consent for principal officers (except recess appointments); (5) removal power limited for independent agencies (good cause required); (6) cannot violate Congressional statutes in Category 3 (Youngstown).",
        elements=["No lawmaking power (line-item veto invalid)", "Cannot impound funds", "Executive privilege qualified, not absolute", "Principal officers need Senate consent", "Limited removal power for independent agencies", "Cannot violate Congressional prohibition"],
        citations=["Clinton v. City of New York, 524 U.S. 417 (1998)", "United States v. Nixon, 418 U.S. 683 (1974)", "Myers v. United States, 272 U.S. 52 (1926)", "Humphrey's Executor v. United States, 295 U.S. 602 (1935)", "Morrison v. Olson, 487 U.S. 654 (1988)"],
        notes="Line-item veto: unconstitutional presentment clause violation (President must sign/veto bill as whole). Nixon: executive privilege yields to criminal subpoena. Appointments: principal officers need Senate consent; inferior officers can be appointed by President, courts, or dept. heads if Congress so provides. Removal: President can remove executive officers at will (Myers) but not independent agency heads without good cause (Humphrey's Executor)."
    ))

def main():
    """Expand Constitutional Law database"""

    print("="*80)
    print("EXPANDING CONSTITUTIONAL LAW - COMPREHENSIVE UPDATE")
    print("="*80)

    # Load existing database
    db_path = Path(__file__).parent / 'data' / 'black_letter_law.json'
    db = BlackLetterLawDatabase(str(db_path))

    current_const_law_rules = [r for r in db.rules if r.subject == "Constitutional Law"]
    print(f"\nCurrent Constitutional Law rules: {len(current_const_law_rules)}")

    # Add new rules
    print("\n" + "="*80)
    print("ADDING CONSTITUTIONAL LAW RULES")
    print("="*80)

    print("\nAdding 14th Amendment rules (Due Process, Equal Protection, Incorporation)...")
    add_fourteenth_amendment_rules(db)

    print("Adding 11th Amendment rules (Sovereign Immunity)...")
    add_eleventh_amendment_rules(db)

    print("Adding Necessary and Proper Clause rules...")
    add_necessary_and_proper_clause_rules(db)

    print("Adding Commerce Clause rules...")
    add_commerce_clause_rules(db)

    print("Adding Taxing and Spending Powers rules...")
    add_taxing_and_spending_rules(db)

    print("Adding Executive Powers rules...")
    add_executive_powers_rules(db)

    # Save updated database
    db.save_to_file(str(db_path))

    # Show statistics
    stats = db.get_stats()
    new_const_law_rules = [r for r in db.rules if r.subject == "Constitutional Law"]

    print("\n" + "="*80)
    print("UPDATED DATABASE STATISTICS")
    print("="*80)
    print(f"\nTotal Rules: {stats['total_rules']} (was 28)")
    print(f"Constitutional Law Rules: {len(new_const_law_rules)} (was {len(current_const_law_rules)})")
    print(f"Rules Added: {len(new_const_law_rules) - len(current_const_law_rules)}")

    # Show all Constitutional Law topics
    print("\n" + "="*80)
    print("CONSTITUTIONAL LAW TOPICS")
    print("="*80)

    const_topics = {}
    for rule in new_const_law_rules:
        if rule.topic not in const_topics:
            const_topics[rule.topic] = []
        const_topics[rule.topic].append(rule)

    for topic in sorted(const_topics.keys()):
        print(f"\n{topic}:")
        for rule in const_topics[topic]:
            print(f"  • {rule.title}")

    # Show sample rules
    print("\n" + "="*80)
    print("SAMPLE RULES")
    print("="*80)

    # 14th Amendment - Due Process
    due_process = db.get_rule('Constitutional Law', '14th Amendment - Due Process', 'Procedural Due Process')
    if due_process:
        print(f"\n{'='*80}")
        print(f"14TH AMENDMENT - {due_process.title}")
        print(f"{'='*80}")
        print(f"\n{due_process.rule}")
        print(f"\nElements:")
        for i, elem in enumerate(due_process.elements, 1):
            print(f"  {i}. {elem}")

    # Commerce Clause
    commerce = db.get_rule('Constitutional Law', 'Commerce Clause', 'Congressional Power')
    if commerce:
        print(f"\n{'='*80}")
        print(f"COMMERCE CLAUSE - {commerce.title}")
        print(f"{'='*80}")
        print(f"\n{commerce.rule}")
        print(f"\nThree Categories:")
        for i, elem in enumerate(commerce.elements, 1):
            print(f"  {i}. {elem}")

    # Executive Power
    exec_power = db.get_rule('Constitutional Law', 'Executive Power', 'Domestic Powers')
    if exec_power:
        print(f"\n{'='*80}")
        print(f"EXECUTIVE POWER - {exec_power.title}")
        print(f"{'='*80}")
        print(f"\n{exec_power.rule}")
        print(f"\nYoungstown Categories:")
        for i, elem in enumerate(exec_power.elements, 1):
            print(f"  {i}. {elem}")

    print("\n" + "="*80)
    print(f"✅ Constitutional Law expanded and saved to: {db_path}")
    print("="*80)

    print("\n📚 Total Constitutional Law Coverage:")
    print("  • 1st Amendment (2 rules)")
    print("  • 4th Amendment (1 rule)")
    print("  • 11th Amendment (2 rules)")
    print("  • 14th Amendment (4 rules)")
    print("  • Commerce Clause (3 rules)")
    print("  • Equal Protection (2 rules)")
    print("  • Executive Power (3 rules)")
    print("  • Necessary and Proper Clause (2 rules)")
    print("  • Taxing and Spending Powers (2 rules)")
    print(f"\n  TOTAL: {len(new_const_law_rules)} Constitutional Law rules")

if __name__ == '__main__':
    main()

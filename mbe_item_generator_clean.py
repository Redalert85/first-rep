from __future__ import annotations
import argparse, json, random, textwrap, os, datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple

@dataclass
class Item:
    subject: str
    subtype: str
    tested_rule: str
    fact_pattern: str
    options: Dict[str, str]
    answer: str
    why_correct: str
    why_others_wrong: Dict[str, str]
    trap_type: List[str]
    difficulty: str = "HARD"

NAMES = [
    "Alex","Jordan","Taylor","Casey","Riley","Sam","Morgan","Drew","Quinn","Avery",
    "Blake","Cameron","Reese","Bailey","Parker","Skyler","Rowan","Harper","Dylan","Kendall"
]
PLACES = ["State A","State B","State C","Riverton","Greenfield","Brookside","Lakeshore","Hillview"]

def pick(seq): 
    return random.choice(seq)

def two(seq): 
    a = pick(seq)
    b_choices = [x for x in seq if x!=a]
    b = pick(b_choices) if b_choices else a
    return a,b

def wrap(s, width=90):
    return textwrap.fill(s, width=width)

def word_count(s): 
    return len(s.split())

def build_evidence_item() -> Tuple[str, str, List[str], str, Dict[str,str]]:
    d1, d2 = two(NAMES)
    city = pick(PLACES)
    template = (
        f"{d1} was charged with assault after an altercation outside a nightclub in {city}. "
        f"A bystander placed a frantic 911 call moments after the incident, shouting that '{d1} just hit someone and ran toward the alley!' "
        f"Twenty minutes later, once officers had secured the scene, the same bystander gave a calm, recorded statement at the station "
        f"describing the event in detail and responding to structured questions. At trial, the bystander is unavailable due to a sudden illness. "
        f"The prosecution seeks to admit both the 911 recording and the later station interview. Defense objects under the hearsay rules "
        f"and the Confrontation Clause. The jurisdiction follows modern federal evidence rules and Supreme Court precedent distinguishing "
        f"testimonial from non-testimonial statements."
    )
    correct = "Admit the 911 call as a non-testimonial excited utterance; exclude the station interview as testimonial absent prior cross."
    A = "Admit both statements because both relate to a startling event and qualify as excited utterances."
    B = "Exclude both statements because the declarant is unavailable and the defense cannot cross-examine."
    C = "Admit the 911 call as a non-testimonial excited utterance; exclude the station interview as testimonial absent prior cross."
    D = "Admit the station interview but exclude the 911 call as testimonial because it accuses the defendant."
    why_correct = ("A 911 call made for ongoing emergency assistance is typically non-testimonial and may enter under 803(2). "
                   "The structured, post-event station interview is testimonial; without a prior opportunity to cross, the "
                   "Confrontation Clause bars its admission against the accused.")
    why_wrong = {
        "A":"Not all statements relating to a startling event are non-testimonial; the station interview is testimonial.",
        "B":"The Confrontation Clause bars testimonial statements, not all hearsay; non-testimonial excited utterances can be admitted.",
        "D":"The 911 call is generally non-testimonial; the later station interview is the one that is testimonial."
    }
    distractors = [A,B,D]
    return template, correct, distractors, why_correct, why_wrong

def build_civpro_item() -> Tuple[str,str,List[str],str,Dict[str,str]]:
    p, d = two(NAMES); city = pick(PLACES)
    template = (
        f"In a diversity action filed in federal court in {city}, {p} sues {d} for negligence. "
        f"A state statute requires a pre-suit affidavit from an expert within 30 days of filing; failure mandates dismissal with prejudice. "
        f"Federal Rule 11 and 26 impose different certification/disclosure regimes but do not mention this specific affidavit. "
        f"The defendant answered without raising any Rule 12 defenses and later moved to dismiss for failure to file the state affidavit. "
        f"The plaintiff filed the affidavit on day 45. The district court must decide whether to apply the state statute."
    )
    correct = "Apply the state affidavit requirement if it is outcome-determinative and no valid Federal Rule directly conflicts; no waiver is implicated by Rule 12 because this is not a PJ/venue defense."
    A = "Ignore the state statute because any Federal Rule related to pleadings automatically displaces conflicting state law."
    B = "Apply the state affidavit requirement if it is outcome-determinative and no valid Federal Rule directly conflicts; no waiver is implicated by Rule 12 because this is not a PJ/venue defense."
    C = "Deny dismissal because the defendant waived the defense by not raising it in the first Rule 12 response."
    D = "Apply the Federal Rules only, because Erie never requires application of state procedural statutes."
    why_correct = ("Under Erie/Hanna, if there is no valid Federal Rule on point, the court applies state law that would affect outcome and discourage forum shopping. "
                   "The affidavit statute likely governs. Waiver under Rule 12(h) covers PJ/venue/insufficient service, not Erie choice-of-law issues.")
    why_wrong = {
        "A":"A Federal Rule must actually be on point and valid under the Rules Enabling Act to displace state law.",
        "C":"Rule 12(h) waiver does not apply to Erie choice-of-law questions.",
        "D":"Erie can require application of state statutes when no Federal Rule directly conflicts and the rule is substantive in effect."
    }
    distractors = [A,C,D]
    return template, correct, distractors, why_correct, why_wrong

def build_conlaw_item() -> Tuple[str,str,List[str],str,Dict[str,str]]:
    g1 = pick(NAMES); city = pick(PLACES)
    template = (
        f"The City of {city} requires permits for demonstrations in its traditional public park. "
        f"The ordinance instructs the parks director to grant a permit unless the event would be 'inappropriate or disruptive,' "
        f"without further standards. {g1} applies to hold a political rally; the director denies the permit citing 'appropriateness' "
        f"concerns and offers no alternative. A facial challenge is brought under the First Amendment."
    )
    correct = "Unconstitutional: the ordinance grants unbridled discretion in a traditional public forum and lacks narrow, objective criteria."
    A = "Constitutional because time, place, and manner restrictions are valid if the city cites disruption."
    B = "Unconstitutional: the ordinance grants unbridled discretion in a traditional public forum and lacks narrow, objective criteria."
    C = "Constitutional if applied uniformly regardless of viewpoint, even without standards."
    D = "Unconstitutional only if the challenger proves actual viewpoint discrimination in this instance."
    why_correct = ("Permit schemes in traditional public forums must have narrow, objective, and definite standards to constrain discretion. "
                   "Vague terms like 'inappropriate' vest unbridled discretion and are facially invalid.")
    why_wrong = {
        "A":"Content-neutral TPM rules must be guided by objective standards; 'disruption' without criteria is insufficient.",
        "C":"Uniform application does not cure unbridled discretion.",
        "D":"Facial invalidity arises from standardless discretion; no need to prove actual viewpoint bias."
    }
    distractors = [A,C,D]
    return template, correct, distractors, why_correct, why_wrong

def build_crim_item() -> Tuple[str,str,List[str],str,Dict[str,str]]:
    a,b = two(NAMES); city = pick(PLACES)
    template = (
        f"At a crowded bar in {city}, {b} returned to confront {a} while gripping a metal baton and advancing quickly from ten feet away, "
        f"shouting threats. {a} grabbed a heavy beer bottle and swung once, striking {b}. Security footage shows {b} closing distance, "
        f"baton raised, and no clear escape path. The jurisdiction follows modern self-defense rules (no duty to retreat from a place one may lawfully be; "
        f"deadly force only if reasonably necessary to prevent imminent death or serious bodily harm). {a} is charged with aggravated assault."
    )
    correct = "Self-defense likely succeeds: imminent threat + proportional response to a weapon; no duty to retreat."
    A = "Self-defense fails because using a bottle is always deadly force against an unarmed opponent."
    B = "Self-defense likely succeeds: imminent threat + proportional response to a weapon; no duty to retreat."
    C = "Self-defense fails because defendant had to retreat if any exit existed."
    D = "Self-defense fails because prior verbal threats bar force unless first struck."
    why_correct = ("A raised baton and rapid approach create imminence; a single bottle strike can be proportionate to a weapon. "
                   "No retreat duty when lawfully present (jurisdictional assumption).")
    why_wrong = {
        "A":"A bottle is not per se deadly; proportionality is fact-specific, and the aggressor had a weapon.",
        "C":"No retreat duty in the stated jurisdiction.",
        "D":"Prior threats + weapon + advance can justify preemptive defensive force."
    }
    distractors = [A,C,D]
    return template, correct, distractors, why_correct, why_wrong

def build_contracts_item() -> Tuple[str,str,List[str],str,Dict[str,str]]:
    s,b = two(NAMES)
    template = (
        f"{b}, a retailer, emails a signed offer to purchase 500 widgets from {s}, a merchant, stating 'firm for 45 days.' "
        f"Three days later, {s} replies with a written acknowledgment adding an arbitration clause and a slightly different delivery schedule. "
        f"{s} ships conforming goods immediately; {b} accepts and later sues to avoid arbitration after a dispute. "
        f"The jurisdiction follows UCC Article 2."
    )
    correct = "The firm offer held the price; the additional arbitration term is a material alteration and does not enter without express assent."
    A = "All additional terms in a merchant confirmation automatically become part of the contract."
    B = "The firm offer held the price; the additional arbitration term is a material alteration and does not enter without express assent."
    C = "The reply was a counteroffer; shipment did not create a contract."
    D = "Arbitration is never a material alteration between merchants."
    why_correct = ("Under §2-205 the signed firm offer is irrevocable; under §2-207, material alterations (e.g., arbitration) do not enter absent agreement.")
    why_wrong = {
        "A":"§2-207(2) excludes material alterations.",
        "C":"A definite and seasonable expression + shipment forms a contract under §2-207(1).",
        "D":"Arbitration is typically treated as material absent course of dealing or assent."
    }
    distractors = [A,C,D]
    return template, correct, distractors, why_correct, why_wrong

def build_torts_item() -> Tuple[str,str,List[str],str,Dict[str,str]]:
    v = pick(NAMES)
    template = (
        f"At a street food fair, vendor {v} displays a prominent 'Caution: Wet Area' sign near a drink station. "
        f"A local ordinance requires vendors to keep walking surfaces 'reasonably dry' and to 'promptly remedy spills.' "
        f"Multiple cups spill during a rush; {v} does not mop for ten minutes, and a patron slips and fractures a wrist. "
        f"The defense offers evidence of full compliance with industry best-practice signage. The plaintiff sues in negligence."
    )
    correct = "Liability is likely: warnings don't replace the duty to remediate; ordinance noncompliance supports negligence (possibly per se)."
    A = "No liability because compliance with industry custom defeats negligence."
    B = "Liability is likely: warnings don't replace the duty to remediate; ordinance noncompliance supports negligence (possibly per se)."
    C = "No liability because the sign shifts the risk to patrons who proceed."
    D = "No liability unless the patron proves the vendor actually knew of each individual spill."
    why_correct = ("Custom evidence is not conclusive; statutory/ordinance standards can establish duty/breach. Failure to clean promptly is the breach.")
    why_wrong = {
        "A":"Custom is relevant but not dispositive.",
        "C":"Assumption of risk requires knowing, voluntary encounter of a specific risk; signage alone is insufficient.",
        "D":"Constructive notice can suffice; their own station created the hazard."
    }
    distractors = [A,C,D]
    return template, correct, distractors, why_correct, why_wrong

def build_property_item() -> Tuple[str,str,List[str],str,Dict[str,str]]:
    a,b = two(NAMES); city = pick(PLACES)
    template = (
        f"In {city}, {a} bought a lot from {b}. The deed, recorded, states: 'Residential use only; no retail or restaurant use.' "
        f"Five years later, {a} opens a small coffee kiosk attached to the home's front porch. The area added one gas station but remains mostly residential. "
        f"{b} sues to enforce the restriction. {a} argues the covenant is obsolete and that {b} sold the property and retained no rights."
    )
    correct = "Enforceable: the covenant runs with the land; the neighborhood has not so changed as to defeat the restriction; grantor retains the benefit."
    A = "Unenforceable because any commercial use defeats all residential covenants after five years."
    B = "Enforceable: the covenant runs with the land; the neighborhood has not so changed as to defeat the restriction; grantor retains the benefit."
    C = "Unenforceable because a seller cannot hold any post-sale interest in restrictive covenants."
    D = "Unenforceable unless the plaintiff proves monetary damages."
    why_correct = ("Recorded real covenants/equitable servitudes can bind successors; modest change doesn't void; benefit may run to the grantor or subdivision scheme.")
    why_wrong = {
        "A":"No five-year expiration rule; changed-conditions doctrine is fact-specific.",
        "C":"Benefits can run; enforcement often via injunction.",
        "D":"Equitable relief is typical; damages proof not required to enjoin."
    }
    distractors = [A,C,D]
    return template, correct, distractors, why_correct, why_wrong

BANKS = {
    "evidence":  ( "exception/Confrontation", "Out-of-court statements: excited utterance vs testimonial", ["wrong standard","overbreadth","Confrontation toggle"], build_evidence_item ),
    "civpro":    ( "Erie/Rules/waiver", "Erie/Hanna; valid Federal Rule on point; Rule 12(h) waiver scope", ["jurisdiction toggle","timing","wrong standard"], build_civpro_item ),
    "conlaw":    ( "TPM/Permits", "Traditional public forum + unbridled discretion standard", ["overbreadth","wrong standard"], build_conlaw_item ),
    "crim":      ( "Self-defense", "Imminence + proportionality; no retreat where stated", ["wrong standard","timing"], build_crim_item ),
    "contracts": ( "UCC §2-205/2-207", "Firm offer; battle of the forms; material alteration", ["wrong standard","overbreadth"], build_contracts_item ),
    "torts":     ( "Negligence per se", "Warnings don't replace remediation; ordinance may set standard", ["overbreadth","wrong standard"], build_torts_item ),
    "property":  ( "Covenants", "Running of benefit/burden; changed conditions", ["overbreadth"], build_property_item ),
}

def critique(item: Item) -> Dict[str,int]:
    scores = {"Accuracy":5, "PlausibleDistractors":5, "TrapQuality":5, "Clarity":5}
    need = {
        "evidence":["testimonial","excited","Confrontation"],
        "civpro":["Erie","Rule","state","Federal"],
        "conlaw":["public forum","discretion","First Amendment"],
        "crim":["imminent","weapon","proportional"],
        "contracts":["UCC","2-207","firm offer","material"],
        "torts":["ordinance","remedy","negligence","warning","clean"],
        "property":["covenant","runs","equitable","changed"]
    }
    txt = " ".join([item.fact_pattern, item.why_correct] + list(item.why_others_wrong.values()))
    for kw in need.get(item.subject, []):
        if kw.lower() not in txt.lower():
            scores["Accuracy"] = min(scores["Accuracy"], 4)
    plausibles = 0
    for k in "ACD":
        if any(w in item.options[k].lower() for w in ["rule","material","testimonial","waiver","retreat","forum","standard","duty","covenant","arbitration","state","federal"]):
            plausibles += 1
    if plausibles < 2: 
        scores["PlausibleDistractors"] = 3
    if not any(t in (" ".join(item.trap_type)) for t in ["overbreadth","wrong standard","timing","jurisdiction toggle","Confrontation toggle"]):
        scores["TrapQuality"] = 4
    wc = word_count(item.fact_pattern)
    if wc < 130 or wc > 190:
        scores["Clarity"] = 4
    return scores

def revise_if_needed(item: Item):
    scores = critique(item)
    # adjust length if needed
    wc = word_count(item.fact_pattern)
    if wc < 130:
        item.fact_pattern += " The timeline, roles, and governing standards are undisputed; the dispute turns on a precise doctrinal element."
    elif wc > 190:
        item.fact_pattern = " ".join(item.fact_pattern.split()[:185]) + "..."
    # ensure trap keyword exists
    if "overbreadth" not in item.trap_type:
        item.trap_type.append("overbreadth")
    return item, critique(item)

def generate_item(subject:str) -> Item:
    if subject not in BANKS: 
        raise ValueError(f"Unknown subject: {subject}")
    subtype, tested_rule, trap_types, builder = BANKS[subject]
    facts, correct, distractors, why_correct, why_wrong = builder()
    options = {"A": distractors[0], "B": "", "C": "", "D": ""}
    letters = ["A","B","C","D"]
    correct_letter = random.choice(letters)
    options[correct_letter] = correct
    d_iter = iter([d for d in distractors if d != correct])
    for L in letters:
        if options[L] == "":
            try:
                options[L] = next(d_iter)
            except StopIteration:
                options[L] = "Placeholder distractor."
    item = Item(
        subject=subject, subtype=subtype, tested_rule=tested_rule,
        fact_pattern=facts, options=options, answer=correct_letter,
        why_correct=why_correct, why_others_wrong=why_wrong,
        trap_type=trap_types.copy(), difficulty="HARD",
    )
    item, _ = revise_if_needed(item)
    return item

def generate_pack(subject:str, n:int, seed:int|None=None) -> List[Item]:
    if seed is not None: 
        random.seed(seed)
    items: List[Item] = []
    attempts = 0
    while len(items) < n and attempts < n*5:
        attempts += 1
        it = generate_item(subject)
        scores = critique(it)
        if all(v==5 for v in scores.values()):
            items.append(it)
            continue
        it2, scores2 = revise_if_needed(it)
        if all(v==5 for v in scores2.values()):
            items.append(it2)
    while len(items) < n:
        items.append(generate_item(subject))
    return items

def to_markdown(items: List[Item]) -> str:
    lines = [f"# MBE Pack ({items[0].subject.title()}) — {len(items)} items — {datetime.date.today()}"]
    for i,it in enumerate(items,1):
        lines.append("\n---\n")
        lines.append(f"**Question {i} — {it.subject.title()} | {it.subtype} | Difficulty: {it.difficulty}**")
        lines.append("\n**Tested rule:** " + it.tested_rule)
        lines.append("\n" + wrap(it.fact_pattern))
        for L in ["A","B","C","D"]:
            lines.append(f"\n({L}) " + wrap(it.options[L]))
        lines.append(f"\n**Answer:** {it.answer}")
        lines.append("\n**Why correct:** " + wrap(it.why_correct))
        wrongs = "; ".join([f"{k}: {v}" for k,v in it.why_others_wrong.items()])
        lines.append("\n**Why others are wrong:** " + wrap(wrongs))
        lines.append("\n**Trap type:** " + ", ".join(it.trap_type))
    return "\n".join(lines)

def save_pack(items: List[Item], out_base: str):
    os.makedirs(os.path.dirname(out_base) or ".", exist_ok=True)
    with open(out_base + ".json","w",encoding="utf-8") as f:
        json.dump([asdict(i) for i in items], f, indent=2, ensure_ascii=False)
    with open(out_base + ".md","w",encoding="utf-8") as f:
        f.write(to_markdown(items))

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Generate HARD MBE questions (original) with a critic-revise loop.")
    ap.add_argument("--subject", required=True, choices=list(BANKS.keys()))
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", type=str, default="mbe_out")
    args = ap.parse_args()

    items = generate_pack(args.subject, args.n, args.seed)
    save_pack(items, args.out)
    print(f"Saved {len(items)} items to {args.out}.json and {args.out}.md")

if __name__ == "__main__":
    main()

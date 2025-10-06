# HARD MBE Item Generator

Generates ultra-challenging MBE questions with competing doctrines and sophisticated traps. Creates questions at National-style difficulty that rival the California Bar Exam.

## Features

- **HARD Difficulty**: Questions with competing doctrines, overbroad rule temptations, and precise distractor flaws
- **Complete JSON Format**: Structured output with tested rules, trap types, and detailed explanations
- **7 Subjects**: evidence, civpro, conlaw, crim, contracts, torts, property
- **Reproducible**: Seed-based generation for consistent testing
- **No Dependencies**: Pure Python implementation

## Usage

```bash
# Generate 5 evidence questions
python mbe_item_generator.py --subject evidence --n 5 --seed 42 --out out/mbe_evidence

# Generate 3 constitutional law questions
python mbe_item_generator.py --subject conlaw --n 3 --seed 123 --out out/mbe_conlaw
```

## Output Format

Each question follows this HARD MBE structure:

```json
{
  "subject": "Evidence",
  "subtype": "exception",
  "tested_rule": "One-sentence black-letter rule",
  "fact_pattern": "130-180 word realistic scenario",
  "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
  "answer": "B",
  "why_correct": "1-2 sentence explanation",
  "why_others_wrong": {"A": "...", "C": "...", "D": "..."},
  "trap_type": ["overbreadth", "wrong standard", "timing"],
  "difficulty": "HARD"
}
```

## HARD Question Characteristics

- **Competing Doctrines**: At least 2 rules in tension
- **Sophisticated Traps**: 2-3 plausible distractors with precise flaws
- **Overbroad Temptations**: Facts designed to mislead with too-broad applications
- **Precise Analysis**: Requires exact application of legal standards
- **Realistic Scenarios**: Bar-exam level fact patterns and procedural contexts

## Subjects Available

- `evidence` - Character evidence, hearsay, authentication, relevance
- `civpro` - Jurisdiction, venue, pleading, choice of law
- `conlaw` - Equal protection, due process, First Amendment
- `crim` - Mens rea, accomplice liability, defenses
- `contracts` - Consideration, remedies, statute of frauds
- `torts` - Intent, negligence, strict liability
- `property` - Adverse possession, easements, title

## Integration

Questions can be integrated into bar prep tools like `bar_tutor.py` for advanced MBE practice with AI-powered explanations and performance tracking.

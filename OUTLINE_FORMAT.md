# Outline Import Format Guide

## Supported Formats

### PDF Format (.pdf) - NEW!

**Best for:** Barbri, Themis, or other commercial outlines in PDF format

```bash
# Install PDF support first:
pip install PyPDF2

# Then import:
python3 import_pdf.py outline.pdf
```

**What works well:**
- Structured outlines with clear section headers
- Content labeled with RULE:, ELEMENTS:, EXCEPTIONS:, etc.
- Organized by topics and subtopics

**Auto-detection:**
- Automatically detects subjects from content
- Parses section headers (RULE, ELEMENTS, TRAPS, etc.)
- Identifies topics from Roman numerals or numbered sections
- Filters out page headers/footers

**Note:** Works best with text-based PDFs (not scanned images)

### Markdown Format (.md)

```markdown
## Subject Name

### Topic Name

#### Section Type: Title
Content here...
```

**Example:**

```markdown
## Contracts

### Offer and Acceptance

#### Rule: Mailbox Rule
Acceptance is effective upon dispatch when sent by mail...

#### Elements: Valid Offer
An offer requires:
• Manifestation of intent
• Certainty of terms
• Communication to offeree

#### Traps: Revocation
Common mistakes:
• Option contracts cannot be revoked
• UCC firm offers
```

### Plain Text Format (.txt)

```
SUBJECT: Subject Name
TOPIC: Topic Name
SECTION_TYPE: Title
Content here...
```

**Example:**

```
SUBJECT: Contracts
TOPIC: Offer and Acceptance

RULE: Mailbox Rule
Acceptance is effective upon dispatch when sent by mail...

ELEMENTS: Valid Offer
An offer requires:
• Manifestation of intent
• Certainty of terms
• Communication to offeree

TRAPS: Revocation
Common mistakes:
• Option contracts cannot be revoked
• UCC firm offers
```

## Recognized Section Types

The importer automatically detects these section types:

- **RULE** → Creates "rule" type cards
- **ELEMENTS** → Creates "elements" type cards
- **EXCEPTIONS** / **DEFENSES** → Creates "exceptions" type cards
- **TRAPS** / **PITFALLS** / **MISTAKES** → Creates "traps" type cards
- **POLICY** / **RATIONALE** → Creates "policy" type cards

## Supported Subjects

- contracts
- torts
- constitutional_law
- criminal_law
- criminal_procedure
- civil_procedure
- evidence
- real_property
- professional_responsibility
- corporations
- wills_trusts_estates
- family_law
- secured_transactions
- iowa_procedure

## Features

### Automatic Processing

1. **Card Type Detection** - Automatically assigns appropriate card type based on section header
2. **Difficulty Estimation** - Estimates difficulty (1-5 stars) based on content length:
   - < 30 words: Basic (⭐⭐)
   - 30-60 words: Intermediate (⭐⭐⭐)
   - 60-100 words: Advanced (⭐⭐⭐⭐)
   - 100+ words: Expert (⭐⭐⭐⭐⭐)
3. **Topic Grouping** - Keeps cards organized by subject and topic
4. **Preview** - Shows sample cards before importing
5. **Statistics** - Displays breakdown by subject, type, and difficulty

### Front Card Format

```
[TYPE] Topic Name

Section Title
```

### Back Card Format

```
Content from outline
```

## Usage

### Basic Import

```bash
python3 import_outline.py outline.md
```

### Preview Without Importing

```bash
# Import will ask for confirmation
# Type 'n' to cancel after preview
python3 import_outline.py outline.md
```

### Example Workflow

1. Create your outline in markdown:

```markdown
## Contracts

### Consideration

#### Rule: Bargained-For Exchange
Consideration requires something of legal value...

#### Exceptions: Past Consideration
Past consideration is NOT valid because...
```

2. Import the outline:

```bash
python3 import_outline.py my_contracts_outline.md
```

3. Review the preview and statistics

4. Confirm import (y/n)

5. Study the new cards:

```bash
python3 daily_study.py
python3 subject_study.py
```

## Tips

### Best Practices

- **Keep sections concise** - Shorter cards are easier to review
- **Use bullet points** - Makes content scannable
- **Include examples** - Helps with retention
- **Add mnemonics** - Include memory aids in the content
- **Break up complex topics** - Multiple simple cards > one complex card

### Content Organization

**Good:**
```markdown
#### Rule: Statute of Frauds
The Statute of Frauds requires written evidence for:
• Contracts for sale of land
• Contracts not performable within one year
• Promises to pay another's debt
• Marriage contracts
• UCC: goods ≥ $500
```

**Better:**
```markdown
#### Rule: Statute of Frauds - Land Contracts
Land sale contracts must be in writing.

Writing must contain:
• Parties
• Property description
• Price
• Signature of party to be charged

#### Rule: Statute of Frauds - One Year Rule
Contracts not performable within one year from signing must be in writing.

Key: Measured from date of agreement, not performance start date
```

### Common Patterns

**For Rules:**
```markdown
#### Rule: Topic Name
[Rule statement]

[Key points or requirements]

[Exceptions if brief]
```

**For Elements:**
```markdown
#### Elements: Topic Name
To prove [topic], plaintiff must show:
1. Element one
2. Element two
3. Element three

[Memory aid or mnemonic]
```

**For Traps:**
```markdown
#### Traps: Topic Name
Common mistakes:
• Trap 1 - explanation
• Trap 2 - explanation
• Trap 3 - explanation
```

## Troubleshooting

### No cards generated?

Check that:
- Subject headers use `##` (markdown) or `SUBJECT:` (text)
- Section headers use `####` (markdown) or section type keywords (text)
- File encoding is UTF-8

### Wrong subject assigned?

Subject names must match one of the 14 Iowa Bar subjects. Use underscores or spaces:
- `## Constitutional Law` ✓
- `## constitutional_law` ✓
- `## Con Law` ✗ (too abbreviated)

### Cards not showing up in study?

All imported cards start with:
- `next_review = NULL` (due immediately)
- `interval = 1` day
- `ease_factor = 2.5`

They should appear in your next study session.

## Advanced: Bulk Import

Import multiple outlines:

```bash
for file in outlines/*.md; do
    echo "Importing $file..."
    python3 import_outline.py "$file" <<< "y"
done
```

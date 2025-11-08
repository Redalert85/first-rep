# Knowledge Base Import Guide

## Overview

The `import_knowledge_to_adaptive.py` script converts existing `KnowledgeNode` concepts from your bar prep system into the new Adaptive Learning System format with proper enum-based typing and SM-2 spaced repetition.

## What It Does

### 1. Subject Mapping

Automatically maps old subject strings to new `Subject` enum:

| Old Format | New Enum |
|-----------|----------|
| `"civil_procedure"` | `Subject.CIVIL_PROCEDURE` |
| `"constitutional_law"` | `Subject.CONSTITUTIONAL_LAW` |
| `"contracts"` | `Subject.CONTRACTS` |
| `"torts"` | `Subject.TORTS` |
| `"criminal_law"` | `Subject.CRIMINAL_LAW` |
| `"criminal_procedure"` | `Subject.CRIMINAL_PROCEDURE` |
| `"evidence"` | `Subject.EVIDENCE` |
| `"real_property"` | `Subject.REAL_PROPERTY` |

### 2. Intelligent Topic Mapping

Uses keyword matching to map concepts to specific topics:

**Constitutional Law** (35 topics):
- Detects keywords like "strict scrutiny", "commerce clause", "due process"
- Maps to `ConstitutionalLawTopic` enum values

**Evidence** (50+ topics):
- Detects keywords like "hearsay", "403", "impeachment"
- Maps to `EvidenceTopic` enum values

**Other Subjects**:
- Uses concept name as topic identifier

### 3. Multi-Card Generation

Each `KnowledgeNode` generates multiple learning cards:

| Card Type | Generated When | Example |
|-----------|---------------|---------|
| **Rule Statement** | `rule_statement` field present | "State the rule for: Strict Scrutiny" |
| **Elements** | `elements` list has content | "What are the elements of Negligence?" |
| **Common Traps** | `common_traps` list present | "What are common exam traps for Hearsay?" |
| **Exceptions** | `exceptions` list present | "What are the exceptions to Hearsay?" |
| **Policy** | `policy_rationales` list present | "What policy rationales support Takings?" |

### 4. Difficulty Mapping

| Old Difficulty (1-5) | New DifficultyLevel |
|---------------------|---------------------|
| 1 | FOUNDATIONAL |
| 2-3 | INTERMEDIATE |
| 4 | ADVANCED |
| 5 | BAR_EXAM_LEVEL |

**Note**: Common traps cards are always marked as `ADVANCED` difficulty.

## Usage

### Option 1: Import from Existing Module

```bash
# Import from bar_tutor_unified.py
python3 import_knowledge_to_adaptive.py --module bar_tutor_unified --db my_bar_prep.db

# Import from custom module
python3 import_knowledge_to_adaptive.py --module your_custom_module --db output.db
```

### Option 2: Run with Example Data

```bash
# Test with built-in examples
python3 import_knowledge_to_adaptive.py --example --db test.db
```

### Option 3: Use as Python Module

```python
from import_knowledge_to_adaptive import CardGenerator
from adaptive_learning_system import AdaptiveLearningSystem

# Initialize system
system = AdaptiveLearningSystem("my_cards.db")
generator = CardGenerator(system)

# Convert your concepts
for concept in your_concepts:
    cards_created = generator.generate_cards_from_node(concept)
    print(f"{concept.name}: {cards_created} cards")

# View stats
stats = system.get_statistics()
system.close()
```

## Real-World Import Results

### From bar_tutor_unified (331 concepts)

```
📊 Total Cards Created: 388 cards from 331 concepts
📊 Average: 1.17 cards per concept

By Subject:
  contracts                       62 cards
  torts                          51 cards
  constitutional_law             44 cards
  criminal_law                   46 cards
  criminal_procedure             36 cards
  civil_procedure                37 cards
  evidence                       47 cards
  real_property                  65 cards
```

### Card Type Distribution

Typical distribution for a well-structured concept:
- 1 Rule Statement card
- 1 Elements card (if elements defined)
- 1 Common Traps card (if traps defined)
- 0-1 Exceptions card (if exceptions defined)
- 0-1 Policy card (if policy rationales defined)

## Topic Mapping Examples

### Constitutional Law

```python
# Input KnowledgeNode
concept = KnowledgeNode(
    name="Equal Protection",
    subject="constitutional_law",
    rule_statement="Classification triggers scrutiny: suspect (strict)..."
)

# Detected topic: equal_protection
# Matches keyword: "equal protection"
# Maps to: ConstitutionalLawTopic.EQUAL_PROTECTION
```

### Evidence

```python
# Input KnowledgeNode
concept = KnowledgeNode(
    name="Present Sense Impression",
    subject="evidence",
    rule_statement="Statement describing event made while perceiving..."
)

# Detected topic: present_sense_impression
# Matches keyword: "present sense impression"
# Maps to: EvidenceTopic.PRESENT_SENSE_IMPRESSION
```

## Handling Unknown Subjects

The script automatically skips subjects not in the `Subject` enum:

```
⚠️  Skipping Bankruptcy Trustee Powers - unknown subject: secured_transactions
⚠️  Skipping Iowa Pleading Requirements - unknown subject: iowa_procedure
```

To add support for additional subjects:

1. Add subject to `Subject` enum in `adaptive_learning_system.py`
2. Add to `SUBJECT_MAP` in import script
3. (Optional) Create topic enum and keyword mapping

## Verification After Import

```python
from adaptive_learning_system import AdaptiveLearningSystem, Subject

system = AdaptiveLearningSystem("your_db.db")

# Overall stats
stats = system.get_statistics()
print(f"Total Cards: {stats['total_cards']}")
print(f"Due Today: {stats['due_cards']}")

# Subject-specific
conlaw_perf = system.get_subject_performance(Subject.CONSTITUTIONAL_LAW, days=30)
print(f"Constitutional Law: {conlaw_perf['total_reviews']} reviews")

# View sample cards
cards = system.db.get_all_cards(Subject.EVIDENCE)
for card in cards[:5]:
    print(f"{card.concept_name}: {card.question}")

system.close()
```

## Customizing the Import

### Add Custom Subject

```python
# In adaptive_learning_system.py
class Subject(Enum):
    # ... existing subjects ...
    SECURED_TRANSACTIONS = "secured_transactions"
    FAMILY_LAW = "family_law"

# In import_knowledge_to_adaptive.py
SUBJECT_MAP = {
    # ... existing mappings ...
    "secured_transactions": Subject.SECURED_TRANSACTIONS,
    "family_law": Subject.FAMILY_LAW,
}
```

### Add Custom Topic Keywords

```python
EVIDENCE_KEYWORDS = {
    # ... existing keywords ...
    EvidenceTopic.YOUR_NEW_TOPIC: ["keyword1", "keyword2"],
}
```

### Modify Card Generation Logic

```python
class CardGenerator:
    def generate_cards_from_node(self, node: KnowledgeNode) -> int:
        # Add custom card types here

        # 6. Your custom card type
        if node.custom_field:
            self._create_card(
                subject=subject,
                topic=topic,
                concept_name=f"{node.name} - Custom",
                question=f"Your custom question about {node.name}?",
                answer=node.custom_field,
                difficulty=difficulty,
                tags=["custom"]
            )
```

## Troubleshooting

### "No module named 'dotenv'"

```bash
pip3 install python-dotenv
```

### "Could not find LegalKnowledgeGraph"

The source module must have a class called `LegalKnowledgeGraph` with a `nodes` dictionary attribute.

### "Skipping... - unknown subject"

The subject is not in the `SUBJECT_MAP`. Either:
1. Add it to the mapping, or
2. This is expected for non-MBE subjects

### Cards not appearing

Check that:
1. `rule_statement`, `elements`, or `common_traps` have content
2. Subject mapping is correct
3. Database connection is working

### Duplicate cards

The script may create duplicates if run multiple times. To start fresh:

```bash
rm your_database.db
python3 import_knowledge_to_adaptive.py --module bar_tutor_unified --db your_database.db
```

## Integration with Existing Workflow

### Recommended Workflow

1. **Initial Import**: Convert all existing concepts
   ```bash
   python3 import_knowledge_to_adaptive.py --module bar_tutor_unified --db bar_prep.db
   ```

2. **Verify Import**: Check statistics and sample cards
   ```python
   system = AdaptiveLearningSystem("bar_prep.db")
   print(system.get_statistics())
   ```

3. **Start Studying**: Begin daily review sessions
   ```python
   session = system.start_session()
   cards = system.get_study_block(block_size=20)
   # Review cards...
   system.end_session()
   ```

4. **Track Progress**: Monitor performance
   ```python
   weak_topics = system.identify_weak_topics(Subject.EVIDENCE, threshold=0.7)
   ```

5. **Add New Concepts**: Import incrementally as you create new concepts
   ```python
   generator = CardGenerator(system)
   cards = generator.generate_cards_from_node(new_concept)
   ```

## Performance Expectations

- **Import Speed**: ~100 concepts per second
- **Storage**: ~2KB per card (SQLite)
- **Memory**: Minimal (streaming import)

**Example**: 331 concepts → 388 cards in < 5 seconds

## Next Steps After Import

1. **Backup Database**
   ```bash
   cp bar_prep.db bar_prep_backup.db
   ```

2. **Start First Session**
   ```python
   from adaptive_learning_system import AdaptiveLearningSystem

   system = AdaptiveLearningSystem("bar_prep.db")
   session = system.start_session()

   # Get 10 new cards to start
   cards = system.get_study_block(block_size=10, include_new=True)
   ```

3. **Review Statistics Daily**
   ```python
   stats = system.get_statistics()
   print(f"Mastery: {stats['mastery_percentage']:.1f}%")
   ```

4. **Track Weak Areas**
   ```python
   for subject in [Subject.CONSTITUTIONAL_LAW, Subject.EVIDENCE]:
       weak = system.identify_weak_topics(subject, threshold=0.7)
       print(f"{subject.value}: {len(weak)} weak topics")
   ```

## Advanced: Batch Import from Multiple Sources

```python
from import_knowledge_to_adaptive import CardGenerator
from adaptive_learning_system import AdaptiveLearningSystem

system = AdaptiveLearningSystem("comprehensive_bar_prep.db")
generator = CardGenerator(system)

# Import from multiple knowledge bases
sources = [
    ("bar_tutor_unified", "LegalKnowledgeGraph"),
    ("mbe_concepts", "MBEKnowledgeBase"),
    ("essay_concepts", "EssayConceptGraph"),
]

for module_name, class_name in sources:
    module = importlib.import_module(module_name)
    kb_class = getattr(module, class_name)
    kb = kb_class()

    for concept_id, node in kb.nodes.items():
        cards = generator.generate_cards_from_node(node)

print(f"Total: {generator.cards_created} cards")
system.close()
```

## License

Part of the Iowa Bar Prep Study Aid system.

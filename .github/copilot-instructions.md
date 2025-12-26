# Copilot Instructions for Bar Exam MBE Tutor Repository

## Repository Overview

This is a comprehensive Bar Exam MBE (Multistate Bar Examination) tutoring system that implements evidence-based learning strategies from cognitive science. The system includes:

- **Python-based tutoring engine** with advanced pedagogical features
- **Interactive learning modes** (spaced repetition, interleaved practice, retrieval practice, etc.)
- **Knowledge graph** of legal concepts and relationships
- **Performance analytics** and adaptive study planning
- **React-based web interface** (enhanced-app.jsx)

## Core Components

### Main Files
- `bar_tutor_unified.py` - Primary tutor system with all integrated features
- `advanced_pedagogy.py` - Evidence-based learning strategies implementation
- `interactive_tutor_agent.py` - Conversational AI tutor interface
- `test_tutor.py` - Basic test suite for core functionality

### Data & Content
- `data/` - User performance data, flashcards, analytics (JSONL format)
- `comprehensive_knowledge_base.json` - MBE subject matter content
- `flashcards_v3.jsonl` - Spaced repetition flashcard data

### Documentation
- `START_HERE.md` - Primary user guide
- `QUICK_START.md` - Quick reference for users
- `ADVANCED_PEDAGOGY_README.md` - Feature documentation
- `IMPLEMENTATION-GUIDE.md` - Technical implementation details

## Coding Standards

### Python Style
- **Use Python 3.7+** features (dataclasses, type hints, f-strings)
- **Type hints required** for all function signatures
- **Docstrings** for classes and public methods using multi-line format
- **Dataclasses** for structured data (see examples in bar_tutor_unified.py)
- **Enums** for categorical types (e.g., LearningMode, CognitiveStrategy)
- **Logging** via the logging module (not print statements)
- **Error handling** with specific exception types

Example:
```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

@dataclass
class StudySession:
    """Represents a single study session with metrics."""
    subject: str
    mode: str
    duration_minutes: int
    questions_answered: int
    accuracy: float
```

### File Organization
- **Keep related functionality together** - Large unified files are preferred over many small files
- **Use clear section headers** with `# ====` style markers
- **Group imports** - stdlib, third-party, local (with blank lines between)
- **Configuration constants** at top of file after imports

### Error Handling
- **Use try/except blocks** for external dependencies (OpenAI API, file I/O)
- **Log errors** to error_log.jsonl for user-facing issues
- **Provide fallback behavior** when AI services are unavailable
- **Validate user inputs** for interactive commands

### Data Persistence
- **JSONL format** for append-only logs (performance, analytics, errors)
- **JSON format** for structured data (knowledge base, configurations)
- **Dataclass serialization** using `asdict()` for saving to JSON
- **Create data directory** if it doesn't exist (`DATA_DIR.mkdir(exist_ok=True)`)

## Testing Approach

- **Simple assertion-based tests** in test_tutor.py
- **No external test frameworks** currently (pytest not used)
- **Manual testing** via interactive sessions is primary validation method
- **Test core components**: Knowledge graph, interleaved practice engine, tutor initialization
- When adding tests, follow the pattern in test_tutor.py with clear success messages

## Development Workflow

### Making Changes
1. **Preserve existing functionality** - This is a working system used by students
2. **Test interactively** using `./start_interactive_tutor.sh` after changes
3. **Verify core features** using test_tutor.py
4. **Update documentation** if adding new features or changing workflows

### Adding New Features
- **Follow existing patterns** for learning modes and cognitive strategies
- **Use dataclasses** for new data structures
- **Add to knowledge graph** if introducing new legal concepts
- **Update START_HERE.md** with user-facing features
- **Log to appropriate JSONL file** for persistent data

### Environment Setup
- **API keys** stored in `.env` or `brett.env` (OPENAI_API_KEY or XAI_API_KEY)
- **Load env files** using `python-dotenv`
- **Check for API key** before making LLM calls

## Legal/Subject Matter Guidelines

### MBE Subject Areas
The system covers seven MBE subjects:
- Contracts (formation, performance, remedies, UCC)
- Torts (negligence, intentional torts, strict liability)
- Constitutional Law (due process, equal protection)
- Criminal Law & Procedure (mens rea, homicide, 4th/5th/6th amendments)
- Evidence (hearsay, relevance, character)
- Civil Procedure (jurisdiction, pleadings, discovery)
- Real Property (estates, servitudes, land transactions)

### Content Quality
- **Use accurate legal principles** - This is educational software
- **Follow MBE format** for questions (fact pattern + multiple choice)
- **Include explanations** for correct and incorrect answers
- **Cite rules** when applicable (but avoid overly specific case names)

## Common Patterns

### Spaced Repetition (SM-2 Algorithm)
```python
def calculate_next_review(quality: int, repetitions: int, 
                         easiness_factor: float, interval: int) -> Tuple[int, int, float]:
    """
    SM-2 spaced repetition algorithm implementation.
    
    Args:
        quality: User rating 0-5 (0=complete blackout, 5=perfect recall)
        repetitions: Number of consecutive correct reviews
        easiness_factor: Current easiness factor (typically 1.3-2.5)
        interval: Current interval in days
    
    Returns:
        Tuple of (next_interval_days, new_repetitions, new_easiness_factor)
    """
    # Used throughout for flashcard scheduling
```

### Knowledge Graph Queries
```python
kg = LegalKnowledgeGraph()
concepts = kg.get_subject_concepts("contracts")
related = kg.get_related_concepts("consideration")
```

### Interleaved Practice
```python
engine = InterleavedPracticeEngine(knowledge_graph)
mixed_concepts = engine.generate_practice("contracts", num_questions=10)
```

### Session Management
```python
tutor.start_advanced_session(mode="adaptive", subject="contracts")
# ... practice activities ...
tutor.end_advanced_session()  # Generates insights
```

## Anti-Patterns to Avoid

- **Don't break backward compatibility** - Users have saved progress data
- **Don't remove or rename** existing tutor methods without updating all callers
- **Don't use print()** for logging - use the logging module
- **Don't hardcode paths** - use pathlib.Path and ROOT constant
- **Don't commit API keys** - they go in .env (already in .gitignore)
- **Avoid small utility files** - add utilities to existing modules

## Performance Considerations

- **Lazy load LLM clients** - Only initialize when needed
- **Cache knowledge graph** - Don't rebuild on every query
- **Batch operations** when possible (e.g., loading flashcards)
- **Use generators** for large result sets

## Documentation Standards

### User-Facing Docs
- **Use emoji** for visual appeal (🎓, 📚, 🎯, etc.)
- **Step-by-step instructions** with code examples
- **Troubleshooting sections** for common issues
- **Visual hierarchy** with headers and formatting

### Code Comments
- **Explain "why"** not "what" - code shows what
- **Document assumptions** and edge cases
- **Keep comments up-to-date** with code changes
- **Use section dividers** for major blocks (# ==== SECTION ====)

## Git Workflow

- **Descriptive commit messages** explaining the change
- **Test before committing** - run test_tutor.py at minimum
- **Check .gitignore** - Don't commit __pycache__, .env, data files (except examples)
- **Update relevant docs** in the same commit as code changes

## AI/LLM Integration

- **Support multiple providers** (OpenAI, XAI/Grok)
- **Handle API failures gracefully** with fallback responses
- **Include system prompts** for consistent AI behavior
- **Log AI interactions** for debugging when appropriate
- **Token-efficient prompts** - Be concise but complete

## When in Doubt

1. Check existing implementations in bar_tutor_unified.py
2. Follow patterns from advanced_pedagogy.py for learning features
3. Test with the interactive tutor before finalizing
4. Reference START_HERE.md for user-facing behavior
5. Maintain the balance between powerful features and usability

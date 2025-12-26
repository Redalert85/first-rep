# GitHub Copilot Instructions for MBE Bar Exam Tutor

## Repository Overview

This repository contains an advanced AI-powered MBE (Multistate Bar Examination) study system that implements evidence-based learning strategies from cognitive science. The system combines AI tutoring with proven pedagogical techniques including spaced repetition, interleaved practice, Socratic dialogue, and adaptive learning.

## Tech Stack

- **Language**: Python 3.10+
- **AI/ML**: OpenAI API, xAI (Grok)
- **Key Libraries**:
  - `dotenv` - Environment variable management
  - Standard library: `json`, `logging`, `pathlib`, `dataclasses`, `datetime`, `typing`
- **Testing**: pytest
- **Linting**: flake8
- **CI/CD**: GitHub Actions (Python application workflow)

## Project Structure

### Core Files
- `bar_tutor_unified.py` - Main unified tutor system (v4.0) with all components integrated
- `bar_tutor_unified_v4.py` - Version 4 of the tutor
- `interactive_tutor_agent.py` - Interactive conversational agent
- `advanced_pedagogy.py` - Advanced pedagogical features implementation

### Knowledge Base & Content
- `comprehensive_knowledge_base.json` - Complete MBE knowledge base
- `ultimate_knowledge_base.json` - Extended knowledge base
- `essay_subjects.json` - Essay question subjects and topics
- `flashcards_v3.jsonl` - Flashcard content in JSONL format
- `tags_index.json` - Content tagging and indexing

### Utilities
- `advanced_parser.py` / `universal_advanced_parser.py` - Content parsing utilities
- `content_integrator.py` - Content integration system
- `pattern_recognition.py` - Pattern recognition for legal concepts
- `elite_memory_palace.py` / `optimized_memory_palace.py` - Memory palace techniques
- `practice_exam_system.py` - Practice exam generation and management
- `readiness_dashboard.py` - Student readiness tracking

### Data Directories
- `data/` - Data files and storage
- `out/` - Generated output (practice questions, study guides)
- `generated_questions/` - Auto-generated MBE questions
- `study_guides/` - Subject-specific study guides
- `materials/` - Study materials and resources

### Testing
- `test_tutor.py` - Core functionality tests
- Run tests with: `pytest`

## MBE Subjects Covered

1. **Contracts** - Formation, performance, remedies, UCC
2. **Torts** - Negligence, intentional torts, strict liability
3. **Constitutional Law (conlaw)** - Due process, equal protection
4. **Criminal Law (crim)** - Mens rea, homicide, defenses
5. **Evidence** - Hearsay, relevance, character evidence
6. **Civil Procedure (civpro)** - Jurisdiction, pleadings, discovery
7. **Real Property (property)** - Estates, servitudes, land use

## Key Features & Learning Modes

### Pedagogical Techniques
- **Adaptive Learning** - AI-driven personalized study paths
- **Spaced Repetition** - SM-2 algorithm for optimal review intervals
- **Interleaved Practice** - Mixing concepts for better retention (2x improvement)
- **Socratic Dialogue** - Guided discovery learning for wrong answers
- **Concept Mapping** - Visual knowledge graphs and relationships
- **Retrieval Practice** - Testing before revealing answers
- **Dual Coding** - Visual + verbal learning
- **Metacognition** - Self-reflection and confidence calibration

### Core Classes & Components
- `BarExamTutor` - Main tutor class
- `LegalKnowledgeGraph` - Knowledge representation system
- `InterleavedPracticeEngine` - Interleaved practice generation
- `SpacedRepetitionEngine` - SM-2 spaced repetition implementation
- `AdaptiveLearningEngine` - Bayesian Knowledge Tracing
- `SocraticLearningEngine` - Socratic dialogue system

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use type hints for function signatures (`typing` module)
- Use dataclasses for structured data
- Maximum line length: 127 characters (as per flake8 config)
- Use descriptive variable names that reflect legal terminology

### API Keys & Environment
- API keys stored in `brett.env` file (not committed to repo)
- Required environment variables:
  - `OPENAI_API_KEY` or `XAI_API_KEY` for AI features
- Load with `python-dotenv`

### Logging
- Use Python's `logging` module
- Log files: `bar_tutor.log`, `bar_tutor_unified.log`
- Include timestamps and log levels

### File Formats
- JSON for structured data (knowledge bases, questions)
- JSONL for line-delimited JSON (flashcards)
- Markdown for documentation and study guides
- Python for all application code

### Testing
- Write tests in `test_*.py` format
- Use simple assertions and clear test names
- Run full test suite before committing: `pytest`
- Lint before committing: `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`

### Building & Running
- No build step required (Python interpreted)
- Main entry points:
  - Interactive tutor: Run tutor scripts directly
  - Tests: `pytest`
  - Lint: `flake8`

### CI/CD
- GitHub Actions workflow: `.github/workflows/python-app.yml`
- Runs on: Python 3.10, Ubuntu latest
- Steps: Install dependencies → Lint with flake8 → Test with pytest
- Triggers: Push/PR to `main` branch

## Common Patterns

### Question Generation
- Questions stored in JSON format with structure:
  - `question` - The question text
  - `options` - List of answer choices
  - `correct_answer` - The correct option
  - `explanation` - Detailed explanation
  - `subject` - MBE subject area
  - `concept` - Specific legal concept

### Knowledge Base Structure
- Hierarchical: Subject → Topics → Concepts
- Each concept includes:
  - ID, name, description
  - Prerequisites and related concepts
  - Difficulty level
  - Practice questions

### Session Management
- Start sessions with `start_advanced_session(mode, subject)`
- End sessions with `end_advanced_session()` for analytics
- Modes: `"adaptive"`, `"focused"`, `"interleaved"`, `"spaced"`, `"retrieval"`, `"diagnostic"`

## Documentation
- `START_HERE.md` - Primary getting started guide
- `QUICK_START.md` - Quick start instructions
- `ADVANCED_PEDAGOGY_README.md` - Complete feature documentation
- `USAGE_GUIDE.md` - Detailed usage instructions
- `IMPLEMENTATION-GUIDE.md` - Implementation details
- Subject-specific READMEs (e.g., `BAR_TUTOR_README.md`, `SOCRATIC_TUTOR_README.md`)

## Important Notes

### Legal Domain
- This is a legal education tool - accuracy is critical
- Legal concepts must be precise and up-to-date
- Use proper legal terminology and citation formats
- MBE questions follow specific formats and patterns

### AI Integration
- OpenAI or xAI APIs used for question generation and tutoring
- Handle API errors gracefully
- Implement rate limiting and error recovery
- Consider token usage and API costs

### User Experience
- Focus on evidence-based learning outcomes
- Provide immediate feedback on practice questions
- Track user progress and adapt difficulty
- Encourage metacognition and self-assessment

## When Making Changes

1. **Understand the legal context** - Research MBE topics if unfamiliar
2. **Maintain pedagogical integrity** - Don't break learning features
3. **Test thoroughly** - Run `pytest` and manual tests
4. **Update documentation** - Keep README files current
5. **Check knowledge bases** - Ensure JSON is valid and complete
6. **Preserve user data** - Don't break saved progress or history
7. **Follow existing patterns** - Match code style and structure
8. **Consider API costs** - Optimize AI calls where possible

## Getting Help

- Review existing documentation in README files
- Check `test_tutor.py` for usage examples
- Examine `bar_tutor_unified.py` for the main API
- Look at generated output in `out/` directory for examples

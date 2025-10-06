#!/usr/bin/env python3
"""
Content Integration System
Parses and integrates user's study materials into the tutor system
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import markdown
import PyPDF2

@dataclass
class StudyContent:
    """Represents parsed study content"""
    subject: str
    title: str
    content_type: str  # 'outline', 'guide', 'notes', 'flashcards'
    raw_content: str
    parsed_sections: Dict[str, Any] = field(default_factory=dict)
    key_concepts: List[Dict] = field(default_factory=list)
    mnemonics: List[Dict] = field(default_factory=list)
    traps: List[Dict] = field(default_factory=list)
    examples: List[Dict] = field(default_factory=list)
    micro_hypos: List[Dict] = field(default_factory=list)

class ContentIntegrator:
    """
    Integrates user's study materials into the tutor system
    Parses markdown guides, outlines, and other study materials
    """

    def __init__(self, repo_path: str = "/Users/bcwelling/Documents/GitHub/first-rep"):
        self.repo_path = Path(repo_path)
        self.content_database = {}
        self.parsed_content = {}
        self.initialize_content_parsers()

    def initialize_content_parsers(self):
        """Initialize parsers for different content types"""
        self.parsers = {
            'markdown': self.parse_markdown_content,
            'pdf': self.parse_pdf_content,
        }

    def scan_repository(self) -> Dict[str, List[Path]]:
        """
        Scan repository for study materials
        Returns categorized file lists
        """
        study_files = {
            'markdown_guides': [],
            'pdf_outlines': [],
            'word_outlines': [],
            'study_guides': [],
            'flashcards': [],
            'notes': []
        }

        # Find markdown study guides
        for md_file in self.repo_path.glob('**/*.md'):
            if any(keyword in md_file.name.lower() for keyword in ['guide', 'outline', 'master', 'study']):
                if 'contracts' in md_file.name.lower():
                    study_files['study_guides'].append(('contracts', md_file))
                elif 'real_property' in md_file.name.lower() or 'property' in md_file.name.lower():
                    study_files['study_guides'].append(('real_property', md_file))
                elif 'torts' in md_file.name.lower():
                    study_files['study_guides'].append(('torts', md_file))
                elif 'conlaw' in md_file.name.lower() or 'constitutional' in md_file.name.lower():
                    study_files['study_guides'].append(('constitutional_law', md_file))
                elif 'crim' in md_file.name.lower():
                    if 'procedure' in md_file.name.lower():
                        study_files['study_guides'].append(('criminal_procedure', md_file))
                    else:
                        study_files['study_guides'].append(('criminal_law', md_file))
                elif 'evidence' in md_file.name.lower():
                    study_files['study_guides'].append(('evidence', md_file))
                elif 'civil' in md_file.name.lower() and 'procedure' in md_file.name.lower():
                    study_files['study_guides'].append(('civil_procedure', md_file))
                else:
                    study_files['markdown_guides'].append(md_file)

        # Find PDF outlines
        for pdf_file in self.repo_path.glob('**/*.pdf'):
            if any(keyword in pdf_file.name.lower() for keyword in ['outline', '1l', '2l']):
                if 'contracts' in pdf_file.name.lower() or 'sales' in pdf_file.name.lower():
                    study_files['pdf_outlines'].append(('contracts', pdf_file))
                elif 'torts' in pdf_file.name.lower():
                    study_files['pdf_outlines'].append(('torts', pdf_file))
                elif 'constitutional' in pdf_file.name.lower() or 'conlaw' in pdf_file.name.lower():
                    study_files['pdf_outlines'].append(('constitutional_law', pdf_file))
                elif 'criminal' in pdf_file.name.lower():
                    if 'procedure' in pdf_file.name.lower():
                        study_files['pdf_outlines'].append(('criminal_procedure', pdf_file))
                    else:
                        study_files['pdf_outlines'].append(('criminal_law', pdf_file))
                elif 'evidence' in pdf_file.name.lower():
                    study_files['pdf_outlines'].append(('evidence', pdf_file))
                elif 'civil' in pdf_file.name.lower() and 'procedure' in pdf_file.name.lower():
                    study_files['pdf_outlines'].append(('civil_procedure', pdf_file))
                elif 'property' in pdf_file.name.lower():
                    study_files['pdf_outlines'].append(('real_property', pdf_file))

        # Find Word outlines
        for docx_file in self.repo_path.glob('**/*.docx'):
            if 'outline' in docx_file.name.lower():
                if 'property' in docx_file.name.lower():
                    study_files['word_outlines'].append(('real_property', docx_file))

        return study_files

    def parse_markdown_content(self, file_path: Path) -> StudyContent:
        """Parse markdown study guide"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract subject from filename
        subject = self._identify_subject_from_filename(file_path.name)

        study_content = StudyContent(
            subject=subject,
            title=file_path.stem.replace('_', ' ').title(),
            content_type='guide',
            raw_content=content
        )

        # Parse sections
        study_content.parsed_sections = self._parse_markdown_sections(content)

        # Extract key elements
        study_content.key_concepts = self._extract_key_concepts(content)
        study_content.mnemonics = self._extract_mnemonics(content)
        study_content.traps = self._extract_traps(content)
        study_content.examples = self._extract_examples(content)
        study_content.micro_hypos = self._extract_micro_hypos(content)

        return study_content

    def _parse_markdown_sections(self, content: str) -> Dict[str, Any]:
        """Parse markdown into structured sections"""
        sections = {}

        # Split by headers
        lines = content.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            if line.startswith('#'):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()

                # Start new section
                current_section = line.lstrip('#').strip()
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def _extract_key_concepts(self, content: str) -> List[Dict]:
        """Extract key concepts from content"""
        concepts = []

        # Look for bolded terms or key definitions
        bold_pattern = r'\*\*([^*]+)\*\*'
        rule_pattern = r'Rule:?\s*([^.!?\n]+)'

        for match in re.finditer(bold_pattern, content):
            concept_text = match.group(1).strip()
            if len(concept_text) > 3 and len(concept_text) < 100:
                concepts.append({
                    'term': concept_text,
                    'context': content[max(0, match.start()-200):match.end()+200]
                })

        for match in re.finditer(rule_pattern, content, re.IGNORECASE):
            rule_text = match.group(1).strip()
            if len(rule_text) > 10:
                concepts.append({
                    'type': 'rule',
                    'content': rule_text,
                    'context': content[max(0, match.start()-100):match.end()+100]
                })

        return concepts

    def _extract_mnemonics(self, content: str) -> List[Dict]:
        """Extract mnemonics from content"""
        mnemonics = []

        # Look for mnemonic patterns
        mnemonic_patterns = [
            r'Mnemonic:?\s*`([^`]+)`',
            r'`([^`]+)`',
            r'Mnemonic:?\s*([A-Z\s&]+)',
            r'([A-Z]{3,})'  # Capital letter sequences
        ]

        for pattern in mnemonic_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                mnemonic_text = match.group(1).strip()
                if 3 <= len(mnemonic_text) <= 50 and mnemonic_text.replace(' ', '').isalnum():
                    # Get surrounding context
                    start = max(0, match.start() - 300)
                    end = min(len(content), match.end() + 300)
                    context = content[start:end]

                    mnemonics.append({
                        'mnemonic': mnemonic_text,
                        'context': context,
                        'purpose': self._identify_mnemonic_purpose(context)
                    })

        return mnemonics

    def _extract_traps(self, content: str) -> List[Dict]:
        """Extract common traps and pitfalls"""
        traps = []

        trap_patterns = [
            r'Traps?:?\s*([^.!?\n]+)',
            r'Pitfalls?:?\s*([^.!?\n]+)',
            r'Common errors?:?\s*([^.!?\n]+)',
            r'⚠️\s*([^.!?\n]+)',
            r'Watch out:?\s*([^.!?\n]+)'
        ]

        for pattern in trap_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                trap_text = match.group(1).strip()
                if len(trap_text) > 5:
                    traps.append({
                        'trap': trap_text,
                        'context': content[max(0, match.start()-200):match.end()+200]
                    })

        return traps

    def _extract_examples(self, content: str) -> List[Dict]:
        """Extract examples and hypotheticals"""
        examples = []

        example_patterns = [
            r'Example:?\s*([^.!?\n]+)',
            r'✅\s*([^.!?\n]+)',
            r'❌\s*([^.!?\n]+)',
            r'Micro-Hypo:?\s*([^.!?\n]+)'
        ]

        for pattern in example_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                example_text = match.group(1).strip()
                if len(example_text) > 5:
                    examples.append({
                        'example': example_text,
                        'type': 'valid' if '✅' in content[match.start():match.end()+10] else 'invalid',
                        'context': content[max(0, match.start()-150):match.end()+150]
                    })

        return examples

    def _extract_micro_hypos(self, content: str) -> List[Dict]:
        """Extract micro-hypotheticals"""
        hypos = []

        hypo_pattern = r'Micro-Hypo[^:]*:\s*([^.!?\n]+)'

        for match in re.finditer(hypo_pattern, content, re.IGNORECASE):
            hypo_text = match.group(1).strip()
            if len(hypo_text) > 5:
                hypos.append({
                    'hypo': hypo_text,
                    'context': content[max(0, match.start()-200):match.end()+200]
                })

        return hypos

    def _identify_subject_from_filename(self, filename: str) -> str:
        """Identify subject from filename"""
        filename_lower = filename.lower()

        if 'contracts' in filename_lower:
            return 'contracts'
        elif 'torts' in filename_lower:
            return 'torts'
        elif 'constitutional' in filename_lower or 'conlaw' in filename_lower:
            return 'constitutional_law'
        elif 'criminal' in filename_lower:
            if 'procedure' in filename_lower:
                return 'criminal_procedure'
            else:
                return 'criminal_law'
        elif 'evidence' in filename_lower:
            return 'evidence'
        elif 'civil' in filename_lower and 'procedure' in filename_lower:
            return 'civil_procedure'
        elif 'property' in filename_lower:
            return 'real_property'
        else:
            return 'general'

    def _identify_mnemonic_purpose(self, context: str) -> str:
        """Identify what a mnemonic is for"""
        context_lower = context.lower()

        if 'rule' in context_lower or 'elements' in context_lower:
            return 'rule_elements'
        elif 'scrutiny' in context_lower or 'test' in context_lower:
            return 'tests_levels'
        elif 'order' in context_lower or 'sequence' in context_lower:
            return 'sequence_order'
        elif 'exceptions' in context_lower or 'cases' in context_lower:
            return 'exceptions_cases'
        else:
            return 'general_memory'

    def parse_pdf_content(self, file_path: Path) -> Optional[StudyContent]:
        """Parse PDF content (basic text extraction)"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                # Extract text from first few pages
                for page_num in range(min(10, len(pdf_reader.pages))):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"

                subject = self._identify_subject_from_filename(file_path.name)

                return StudyContent(
                    subject=subject,
                    title=file_path.stem.replace('-', ' ').title(),
                    content_type='pdf_outline',
                    raw_content=text
                )
        except Exception as e:
            print(f"Could not parse PDF {file_path}: {e}")
            return None

    def integrate_content(self) -> Dict[str, StudyContent]:
        """Integrate all study materials into the system"""
        print("🔍 Scanning repository for study materials...")

        study_files = self.scan_repository()

        print(f"📚 Found {len(study_files['study_guides'])} study guides")
        print(f"📄 Found {len(study_files['pdf_outlines'])} PDF outlines")
        print(f"📝 Found {len(study_files['markdown_guides'])} markdown guides")

        # Parse all content
        for subject, file_path in study_files['study_guides']:
            if file_path.suffix == '.md':
                try:
                    content = self.parse_markdown_content(file_path)
                    self.content_database[f"{subject}_guide"] = content
                    print(f"✅ Parsed {subject} study guide")
                except Exception as e:
                    print(f"❌ Failed to parse {file_path}: {e}")

        # Parse PDF outlines
        for subject, file_path in study_files['pdf_outlines']:
            try:
                content = self.parse_pdf_content(file_path)
                if content:
                    self.content_database[f"{subject}_pdf"] = content
                    print(f"✅ Parsed {subject} PDF outline")
            except Exception as e:
                print(f"❌ Failed to parse PDF {file_path}: {e}")

        print(f"🎯 Successfully integrated {len(self.content_database)} study materials")
        return self.content_database

    def get_content_for_subject(self, subject: str) -> Dict[str, Any]:
        """Get all integrated content for a subject"""
        content_keys = [k for k in self.content_database.keys() if subject in k]
        content = {}

        for key in content_keys:
            study_content = self.content_database[key]
            content[key] = {
                'title': study_content.title,
                'key_concepts': study_content.key_concepts[:10],  # Top 10 concepts
                'mnemonics': study_content.mnemonics[:5],  # Top 5 mnemonics
                'traps': study_content.traps[:5],  # Top 5 traps
                'examples': study_content.examples[:5],  # Top 5 examples
                'sections': study_content.parsed_sections
            }

        return content

    def search_content(self, query: str, subject: str = None) -> List[Dict]:
        """Search across all integrated content"""
        results = []

        for key, content in self.content_database.items():
            if subject and subject not in key:
                continue

            # Search in key concepts
            for concept in content.key_concepts:
                if query.lower() in concept.get('term', '').lower() or query.lower() in concept.get('context', '').lower():
                    results.append({
                        'type': 'concept',
                        'source': key,
                        'content': concept,
                        'relevance': 'high'
                    })

            # Search in mnemonics
            for mnemonic in content.mnemonics:
                if query.lower() in mnemonic.get('mnemonic', '').lower():
                    results.append({
                        'type': 'mnemonic',
                        'source': key,
                        'content': mnemonic,
                        'relevance': 'high'
                    })

            # Search in traps
            for trap in content.traps:
                if query.lower() in trap.get('trap', '').lower():
                    results.append({
                        'type': 'trap',
                        'source': key,
                        'content': trap,
                        'relevance': 'medium'
                    })

        return results[:10]  # Return top 10 results

    def generate_study_summary(self, subject: str) -> str:
        """Generate a comprehensive study summary for a subject"""
        content = self.get_content_for_subject(subject)

        if not content:
            return f"I don't have detailed study materials for {subject} yet."

        summary = f"# 📚 {subject.replace('_', ' ').title()} Study Summary\n\n"

        # Add key concepts
        all_concepts = []
        for source_content in content.values():
            all_concepts.extend(source_content.get('key_concepts', []))

        if all_concepts:
            summary += "## 🎯 Key Concepts\n"
            for concept in all_concepts[:15]:  # Top 15 concepts
                summary += f"• **{concept.get('term', 'Concept')}**\n"

        # Add mnemonics
        all_mnemonics = []
        for source_content in content.values():
            all_mnemonics.extend(source_content.get('mnemonics', []))

        if all_mnemonics:
            summary += "\n## 🧠 Mnemonics\n"
            for mnemonic in all_mnemonics[:8]:  # Top 8 mnemonics
                summary += f"• `{mnemonic.get('mnemonic', '')}` - {mnemonic.get('purpose', '')}\n"

        # Add traps
        all_traps = []
        for source_content in content.values():
            all_traps.extend(source_content.get('traps', []))

        if all_traps:
            summary += "\n## ⚠️ Common Traps\n"
            for trap in all_traps[:6]:  # Top 6 traps
                summary += f"• {trap.get('trap', '')}\n"

        summary += "\n## 📖 Study Tips\n"
        summary += f"• Focus on the key concepts listed above\n"
        summary += f"• Use the mnemonics to remember complex rules\n"
        summary += f"• Watch out for the common traps\n"
        summary += f"• Practice with micro-hypotheticals\n"
        summary += f"• Review regularly using spaced repetition\n"

        return summary

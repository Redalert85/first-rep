#!/usr/bin/env python3
"""
Universal Advanced Parser - Makes ALL subjects as rich as Real Property
Parses: mbe_master_guide.md, cross_subject_headline_rulebook.md, and any subject-specific files
"""

import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Set

@dataclass
class MicroHypo:
    number: int
    context: str
    scenario: str
    answer: str
    memory_hook: Optional[str] = None

@dataclass
class ComprehensiveConcept:
    """Comprehensive legal concept with all possible features"""
    concept_id: str
    name: str
    subject: str
    
    # Core content
    rule_statement: str = ""
    rule_word_count: int = 0
    
    # Hierarchical structure
    subtopics: List[str] = field(default_factory=list)
    parent_concept: Optional[str] = None
    
    # Multi-modal learning
    story_method: Optional[str] = None
    mnemonic: Optional[str] = None
    mnemonic_type: Optional[str] = None
    kinesthetic_gesture: Optional[str] = None
    ascii_visual: Optional[str] = None
    
    # Legal analysis
    elements: List[str] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    policy_rationales: List[str] = field(default_factory=list)
    
    # Practice materials
    micro_hypos: List[MicroHypo] = field(default_factory=list)
    pitfalls: List[str] = field(default_factory=list)
    
    # Cross-references
    related_concepts: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    
    # Metadata
    emoji: Optional[str] = None
    difficulty: int = 3
    exam_frequency: Optional[str] = None
    source_file: str = ""

class UniversalAdvancedParser:
    """Parse all subjects to Real Property level + 50%"""
    
    SUBJECT_MAP = {
        'Constitutional Law': 'constitutional_law',
        'Torts': 'torts',
        'Contracts': 'contracts',
        'Criminal Law': 'criminal_law',
        'Criminal Procedure': 'criminal_procedure',
        'Civil Procedure': 'civil_procedure',
        'Evidence': 'evidence',
        'Real Property': 'real_property'
    }
    
    def __init__(self):
        self.concepts: Dict[str, List[ComprehensiveConcept]] = {}
        self.all_concepts: List[ComprehensiveConcept] = []
    
    def parse_mbe_master_guide(self, filepath: Path) -> Dict[str, List[ComprehensiveConcept]]:
        """Parse the comprehensive MBE master guide"""
        print(f"\n📖 Parsing {filepath.name}...")
        
        content = filepath.read_text()
        concepts_by_subject = {}
        
        # Split by major subject sections (## headers)
        sections = re.split(r'\n## (.+?)\n', content)
        
        for i in range(1, len(sections), 2):
            section_title = sections[i].strip()
            section_content = sections[i+1] if i+1 < len(sections) else ""
            
            # Identify subject
            subject = None
            for subj_name, subj_id in self.SUBJECT_MAP.items():
                if subj_name in section_title:
                    subject = subj_id
                    break
            
            if not subject:
                continue
            
            print(f"  📌 Processing {section_title}...")
            
            # Find all subsections (#### headers)
            subsections = re.split(r'\n#### (\d+\. .+?)\n', section_content)
            
            subject_concepts = []
            for j in range(1, len(subsections), 2):
                subsection_title = subsections[j].strip()
                subsection_content = subsections[j+1] if j+1 < len(subsections) else ""
                
                # Skip visuals/flowcharts
                if 'Visual' in subsection_title or 'Flowchart' in subsection_title:
                    continue
                
                concept = self._parse_subsection(
                    subject, 
                    subsection_title, 
                    subsection_content,
                    filepath.name
                )
                
                if concept:
                    subject_concepts.append(concept)
            
            if subject_concepts:
                concepts_by_subject[subject] = subject_concepts
                print(f"    ✓ Extracted {len(subject_concepts)} concepts")
        
        return concepts_by_subject
    
    def parse_cross_subject_rulebook(self, filepath: Path) -> Dict[str, List[ComprehensiveConcept]]:
        """Parse cross-subject headline rulebook for additional concepts"""
        print(f"\n📖 Parsing {filepath.name}...")
        
        content = filepath.read_text()
        concepts_by_subject = {}
        
        # Split by numbered sections (## NUMBER. SUBJECT)
        sections = re.split(r'\n## (\d+)\. (.+?)\n', content)
        
        for i in range(1, len(sections), 3):
            if i+2 >= len(sections):
                break
            
            section_num = sections[i]
            section_title = sections[i+1].strip()
            section_content = sections[i+2]
            
            # Identify subject from title
            subject = None
            for subj_name, subj_id in self.SUBJECT_MAP.items():
                if subj_name.upper() in section_title.upper():
                    subject = subj_id
                    break
            
            if not subject:
                continue
            
            concept = self._parse_rulebook_section(
                subject,
                section_title,
                section_content,
                filepath.name
            )
            
            if concept:
                if subject not in concepts_by_subject:
                    concepts_by_subject[subject] = []
                concepts_by_subject[subject].append(concept)
        
        for subj, concepts in concepts_by_subject.items():
            print(f"  ✓ {subj}: {len(concepts)} concepts")
        
        return concepts_by_subject
    
    def _parse_subsection(self, subject: str, title: str, content: str, source: str) -> Optional[ComprehensiveConcept]:
        """Parse a subsection into a concept"""
        # Clean title
        clean_title = re.sub(r'^\d+\.\s*', '', title)
        clean_title = re.sub(r'\s*–.+$', '', clean_title)
        clean_title = clean_title.strip()
        
        # Generate ID
        concept_id = f"{subject}_{clean_title.lower().replace(' ', '_').replace('&', 'and')}"
        concept_id = re.sub(r'[^a-z0-9_]', '', concept_id)
        
        concept = ComprehensiveConcept(
            concept_id=concept_id,
            name=clean_title,
            subject=subject,
            source_file=source
        )
        
        # Extract rule statement
        rule_match = re.search(r'\*\*Rule\*\*:\s*(.+?)(?:\n|\.\.\.)', content)
        if rule_match:
            concept.rule_statement = rule_match.group(1).strip()
            words = len(concept.rule_statement.split())
            concept.rule_word_count = words
        
        # Extract mnemonic
        mnemonic_match = re.search(r'\*\*Mnemonic\*\*:\s*`(.+?)`', content)
        if mnemonic_match:
            concept.mnemonic = mnemonic_match.group(1)
            concept.mnemonic_type = "acronym"
        
        # Extract elements (look for bullet lists)
        elements = re.findall(r'^- \*\*([^*:]+)\*\*', content, re.MULTILINE)
        if elements:
            concept.elements = elements[:10]
        
        # Extract traps
        traps_match = re.search(r'\*\*Traps\*\*:\s*(.+?)(?:\n-|\*\*|$)', content, re.DOTALL)
        if traps_match:
            traps_text = traps_match.group(1).strip()
            traps = [t.strip() for t in traps_text.split(',') if t.strip()]
            concept.pitfalls = traps[:5]
        
        # Extract policy rationales
        policy_match = re.search(r'\*\*Policy\*\*:\s*(.+?)(?:\n-|\*\*|$)', content, re.DOTALL)
        if policy_match:
            policies = [p.strip() for p in policy_match.group(1).split(',')]
            concept.policy_rationales = policies[:5]
        
        return concept
    
    def _parse_rulebook_section(self, subject: str, title: str, content: str, source: str) -> Optional[ComprehensiveConcept]:
        """Parse cross-subject rulebook section"""
        # Extract the main topic from title (after the dash)
        topic_match = re.search(r'–\s*(.+)$', title)
        topic_name = topic_match.group(1).strip() if topic_match else title
        
        concept_id = f"{subject}_{topic_name.lower().replace(' ', '_').replace('&', 'and')}"
        concept_id = re.sub(r'[^a-z0-9_]', '', concept_id)
        
        concept = ComprehensiveConcept(
            concept_id=concept_id,
            name=topic_name,
            subject=subject,
            source_file=source
        )
        
        # Extract rule with word count
        rule_match = re.search(r'\*\*Rule \((\d+) words?\):\*\*\s*(.+?)(?:\n\n|\*\*)', content, re.DOTALL)
        if rule_match:
            concept.rule_word_count = int(rule_match.group(1))
            concept.rule_statement = rule_match.group(2).strip()
        
        # Extract major subtopics
        subtopics_match = re.search(r'\*\*Major Subtopics:\*\*\s*\n((?:- \*\*[^:]+:[^\n]+\n?)+)', content, re.DOTALL)
        if subtopics_match:
            subtopics = re.findall(r'- \*\*([^:]+):', subtopics_match.group(1))
            concept.subtopics = subtopics[:8]
        
        return concept
    
    def merge_concepts(self, concepts_dict1: Dict, concepts_dict2: Dict) -> Dict[str, List[ComprehensiveConcept]]:
        """Merge concepts from multiple sources, avoiding duplicates"""
        merged = {}
        
        for subject in set(list(concepts_dict1.keys()) + list(concepts_dict2.keys())):
            concepts1 = concepts_dict1.get(subject, [])
            concepts2 = concepts_dict2.get(subject, [])
            
            # Use concept_id to avoid duplicates
            seen_ids = set()
            merged_list = []
            
            for concept in concepts1 + concepts2:
                if concept.concept_id not in seen_ids:
                    merged_list.append(concept)
                    seen_ids.add(concept.concept_id)
            
            merged[subject] = merged_list
        
        return merged
    
    def export_to_python(self, concepts_by_subject: Dict[str, List[ComprehensiveConcept]]) -> str:
        """Generate Python code for ALL subjects"""
        code = "# Generated Comprehensive Knowledge Base\n"
        code += "# Each subject enhanced to Real Property level + 50%\n\n"
        
        for subject, concepts in sorted(concepts_by_subject.items()):
            code += f"    def _initialize_{subject}(self):\n"
            code += f'        """Initialize {subject} - Comprehensive expansion"""\n'
            code += "        concepts = [\n"
            
            for concept in concepts:
                code += "            KnowledgeNode(\n"
                code += f"                concept_id=\"{concept.concept_id}\",\n"
                code += f"                name=\"{concept.name}\",\n"
                code += f"                subject=\"{concept.subject}\",\n"
                code += f"                difficulty={concept.difficulty},\n"
                
                # Escape rule
                rule_escaped = concept.rule_statement.replace('"', '\\"').replace('\n', ' ')[:200]
                code += f"                rule_statement=\"{rule_escaped}\",\n"
                
                # Elements - use subtopics or elements
                elements = concept.subtopics or concept.elements
                code += f"                elements={elements[:5]},\n"
                
                # Policy rationales
                code += f"                policy_rationales={concept.policy_rationales[:3]},\n"
                
                # Common traps
                if concept.pitfalls:
                    code += "                common_traps=[\n"
                    for trap in concept.pitfalls[:3]:
                        trap_escaped = trap.replace('"', '\\"').replace('\n', ' ')[:100]
                        code += f"                    \"{trap_escaped}\",\n"
                    code += "                ],\n"
                else:
                    code += "                common_traps=[],\n"
                
                if concept.mnemonic:
                    code += f"                # Mnemonic: {concept.mnemonic[:60]}\n"
                
                code += "            ),\n"
            
            code += "        ]\n"
            code += "        for node in concepts:\n"
            code += "            self.nodes[node.concept_id] = node\n\n"
        
        return code
    
    def export_statistics(self, concepts_by_subject: Dict[str, List[ComprehensiveConcept]]):
        """Show comprehensive statistics"""
        print("\n" + "="*70)
        print("COMPREHENSIVE EXPANSION STATISTICS")
        print("="*70 + "\n")
        
        total = 0
        target_per_subject = 14
        
        print(f"{'Subject':<25} {'Current':<10} {'Target':<10} {'Progress':<15}")
        print("-"*70)
        
        for subject in sorted(self.SUBJECT_MAP.values()):
            count = len(concepts_by_subject.get(subject, []))
            total += count
            progress = count / target_per_subject * 100
            bar = "█" * int(progress / 10) + "░" * (10 - int(progress / 10))
            
            print(f"{subject:<25} {count:<10} {target_per_subject:<10} {bar} {progress:.0f}%")
        
        print("-"*70)
        print(f"{'TOTAL':<25} {total:<10} {len(self.SUBJECT_MAP)*target_per_subject:<10}")
        print()

def main():
    print("="*70)
    print("UNIVERSAL ADVANCED PARSER v1.0")
    print("Making ALL subjects as rich as Real Property + 50%")
    print("="*70)
    
    parser = UniversalAdvancedParser()
    
    # Parse MBE master guide
    mbe_guide = Path("mbe_master_guide.md")
    if mbe_guide.exists():
        concepts_mbe = parser.parse_mbe_master_guide(mbe_guide)
    else:
        print(f"⚠️  {mbe_guide} not found")
        concepts_mbe = {}
    
    # Parse cross-subject rulebook
    rulebook = Path("cross_subject_headline_rulebook_preview.md")
    if rulebook.exists():
        concepts_rulebook = parser.parse_cross_subject_rulebook(rulebook)
    else:
        print(f"⚠️  {rulebook} not found")
        concepts_rulebook = {}
    
    # Merge all sources
    print("\n🔄 Merging concepts from all sources...")
    all_concepts = parser.merge_concepts(concepts_mbe, concepts_rulebook)
    
    # Show statistics
    parser.export_statistics(all_concepts)
    
    # Export Python code
    print("💾 Exporting comprehensive Python code...")
    python_code = parser.export_to_python(all_concepts)
    Path("comprehensive_knowledge_base.py").write_text(python_code)
    print("✓ Saved to: comprehensive_knowledge_base.py")
    
    # Export JSON
    print("💾 Exporting comprehensive JSON...")
    all_concepts_list = []
    for subject, concepts in all_concepts.items():
        all_concepts_list.extend([asdict(c) for c in concepts])
    
    with open("comprehensive_knowledge_base.json", 'w') as f:
        json.dump(all_concepts_list, f, indent=2)
    print("✓ Saved to: comprehensive_knowledge_base.json")
    
    print("\n" + "="*70)
    print("✅ UNIVERSAL PARSING COMPLETE!")
    print("="*70)
    print(f"\nTotal concepts extracted: {len(all_concepts_list)}")
    print("\nNext: Review comprehensive_knowledge_base.py")
    print("Then: Integrate into bar_tutor_unified.py")

if __name__ == "__main__":
    main()

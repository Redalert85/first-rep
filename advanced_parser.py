#!/usr/bin/env python3
"""
Advanced Real Property Parser
Extracts hierarchical concepts, mnemonics, flowcharts, tables, and micro-hypos
"""

import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any

@dataclass
class MicroHypo:
    """Practice scenario with answer and memory hook"""
    number: int
    context: str
    scenario: str
    answer: str
    memory_hook: Optional[str] = None

@dataclass
class ContrastRow:
    """Single row from comparison table"""
    element: str
    values: Dict[str, str]  # Column name -> value

@dataclass
class FlowchartNode:
    """Decision tree node"""
    question: str
    yes_path: Optional[str] = None
    no_path: Optional[str] = None
    children: List['FlowchartNode'] = field(default_factory=list)

@dataclass
class AdvancedConcept:
    """Rich legal concept with all learning modalities"""
    concept_id: str
    name: str
    subject: str
    parent_concept: Optional[str] = None
    
    # Core content
    rule_statement: str = ""
    rule_word_count: int = 0
    
    # Hierarchical structure
    subtopics: List[str] = field(default_factory=list)
    
    # Multi-modal learning
    story_method: Optional[str] = None
    mnemonic: Optional[str] = None
    mnemonic_type: Optional[str] = None  # rhythmic, acronym, visual
    kinesthetic_gesture: Optional[str] = None
    ascii_visual: Optional[str] = None
    
    # Elements and analysis
    elements: List[str] = field(default_factory=list)
    pitfalls: List[str] = field(default_factory=list)
    
    # Practice materials
    micro_hypos: List[MicroHypo] = field(default_factory=list)
    
    # Comparative analysis
    contrasts: List[ContrastRow] = field(default_factory=list)
    
    # Decision logic
    flowchart: Optional[FlowchartNode] = None
    
    # Metadata
    emoji: Optional[str] = None
    difficulty: int = 3
    exam_frequency: Optional[str] = None

class AdvancedRealPropertyParser:
    """Parse complex real property materials"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.concepts = []
        # Map section numbers to their expected emoji when the outline omits them
        self.section_emoji_map = {
            "1": "🏰",
            "2": "📜",
            "3": "🛤️",
            "4": "👥",
            "5": "🏠",
            "6": "🏦",
            "7": "🏛️",
            "8": "⚔️",
            "9": "🪑",
            "10": "💧",
            "11": "⛏️",
            "12": "🎯",
            "13": "🏗️",
            "14": "🗓️",
        }

    def parse_outline(self, filepath: Path) -> List[AdvancedConcept]:
        """Parse the main outline with all features"""
        content = filepath.read_text()
        concepts = []

        # Identify all major outline sections. Some headings omit the emoji, so
        # we capture an optional emoji followed by the numbered title.
        emoji_class = "\u2600-\u27BF\U0001F300-\U0001FAFF"
        pattern = re.compile(
            rf'^##\s+(?:([{emoji_class}])\s+)?(\d+)([.)])?\s*(.+)$',
            re.MULTILINE
        )

        matches = list(pattern.finditer(content))
        for index, match in enumerate(matches):
            emoji_group, section_number, _, name = match.groups()
            emoji = emoji_group if emoji_group else None
            name = name.strip()
            if name.startswith('-'):
                name = f"{section_number}{name}"
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
            section_content = content[start:end]

            if not emoji:
                emoji = self.section_emoji_map.get(section_number, "📘")

            concept = self._parse_major_section(emoji, name, section_content)
            if concept:
                concepts.append(concept)

        return concepts

    def _parse_major_section(self, emoji: str, name: str, content: str) -> Optional[AdvancedConcept]:
        """Parse a major section with all sub-elements"""
        concept_id = f"real_property_{name.lower().replace(' ', '_').replace('&', 'and')}"
        concept_id = re.sub(r'[^a-z0-9_]', '', concept_id)

        concept = AdvancedConcept(
            concept_id=concept_id,
            name=name,
            subject="real_property",
            emoji=emoji
        )
        
        # Extract rule statement
        rule_match = re.search(r'\*\*Rule \((\d+) words?\):\*\*\s*(.+?)(?:\n\n|\*\*)', content, re.DOTALL)
        if rule_match:
            concept.rule_word_count = int(rule_match.group(1))
            concept.rule_statement = rule_match.group(2).strip()
        
        # Extract story method
        story_match = re.search(r'\*\*🎭 Story Method - "(.+?)":\*\*\s*(.+?)(?:\n\n|\*\*)', content, re.DOTALL)
        if story_match:
            concept.story_method = f"{story_match.group(1)}: {story_match.group(2).strip()}"
        
        # Extract subtopics (bullets under Major Subtopics)
        subtopics_section = re.search(r'\*\*Major Subtopics:\*\*\s*\n((?:- \*\*.+?\n)+)', content)
        if subtopics_section:
            subtopics = re.findall(r'- \*\*(.+?):\*\*', subtopics_section.group(1))
            concept.subtopics = subtopics
        
        # Extract mnemonic
        mnemonic_match = re.search(r'\*\*🎵 Rhythmic Mnemonic: "(.+?)"', content)
        if mnemonic_match:
            concept.mnemonic = mnemonic_match.group(1)
            concept.mnemonic_type = "rhythmic"
        else:
            # Try other mnemonic types
            mnemonic_match = re.search(r'\*\*Mnemonic:\*\*\s*"?(.+?)"?(?:\n|\*\*)', content)
            if mnemonic_match:
                concept.mnemonic = mnemonic_match.group(1)
                concept.mnemonic_type = "acronym"
        
        # Extract kinesthetic gestures
        kine_match = re.search(r'\*\*🤲 Kinesthetic Memory.*?:\*\*\s*\n((?:- \*\*.+?\n)+)', content, re.DOTALL)
        if kine_match:
            gestures = re.findall(r'- \*\*(.+?):\*\* (.+)', kine_match.group(1))
            concept.kinesthetic_gesture = "; ".join([f"{g[0]}: {g[1]}" for g in gestures])
        
        # Extract ASCII visual
        ascii_match = re.search(r'```\n(.*?)\n```', content, re.DOTALL)
        if ascii_match:
            concept.ascii_visual = ascii_match.group(1)
        
        # Extract pitfalls
        pitfalls_match = re.search(r'\*\*🚨 Most-Tested Pitfalls.*?:\*\*\s*\n((?:- \*\*.+?\n)+)', content, re.DOTALL)
        if pitfalls_match:
            pitfalls = re.findall(r'- \*\*"(.+?)":\*\* (.+)', pitfalls_match.group(1))
            concept.pitfalls = [f"{p[0]}: {p[1]}" for p in pitfalls]
        
        # Extract micro-hypos
        hypo_pattern = r'\*\*Micro-Hypo (\d+) \((.+?)\):\*\*\s*(.+?)\n→ (.+?)\n\*Memory: (.+?)\*'
        hypos = re.findall(hypo_pattern, content)
        for hypo in hypos:
            concept.micro_hypos.append(MicroHypo(
                number=int(hypo[0]),
                context=hypo[1],
                scenario=hypo[2],
                answer=hypo[3],
                memory_hook=hypo[4]
            ))
        
        return concept
    
    def parse_contrast_tables(self, filepath: Path) -> Dict[str, List[ContrastRow]]:
        """Parse comparison tables"""
        content = filepath.read_text()
        tables = {}
        
        # Find table sections
        table_sections = re.split(r'\n## (.+?) COMPARISON\n', content)
        
        for i in range(1, len(table_sections), 2):
            table_name = table_sections[i]
            table_content = table_sections[i+1] if i+1 < len(table_sections) else ""
            
            # Parse markdown table
            lines = [l.strip() for l in table_content.split('\n') if '|' in l]
            if len(lines) < 3:
                continue
            
            # Extract headers
            headers = [h.strip() for h in lines[0].split('|')[1:-1]]
            
            # Extract rows (skip separator line)
            rows = []
            for line in lines[2:]:
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if cells:
                    row_data = {headers[j]: cells[j] for j in range(min(len(headers), len(cells)))}
                    rows.append(ContrastRow(
                        element=cells[0] if cells else "",
                        values=row_data
                    ))
            
            tables[table_name] = rows
        
        return tables
    
    def parse_flowcharts(self, filepath: Path) -> Dict[str, FlowchartNode]:
        """Parse decision trees"""
        content = filepath.read_text()
        flowcharts = {}
        
        # Find flowchart sections
        sections = re.split(r'\n## \d+\. (.+?)\n', content)
        
        for i in range(1, len(sections), 2):
            name = sections[i]
            section_content = sections[i+1] if i+1 < len(sections) else ""
            
            # Extract the ASCII tree
            tree_match = re.search(r'```\n(.*?)\n```', section_content, re.DOTALL)
            if tree_match:
                tree_text = tree_match.group(1)
                # Simplified parsing - just store the text
                flowcharts[name] = FlowchartNode(
                    question=name,
                    yes_path=tree_text  # Store full tree as text for now
                )
        
        return flowcharts
    
    def export_to_python(self, concepts: List[AdvancedConcept]) -> str:
        """Generate Python code for KnowledgeNode objects"""
        code = "# Generated Advanced Real Property Concepts\n\n"
        code += "real_property_concepts = [\n"
        
        for concept in concepts:
            code += "    KnowledgeNode(\n"
            code += f"        concept_id=\"{concept.concept_id}\",\n"
            code += f"        name=\"{concept.name}\",\n"
            code += f"        subject=\"real_property\",\n"
            code += f"        difficulty={concept.difficulty},\n"
            code += f"        rule_statement=\"{concept.rule_statement[:200]}\",\n"
            code += f"        elements={concept.subtopics},\n"
            code += f"        common_traps={[p[:100] for p in concept.pitfalls[:3]]},\n"
            if concept.mnemonic:
                code += f"        # Mnemonic: {concept.mnemonic}\n"
            code += "    ),\n"
        
        code += "]\n"
        return code
    
    def export_to_json(self, concepts: List[AdvancedConcept], filepath: Path):
        """Export to JSON for data interchange"""
        data = [asdict(c) for c in concepts]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

def main():
    print("="*70)
    print("ADVANCED REAL PROPERTY PARSER")
    print("="*70)
    
    parser = AdvancedRealPropertyParser(Path("."))
    
    # Parse outline
    print("\n📖 Parsing real_property_outline.md...")
    concepts = parser.parse_outline(Path("real_property_outline.md"))
    print(f"✓ Extracted {len(concepts)} major concepts")
    
    for c in concepts:
        print(f"\n  {c.emoji} {c.name}")
        print(f"     Rule: {c.rule_word_count} words")
        print(f"     Subtopics: {len(c.subtopics)}")
        print(f"     Micro-hypos: {len(c.micro_hypos)}")
        if c.mnemonic:
            print(f"     Mnemonic: {c.mnemonic[:50]}...")
    
    # Parse contrast tables
    print("\n📊 Parsing contrast tables...")
    tables = parser.parse_contrast_tables(Path("real_property_contrast_tables.md"))
    print(f"✓ Extracted {len(tables)} comparison tables")
    
    # Parse flowcharts
    print("\n🌳 Parsing flowcharts...")
    flowcharts = parser.parse_flowcharts(Path("real_property_flowchart.md"))
    print(f"✓ Extracted {len(flowcharts)} decision trees")
    
    # Export
    print("\n💾 Exporting...")
    python_code = parser.export_to_python(concepts)
    Path("real_property_advanced.py").write_text(python_code)
    print("✓ Python code: real_property_advanced.py")
    
    parser.export_to_json(concepts, Path("real_property_advanced.json"))
    print("✓ JSON data: real_property_advanced.json")
    
    print("\n" + "="*70)
    print("✅ ADVANCED PARSING COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    main()

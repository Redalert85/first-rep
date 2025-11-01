#!/usr/bin/env python3
"""
Fixed Advanced Real Property Parser - Captures all 9 major sections
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
    values: Dict[str, str]

@dataclass
class FlowchartNode:
    """Decision tree node"""
    question: str
    tree_content: str = ""

@dataclass
class AdvancedConcept:
    """Rich legal concept with all learning modalities"""
    concept_id: str
    name: str
    subject: str
    
    # Core content
    rule_statement: str = ""
    rule_word_count: int = 0
    
    # Hierarchical structure
    subtopics: List[str] = field(default_factory=list)
    
    # Multi-modal learning
    story_method: Optional[str] = None
    mnemonic: Optional[str] = None
    mnemonic_type: Optional[str] = None
    kinesthetic_gesture: Optional[str] = None
    ascii_visual: Optional[str] = None
    
    # Practice materials
    micro_hypos: List[MicroHypo] = field(default_factory=list)
    pitfalls: List[str] = field(default_factory=list)
    
    # Metadata
    emoji: Optional[str] = None
    difficulty: int = 3

class AdvancedRealPropertyParser:
    """Parse complex real property materials"""
    
    def __init__(self):
        self.concepts = []
        
    def parse_outline(self, filepath: Path) -> List[AdvancedConcept]:
        """Parse the main outline with all features"""
        content = filepath.read_text()
        concepts = []
        
        # Split by major sections - look for ## with emoji and number
        pattern = r'\n## ([🏰📜🛤️👥🏠🏦🏛️⚔️🪑]) (\d+)\. (.+?)\n'
        sections = re.split(pattern, content)
        
        # Process in groups of 4: text, emoji, number, name
        for i in range(1, len(sections), 4):
            if i+3 >= len(sections):
                break
                
            emoji = sections[i]
            section_num = sections[i+1]
            name = sections[i+2]
            section_content = sections[i+3]
            
            concept = self._parse_major_section(emoji, name, section_content)
            if concept:
                concepts.append(concept)
                print(f"  ✓ Parsed: {emoji} {name}")
        
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
        story_match = re.search(r'\*\*🎭 Story Method[^:]*:\*\*\s*(.+?)(?:\n\n\*\*|$)', content, re.DOTALL)
        if story_match:
            story_text = story_match.group(1).strip()
            concept.story_method = story_text[:200]
        
        # Extract subtopics
        subtopics_match = re.search(r'\*\*Major Subtopics:\*\*\s*\n((?:- \*\*[^:]+:[^\n]+\n?)+)', content, re.DOTALL)
        if subtopics_match:
            subtopics = re.findall(r'- \*\*([^:]+):', subtopics_match.group(1))
            concept.subtopics = subtopics[:8]
        
        # Extract mnemonic
        mnemonic_match = re.search(r'Mnemonic[^:]*:\s*["\']?([^"\'\n]+)', content)
        if mnemonic_match:
            concept.mnemonic = mnemonic_match.group(1).strip()
            if '🎵' in content:
                concept.mnemonic_type = "rhythmic"
            else:
                concept.mnemonic_type = "acronym"
        
        # Extract kinesthetic gestures
        kine_match = re.search(r'🤲 Kinesthetic Memory[^:]*:\*\*\s*\n((?:- \*\*[^:]+:[^\n]+\n?)+)', content, re.DOTALL)
        if kine_match:
            gestures = re.findall(r'- \*\*([^:]+):\*\* ([^\n]+)', kine_match.group(1))
            concept.kinesthetic_gesture = "; ".join([f"{g[0]}: {g[1]}" for g in gestures[:3]])
        
        # Extract ASCII visual
        ascii_match = re.search(r'```\n(.*?)\n```', content, re.DOTALL)
        if ascii_match:
            concept.ascii_visual = ascii_match.group(1)
        
        # Extract pitfalls
        pitfalls_match = re.search(r'🚨 Most-Tested Pitfalls[^:]*:\*\*\s*\n((?:- \*\*[^:]+:[^\n]+\n?)+)', content, re.DOTALL)
        if pitfalls_match:
            pitfalls = re.findall(r'- \*\*"([^"]+)":\*\* ([^\n]+)', pitfalls_match.group(1))
            concept.pitfalls = [f"{p[0]}: {p[1]}" for p in pitfalls[:5]]
        
        # Extract micro-hypos
        hypo_pattern = r'\*\*Micro-Hypo (\d+) \(([^)]+)\):\*\*\s*([^\n]+)\n[→»]\s*([^\n]+)\n\*Memory: ([^\n*]+)'
        hypos = re.findall(hypo_pattern, content)
        for hypo in hypos:
            concept.micro_hypos.append(MicroHypo(
                number=int(hypo[0]),
                context=hypo[1],
                scenario=hypo[2].strip(),
                answer=hypo[3].strip(),
                memory_hook=hypo[4].strip()
            ))
        
        return concept
    
    def parse_contrast_tables(self, filepath: Path) -> Dict[str, List[ContrastRow]]:
        """Parse comparison tables"""
        content = filepath.read_text()
        tables = {}
        
        # Find table sections
        table_sections = re.split(r'\n## ([A-Z\s&]+) COMPARISON\n', content)
        
        for i in range(1, len(table_sections), 2):
            table_name = table_sections[i].strip()
            table_content = table_sections[i+1] if i+1 < len(table_sections) else ""
            
            # Parse markdown table
            lines = [l.strip() for l in table_content.split('\n') if '|' in l]
            if len(lines) < 3:
                continue
            
            # Extract headers
            headers = [h.strip().replace('**', '') for h in lines[0].split('|')[1:-1]]
            
            # Extract rows (skip separator line)
            rows = []
            for line in lines[2:]:
                if not line.strip() or line.startswith('###'):
                    break
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if cells and len(cells) >= 2:
                    row_data = {headers[j]: cells[j] for j in range(min(len(headers), len(cells)))}
                    rows.append(ContrastRow(
                        element=cells[0],
                        values=row_data
                    ))
            
            if rows:
                tables[table_name] = rows
        
        return tables
    
    def parse_flowcharts(self, filepath: Path) -> Dict[str, FlowchartNode]:
        """Parse decision trees"""
        content = filepath.read_text()
        flowcharts = {}
        
        # Find flowchart sections
        sections = re.split(r'\n## \d+\. (.+?)\n', content)
        
        for i in range(1, len(sections), 2):
            name = sections[i].strip()
            section_content = sections[i+1] if i+1 < len(sections) else ""
            
            # Extract the ASCII tree
            tree_match = re.search(r'```\n(.*?)\n```', section_content, re.DOTALL)
            if tree_match:
                flowcharts[name] = FlowchartNode(
                    question=name,
                    tree_content=tree_match.group(1)
                )
        
        return flowcharts
    
    def export_to_python(self, concepts: List[AdvancedConcept]) -> str:
        """Generate Python code for KnowledgeNode objects"""
        code = '    def _initialize_real_property(self):\n'
        code += '        """Initialize real property concepts with advanced features"""\n'
        code += "        concepts = [\n"
        
        for concept in concepts:
            code += "            KnowledgeNode(\n"
            code += f"                concept_id=\"{concept.concept_id}\",\n"
            code += f"                name=\"{concept.name}\",\n"
            code += f"                subject=\"real_property\",\n"
            code += f"                difficulty={concept.difficulty},\n"
            
            # Escape quotes in rule
            rule_escaped = concept.rule_statement.replace('"', '\\"').replace('\n', ' ')[:200]
            code += f"                rule_statement=\"{rule_escaped}\",\n"
            
            code += f"                elements={concept.subtopics[:5]},\n"
            code += "                policy_rationales=[],\n"
            
            if concept.pitfalls:
                code += "                common_traps=[\n"
                for trap in concept.pitfalls[:3]:
                    trap_escaped = trap.replace('"', '\\"').replace('\n', ' ')[:100]
                    code += f"                    \"{trap_escaped}\",\n"
                code += "                ],\n"
            else:
                code += "                common_traps=[],\n"
            
            if concept.mnemonic:
                code += f"                # Mnemonic ({concept.mnemonic_type}): {concept.mnemonic[:60]}\n"
            
            code += "            ),\n"
        
        code += "        ]\n"
        code += "        for node in concepts:\n"
        code += "            self.nodes[node.concept_id] = node\n"
        
        return code
    
    def export_to_json(self, concepts: List[AdvancedConcept], filepath: Path):
        """Export to JSON"""
        data = []
        for c in concepts:
            # Convert micro_hypos to dict
            c_dict = asdict(c)
            data.append(c_dict)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

def main():
    print("="*70)
    print("ADVANCED REAL PROPERTY PARSER v2.0")
    print("="*70)
    
    parser = AdvancedRealPropertyParser()
    
    # Parse outline
    print("\n📖 Parsing real_property_outline.md...")
    concepts = parser.parse_outline(Path("real_property_outline.md"))
    print(f"\n✓ Extracted {len(concepts)} major concepts\n")
    
    # Show summary
    for c in concepts:
        print(f"  {c.emoji} {c.name}")
        print(f"     Rule: {c.rule_word_count} words")
        print(f"     Subtopics: {len(c.subtopics)}")
        print(f"     Micro-hypos: {len(c.micro_hypos)}")
        print(f"     Pitfalls: {len(c.pitfalls)}")
        if c.mnemonic:
            print(f"     Mnemonic: {c.mnemonic[:50]}...")
        print()
    
    # Parse contrast tables
    print("\n📊 Parsing contrast tables...")
    tables = parser.parse_contrast_tables(Path("real_property_contrast_tables.md"))
    print(f"✓ Extracted {len(tables)} comparison tables")
    for name, rows in tables.items():
        print(f"   • {name}: {len(rows)} comparisons")
    
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
    print(f"\nReady to integrate {len(concepts)} real property concepts")
    print("into your bar exam tutor!")

if __name__ == "__main__":
    main()

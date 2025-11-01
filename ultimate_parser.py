#!/usr/bin/env python3
"""
Ultimate Real Property Parser - Handles all section formats
"""

import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional

@dataclass
class MicroHypo:
    number: int
    context: str
    scenario: str
    answer: str
    memory_hook: Optional[str] = None

@dataclass
class AdvancedConcept:
    """Rich legal concept"""
    concept_id: str
    name: str
    subject: str
    section_number: int
    
    # Core content
    rule_statement: str = ""
    rule_word_count: int = 0
    
    # Structure
    subtopics: List[str] = field(default_factory=list)
    
    # Learning aids
    story_method: Optional[str] = None
    mnemonic: Optional[str] = None
    mnemonic_type: Optional[str] = None
    kinesthetic_gesture: Optional[str] = None
    ascii_visual: Optional[str] = None
    
    # Practice
    micro_hypos: List[MicroHypo] = field(default_factory=list)
    pitfalls: List[str] = field(default_factory=list)
    
    # Metadata
    emoji: Optional[str] = None
    difficulty: int = 3

class UltimateParser:
    """Parse all real property content"""
    
    EMOJI_MAP = {
        1: "🏰", 2: "📜", 3: "🛤️", 4: "👥", 5: "🏠",
        6: "🏦", 7: "🏛️", 8: "⚔️", 9: "🪑"
    }
    
    def parse_outline(self, filepath: Path) -> List[AdvancedConcept]:
        """Parse all numbered sections (1-9 from LAND BARON framework)"""
        content = filepath.read_text()
        concepts = []
        
        # Pattern: ## [emoji?] NUMBER. NAME
        # Matches: "## 🏰 1. ESTATES" or "## 3. EASEMENTS"
        pattern = r'\n## ([🏰📜🛤️👥🏠🏦🏛️⚔️🪑])? ?(\d+)\. (.+?)\n'
        matches = list(re.finditer(pattern, content))
        
        for i, match in enumerate(matches):
            emoji = match.group(1)
            section_num = int(match.group(2))
            name = match.group(3).strip()
            
            # Skip sections beyond 9 (study plans, etc.)
            if section_num > 9:
                break
            
            # Get section content (up to next ## or end)
            start = match.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(content)
            section_content = content[start:end]
            
            # Assign emoji if missing
            if not emoji and section_num in self.EMOJI_MAP:
                emoji = self.EMOJI_MAP[section_num]
            
            concept = self._parse_section(emoji, section_num, name, section_content)
            if concept:
                concepts.append(concept)
                print(f"  ✓ Parsed: {emoji or '📋'} #{section_num} {name}")
        
        return concepts
    
    def _parse_section(self, emoji: Optional[str], num: int, name: str, content: str) -> Optional[AdvancedConcept]:
        """Parse individual section"""
        concept_id = f"real_property_{name.lower().replace(' ', '_').replace(',', '').replace('&', 'and')}"
        concept_id = re.sub(r'[^a-z0-9_]', '', concept_id)
        
        concept = AdvancedConcept(
            concept_id=concept_id,
            name=name,
            subject="real_property",
            section_number=num,
            emoji=emoji
        )
        
        # Extract rule (with word count)
        rule_match = re.search(r'\*\*Rule \((\d+) words?\):\*\*\s*(.+?)(?:\n\n|\*\*)', content, re.DOTALL)
        if rule_match:
            concept.rule_word_count = int(rule_match.group(1))
            concept.rule_statement = rule_match.group(2).strip()
        
        # Extract story method
        story_match = re.search(r'\*\*🎭 Story Method[^:]*:\*\*\s*(.+?)(?:\n\n\*\*|$)', content, re.DOTALL)
        if story_match:
            concept.story_method = story_match.group(1).strip()[:300]
        
        # Extract subtopics
        subtopics_match = re.search(r'\*\*Major Subtopics:\*\*\s*\n((?:- \*\*[^:]+:[^\n]+\n?)+)', content, re.DOTALL)
        if subtopics_match:
            subtopics = re.findall(r'- \*\*([^:]+):', subtopics_match.group(1))
            concept.subtopics = subtopics[:8]
        
        # Extract mnemonic (various formats)
        mnemonic_patterns = [
            r'Mnemonic[^:]*:\s*["\']([^"\'\n]+)',
            r'🎵 Rhythmic Mnemonic[^:]*:\s*["\']([^"\'\n]+)',
            r'\*\*Acronym:\*\*\s*([A-Z]+)',
        ]
        for pattern in mnemonic_patterns:
            match = re.search(pattern, content)
            if match:
                concept.mnemonic = match.group(1).strip()
                if '🎵' in content or 'Rhythmic' in content:
                    concept.mnemonic_type = "rhythmic"
                else:
                    concept.mnemonic_type = "acronym"
                break
        
        # Extract kinesthetic gestures
        kine_match = re.search(r'🤲 Kinesthetic[^:]*:\*\*\s*\n((?:- \*\*[^:]+:[^\n]+\n?)+)', content, re.DOTALL)
        if kine_match:
            gestures = re.findall(r'- \*\*([^:]+):\*\* ([^\n]+)', kine_match.group(1))
            concept.kinesthetic_gesture = "; ".join([f"{g[0]}: {g[1]}" for g in gestures[:3]])
        
        # Extract ASCII visual
        ascii_match = re.search(r'```\n(.*?)\n```', content, re.DOTALL)
        if ascii_match:
            concept.ascii_visual = ascii_match.group(1)[:500]
        
        # Extract pitfalls
        pitfalls_match = re.search(r'🚨 Most-Tested Pitfalls[^:]*:\*\*\s*\n((?:- \*\*[^:]+:[^\n]+\n?)+)', content, re.DOTALL)
        if pitfalls_match:
            pitfalls = re.findall(r'- \*\*"?([^":\n]+)"?:\*\* ([^\n]+)', pitfalls_match.group(1))
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
    
    def export_to_python(self, concepts: List[AdvancedConcept]) -> str:
        """Generate Python code"""
        code = '    def _initialize_real_property(self):\n'
        code += '        """Initialize real property - LAND BARON framework (9 concepts)"""\n'
        code += "        concepts = [\n"
        
        for concept in concepts:
            code += "            KnowledgeNode(\n"
            code += f"                concept_id=\"{concept.concept_id}\",\n"
            code += f"                name=\"{concept.name}\",\n"
            code += f"                subject=\"real_property\",\n"
            code += f"                difficulty={concept.difficulty},\n"
            
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
                code += f"                # {concept.emoji} Mnemonic ({concept.mnemonic_type}): {concept.mnemonic[:60]}\n"
            
            code += "            ),\n"
        
        code += "        ]\n"
        code += "        for node in concepts:\n"
        code += "            self.nodes[node.concept_id] = node\n"
        
        return code

def main():
    print("="*70)
    print("ULTIMATE REAL PROPERTY PARSER v3.0")
    print("="*70)
    
    parser = UltimateParser()
    
    print("\n📖 Parsing real_property_outline.md (sections 1-9)...")
    concepts = parser.parse_outline(Path("real_property_outline.md"))
    
    print(f"\n✓ Extracted {len(concepts)}/9 LAND BARON concepts\n")
    
    # Show detailed summary
    for c in concepts:
        print(f"  {c.emoji} #{c.section_number}. {c.name}")
        print(f"     Rule: {c.rule_word_count} words")
        print(f"     Subtopics: {len(c.subtopics)}")
        print(f"     Micro-hypos: {len(c.micro_hypos)}")
        print(f"     Pitfalls: {len(c.pitfalls)}")
        if c.mnemonic:
            print(f"     Mnemonic: {c.mnemonic[:40]}...")
        print()
    
    # Export
    print("💾 Exporting...")
    python_code = parser.export_to_python(concepts)
    Path("real_property_code.py").write_text(python_code)
    print("✓ Python: real_property_code.py")
    
    # Save JSON
    data = [asdict(c) for c in concepts]
    with open("real_property_full.json", 'w') as f:
        json.dump(data, f, indent=2)
    print("✓ JSON: real_property_full.json")
    
    print("\n" + "="*70)
    print("✅ PARSING COMPLETE!")
    print("="*70)
    print(f"\nReady to add {len(concepts)} Real Property concepts")
    print("(Estates, Conveyancing, Easements, Concurrent, Landlord-Tenant,")
    print(" Mortgages, Zoning, Adverse Possession, Fixtures)")

if __name__ == "__main__":
    main()

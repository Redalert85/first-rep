#!/usr/bin/env python3
"""
Knowledge Base Expansion Script
Parses mbe_master_guide.md and generates Python code for KnowledgeNode objects
"""

import re
from pathlib import Path

def parse_master_guide(filepath):
    """Parse the master guide and extract all concepts"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    concepts = []
    current_subject = None
    subject_map = {
        'Constitutional Law': 'constitutional_law',
        'Torts': 'torts',
        'Contracts': 'contracts',
        'Criminal Law': 'criminal_law',
        'Criminal Procedure': 'criminal_procedure',
        'Civil Procedure': 'civil_procedure',
        'Evidence': 'evidence'
    }
    
    # Split by major subjects
    sections = re.split(r'^## (.+?)$', content, flags=re.MULTILINE)
    
    for i in range(1, len(sections), 2):
        section_title = sections[i].strip()
        section_content = sections[i+1] if i+1 < len(sections) else ""
        
        # Find subject name
        for subj_name, subj_id in subject_map.items():
            if subj_name in section_title:
                current_subject = subj_id
                break
        
        if not current_subject:
            continue
        
        # Find all #### subsections (concepts)
        subsections = re.split(r'^#### (\d+\. .+?)$', section_content, flags=re.MULTILINE)
        
        for j in range(1, len(subsections), 2):
            concept_title = subsections[j].strip()
            concept_content = subsections[j+1] if j+1 < len(subsections) else ""
            
            # Skip "Visuals" sections
            if 'Visual' in concept_title or 'Flowchart' in concept_title:
                continue
            
            # Extract components
            rule_match = re.search(r'\*\*Rule\*\*:\s*(.+?)(?:\n|\.\.\.)', concept_content)
            mnemonic_match = re.search(r'\*\*Mnemonic\*\*:\s*`(.+?)`', concept_content)
            traps_match = re.search(r'\*\*Traps\*\*:\s*(.+?)(?:\n-|\*\*|$)', concept_content, re.DOTALL)
            
            # Clean concept title
            clean_title = re.sub(r'^\d+\.\s*', '', concept_title)
            clean_title = re.sub(r'\s*–.+$', '', clean_title)
            clean_title = clean_title.strip()
            
            # Generate concept ID
            concept_id = f"{current_subject}_{clean_title.lower().replace(' ', '_').replace('&', 'and')}"
            concept_id = re.sub(r'[^a-z0-9_]', '', concept_id)
            
            # Extract rule
            rule = rule_match.group(1).strip() if rule_match else "See study guide for details"
            
            # Extract mnemonic
            mnemonic = mnemonic_match.group(1) if mnemonic_match else None
            
            # Extract traps
            traps = []
            if traps_match:
                traps_text = traps_match.group(1).strip()
                traps = [t.strip() for t in traps_text.split(',') if t.strip()]
                traps = traps[:3]
            
            # Estimate difficulty
            difficulty = 3
            if any(word in concept_title.lower() for word in ['commerce', 'hearsay', 'jurisdiction']):
                difficulty = 4
            elif any(word in concept_title.lower() for word in ['formation', 'elements']):
                difficulty = 2
            
            concepts.append({
                'concept_id': concept_id,
                'name': clean_title,
                'subject': current_subject,
                'difficulty': difficulty,
                'rule_statement': rule[:150] if len(rule) > 150 else rule,
                'mnemonic': mnemonic,
                'common_traps': traps
            })
    
    return concepts

def generate_python_code(concepts, subject):
    """Generate Python code for a subject's concepts"""
    subject_concepts = [c for c in concepts if c['subject'] == subject]
    
    if not subject_concepts:
        return ""
    
    code = f"    def _initialize_{subject}(self):\n"
    code += f'        """Initialize {subject} concepts from master guide"""\n'
    code += f"        concepts = [\n"
    
    for concept in subject_concepts:
        code += "            KnowledgeNode(\n"
        code += f"                concept_id=\"{concept['concept_id']}\",\n"
        code += f"                name=\"{concept['name']}\",\n"
        code += f"                subject=\"{concept['subject']}\",\n"
        code += f"                difficulty={concept['difficulty']},\n"
        
        # Escape quotes in rule
        rule_escaped = concept['rule_statement'].replace('"', '\\"')
        code += f"                rule_statement=\"{rule_escaped}\",\n"
        
        code += "                elements=[],\n"
        code += "                policy_rationales=[],\n"
        
        if concept['common_traps']:
            code += "                common_traps=[\n"
            for trap in concept['common_traps']:
                trap_escaped = trap.replace('"', '\\"')
                code += f"                    \"{trap_escaped}\",\n"
            code += "                ]\n"
        else:
            code += "                common_traps=[]\n"
        
        code += "            ),\n"
    
    code += "        ]\n"
    code += "        for node in concepts:\n"
    code += "            self.nodes[node.concept_id] = node\n"
    code += "\n"
    
    return code

def main():
    guide_path = Path("mbe_master_guide.md")
    
    if not guide_path.exists():
        print(f"Error: {guide_path} not found")
        return
    
    print("="*70)
    print("KNOWLEDGE BASE EXPANSION TOOL")
    print("="*70)
    print("\nParsing mbe_master_guide.md...")
    
    concepts = parse_master_guide(guide_path)
    
    print(f"\n✓ Found {len(concepts)} concepts\n")
    
    subjects = {}
    for c in concepts:
        subjects[c['subject']] = subjects.get(c['subject'], 0) + 1
    
    print("Concepts by subject:")
    for subj, count in sorted(subjects.items()):
        print(f"  • {subj}: {count} concepts")
    
    print("\n" + "="*70)
    print("GENERATED CODE (copy this into bar_tutor_unified.py)")
    print("="*70 + "\n")
    
    # Generate code for each subject
    all_subjects = ['torts', 'contracts', 'criminal_law', 'criminal_procedure', 
                    'civil_procedure', 'evidence', 'constitutional_law']
    
    for subject in all_subjects:
        code = generate_python_code(concepts, subject)
        if code:
            print(code)
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("1. Copy the generated code above")
    print("2. Open bar_tutor_unified.py in an editor")
    print("3. Find and replace the _initialize_<subject> methods")
    print("4. Save the file")
    print("5. Test: python3 test_tutor.py")
    print("6. Run: python3 bar_tutor_unified.py")

if __name__ == "__main__":
    main()

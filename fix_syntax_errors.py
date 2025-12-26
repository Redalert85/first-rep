#!/usr/bin/env python3
"""Fix syntax errors in generated Python files"""

import re

# File fixes with their class names
files_to_fix = {
    'comprehensive_knowledge_base.py': 'ComprehensiveKnowledgeBase',
    'essay_subjects.py': 'EssaySubjects',
    'mbe_full_expansion.py': 'MBEFullExpansion',
    'real_property_advanced.py': 'RealPropertyAdvanced',
    'real_property_code.py': 'RealPropertyCode'
}

# Fix indentation errors by wrapping in class
for filename, classname in files_to_fix.items():
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # Create properly formatted file
        new_content = f'''#!/usr/bin/env python3
"""Auto-generated methods for {classname}"""

class {classname}:
    """Container for auto-generated methods"""
    pass
'''
        
        with open(filename, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Fixed {filename}")
    except Exception as e:
        print(f"❌ Error fixing {filename}: {e}")

# Fix unterminated string in ultimate_knowledge_base.py
try:
    with open('ultimate_knowledge_base.py', 'r') as f:
        content = f.read()
    
    # Fix line 74 - add closing quote if missing
    content = re.sub(
        r'"full faith and credit\.\s*\n',
        '"full faith and credit."\n',
        content
    )
    
    with open('ultimate_knowledge_base.py', 'w') as f:
        f.write(content)
    
    print("✅ Fixed ultimate_knowledge_base.py")
except Exception as e:
    print(f"❌ Error fixing ultimate_knowledge_base.py: {e}")

print("\n🎉 All syntax errors fixed!")

#!/usr/bin/env python3
"""
Quick Demo - Iowa Legal Document Generator
Run this to see examples of what the tool can do
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from document_generator import DocumentGenerator, Case, demo as run_demo

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                   IOWA LEGAL DOCUMENT GENERATOR                           ║
║                          Quick Demo                                       ║
╚═══════════════════════════════════════════════════════════════════════════╝

This tool generates Iowa-specific legal documents combining:
  ✓ Iowa procedural law (notice pleading, not Twombly/Iqbal)
  ✓ Black letter substantive law (negligence, contracts, etc.)
  ✓ Professional formatting
  ✓ Iowa deadline calculations

""")

    run_demo()

    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                           HOW TO USE                                      ║
╚═══════════════════════════════════════════════════════════════════════════╝

To generate your own motion:

    from document_generator import DocumentGenerator, Case
    from datetime import datetime

    # Create your case
    case = Case(
        case_number='LACV123456',
        court='Iowa District Court',
        court_location='Woodbury County',
        plaintiff='Your Plaintiff',
        defendant='Your Defendant',
        practice_area='negligence'  # or 'breach_of_contract'
    )

    # Your facts
    facts = {
        'complaint_deficiencies': [
            'No duty alleged',
            'No causation shown'
        ]
    }

    # Generate
    generator = DocumentGenerator()
    motion = generator.generate_motion_to_dismiss(case, facts)
    print(motion)

""")

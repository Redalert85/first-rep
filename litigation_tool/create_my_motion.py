#!/usr/bin/env python3
"""
Create Your Own Motion - Customizable Template
Edit the case and facts below, then run: python3 create_my_motion.py
"""
import sys
sys.path.insert(0, 'src')

from document_generator import DocumentGenerator, Case
from datetime import datetime

# ============================================================================
# CUSTOMIZE YOUR CASE HERE
# ============================================================================

case = Case(
    case_number='LACV123456',           # Your case number
    court='Iowa District Court',        # Or 'U.S. District Court, N.D. Iowa'
    court_location='Woodbury County',   # County or Division
    plaintiff='Jane Doe',               # Plaintiff name
    defendant='John Smith',             # Defendant name
    practice_area='negligence',         # 'negligence', 'breach_of_contract', etc.
    trial_date=datetime(2025, 6, 15)    # Your trial date (optional)
)

# ============================================================================
# CUSTOMIZE YOUR FACTS HERE
# ============================================================================

# For NEGLIGENCE cases:
facts_negligence = {
    'complaint_deficiencies': [
        'The Complaint fails to allege that Defendant owed Plaintiff any duty of care',
        'The Complaint contains no factual allegations of breach',
        'The Complaint fails to allege causation',
        'Damages are pled conclusorily without factual support'
    ],
    'damages_argument': 'The Complaint alleges only that Plaintiff suffered "damages" without any specific factual allegations regarding the nature or extent of those damages.'
}

# For CONTRACT cases:
facts_contract = {
    'complaint_deficiencies': [
        'No valid offer is alleged with definite terms',
        'No acceptance is alleged',
        'Consideration is not properly pled'
    ],
    'offer_deficiency': 'The alleged "offer" in ¶ 10 lacks definite terms regarding price, quantity, and time for performance.',
    'acceptance_deficiency': 'The Complaint does not allege any facts showing unequivocal acceptance of the alleged offer.',
    'consideration_argument': 'The Complaint fails to allege a bargained-for exchange. The alleged "consideration" in ¶ 15 is past consideration, which is not valid.'
}

# ============================================================================
# CHOOSE WHICH FACTS TO USE
# ============================================================================

# For negligence case, use this:
facts = facts_negligence

# For contract case, use this instead:
# facts = facts_contract

# ============================================================================
# GENERATE THE MOTION
# ============================================================================

print("Generating motion...")

generator = DocumentGenerator()
motion = generator.generate_motion_to_dismiss(case, facts)

# Save to file
output_file = 'Motion_to_Dismiss.txt'
with open(output_file, 'w') as f:
    f.write(motion)

print(f"\n✅ SUCCESS! Motion saved to: {output_file}\n")

# Print preview
print("="*80)
print("PREVIEW (first 50 lines):")
print("="*80)
lines = motion.split('\n')
for line in lines[:50]:
    print(line)

if len(lines) > 50:
    print(f"\n... ({len(lines) - 50} more lines in file)")

print("\n" + "="*80)

# Show Iowa deadlines if trial date provided
if case.trial_date:
    print("IOWA DEADLINES:")
    print("="*80)
    deadlines = generator.calculate_iowa_deadlines(case.trial_date)
    print(f"Trial Date:           {deadlines['trial_date'].strftime('%B %d, %Y')}")
    print(f"Discovery Cutoff:     {deadlines['discovery_cutoff'].strftime('%B %d, %Y')} (Iowa R. Civ. P. 1.507)")
    print(f"Plaintiff Expert:     {deadlines['plaintiff_expert_disclosure'].strftime('%B %d, %Y')} (Iowa R. Civ. P. 1.500)")
    print(f"Defendant Expert:     {deadlines['defendant_expert_disclosure'].strftime('%B %d, %Y')} (Iowa R. Civ. P. 1.500)")
    print("="*80)

print(f"\n✅ Your motion is ready in: {output_file}")
print("📝 To customize: Edit the 'case' and 'facts' sections at the top of this file\n")

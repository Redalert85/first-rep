#!/bin/bash
# Bar Exam Tutor V3 Launcher

cd /Users/bcwelling/Documents/GitHub/first-rep

# Load API key from brett.env
if [ -f "brett.env" ]; then
    export $(cat brett.env | xargs)
    echo "✅ API key loaded from brett.env"
else
    echo "❌ brett.env file not found!"
    echo "Please create brett.env with: OPENAI_API_KEY=your-key-here"
    exit 1
fi

# Start the tutor
python3 -c "
import sys
sys.path.append('.')
from bar_tutor import BarTutorV3
from openai import OpenAI
import os

print('🚀 Starting Bar Exam Tutor V3...')
print('Loading elite memory system...')

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
tutor = BarTutorV3(client, 'gpt-4', 'MBE focused preparation')

print('✅ Bar Tutor V3 loaded successfully!')
print()
print('💡 Quick Start Commands:')
print('   tutor._real_property_memory_palace_agent()  # Memory palace training')
print('   tutor.advanced_mbe_drill()                  # MBE practice')
print('   tutor.get_performance_analytics()          # View progress')
print('   tutor.generate_study_plan()                # Get study plan')
print('   tutor.mistake_analyzer.analyze_wrong_answer(question, correct, wrong, explanation)')
print('   tutor.issue_spotter.train_systematic_scanning(fact_pattern)')
print()
print('💡 Available modules:')
print('   - tutor.elite_system (memory palace)')
print('   - tutor.mistake_analyzer (error patterns)')
print('   - tutor.issue_spotter (fact analysis)')
print('   - tutor.analytics (performance tracking)')
print()
print('Ready for interactive use! 🎯')
"

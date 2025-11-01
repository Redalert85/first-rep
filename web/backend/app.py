#!/usr/bin/env python3
"""
Flask Backend for MBE Bar Exam Study System
Provides REST API for the web interface
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging

# Add parent directory to path to import existing modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from bar_tutor_unified import (
    LegalKnowledgeGraph,
    FlashcardEntry,
    LearningState,
    generate_id,
    DATA_DIR
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = str(DATA_DIR / 'sessions')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Enable CORS for React frontend
CORS(app, supports_credentials=True)

# Initialize session
Session(app)

# Initialize knowledge graph
knowledge_graph = LegalKnowledgeGraph()

# ==================== HELPER FUNCTIONS ====================

def get_user_data_path(user_id: str) -> Path:
    """Get user-specific data directory"""
    user_dir = DATA_DIR / 'users' / user_id
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

def load_user_progress(user_id: str) -> dict:
    """Load user progress from file"""
    progress_file = get_user_data_path(user_id) / 'progress.json'
    if progress_file.exists():
        return json.loads(progress_file.read_text())
    return {
        'total_questions': 0,
        'correct_answers': 0,
        'by_subject': {},
        'streak': 0,
        'last_study': None
    }

def save_user_progress(user_id: str, progress: dict):
    """Save user progress to file"""
    progress_file = get_user_data_path(user_id) / 'progress.json'
    progress_file.write_text(json.dumps(progress, indent=2))

def load_user_flashcards(user_id: str) -> list:
    """Load user flashcards"""
    flashcards_file = get_user_data_path(user_id) / 'flashcards.jsonl'
    if not flashcards_file.exists():
        return []

    flashcards = []
    with flashcards_file.open('r') as f:
        for line in f:
            if line.strip():
                flashcards.append(json.loads(line))
    return flashcards

def save_flashcard(user_id: str, flashcard: dict):
    """Save a flashcard for user"""
    flashcards_file = get_user_data_path(user_id) / 'flashcards.jsonl'
    with flashcards_file.open('a') as f:
        f.write(json.dumps(flashcard) + '\n')

def get_or_create_user_id():
    """Get user ID from session or create new one"""
    if 'user_id' not in session:
        session['user_id'] = generate_id(str(datetime.now()))
        session.permanent = True
    return session['user_id']

# ==================== API ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Get all available subjects"""
    subjects = {}
    for concept_id, node in knowledge_graph.nodes.items():
        subject = node.subject
        if subject not in subjects:
            subjects[subject] = {
                'name': subject.title(),
                'count': 0,
                'concepts': []
            }
        subjects[subject]['count'] += 1
        subjects[subject]['concepts'].append({
            'id': concept_id,
            'name': node.name,
            'difficulty': node.difficulty
        })

    return jsonify({
        'subjects': list(subjects.values())
    })

@app.route('/api/concepts/<subject>', methods=['GET'])
def get_concepts_by_subject(subject):
    """Get concepts for a specific subject"""
    concepts = []
    for concept_id, node in knowledge_graph.nodes.items():
        if node.subject == subject:
            concepts.append({
                'id': concept_id,
                'name': node.name,
                'difficulty': node.difficulty,
                'rule_statement': node.rule_statement,
                'elements': node.elements,
                'prerequisites': node.prerequisites,
                'mastery_level': node.mastery_level
            })

    return jsonify({
        'subject': subject,
        'concepts': concepts
    })

@app.route('/api/concept/<concept_id>', methods=['GET'])
def get_concept_details(concept_id):
    """Get detailed information about a concept"""
    node = knowledge_graph.nodes.get(concept_id)
    if not node:
        return jsonify({'error': 'Concept not found'}), 404

    return jsonify({
        'id': concept_id,
        'name': node.name,
        'subject': node.subject,
        'difficulty': node.difficulty,
        'rule_statement': node.rule_statement,
        'elements': node.elements,
        'exceptions': node.exceptions,
        'policy_rationales': node.policy_rationales,
        'common_traps': node.common_traps,
        'prerequisites': node.prerequisites,
        'related_concepts': node.related_concepts,
        'mastery_level': node.mastery_level,
        'last_reviewed': node.last_reviewed.isoformat() if node.last_reviewed else None,
        'review_count': node.review_count
    })

@app.route('/api/practice/start', methods=['POST'])
def start_practice_session():
    """Start a new practice session"""
    user_id = get_or_create_user_id()
    data = request.json

    subject = data.get('subject', 'contracts')
    num_questions = data.get('num_questions', 5)
    difficulty = data.get('difficulty', 'mixed')

    # Get concepts for subject
    concepts = [
        node for node in knowledge_graph.nodes.values()
        if node.subject == subject
    ]

    # Filter by difficulty if specified
    if difficulty != 'mixed':
        difficulty_map = {'easy': [1, 2], 'medium': [3], 'hard': [4, 5]}
        concepts = [c for c in concepts if c.difficulty in difficulty_map.get(difficulty, [1, 2, 3, 4, 5])]

    # Select random concepts (ensure unique)
    import random
    selected = random.sample(concepts, min(num_questions, len(concepts)))

    # Create session data
    session_data = {
        'session_id': generate_id(f"{user_id}_{datetime.now()}"),
        'user_id': user_id,
        'subject': subject,
        'num_questions': num_questions,
        'difficulty': difficulty,
        'concepts': [
            {
                'id': c.concept_id,
                'name': c.name,
                'difficulty': c.difficulty,
                'rule_statement': c.rule_statement,
                'elements': c.elements,
                'common_traps': c.common_traps
            }
            for c in selected
        ],
        'current_index': 0,
        'answers': [],
        'started_at': datetime.now().isoformat()
    }

    # Store in session
    session['practice_session'] = session_data

    return jsonify({
        'session_id': session_data['session_id'],
        'total_questions': len(selected),
        'current_question': session_data['concepts'][0] if selected else None
    })

@app.route('/api/practice/answer', methods=['POST'])
def submit_practice_answer():
    """Submit answer to practice question"""
    user_id = get_or_create_user_id()
    data = request.json

    if 'practice_session' not in session:
        return jsonify({'error': 'No active session'}), 400

    practice_session = session['practice_session']
    current_index = practice_session['current_index']

    # Record answer
    answer = {
        'concept_id': data.get('concept_id'),
        'user_answer': data.get('answer'),
        'is_correct': data.get('is_correct'),
        'time_spent': data.get('time_spent', 0),
        'timestamp': datetime.now().isoformat()
    }

    practice_session['answers'].append(answer)

    # Update progress
    progress = load_user_progress(user_id)
    progress['total_questions'] += 1
    if answer['is_correct']:
        progress['correct_answers'] += 1
        progress['streak'] = progress.get('streak', 0) + 1
    else:
        progress['streak'] = 0

    subject = practice_session['subject']
    if subject not in progress['by_subject']:
        progress['by_subject'][subject] = {'total': 0, 'correct': 0}
    progress['by_subject'][subject]['total'] += 1
    if answer['is_correct']:
        progress['by_subject'][subject]['correct'] += 1

    progress['last_study'] = datetime.now().isoformat()
    save_user_progress(user_id, progress)

    # Move to next question
    practice_session['current_index'] += 1
    session['practice_session'] = practice_session

    # Check if session complete
    if practice_session['current_index'] >= len(practice_session['concepts']):
        return jsonify({
            'session_complete': True,
            'total_questions': len(practice_session['concepts']),
            'correct_answers': sum(1 for a in practice_session['answers'] if a['is_correct']),
            'accuracy': sum(1 for a in practice_session['answers'] if a['is_correct']) / len(practice_session['answers']) * 100
        })

    # Return next question
    next_question = practice_session['concepts'][practice_session['current_index']]
    return jsonify({
        'session_complete': False,
        'current_index': practice_session['current_index'],
        'current_question': next_question,
        'is_correct': answer['is_correct']
    })

@app.route('/api/flashcards', methods=['GET'])
def get_flashcards():
    """Get user flashcards"""
    user_id = get_or_create_user_id()
    subject = request.args.get('subject', None)

    flashcards = load_user_flashcards(user_id)

    if subject:
        flashcards = [f for f in flashcards if f.get('subject') == subject]

    # Sort by due date (spaced repetition)
    now = datetime.now()
    for card in flashcards:
        last_reviewed = datetime.fromisoformat(card.get('last_reviewed', card['created_at']))
        interval = card.get('interval', 1)
        next_review = last_reviewed + timedelta(days=interval)
        card['due'] = next_review < now
        card['next_review'] = next_review.isoformat()

    flashcards.sort(key=lambda x: x.get('next_review', ''))

    return jsonify({
        'flashcards': flashcards,
        'total': len(flashcards),
        'due': sum(1 for f in flashcards if f['due'])
    })

@app.route('/api/flashcards/create', methods=['POST'])
def create_flashcard():
    """Create new flashcard"""
    user_id = get_or_create_user_id()
    data = request.json

    flashcard = {
        'id': generate_id(f"{user_id}_{data['front']}"),
        'front': data['front'],
        'back': data['back'],
        'subject': data.get('subject', 'Mixed/Other'),
        'difficulty': data.get('difficulty', 'Intermediate'),
        'created_at': datetime.now().isoformat(),
        'last_reviewed': None,
        'ease_factor': 2.5,
        'interval': 1,
        'repetitions': 0
    }

    save_flashcard(user_id, flashcard)

    return jsonify({
        'success': True,
        'flashcard': flashcard
    })

@app.route('/api/flashcards/<flashcard_id>/review', methods=['POST'])
def review_flashcard(flashcard_id):
    """Record flashcard review using SM-2 algorithm"""
    user_id = get_or_create_user_id()
    data = request.json
    quality = data.get('quality', 3)  # 0-5 scale

    flashcards = load_user_flashcards(user_id)

    # Find and update flashcard
    updated_flashcards = []
    for card in flashcards:
        if card['id'] == flashcard_id:
            # SM-2 algorithm
            ease_factor = card.get('ease_factor', 2.5)
            repetitions = card.get('repetitions', 0)
            interval = card.get('interval', 1)

            if quality >= 3:
                if repetitions == 0:
                    interval = 1
                elif repetitions == 1:
                    interval = 6
                else:
                    interval = int(interval * ease_factor)

                repetitions += 1
            else:
                repetitions = 0
                interval = 1

            ease_factor = max(1.3, ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

            card['ease_factor'] = ease_factor
            card['interval'] = interval
            card['repetitions'] = repetitions
            card['last_reviewed'] = datetime.now().isoformat()

        updated_flashcards.append(card)

    # Save updated flashcards
    flashcards_file = get_user_data_path(user_id) / 'flashcards.jsonl'
    with flashcards_file.open('w') as f:
        for card in updated_flashcards:
            f.write(json.dumps(card) + '\n')

    return jsonify({
        'success': True,
        'next_review_days': interval
    })

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get user progress and statistics"""
    user_id = get_or_create_user_id()
    progress = load_user_progress(user_id)

    # Calculate overall accuracy
    total = progress.get('total_questions', 0)
    correct = progress.get('correct_answers', 0)
    accuracy = (correct / total * 100) if total > 0 else 0

    # Calculate subject breakdown
    subject_stats = []
    for subject, stats in progress.get('by_subject', {}).items():
        subject_accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        subject_stats.append({
            'subject': subject,
            'total': stats['total'],
            'correct': stats['correct'],
            'accuracy': round(subject_accuracy, 1)
        })

    return jsonify({
        'total_questions': total,
        'correct_answers': correct,
        'accuracy': round(accuracy, 1),
        'current_streak': progress.get('streak', 0),
        'last_study': progress.get('last_study'),
        'by_subject': subject_stats
    })

@app.route('/api/study-materials/<subject>', methods=['GET'])
def get_study_materials(subject):
    """Get study materials for a subject"""
    # Map of study materials files
    materials_map = {
        'property': {
            'outline': 'real_property_outline.md',
            'flowchart': 'real_property_flowchart.md',
            'contrast_tables': 'real_property_contrast_tables.md',
            'checklist': 'real_property_checklist.md',
            'drill': 'real_property_drill.md'
        }
    }

    materials = materials_map.get(subject, {})
    result = {}

    for material_type, filename in materials.items():
        filepath = Path(__file__).parent.parent.parent / filename
        if filepath.exists():
            result[material_type] = filepath.read_text()

    return jsonify({
        'subject': subject,
        'materials': result
    })

# ==================== RUN SERVER ====================

if __name__ == '__main__':
    # Create necessary directories
    (DATA_DIR / 'sessions').mkdir(parents=True, exist_ok=True)
    (DATA_DIR / 'users').mkdir(parents=True, exist_ok=True)

    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

"""
Bar Prep Flashcard Web Application
Flask-based web interface for studying with flashcards
"""

from flask import Flask, render_template, request, jsonify, session
import sqlite3
import random
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Database configuration
DB_PATH = 'flashcards.db'

def init_db():
    """Initialize the SQLite database with flashcards table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create flashcards table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            difficulty TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create sessions table for tracking study progress
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            card_id INTEGER NOT NULL,
            user_answer TEXT,
            is_correct BOOLEAN,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_id) REFERENCES flashcards (id)
        )
    ''')

    conn.commit()
    conn.close()

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Render the main flashcard interface"""
    return render_template('index.html')

@app.route('/api/card/random', methods=['GET'])
def get_random_card():
    """Get a random flashcard from the database"""
    conn = get_db_connection()
    subject = request.args.get('subject', None)

    if subject:
        card = conn.execute(
            'SELECT * FROM flashcards WHERE subject = ? ORDER BY RANDOM() LIMIT 1',
            (subject,)
        ).fetchone()
    else:
        card = conn.execute(
            'SELECT * FROM flashcards ORDER BY RANDOM() LIMIT 1'
        ).fetchone()

    conn.close()

    if card:
        return jsonify({
            'id': card['id'],
            'subject': card['subject'],
            'question': card['question'],
            'answer': card['answer'],
            'difficulty': card['difficulty']
        })
    else:
        return jsonify({'error': 'No cards found'}), 404

@app.route('/api/card/check', methods=['POST'])
def check_answer():
    """Check user's answer against the correct answer"""
    data = request.json
    card_id = data.get('card_id')
    user_answer = data.get('user_answer', '').strip()

    conn = get_db_connection()
    card = conn.execute(
        'SELECT * FROM flashcards WHERE id = ?', (card_id,)
    ).fetchone()

    if not card:
        conn.close()
        return jsonify({'error': 'Card not found'}), 404

    correct_answer = card['answer'].strip()

    # Simple answer checking (case-insensitive comparison)
    is_correct = user_answer.lower() == correct_answer.lower()

    # Track in session
    session_id = session.get('session_id')
    if not session_id:
        session_id = os.urandom(16).hex()
        session['session_id'] = session_id

    # Record the attempt
    conn.execute(
        'INSERT INTO study_sessions (session_id, card_id, user_answer, is_correct) VALUES (?, ?, ?, ?)',
        (session_id, card_id, user_answer, is_correct)
    )
    conn.commit()
    conn.close()

    return jsonify({
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'user_answer': user_answer
    })

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Get list of all subjects in the database"""
    conn = get_db_connection()
    subjects = conn.execute(
        'SELECT DISTINCT subject FROM flashcards ORDER BY subject'
    ).fetchall()
    conn.close()

    return jsonify({
        'subjects': [s['subject'] for s in subjects]
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get session statistics"""
    session_id = session.get('session_id')

    if not session_id:
        return jsonify({
            'total': 0,
            'correct': 0,
            'accuracy': 0
        })

    conn = get_db_connection()
    stats = conn.execute(
        '''SELECT
            COUNT(*) as total,
            SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
        FROM study_sessions
        WHERE session_id = ?''',
        (session_id,)
    ).fetchone()
    conn.close()

    total = stats['total'] or 0
    correct = stats['correct'] or 0
    accuracy = (correct / total * 100) if total > 0 else 0

    return jsonify({
        'total': total,
        'correct': correct,
        'accuracy': round(accuracy, 1)
    })

@app.route('/api/card/add', methods=['POST'])
def add_card():
    """Add a new flashcard to the database"""
    data = request.json
    subject = data.get('subject')
    question = data.get('question')
    answer = data.get('answer')
    difficulty = data.get('difficulty', 'medium')

    if not all([subject, question, answer]):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO flashcards (subject, question, answer, difficulty) VALUES (?, ?, ?, ?)',
        (subject, question, answer, difficulty)
    )
    card_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        'id': card_id,
        'message': 'Card added successfully'
    }), 201

if __name__ == '__main__':
    # Initialize database on startup
    init_db()

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

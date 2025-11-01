# MBE Study System - Web Interface

A professional web application for bar exam preparation with practice questions, flashcards, progress tracking, and study materials.

## 🎯 Features

- **📚 Practice Questions** - Interactive MBE practice with instant feedback
- **🗂️ Flashcards** - Spaced repetition learning system (SM-2 algorithm)
- **📊 Progress Tracking** - Detailed analytics and performance metrics
- **📖 Study Materials** - Access to outlines, flowcharts, and study guides
- **🎓 Subject Coverage** - Contracts, Torts, Evidence, Constitutional Law, Criminal Law, Civil Procedure, and more

## 🏗️ Architecture

```
web/
├── backend/          # Flask REST API
│   ├── app.py        # Main Flask application
│   └── requirements.txt
└── frontend/         # React SPA
    ├── src/
    │   ├── pages/    # Main page components
    │   ├── api/      # API client
    │   └── App.jsx   # Root component
    └── package.json
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### 1. Set Up Backend

```bash
# Navigate to backend directory
cd web/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python app.py
```

Backend will run on `http://localhost:5000`

### 2. Set Up Frontend

```bash
# Navigate to frontend directory (in new terminal)
cd web/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on `http://localhost:3000`

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

## 📖 Usage Guide

### Dashboard
- View overall statistics and progress
- Quick access to all features
- Subject-specific performance metrics

### Practice Mode
1. Select a subject (Contracts, Torts, etc.)
2. Choose difficulty level (Easy, Medium, Hard, or Mixed)
3. Set number of questions (1-20)
4. Practice with instant feedback
5. Review correct answers and common traps

### Flashcards
1. Create custom flashcards for any subject
2. Review cards using spaced repetition
3. Rate your recall (Again, Good, Easy)
4. System automatically schedules next review

### Progress Analytics
- Overall accuracy and statistics
- Performance by subject
- Visual charts and graphs
- Identify weak areas
- Track study streaks

### Study Materials
- Access comprehensive outlines
- View decision tree flowcharts
- Compare concepts with contrast tables
- Use checklists for exam prep

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### Frontend Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:5000
```

## 📊 Data Storage

User data is stored in the `data/` directory:

```
data/
├── users/
│   └── [user_id]/
│       ├── progress.json
│       └── flashcards.jsonl
└── sessions/
```

## 🎨 Tech Stack

### Backend
- **Flask** - Lightweight Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-Session** - Server-side session management

### Frontend
- **React 18** - UI library
- **React Router** - Client-side routing
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **Lucide React** - Icon library

## 🚢 Production Deployment

### Backend (Heroku/Railway)

1. Add `Procfile`:
```
web: gunicorn app:app
```

2. Update `requirements.txt`:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

3. Deploy to platform of choice

### Frontend (Vercel/Netlify)

1. Build production assets:
```bash
npm run build
```

2. Deploy `dist/` directory

3. Configure environment variables:
```
VITE_API_URL=https://your-backend-url.com
```

## 📱 API Endpoints

### Health
- `GET /api/health` - Health check

### Subjects & Concepts
- `GET /api/subjects` - Get all subjects
- `GET /api/concepts/:subject` - Get concepts by subject
- `GET /api/concept/:id` - Get concept details

### Practice
- `POST /api/practice/start` - Start practice session
- `POST /api/practice/answer` - Submit answer

### Flashcards
- `GET /api/flashcards` - Get user flashcards
- `POST /api/flashcards/create` - Create flashcard
- `POST /api/flashcards/:id/review` - Review flashcard

### Progress
- `GET /api/progress` - Get user progress stats

### Study Materials
- `GET /api/study-materials/:subject` - Get study materials

## 🧪 Development

### Run Tests

```bash
# Backend tests
cd web/backend
python -m pytest

# Frontend tests
cd web/frontend
npm test
```

### Linting

```bash
# Frontend
cd web/frontend
npm run lint
```

## 🤝 Contributing

This is an educational tool for bar exam preparation. Contributions are welcome!

## 📄 License

Educational use only.

## 🎓 Credits

Built for MBE bar exam preparation, integrating evidence-based learning techniques:
- Spaced repetition (SM-2 algorithm)
- Interleaved practice
- Active recall
- Progress tracking

---

**Start studying smarter, not harder! 📚✨**

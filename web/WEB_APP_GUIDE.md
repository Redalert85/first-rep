# MBE Study System - Web Application Guide

## 🎉 What You Have Now

A **complete, professional web application** for MBE bar exam preparation with:

### ✨ Core Features

1. **Interactive Practice Questions**
   - Select subjects and difficulty levels
   - Instant feedback on answers
   - Track correct/incorrect responses
   - Learn from common traps and mistakes

2. **Smart Flashcard System**
   - Create custom flashcards for any subject
   - Spaced repetition using SM-2 algorithm
   - Automatic review scheduling
   - Visual progress indicators

3. **Comprehensive Analytics**
   - Overall accuracy tracking
   - Subject-by-subject performance
   - Visual charts and graphs (Chart.js)
   - Streak tracking for consistency
   - Performance insights and recommendations

4. **Study Materials Library**
   - Real Property outlines
   - Decision tree flowcharts
   - Contrast tables for comparison
   - Checklists and drills
   - Markdown-rendered content

5. **User Progress Tracking**
   - Persistent session storage
   - Individual user profiles
   - Historical performance data
   - Personalized recommendations

## 🏗️ Technical Architecture

### Backend (Flask REST API)
```
web/backend/
├── app.py              # Main Flask application
│   ├── 15 API endpoints
│   ├── Session management
│   ├── User data persistence
│   └── Integration with existing tutor
└── requirements.txt
```

**Key Features:**
- RESTful API design
- CORS enabled for frontend
- File-based session storage
- User-specific data directories
- SM-2 spaced repetition algorithm
- Integration with existing `bar_tutor_unified.py`

### Frontend (React SPA)
```
web/frontend/
├── src/
│   ├── App.jsx                 # Root component with routing
│   ├── pages/
│   │   ├── Dashboard.jsx       # Main dashboard with stats
│   │   ├── Practice.jsx        # Interactive practice mode
│   │   ├── Flashcards.jsx      # Flashcard study system
│   │   ├── Progress.jsx        # Analytics & charts
│   │   └── StudyMaterials.jsx  # Study materials viewer
│   ├── api/
│   │   └── client.js           # Axios API client
│   └── index.css               # Tailwind styles
├── package.json
├── vite.config.js
└── tailwind.config.js
```

**Key Features:**
- Modern React 18 with Hooks
- React Router for navigation
- Tailwind CSS for styling
- Chart.js for visualizations
- Responsive design (mobile-friendly)
- Component-based architecture

## 📱 User Interface

### 🏠 Dashboard
- Quick stats overview (questions, accuracy, streak)
- Subject cards with progress bars
- Quick action buttons
- Recent activity

### 🧠 Practice Mode
- Subject & difficulty selection
- Interactive question interface
- Real-time feedback
- Common traps display
- Session results summary

### 🗂️ Flashcards
- Browse all flashcards
- Filter by subject
- Study mode with flip animation
- Rate recall (Again/Good/Easy)
- Create custom flashcards
- Due date tracking

### 📊 Progress & Analytics
- Performance statistics
- Bar charts by subject
- Doughnut chart (correct vs incorrect)
- Detailed subject breakdown table
- Performance insights
- Last study session info

### 📖 Study Materials
- Subject selection
- Material type navigation
- Markdown rendering
- Professional typography
- Easy navigation

## 🎨 Design System

### Colors
- **Primary Blue**: `#0ea5e9` - Main brand color
- **Success Green**: `#22c55e` - Positive feedback
- **Warning Yellow**: `#eab308` - Attention items
- **Danger Red**: `#ef4444` - Errors/incorrect

### Components
- **Cards**: White background, subtle shadow, rounded corners
- **Buttons**: Primary, secondary, with hover states
- **Inputs**: Clean, focused states with primary color
- **Charts**: Colorful, accessible data visualization

## 🚀 Getting Started

### Option 1: Quick Start (Recommended)

```bash
cd web
./start.sh
```

This single script will:
1. ✅ Check prerequisites (Python, Node.js)
2. ✅ Set up Python virtual environment
3. ✅ Install backend dependencies
4. ✅ Start Flask server (port 5000)
5. ✅ Install frontend dependencies
6. ✅ Start Vite dev server (port 3000)
7. ✅ Open your browser automatically

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd web/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd web/frontend
npm install
npm run dev
```

**Access:** http://localhost:3000

## 📊 Data Flow

```
User Browser
    ↓
React Frontend (localhost:3000)
    ↓ API Calls (Axios)
Flask Backend (localhost:5000)
    ↓ Integrates with
Existing Python Modules
    ├── bar_tutor_unified.py
    ├── advanced_pedagogy.py
    └── Knowledge Graph
    ↓ Persists to
File System
    └── data/
        ├── users/[user_id]/
        │   ├── progress.json
        │   └── flashcards.jsonl
        └── sessions/
```

## 🔌 API Endpoints

### Core Endpoints
```
GET  /api/health                    - Health check
GET  /api/subjects                  - Get all subjects
GET  /api/concepts/:subject         - Get concepts by subject
GET  /api/concept/:id               - Get concept details
POST /api/practice/start            - Start practice session
POST /api/practice/answer           - Submit answer
GET  /api/flashcards                - Get user flashcards
POST /api/flashcards/create         - Create flashcard
POST /api/flashcards/:id/review     - Review flashcard (SM-2)
GET  /api/progress                  - Get user progress
GET  /api/study-materials/:subject  - Get study materials
```

## 🎯 Integration with Existing System

The web app seamlessly integrates with your existing codebase:

1. **Knowledge Graph** → Powers subject & concept data
2. **Learning State** → Tracks user sessions
3. **Flashcard System** → SM-2 spaced repetition
4. **Advanced Pedagogy** → Evidence-based learning
5. **Study Materials** → Real property outlines, etc.

## 📈 Future Enhancements

Easy to add:
- [ ] User authentication (login/signup)
- [ ] Study plan recommendations
- [ ] Social features (study groups)
- [ ] Mobile app (React Native)
- [ ] Offline mode (PWA)
- [ ] Export progress to PDF
- [ ] Email reminders for reviews
- [ ] AI-generated questions
- [ ] Leaderboards
- [ ] Study timer (Pomodoro)

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Reinstall dependencies
cd web/backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 16+

# Clear cache and reinstall
cd web/frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Port already in use
```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### CORS errors
Make sure:
1. Backend is running on port 5000
2. Frontend proxy is configured in `vite.config.js`
3. `withCredentials: true` in API client

## 🎓 Learning Features

### Spaced Repetition (SM-2 Algorithm)
- Automatically calculates optimal review intervals
- Adjusts based on recall quality (1-5 scale)
- Ease factor modification
- Long-term retention optimization

### Performance Analytics
- Accuracy tracking by subject
- Weak area identification
- Progress visualization
- Study streak encouragement

### Interleaved Practice
- Mixes concepts for better retention
- Prevents compartmentalization
- Research-backed effectiveness

## 🌟 Best Practices

### For Students
1. Study daily (build a streak!)
2. Review flashcards when due
3. Focus on weak subjects (< 70% accuracy)
4. Use study materials for difficult concepts
5. Track progress weekly

### For Developers
1. Keep components small and focused
2. Use TypeScript for type safety (future)
3. Test API endpoints thoroughly
4. Follow React best practices
5. Keep state management simple

## 📞 Support

Issues? Questions?
1. Check this guide first
2. Review `README.md`
3. Check console for errors (F12 in browser)
4. Verify both servers are running

---

## 🎉 You're Ready!

You now have a **production-quality web application** for MBE bar exam preparation!

**Next Steps:**
1. Run `./start.sh` to launch the app
2. Create your first flashcards
3. Start a practice session
4. Track your progress
5. Ace the bar exam! 🎓✨

---

Built with ❤️ for bar exam success

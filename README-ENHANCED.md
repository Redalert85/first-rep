# First-Rep: Enhanced Bar Exam Study Platform

## 🎯 Overview

First-Rep is a comprehensive, AI-powered bar exam preparation platform featuring:
- **Adaptive Spaced Repetition**: SM-2 algorithm for optimized review scheduling
- **AI-Generated Fact Patterns**: Unlimited practice hypotheticals with IRAC analysis
- **Socratic Tutor**: Context-aware AI assistant for deeper understanding
- **Performance Analytics**: Granular tracking of progress and weak areas
- **Study Planning**: AI-generated personalized study schedules

---

## 🚀 New Features

### 1. Enhanced Flashcard System
- **12+ Cards** across all MBE subjects (Evidence, Torts, Contracts, Criminal Law, Civil Procedure, Con Law, Real Property)
- **Difficulty Levels**: Easy, Medium, Hard ratings for each card
- **Subject Filtering**: Focus on specific subjects or study all topics
- **Bookmark System**: Save important cards for quick review
- **Progress Tracking**: Real-time accuracy and mastery metrics

### 2. Advanced Hypothetical Engine
- **Difficulty Selection**: Easy, Medium, Hard, Bar Exam Level
- **Multi-Subject Coverage**: All 7 MBE subjects
- **User Answer Input**: Write your own analysis before revealing model answer
- **AI Evaluation**: Get instant feedback comparing your answer to model
- **History & Bookmarks**: Save practice sessions for review
- **Detailed IRAC Analysis**: Comprehensive issue spotting with case citations

### 3. Intelligent Study Planner
- **Custom Timeline**: Configure study period (1-52 weeks)
- **Daily Hour Allocation**: Optimize for your available study time
- **Priority Subjects**: Front-load weak areas
- **Learning Modalities**: Textual, Visual, Auditory, Practice-Based, Hybrid
- **MBE Focus Mode**: Option for MBE-only preparation
- **Plan History**: Save and revisit up to 5 generated plans
- **Export Functionality**: Download plans as HTML

### 4. Comprehensive Analytics Dashboard
- **Overall Performance**: Accuracy, streak, cards studied, study time
- **Subject Breakdown**: Performance metrics by topic with visual progress bars
- **Activity Heatmap**: 21-day visualization of study patterns
- **Strength/Weakness Analysis**: Automatic identification of strong/weak subjects
- **Trend Tracking**: Monitor improvement over time

### 5. Enhanced UX Features
- **Local Storage Persistence**: All progress saved in browser
- **Mobile Responsive**: Fully functional on all device sizes
- **Dark Mode Cards**: Issue spotter section with dark theme
- **Keyboard Shortcuts**: Enter to send chat messages
- **Settings Panel**: Deck controls and session management
- **Streak Tracking**: Gamified daily study motivation

---

## 🛠️ Technical Architecture

### State Management
```javascript
// Local Storage Keys
- first_rep_user_stats: Global user statistics
- first_rep_card_history: Individual card performance
- first_rep_study_sessions: Session metadata
- first_rep_bookmarks: Bookmarked card IDs
- saved_plans: Generated study plans
- hypo_history: Saved hypotheticals
```

### Custom Hooks
- `useLocalStorage(key, initialValue)`: Persistent state management with automatic localStorage sync

### Spaced Repetition Logic
Based on SM-2 algorithm:
- **Again (1)**: Review in <1 day
- **Hard (2)**: Review in 1-3 days
- **Good (3)**: Review in 4-7 days
- **Easy (5)**: Review in 14+ days

---

## 📊 Data Flow

```
User Interaction
      ↓
Component State Update
      ↓
Local Storage Sync (useLocalStorage hook)
      ↓
Analytics Calculation (useMemo)
      ↓
UI Re-render with Updated Stats
```

---

## 🎨 Design System

### Color Palette
- **Primary**: Amber (700-600) - CTA buttons, highlights
- **Neutral**: Stone (50-900) - Background, text, borders
- **Success**: Emerald (500-700) - Correct answers, mastery
- **Warning**: Orange/Red (500-700) - Errors, focus areas
- **Accent**: Blue, Purple (for various stats)

### Typography
- **Headings**: Font Serif (classic legal aesthetic)
- **Body**: Sans-serif (readability)
- **Mono**: Stats and code-like elements

### Components Structure
```
App (Main Container)
├── Navigation (Fixed header with stats)
├── Hero Section (Landing with stats preview)
├── Features Overview (6 feature cards)
├── EnhancedAIPlanner
│   ├── Configuration Panel
│   └── Output Display with Save/Export
├── EnhancedHypotheticalEngine
│   ├── Controls (Subject, Difficulty)
│   ├── Fact Pattern Display
│   ├── User Answer Input
│   ├── AI Evaluation
│   └── History Browser
├── EnhancedMiniTutor
│   ├── Stats Sidebar
│   ├── Flashcard with Flip Animation
│   ├── Socratic Chat Interface
│   └── Rating System
├── AnalyticsDashboard
│   ├── Overview Metrics
│   ├── Subject Performance Chart
│   ├── Activity Heatmap
│   └── Strengths/Weaknesses
└── Footer
```

---

## 🔧 Configuration

### Gemini API Setup
```javascript
const apiKey = "YOUR_API_KEY_HERE";
```
Set your Gemini API key for AI features to function.

### Customization Options

#### Add More Flashcards
```javascript
const allCards = [
  {
    id: 13,
    subject: "Your Subject",
    topic: "Specific Topic",
    question: "Question prompt",
    answer: "Black letter law rule",
    subtext: "Memory aid or case citation",
    difficulty: "Easy" // Easy, Medium, or Hard
  }
];
```

#### Adjust Spaced Repetition Intervals
```javascript
// In handleRate function
const intervals = {
  1: "<1 day",    // Again
  2: "1-3 days",  // Hard
  3: "4-7 days",  // Good
  5: "14+ days"   // Easy
};
```

---

## 📱 Responsive Breakpoints

- **Mobile**: < 768px (md breakpoint)
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px (lg breakpoint)

Mobile-specific features:
- Collapsible navigation menu
- Stacked layouts for cards
- Touch-optimized card flipping
- Simplified analytics views

---

## 🎓 Study Methodology

### Spaced Repetition Best Practices
1. **Be Honest**: Rate difficulty accurately
2. **Daily Consistency**: Study every day to maintain streak
3. **Focus on Weaknesses**: Use subject filter for areas <60%
4. **Use Socratic Chat**: Don't just memorize, understand
5. **Regular Review**: Check analytics weekly

### Effective Hypothetical Practice
1. **Start Medium Difficulty**: Build confidence before advancing
2. **Write Full Answers**: Use the text input before revealing model
3. **Request AI Feedback**: Compare your analysis to model
4. **Bookmark Challenging Ones**: Review difficult patterns
5. **Vary Subjects**: Rotate through all 7 topics

### Study Plan Optimization
1. **Front-load Weaknesses**: Prioritize lowest-performing subjects
2. **Match Learning Style**: Select appropriate modality
3. **Realistic Hours**: Don't overcommit on daily hours
4. **Include Buffer Time**: Account for life events
5. **Checkpoint Assessments**: Follow suggested review periods

---

## 📈 Analytics Interpretation

### Accuracy Metrics
- **80%+**: Excellent mastery, reduce review frequency
- **60-79%**: Solid understanding, maintain current pace
- **40-59%**: Needs improvement, increase study time
- **<40%**: Critical weakness, prioritize immediately

### Streak Tracking
- Tracks consecutive days with at least one card studied
- Resets to 0 if a day is missed
- Motivational tool for consistency

### Subject Performance
- Green bar (80%+): Strong subject
- Amber bar (60-79%): Adequate
- Red bar (<60%): Focus area

---

## 🔐 Data Privacy

All data is stored **locally in your browser** using localStorage:
- No server uploads
- No account required
- Full data control
- Export functionality for backup

### Data Persistence
Data persists unless:
- Browser cache is cleared
- localStorage is manually deleted
- Using incognito/private mode (session-only)

---

## 🐛 Troubleshooting

### AI Features Not Working
- Verify Gemini API key is set
- Check browser console for errors
- Ensure internet connection is stable
- API may have rate limits

### Lost Progress
- Export study plans regularly
- Bookmark important cards
- Use standard browsing mode (not incognito)
- Consider manual backup of localStorage

### Performance Issues
- Clear card history if >1000 entries
- Reduce saved plans to <5
- Limit hypothetical history to <20

---

## 🚀 Future Enhancements

Potential additions:
- [ ] Full SM-2 implementation with easiness factor
- [ ] Essay writing practice with AI grading
- [ ] MPT (Multistate Performance Test) simulator
- [ ] Collaborative study groups
- [ ] Progress export to PDF
- [ ] Mobile app version
- [ ] Advanced analytics (forgetting curve, retention rate)
- [ ] Custom card creation
- [ ] Audio flashcard mode
- [ ] Pomodoro timer integration
- [ ] Bar exam countdown widget

---

## 📄 License

Copyright © 2025 First-Rep. Not affiliated with the NCBE.

---

## 💡 Tips for Maximum Effectiveness

1. **Daily Habit**: Study at the same time each day
2. **Quality Over Quantity**: 30 focused minutes > 2 distracted hours
3. **Active Recall**: Don't peek at answers too quickly
4. **Teach Others**: Use Socratic chat to explain concepts
5. **Track Trends**: Weekly analytics review
6. **Celebrate Progress**: Acknowledge improvements
7. **Adjust Plans**: Update study schedule as needed
8. **Mix Modalities**: Combine flashcards, hypotheticals, and reading

---

## 🎯 Success Metrics

Target benchmarks for bar exam readiness:
- Overall accuracy: **75%+**
- All subjects: **>60%**
- Study streak: **21+ days**
- Cards mastered: **200+**
- Hypotheticals completed: **50+ per subject**
- Average session: **45+ minutes**

---

Built with precision for legal scholars. Good luck on your bar exam! ⚖️

/**
 * Application Constants and Configuration
 * Central location for all app-wide settings and constants
 */

// ===== STORAGE KEYS =====
export const STORAGE_KEYS = {
  USER_STATS: 'first_rep_user_stats',
  CARD_HISTORY: 'first_rep_card_history',
  STUDY_SESSIONS: 'first_rep_study_sessions',
  BOOKMARKS: 'first_rep_bookmarks',
  PREFERENCES: 'first_rep_preferences',
  ACHIEVEMENTS: 'first_rep_achievements',
  SAVED_PLANS: 'saved_plans',
  HYPO_HISTORY: 'hypo_history',
  LAST_VISIT: 'last_visit_date'
};

// ===== SPACED REPETITION CONSTANTS =====
export const SR_CONSTANTS = {
  DEFAULT_EASINESS_FACTOR: 2.5,
  MIN_EASINESS_FACTOR: 1.3,
  MAX_EASINESS_FACTOR: 2.5,
  INTERVAL_MODIFIERS: {
    AGAIN: 1,      // <1 day
    HARD: 1.2,     // 1-3 days
    GOOD: 2.5,     // 4-7 days
    EASY: 3.0      // 14+ days
  },
  QUALITY_RATINGS: {
    AGAIN: 1,
    HARD: 2,
    GOOD: 3,
    EASY: 5
  },
  MATURE_INTERVAL_THRESHOLD: 21, // Cards with 21+ day intervals are "mature"
  YOUNG_INTERVAL_THRESHOLD: 7    // Cards with <7 day intervals are "young"
};

// ===== PERFORMANCE THRESHOLDS =====
export const PERFORMANCE_THRESHOLDS = {
  EXCELLENT: 85,
  GOOD: 70,
  FAIR: 60,
  POOR: 50,
  CRITICAL: 40
};

// ===== SUBJECT CONFIGURATION =====
export const SUBJECTS = {
  EVIDENCE: {
    name: 'Evidence',
    code: 'EV',
    color: 'blue',
    icon: 'scale',
    mbeWeight: 25,
    topics: ['Hearsay', 'Character Evidence', 'Authentication', 'Privileges', 'Relevance', 'Impeachment']
  },
  CRIMINAL_PROCEDURE: {
    name: 'Criminal Procedure',
    code: 'CP',
    color: 'red',
    icon: 'shield',
    mbeWeight: 25,
    topics: ['4th Amendment', 'Miranda', '6th Amendment', 'Exclusionary Rule', 'Identification', 'Double Jeopardy']
  },
  CRIMINAL_LAW: {
    name: 'Criminal Law',
    code: 'CR',
    color: 'purple',
    icon: 'alert',
    mbeWeight: 25,
    topics: ['Homicide', 'Inchoate Crimes', 'Theft', 'Defenses', 'Accomplice Liability', 'Mens Rea']
  },
  CONTRACTS: {
    name: 'Contracts',
    code: 'K',
    color: 'green',
    icon: 'file-text',
    mbeWeight: 25,
    topics: ['Formation', 'Consideration', 'Statute of Frauds', 'Remedies', 'Third Party', 'Performance']
  },
  TORTS: {
    name: 'Torts',
    code: 'T',
    color: 'orange',
    icon: 'alert-circle',
    mbeWeight: 25,
    topics: ['Negligence', 'Intentional Torts', 'Strict Liability', 'Products Liability', 'Defamation', 'Nuisance']
  },
  REAL_PROPERTY: {
    name: 'Real Property',
    code: 'RP',
    color: 'amber',
    icon: 'home',
    mbeWeight: 25,
    topics: ['Present Estates', 'Future Interests', 'Covenants', 'Easements', 'Adverse Possession', 'Recording Acts']
  },
  CONSTITUTIONAL_LAW: {
    name: 'Constitutional Law',
    code: 'CON',
    color: 'indigo',
    icon: 'book',
    mbeWeight: 25,
    topics: ['Equal Protection', 'Due Process', 'First Amendment', 'Commerce Clause', 'Takings', 'Standing']
  },
  CIVIL_PROCEDURE: {
    name: 'Civil Procedure',
    code: 'CIV',
    color: 'teal',
    icon: 'briefcase',
    mbeWeight: 25,
    topics: ['Jurisdiction', 'Erie', 'Pleadings', 'Discovery', 'Summary Judgment', 'Class Actions']
  }
};

// ===== DIFFICULTY LEVELS =====
export const DIFFICULTY_LEVELS = {
  EASY: {
    label: 'Easy',
    color: 'green',
    multiplier: 1.0,
    description: 'Single-issue, straightforward facts'
  },
  MEDIUM: {
    label: 'Medium',
    color: 'blue',
    multiplier: 1.2,
    description: '2-3 interrelated issues with moderate complexity'
  },
  HARD: {
    label: 'Hard',
    color: 'orange',
    multiplier: 1.5,
    description: 'Multiple overlapping issues with nuanced fact patterns'
  },
  BAR_EXAM: {
    label: 'Bar Exam Level',
    color: 'red',
    multiplier: 2.0,
    description: 'Maximum complexity with subtle distinctions'
  }
};

// ===== STUDY PLAN DEFAULTS =====
export const STUDY_PLAN_DEFAULTS = {
  MIN_WEEKS: 1,
  MAX_WEEKS: 52,
  DEFAULT_WEEKS: 10,
  MIN_HOURS_PER_DAY: 1,
  MAX_HOURS_PER_DAY: 16,
  DEFAULT_HOURS_PER_DAY: 6,
  LEARNING_MODALITIES: [
    'Textual (Outlines)',
    'Visual (Flowcharts)',
    'Auditory (Lectures)',
    'Practice-Based (MCQ heavy)',
    'Hybrid (Mixed methods)'
  ]
};

// ===== SESSION DEFAULTS =====
export const SESSION_DEFAULTS = {
  TARGET_CARDS_PER_SESSION: 20,
  MIN_SESSION_DURATION: 15, // minutes
  OPTIMAL_SESSION_DURATION: 45, // minutes
  MAX_SESSION_DURATION: 120, // minutes
  BREAK_INTERVAL: 25, // Pomodoro-style
  BREAK_DURATION: 5 // minutes
};

// ===== ANALYTICS CONSTANTS =====
export const ANALYTICS = {
  RETENTION_TARGETS: {
    EXCELLENT: 90,
    GOOD: 80,
    ACCEPTABLE: 70,
    NEEDS_IMPROVEMENT: 60
  },
  STREAK_MILESTONES: [7, 14, 21, 30, 60, 90, 180, 365],
  MASTERY_THRESHOLDS: {
    BEGINNER: 0,
    INTERMEDIATE: 50,
    ADVANCED: 100,
    EXPERT: 200,
    MASTER: 500
  },
  CHART_COLORS: {
    primary: '#d97706',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#3b82f6',
    neutral: '#6b7280'
  }
};

// ===== ACHIEVEMENT DEFINITIONS =====
export const ACHIEVEMENTS = {
  FIRST_CARD: {
    id: 'first_card',
    title: 'First Step',
    description: 'Complete your first flashcard',
    icon: 'star',
    threshold: 1
  },
  TEN_STREAK: {
    id: 'ten_streak',
    title: 'Dedicated Scholar',
    description: 'Maintain a 10-day study streak',
    icon: 'flame',
    threshold: 10
  },
  HUNDRED_CARDS: {
    id: 'hundred_cards',
    title: 'Century Club',
    description: 'Study 100 flashcards',
    icon: 'award',
    threshold: 100
  },
  PERFECT_SESSION: {
    id: 'perfect_session',
    title: 'Perfectionist',
    description: 'Complete a session with 100% accuracy',
    icon: 'check-circle',
    threshold: 1
  },
  SUBJECT_MASTER: {
    id: 'subject_master',
    title: 'Subject Matter Expert',
    description: 'Achieve 90%+ accuracy in a subject',
    icon: 'brain',
    threshold: 90
  },
  EARLY_BIRD: {
    id: 'early_bird',
    title: 'Early Bird',
    description: 'Study before 7 AM',
    icon: 'sunrise',
    threshold: 1
  },
  NIGHT_OWL: {
    id: 'night_owl',
    title: 'Night Owl',
    description: 'Study after 10 PM',
    icon: 'moon',
    threshold: 1
  },
  WEEK_WARRIOR: {
    id: 'week_warrior',
    title: 'Week Warrior',
    description: 'Study every day for a week',
    icon: 'calendar',
    threshold: 7
  }
};

// ===== API CONFIGURATION =====
export const API_CONFIG = {
  GEMINI: {
    BASE_URL: 'https://generativelanguage.googleapis.com/v1beta/models',
    MODEL: 'gemini-2.5-flash-preview-09-2025',
    TIMEOUT: 30000, // 30 seconds
    MAX_RETRIES: 3,
    RETRY_DELAYS: [1000, 2000, 4000], // exponential backoff
    MAX_TOKENS: 2048,
    TEMPERATURE: 0.7,
    TOP_P: 0.95
  }
};

// ===== UI CONSTANTS =====
export const UI = {
  ANIMATION_DURATION: {
    FAST: 150,
    NORMAL: 300,
    SLOW: 500
  },
  BREAKPOINTS: {
    SM: 640,
    MD: 768,
    LG: 1024,
    XL: 1280,
    '2XL': 1536
  },
  Z_INDEX: {
    DROPDOWN: 40,
    STICKY: 50,
    MODAL_OVERLAY: 60,
    MODAL: 70,
    TOOLTIP: 80,
    NOTIFICATION: 90
  },
  TOAST_DURATION: 3000, // 3 seconds
  DEBOUNCE_DELAY: 300, // milliseconds
  THROTTLE_DELAY: 200 // milliseconds
};

// ===== ERROR MESSAGES =====
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network connection failed. Please check your internet and try again.',
  API_ERROR: 'Unable to reach the AI service. Please try again later.',
  STORAGE_ERROR: 'Unable to save your progress. Please check browser storage settings.',
  INVALID_INPUT: 'Please check your input and try again.',
  SESSION_EXPIRED: 'Your session has expired. Please refresh the page.',
  UNKNOWN_ERROR: 'An unexpected error occurred. Please try again.'
};

// ===== SUCCESS MESSAGES =====
export const SUCCESS_MESSAGES = {
  CARD_COMPLETED: 'Great work! Card completed.',
  PLAN_SAVED: 'Study plan saved successfully.',
  BOOKMARK_ADDED: 'Card bookmarked for review.',
  STREAK_MAINTAINED: 'Streak maintained! Keep it up!',
  SESSION_COMPLETE: 'Session completed. Excellent work!'
};

// ===== EXPORT FORMATS =====
export const EXPORT_FORMATS = {
  JSON: 'json',
  CSV: 'csv',
  HTML: 'html',
  PDF: 'pdf',
  MARKDOWN: 'md'
};

// ===== FEATURE FLAGS =====
export const FEATURES = {
  ENABLE_ANALYTICS: true,
  ENABLE_ACHIEVEMENTS: true,
  ENABLE_SOCIAL_SHARING: false,
  ENABLE_AUDIO_MODE: false,
  ENABLE_DARK_MODE: false,
  ENABLE_OFFLINE_MODE: false,
  ENABLE_AI_TUTOR: true,
  ENABLE_EXPORT: true,
  ENABLE_CUSTOM_CARDS: false // Future feature
};

// ===== VALIDATION RULES =====
export const VALIDATION = {
  MIN_CARD_TITLE_LENGTH: 3,
  MAX_CARD_TITLE_LENGTH: 200,
  MIN_CARD_ANSWER_LENGTH: 10,
  MAX_CARD_ANSWER_LENGTH: 2000,
  MIN_PLAN_WEEKS: 1,
  MAX_PLAN_WEEKS: 52,
  MIN_HOURS_PER_DAY: 0.5,
  MAX_HOURS_PER_DAY: 16,
  MAX_SAVED_PLANS: 10,
  MAX_BOOKMARKS: 200,
  MAX_HISTORY_ITEMS: 1000
};

// ===== RATING LABELS =====
export const RATING_LABELS = {
  1: {
    label: 'Again',
    description: 'Complete blackout - review immediately',
    interval: '<1 day',
    color: 'red'
  },
  2: {
    label: 'Hard',
    description: 'Difficult recall - needs more practice',
    interval: '1-3 days',
    color: 'orange'
  },
  3: {
    label: 'Good',
    description: 'Correct with some effort',
    interval: '4-7 days',
    color: 'blue'
  },
  4: {
    label: 'Easy',
    description: 'Perfect recall - confident',
    interval: '14+ days',
    color: 'green'
  },
  5: {
    label: 'Perfect',
    description: 'Instant recall - mastered',
    interval: '30+ days',
    color: 'emerald'
  }
};

// ===== KEYBOARD SHORTCUTS =====
export const KEYBOARD_SHORTCUTS = {
  FLIP_CARD: ' ', // Spacebar
  RATE_AGAIN: '1',
  RATE_HARD: '2',
  RATE_GOOD: '3',
  RATE_EASY: '4',
  NEXT_CARD: 'ArrowRight',
  PREV_CARD: 'ArrowLeft',
  BOOKMARK: 'b',
  OPEN_CHAT: 't', // tutor
  ESC_CLOSE: 'Escape',
  SEARCH: '/',
  HELP: '?'
};

// ===== DEFAULT USER STATS =====
export const DEFAULT_USER_STATS = {
  totalCards: 0,
  masteredCards: 0,
  currentStreak: 0,
  longestStreak: 0,
  totalStudyTime: 0,
  lastStudyDate: null,
  totalSessions: 0,
  averageAccuracy: 0,
  achievementsUnlocked: []
};

// ===== NOTIFICATION TYPES =====
export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info'
};

// ===== BAR EXAM DATES (2025) =====
export const BAR_EXAM_DATES = {
  FEBRUARY_2025: '2025-02-25',
  JULY_2025: '2025-07-29',
  FEBRUARY_2026: '2026-02-24',
  JULY_2026: '2026-07-28'
};

// ===== TIPS & ADVICE =====
export const STUDY_TIPS = [
  "Study at the same time each day to build a habit.",
  "Use active recall: Try to remember before flipping the card.",
  "Take breaks every 25-30 minutes (Pomodoro technique).",
  "Focus on understanding, not just memorization.",
  "Review weak subjects first when your mind is fresh.",
  "Don't skip difficult cards - they need the most attention.",
  "Explain concepts out loud to test your understanding.",
  "Connect new rules to real-world examples or cases.",
  "Practice issue spotting in everyday situations.",
  "Maintain your streak - consistency beats cramming."
];

// ===== EXPORT DEFAULT =====
export default {
  STORAGE_KEYS,
  SR_CONSTANTS,
  PERFORMANCE_THRESHOLDS,
  SUBJECTS,
  DIFFICULTY_LEVELS,
  STUDY_PLAN_DEFAULTS,
  SESSION_DEFAULTS,
  ANALYTICS,
  ACHIEVEMENTS,
  API_CONFIG,
  UI,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
  EXPORT_FORMATS,
  FEATURES,
  VALIDATION,
  RATING_LABELS,
  KEYBOARD_SHORTCUTS,
  DEFAULT_USER_STATS,
  NOTIFICATION_TYPES,
  BAR_EXAM_DATES,
  STUDY_TIPS
};

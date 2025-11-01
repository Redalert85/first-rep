import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for session cookies
})

// API methods
export const api = {
  // Health check
  healthCheck: () => apiClient.get('/api/health'),

  // Subjects
  getSubjects: () => apiClient.get('/api/subjects'),
  getConcepts: (subject) => apiClient.get(`/api/concepts/${subject}`),
  getConceptDetails: (conceptId) => apiClient.get(`/api/concept/${conceptId}`),

  // Practice
  startPracticeSession: (data) => apiClient.post('/api/practice/start', data),
  submitAnswer: (data) => apiClient.post('/api/practice/answer', data),

  // Flashcards
  getFlashcards: (subject = null) =>
    apiClient.get('/api/flashcards', { params: subject ? { subject } : {} }),
  createFlashcard: (data) => apiClient.post('/api/flashcards/create', data),
  reviewFlashcard: (flashcardId, quality) =>
    apiClient.post(`/api/flashcards/${flashcardId}/review`, { quality }),

  // Progress
  getProgress: () => apiClient.get('/api/progress'),

  // Study Materials
  getStudyMaterials: (subject) => apiClient.get(`/api/study-materials/${subject}`),
}

export default apiClient

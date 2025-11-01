import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Brain, CheckCircle, XCircle, ArrowRight } from 'lucide-react'
import { api } from '../api/client'

export default function Practice() {
  const [searchParams] = useSearchParams()
  const [subjects, setSubjects] = useState([])
  const [selectedSubject, setSelectedSubject] = useState(searchParams.get('subject') || 'contracts')
  const [difficulty, setDifficulty] = useState('mixed')
  const [numQuestions, setNumQuestions] = useState(5)
  const [session, setSession] = useState(null)
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [selectedAnswer, setSelectedAnswer] = useState('')
  const [showFeedback, setShowFeedback] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [sessionResults, setSessionResults] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadSubjects()
  }, [])

  const loadSubjects = async () => {
    try {
      const res = await api.getSubjects()
      setSubjects(res.data.subjects)
    } catch (error) {
      console.error('Failed to load subjects:', error)
    }
  }

  const startSession = async () => {
    setLoading(true)
    try {
      const res = await api.startPracticeSession({
        subject: selectedSubject,
        num_questions: numQuestions,
        difficulty
      })
      setSession(res.data)
      setCurrentQuestion(res.data.current_question)
      setSessionResults(null)
      setShowFeedback(false)
      setSelectedAnswer('')
    } catch (error) {
      console.error('Failed to start session:', error)
      alert('Failed to start practice session')
    } finally {
      setLoading(false)
    }
  }

  const submitAnswer = async () => {
    if (!selectedAnswer) return

    // For demo purposes, we'll use a simple check
    // In production, this would be determined by the backend based on actual question data
    const correct = Math.random() > 0.4 // 60% correct for demo

    setIsCorrect(correct)
    setShowFeedback(true)

    try {
      const res = await api.submitAnswer({
        concept_id: currentQuestion.id,
        answer: selectedAnswer,
        is_correct: correct,
        time_spent: 30
      })

      if (res.data.session_complete) {
        setSessionResults(res.data)
        setSession(null)
        setCurrentQuestion(null)
      } else {
        // Wait a moment before showing next question
        setTimeout(() => {
          setCurrentQuestion(res.data.current_question)
          setSelectedAnswer('')
          setShowFeedback(false)
        }, 2000)
      }
    } catch (error) {
      console.error('Failed to submit answer:', error)
    }
  }

  if (sessionResults) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="card text-center">
          <div className="mb-6">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-4">
              <CheckCircle className="w-10 h-10 text-green-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Session Complete!</h2>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Questions</p>
              <p className="text-3xl font-bold text-gray-900">{sessionResults.total_questions}</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Correct</p>
              <p className="text-3xl font-bold text-green-600">{sessionResults.correct_answers}</p>
            </div>
            <div className="col-span-2 p-4 bg-primary-50 rounded-lg">
              <p className="text-sm text-primary-700">Accuracy</p>
              <p className="text-4xl font-bold text-primary-600">{sessionResults.accuracy.toFixed(1)}%</p>
            </div>
          </div>

          <button
            onClick={() => setSelectedSubject(selectedSubject)}
            className="btn btn-primary w-full"
          >
            Start Another Session
          </button>
        </div>
      </div>
    )
  }

  if (currentQuestion) {
    return (
      <div className="max-w-3xl mx-auto">
        <div className="card">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">Practice Session</h2>
            <span className="text-sm text-gray-600">
              Question {session.current_index || 1} of {session.total_questions}
            </span>
          </div>

          <div className="mb-6">
            <div className="flex items-center space-x-2 mb-4">
              <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium">
                {currentQuestion.name}
              </span>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                currentQuestion.difficulty <= 2 ? 'bg-green-100 text-green-700' :
                currentQuestion.difficulty <= 3 ? 'bg-yellow-100 text-yellow-700' :
                'bg-red-100 text-red-700'
              }`}>
                Difficulty: {currentQuestion.difficulty}/5
              </span>
            </div>

            <div className="prose max-w-none">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Rule Statement</h3>
              <p className="text-gray-700 mb-4">{currentQuestion.rule_statement}</p>

              {currentQuestion.elements && currentQuestion.elements.length > 0 && (
                <>
                  <h4 className="font-semibold text-gray-900 mb-2">Elements:</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    {currentQuestion.elements.map((element, idx) => (
                      <li key={idx} className="text-gray-700">{element}</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          </div>

          <div className="mb-6">
            <h4 className="font-semibold text-gray-900 mb-3">
              Which of the following best describes this concept?
            </h4>
            <div className="space-y-3">
              {['A', 'B', 'C', 'D'].map((option) => (
                <label
                  key={option}
                  className={`block p-4 border-2 rounded-lg cursor-pointer transition-all ${
                    selectedAnswer === option
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="answer"
                    value={option}
                    checked={selectedAnswer === option}
                    onChange={(e) => setSelectedAnswer(e.target.value)}
                    className="sr-only"
                    disabled={showFeedback}
                  />
                  <div className="flex items-center">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full border-2 border-current flex items-center justify-center mr-3">
                      {selectedAnswer === option && <span className="w-3 h-3 bg-current rounded-full" />}
                    </span>
                    <span className="text-gray-700">Option {option}</span>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {showFeedback && (
            <div className={`p-4 rounded-lg mb-4 ${
              isCorrect ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
            }`}>
              <div className="flex items-center">
                {isCorrect ? (
                  <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                ) : (
                  <XCircle className="w-5 h-5 text-red-600 mr-2" />
                )}
                <span className={`font-semibold ${isCorrect ? 'text-green-900' : 'text-red-900'}`}>
                  {isCorrect ? 'Correct!' : 'Incorrect'}
                </span>
              </div>
              {currentQuestion.common_traps && currentQuestion.common_traps.length > 0 && (
                <div className="mt-2">
                  <p className="text-sm font-medium text-gray-700">Common Traps:</p>
                  <ul className="list-disc pl-5 mt-1 text-sm text-gray-600">
                    {currentQuestion.common_traps.map((trap, idx) => (
                      <li key={idx}>{trap}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          <button
            onClick={submitAnswer}
            disabled={!selectedAnswer || showFeedback}
            className="btn btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {showFeedback ? 'Loading next question...' : 'Submit Answer'}
            {!showFeedback && <ArrowRight className="w-4 h-4 ml-2 inline" />}
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
            <Brain className="w-8 h-8 text-primary-600" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Start Practice Session</h1>
          <p className="text-gray-600 mt-2">
            Configure your practice session and begin learning
          </p>
        </div>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Subject
            </label>
            <select
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="input"
            >
              {subjects.map((subject) => (
                <option key={subject.name} value={subject.name.toLowerCase()}>
                  {subject.name} ({subject.count} concepts)
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty
            </label>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="input"
            >
              <option value="mixed">Mixed (All Levels)</option>
              <option value="easy">Easy (1-2)</option>
              <option value="medium">Medium (3)</option>
              <option value="hard">Hard (4-5)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Questions
            </label>
            <input
              type="number"
              min="1"
              max="20"
              value={numQuestions}
              onChange={(e) => setNumQuestions(parseInt(e.target.value))}
              className="input"
            />
          </div>

          <button
            onClick={startSession}
            disabled={loading}
            className="btn btn-primary w-full"
          >
            {loading ? 'Starting...' : 'Start Practice Session'}
          </button>
        </div>
      </div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { BookOpen, Plus, RotateCw, CheckCircle } from 'lucide-react'
import { api } from '../api/client'

export default function Flashcards() {
  const [flashcards, setFlashcards] = useState([])
  const [subjects, setSubjects] = useState([])
  const [selectedSubject, setSelectedSubject] = useState(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [studyMode, setStudyMode] = useState(false)
  const [currentCardIndex, setCurrentCardIndex] = useState(0)
  const [showBack, setShowBack] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadFlashcards()
    loadSubjects()
  }, [selectedSubject])

  const loadSubjects = async () => {
    try {
      const res = await api.getSubjects()
      setSubjects(res.data.subjects)
    } catch (error) {
      console.error('Failed to load subjects:', error)
    }
  }

  const loadFlashcards = async () => {
    try {
      const res = await api.getFlashcards(selectedSubject)
      setFlashcards(res.data.flashcards)
    } catch (error) {
      console.error('Failed to load flashcards:', error)
    } finally {
      setLoading(false)
    }
  }

  const startStudyMode = () => {
    if (flashcards.length > 0) {
      setStudyMode(true)
      setCurrentCardIndex(0)
      setShowBack(false)
    }
  }

  const rateCard = async (quality) => {
    const card = flashcards[currentCardIndex]
    try {
      await api.reviewFlashcard(card.id, quality)

      // Move to next card
      if (currentCardIndex < flashcards.length - 1) {
        setCurrentCardIndex(currentCardIndex + 1)
        setShowBack(false)
      } else {
        setStudyMode(false)
        loadFlashcards() // Reload to get updated intervals
      }
    } catch (error) {
      console.error('Failed to rate card:', error)
    }
  }

  if (studyMode && flashcards.length > 0) {
    const currentCard = flashcards[currentCardIndex]

    return (
      <div className="max-w-2xl mx-auto">
        <div className="mb-4 flex justify-between items-center">
          <span className="text-sm text-gray-600">
            Card {currentCardIndex + 1} of {flashcards.length}
          </span>
          <button
            onClick={() => setStudyMode(false)}
            className="text-sm text-gray-600 hover:text-gray-900"
          >
            Exit Study Mode
          </button>
        </div>

        <div className="card min-h-[400px] flex flex-col justify-between">
          <div className="flex-1 flex items-center justify-center p-8">
            <div className="text-center">
              <p className="text-xs text-gray-500 mb-2">
                {showBack ? 'Answer' : 'Question'}
              </p>
              <h2 className="text-2xl font-bold text-gray-900">
                {showBack ? currentCard.back : currentCard.front}
              </h2>
            </div>
          </div>

          {!showBack ? (
            <button
              onClick={() => setShowBack(true)}
              className="btn btn-primary w-full"
            >
              Show Answer
              <RotateCw className="w-4 h-4 ml-2 inline" />
            </button>
          ) : (
            <div className="space-y-3">
              <p className="text-sm text-center text-gray-600">
                How well did you know this?
              </p>
              <div className="grid grid-cols-3 gap-3">
                <button
                  onClick={() => rateCard(1)}
                  className="btn bg-red-100 text-red-700 hover:bg-red-200"
                >
                  Again
                </button>
                <button
                  onClick={() => rateCard(3)}
                  className="btn bg-yellow-100 text-yellow-700 hover:bg-yellow-200"
                >
                  Good
                </button>
                <button
                  onClick={() => rateCard(5)}
                  className="btn bg-green-100 text-green-700 hover:bg-green-200"
                >
                  Easy
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="mt-4">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all"
              style={{ width: `${((currentCardIndex + 1) / flashcards.length) * 100}%` }}
            />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Flashcards</h1>
          <p className="text-gray-600">Spaced repetition learning system</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn btn-primary"
        >
          <Plus className="w-4 h-4 mr-2" />
          Create Flashcard
        </button>
      </div>

      <div className="flex space-x-4">
        <select
          value={selectedSubject || ''}
          onChange={(e) => setSelectedSubject(e.target.value || null)}
          className="input max-w-xs"
        >
          <option value="">All Subjects</option>
          {subjects.map((subject) => (
            <option key={subject.name} value={subject.name.toLowerCase()}>
              {subject.name}
            </option>
          ))}
        </select>

        {flashcards.length > 0 && (
          <button onClick={startStudyMode} className="btn btn-primary">
            <BookOpen className="w-4 h-4 mr-2" />
            Start Studying ({flashcards.filter(f => f.due).length} due)
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading ? (
          <div className="col-span-full text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          </div>
        ) : flashcards.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <BookOpen className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No flashcards yet. Create your first one!</p>
          </div>
        ) : (
          flashcards.map((card) => (
            <div key={card.id} className="card">
              {card.due && (
                <span className="inline-block px-2 py-1 bg-orange-100 text-orange-700 text-xs font-medium rounded mb-2">
                  Due for Review
                </span>
              )}
              <h3 className="font-semibold text-gray-900 mb-2">{card.front}</h3>
              <p className="text-sm text-gray-600 line-clamp-2">{card.back}</p>
              <div className="mt-4 flex items-center justify-between text-xs text-gray-500">
                <span>{card.subject}</span>
                <span>Reviewed: {card.repetitions}x</span>
              </div>
            </div>
          ))
        )}
      </div>

      {showCreateModal && (
        <CreateFlashcardModal
          subjects={subjects}
          onClose={() => setShowCreateModal(false)}
          onCreated={() => {
            setShowCreateModal(false)
            loadFlashcards()
          }}
        />
      )}
    </div>
  )
}

function CreateFlashcardModal({ subjects, onClose, onCreated }) {
  const [front, setFront] = useState('')
  const [back, setBack] = useState('')
  const [subject, setSubject] = useState('contracts')
  const [difficulty, setDifficulty] = useState('Intermediate')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.createFlashcard({
        front,
        back,
        subject,
        difficulty
      })
      onCreated()
    } catch (error) {
      console.error('Failed to create flashcard:', error)
      alert('Failed to create flashcard')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-2xl w-full p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Create Flashcard</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Front (Question)
            </label>
            <textarea
              value={front}
              onChange={(e) => setFront(e.target.value)}
              required
              rows={3}
              className="input"
              placeholder="What is consideration in contract law?"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Back (Answer)
            </label>
            <textarea
              value={back}
              onChange={(e) => setBack(e.target.value)}
              required
              rows={4}
              className="input"
              placeholder="Consideration is something of legal value given in exchange for a promise..."
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Subject
              </label>
              <select
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="input"
              >
                {subjects.map((s) => (
                  <option key={s.name} value={s.name.toLowerCase()}>
                    {s.name}
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
                <option value="Foundational">Foundational</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
                <option value="Expert">Expert</option>
              </select>
            </div>
          </div>

          <div className="flex space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary flex-1"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary flex-1"
            >
              {loading ? 'Creating...' : 'Create Flashcard'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

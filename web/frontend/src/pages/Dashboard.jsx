import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Brain, BookOpen, BarChart3, TrendingUp, Award, Flame } from 'lucide-react'
import { api } from '../api/client'

export default function Dashboard() {
  const [progress, setProgress] = useState(null)
  const [subjects, setSubjects] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [progressRes, subjectsRes] = await Promise.all([
        api.getProgress(),
        api.getSubjects()
      ])
      setProgress(progressRes.data)
      setSubjects(subjectsRes.data.subjects)
    } catch (error) {
      console.error('Failed to load dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Welcome to MBE Study System</h1>
        <p className="mt-2 text-gray-600">
          Your comprehensive bar exam preparation platform
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={Brain}
          label="Questions Answered"
          value={progress?.total_questions || 0}
          color="blue"
        />
        <StatCard
          icon={TrendingUp}
          label="Overall Accuracy"
          value={`${progress?.accuracy || 0}%`}
          color="green"
        />
        <StatCard
          icon={Flame}
          label="Current Streak"
          value={progress?.current_streak || 0}
          color="orange"
        />
        <StatCard
          icon={Award}
          label="Correct Answers"
          value={progress?.correct_answers || 0}
          color="purple"
        />
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <QuickActionCard
          to="/practice"
          icon={Brain}
          title="Start Practice"
          description="Practice MBE questions with instant feedback"
          color="primary"
        />
        <QuickActionCard
          to="/flashcards"
          icon={BookOpen}
          title="Review Flashcards"
          description="Spaced repetition learning system"
          color="indigo"
        />
        <QuickActionCard
          to="/progress"
          icon={BarChart3}
          title="View Progress"
          description="Track your performance and analytics"
          color="green"
        />
      </div>

      {/* Subjects Overview */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Available Subjects</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {subjects.map((subject) => (
            <Link
              key={subject.name}
              to={`/practice?subject=${subject.name.toLowerCase()}`}
              className="p-4 border border-gray-200 rounded-lg hover:border-primary-500 hover:shadow-md transition-all"
            >
              <h3 className="font-semibold text-gray-900">{subject.name}</h3>
              <p className="text-sm text-gray-600 mt-1">
                {subject.count} concepts available
              </p>
              {progress?.by_subject?.find(s => s.subject === subject.name.toLowerCase()) && (
                <div className="mt-2">
                  <div className="flex justify-between text-xs text-gray-600">
                    <span>Accuracy</span>
                    <span className="font-medium">
                      {progress.by_subject.find(s => s.subject === subject.name.toLowerCase()).accuracy}%
                    </span>
                  </div>
                  <div className="mt-1 w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full"
                      style={{
                        width: `${progress.by_subject.find(s => s.subject === subject.name.toLowerCase()).accuracy}%`
                      }}
                    />
                  </div>
                </div>
              )}
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      {progress?.last_study && (
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-2">Last Study Session</h2>
          <p className="text-gray-600">
            {new Date(progress.last_study).toLocaleDateString()} at{' '}
            {new Date(progress.last_study).toLocaleTimeString()}
          </p>
        </div>
      )}
    </div>
  )
}

function StatCard({ icon: Icon, label, value, color }) {
  const colors = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    orange: 'bg-orange-50 text-orange-600',
    purple: 'bg-purple-50 text-purple-600',
  }

  return (
    <div className="card">
      <div className="flex items-center">
        <div className={`p-3 rounded-lg ${colors[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
        <div className="ml-4">
          <p className="text-sm text-gray-600">{label}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  )
}

function QuickActionCard({ to, icon: Icon, title, description, color }) {
  const colors = {
    primary: 'text-primary-600 bg-primary-50',
    indigo: 'text-indigo-600 bg-indigo-50',
    green: 'text-green-600 bg-green-50',
  }

  return (
    <Link to={to} className="card hover:shadow-lg transition-shadow">
      <div className={`inline-flex p-3 rounded-lg ${colors[color]} mb-4`}>
        <Icon className="w-6 h-6" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 text-sm">{description}</p>
    </Link>
  )
}

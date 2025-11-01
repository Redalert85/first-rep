import { useState, useEffect } from 'react'
import { BarChart3, TrendingUp, Award, Target, Calendar } from 'lucide-react'
import { api } from '../api/client'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { Bar, Doughnut } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

export default function Progress() {
  const [progress, setProgress] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProgress()
  }, [])

  const loadProgress = async () => {
    try {
      const res = await api.getProgress()
      setProgress(res.data)
    } catch (error) {
      console.error('Failed to load progress:', error)
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

  if (!progress || progress.total_questions === 0) {
    return (
      <div className="text-center py-12">
        <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">No Progress Yet</h2>
        <p className="text-gray-600 mb-6">
          Start practicing to see your progress and analytics
        </p>
        <a href="/practice" className="btn btn-primary inline-flex items-center">
          Start Practicing
        </a>
      </div>
    )
  }

  // Prepare data for subject performance chart
  const subjectData = {
    labels: progress.by_subject.map(s => s.subject.toUpperCase()),
    datasets: [
      {
        label: 'Accuracy (%)',
        data: progress.by_subject.map(s => s.accuracy),
        backgroundColor: 'rgba(14, 165, 233, 0.8)',
        borderColor: 'rgba(14, 165, 233, 1)',
        borderWidth: 1,
      }
    ]
  }

  // Prepare data for correct vs incorrect doughnut chart
  const correctIncorrectData = {
    labels: ['Correct', 'Incorrect'],
    datasets: [
      {
        data: [
          progress.correct_answers,
          progress.total_questions - progress.correct_answers
        ],
        backgroundColor: [
          'rgba(34, 197, 94, 0.8)',
          'rgba(239, 68, 68, 0.8)',
        ],
        borderColor: [
          'rgba(34, 197, 94, 1)',
          'rgba(239, 68, 68, 1)',
        ],
        borderWidth: 1,
      }
    ]
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
      }
    }
  }

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
    },
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Progress & Analytics</h1>
        <p className="text-gray-600 mt-2">Track your performance and identify areas for improvement</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={Target}
          label="Total Questions"
          value={progress.total_questions}
          color="blue"
        />
        <StatCard
          icon={Award}
          label="Correct Answers"
          value={progress.correct_answers}
          color="green"
        />
        <StatCard
          icon={TrendingUp}
          label="Accuracy"
          value={`${progress.accuracy}%`}
          color="purple"
        />
        <StatCard
          icon={BarChart3}
          label="Current Streak"
          value={progress.current_streak}
          color="orange"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Performance by Subject</h2>
          <Bar data={subjectData} options={chartOptions} />
        </div>

        <div className="card">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Overall Performance</h2>
          <div className="max-w-sm mx-auto">
            <Doughnut data={correctIncorrectData} options={doughnutOptions} />
          </div>
        </div>
      </div>

      {/* Subject Breakdown Table */}
      <div className="card">
        <h2 className="text-lg font-bold text-gray-900 mb-4">Subject Breakdown</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Subject
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Questions
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Correct
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Accuracy
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Progress
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {progress.by_subject.map((subject) => (
                <tr key={subject.subject}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {subject.subject.toUpperCase()}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{subject.total}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{subject.correct}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      subject.accuracy >= 70
                        ? 'bg-green-100 text-green-800'
                        : subject.accuracy >= 50
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {subject.accuracy}%
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-600 h-2 rounded-full"
                        style={{ width: `${subject.accuracy}%` }}
                      />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Last Study Session */}
      {progress.last_study && (
        <div className="card">
          <div className="flex items-center">
            <Calendar className="w-5 h-5 text-gray-600 mr-2" />
            <div>
              <h3 className="text-sm font-medium text-gray-900">Last Study Session</h3>
              <p className="text-sm text-gray-600">
                {new Date(progress.last_study).toLocaleDateString('en-US', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Performance Insights */}
      <div className="card">
        <h2 className="text-lg font-bold text-gray-900 mb-4">Performance Insights</h2>
        <div className="space-y-4">
          {progress.accuracy >= 80 && (
            <InsightCard
              type="success"
              title="Excellent Performance!"
              description="You're doing great! Keep up the consistent practice."
            />
          )}
          {progress.accuracy >= 60 && progress.accuracy < 80 && (
            <InsightCard
              type="warning"
              title="Good Progress"
              description="You're on the right track. Focus on your weaker subjects to improve."
            />
          )}
          {progress.accuracy < 60 && (
            <InsightCard
              type="info"
              title="Keep Practicing"
              description="More practice will help improve your scores. Review the concepts you're struggling with."
            />
          )}
          {progress.current_streak >= 5 && (
            <InsightCard
              type="success"
              title={`🔥 ${progress.current_streak} Day Streak!`}
              description="Amazing consistency! Daily practice leads to better retention."
            />
          )}
          {progress.by_subject.some(s => s.accuracy < 50) && (
            <InsightCard
              type="warning"
              title="Focus Areas Identified"
              description={`Consider reviewing: ${progress.by_subject
                .filter(s => s.accuracy < 50)
                .map(s => s.subject.toUpperCase())
                .join(', ')}`}
            />
          )}
        </div>
      </div>
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

function InsightCard({ type, title, description }) {
  const styles = {
    success: 'bg-green-50 border-green-200 text-green-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    info: 'bg-blue-50 border-blue-200 text-blue-800',
  }

  return (
    <div className={`p-4 rounded-lg border ${styles[type]}`}>
      <h4 className="font-semibold mb-1">{title}</h4>
      <p className="text-sm opacity-90">{description}</p>
    </div>
  )
}

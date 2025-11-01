import { useState, useEffect } from 'react'
import { Library, BookOpen, FileText, ChevronRight } from 'lucide-react'
import { api } from '../api/client'
import ReactMarkdown from 'react-markdown'

export default function StudyMaterials() {
  const [subjects, setSubjects] = useState([])
  const [selectedSubject, setSelectedSubject] = useState(null)
  const [materials, setMaterials] = useState(null)
  const [selectedMaterial, setSelectedMaterial] = useState(null)
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

  const loadMaterials = async (subject) => {
    setLoading(true)
    setSelectedSubject(subject)
    try {
      const res = await api.getStudyMaterials(subject.toLowerCase())
      setMaterials(res.data.materials)
      // Auto-select first available material
      if (res.data.materials) {
        const firstMaterial = Object.keys(res.data.materials)[0]
        if (firstMaterial) {
          setSelectedMaterial(firstMaterial)
        }
      }
    } catch (error) {
      console.error('Failed to load materials:', error)
      setMaterials({})
    } finally {
      setLoading(false)
    }
  }

  const materialTypes = {
    outline: { icon: FileText, label: 'Outline', color: 'blue' },
    flowchart: { icon: ChevronRight, label: 'Flowcharts', color: 'green' },
    contrast_tables: { icon: BookOpen, label: 'Contrast Tables', color: 'purple' },
    checklist: { icon: Library, label: 'Checklist', color: 'orange' },
    drill: { icon: BookOpen, label: 'Drills', color: 'red' },
  }

  if (!selectedSubject) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Study Materials</h1>
          <p className="text-gray-600 mt-2">Access outlines, flowcharts, and study guides</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {subjects.map((subject) => (
            <button
              key={subject.name}
              onClick={() => loadMaterials(subject.name)}
              className="card hover:shadow-lg transition-all text-left"
            >
              <div className="flex items-center mb-4">
                <div className="p-3 bg-primary-100 rounded-lg">
                  <Library className="w-6 h-6 text-primary-600" />
                </div>
                <h3 className="ml-4 text-lg font-semibold text-gray-900">
                  {subject.name}
                </h3>
              </div>
              <p className="text-sm text-gray-600">
                {subject.count} concepts available
              </p>
              <div className="mt-4 flex items-center text-primary-600 text-sm font-medium">
                View Materials
                <ChevronRight className="w-4 h-4 ml-1" />
              </div>
            </button>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-12 gap-6">
      {/* Sidebar */}
      <div className="col-span-12 lg:col-span-3">
        <div className="card sticky top-6">
          <button
            onClick={() => {
              setSelectedSubject(null)
              setMaterials(null)
              setSelectedMaterial(null)
            }}
            className="text-primary-600 text-sm font-medium mb-4 hover:underline"
          >
            ← Back to Subjects
          </button>

          <h2 className="text-lg font-bold text-gray-900 mb-4">
            {selectedSubject}
          </h2>

          {loading ? (
            <div className="text-center py-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
            </div>
          ) : materials && Object.keys(materials).length > 0 ? (
            <div className="space-y-2">
              {Object.keys(materials).map((materialType) => {
                const typeInfo = materialTypes[materialType]
                if (!typeInfo) return null

                const Icon = typeInfo.icon
                return (
                  <button
                    key={materialType}
                    onClick={() => setSelectedMaterial(materialType)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      selectedMaterial === materialType
                        ? 'bg-primary-50 text-primary-700'
                        : 'hover:bg-gray-50 text-gray-700'
                    }`}
                  >
                    <div className="flex items-center">
                      <Icon className="w-4 h-4 mr-2" />
                      <span className="text-sm font-medium">{typeInfo.label}</span>
                    </div>
                  </button>
                )
              })}
            </div>
          ) : (
            <p className="text-sm text-gray-600">
              No materials available for this subject yet.
            </p>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="col-span-12 lg:col-span-9">
        <div className="card">
          {selectedMaterial && materials[selectedMaterial] ? (
            <div className="prose max-w-none">
              <ReactMarkdown>{materials[selectedMaterial]}</ReactMarkdown>
            </div>
          ) : (
            <div className="text-center py-12">
              <Library className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">Select a material type from the sidebar</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

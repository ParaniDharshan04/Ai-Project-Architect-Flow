import { useState, useEffect } from 'react'
import { getHistory } from '../services/api'
import Sidebar from '../components/Sidebar'
import ReactMarkdown from 'react-markdown'
import './History.css'

function History() {
  const [projects, setProjects] = useState([])
  const [selectedProject, setSelectedProject] = useState(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    loadHistory()
  }, [])
  
  const loadHistory = async () => {
    try {
      const response = await getHistory()
      setProjects(response.data)
    } catch (err) {
      alert('Failed to load history')
    } finally {
      setLoading(false)
    }
  }
  
  const handleCopy = (readme) => {
    navigator.clipboard.writeText(readme)
    alert('Copied to clipboard!')
  }
  
  const handleDownload = (readme, name) => {
    const blob = new Blob([readme], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${name}_README.md`
    a.click()
  }
  
  return (
    <div className="dashboard-layout">
      <Sidebar />
      <div className="history-content">
        <h1>Project History</h1>
        
        {loading ? (
          <div className="loading">Loading...</div>
        ) : projects.length === 0 ? (
          <div className="empty">No projects yet</div>
        ) : (
          <div className="history-grid">
            <div className="projects-list">
              {projects.map((project) => (
                <div
                  key={project.id}
                  className={`project-card ${selectedProject?.id === project.id ? 'active' : ''}`}
                  onClick={() => setSelectedProject(project)}
                >
                  <h3>{project.project_name}</h3>
                  <p>{new Date(project.created_at).toLocaleDateString()}</p>
                </div>
              ))}
            </div>
            
            {selectedProject && (
              <div className="project-detail">
                <div className="detail-header">
                  <h2>{selectedProject.project_name}</h2>
                  <div className="detail-actions">
                    <button onClick={() => handleCopy(selectedProject.generated_readme)}>
                      Copy
                    </button>
                    <button onClick={() => handleDownload(selectedProject.generated_readme, selectedProject.project_name)}>
                      Download
                    </button>
                  </div>
                </div>
                <div className="markdown-preview">
                  <ReactMarkdown>{selectedProject.generated_readme}</ReactMarkdown>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default History

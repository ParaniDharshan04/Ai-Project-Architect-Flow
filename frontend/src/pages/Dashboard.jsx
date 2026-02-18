import { useState } from 'react'
import { generateReadme } from '../services/api'
import Sidebar from '../components/Sidebar'
import ReactMarkdown from 'react-markdown'
import './Dashboard.css'

function Dashboard() {
  const [formData, setFormData] = useState({
    project_name: '',
    description: '',
    tech_stack: '',
    features: '',
    installation_steps: '',
    extra_notes: ''
  })
  const [mode, setMode] = useState('basic')
  const [readme, setReadme] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingStage, setLoadingStage] = useState('')
  
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }
  
  const handleGenerate = async () => {
    setLoading(true)
    setReadme('')
    
    if (mode === 'advanced') {
      setLoadingStage('Analyzing...')
      setTimeout(() => setLoadingStage('Planning...'), 2000)
      setTimeout(() => setLoadingStage('Writing...'), 4000)
      setTimeout(() => setLoadingStage('Reviewing...'), 6000)
    }
    
    try {
      const response = await generateReadme({ ...formData, mode })
      setReadme(response.data.readme)
    } catch (err) {
      alert(err.response?.data?.detail || 'Generation failed')
    } finally {
      setLoading(false)
      setLoadingStage('')
    }
  }
  
  const handleCopy = () => {
    navigator.clipboard.writeText(readme)
    alert('Copied to clipboard!')
  }
  
  const handleDownload = () => {
    const blob = new Blob([readme], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'README.md'
    a.click()
  }
  
  return (
    <div className="dashboard-layout">
      <Sidebar />
      <div className="dashboard-content">
        <div className="dashboard-header">
          <h1>AI README Architect</h1>
        </div>
        
        <div className="dashboard-main">
          <div className="form-section">
            <div className="mode-toggle">
              <button 
                className={mode === 'basic' ? 'active' : ''}
                onClick={() => setMode('basic')}
              >
                Basic README
              </button>
              <button 
                className={mode === 'advanced' ? 'active' : ''}
                onClick={() => setMode('advanced')}
              >
                Advanced AI Architect
              </button>
            </div>
            
            <div className="form-grid">
              <input
                name="project_name"
                placeholder="Project Name"
                value={formData.project_name}
                onChange={handleChange}
                required
              />
              <textarea
                name="description"
                placeholder="Project Description"
                value={formData.description}
                onChange={handleChange}
                rows="3"
                required
              />
              <textarea
                name="tech_stack"
                placeholder="Tech Stack (e.g., React, Node.js, PostgreSQL)"
                value={formData.tech_stack}
                onChange={handleChange}
                rows="2"
                required
              />
              <textarea
                name="features"
                placeholder="Features (one per line)"
                value={formData.features}
                onChange={handleChange}
                rows="4"
                required
              />
              <textarea
                name="installation_steps"
                placeholder="Installation Steps"
                value={formData.installation_steps}
                onChange={handleChange}
                rows="4"
                required
              />
              <textarea
                name="extra_notes"
                placeholder="Extra Notes (optional)"
                value={formData.extra_notes}
                onChange={handleChange}
                rows="2"
              />
            </div>
            
            <button 
              className="generate-btn"
              onClick={handleGenerate}
              disabled={loading}
            >
              {loading ? loadingStage || 'Generating...' : 'Generate README'}
            </button>
          </div>
          
          {readme && (
            <div className="result-section">
              <div className="result-header">
                <h2>Generated README</h2>
                <div className="result-actions">
                  <button onClick={handleCopy}>Copy</button>
                  <button onClick={handleDownload}>Download</button>
                </div>
              </div>
              <div className="markdown-preview">
                <ReactMarkdown>{readme}</ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard

import { useNavigate, useLocation } from 'react-router-dom'
import './Sidebar.css'

function Sidebar() {
  const navigate = useNavigate()
  const location = useLocation()
  
  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }
  
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>AI README</h2>
      </div>
      <nav className="sidebar-nav">
        <button 
          className={location.pathname === '/dashboard' ? 'active' : ''}
          onClick={() => navigate('/dashboard')}
        >
          Dashboard
        </button>
        <button 
          className={location.pathname === '/history' ? 'active' : ''}
          onClick={() => navigate('/history')}
        >
          History
        </button>
        <button onClick={handleLogout}>Logout</button>
      </nav>
    </div>
  )
}

export default Sidebar

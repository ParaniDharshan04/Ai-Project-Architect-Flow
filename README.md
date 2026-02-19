# AI Project Analyst & README Architect

![AI](https://img.shields.io/badge/AI-Multi--Agent-blue)
![Langflow](https://img.shields.io/badge/Built%20With-Langflow-purple)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![React](https://img.shields.io/badge/Frontend-React-blue)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![License](https://img.shields.io/badge/License-MIT-orange)

> An elite multi-agent AI system that analyzes software project ideas and automatically generates professional GitHub README documentation using Langflow orchestration.

---

## Overview

**AI Project Analyst & README Architect** is a production-ready full-stack AI SaaS platform that demonstrates modern **Agentic AI Architecture**. Instead of relying on a single prompt, this system orchestrates multiple specialized AI agents working together:

- **Analyzer Agent** - Understands and refines project ideas
- **Planner Agent** - Designs structured documentation
- **Writer Agent** - Generates professional README files  
- **Reviewer Agent** - Produces polished final content

This project showcases the evolution from writing prompts to **orchestrating intelligent AI systems**.

---

## Architecture

### System Flow

```
User Input (Project Details)
        ↓
   Prompt Template
        ↓
   Analyzer LLM (Refines understanding)
        ↓
   Planner LLM (Structures documentation)
        ↓
   Writer LLM (Generates content)
        ↓
   Reviewer LLM (Polishes output)
        ↓
Final Professional README
```

### Multi-Agent Pipeline

| Stage    | Role          | Purpose                           |
|----------|---------------|-----------------------------------|
| Analyzer | AI Analyst    | Improves project understanding    |
| Planner  | AI Architect  | Structures documentation          |
| Writer   | AI Writer     | Generates README content          |
| Reviewer | AI Publisher  | Final quality assurance & delivery|

---

## Tech Stack

### Frontend
- **React** with Vite
- **React Router** for navigation
- **Axios** for API calls
- **React Markdown** for preview
- **Glassmorphism UI** with dark theme

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Production database
- **JWT Authentication** - Secure user sessions
- **Pydantic** - Data validation

### AI Orchestration
- **Langflow** - Visual AI pipeline builder
- **Google Gemini API** - LLM provider
- **Multi-Stage Agent System** - Specialized AI roles
- **httpx** - Async HTTP client

### DevOps
- **Docker** ready
- **Environment-based configuration**
- **Auto-reload development servers**

---

## Features

- User registration & JWT authentication
- **Basic Mode** - Template-based README generation
- **Advanced AI Mode** - Multi-agent Langflow pipeline
- Project history tracking
- Real-time markdown preview
- Copy to clipboard functionality
- Download README.md files
- Responsive dark glassmorphism UI
- Protected routes & secure API endpoints
- Loading states with agent progress indicators

---

## Installation

### Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL 12+
- Langflow (for Advanced AI mode)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ai-readme-architect.git
cd ai-readme-architect
```

### 2. Database Setup
```bash
# Create PostgreSQL database
createdb ai_readme_db

# Or use the provided script (Windows)
powershell -ExecutionPolicy Bypass -File setup_database.ps1
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials:
# - DATABASE_URL
# - SECRET_KEY
# - LANGFLOW_API_KEY
# - LANGFLOW_FLOW_ID

# Start backend server
python -m uvicorn app.main:app --reload
```

Backend will run at: `http://localhost:8000`

### 4. Frontend Setup
```bash
cd frontend
npm install

# Start development server
npm run dev
```

Frontend will run at: `http://localhost:5173`

### 5. Langflow Setup (Optional - for Advanced AI Mode)
```bash
# Install Langflow
pip install langflow

# Start Langflow
langflow run

# Access Langflow UI at http://127.0.0.1:7860
# Import the multi-agent flow and get your Flow ID
```

---

## How It Works

### Input Structure
Provide structured project information:
- **Project Name** - Your project title
- **Description** - What your project does
- **Tech Stack** - Technologies used
- **Features** - Key functionality
- **Installation Steps** - Setup instructions
- **Extra Notes** - Additional information

### AI Pipeline Process

1. **Analysis Phase** - AI analyzes and understands your project concept
2. **Planning Phase** - Structures optimal documentation layout
3. **Writing Phase** - Generates professional README content
4. **Review Phase** - Polishes and finalizes output

### Output
- Production-ready GitHub README
- Structured sections (Description, Features, Installation, etc.)
- Professional formatting
- Markdown-compatible content

---

## API Endpoints

### Authentication
- `POST /auth/register` - Create new user account
- `POST /auth/login` - Login and receive JWT token
- `GET /auth/me` - Get current user info

### Projects
- `POST /projects/generate-readme` - Generate README (Basic or Advanced mode)
- `GET /projects/history` - Retrieve user's project history

### API Documentation
Interactive API docs available at: `http://localhost:8000/docs`

---

## Database Schema

### Users Table
```sql
id              UUID PRIMARY KEY
name            VARCHAR
email           VARCHAR UNIQUE
password_hash   VARCHAR
created_at      TIMESTAMP
```

### Projects Table
```sql
id                  UUID PRIMARY KEY
user_id             UUID FOREIGN KEY
project_name        VARCHAR
description         TEXT
tech_stack          TEXT
features            TEXT
installation_steps  TEXT
extra_notes         TEXT
generated_readme    TEXT
created_at          TIMESTAMP
```

---

## Example Use Case

**Input:**
```
Project: AI Web Scraper
Description: Automated web scraping tool with AI-powered data extraction
Tech Stack: Python, BeautifulSoup, OpenAI API
Features: Smart extraction, Data cleaning, Export to CSV
Installation: pip install -r requirements.txt
```

**Output:**
- Structured GitHub README
- Professional formatting
- Complete documentation sections
- Installation guide
- Feature breakdown

---

## Why This Project Matters

This project demonstrates:
- **Agentic AI System Design** - Multiple specialized agents working together
- **Multi-LLM Orchestration** - Coordinating different AI models
- **Langflow Automation** - Visual pipeline building
- **Real-World AI Architecture** - Production-ready patterns
- **Full-Stack Integration** - React + FastAPI + PostgreSQL + AI

Perfect for showcasing advanced AI engineering skills and modern software architecture

---

## Project Structure

```
ai-readme-architect/
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service layer
│   │   └── App.jsx         # Main app component
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── app/
│   │   ├── routes/         # API endpoints
│   │   ├── models.py       # Database models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── auth.py         # JWT authentication
│   │   ├── database.py     # Database connection
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── .env
├── README.md
└── setup_database.ps1
```

---

## Configuration

### Environment Variables

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/ai_readme_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
LANGFLOW_API_URL=http://127.0.0.1:7860/api/v1/run
LANGFLOW_FLOW_ID=your-flow-id
LANGFLOW_API_KEY=your-api-key
```

---

## Troubleshooting

### Common Issues

**Database Connection Error**
- Ensure PostgreSQL is running
- Verify DATABASE_URL in .env
- Check password encoding (use %40 for @ symbol)

**Langflow API Error**
- Verify Langflow is running at port 7860
- Check LANGFLOW_FLOW_ID is correct
- Ensure API key is valid
- Monitor API quota limits

**Frontend Not Loading**
- Check if backend is running on port 8000
- Verify CORS settings in backend
- Clear browser cache

---

## Future Enhancements

- Auto diagram generation from project structure
- Repository structure analysis
- Direct GitHub API integration
- README version history and comparison
- Multi-language README generation
- Custom template support
- Collaborative editing features
- AI-powered code documentation

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

MIT License - Feel free to use and modify this project.

---

## Acknowledgments

- Built with Langflow for AI orchestration
- Powered by Google Gemini API
- Inspired by modern agentic AI architectures

---

## Contact & Support

For questions, issues, or feature requests, please open an issue on GitHub.

**Built with passion for AI engineering and developer productivity.**

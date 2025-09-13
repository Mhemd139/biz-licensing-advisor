# System Architecture

## Overview
Business Licensing Advisor - A full-stack system helping Israeli restaurant owners understand regulatory requirements through AI-powered report generation.

## Architecture Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │  External APIs  │
│   (React)       │    │   (FastAPI)     │    │                 │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Questionnaire │◄──►│ • /health       │    │ • OpenAI API    │
│ • Report Display│    │ • /assess       │◄──►│   GPT-3.5-turbo │
│ • PDF Export    │    │ • /requirements │    │ • 1000 tokens   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Data Layer     │
                       ├─────────────────┤
                       │ requirements.json│
                       │ • 17 rules      │
                       │ • Hebrew/English│
                       │ • Source refs   │
                       └─────────────────┘
```

## Component Breakdown

### Frontend (React + Vite)
- **Location**: `/frontend/`
- **Port**: `http://localhost:5173`
- **Technology**: React 18, Vite, vanilla CSS
- **Components**:
  - Business questionnaire form (5 inputs)
  - Report display with sections
  - PDF export functionality

### Backend (FastAPI + Python)
- **Location**: `/backend/`
- **Port**: `http://localhost:8000`
- **Technology**: FastAPI, Pydantic, Python 3.9+
- **Modules**:
  - `app.py` - Main API server with 3 endpoints
  - `matching.py` - Rule matching algorithm
  - `llm.py` - OpenAI integration and report generation

### Data Layer
- **Location**: `/data/`
- **Format**: JSON files
- **Content**: 17 curated Israeli licensing rules
- **Languages**: Hebrew (source) + English (translated)

### AI Integration
- **Provider**: OpenAI
- **Model**: GPT-3.5-turbo
- **Configuration**: 1000 max tokens, 0.3 temperature
- **Purpose**: Transform rule matches into personalized reports

## Data Flow

### 1. User Input Flow
```
User fills form → Frontend validates → POST /assess → Backend processes
```

### 2. Rule Matching Flow
```
Business Profile → Matching Engine → Filtered Rules → LLM Processing → Report
```

### 3. Response Flow
```
Generated Report → Backend validates → Frontend displays → PDF export option
```

## Key Algorithms

### Matching Engine
1. **Filter**: Check each rule against profile triggers
2. **Guard Logic**: Apply Police exemption rules
3. **Sort**: Priority → tightness → authority
4. **Return**: Ordered list of applicable rules

### LLM Processing
1. **Input**: Business profile + matched rules
2. **Prompt**: Structured template with Israeli context
3. **Output**: JSON report with sections
4. **Validation**: Ensure only provided rule IDs referenced

## Technology Stack

### Backend Stack
- **Framework**: FastAPI (async, OpenAPI docs)
- **Validation**: Pydantic models
- **AI**: OpenAI Python SDK
- **Environment**: dotenv for configuration
- **CORS**: Configured for localhost:5173

### Frontend Stack
- **Framework**: React 18 + Vite
- **Styling**: Vanilla CSS (functionality over aesthetics)
- **Build**: Vite for fast development
- **HTTP**: Fetch API for backend communication

### Development Tools
- **Primary**: Claude Code (Anthropic)
- **Planning**: ChatGPT (OpenAI)
- **Prototyping**: Replit for UX validation

## Security & Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-proj-...  # Required for LLM integration
```

### CORS Policy
- Frontend: `http://localhost:5173`
- Development only (not production-ready)

### API Security
- Input validation via Pydantic
- Error handling with proper HTTP codes
- LLM response validation

## Deployment Architecture

### Local Development
```
Backend:  uvicorn app:app --reload  (port 8000)
Frontend: npm run dev              (port 5173)
```

### Production Ready
- Backend: Render/Railway deployment
- Frontend: Vercel/Netlify hosting
- Environment: Secure API key management

## File Structure
```
biz-licensing-advisor/
├── backend/           # FastAPI server
│   ├── app.py        # Main API endpoints
│   ├── matching.py   # Rule matching logic
│   ├── llm.py        # OpenAI integration
│   └── tests/        # Test suite
├── frontend/         # React application
│   └── src/          # React components
├── data/             # JSON data files
│   └── requirements.json  # 17 licensing rules
├── docs/             # Documentation
├── ai/               # AI tools documentation
└── scripts/          # Data processing scripts
```

## Performance Characteristics

### Response Times
- Rule matching: <100ms (deterministic)
- LLM report generation: 2-5 seconds
- Total /assess endpoint: 2-6 seconds

### Scalability
- Current: Single-server, file-based
- Bottleneck: OpenAI API rate limits
- Future: Database, caching, async processing

### Resource Usage
- Memory: <100MB (17 rules in memory)
- Storage: <10MB (JSON files)
- Network: Depends on LLM usage

## Error Handling Strategy

### Backend Errors
- File not found → Graceful degradation
- LLM API failure → Error message with rule list
- Validation errors → Clear error responses

### Frontend Errors
- Network failures → User-friendly messages
- Form validation → Real-time feedback
- API errors → Fallback display options
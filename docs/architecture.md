# System Architecture

## Overview
The Business Licensing Advisor is a full-stack web application that processes Israeli restaurant licensing requirements and generates personalized compliance reports using AI.

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   Services      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
│                      │                      │
├─ Business Form      ├─ Rule Matching      ├─ OpenAI API
├─ Report Display     ├─ LLM Integration    └─ GPT-3.5-turbo
├─ PDF Export         ├─ Data Validation
└─ Error Handling     └─ API Endpoints

                      ┌─────────────────┐
                      │   Data Layer    │
                      │   (JSON)        │
                      └─────────────────┘
                      │
                      ├─ requirements.json
                      └─ 17 licensing rules
```

## Component Details

### Frontend (React + Vite)
- **Technology**: React 19, TypeScript, Tailwind CSS
- **Build Tool**: Vite 7.1.2
- **Deployment**: Vercel/Netlify ready
- **Features**:
  - Business profile questionnaire
  - Real-time form validation
  - Report visualization
  - PDF export via browser print
  - Error handling with fallback

### Backend (FastAPI + Python)
- **Technology**: FastAPI, Python 3.9+, Pydantic
- **Server**: Uvicorn ASGI
- **Deployment**: Render/Railway ready
- **Features**:
  - RESTful API design
  - Automatic API documentation
  - Input validation
  - CORS configuration
  - Environment-based configuration

### AI Integration
- **Model**: OpenAI GPT-3.5-turbo
- **Configuration**:
  - Temperature: 0.3 (consistent output)
  - Max Tokens: 1000 (optimized for speed)
  - System prompt: Structured report generation
- **Features**:
  - Personalized report generation
  - Rule reference validation
  - Hebrew/English bilingual support

### Data Layer
- **Format**: JSON (development), PostgreSQL-ready
- **Source**: Curated from Hebrew PDF documents
- **Structure**: 17 licensing rules with triggers
- **Features**:
  - Schema validation
  - Bilingual descriptions
  - Priority classification
  - Authority mapping

## Data Flow

### 1. User Input
```
User fills questionnaire → Frontend validation → API request
```

### 2. Rule Matching
```
Business profile → Matching engine → Filtered rules → Rule IDs
```

### 3. AI Processing
```
Profile + Rules → OpenAI API → Structured report → Validation
```

### 4. Response
```
Report JSON → Frontend rendering → User display/PDF export
```

## API Endpoints

### Core Endpoints
```
GET  /health          - Health check
GET  /requirements    - All licensing rules
POST /assess          - Generate assessment report
```

## Performance Characteristics

### Response Times
- Rule matching: <100ms (deterministic algorithm)
- LLM processing: 2-5 seconds (GPT-3.5-turbo)
- Total request: 2-6 seconds
- Static assets: <500ms (CDN)

## Development Tools Integration

### AI-First Development
- **Claude Code**: Primary development assistant
- **ChatGPT**: System planning and design
- **Replit**: UI/UX prototyping and validation

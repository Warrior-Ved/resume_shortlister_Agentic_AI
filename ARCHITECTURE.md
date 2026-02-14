# Project Architecture & Design Document

## Resume Shortlister AI - Technical Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 3000)                │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ Job Posting  │ │   Resume     │ │  Dashboard   │        │
│  │    Form      │ │   Uploader   │ │  & Results   │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/REST API
┌────────────────────────────┴────────────────────────────────┐
│              FastAPI Backend (Port 8000)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  API Endpoints                        │  │
│  │  /jobs/create  /upload  /start  /status  /shortlist  │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                            │                                 │
│  ┌────────────────────────┴─────────────────────────────┐  │
│  │              Resume Processing Pipeline               │  │
│  │                                                        │  │
│  │  1. PDF Parser (PyMuPDF)                             │  │
│  │     └─> Extract text & metadata from each page       │  │
│  │                                                        │  │
│  │  2. Phase 1 Shortlister (No LLM)                     │  │
│  │     └─> Keyword matching & experience filtering      │  │
│  │                                                        │  │
│  │  3. Phase 2 Shortlister (Ollama + LLM)               │  │
│  │     └─> Comprehensive AI-powered review              │  │
│  │                                                        │  │
│  │  4. MCP Tools (Model Context Protocol)               │  │
│  │     └─> Structured resume analysis for LLM           │  │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────┐
│              Ollama LLM (Port 11434)                         │
│              Model: Ministral 3B                             │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. Job Creation
   User Input → Frontend → Backend → Job Storage (In-Memory)
   
2. Resume Upload
   PDF File → Frontend → Backend → PDF Parser
   └─> Individual Resume Pages → Text Extraction
       └─> Structured Resume Objects → Resume Storage
   
3. Two-Phase Shortlisting
   
   Phase 1 (Keyword Matching):
   Resumes → Keyword Scorer → Experience Filter → Phase 1 Results
   
   Phase 2 (LLM Review):
   Phase 1 Results → Prompt Generator → Ollama LLM
   └─> Confidence Scores → Cover Letter Generation
       └─> Final Shortlist
   
4. Results Display
   Final Shortlist → Frontend → Dashboard & Candidate Cards
```

### Component Details

#### 1. Frontend Components

**JobPostingForm.jsx**
- Collects job requirements
- Validates input
- Sends data to backend
- Manages form state

**ResumeUploader.jsx**
- File selection interface
- PDF validation
- Upload progress
- Triggers parsing

**Dashboard.jsx**
- Real-time status updates
- Statistics display
- Phase progress tracking
- Visual indicators

**ShortlistedCandidates.jsx**
- Collapsible candidate cards
- Confidence score display
- Skills visualization
- Cover letter presentation

#### 2. Backend Components

**main.py** - FastAPI Application
- Route definitions
- CORS configuration
- Background task management
- In-memory data storage

**models.py** - Data Models
- Pydantic schemas
- Type validation
- Data serialization
- API contracts

**resume_parser.py** - PDF Processing
- Multi-page PDF splitting
- Text extraction (PyMuPDF)
- Metadata extraction
- Skill identification
- Experience parsing

**phase1_shortlister.py** - Keyword Filtering
- Tech stack matching
- Experience validation
- Score calculation
- Candidate ranking

**phase2_shortlister.py** - LLM Integration
- Ollama API client
- Prompt engineering
- Response parsing
- Confidence scoring
- Cover letter generation

**mcp_tools.py** - MCP Implementation
- Tool definitions
- Resume data access
- Requirement matching
- Structured analysis

### Database Schema (In-Memory)

```python
jobs_db = {
    "job_id": {
        "id": str,
        "job_posting": JobPosting,
        "total_resumes": int,
        "resumes_in_review": int,
        "phase1_completed": int,
        "phase2_completed": int,
        "shortlisted_count": int,
        "status": str,  # pending, uploaded, phase1, phase2, completed
        "created_at": datetime,
        "phase1_results": List[Resume],
        "phase2_results": List[ShortlistedCandidate],
        "shortlisted": List[dict]
    }
}

resumes_db = {
    "job_id": List[Resume]
}
```

### API Endpoints

#### Job Management
```
POST   /api/jobs/create
GET    /api/jobs
GET    /api/jobs/{job_id}/status
GET    /api/jobs/{job_id}/shortlisted
```

#### Resume Processing
```
POST   /api/jobs/{job_id}/upload-resumes
POST   /api/jobs/{job_id}/start-shortlisting
```

#### MCP Tools
```
GET    /api/mcp/tools
```

### Algorithms

#### Phase 1 Scoring Algorithm
```python
score = (keyword_match_ratio * 0.7) + (experience_score * 0.3)

where:
- keyword_match_ratio = matched_skills / required_skills
- experience_score = min(1.0, experience / (min_experience * 2))
```

#### Phase 2 LLM Prompting
```
Input: Resume + Job Requirements
Output: {
    "is_suitable": boolean,
    "confidence": float (0-1),
    "reasoning": string,
    "cover_letter": string
}
```

### Security Considerations

1. **File Upload**
   - PDF validation only
   - File size limits
   - Sanitized filenames

2. **API Security**
   - CORS configuration
   - Input validation (Pydantic)
   - Error handling

3. **Data Privacy**
   - In-memory storage (no persistence)
   - No data retention
   - Local processing

### Performance Optimization

1. **Background Processing**
   - Async shortlisting
   - Non-blocking API responses
   - Status polling

2. **Efficient Parsing**
   - Page-by-page processing
   - Streaming text extraction
   - Cached results

3. **LLM Optimization**
   - Local inference (Ollama)
   - Batched processing
   - Timeout handling

### Error Handling

1. **Frontend**
   - User-friendly error messages
   - Retry mechanisms
   - Loading states

2. **Backend**
   - Try-catch blocks
   - Graceful degradation
   - Logging

3. **LLM**
   - Timeout handling
   - Fallback responses
   - Error recovery

### Future Enhancements

1. **Database Integration**
   - PostgreSQL for job storage
   - MongoDB for resume documents
   - Redis for caching

2. **Advanced Features**
   - Email notifications
   - Interview scheduling
   - Resume ranking explanation
   - Multi-model comparison

3. **Scalability**
   - Microservices architecture
   - Queue-based processing (Celery)
   - Distributed LLM inference

4. **Analytics**
   - Hiring funnel metrics
   - Model performance tracking
   - A/B testing

### Testing Strategy

1. **Unit Tests**
   - Resume parsing
   - Scoring algorithms
   - API endpoints

2. **Integration Tests**
   - End-to-end workflow
   - LLM integration
   - File upload

3. **Performance Tests**
   - Large PDF handling
   - Concurrent requests
   - LLM response time

### Deployment

1. **Local Development**
   - Vite dev server (Frontend)
   - Uvicorn (Backend)
   - Ollama (LLM)

2. **Production**
   - Nginx reverse proxy
   - Gunicorn + Uvicorn workers
   - Docker containers
   - Cloud deployment (AWS/Azure/GCP)

### Monitoring

1. **Application Metrics**
   - Request/response times
   - Error rates
   - Active jobs

2. **LLM Metrics**
   - Inference time
   - Token usage
   - Success rate

3. **Business Metrics**
   - Jobs created
   - Resumes processed
   - Shortlist conversion rate

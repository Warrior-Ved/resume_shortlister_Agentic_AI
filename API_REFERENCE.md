# API Reference

Complete API documentation for the Resume Shortlister AI backend.

---

## Base URL

```
http://localhost:8000
```

---

## Table of Contents

- [Endpoints Overview](#endpoints-overview)
- [Root Endpoint](#root-endpoint)
- [Job Management](#job-management)
  - [Create Job](#create-job)
  - [Upload Resumes](#upload-resumes)
  - [Start Shortlisting](#start-shortlisting)
  - [Get Job Status](#get-job-status)
  - [Get Shortlisted Candidates](#get-shortlisted-candidates)
  - [List All Jobs](#list-all-jobs)
- [MCP Tools](#mcp-tools)
- [Data Models](#data-models)
- [Error Handling](#error-handling)

---

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/jobs/create` | Create a new job posting |
| POST | `/api/jobs/{job_id}/upload-resumes` | Upload PDF with multiple resumes |
| POST | `/api/jobs/{job_id}/start-shortlisting` | Start two-phase shortlisting process |
| GET | `/api/jobs/{job_id}/status` | Get job processing status |
| GET | `/api/jobs/{job_id}/shortlisted` | Get final shortlisted candidates |
| GET | `/api/jobs` | List all jobs |
| GET | `/api/mcp/tools` | Get MCP tools definition |

---

## Root Endpoint

### GET `/`

Health check endpoint to verify API is running.

**Response:**
```json
{
  "message": "Resume Shortlister AI API",
  "status": "running"
}
```

---

## Job Management

### Create Job

Create a new job posting for resume screening.

**Endpoint:** `POST /api/jobs/create`

**Request Body:**
```json
{
  "job_title": "Senior Full Stack Developer",
  "required_skills": ["React", "Node.js", "Python", "AWS"],
  "preferred_skills": ["Docker", "Kubernetes", "CI/CD"],
  "minimum_experience_years": 5,
  "job_description": "We are looking for an experienced full stack developer...",
  "phase1_shortlist_count": 10,
  "phase2_shortlist_count": 5
}
```

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| job_title | string | Yes | Title of the job position |
| required_skills | array[string] | Yes | List of mandatory skills |
| preferred_skills | array[string] | No | List of preferred/nice-to-have skills |
| minimum_experience_years | integer | Yes | Minimum years of experience required |
| job_description | string | Yes | Detailed job description |
| phase1_shortlist_count | integer | No | Number of candidates to shortlist in Phase 1 (default: 10) |
| phase2_shortlist_count | integer | No | Number of candidates to shortlist in Phase 2 (default: 5) |

**Response:**
```json
{
  "job_id": "2f9451b4-7c01-4d47-8bb5-6660f131917b",
  "message": "Job created successfully",
  "status": "pending"
}
```

**Status Codes:**
- `200 OK` - Job created successfully
- `422 Unprocessable Entity` - Invalid request body

---

### Upload Resumes

Upload a PDF file containing multiple resumes for a job.

**Endpoint:** `POST /api/jobs/{job_id}/upload-resumes`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| job_id | string (UUID) | The job ID returned from create job |

**Request:**
- Content-Type: `multipart/form-data`
- Form field: `file` (PDF file)

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/api/jobs/{job_id}/upload-resumes" \
  -F "file=@resumes.pdf"
```

**Response:**
```json
{
  "message": "Uploaded and processed 8 resumes",
  "total_resumes": 8
}
```

**Status Codes:**
- `200 OK` - Resumes uploaded and processed successfully
- `404 Not Found` - Job ID not found
- `500 Internal Server Error` - Error processing file

**Notes:**
- Accepts single PDF file containing multiple resumes
- Each page is treated as a separate resume
- PDF is automatically parsed and text extracted
- Resumes are stored in memory for processing

---

### Start Shortlisting

Start the two-phase AI shortlisting process.

**Endpoint:** `POST /api/jobs/{job_id}/start-shortlisting`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| job_id | string (UUID) | The job ID |

**Request:**
No request body required.

**Response:**
```json
{
  "message": "Shortlisting process started",
  "status": "processing"
}
```

**Status Codes:**
- `200 OK` - Shortlisting process started
- `404 Not Found` - Job ID not found
- `400 Bad Request` - No resumes uploaded for this job

**Processing Phases:**

1. **Phase 1** - Keyword & Experience Matching
   - Fast, rule-based filtering
   - Skills matching algorithm
   - Experience threshold check
   - No LLM required

2. **Phase 2** - AI-Powered Review
   - Comprehensive LLM analysis (Ollama)
   - Confidence scoring (0-100%)
   - AI-generated cover letters
   - MCP tool integration

**Notes:**
- Process runs asynchronously in the background
- Poll `/api/jobs/{job_id}/status` for progress updates
- Status transitions: `pending` → `processing` → `phase1` → `phase2` → `completed`

---

### Get Job Status

Get the current processing status of a job.

**Endpoint:** `GET /api/jobs/{job_id}/status`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| job_id | string (UUID) | The job ID |

**Response:**
```json
{
  "job_id": "2f9451b4-7c01-4d47-8bb5-6660f131917b",
  "job_title": "Senior Full Stack Developer",
  "total_resumes": 8,
  "resumes_in_review": 0,
  "phase1_completed": 5,
  "phase2_completed": 3,
  "shortlisted_count": 3,
  "status": "completed",
  "created_at": "2026-02-14T10:30:00"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| job_id | string | Unique job identifier |
| job_title | string | Job title |
| total_resumes | integer | Total number of resumes uploaded |
| resumes_in_review | integer | Number of resumes currently being processed |
| phase1_completed | integer | Number of resumes that passed Phase 1 |
| phase2_completed | integer | Number of resumes that passed Phase 2 |
| shortlisted_count | integer | Final number of shortlisted candidates |
| status | string | Current job status (see below) |
| created_at | string (ISO 8601) | Job creation timestamp |

**Status Values:**

| Status | Description |
|--------|-------------|
| pending | Job created, waiting for resume upload |
| uploaded | Resumes uploaded, ready to process |
| processing | Shortlisting process started |
| phase1 | Phase 1 (keyword matching) in progress |
| phase2 | Phase 2 (AI review) in progress |
| completed | All processing completed |
| error | An error occurred during processing |

**Status Codes:**
- `200 OK` - Status retrieved successfully
- `404 Not Found` - Job ID not found

---

### Get Shortlisted Candidates

Get the final list of shortlisted candidates with AI analysis.

**Endpoint:** `GET /api/jobs/{job_id}/shortlisted`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| job_id | string (UUID) | The job ID |

**Response:**
```json
{
  "job_id": "2f9451b4-7c01-4d47-8bb5-6660f131917b",
  "job_title": "Senior Full Stack Developer",
  "status": "completed",
  "shortlisted": [
    {
      "resume_id": "resume_1",
      "candidate_name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1-234-567-8900",
      "skills": ["React", "Node.js", "Python", "AWS", "Docker"],
      "experience_years": 7,
      "confidence_score": 92,
      "ai_summary": "Excellent candidate with 7 years of experience...",
      "cover_letter": "Dear Hiring Manager,\n\nI am writing to express my strong interest..."
    },
    {
      "resume_id": "resume_3",
      "candidate_name": "Jane Smith",
      "email": "jane.smith@example.com",
      "phone": "+1-234-567-8901",
      "skills": ["React", "Node.js", "Python", "Kubernetes"],
      "experience_years": 6,
      "confidence_score": 88,
      "ai_summary": "Strong candidate with relevant cloud experience...",
      "cover_letter": "Dear Hiring Manager,\n\nWith 6 years of experience in full stack development..."
    }
  ]
}
```

**Candidate Object Fields:**

| Field | Type | Description |
|-------|------|-------------|
| resume_id | string | Unique resume identifier |
| candidate_name | string | Candidate's full name |
| email | string | Email address |
| phone | string | Phone number |
| skills | array[string] | List of candidate's skills |
| experience_years | integer | Years of experience |
| confidence_score | integer | AI confidence score (0-100) |
| ai_summary | string | AI-generated summary of candidate |
| cover_letter | string | AI-generated personalized cover letter |

**Status Codes:**
- `200 OK` - Shortlisted candidates retrieved successfully
- `404 Not Found` - Job ID not found

**Notes:**
- Only available after job status is `completed`
- Candidates are ordered by confidence score (highest first)
- Empty array if no candidates passed shortlisting criteria

---

### List All Jobs

Get a list of all jobs in the system.

**Endpoint:** `GET /api/jobs`

**Response:**
```json
{
  "jobs": [
    {
      "job_id": "2f9451b4-7c01-4d47-8bb5-6660f131917b",
      "job_title": "Senior Full Stack Developer",
      "status": "completed",
      "total_resumes": 8,
      "shortlisted_count": 3,
      "created_at": "2026-02-14T10:30:00"
    },
    {
      "job_id": "3b484dd9-ca79-4fe7-992f-5edf4bb01b57",
      "job_title": "DevOps Engineer",
      "status": "phase2",
      "total_resumes": 12,
      "shortlisted_count": 0,
      "created_at": "2026-02-14T11:15:00"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Jobs list retrieved successfully

---

## MCP Tools

### Get MCP Tools Definition

Get the Model Context Protocol (MCP) tools definition used for LLM integration.

**Endpoint:** `GET /api/mcp/tools`

**Response:**
```json
{
  "tools": [
    {
      "name": "analyze_resume",
      "description": "Analyze a resume against job requirements",
      "input_schema": {
        "type": "object",
        "properties": {
          "resume_text": {
            "type": "string",
            "description": "Full text of the resume"
          },
          "job_requirements": {
            "type": "object",
            "description": "Job requirements and skills"
          }
        }
      }
    }
  ]
}
```

**Status Codes:**
- `200 OK` - MCP tools definition retrieved successfully

---

## Data Models

### JobPosting

```python
{
  "job_title": str,
  "required_skills": List[str],
  "preferred_skills": List[str] = [],
  "minimum_experience_years": int,
  "job_description": str,
  "phase1_shortlist_count": int = 10,
  "phase2_shortlist_count": int = 5
}
```

### Resume

```python
{
  "resume_id": str,
  "page_number": int,
  "text_content": str,
  "candidate_name": str,
  "email": str,
  "phone": str,
  "skills": List[str],
  "experience_years": int
}
```

### ShortlistedCandidate

```python
{
  "resume_id": str,
  "candidate_name": str,
  "email": str,
  "phone": str,
  "skills": List[str],
  "experience_years": int,
  "confidence_score": int,
  "ai_summary": str,
  "cover_letter": str
}
```

### JobStatus

```python
{
  "job_id": str,
  "job_title": str,
  "total_resumes": int,
  "resumes_in_review": int,
  "phase1_completed": int,
  "phase2_completed": int,
  "shortlisted_count": int,
  "status": str,
  "created_at": datetime
}
```

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input or missing data |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server-side error |

### Common Errors

**Job Not Found:**
```json
{
  "detail": "Job not found"
}
```

**No Resumes Uploaded:**
```json
{
  "detail": "No resumes uploaded for this job"
}
```

**File Processing Error:**
```json
{
  "detail": "Error processing file: [error details]"
}
```

---

## Usage Examples

### Complete Workflow

#### 1. Create a Job

```bash
curl -X POST "http://localhost:8000/api/jobs/create" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Senior Full Stack Developer",
    "required_skills": ["React", "Node.js", "Python"],
    "minimum_experience_years": 5,
    "job_description": "Looking for an experienced developer...",
    "phase1_shortlist_count": 10,
    "phase2_shortlist_count": 5
  }'
```

Response:
```json
{
  "job_id": "abc-123-def",
  "message": "Job created successfully",
  "status": "pending"
}
```

#### 2. Upload Resumes

```bash
curl -X POST "http://localhost:8000/api/jobs/abc-123-def/upload-resumes" \
  -F "file=@resumes.pdf"
```

#### 3. Start Shortlisting

```bash
curl -X POST "http://localhost:8000/api/jobs/abc-123-def/start-shortlisting"
```

#### 4. Poll Status (repeat until completed)

```bash
curl "http://localhost:8000/api/jobs/abc-123-def/status"
```

#### 5. Get Shortlisted Candidates

```bash
curl "http://localhost:8000/api/jobs/abc-123-def/shortlisted"
```

---

## Configuration

The API can be configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| UPLOAD_DIR | ./uploads | Directory for uploaded PDF files |
| RESUME_DIR | ./resumes | Directory for extracted resume pages |
| OLLAMA_BASE_URL | http://localhost:11434 | Ollama API endpoint |
| OLLAMA_MODEL | ministral-3:3b | LLM model to use |

---

## Notes

- All timestamps are in ISO 8601 format
- Job IDs are UUIDs generated by the server
- Resume processing is asynchronous - use status endpoint for updates
- In-memory storage is used (data lost on restart)
- For production, use a persistent database
- CORS is enabled for localhost:3000 and localhost:5173

---

## Support

For issues or questions:
- Check the [README](README.md) for setup instructions
- Review [ARCHITECTURE](ARCHITECTURE.md) for system design
- See [TROUBLESHOOTING](README.md#-troubleshooting) in README

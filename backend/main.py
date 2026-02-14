from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import os
import uuid
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from models import JobPosting, JobStatus, ShortlistResponse
from resume_parser import ResumeParser
from phase1_shortlister import Phase1Shortlister
from phase2_shortlister import Phase2Shortlister
from mcp_tools import MCPResumeTools

# Initialize FastAPI
app = FastAPI(title="Resume Shortlister AI", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
RESUME_DIR = os.getenv("RESUME_DIR", "./resumes")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "ministral-3:3b")

# Create directories
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESUME_DIR, exist_ok=True)

# Initialize components
resume_parser = ResumeParser(UPLOAD_DIR, RESUME_DIR)
phase1_shortlister = Phase1Shortlister()
phase2_shortlister = Phase2Shortlister(OLLAMA_BASE_URL, OLLAMA_MODEL)
mcp_tools = MCPResumeTools()

# Print configuration on startup
print(f"🚀 Resume Shortlister AI Starting...")
print(f"   Ollama URL: {OLLAMA_BASE_URL}")
print(f"   Ollama Model: {OLLAMA_MODEL}")
print(f"   Upload Dir: {UPLOAD_DIR}")
print(f"   Resume Dir: {RESUME_DIR}")

# In-memory storage (in production, use a database)
jobs_db: Dict[str, Dict[str, Any]] = {}
resumes_db: Dict[str, List[Any]] = {}


@app.get("/")
async def root():
    return {"message": "Resume Shortlister AI API", "status": "running"}


@app.post("/api/jobs/create")
async def create_job(job: JobPosting, background_tasks: BackgroundTasks):
    """Create a new job posting"""

    job_id = str(uuid.uuid4())

    jobs_db[job_id] = {
        "id": job_id,
        "job_posting": job.model_dump(),
        "total_resumes": 0,
        "resumes_in_review": 0,
        "phase1_completed": 0,
        "phase2_completed": 0,
        "shortlisted_count": 0,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "phase1_results": [],
        "phase2_results": [],
        "shortlisted": []
    }

    resumes_db[job_id] = []

    return {
        "job_id": job_id,
        "message": "Job created successfully",
        "status": "pending"
    }


@app.post("/api/jobs/{job_id}/upload-resumes")
async def upload_resumes(job_id: str, file: UploadFile = File(...)):
    """Upload a PDF containing multiple resumes"""

    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")

    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Extract resumes from PDF
        resumes = resume_parser.extract_resumes_from_pdf(file_path)

        # Store resumes
        resumes_db[job_id].extend(resumes)

        # Update job status
        jobs_db[job_id]["total_resumes"] = len(resumes_db[job_id])
        jobs_db[job_id]["resumes_in_review"] = len(resumes_db[job_id])
        jobs_db[job_id]["status"] = "uploaded"

        return {
            "message": f"Uploaded and processed {len(resumes)} resumes",
            "total_resumes": jobs_db[job_id]["total_resumes"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/api/jobs/{job_id}/start-shortlisting")
async def start_shortlisting(job_id: str, background_tasks: BackgroundTasks):
    """Start the two-phase shortlisting process"""

    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")

    if not resumes_db.get(job_id):
        raise HTTPException(status_code=400, detail="No resumes uploaded for this job")

    # Start shortlisting in background
    background_tasks.add_task(run_shortlisting_process, job_id)

    jobs_db[job_id]["status"] = "processing"

    return {
        "message": "Shortlisting process started",
        "status": "processing"
    }


async def run_shortlisting_process(job_id: str):
    """Run the complete two-phase shortlisting process"""

    try:
        job_data = jobs_db[job_id]
        job_posting = JobPosting(**job_data["job_posting"])
        resumes = resumes_db[job_id]

        # Phase 1: Keyword and experience-based shortlisting
        jobs_db[job_id]["status"] = "phase1"

        phase1_results = phase1_shortlister.shortlist(
            resumes,
            job_posting,
            job_posting.phase1_shortlist_count
        )

        jobs_db[job_id]["phase1_results"] = phase1_results
        jobs_db[job_id]["phase1_completed"] = len(phase1_results)
        jobs_db[job_id]["resumes_in_review"] = len(phase1_results)

        # Phase 2: LLM-based comprehensive review
        jobs_db[job_id]["status"] = "phase2"

        phase2_response = await phase2_shortlister.shortlist(
            phase1_results,
            job_posting,
            job_posting.phase2_shortlist_count
        )

        jobs_db[job_id]["phase2_results"] = phase2_response.shortlisted
        jobs_db[job_id]["phase2_completed"] = len(phase2_response.shortlisted)
        jobs_db[job_id]["shortlisted"] = [
            candidate.model_dump() for candidate in phase2_response.shortlisted
        ]
        jobs_db[job_id]["shortlisted_count"] = len(phase2_response.shortlisted)
        jobs_db[job_id]["status"] = "completed"
        jobs_db[job_id]["resumes_in_review"] = 0

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in shortlisting process: {e}")
        print(error_details)
        jobs_db[job_id]["status"] = "error"
        jobs_db[job_id]["error"] = str(e)
        jobs_db[job_id]["error_details"] = error_details


@app.get("/api/jobs/{job_id}/status")
async def get_job_status(job_id: str):
    """Get the current status of a job"""

    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")

    job_data = jobs_db[job_id]

    return JobStatus(
        job_id=job_id,
        job_title=job_data["job_posting"]["job_title"],
        total_resumes=job_data["total_resumes"],
        resumes_in_review=job_data["resumes_in_review"],
        phase1_completed=job_data["phase1_completed"],
        phase2_completed=job_data["phase2_completed"],
        shortlisted_count=job_data["shortlisted_count"],
        status=job_data["status"],
        created_at=datetime.fromisoformat(job_data["created_at"])
    )


@app.get("/api/jobs/{job_id}/shortlisted")
async def get_shortlisted_candidates(job_id: str):
    """Get the final shortlisted candidates"""

    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")

    job_data = jobs_db[job_id]

    return {
        "job_id": job_id,
        "job_title": job_data["job_posting"]["job_title"],
        "status": job_data["status"],
        "shortlisted": job_data.get("shortlisted", [])
    }


@app.get("/api/jobs")
async def list_jobs():
    """List all jobs"""

    jobs = []
    for job_id, job_data in jobs_db.items():
        jobs.append({
            "job_id": job_id,
            "job_title": job_data["job_posting"]["job_title"],
            "status": job_data["status"],
            "total_resumes": job_data["total_resumes"],
            "shortlisted_count": job_data["shortlisted_count"],
            "created_at": job_data["created_at"]
        })

    return {"jobs": jobs}


@app.get("/api/mcp/tools")
async def get_mcp_tools():
    """Get MCP tools definition"""
    return {"tools": mcp_tools.get_tools_definition()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

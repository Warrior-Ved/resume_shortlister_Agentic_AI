"""
Test the Resume Shortlister API
Run this after starting the backend server
"""

import requests
import json
import time

API_BASE = "http://localhost:8000/api"

def test_api():
    print("=" * 60)
    print("Testing Resume Shortlister API")
    print("=" * 60)

    # 1. Test root endpoint
    print("\n1. Testing root endpoint...")
    response = requests.get("http://localhost:8000/")
    print(f"Response: {response.json()}")

    # 2. Create job posting
    print("\n2. Creating job posting...")
    job_data = {
        "job_title": "Senior Python Developer",
        "description": "Looking for an experienced Python developer with ML expertise",
        "required_tech_stack": ["Python", "Machine Learning", "FastAPI", "Docker"],
        "minimum_experience": 3,
        "hiring_slots": 2,
        "phase1_shortlist_count": 3,
        "phase2_shortlist_count": 2
    }

    response = requests.post(f"{API_BASE}/jobs/create", json=job_data)
    job = response.json()
    job_id = job["job_id"]
    print(f"Job created: {job_id}")

    # 3. Check job status
    print("\n3. Checking job status...")
    response = requests.get(f"{API_BASE}/jobs/{job_id}/status")
    print(f"Status: {response.json()}")

    # 4. Instructions for manual testing
    print("\n" + "=" * 60)
    print("Manual Testing Instructions:")
    print("=" * 60)
    print(f"Job ID: {job_id}")
    print("\nNext steps:")
    print("1. Create sample resumes:")
    print("   python create_sample_resumes.py")
    print("\n2. Upload sample resumes via API:")
    print(f"   curl -X POST http://localhost:8000/api/jobs/{job_id}/upload-resumes \\")
    print(f'        -F "file=@sample_resumes.pdf"')
    print("\n3. Or use the web interface at http://localhost:3000")

    # 5. List all jobs
    print("\n4. Listing all jobs...")
    response = requests.get(f"{API_BASE}/jobs")
    print(f"Jobs: {json.dumps(response.json(), indent=2)}")

    # 6. Get MCP tools
    print("\n5. Getting MCP tools...")
    response = requests.get(f"{API_BASE}/mcp/tools")
    print(f"MCP Tools: {json.dumps(response.json(), indent=2)[:500]}...")

    print("\n" + "=" * 60)
    print("API Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend server!")
        print("Please make sure the backend is running:")
        print("  cd backend")
        print("  .venv\\Scripts\\activate")
        print("  python main.py")
    except Exception as e:
        print(f"ERROR: {e}")

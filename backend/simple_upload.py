"""
SIMPLE RESUME UPLOADER - NO COMMAND LINE PARSING
Just change the variables below and run: python simple_upload.py
"""

import os
import time
import requests

# ============================================================================
# 👇 CHANGE THESE VARIABLES - THAT'S ALL YOU NEED TO DO!
# ============================================================================

# PDF Configuration
PDF_PATH = "F:/projects/ruya_AI_hackathon/data/full_stack_resumes.pdf"  # Change this to your PDF path

# Job Configuration
JOB_TITLE = "Software Engineer"
JOB_DESCRIPTION = "Looking for experienced software engineer"
REQUIRED_SKILLS = ["Python", "JavaScript", "React", "Docker"]  # Add your required skills
MINIMUM_EXPERIENCE = 3  # Minimum years of experience (use 0 for entry-level/any experience)
HIRING_SLOTS = 2  # Number of positions to fill

# Shortlisting Configuration
PHASE1_SHORTLIST_COUNT = 10  # How many to shortlist in phase 1
PHASE2_SHORTLIST_COUNT = 5   # Final shortlist count

# API Configuration (usually no need to change)
API_BASE = "http://localhost:8000/api"

# ============================================================================
# DON'T CHANGE ANYTHING BELOW THIS LINE
# ============================================================================

class SimpleUploader:
    def __init__(self):
        self.job_id = None

    def check_backend(self):
        """Check if backend is running"""
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is running")
                return True
        except:
            print("❌ Backend is not running!")
            print("   Please start: cd backend && .venv\\Scripts\\activate && python main.py")
            return False

    def create_job(self):
        """Create job posting"""
        print("\n📝 Creating job posting...")
        print(f"   Title: {JOB_TITLE}")
        print(f"   Skills: {', '.join(REQUIRED_SKILLS)}")
        print(f"   Experience: {MINIMUM_EXPERIENCE} years")

        job_data = {
            'job_title': JOB_TITLE,
            'description': JOB_DESCRIPTION,
            'required_tech_stack': REQUIRED_SKILLS,
            'minimum_experience': MINIMUM_EXPERIENCE,
            'hiring_slots': HIRING_SLOTS,
            'phase1_shortlist_count': PHASE1_SHORTLIST_COUNT,
            'phase2_shortlist_count': PHASE2_SHORTLIST_COUNT
        }

        try:
            response = requests.post(f"{API_BASE}/jobs/create", json=job_data)
            response.raise_for_status()
            result = response.json()
            self.job_id = result["job_id"]
            print(f"✅ Job created! ID: {self.job_id}")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def upload_pdf(self):
        """Upload the PDF"""
        print(f"\n📤 Uploading: {PDF_PATH}")

        if not os.path.exists(PDF_PATH):
            print(f"❌ File not found: {PDF_PATH}")
            print("   Please check the PDF_PATH variable!")
            return False

        try:
            with open(PDF_PATH, 'rb') as f:
                files = {'file': (os.path.basename(PDF_PATH), f, 'application/pdf')}
                response = requests.post(
                    f"{API_BASE}/jobs/{self.job_id}/upload-resumes",
                    files=files
                )
                response.raise_for_status()
                result = response.json()
                print(f"✅ Uploaded! Processed {result['total_resumes']} resumes")
                return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def start_shortlisting(self):
        """Start the shortlisting process"""
        print("\n🚀 Starting shortlisting process...")

        try:
            response = requests.post(f"{API_BASE}/jobs/{self.job_id}/start-shortlisting")
            response.raise_for_status()
            print("✅ Shortlisting started!")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def monitor_progress(self):
        """Monitor progress"""
        print("\n⏳ Monitoring progress (press Ctrl+C to stop)...\n")

        previous_status = None

        try:
            while True:
                response = requests.get(f"{API_BASE}/jobs/{self.job_id}/status")
                response.raise_for_status()
                status = response.json()

                current_status = status['status']

                if current_status != previous_status:
                    print(f"\n📊 Status: {current_status.upper()}")
                    print(f"   Total: {status['total_resumes']} | Phase1: {status['phase1_completed']} | Phase2: {status['phase2_completed']} | Shortlisted: {status['shortlisted_count']}")
                    previous_status = current_status

                if current_status == 'completed':
                    print("\n✅ Completed!")
                    break
                elif current_status == 'error':
                    print("\n❌ Error occurred!")
                    break

                time.sleep(3)

        except KeyboardInterrupt:
            print("\n⏸️  Monitoring stopped")

    def show_results(self):
        """Display results"""
        print("\n📋 Fetching results...")

        try:
            response = requests.get(f"{API_BASE}/jobs/{self.job_id}/shortlisted")
            response.raise_for_status()
            result = response.json()

            candidates = result.get('shortlisted', [])

            if not candidates:
                print("❌ No candidates shortlisted")
                return

            print(f"\n✨ {len(candidates)} Candidates Shortlisted!\n")
            print("=" * 80)

            for i, candidate in enumerate(candidates, 1):
                print(f"\n{i}. {candidate['name']}")
                print(f"   📧 Email: {candidate.get('email', 'N/A')}")
                print(f"   🎯 Confidence: {candidate['confidence']*100:.1f}%")
                print(f"   💼 Experience: {candidate.get('experience', 'N/A')} years")
                print(f"   🛠️  Skills: {', '.join(candidate.get('skills', [])[:5])}")

                if candidate.get('cover_letter'):
                    preview = candidate['cover_letter'][:150]
                    print(f"   💬 Cover Letter: {preview}...")

                print("-" * 80)

            # Save to file
            import json
            output_file = f"shortlisted_{self.job_id}.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to: {output_file}")

        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    print("\n" + "="*80)
    print("🎯 SIMPLE RESUME UPLOADER")
    print("="*80)

    print("\n📋 Configuration:")
    print(f"   PDF: {PDF_PATH}")
    print(f"   Job: {JOB_TITLE}")
    print(f"   Skills: {', '.join(REQUIRED_SKILLS)}")
    print(f"   Experience: {MINIMUM_EXPERIENCE} years")
    print(f"   Phase 1 Count: {PHASE1_SHORTLIST_COUNT}")
    print(f"   Phase 2 Count: {PHASE2_SHORTLIST_COUNT}")

    uploader = SimpleUploader()

    # Run the workflow
    if not uploader.check_backend():
        return

    if not uploader.create_job():
        return

    if not uploader.upload_pdf():
        return

    if not uploader.start_shortlisting():
        return

    uploader.monitor_progress()
    uploader.show_results()

    print("\n" + "="*80)
    print("✅ DONE!")
    print("="*80)
    print(f"\n💡 View in browser: http://localhost:3000")
    print(f"💡 Job ID: {uploader.job_id}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

"""
Automated Resume Upload and Shortlisting Script

This script allows you to upload resumes directly from your data folder
and automatically start the shortlisting process.

Usage:
    python upload_and_process.py --pdf "resumes.pdf" --job-title "Software Engineer" --skills "Python,React,Docker" --experience 3

Or use interactive mode:
    python upload_and_process.py --interactive
"""

import os
import sys
import time
import argparse
import requests
from pathlib import Path


class ResumeProcessor:
    def __init__(self, api_base="http://localhost:8000/api"):
        self.api_base = api_base
        self.job_id = None

    def check_backend(self):
        """Check if backend is running"""
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is running")
                return True
        except requests.exceptions.ConnectionError:
            print("❌ Backend is not running!")
            print("   Please start the backend first:")
            print("   cd backend && .venv\\Scripts\\activate && python main.py")
            return False
        except Exception as e:
            print(f"❌ Error connecting to backend: {e}")
            return False

    def create_job(self, job_data):
        """Create a new job posting"""
        print("\n📝 Creating job posting...")
        print(f"   Title: {job_data['job_title']}")
        print(f"   Required Skills: {', '.join(job_data['required_tech_stack'])}")
        print(f"   Min Experience: {job_data['minimum_experience']} years")

        try:
            response = requests.post(
                f"{self.api_base}/jobs/create",
                json=job_data
            )
            response.raise_for_status()
            result = response.json()
            self.job_id = result["job_id"]
            print(f"✅ Job created successfully! ID: {self.job_id}")
            return True
        except Exception as e:
            print(f"❌ Error creating job: {e}")
            return False

    def upload_resumes(self, pdf_path):
        """Upload resume PDF"""
        print(f"\n📤 Uploading resumes from: {pdf_path}")

        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return False

        try:
            with open(pdf_path, 'rb') as f:
                files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
                response = requests.post(
                    f"{self.api_base}/jobs/{self.job_id}/upload-resumes",
                    files=files
                )
                response.raise_for_status()
                result = response.json()
                print(f"✅ Uploaded and processed {result['total_resumes']} resumes!")
                return True
        except Exception as e:
            print(f"❌ Error uploading resumes: {e}")
            return False

    def start_shortlisting(self):
        """Start the shortlisting process"""
        print("\n🚀 Starting shortlisting process...")

        try:
            response = requests.post(
                f"{self.api_base}/jobs/{self.job_id}/start-shortlisting"
            )
            response.raise_for_status()
            print("✅ Shortlisting process started!")
            return True
        except Exception as e:
            print(f"❌ Error starting shortlisting: {e}")
            return False

    def monitor_progress(self):
        """Monitor the shortlisting progress"""
        print("\n⏳ Monitoring progress (updating every 3 seconds)...")
        print("   Press Ctrl+C to stop monitoring\n")

        previous_status = None

        try:
            while True:
                response = requests.get(f"{self.api_base}/jobs/{self.job_id}/status")
                response.raise_for_status()
                status = response.json()

                current_status = status['status']

                # Only print if status changed
                if current_status != previous_status:
                    print(f"\n📊 Status: {current_status.upper()}")
                    print(f"   Total Resumes: {status['total_resumes']}")
                    print(f"   Phase 1 Completed: {status['phase1_completed']}")
                    print(f"   Phase 2 Completed: {status['phase2_completed']}")
                    print(f"   Final Shortlisted: {status['shortlisted_count']}")
                    previous_status = current_status

                if current_status == 'completed':
                    print("\n✅ Shortlisting completed!")
                    break
                elif current_status == 'error':
                    print("\n❌ Shortlisting process encountered an error!")
                    break

                time.sleep(3)

        except KeyboardInterrupt:
            print("\n\n⏸️  Monitoring stopped (process continues in background)")
        except Exception as e:
            print(f"\n❌ Error monitoring progress: {e}")

    def get_results(self):
        """Get and display shortlisted candidates"""
        print("\n📋 Fetching results...")

        try:
            response = requests.get(f"{self.api_base}/jobs/{self.job_id}/shortlisted")
            response.raise_for_status()
            result = response.json()

            candidates = result.get('shortlisted', [])

            if not candidates:
                print("❌ No candidates were shortlisted")
                return

            print(f"\n✨ {len(candidates)} Candidates Shortlisted!\n")
            print("=" * 80)

            for i, candidate in enumerate(candidates, 1):
                print(f"\n{i}. {candidate['name']}")
                print(f"   📧 Email: {candidate.get('email', 'N/A')}")
                print(f"   🎯 Confidence: {candidate['confidence']*100:.1f}%")
                print(f"   💼 Experience: {candidate.get('experience', 'N/A')} years")
                print(f"   🛠️  Skills: {', '.join(candidate.get('skills', [])[:5])}")
                if len(candidate.get('skills', [])) > 5:
                    print(f"             (+{len(candidate['skills'])-5} more)")
                print(f"   📄 CV: {candidate['cv_path']}")

                if candidate.get('cover_letter'):
                    print(f"\n   💬 Cover Letter Preview:")
                    preview = candidate['cover_letter'][:150]
                    print(f"      {preview}{'...' if len(candidate['cover_letter']) > 150 else ''}")

                print("-" * 80)

            # Save to file
            output_file = f"shortlisted_{self.job_id}.json"
            import json
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to: {output_file}")

        except Exception as e:
            print(f"❌ Error fetching results: {e}")


def interactive_mode():
    """Interactive mode for user input"""
    print("\n" + "="*80)
    print("🎯 RESUME SHORTLISTER - INTERACTIVE MODE")
    print("="*80)

    # Get PDF path
    print("\n📁 Step 1: Resume PDF Location")
    print("   Enter the path to your PDF file (or just filename if in data folder)")
    pdf_input = input("   PDF file: ").strip()

    # Check common locations
    pdf_path = None
    locations_to_check = [
        pdf_input,
        os.path.join("data", pdf_input),
        os.path.join("..", "data", pdf_input),
        os.path.join("backend", "data", pdf_input),
    ]

    for location in locations_to_check:
        if os.path.exists(location):
            pdf_path = location
            break

    if not pdf_path:
        print(f"❌ PDF file not found in common locations")
        print(f"   Tried: {locations_to_check}")
        return None

    print(f"   ✅ Found: {pdf_path}")

    # Get job details
    print("\n💼 Step 2: Job Details")
    job_title = input("   Job Title: ").strip() or "Software Engineer"
    description = input("   Job Description (optional): ").strip() or f"Looking for {job_title}"

    print("\n🛠️  Step 3: Required Skills")
    print("   Enter skills separated by commas (e.g., Python, React, Docker)")
    skills_input = input("   Skills: ").strip()
    skills = [s.strip() for s in skills_input.split(",") if s.strip()]

    if not skills:
        skills = ["Python"]  # Default

    print("\n⏰ Step 4: Experience Requirements")
    min_exp = input("   Minimum years of experience (default 2): ").strip()
    min_exp = int(min_exp) if min_exp.isdigit() else 2

    hiring_slots = input("   Number of hiring slots (default 1): ").strip()
    hiring_slots = int(hiring_slots) if hiring_slots.isdigit() else 1

    print("\n🎯 Step 5: Shortlisting Configuration")
    phase1_count = input("   Phase 1 shortlist count (default 10): ").strip()
    phase1_count = int(phase1_count) if phase1_count.isdigit() else 10

    phase2_count = input("   Phase 2 shortlist count (default 5): ").strip()
    phase2_count = int(phase2_count) if phase2_count.isdigit() else 5

    return {
        'pdf_path': pdf_path,
        'job_data': {
            'job_title': job_title,
            'description': description,
            'required_tech_stack': skills,
            'minimum_experience': min_exp,
            'hiring_slots': hiring_slots,
            'phase1_shortlist_count': phase1_count,
            'phase2_shortlist_count': phase2_count
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='Upload and process resumes automatically',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Interactive mode (easiest)
    python upload_and_process.py --interactive
    
    # Command line mode
    python upload_and_process.py --pdf "data/resumes.pdf" --job-title "Python Developer" --skills "Python,Django,FastAPI" --experience 3
    
    # Quick mode with defaults
    python upload_and_process.py --pdf "resumes.pdf"
        """
    )

    parser.add_argument('--interactive', '-i', action='store_true',
                      help='Run in interactive mode')
    parser.add_argument('--pdf', type=str,
                      help='Path to PDF file containing resumes')
    parser.add_argument('--job-title', type=str, default='Software Engineer',
                      help='Job title (default: Software Engineer)')
    parser.add_argument('--description', type=str, default='',
                      help='Job description')
    parser.add_argument('--skills', type=str, default='Python,JavaScript,React',
                      help='Required skills (comma-separated)')
    parser.add_argument('--experience', type=int, default=2,
                      help='Minimum years of experience (default: 2)')
    parser.add_argument('--hiring-slots', type=int, default=1,
                      help='Number of hiring slots (default: 1)')
    parser.add_argument('--phase1-count', type=int, default=10,
                      help='Phase 1 shortlist count (default: 10)')
    parser.add_argument('--phase2-count', type=int, default=5,
                      help='Phase 2 shortlist count (default: 5)')
    parser.add_argument('--no-monitor', action='store_true',
                      help='Skip progress monitoring')

    args = parser.parse_args()

    print("\n" + "="*80)
    print("🎯 RESUME SHORTLISTER - AUTOMATED UPLOAD & PROCESSING")
    print("="*80)

    # Create processor
    processor = ResumeProcessor()

    # Check backend
    if not processor.check_backend():
        return 1

    # Get configuration
    if args.interactive:
        config = interactive_mode()
        if not config:
            return 1
        pdf_path = config['pdf_path']
        job_data = config['job_data']
    else:
        if not args.pdf:
            print("\n❌ Error: --pdf argument is required (or use --interactive)")
            parser.print_help()
            return 1

        # Check PDF path
        pdf_path = None
        locations_to_check = [
            args.pdf,
            os.path.join("data", args.pdf),
            os.path.join("..", "data", args.pdf),
            os.path.join("backend", "data", args.pdf),
        ]

        for location in locations_to_check:
            if os.path.exists(location):
                pdf_path = location
                break

        if not pdf_path:
            print(f"\n❌ PDF file not found: {args.pdf}")
            print(f"   Tried locations: {locations_to_check}")
            return 1

        job_data = {
            'job_title': args.job_title,
            'description': args.description or f"Looking for {args.job_title}",
            'required_tech_stack': [s.strip() for s in args.skills.split(',')],
            'minimum_experience': args.experience,
            'hiring_slots': args.hiring_slots,
            'phase1_shortlist_count': args.phase1_count,
            'phase2_shortlist_count': args.phase2_count
        }

    # Execute workflow
    print("\n" + "="*80)
    print("🚀 STARTING AUTOMATED WORKFLOW")
    print("="*80)

    # Step 1: Create job
    if not processor.create_job(job_data):
        return 1

    # Step 2: Upload resumes
    if not processor.upload_resumes(pdf_path):
        return 1

    # Step 3: Start shortlisting
    if not processor.start_shortlisting():
        return 1

    # Step 4: Monitor progress
    if not args.no_monitor:
        processor.monitor_progress()
    else:
        print("\n⏭️  Skipping progress monitoring")
        print(f"   Check status at: http://localhost:3000")
        print(f"   Or run: python test_api.py")

    # Step 5: Get results
    processor.get_results()

    print("\n" + "="*80)
    print("✅ WORKFLOW COMPLETED SUCCESSFULLY!")
    print("="*80)
    print(f"\n💡 View full results in the web interface:")
    print(f"   http://localhost:3000")
    print(f"\n💡 Job ID: {processor.job_id}")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏸️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

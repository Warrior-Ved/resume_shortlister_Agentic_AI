import json
from typing import List, Dict, Any
from models import Resume, JobPosting, ShortlistedCandidate, ShortlistResponse
import httpx


class Phase2Shortlister:
    """
    Phase 2: LLM-based comprehensive review using Ollama
    Uses MCP tools for resume analysis
    """

    def __init__(self, ollama_url: str, model_name: str):
        self.ollama_url = ollama_url
        self.model_name = model_name
        self.client = httpx.AsyncClient(timeout=120.0)

    async def shortlist(
        self,
        resumes: List[Resume],
        job_posting: JobPosting,
        target_count: int
    ) -> ShortlistResponse:
        """
        Use LLM to comprehensively review resumes and shortlist candidates
        """

        shortlisted_candidates = []

        print(f"Phase 2: Starting LLM review of {len(resumes)} candidates...")

        for i, resume in enumerate(resumes, 1):
            try:
                print(f"  [{i}/{len(resumes)}] Reviewing {resume.name}...")
                result = await self.review_resume(resume, job_posting)
                if result:
                    shortlisted_candidates.append(result)
                    print(f"    ✅ Shortlisted with confidence {result.confidence:.2f}")
                else:
                    print(f"    ❌ Not suitable")
            except Exception as e:
                import traceback
                print(f"    ⚠️ Error reviewing {resume.name}: {e}")
                print(f"    Traceback: {traceback.format_exc()}")
                continue

        print(f"Phase 2: Completed. {len(shortlisted_candidates)} candidates shortlisted.")

        # Sort by confidence score
        shortlisted_candidates.sort(key=lambda x: x.confidence, reverse=True)

        # Take top N candidates
        final_shortlist = shortlisted_candidates[:target_count]

        return ShortlistResponse(shortlisted=final_shortlist)

    async def review_resume(
        self,
        resume: Resume,
        job_posting: JobPosting
    ) -> ShortlistedCandidate:
        """
        Review a single resume using LLM
        """

        prompt = self.create_review_prompt(resume, job_posting)

        # Call Ollama API
        response = await self.call_ollama(prompt)

        # Parse LLM response
        result = self.parse_llm_response(response, resume)

        return result

    def create_review_prompt(self, resume: Resume, job_posting: JobPosting) -> str:
        """
        Create a comprehensive prompt for LLM to review the resume
        """

        prompt = f"""You are an expert HR recruiter. Review the following resume against the job requirements and provide a detailed assessment.

Job Title: {job_posting.job_title}
Job Description: {job_posting.description}
Required Tech Stack: {', '.join(job_posting.required_tech_stack)}
Minimum Experience: {job_posting.minimum_experience} years

Candidate Resume:
Name: {resume.name}
Email: {resume.email or 'Not provided'}
Skills: {', '.join(resume.skills)}
Experience: {resume.experience if resume.experience is not None else 'Not specified'} years
Resume Content:
{resume.text_content[:1500]}

Based on this information, provide your assessment in the following JSON format:
{{
    "is_suitable": true or false,
    "confidence": 0.0 to 1.0 (confidence score),
    "reasoning": "Brief explanation of your decision",
    "cover_letter": "A personalized cover letter (2-3 sentences) that the candidate could use for this position, highlighting their relevant experience and skills"
}}

Respond ONLY with the JSON object, no additional text."""

        return prompt

    async def call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API with the prompt
        """

        try:
            print(f"      Calling Ollama API ({self.model_name})...")
            response = await self.client.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                }
            )

            response.raise_for_status()
            result = response.json()

            llm_response = result.get("response", "")
            print(f"      Ollama responded with {len(llm_response)} characters")

            return llm_response

        except Exception as e:
            import traceback
            print(f"      ❌ Error calling Ollama: {e}")
            print(f"      Traceback: {traceback.format_exc()}")
            raise

    def parse_llm_response(
        self,
        llm_response: str,
        resume: Resume
    ) -> ShortlistedCandidate:
        """
        Parse LLM response and create ShortlistedCandidate object
        """

        try:
            # Parse JSON response
            print(f"      Parsing LLM response...")
            data = json.loads(llm_response)

            # Check if candidate is suitable
            is_suitable = data.get("is_suitable", False)
            confidence = float(data.get("confidence", 0.5))

            print(f"      LLM Decision: is_suitable={is_suitable}, confidence={confidence}")

            if not is_suitable:
                print(f"      Candidate not suitable according to LLM")
                return None

            cover_letter = data.get("cover_letter", "")

            return ShortlistedCandidate(
                name=resume.name,
                confidence=confidence,
                email=resume.email,
                cv_path=resume.cv_path,
                skills=resume.skills,
                experience=resume.experience,
                cover_letter=cover_letter
            )

        except json.JSONDecodeError as e:
            print(f"      ⚠️ Error parsing LLM response: {e}")
            print(f"      Response was: {llm_response[:200]}...")

            # Fallback: create candidate with lower confidence
            print(f"      Using fallback - accepting with 0.5 confidence")
            return ShortlistedCandidate(
                name=resume.name,
                confidence=0.5,
                email=resume.email,
                cv_path=resume.cv_path,
                skills=resume.skills,
                experience=resume.experience,
                cover_letter=f"I am interested in applying for this position. With my experience in {', '.join(resume.skills[:3])}, I believe I would be a good fit for your team."
            )

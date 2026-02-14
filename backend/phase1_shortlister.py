from typing import List, Dict, Tuple
from models import Resume, JobPosting


class Phase1Shortlister:
    """
    Phase 1: Keyword-based and experience-based shortlisting
    No LLM required
    """

    def __init__(self):
        pass

    def shortlist(
        self,
        resumes: List[Resume],
        job_posting: JobPosting,
        target_count: int
    ) -> List[Resume]:
        """
        Shortlist resumes based on:
        1. Keyword matching with required tech stack
        2. Minimum experience requirement
        """

        scored_resumes = []

        for resume in resumes:
            score = self.calculate_score(resume, job_posting)
            scored_resumes.append((resume, score))

        # Sort by score (descending)
        scored_resumes.sort(key=lambda x: x[1], reverse=True)

        # Filter by minimum experience
        filtered_resumes = [
            (resume, score) for resume, score in scored_resumes
            if resume.experience is not None and resume.experience >= job_posting.minimum_experience
        ]

        # If not enough candidates meet minimum experience, include those without specified experience
        if len(filtered_resumes) < target_count:
            no_exp_resumes = [
                (resume, score) for resume, score in scored_resumes
                if resume.experience is None
            ]
            filtered_resumes.extend(no_exp_resumes)

        # Take top N candidates
        shortlisted = [resume for resume, score in filtered_resumes[:target_count]]

        return shortlisted

    def calculate_score(self, resume: Resume, job_posting: JobPosting) -> float:
        """
        Calculate match score based on:
        - Tech stack keyword matching
        - Experience level
        """
        score = 0.0

        # Keyword matching (70% weight)
        required_skills = set([skill.lower() for skill in job_posting.required_tech_stack])
        resume_skills = set([skill.lower() for skill in resume.skills])

        if required_skills:
            matched_skills = required_skills.intersection(resume_skills)
            keyword_score = len(matched_skills) / len(required_skills)
            score += keyword_score * 0.7

        # Experience matching (30% weight)
        if resume.experience is not None:
            if job_posting.minimum_experience == 0:
                # If no experience required, give full score for any experience
                score += 0.3
            elif resume.experience >= job_posting.minimum_experience:
                # Give full score if meets minimum
                experience_score = min(1.0, resume.experience / (job_posting.minimum_experience * 2))
                score += experience_score * 0.3

        return score

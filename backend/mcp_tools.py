import json
from typing import List, Dict, Any, Optional


class MCPResumeTools:
    """
    MCP (Model Context Protocol) Tools for Resume Processing
    These tools make resume data available to the LLM agent
    """

    def __init__(self):
        self.tools = self._define_tools()

    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define MCP tools for resume processing"""

        return [
            {
                "name": "get_resume_content",
                "description": "Get the full text content of a resume",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resume_id": {
                            "type": "string",
                            "description": "The unique identifier of the resume"
                        }
                    },
                    "required": ["resume_id"]
                }
            },
            {
                "name": "extract_skills",
                "description": "Extract and list all skills from a resume",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resume_id": {
                            "type": "string",
                            "description": "The unique identifier of the resume"
                        }
                    },
                    "required": ["resume_id"]
                }
            },
            {
                "name": "check_experience",
                "description": "Check the years of experience mentioned in a resume",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resume_id": {
                            "type": "string",
                            "description": "The unique identifier of the resume"
                        }
                    },
                    "required": ["resume_id"]
                }
            },
            {
                "name": "match_requirements",
                "description": "Match resume skills and experience against job requirements",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resume_id": {
                            "type": "string",
                            "description": "The unique identifier of the resume"
                        },
                        "required_skills": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of required skills for the job"
                        },
                        "min_experience": {
                            "type": "integer",
                            "description": "Minimum years of experience required"
                        }
                    },
                    "required": ["resume_id", "required_skills", "min_experience"]
                }
            }
        ]

    def get_tools_definition(self) -> List[Dict[str, Any]]:
        """Get the tools definition for MCP"""
        return self.tools

    def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        resume_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool with given parameters"""

        if tool_name == "get_resume_content":
            return self._get_resume_content(parameters, resume_data)
        elif tool_name == "extract_skills":
            return self._extract_skills(parameters, resume_data)
        elif tool_name == "check_experience":
            return self._check_experience(parameters, resume_data)
        elif tool_name == "match_requirements":
            return self._match_requirements(parameters, resume_data)
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def _get_resume_content(
        self,
        parameters: Dict[str, Any],
        resume_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get full resume content"""

        resume_id = parameters.get("resume_id")
        resume = resume_data.get(resume_id)

        if not resume:
            return {"error": "Resume not found"}

        return {
            "content": resume.get("text_content", ""),
            "name": resume.get("name", "Unknown"),
            "email": resume.get("email")
        }

    def _extract_skills(
        self,
        parameters: Dict[str, Any],
        resume_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract skills from resume"""

        resume_id = parameters.get("resume_id")
        resume = resume_data.get(resume_id)

        if not resume:
            return {"error": "Resume not found"}

        return {
            "skills": resume.get("skills", []),
            "skill_count": len(resume.get("skills", []))
        }

    def _check_experience(
        self,
        parameters: Dict[str, Any],
        resume_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check experience in resume"""

        resume_id = parameters.get("resume_id")
        resume = resume_data.get(resume_id)

        if not resume:
            return {"error": "Resume not found"}

        return {
            "experience_years": resume.get("experience"),
            "has_experience": resume.get("experience") is not None
        }

    def _match_requirements(
        self,
        parameters: Dict[str, Any],
        resume_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Match resume against job requirements"""

        resume_id = parameters.get("resume_id")
        resume = resume_data.get(resume_id)
        required_skills = parameters.get("required_skills", [])
        min_experience = parameters.get("min_experience", 0)

        if not resume:
            return {"error": "Resume not found"}

        resume_skills = set([s.lower() for s in resume.get("skills", [])])
        required_skills_set = set([s.lower() for s in required_skills])

        matched_skills = resume_skills.intersection(required_skills_set)
        missing_skills = required_skills_set - resume_skills

        experience_met = False
        if resume.get("experience") is not None:
            experience_met = resume.get("experience") >= min_experience

        match_percentage = len(matched_skills) / len(required_skills_set) if required_skills_set else 0

        return {
            "matched_skills": list(matched_skills),
            "missing_skills": list(missing_skills),
            "match_percentage": match_percentage,
            "experience_met": experience_met,
            "candidate_experience": resume.get("experience"),
            "required_experience": min_experience
        }

## Unused

from typing import List, Tuple
from dotenv import load_dotenv
from google import genai
from google.genai import errors
import os
import datetime
import json
import re
from pydantic import BaseModel, Field

load_dotenv()

API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_GENAI_API_KEY key not found in .env")

client = genai.Client(api_key=API_KEY)

class ProjectSchema(BaseModel):
    project_title: str = Field(description="A catchy title for the project")
    difficulty: str = Field(description="Beginner, Intermediate, or Advanced")
    description: str = Field(description="A 2-sentence summary of what to build")
    tech_stack: List[str] = Field(description="List of specific technologies to use")
    skills_practiced: List[str] = Field(description="List of user's current skills used in this project")
    new_skills_to_gain: List[str] = Field(description="List of new skills/knowledge this project introduces")

# return (bool, str)
def generate_ict_projects(skill_list: list[str], knowledge_list: list[str], num_projects=5) -> Tuple[bool, str]:
    prompt = f"""
    Role: You are an expert ICT Career Coach and Technical Mentor.

    Task: Suggest {num_projects} practical ICT projects for a student/professional with the following skillset:
    Skill: {skill_list}
    Knowledge: {knowledge_list}

    Objectives for the projects:
    1. Consolidate: Heavily utilize the Current Skills listed above.
    2. Expand: Introduce 1-2 new, adjacent, or advanced skills (high-demand in the industry) for each project.
    3. Context: The projects should be realistic, portfolio-worthy, and varied in domain (e.g., healthcare, finance, e-commerce, or automation).

    CRITICAL INSTRUCTION: Output valid JSON only. Do not add markdown formatting like ```json ... ```.
    The JSON must follow this exact structure:
    {{
        "projects": [
        {{
            "project_title": "string",
            "difficulty": "string",
            "description": "string",
            "tech_stack": ["string"],
            "skills_practiced": ["string"],
            "new_skills_to_gain": ["string"]
        }}
        ]
    }}
    """

    try:
        # 4. GENERATION
        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.2,
            )
        )

        if(response.text is None):
            raise ValueError("No response text received.")

        raw_text = response.text
        cleaned_json_text = re.sub(r"```json\n?|```", "", raw_text).strip()
        return (True, cleaned_json_text)
    except Exception as e:
        return (False, f"Error occurred: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Example Input: A user with basic Data Science & Web skills
    user_skill = [
        "use scripting programming",
        "use concurrent programming",
        "use object-oriented programming",
        "design computer network",
        "manage content development projects",
        "write scientific publications"
    ]
    user_knowledge = [
        "R",
        "C++",
        "Python (computer programming)",
        "ethical hacking principles",
        "JavaScript",
        "Swift (computer programming)",
        "hardware architectures",
        "Java (computer programming)",
        "TypeScript",
        "NoSQL",
        "algorithms",
        "computer science",
        "operating systems"
    ]


    status, string = generate_ict_projects(user_skill, user_knowledge)
    if(status):
        data = json.loads(string)
        projects_json = data.get("projects", [])
        print(projects_json)
        projects = [ProjectSchema(**project) for project in projects_json]
    else:
        print(string)

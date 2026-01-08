import datetime
import os
from dotenv import load_dotenv
from google import genai
import time
import json

from .datatype import *

load_dotenv()

API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
# THINKING_BUDGET = 8192
THINKING_BUDGET = 0
TEMPERATURE = 1.5
# MODEL = "gemini-2.5-flash-preview-09-2025"
MODEL = "gemma-3-27b-it"
# MODEL = "gemini-2.5-pro"

system_instruction = '''
You are a project advisor AI. Your task is to analyze the provided IT job information and the student's skill set, and suggest relevant projects that can help the student bridge the gap between their current skills and those required for the job.
'''

prompt = '''
Given the job information: 
{
    "name": "ICT system developer",
    "description": "ICT system developers maintain, audit and improve organisational support systems. They use existing or new technologies to meet particular needs. They test both hardware and software system components, diagnose and resolve system faults.",
    "other_name": [
        "ICT system developers",
        "ICT systems developer",
        "systems programmer",
        "system developer",
        "component developer",
        "system software developer",
        "chief ICT system developer",
        "ICT systems developers",
        "systems developer",
        "IT system developer"
    ],
    "essential_knowledge": [
        "digital systems",
        "computer programming",
        "tools for software configuration management",
        "ICT debugging tools",
        "ICT system programming",
        "ICT system integration",
        "integrated development environment software"
    ],
    "optional_knowledge": [
        "Apache Maven",
        "core banking software",
        "object-oriented modelling",
        "defence standard procedures",
        "Internet of Things",
        "Ansible",
        "JavaScript",
        "R",
        "software anomalies",
        "system design",
        "Prolog (computer programming)",
        "AJAX",
        "Lisp",
        "Perl",
        "OpenEdge Advanced Business Language",
        "COBOL",
        "blockchain openness",
        "Scala",
        "Visual Basic",
        "Xcode",
        "Objective-C",
        "ASP.NET",
        "Assembly (computer programming)",
        "STAF",
        "SAP R3",
        "C#",
        "Salt (tools for software configuration management)",
        "Python (computer programming)",
        "World Wide Web Consortium standards",
        "Swift (computer programming)",
        "Groovy",
        "smart contract",
        "TypeScript",
        "ML (computer programming)",
        "VBScript",
        "blockchain platforms",
        "APL",
        "Pascal (computer programming)",
        "systems theory",
        "ICT security legislation",
        "attack vectors",
        "Eclipse (integrated development environment software)",
        "SAS language",
        "Puppet (tools for software configuration management)",
        "KDevelop",
        "C++",
        "Jenkins (tools for software configuration management)",
        "Haskell",
        "Common Lisp",
        "MATLAB",
        "Java (computer programming)",
        "security engineering",
        "Ruby (computer programming)",
        "Scratch (computer programming)",
        "PHP",
        "Microsoft Visual C++"
    ]
},

Given the student knowledge set:
{
    "computer programming",
    "web programming",
    "JavaScript",
    "C++",
    "PHP",
    "MATLAB",
    "deep learning",
    "Xcode",
    "algorithms",
    "artificial neural networks",
    "Interface Builder usage",
    "SQL",
    "JavaScript frameworks",
    "Python (computer programming)",
    "Pascal (computer programming)"
}

You are a project advisor AI. Your task is to analyze the provided IT job information and the student's skill set, and suggest relevant projects that can help the student bridge the gap between their current skills and those required for the job.
Suggest 5 projects that would help the student bridge the gap between their current knowledge and those required for the job. Priortize essential knowledge first, then optional knowledge that is closely related to the student's existing skills.
Do not make up knowledges that are not in the provided job information.
Output in JSON format. Only output like a JSON file. Do not include any Markdown elements or code blocks. (for example ```json ... ```).

Output format:
{
  "project_suggestions": [
    {
      "title": "...",
      "description": "...",
      "knowledge_gain": [
        "a",
        "b",
        ...
      ],
      "reasoning": "..."
    },
    ...
  ]
}
'''

client = genai.Client(api_key=API_KEY)

print("Available Models:")
for model in client.models.list():
    print(model.name)

def call_gemma(prompt: str, temperature: float) -> bool:
    model = "gemma-3-27b-it"
    print("Running gemma-3-27b-it...")
    start_time = time.perf_counter()
    response = client.models.generate_content(
        model=model, 
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            temperature=temperature,
        ),
    )
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    try:
        filename: str = f"ailog_projectprompt_{datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}_{model}_temp{temperature}.txt"
        with open(filename, 'w') as file:
            file.write(response.text)
        print(f"Data written. Task took {execution_time:.2f} seconds.")
    except IOError as e:
        print(f"An error occurred: {e}")
        return False
    return True

def call_model(model: str, prompt: str, system_instruction: str, thinking_budget: int, temperature: float) -> bool:
    print(f"Running {model}...")
    start_time = time.perf_counter()
    response = client.models.generate_content(
        model=model, 
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            thinking_config=genai.types.ThinkingConfig(thinking_budget=thinking_budget)
        ),
    )
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    try:
        filename: str = f"ailog_projectprompt_{datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}_{model}_temp{temperature}.txt"
        with open(filename, 'w') as file:
            file.write(response.text)
        print(f"Data written. Task took {execution_time:.2f} seconds.")
    except IOError as e:
        print(f"An error occurred: {e}")
        return False
    return True

job_profile_list: list[JobProfile] = []

def load_knowledge_ext(filename: str):
    with open(filename, "r") as file:
        json_str = file.read()
    json_root = json.load(json_str)
    for ele in json_root:
        job_profile_list.append(JobProfile(ele))


if(__name__ == "__main__"):
    exit(0)
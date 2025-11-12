import datetime
import os
from dotenv import load_dotenv
from google import genai
import time

load_dotenv()

API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
THINKING_BUDGET = 8192
# THINKING_BUDGET = 4500
TEMPERATURE = 1.5
# MODEL = "gemini-2.5-flash-preview-09-2025"
MODEL = "gemini-2.5-pro"

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

start_time = time.perf_counter()
response = client.models.generate_content(
    model=MODEL, 
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=TEMPERATURE,
        thinking_config=genai.types.ThinkingConfig(thinking_budget=THINKING_BUDGET)
    ),
)
end_time = time.perf_counter()

try:
    filename: str = f"ailog_projectprompt_{datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}_{MODEL}_temp{TEMPERATURE}_thinkbudget{THINKING_BUDGET}.txt"
    with open(filename, 'w') as file:
        file.write(response.text)
    print(f"Data written")
except IOError as e:
    print(f"An error occurred: {e}")
    exit(1)

execution_time = end_time - start_time
print(f"The function took {execution_time:.2f} seconds to run.")
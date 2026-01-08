from typing import List, Tuple
from dotenv import load_dotenv
from google import genai
from google.genai import errors
import os
import datetime
import json
import re

load_dotenv()

API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_GENAI_API_KEY key not found in .env")

client = genai.Client(api_key=API_KEY)

def load_json_wrapper(filename: str) -> list[str]:
    try:
        with open(filename, "r") as file:
            data: list[str] = json.load(file)
            return data
    except Exception as e:
        return []

def trim_markdown_code_block(markdown_string: str) -> str:
    code_block_regex = re.compile(
        r"^\s*```[a-zA-Z]*\s*\n([\s\S]*?)\n\s*```", re.MULTILINE | re.DOTALL
    )

    match = code_block_regex.search(markdown_string)

    if match:
        return match.group(1).strip()
    return markdown_string.strip()


def func(userList: list[str], baseKnowledgeList: list[str], baseSkillList: list[str]) -> Tuple[bool, List[str]]:
    prompt = f'''
    You are an expert in ICT knowledge and skill taxonomy.
    Inputs (all JSON arrays):
    user_items: the user’s existing knowledge and skills.
    base_skills: the system’s canonical skill list.
    base_knowledge: the system’s canonical knowledge list.
    Task:
    For each item in user_items, find the best match in either base_skills or base_knowledge.
    Map each user item to a single entry or multiple entries either a skill or knowledge.
    Do not introduce or invent any concepts outside base_skills and base_knowledge.
    Output: A single JSON array containing all matched skills and knowledge items.
    Behavior rules:
    Prefer exact or near-exact lexical matches; use semantic matching only when necessary.
    If multiple base entries are equally good, choose the one with higher specificity (e.g., "IPv4 routing" over "networking").
    Output only the JSON array—no extra text, explanations, or metadata.

    Now perform the mapping using these variables:
    user_items = {json.dumps(userList)}
    base_skills = {json.dumps(baseSkillList)}
    base_knowledge = {json.dumps(baseKnowledgeList)}
    '''
    try:
        response = client.models.generate_content(
            model="gemma-3-27b-it",
            # model="gemini-flash-lite-latest",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.2
            )
        )
        if not response.text:
            return False, []

        response_text = trim_markdown_code_block(response.text)

        try:
            response_list: List[str] = json.loads(response_text)
            return True, response_list
        except:
            return False, []

    except errors.APIError as e:
        print(f"Error generating content: {e}")
        return False, []

def main():
    baseKnowledge = load_json_wrapper("assets/knowledge.json")
    baseSkill = load_json_wrapper("assets/skill.json")
    userList = ["python", "c", "c++", "x86", "java", "tensorflow", "dart", "flutter", "typescript", "nodejs", "GCP", "firebase", "tensorflow", "winapi", "parallel programming", "AVX512", "algorithms & data structures", "object oriented programming", "computer networking", "computer architecture", "read scentific papers", "linux", "bash scripting", "git", "docker", "nosql"]

    time_start = datetime.datetime.now()
    success, result = func(userList, baseKnowledge, baseSkill)
    time_end = datetime.datetime.now()

    print(f"Time taken: {time_end - time_start}")
    if success:
        print(f"Generated content successfully. Total {len(result)} items:")
        for item in result:
            if item in baseKnowledge:
                print(f"[KNOWLEDGE] {item}")
            elif item in baseSkill:
                print(f"[SKILL] {item}")
            else:
                print(f"[ERROR] {item}")
    else:
        print("Failed to generate content.")

def main2():
    print("List of models:\n")
    for m in client.models.list():
        print(m.name)

if __name__ == "__main__":
    # main()
    main2()

import json
import os
import time
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

MODEL = "gemini-flash-latest"
TEMPERATURE = 0.0


def load_json_wrapper(filename: str) -> list[str]:
    try:
        with open(filename, "r") as file:
            data: list[str] = json.load(file)
            return data
    except Exception as _:
        return []

# model for LLM to adhere to
class KnowledgeItem(BaseModel):
    knowledge: str = Field(..., description="The name of the knowledge, copied exactly from the input.")
    level: int = Field(..., description="Proficiency level from 1 to 10.")
    prerequisites: List[str] = Field(..., description="List of 1-5 direct prerequisite knowledges. MUST exist in the main input list.")

class TaxonomyResponse(BaseModel):
    knowledges: List[KnowledgeItem]

client = genai.Client(api_key=API_KEY)

input_knowledges = load_json_wrapper("assets/knowledge.json")

prompt = f"""
Analyze the following list of IT knowledges and enrich them according to the schema.
Input List: {input_knowledges}

CRITICAL REASONING RULES:
1. **Prerequisites:** Must ONLY contain strings that appear exactly in the "Input List".
2. **Cycle Prevention:** Do not create circular dependencies (e.g., A requires B, and B requires A). If a cycle is detected, remove the prerequisite relation.
3. **Empty Prerequisites:** If a knowledge has no logical parent in this specific list, return an empty list.
"""

print(f"Generating with {MODEL}...")
start_time = time.perf_counter()

try:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE,
            # 4. Enforce the schema here
            response_mime_type="application/json",
            response_schema=TaxonomyResponse,
            system_instruction="You are an expert IT curriculum designer. You are strict and factual.",
        ),
    )

    response_text = None
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text = part.text
                        break

    if response_text is None:
        raise ValueError("No response text received from the model.")

    # Write to file
    filename = "assets/knowledge2.json"
    with open(filename, "w") as f:
        f.write(response_text)

except Exception as e:
    print(f"Error: {e}")

end_time = time.perf_counter()
print(f"Time taken: {end_time - start_time:.2f}s")

import json
import datetime
from operator import is_
import os
from typing import List, Tuple
from sentence_transformers import SentenceTransformer, util
from typing import List, NamedTuple
import torch

# MODEL_NAME = 'all-MiniLM-L6-v2'
MODEL_NAME = 'nomic-ai/nomic-embed-text-v1.5'
SIMILARITY_THRESHOLD = 0.65  # Higher = strict matching, Lower = fuzzy matching

class TaxonomyItem(NamedTuple):
    text: str
    is_knowledge: bool

class TaxonomyMapper:
    def __init__(self, model: str, threshold: float, knowledge_list: List[str], skill_list: List[str]):
        print(f"TaxonomyMapper: Loading embedding model {model}... ")
        self.model = SentenceTransformer(model, trust_remote_code=True)
        self.threshold = threshold

        self.corpus: List[TaxonomyItem] = []
        for k in knowledge_list:
            self.corpus.append(TaxonomyItem(text=k, is_knowledge=True))
        for s in skill_list:
            self.corpus.append(TaxonomyItem(text=s, is_knowledge=False))

        flat_corpus = [item.text for item in self.corpus]
        self.corpus_embeddings = self.model.encode(flat_corpus, convert_to_tensor=True)
        print("TaxonomyMapper: Indexing complete.")

    #return list of skill, knowledge
    def map_items(self, user_items: List[str]) -> Tuple[List[str], List[str]]:
        if not user_items:
            return ([], [])

        query_embeddings = self.model.encode(user_items, convert_to_tensor=True)
        cosine_scores = util.cos_sim(query_embeddings, self.corpus_embeddings)

        mapped_skill = []
        mapped_knowledge = []

        for i, item_text in enumerate(user_items):
            # Get the single highest score
            best_score_tensor = torch.max(cosine_scores[i], dim=0)
            best_score = best_score_tensor.values.item()
            best_idx = best_score_tensor.indices.item()

            if best_score >= self.threshold:
                match_text = self.corpus[int(best_idx)].text
                is_knowledge = self.corpus[int(best_idx)].is_knowledge
                if is_knowledge:
                    mapped_knowledge.append(match_text)
                else:
                    mapped_skill.append(match_text)
            else:
                pass

        return (list(set(mapped_skill)), list(set(mapped_knowledge)))

def run_translate(userList: list[str], baseKnowledgeList: list[str], baseSkillList: list[str]) -> Tuple[List[str], List[str]] | None:
    try:
        mapper = TaxonomyMapper(MODEL_NAME, SIMILARITY_THRESHOLD, baseKnowledgeList, baseSkillList)

        result = mapper.map_items(userList)
        return result
    except Exception as e:
        print(f"TaxonomyMapper: error: {e}")
        return None

def load_json_wrapper(filename: str) -> list[str]:
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except:
        return []

def main():
    baseKnowledge = load_json_wrapper("assets/knowledge.json")
    baseSkill = load_json_wrapper("assets/skill.json")
    userList = ["python", "c", "c++", "x86", "java", "tensorflow", "dart", "flutter", "typescript", "nodejs", "GCP", "firebase", "tensorflow", "winapi", "parallel programming", "AVX512", "algorithms & data structures", "object oriented programming", "computer networking", "computer architecture", "read scentific papers", "linux", "bash scripting", "git", "docker", "nosql", "xcode", "swift", "kotlin", "android development", "swelte", "hackathon", "computational thinking", "manage small groups projects"]

    time_start = datetime.datetime.now()
    result = run_translate(userList, baseKnowledge, baseSkill)
    time_end = datetime.datetime.now()

    print(f"Time taken: {time_end - time_start}")
    if result:
        print(f"Mapped {len(result[0])} skills and {len(result[1])} knowledge items:")
        for skill in result[0]:
            print(skill)
        for knowledge in result[1]:
            print(knowledge)
    else:
        print("Failed to generate content.")

if __name__ == "__main__":
    main()

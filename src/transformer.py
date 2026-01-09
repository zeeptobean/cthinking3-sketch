from sentence_transformers import SentenceTransformer, util
from typing import List, NamedTuple, Tuple
from data_loader import Job, data_loader
import torch

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
    
class JobMapper:
    def _create_job_embedding_string(self, job: Job) -> str:
        full_text = f"Job Title: {job.name}. "
        alt_names_str = ", ".join(job.other_name)

        full_text += f"Also known as: {alt_names_str}. "
        full_text += f"Description: {job.description}"
        return full_text

    def __init__(self, model: str, threshold: float):
        print(f"JobMapper: Loading embedding model {model}... ")
        self.model = SentenceTransformer(model, trust_remote_code=True)
        self.threshold = threshold

        corpus: List[str] = []
        for item in data_loader.job_map.values():
            corpus.append(self._create_job_embedding_string(item))
        self.corpus_embeddings = self.model.encode(corpus, convert_to_tensor=True)
        print("JobMapper: Indexing complete.")

    def map(self, input_str: str) -> List:
        query_embedding = self.model.encode(input_str, convert_to_tensor=True)
        cosine_scores = util.cos_sim(query_embedding, self.corpus_embeddings)

        results: List[Tuple[float, Job]] = []

        for i in range(len(data_loader.job_map)):
            score = cosine_scores[0][i].item()
            if score >= self.threshold:
                job = list(data_loader.job_map.values())[i]
                results.append((score, job))

        results.sort(key=lambda x: x[0], reverse=True)

        return results
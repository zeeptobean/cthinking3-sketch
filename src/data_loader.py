import json
from typing import Any
from dataclasses import dataclass

def load_json_array_wrapper(filename: str) -> list[str] | None:
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON from {filename}: {e}")
        return None
    
@dataclass
class KnowledgeDetail:
    knowledge: str
    level: int
    prerequisites: list[str]
    
@dataclass
class Job:
    url: str
    name: str
    description: str
    other_name: list[str]
    essential_skill: list[str]
    optional_skill: list[str]
    essential_knowledge: list[str]
    optional_knowledge: list[str]

class DataLoader:
    def _load_json_internal(self, filename: str) -> Any | None:
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON from {filename}: {e}")
            return None

    def __init__(self):
        temp = load_json_array_wrapper("assets/knowledge.json")
        if(temp is None):
            raise RuntimeError("Failed to load data")
        self.base_knowledge = temp

        temp = load_json_array_wrapper("assets/skill.json")
        if(temp is None):
            raise RuntimeError("Failed to load data")
        self.base_skill = temp

        temp = self._load_json_internal("assets/job.json")
        if(temp is None):
            raise RuntimeError("Failed to load data")
        jobobj_list = [Job(**item) for item in temp]
        self.job_map = {item.name: item for item in jobobj_list}
        self.alternative_job_map: dict[str, str] = {}

        for item in jobobj_list:
            for alternative_name in item.other_name:
                self.alternative_job_map[alternative_name] = item.name

        temp = self._load_json_internal("assets/knowledge2.json")
        if(temp is None):
            raise RuntimeError("Failed to load data")
        temp = temp["knowledges"]
        knowledge_detailobj_list = [KnowledgeDetail(**item) for item in temp]
        self.knowledge_detail_map = {item.knowledge: item for item in knowledge_detailobj_list}

data_loader = DataLoader()
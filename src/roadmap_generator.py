"""
Module tạo roadmap học tập dựa trên topological sort
"""
from typing import Any, List, Dict, Set, NamedTuple
from graph_utils import GraphUtils
from data_loader import Job, data_loader

class Roadmap(NamedTuple):
    roadmap: List[Dict[str, Any]]
    has_cycles: bool
    cycles: List[List[str]]
    total_items: int


def generate_learning_roadmap(job: Job, user_knowledge: List[str]) -> Roadmap:
    graph = GraphUtils()
    
    def get_missing_knowledge(job: Job, user_knowledge: List[str]) -> List[str]:
        required_knowledge = set(job.essential_knowledge + job.optional_knowledge)
        learned_knowledge_set = set(user_knowledge)
        missing_knowledge = list(required_knowledge - learned_knowledge_set)
        return missing_knowledge

    def get_prerequisites(item: str) -> List[str]:
        info = data_loader.knowledge_detail_map.get(item)
        if not info:
            return []
        else:
            return info.prerequisites
    
    def get_level(item: str) -> int:
        info = data_loader.knowledge_detail_map.get(item)
        if not info:
            return 0
        else:
            return info.level
        
    missing_items = get_missing_knowledge(job, user_knowledge)
    learned_items = set(user_knowledge)

    # Tạo learning path (truyền learned_items)
    path_info = graph.get_learning_path(missing_items, get_prerequisites, get_level, learned_items)
    
    # Chuyển đổi sang format dễ đọc
    formatted_groups = graph.get_parallel_learning_groups(path_info["path"])
    
    roadmap_data = {
        "roadmap": formatted_groups,
        "has_cycles": path_info["has_cycles"],
        "cycles": path_info["cycles"],
        "total_items": path_info["total_items"]
    }
    roadmap_obj = Roadmap(**roadmap_data)
    return roadmap_obj
    
def format_roadmap_for_display(roadmap: Roadmap) -> str:
    output = []
    output.append("=" * 60)
    output.append("📚 KNOWLEDGE LEARNING ROADMAP")
    output.append("=" * 60)
    output.append("")

    total_difficulty = 0
    total_items = roadmap.total_items
    hours_per_item = 20
    
    for stage in roadmap.roadmap:
        stage_num = stage["stage"]
        items = stage["items"]
        count = stage["count"]
        stage_type = stage.get("type", "path")
        
        # Xử lý 2 loại stage: scc và path
        if stage_type == "scc":
            # SCC - các knowledge phụ thuộc lẫn nhau, học song song
            output.append(f"Stage {stage_num}: 🔄 Learn in Parallel ({count} items)")
        else:
            # Path - học tuần tự
            output.append(f"Stage {stage_num}: ➡️ Learn Sequentially ({count} items)")
        
        for item in items:
            output.append(f"  • {item}")
            info = data_loader.knowledge_detail_map.get(item)
            if not info:
                continue
            total_difficulty += info.level

    estimated_difficulty = round(total_difficulty / total_items, 2)
    difficulty_multiplier = estimated_difficulty / 5.0
    adjusted_hours = total_items * hours_per_item * difficulty_multiplier
    if roadmap.has_cycles:
        adjusted_hours *= 0.8  # Giảm 20% nhờ học song song
        
    output.append(f"⏰ Estimated Learning Time: {round(adjusted_hours, 1)} hours")
    
    return "\n".join(output)
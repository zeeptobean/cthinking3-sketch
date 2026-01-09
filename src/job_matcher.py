from typing import List, Dict, Set, Tuple
from data_loader import Job, data_loader
    
def calculate_match_score(job: Job, user_skills: List[str], user_knowledge: List[str]) -> float:
    # user_skills_lower = set(s.lower() for s in user_skills)
    # user_knowledge_lower = set(k.lower() for k in user_knowledge)
    
    # Tính matched và missing
    # matched_required_skills = user_skills_lower & set(job.essential_skill)
    # matched_optional_skills = user_skills_lower & set(job.optional_skill)
    # matched_required_knowledge = user_knowledge_lower & set(job.essential_knowledge)
    # matched_optional_knowledge = user_knowledge_lower & set(job.optional_knowledge)
    
    # missing_required_skills = set(job.essential_skill) - user_skills_lower
    # missing_optional_skills = set(job.optional_skill) - user_skills_lower
    # missing_required_knowledge = set(job.essential_knowledge) - user_knowledge_lower
    # missing_optional_knowledge = set(job.optional_knowledge) - user_knowledge_lower

    matched_required_skills = set(user_skills) & set(job.essential_skill)
    matched_optional_skills = set(user_skills) & set(job.optional_skill)
    matched_required_knowledge = set(user_knowledge) & set(job.essential_knowledge)
    matched_optional_knowledge = set(user_knowledge) & set(job.optional_knowledge)
    
    # Tính điểm
    # Required: 70% trọng số, Optional: 30% trọng số
    total_required = len(job.essential_skill) + len(job.essential_knowledge)
    total_optional = len(job.optional_skill) + len(job.optional_knowledge)
    
    matched_required = len(matched_required_skills) + len(matched_required_knowledge)
    matched_optional = len(matched_optional_skills) + len(matched_optional_knowledge)

    # print(f"Job: {job.name}")
    # print(f"  Matched Required: {matched_required}, Total Required: {total_required}")
    # print(f"  Matched Optional: {matched_optional}, Total Optional: {total_optional}")
    
    # Cải thiện: Nếu không có required items, tính điểm dựa trên optional
    if total_required > 0:
        required_score = (matched_required / total_required * 100)
    else:
        required_score = 100  # Nếu job không có required items
    
    if total_optional > 0:
        optional_score = (matched_optional / total_optional * 100)
    else:
        optional_score = 100  # Nếu job không có optional items
    
    # Tổng điểm: Nếu có ít nhất 1 match, cho điểm tối thiểu
    total_match = matched_required + matched_optional
    if total_match > 0:
        # Có match: tính điểm bình thường + bonus
        total_score = required_score * 0.7 + optional_score * 0.3
        # Bonus cho mỗi item matched (tối đa 20 điểm)
        bonus = min(total_match * 5, 20)
        total_score = min(total_score + bonus, 100)
    else:
        # Không có match nào
        total_score = float(0)
    
    return total_score

async def find_suitable_jobs(user_skills: List[str], user_knowledge: List[str],  min_score: float = 5.0, top_n: int = 15) -> List[Tuple[float, Job]]:
    results = []
    
    for job in data_loader.job_map.values():
        match_score = calculate_match_score(job, user_skills, user_knowledge)
        if match_score >= min_score:
            results.append([match_score, job])
    
    # Sắp xếp theo điểm giảm dần
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top_n]

# a: stuff, scoring 0.0-100.0
# b: job, scoring 0.0-100.0
def merge_job_list(a: List[Tuple[float, Job]], b: List[Tuple[float, Job]]) -> List[Tuple[float, Job]]:
    map_a: dict[str, float] = {}
    map_b: dict[str, float] = {}
    for score, job in a:
        map_a[job.name] = score
    for score, job in b:
        map_b[job.name] = score

    map_c: List[Tuple[float, Job]] = []
    for job_name in map_a.keys():
        if job_name in map_b:
            b_score = map_b[job_name]
        else:
            b_score = 0.0
        
        fused_score = map_a[job_name]/100.0*0.7 + b_score*0.3
        map_c.append( (fused_score, data_loader.job_map[job_name]) )

    map_c.sort(key=lambda x: x[0], reverse=True)

    return map_c
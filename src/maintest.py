import asyncio
from typing import List, Tuple
from data_loader import Job, data_loader
from translate import run_translate_job
from job_matcher import find_suitable_jobs

# a: stuff, scoring 0.0-100.0
# b: job, scoring 0.0-100.0
def calculate_fusion_score(a: List[Tuple[float, Job]], b: List[Tuple[float, Job]]) -> List[Tuple[float, Job]]:
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


async def test():
    stuff_translated = await find_suitable_jobs(["implement ICT recovery system", "use markup languages", "define technical requirements", "protect ICT devices"], ["Pascal (computer programming)", "systems theory", "Assembly (computer programming)", ])
    job_translated = await run_translate_job("hacker, networking related, low-level, kernel")
    if(job_translated is None or stuff_translated is None):
        print("Error")
    else:
        res = calculate_fusion_score(stuff_translated, job_translated)
        for score, job in res:
            print(f"Score: {score}, Job: {job.name}")
        print("done")
    # print(res)

asyncio.run(test())
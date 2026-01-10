import json
import datetime
from operator import is_
import os
from typing import List, Tuple, NamedTuple
from transformer import JobMapper, TaxonomyMapper
from data_loader import Job, data_loader

_taxonomy_mapper = None
_job_taxonomy_mapper = None

# If this is true, the transfomers will be init later on first use
_translate_debug = False

if not _translate_debug:
    _taxonomy_mapper = TaxonomyMapper(
        'nomic-ai/nomic-embed-text-v1.5',
        0.65,
        data_loader.base_knowledge,
        data_loader.base_skill
    )
    _job_taxonomy_mapper = JobMapper(
        'nomic-ai/nomic-embed-text-v1.5',
        0.525
    )

def _get_taxonomy_mapper() -> TaxonomyMapper:
    global _taxonomy_mapper
    if _taxonomy_mapper is None:
        _taxonomy_mapper = TaxonomyMapper(
            'nomic-ai/nomic-embed-text-v1.5',
            0.65,
            data_loader.base_knowledge,
            data_loader.base_skill
        )
    return _taxonomy_mapper

def _get_job_taxonomy_mapper() -> JobMapper:
    global _job_taxonomy_mapper
    if _job_taxonomy_mapper is None:
        _job_taxonomy_mapper = JobMapper(
            'nomic-ai/nomic-embed-text-v1.5',
            0.525
        )
    return _job_taxonomy_mapper

#return list of skill, knowledge
async def run_translate(userList: list[str]) -> Tuple[List[str], List[str]] | None:
    try:
        result = _get_taxonomy_mapper().map_items(userList)
        return result
    except Exception as e:
        print(f"TaxonomyMapper: error: {e}")
        return None
    
async def run_translate_job(input_str: str) -> List[Tuple[float, Job]] | None:
    try:
        result = _get_job_taxonomy_mapper().map(input_str)
        return result
    except Exception as e:
        print(f"JobMapper: error: {e}")
        return None

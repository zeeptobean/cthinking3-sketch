import json
import datetime
from operator import is_
import os
from typing import List, Tuple, NamedTuple
from transformer import TaxonomyMapper
from data_loader import data_loader

#Load engine first, the init gui

#return list of skill, knowledge
async def run_translate(userList: list[str]) -> Tuple[List[str], List[str]] | None:
    try:
        result = _get_taxonomy_mapper().map_items(userList)
        return result
    except Exception as e:
        print(f"TaxonomyMapper: error: {e}")
        return None
    
async def run_translate_job(input_str: str) -> Job | None:

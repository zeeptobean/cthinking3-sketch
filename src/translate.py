import json
import datetime
from operator import is_
import os
from typing import List, Tuple, NamedTuple
from transformer import TaxonomyMapper
from data_loader import data_loader

_taxonomy_mapper = None

def _get_taxonomy_mapper() -> TaxonomyMapper:
    global _taxonomy_mapper
    if _taxonomy_mapper is None:
        _taxonomy_mapper = TaxonomyMapper(
            'nomic-ai/nomic-embed-text-v1.5',
            0.7,
            data_loader.base_knowledge,
            data_loader.base_skill
        )
    return _taxonomy_mapper

async def run_translate(userList: list[str]) -> Tuple[List[str], List[str]] | None:
    try:
        result = _get_taxonomy_mapper().map_items(userList)
        return result
    except Exception as e:
        print(f"TaxonomyMapper: error: {e}")
        return None
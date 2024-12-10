# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import fastapi
from ..core import create_chroma_client, DateRange
from .models import *


api = fastapi.FastAPI(title="T4Search API")
chroma_client = create_chroma_client()


@api.get("/api/query", response_model=t.List[QueryResponseModel])
def query(
        topics: t.List[str] = fastapi.Query(min_length=1),
        persons: t.List[str] =  fastapi.Query(default_factory=list),
        dates: t.List[str] = fastapi.Query(default_factory=list),
        parties: t.List[str] = fastapi.Query(default_factory=list),
) -> t.List[QueryResponseModel]:
    dates: t.List[DateRange] = list(map(DateRange.from_string, dates))

    result = search(start_date=dates[0], end_date=dates[1], parties=parties, person_ids=persons)
    return result


def __main__(**kwargs):
    import uvicorn, configlib
    uvicorn.run(app=api, **configlib.config.get('api', fallback={}), **kwargs)



def search(query_text=None, start_date=None, end_date=None, parties=[], person_ids=[]):
    # Keyword suche

    # ands = []
    filters = {}

    if len(parties):
        filters['party'] = {"$in": parties}
    
    if len(person_ids):
        filters['speaker'] = {"$in": person_ids}

    if start_date:
        filters['date'] = {"$gte": start_date}
        
    if not len(filters):
        filters = None


    where_obj = {}
    if len(filters) > 1:
        where_obj["$and"] = []
        for key, value in filters.items():
            where_obj["$and"].append({key: value})
    else:
        where_obj = filters


    protokolle_coll = chroma_client.get_collection(name="protokolle_coll")

    return protokolle_coll.query(
        query_texts=[query_text],
        where=where_obj,
        n_results=5
    )
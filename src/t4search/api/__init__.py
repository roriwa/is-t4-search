# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import fastapi, pprint
from ..core import create_chroma_client, DateRange
from .models import *


api = fastapi.FastAPI(title="T4Search API")
chroma_client = create_chroma_client()


@api.get("/api/query", response_model=t.List[QueryResponseModel])
def query(
        query_text: str = fastapi.Query(),
        # topics: t.List[str] = fastapi.Query(default_factory=list),
        persons: t.List[str] =  fastapi.Query(default_factory=list),
        dates: t.List[str] = fastapi.Query(default_factory=list),
        parties: t.List[str] = fastapi.Query(default_factory=list),
        limit: t.Optional[int] = fastapi.Query(default=10),
) -> t.List[QueryResponseModel]:
    dates: t.List[DateRange] = list(map(DateRange.from_string, dates))

    wheres = []

    if persons:
        wheres.append({
            'person': {
                '$in': persons,
            }
        })

    if parties:
        wheres.append({
            'party': {
                '$in': parties,
            }
        })

    if dates:
        date_ranges = []
        for date in dates:
            if date.start and date.end:
                date_ranges.append({
                    '$and': [
                        { 'date': { '$gte': date.start } },
                        { 'date': { '$lte': date.end } },
                    ],
                })
            elif date.start:
                date_ranges.append({
                    'date': { '$gte': date.start },
                })
            elif date.end:
                date_ranges.append({
                    'date': { '$lte': date.end }
                })
            else:
                raise
        wheres.append({
            '$or': date_ranges,
        })

    where = {'$and': wheres}

    if len(wheres) == 1:
        where = wheres[0]
    elif len(wheres) == 0:
        where = None 

    protocols = chroma_client.get_collection(name="protocols")
    results = ChromaResponseObject.model_validate(protocols.query(
        query_texts=[query_text],
        where=where,
        n_results=limit,
    ))

    n_results = len(results.documents[0])

    pprint.pprint(results)

    return [
        QueryResponseModel(
            mongo_id=results.ids[0][i],
            metadata=results.metadatas[0][i],
            distances=results.distances[0][i],
        )
        for i in range(n_results)
    ]


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
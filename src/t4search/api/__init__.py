# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import fastapi
from pydantic import ValidationError
from ..core import create_chroma_client, DateRange, split_vector_id
from .models import *


api = fastapi.FastAPI(title="T4Search API")
chroma_client = create_chroma_client()


@api.post("/api/query", response_model=t.List[QueryResponseModel])
def query(
        query_text: str = fastapi.Body(),
        # topics: t.List[str] = fastapi.Body(default_factory=list),
        persons: t.List[str] =  fastapi.Body(default_factory=list),
        dates: t.List[str] = fastapi.Body(default_factory=list),
        parties: t.List[str] = fastapi.Body(default_factory=list),
        limit: t.Optional[int] = fastapi.Body(default=10),
) -> t.List[QueryResponseModel]:
    r"""
    ## `query_text`:
    Query text to search for

    ## `persons`
    List of speaker (id) that are allowed

    ## `dates`
    Examples:
    - `2021-01-01:2022-01-01` (between two dates)
    - `2021-01-01:` (after a date)
    - `:2022-01-01` (before a date)
    - `2022-01-01` (specific date)

    ## `parties`:
    List of parties (names) that are allowed

    ## `limit`:
    Maximum Number of results to return
    """
    try:
        dates: t.List[DateRange] = list(map(DateRange.from_string, dates))
    except ValidationError as e:
        raise fastapi.exceptions.RequestValidationError(e.errors())

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
                '$in': [p.casefold() for p in parties],
            }
        })

    if dates:
        date_ranges = []
        for date in dates:
            if date.start and date.end:
                date_ranges.append({
                    '$and': [
                        { 'date': { '$gte': date.start.toordinal() } },
                        { 'date': { '$lte': date.end.toordinal() } },
                    ],
                })
            elif date.start:
                date_ranges.append({
                    'date': { '$gte': date.start.toordinal() },
                })
            elif date.end:
                date_ranges.append({
                    'date': { '$lte': date.end.toordinal() },
                })
            else:
                raise
        if len(date_ranges) == 1:
            wheres.append(date_ranges[0])
        else:
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

    print(results)

    n_results = len(results.documents[0])

    return [
        QueryResponseModel(
            **split_vector_id(results.ids[0][i]),
            metadata=results.metadatas[0][i],
            distances=results.distances[0][i],
            document=results.documents[0][i],
        )
        for i in range(n_results)
    ]


def __main__(**kwargs):
    import uvicorn, configlib
    uvicorn.run(app=api, **configlib.config.get('api', fallback={}), **kwargs)

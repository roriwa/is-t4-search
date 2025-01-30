# -*- coding=utf-8 -*-
r"""

"""
import time
import typing as t
import nltk
import fastapi
from pydantic import ValidationError
from ..core import create_chroma_client, DateRange, split_vector_id
from .models import *


api = fastapi.FastAPI(title="T4Search API")


@api.middleware("http")
async def add_process_time_header(request: fastapi.Request, call_next: callable) -> fastapi.Response:
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@api.post("/api/query", response_model=t.List[QueryResponseModel])
def api_query(
        query_text: str = fastapi.Body(examples=[""]),
        topics: t.List[str] = fastapi.Body(default_factory=list, examples=[[]]),
        speaker: t.List[str] =  fastapi.Body(default_factory=list, examples=[[]]),
        dates: t.List[str] = fastapi.Body(default_factory=list, examples=[[]]),
        parties: t.List[str] = fastapi.Body(default_factory=list, examples=[[]]),
        limit: t.Optional[int] = fastapi.Body(default=10),
) -> t.List[QueryResponseModel]:
    r"""
    ## `query_text`:
    Query text to search for

    ## `topics`:
    specific topics/keywords to search for

    ## `speaker`:
    List of speaker-names that are allowed

    ## `dates`:
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

    chroma_client = create_chroma_client()

    wheres = []

    if speaker:
        speaker_resolved = api_delegated(names=speaker, n_results=len(speaker) * 4)
        wheres.append({
            'speaker_id': {
                '$in': [s.delegated_id for s in speaker_resolved],
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

    per_query_limit = limit // (1 + len(topics))

    protocols = chroma_client.get_or_create_collection(name="protocols")
    results = ChromaResponseObject.model_validate(protocols.query(
        query_texts=[query_text, *topics],
        where=where,
        n_results=per_query_limit,
    ))

    returns: t.List[QueryResponseModel] = []

    for i in range(len(results.ids)):
        for j in range(len(results.ids[i])):
            returns.append(
                QueryResponseModel(
                    **split_vector_id(results.ids[i][j]),
                    metadata=results.metadatas[i][j],
                    distances=results.distances[i][j],
                    document=results.documents[i][j],
                )
            )

    return returns


@api.post("/api/delegated", response_model=t.List[DelegatedResponseModel])
def api_delegated(
        names: t.List[str] = fastapi.Body(examples=[[]]),
        n_results: int = fastapi.Body(default=10),
):
    chroma_client = create_chroma_client()
    delegated_collection = chroma_client.get_or_create_collection(name="delegated")

    results = ChromaResponseObject.model_validate(delegated_collection.query(
        query_texts=names,
        n_results=n_results,
    ))

    returns: t.List[DelegatedResponseModel] = []

    for i in range(len(results.ids)):
        for j in range(len(results.ids[i])):
            returns.append(
                DelegatedResponseModel(
                    delegated_id=results.ids[i][j],
                    delegated_name=results.documents[i][j],
                )
            )

    return returns


@api.post("/api/split", response_model=t.List[str])
def api_split(
        sentence: str = fastapi.Body(media_type="text/plain"),
):
    r"""
    splits a longer text into the sentences
    """
    sent_tokenizer = nltk.PunktTokenizer(lang="german")
    return sent_tokenizer.tokenize(sentence)


def __main__(**kwargs):
    import uvicorn, configlib
    uvicorn.run(app=api, **configlib.config.get('api', fallback={}), **kwargs)

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
    return []


def __main__(**kwargs):
    import uvicorn, configlib
    uvicorn.run(app=api, **configlib.config.get('api', fallback={}), **kwargs)

# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic import BaseModel


__all__ = ['Metadata', 'QueryResponseModel', 'ChromaResponseObject']


class Metadata(BaseModel):
    speaker: str
    # party: str
    date: str


class QueryResponseModel(BaseModel):
    mongo_id: str
    metadata: Metadata
    distances: float


class ChromaResponseObject(BaseModel):
    documents: t.List[t.List[str]]
    ids: t.List[t.List[str]]
    distances: t.List[t.List[float]]
    uris: t.Optional[t.List[t.List[t.Any]]]
    data: t.Optional[t.List[t.List[t.Any]]]
    metadatas: t.List[t.List[t.Any]]
    embeddings: t.Optional[t.List[t.List[t.Any]]]

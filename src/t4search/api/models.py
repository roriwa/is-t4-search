# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic import BaseModel


__all__ = ['Metadata', 'QueryResponseModel', 'ChromaResponseObject']


class Metadata(BaseModel):
    speaker_id: str
    party: t.Optional[str]
    date: float


class QueryResponseModel(BaseModel):
    protocol_id: int
    session_index: int
    speach_index: int
    sentence_index: int
    metadata: Metadata
    distances: float
    document: t.Optional[str]


class ChromaResponseObject(BaseModel):
    documents: t.List[t.List[t.Optional[str]]]
    ids: t.List[t.List[str]]
    distances: t.List[t.List[float]]
    uris: t.Optional[t.List[t.List[t.Any]]]
    data: t.Optional[t.List[t.List[t.Any]]]
    metadatas: t.List[t.List[t.Any]]
    embeddings: t.Optional[t.List[t.List[t.Any]]]

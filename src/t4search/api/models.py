# -*- coding=utf-8 -*-
r"""

"""
from pydantic import BaseModel


__all__ = ['Metadata', 'QueryResponseModel']


class Metadata(BaseModel):
    person: str
    party: str
    date: str


class QueryResponseModel(BaseModel):
    mongo_id: int
    metadata: Metadata
    distance: float

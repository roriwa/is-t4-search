# -*- coding=utf-8 -*-
r"""

"""
from typing import TypedDict


__all__ = ['VectorId', 'split_vector_id', 'create_vector_id']


class VectorId(TypedDict):
    protocol_id: int
    session_index: int
    speach_index: int
    sentence_index: int


def split_vector_id(vector_id: str) -> VectorId:
    protocol_id, session_index, speach_index, sentence_index = map(int, vector_id.split("#"))
    return VectorId(
        protocol_id=protocol_id,
        session_index=session_index,
        speach_index=speach_index,
        sentence_index=sentence_index,
    )


def create_vector_id(protocol_id: int, session_index: int, speach_index: int, sentence_index: int) -> str:
    return f"{protocol_id}#{session_index}#{speach_index}#{sentence_index}"

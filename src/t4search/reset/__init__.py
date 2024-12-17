# -*- coding=utf-8 -*-
r"""

"""
from ..core import create_chroma_client


def __main__():
    chroma_client = create_chroma_client()

    for collection in chroma_client.list_collections():
        chroma_client.delete_collection(name=collection.name)

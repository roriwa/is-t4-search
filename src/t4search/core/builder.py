# -*- coding=utf-8 -*-
r"""

"""
import chromadb
from configlib import config


__all__ = ['create_chroma_client']


def create_chroma_client() -> chromadb.ClientAPI:
    return chromadb.HttpClient(
        host=config.getstr('chroma', 'host', fallback="localhost"),
        port=config.getint('chroma', 'port', fallback=8000),
    )

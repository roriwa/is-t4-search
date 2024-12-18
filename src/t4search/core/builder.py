# -*- coding=utf-8 -*-
r"""

"""
import pymongo
import chromadb.utils.embedding_functions
from configlib import config


__all__ = ['create_chroma_client', 'create_chroma_embedding_function', 'create_mongo_client']


def create_chroma_client() -> chromadb.ClientAPI:
    return chromadb.HttpClient(
        host=config.getstr('chroma', 'host', fallback="localhost"),
        port=config.getint('chroma', 'port', fallback=9010),
        settings=chromadb.Settings(anonymized_telemetry=False),
    )


def create_chroma_embedding_function() -> chromadb.EmbeddingFunction[chromadb.Documents]:
    return chromadb.utils.embedding_functions.DefaultEmbeddingFunction()


def create_mongo_client() -> pymongo.MongoClient:
    return pymongo.MongoClient(
        config.getstr('mongo_uri')
    )

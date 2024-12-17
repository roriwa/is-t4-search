# -*- coding=utf-8 -*-
r"""

"""
import chromadb
import pymongo
from configlib import config


__all__ = ['create_chroma_client', 'create_mongo_client']


def create_chroma_client() -> chromadb.ClientAPI:
    return chromadb.HttpClient(
        host=config.getstr('chroma', 'host', fallback="localhost"),
        port=config.getint('chroma', 'port', fallback=9010),
        settings=chromadb.Settings(anonymized_telemetry=False),
    )


def create_mongo_client() -> pymongo.MongoClient:
    return pymongo.MongoClient(
        config.getstr('mongo_uri')
    )

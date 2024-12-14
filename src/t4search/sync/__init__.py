# -*- coding=utf-8 -*-
r"""

"""
import logging
import typing as t
from datetime import datetime
from ..core import create_mongo_client, create_chroma_client


def __main__():
    logging.info("initiating sync")

    logging.info("creating mongo client")
    mongo_client = create_mongo_client()
    mongo_db = mongo_client.get_database("bundestag")

    logging.info("creating chroma client")
    chroma_client = create_chroma_client()
    protocol_collection = chroma_client.get_or_create_collection(name="protocols")

    for protocol in mongo_db.get_collection("protokolle"):
        logging.info("syncing protocol %s", protocol.name)

        date = datetime.strptime(protocol['datum'], '%d.%m.%Y').date()

        for session_index, session in enumerate(protocol["sitzungsverlauf"]):
            logging.info("syncing session %s", session)

            ids: t.List[str] = []
            documents: t.List[str] = []
            metadatas: t.List[t.Dict[str, t.Any]] = []

            for speach_index, speach in enumerate(session["rede"]):
                ids.append(f"{protocol['id']}#{session_index}#{speach_index}")
                documents.append(speach['text'])
                metadatas.append(dict(
                    speaker=speach['redner_id'],
                    date=date,
                ))

            logging.info("upserting for session %s", session)
            protocol_collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

# -*- coding=utf-8 -*-
r"""

"""
import logging
import typing as t
from loggext.decorators import add_logging
from functools import lru_cache
from datetime import datetime
from ..core import create_mongo_client, create_chroma_client


def __main__():
    logging.info("initiating sync")

    # creating connections

    logging.info("creating mongo client")
    mongo_client = create_mongo_client()
    mongo_db = mongo_client.get_database("bundestag")
    mongo_protocols_collection = mongo_db.get_collection("protokolle")
    mongo_delegated_collection = mongo_db.get_collection(name='mdb_stammdaten')

    logging.info("creating chroma client")
    chroma_client = create_chroma_client()
    chroma_protocol_collection = chroma_client.get_or_create_collection(name="protocols")

    # speaker fetching

    @lru_cache(maxsize=256)
    @add_logging()
    def get_speaker_by_id(id_: str) -> t.Optional[t.Dict[str, t.Any]]:
        return mongo_delegated_collection.find_one({'id': id_})

    # syncing

    for protocol in mongo_protocols_collection:
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
                speaker_id = speach['redner_id']
                speaker = get_speaker_by_id(speaker_id)
                metadatas.append(dict(
                    speaker_id=speaker_id,
                    party=speaker['fraktion'] if speaker else None,
                    date=date,
                ))

            logging.info("upserting for session %s", session)
            chroma_protocol_collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

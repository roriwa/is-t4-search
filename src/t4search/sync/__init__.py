# -*- coding=utf-8 -*-
r"""

"""
import json
import logging
import typing as t
from pathlib import Path
from functools import lru_cache
import datetime
import nltk
import chromadb
import filelock
from loggext.decorators import add_logging
from ..core import create_mongo_client, create_chroma_client, create_chroma_embedding_function, create_vector_id
from .models import *


sync_lock = filelock.FileLock("sync.lock")


@sync_lock
def __main__():
    logging.info("initiating sync")
    sync_delegated()
    sync_protocols()


def sync_delegated():
    logging.info("initiating delegated sync")

    # creating connections

    logging.info("creating mongo client")
    mongo_client = create_mongo_client()
    mongo_db = mongo_client.get_database("bundestag")
    mongo_delegated_collection = mongo_db.get_collection(name='mdb_stammdaten')

    logging.info("creating chroma client")
    chroma_client = create_chroma_client()
    chroma_delegated_collection = chroma_client.get_or_create_collection(name="delegated")

    mongo_delegated_ids: t.List[str] = [doc['id'] for doc in mongo_delegated_collection.find({}, {'id': 1})]

    for delegated_id in mongo_delegated_ids:
        delegated_raw = mongo_delegated_collection.find_one({'id': delegated_id})
        if delegated_raw is None:
            logging.error("Delegated %s disappeared", delegated_id)
            continue
        delegated = MongoDelegatedModel.model_validate(delegated_raw)

        document = f"{delegated.titel} {delegated.vorname} {delegated.nachname}".strip()

        metadata = dict(
            fraktion=delegated.fraktion or '',
        )

        chroma_delegated_collection.upsert(ids=[delegated.id], documents=[document], metadatas=[metadata])


def sync_protocols():
    logging.info("initiating protocol sync")

    # tokenizer

    logging.info("creating nltk tokenizer")
    sent_tokenizer = nltk.PunktTokenizer(lang="german")

    # creating connections

    logging.info("creating mongo client")
    mongo_client = create_mongo_client()

    mongo_db = mongo_client.get_database("bundestag")
    mongo_protocols_collection = mongo_db.get_collection(name="protokolle")
    mongo_delegated_collection = mongo_db.get_collection(name='mdb_stammdaten')

    mongo_protocol_ids: t.List[int] = [doc['id'] for doc in mongo_protocols_collection.find({}, {'id': 1})]

    logging.info("creating chroma client")
    chroma_client = create_chroma_client()
    chroma_protocol_collection = chroma_client.get_or_create_collection(name="protocols")
    embedding_function = create_chroma_embedding_function()

    # loading synced

    synced_protocols_file = Path.cwd() / "synced.json"

    synced_protocols: t.List[int]
    if synced_protocols_file.is_file():
        logging.info("loading synced protocols from %s", synced_protocols_file)
        with open(synced_protocols_file, "r") as f:
            synced_protocols = json.load(fp=f)
    else:
        logging.info("creating synced protocols as file does not exist (%s)", synced_protocols_file)
        synced_protocols = []

    # speaker fetching

    @lru_cache(maxsize=256)
    @add_logging()
    def get_speaker_by_id(id_: str) -> t.Optional[t.Dict[str, t.Any]]:
        return mongo_delegated_collection.find_one({'id': id_})

    # syncing

    logging.info("Starting actual sync")

    for protocol_id in mongo_protocol_ids:
        protocol = mongo_protocols_collection.find_one({'id': protocol_id})
        if protocol is None:
            logging.error("Protocol %s disappeared", protocol_id)
            continue

        if protocol_id in synced_protocols:
            logging.info("Skipping protocol %s as it's already synced", protocol_id)
            continue

        logging.info("syncing protocol %s", protocol_id)

        date = datetime.datetime.strptime(protocol['datum'], '%d.%m.%Y').date().toordinal()

        for session_index, session in enumerate(protocol["sitzungsverlauf"]):
            logging.info("syncing protocol %s - session #%d", protocol_id, session_index)

            ids: t.List[str] = []
            documents: t.List[str] = []
            embeddings: chromadb.Embeddings = []
            metadatas: t.List[t.Dict[str, t.Any]] = []

            for speach_index, speach in enumerate(session["rede"]):
                logging.info("syncing %d - session #%d - speach #%d", protocol_id, session_index, speach_index)

                text = speach['text']

                if not text:
                    logging.info("skipping speach cause text is empty")
                    continue

                speaker_id = speach['redner_id']
                speaker = get_speaker_by_id(speaker_id)

                sentences: t.List[str] = []

                for sentence_index, sentence in enumerate(sent_tokenizer.tokenize(text)):
                    ids.append(create_vector_id(
                        protocol_id=protocol_id,
                        session_index=session_index,
                        speach_index=speach_index,
                        sentence_index=sentence_index,
                    ))
                    logging.debug("Sentence: %r", sentence)
                    sentences.append(sentence)
                    metadatas.append(dict(
                        speaker_id=speaker_id,
                        party=speaker['fraktion'].casefold() if speaker else '', # chroma does not accept None values
                        date=date,
                    ))

                logging.info("syncing %d - session #%d - speach #%d - generating embeddings", protocol_id, session_index, speach_index)
                documents.extend(sentences)
                embeddings.extend(embedding_function(input=sentences))

            logging.info("protocol %s - session #%d - upsert", protocol_id, session_index)
            if ids:
                chroma_protocol_collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

        synced_protocols.append(protocol_id)

        logging.info("writing synced protocols to %s", synced_protocols_file)
        with open(synced_protocols_file, "w") as f:
            json.dump(synced_protocols, fp=f)

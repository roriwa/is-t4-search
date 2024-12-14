# -*- coding=utf-8 -*-
r"""

"""
import logging

from datetime import datetime
import uuid
from pymongo import MongoClient

from t4search.core.builder import create_chroma_client

def __main__():
    logging.info("SYNC")

    # Verbindung zur MongoDB
    client = MongoClient("mongodb://reader:mongoDB_bundestag-projekt@infosys1.f4.htw-berlin.de:27017/bundestag")
    db = client["bundestag"]

    # Daten aus den Kollektionen abfragen
    protocol_data = db["protokolle"].find({})
    deputy_data = db["mdb_stammdaten"].find({})


    speach_ids = []
    speach_texts = [] # volltext rede
    metadatas = [] # datum und redner id

    chroma_client = create_chroma_client()

    # Zerlegen der Sitzung in die einzelnen Reden
    # Danach speichern der einzelnen Redetexte, eine ID und die Metdadaten 
    for sitzung in protocol_data:
        for id_x, speach_obj in enumerate(sitzung["sitzungsverlauf"]):
            for speach in speach_obj["rede"]:

                # Rededaten
                speach["id"] = str(uuid.uuid1()) #zum späteren Identifizieren der gefundenen Rede
                speach_id = speach["id"] 
                speach_ids.append(speach_id)
                speach_texts.append(speach["text"])

                # Metadaten
                date_str = sitzung["datum"]
                date = datetime.strptime(date_str, "%d.%m.%Y").timestamp() 
                
                speaker = speach["redner_id"]
                metadata = {"date": date_str, "speaker": speaker}
                metadatas.append(metadata)

                # Erstellen und befüllen der Collection 
                protokolle_coll = chroma_client.get_or_create_collection(name="protocols")
                protokolle_coll.upsert(ids=speach_ids, documents=speach_texts, metadatas=metadatas)

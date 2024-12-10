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
    
    logging.info("SYNC - CONNECTED TO DB")

    # Daten aus den Kollektionen abfragen
    protokolle = db["protokolle"].find({})
    abgeordnete = db["mdb_stammdaten"].find({})


    rede_ids = []
    rede_texts = [] # volltext rede
    metadatas = [] # datum und redner id

    # Zerlegen der Sitzung in die einzelnen Reden
    # Danach speichern der einzelnen Redetexte, eine ID und die Metdadaten 
    for sitzung in protokolle:
        for id_x, rede_obj in enumerate(sitzung["sitzungsverlauf"]):
            for rede in rede_obj["rede"]:

                # Rededaten
                rede["id"] = str(uuid.uuid1()) #zum späteren Identifizieren der gefundenen Rede
                rede_id = rede["id"] 
                rede_ids.append(rede_id)
                rede_texts.append(rede["text"])

                # Metadaten
                
                date_str = sitzung["datum"]
                date = datetime.strptime(date_str, "%d.%m.%Y").timestamp() 
                speaker = rede["redner_id"]
                metadata = {"date": date, "speaker": speaker}
                metadatas.append(metadata)

                chroma_client = create_chroma_client()

                # Erstellen und befüllen der Collection 
                protokolle_coll = chroma_client.create_collection(name="protokolle_coll")
                protokolle_coll.add(ids=rede_ids, documents=rede_texts, metadatas=metadatas)

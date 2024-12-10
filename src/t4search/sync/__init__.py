# -*- coding=utf-8 -*-
r"""

"""
import logging

from bson import json_util
from datetime import datetime
import chromadb
import pprint, uuid

def __main__():
    logging.info("SYNC")


# Laden der gespeicherten Protokolldaten
with open('protokolle.json') as json_file:
    data_str = json_file.read()
protokolle_json = json_util.loads(data_str)

rede_ids = []
rede_texts = [] # volltext rede
metadatas = [] # datum und redner id

# Zerlegen der Sitzung in die einzelnen Reden
# Danach speichern der einzelnen Redetexte, eine ID und die Metdadaten 
for sitzung in protokolle_json:
    sitzungs_id = sitzung["id"]
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

            chroma_client = crea

            # Erstellen und befüllen der Collection 
            protokolle_coll = chroma_client.create_collection(name="protokolle_coll")
            protokolle_coll.add(ids=rede_ids, documents=rede_texts, metadatas=metadatas)

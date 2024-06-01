import json
import os
from data_collector.dataProcessing import *

###################################################
#    Chargement des données et dl si nécessaire   #
###################################################

def load_data(data : str):
    splited_data = data.split(">")
    clean_data = splited_data[0]
    processData(clean_data)
    # Charger les données JSON depuis un fichier ou une variable
    with open("data/"+clean_data+".json", "r", encoding="utf-8") as file:
        dataJSON = json.load(file)
    return dataJSON

###################################################
#   Traitement du tuple JSON en langage naturel   #
###################################################

def JSON_to_nat(jsonFile : list, jsonLine : list):
    data_dict = json.loads(jsonFile)
    nodes = data_dict["noeud"]
    type_relations = data_dict["type_relation"]

    type, eid1, eid2 = jsonLine["type"], jsonLine["node1"], jsonLine["node2"]
    word1 = next((node for node in nodes if node["eid"] == eid1), None)
    word2 = next((node for node in nodes if node["eid"] == eid2), None)
    relation = next((type_relation for type_relation in type_relations if type_relation["rtid"] == type), None)

    return word1["name"], relation["trname"], word2["name"]

###################################################
#            Fonction de nettoyage               #
###################################################
def clear_console():
    # Efface la console en imprimant 100 retours à la ligne
    os.system('cls' if os.name == 'nt' else 'clear')  # Pour Windows et Unix/Linux
    
###################################################
#             Fonctions utilitaires               #
###################################################

def node_id_to_name(id, dataJSON):
  return str(dataJSON["noeud"][str(id)]["name"]).split(">")[0]

def node_name_to_id(data, dataJSON):
  noeuds = dataJSON["noeud"]
  for cle, valeur in noeuds.items():
    if (valeur.get("name") == data):
      return int(cle)
    
def relation_id_to_name(id, dataJSON):
  return str(dataJSON["type_relation"][id]["trname"]).split(">")[0]

def relation_name_to_id(data, dataJSON):
  relations = dataJSON["type_relation"]
  for cle, valeur in relations.items():
    if (valeur.get("trname") == data):
      return int(cle)
    
###################################################
#        Fonctions d'interrogation simple         #
###################################################

def relation_existe(data1, data2, relation, dataJSON):
  relations = dataJSON["relation"]
  for cle, valeur in relations.items() :
    if(int(valeur["type"]) == relation_name_to_id(relation, dataJSON)):
      if (int(valeur["node1"]) == node_name_to_id(data1, dataJSON)):
        if (int(valeur["node2"]) == node_name_to_id(data2, dataJSON)):
          if (int(valeur["node2"]) == node_name_to_id(data2, dataJSON)):
            if (int(valeur["w"]) > 0.0):
              return "vrai"
            else :
              return "faux"
  return "nsp"


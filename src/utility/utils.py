import json
import math
import os
import statistics
from data_collector.dataProcessing import *

###################################################
#    Chargement des données et dl si nécessaire   #
###################################################

def load_data(data: str):
    clean_data = data.split(">")
    if len(clean_data) > 1:
        clean_data = clean_data[0]
    else:
        clean_data = data
    retour = processData(clean_data)
    if(retour != "erreur"):
        with open(f"data/{clean_data}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {"type_noeud": {},"noeud": {}, "type_relation": {}, "relation":{}}

###################################################
#   Traitement du tuple JSON en langage naturel   #
###################################################

def JSON_to_nat(jsonFile: dict, jsonLine: dict):
    nodes = {node["eid"]: node["name"] for node in jsonFile["noeud"]}
    type_relations = {rel["rtid"]: rel["trname"] for rel in jsonFile["type_relation"]}

    type_id, eid1, eid2 = jsonLine["type"], jsonLine["node1"], jsonLine["node2"]
    word1 = nodes.get(eid1)
    word2 = nodes.get(eid2)
    relation = type_relations.get(type_id)

    return word1, relation, word2

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
    try:
        return dataJSON["noeud"][str(id)]["name"].split('>', 1)[0]
    except KeyError:
        return None

def node_name_to_id(data, dataJSON):
    try:
        return next(int(k) for k, v in dataJSON["noeud"].items() if v.get("name") == data)
    except StopIteration:
        return None
    
def relation_id_to_name(id, dataJSON):
    try:
        return dataJSON["type_relation"][str(id)]["trname"].split('>', 1)[0]
    except KeyError:
        return None

def relation_name_to_id(data, dataJSON):
    try:
        return next(int(k) for k, v in dataJSON["type_relation"].items() if v.get("trname") == data)
    except StopIteration:
        return None
    
###################################################
#        Fonctions d'interrogation simple         #
###################################################

def relation_existe(data1, data2, relation, dataJSON):
    type_id = relation_name_to_id(relation, dataJSON)
    node1_id = node_name_to_id(data1, dataJSON)
    node2_id = node_name_to_id(data2, dataJSON)
    
    relations = dataJSON["relation"]
    
    for valeur in relations.values():
        if int(valeur.get("type")) == type_id and int(valeur.get("node1")) == node1_id and int(valeur.get("node2")) == node2_id:
            if float(valeur.get("w", 0.0)) > 0.0:
                return "vrai"
            else:
                return "faux"
    
    return "nsp"

###################################################
#                    Moyennes                     #
###################################################

def moyenne_geo(data):
    produit = 1.0
    n = len(data)
    for valeur in data:
        produit *= valeur
    return produit ** (1/n)

def mediane(data):
    return statistics.median(data)

def moyenne_quad(data):
    somme_des_carres = sum(x ** 2 for x in data)
    n = len(data)
    return math.sqrt(somme_des_carres / n)

###################################################
#          Vérification alphanumérique            #
###################################################

def contains_alphanumeric(s):
    alnum =  any(c.isalnum() for c in s)
    ponct = all(c!="?" for c in s)
    return alnum and ponct
import json
import os
from data_collector.dataProcessing import *
from reasoner import *

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


#############
# INDUCTION #
#############
def interrogation_induction(data_1_, data_2_, relation, dataJSON1, dataJSON2):
    """
    cette fonction permet de trouver une relation inductive pour justifier une propriété
    @param data_1 : str : nom de la première donnée
    @param data_2 : str : nom de la deuxième donnée
    @param relation : str : nom de la relation
    @param dataJSON1 : dict : données de la première donnée
    @param dataJSON2 : dict : données de la deuxième donnée
    @return validite : list : validité de la propriété
    """
    """
        Exemple :
        * inductive = trouve un spécifique pour lequel la répons est vraie

        chat r_agent-1 miauler  ⇒ oui car  
        chat r_syn chat de gouttière et  chat de gouttière r_agent-1 miauler

    """
    list_valide = []

    

    # Extraire les noeuds et les relations
    nodes_1 = dataJSON1["noeud"]
    relations_1 = dataJSON1["relation"]
    types_relations_1 = dataJSON1["type_relation"]
    nodes_2 = dataJSON2["noeud"]
    relations_2 = dataJSON2["relation"]
    types_relations_2 = dataJSON2["type_relation"]

    # Trouver les noeuds correspondant aux noms donnés
    data_1 = next((eid for eid, node in nodes_1.items() if node["name"] == data_1_), None)
    data_2 = next((eid for eid, node in nodes_2.items() if node["name"] == data_2_), None)
    
    data_1 = int(data_1)
    data_2 = int(data_2)
    print(data_2)

    # num relation entrer
    relation_type_id_base = next((cle for cle, valeur in types_relations_2.items() if valeur["trname"] == relation), None)
    print(relation_type_id_base)
    
    # type relation r_syn
    relation_type_id = next((rtid for rtid, relation in types_relations_1.items() if relation["trname"] == "r_syn"), None)
    if relation_type_id is None:
        relation_type_id = next((rtid for rtid, relation in types_relations_2.items() if relation["trname"] == "r_syn"), None)

    # trie dans l ordre croissant
    list_relations_match = [cle for cle, valeur in relations_1.items() if valeur["node1"] == data_1 and valeur["type"] == int(relation_type_id)]

    # trie les relations en fonction du rang (si le rang est disponible)
    list_relations_match.sort(key=lambda x: relations_1[x].get('rank', float('inf')) if relations_1[x].get('rank') is not None else float('inf'))
    #print("list relation match first mot and r_sin : ",list_relations_match)

    for relation_key in list_relations_match:
        # si il y a plus de 10 element dans la liste on arrete
        if len(list_valide) > 10:
            break
        # recuperer la relation 1
        relation_1_ok = relations_1[str(relation_key)]

        for cle, valeur in relations_2.items():
            if valeur["node1"] == relation_1_ok["node2"]  and valeur["type"] == int(relation_type_id_base) and valeur["node2"] == data_2:
                list_valide.append((relation_1_ok, valeur))

    return list_valide
    

if __name__ == "__main__":
    data1 = input("data 1 : ")
    data2 = input("data 2 : ")
    relation = input("relation : ")
    dataJSON1 = None
    dataJSON2 = None
    try:
        dataJSON1 = load_data(data1)
        dataJSON2 = load_data(data2)
    except AttributeError as ae :
        print("Saisi incorrect")

    #pbdonc je charge le fichier moi meme
    
    # Charger les données JSON depuis le fichier
    """path_1 = "C:\\Users\\Home\\Documents\\GitHub\\ChatBot-LangageNaturel\\data\\" + str(data1) + ".json"
    with open(path_1, "r", encoding="utf-8") as file:
        dataJSON1 = json.load(file)
    # Charger les données JSON depuis le fichier
    path_2 = "C:\\Users\\Home\\Documents\\GitHub\\ChatBot-LangageNaturel\\data\\" + str(data2) + ".json"
    with open(path_2, "r", encoding="utf-8") as file:
        dataJSON2 = json.load(file)"""

        
    validite1 = interrogation_induction(data1, data2, relation, dataJSON1, dataJSON2)
    for i in validite1:
        print(i)
    

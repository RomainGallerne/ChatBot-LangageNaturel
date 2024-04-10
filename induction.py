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

    # num relation entrer
    relation_type_id_base = next((cle for cle, valeur in types_relations_2.items() if valeur["trname"] == relation), None)
    
    # type relation r_syn
    relation_type_id = next((rtid for rtid, relation in types_relations_1.items() if relation["trname"] == "r_syn"), None)
    if relation_type_id is None:
        relation_type_id = next((rtid for rtid, relation in types_relations_2.items() if relation["trname"] == "r_syn"), None)

    # chercher relation dans fichier 1
    list_relations_match = [cle for cle, valeur in relations_1.items() if valeur["node1"] == data_1 and valeur["type"] == int(relation_type_id)]

    # trie les relations en fonction du poid
    list_relations_match.sort(key=lambda x: abs(relations_1[x].get('w')),reverse=True)

    for relation_key in list_relations_match:
        # si il y a plus de 5 element dans la liste on arrete
        if len(list_valide) > 5:
            break
        # recuperer la relation 1
        relation_1_ok = relations_1[str(relation_key)]

        for cle, valeur in relations_2.items() :
            if(int(valeur["type"]) == int(relation_type_id_base)):
                if (int(valeur["node1"]) == int(relation_1_ok["node2"])):
                    if (int(valeur["node2"]) == int(data_2)):
                        list_valide.append((relation_1_ok, valeur))

    return list_valide

###################################################
#          Fonctions de déduction Propre          #
###################################################

    #arguments_global
    #[relation_rank, relation_weight, element1_generique_w, rank_1, element2_generique_w, rank_2, element1_generique, element2_generique]

def get_clean_induction_results(data1, data2, relation, dataJSON1, dataJSON2): 
    resultat_global = 0.0
    inductions = []
    dicos = interrogation_induction(data1, data2, relation, dataJSON1, dataJSON2)
    for dico_induction in dicos:
    
        #formation du tableau de réponse
        list_indcution = []
        if(dico_induction[1]["rank"] == None): #relation_rank
            list_indcution.append(20.0)
        else:
            list_indcution.append(dico_induction[1]["rank"])
        list_indcution.append(dico_induction[1]["w"]) #relation_weight
        list_indcution.append(dico_induction[0]["w"]) #element1_generique_w
        if(dico_induction[0]["rank"] == None):
            list_indcution.append(20.0) #rank_1
        else:
            list_indcution.append(dico_induction[0]["rank"])
        list_indcution.append(None) #element2_generique_w
        list_indcution.append(None) #rank_2
        list_indcution.append(node_id_to_name(dico_induction[0]["node2"],dataJSON1)) #element1_generique
        list_indcution.append(None) #element2_generique

        #calcul de confiance et de score
        confiance = 3*min((float(list_indcution[1])),float(list_indcution[2])) / max(float(list_indcution[0]),float(list_indcution[3]))
        list_indcution.append(abs(confiance))
        if(list_indcution[1] > 0):
            resultat_global += list_indcution[8]
        elif(list_indcution[1] < 0):
            resultat_global -= 2*list_indcution[8]

        inductions.append(list_indcution)
    return inductions[:5], resultat_global

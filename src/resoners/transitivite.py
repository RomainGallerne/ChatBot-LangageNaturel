from math import sqrt, pow
from utility.utils import *

###################################################
#         Recherche d'éléments génériques         #
###################################################

recherche_transitifs = set([
    0, 3, 4, 5, 6, 8, 9, 10, 15, 17, 19, 22, 23, 27, 28, 41, 42, 52, 57, 61, 67, 72, 73, 74, 75, 83, 111, 113, 121, 122, 124, 125, 129, 130, 142, 153, 161, 167, 168, 169, 171
])

def list_elem_relation(data, relation_id, dataJSON):
    if relation_id not in recherche_transitifs:
        return None

    relations = dataJSON["relation"].items()
    elements = []
    data_id = node_name_to_id(data, dataJSON)

    for k, v in relations:
        if v["node1"] == data_id and v["type"] in recherche_transitifs and v["rank"] is not None and v["rank"] <= 10:
            elements.append({"poid": v["wnormed"] or 1.0, "element": v["node2"], "type": v["type"]})
            if len(elements) >= 10:
                break

    elements.sort(key=lambda item: abs(item["poid"]), reverse=True)
    return elements

###################################################
#            Fonctions de déduction               #
###################################################

def transitivite(data1, data2, relation, dataJSON1, dataJSON2):
    """
    Calcule les transtivités basées sur les relations entre data1 et data2 en utilisant les données JSON fournies.

    Parameters:
    data1 (str): Le premier élément de la relation.
    data2 (str): Le deuxième élément de la relation.
    relation (str): Le type de relation entre data1 et data2.
    dataJSON1 (dict): Dictionnaire JSON contenant des informations supplémentaires pour data1.
    dataJSON2 (dict): Dictionnaire JSON contenant des informations supplémentaires pour data2.

    Returns:
    list: Une liste de transtivités, chaque déduction étant un dictionnaire contenant les informations suivantes :
        - rank_relation (float): Le rang de la relation.
        - weight_relation (float): Le poids de la relation.
        - rank_element_1 (float, optional): Le rang de l'élément 1.
        - weight_element_1 (float, optional): Le poids de l'élément 1.
        - rank_element_2 (float, optional): Le rang de l'élément 2.
        - weight_element_2 (float, optional): Le poids de l'élément 2.
        - element1 (str, optional): Le nom de l'élément 1.
        - element2 (str, optional): Le nom de l'élément 2.
    """
    # Elements utilitaires
    transitivites = []
    data2_id = node_name_to_id(data2, dataJSON2)
    relation_id = relation_name_to_id(relation, dataJSON1)

    elements1 = list_elem_relation(data1, relation_id, dataJSON1)

    if(elements1 is not None):
        # Recherche des relations dans lesquelles data1 est en relation avec X, et X est en relation avec data2
        for element in elements1:
            name = node_id_to_name(element["element"], dataJSON1)
            if(not contains_alphanumeric(element)):
                continue
            dataJSON_element = load_data(name)  # Chargement des données nécessaires
            relations_dataJSON_element = dataJSON_element["relation"]

            for valeur in relations_dataJSON_element.values():
                if valeur["type"] == relation_id and valeur["node1"] == element["element"] and valeur["node2"] == data2_id:
                    transitivites.append({
                        "weight_relation": valeur["wnormed"] or 1.0,
                        "weight_element_1": element["poid"],
                        "weight_element_2": None,
                        "element1": str(node_id_to_name(element["element"], dataJSON1)),
                        "element2": None,
                        "relation1": element["type"],
                        "relation2": None
                    })

        return transitivites
    else: return []

###################################################
#          Fonctions de déduction Propre          #
###################################################

def get_clean_transitivite_results(data1, data2, relation, dataJSON1, dataJSON2):
    """
    Calcule les résultats de déduction nettoyés et ordonnés en fonction de la confiance et du poids de la relation.

    Parameters:
    data1 (Any): Données de la première source.
    data2 (Any): Données de la deuxième source.
    relation (Any): Informations de la relation entre les données.
    dataJSON1 (dict): Dictionnaire JSON contenant des informations supplémentaires pour data1.
    dataJSON2 (dict): Dictionnaire JSON contenant des informations supplémentaires pour data2.

    Returns:
    tuple: Un tuple contenant deux éléments :
        - list : Les 10 premières déductions triées par confiance décroissante.
        - float : Le résultat global des poids de la relation, ajusté pour les relations négatives.
    """
    transitivites = transitivite(data1, data2, relation, dataJSON1, dataJSON2)

    resultat_global = 0
    for tran in transitivites:
        weight_relation = tran["weight_relation"]
        resultat_global += weight_relation

<<<<<<< HEAD
        # On booste les relations négatives pour ne pas les rater
        if weight_relation < 0.0:
            resultat_global -= pow(weight_relation, 3.0)
=======
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
    #print(data_2)

    # num relation entrer
    relation_type_id_base = next((cle for cle, valeur in types_relations_2.items() if valeur["trname"] == relation), None)
    #print(relation_type_id_base)

    # chercher relation dans le fichier 1 
    list_relations_match = [cle for cle, valeur in relations_1.items() if valeur["node1"] == data_1 and valeur["type"] == int(relation_type_id_base) and valeur["node2"] != data_2]#and valeur["node2"] != data_2
    #print(list_relations_match)

    # trie les relations en fonction du rang (si le rang est disponible)
    list_relations_match.sort(key=lambda x: relations_1[x].get('rank', float('inf')) if relations_1[x].get('rank') is not None else float('inf'))
    #print("list relation match first mot and r_sin : ",list_relations_match)
    #print([relations_1[str(relation_key)]for relation_key in list_relations_match])

    for relation_key in list_relations_match:
        # si il y a plus de 10 element dans la liste on arrete
        if len(list_valide) > 10:
            break
        # recuperer la relation 1
        relation_1_ok = relations_1[str(relation_key)]

        #Charger nouveau fichier trouve
        # nom du de l id du noeud dans relation_1_ok[node2]
        name = next((node["name"] for eid, node in nodes_1.items() if int(eid) == relation_1_ok["node2"]), None)
        #print(f"nom : {name}")
        dataJSON3 = load_data(name)
        relations_3 = dataJSON3["relation"]
        for cle, valeur in relations_3.items():
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
>>>>>>> c4cf63a601311c38d377aa00380437559f64ba35

        relation_weight = float(weight_relation)
        
        if tran["element1"] is not None and tran["element2"] is not None:
            generique_weight = float(tran["weight_element_1"]) + float(tran["weight_element_2"])
            confiance = moyenne_geo([abs(generique_weight), abs(relation_weight)])
        elif tran["element1"] is not None:
            generique_weight = float(tran["weight_element_1"])
            confiance = moyenne_geo([abs(generique_weight), abs(relation_weight)])
        elif tran["element2"] is not None:
            generique_weight = float(tran["weight_element_2"])
            confiance = moyenne_geo([abs(generique_weight), abs(relation_weight)])
        else:
            confiance = 0.0

        tran["confiance"] = abs(confiance)
        
    unique_transitivites = {}
    for tran in transitivites:
        key = (tran["element1"], tran["element2"])
        if key in unique_transitivites:
            if tran["confiance"] > unique_transitivites[key]["confiance"]:
                unique_transitivites[key] = tran
        else:
            unique_transitivites[key] = tran

    deduped_transitivites = list(unique_transitivites.values())
    deduped_transitivites.sort(key=lambda x: x["confiance"], reverse=True)

    return deduped_transitivites, resultat_global
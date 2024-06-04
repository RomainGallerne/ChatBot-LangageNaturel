from math import sqrt, pow
from utility.utils import *

###################################################
#         Recherche d'éléments génériques         #
###################################################

relations_generiques = [
    6, #r_isa
    10, #r_holo
]

def recherche_generique(data, dataJSON):
    relations = dataJSON["relation"].items()
    generiques = []
    data_id = node_name_to_id(data, dataJSON)

    for k, v in relations:
        if(v["rank"] is None):
            continue
        if v["node1"] == data_id and v["type"] in relations_generiques and v["rank"] <= 10:
            generiques.append({"poid": v["wnormed"] or 1.0, "element": v["node2"], "type": v["type"]})

    generiques.sort(key=lambda item: abs(item["poid"]), reverse=True)
    return generiques

###################################################
#            Fonctions de déduction               #
###################################################

def deduction(data1, data2, relation, dataJSON1, dataJSON2):
    """
    Calcule les déductions basées sur les relations entre data1 et data2 en utilisant les données JSON fournies.

    Parameters:
    data1 (str): Le premier élément de la relation.
    data2 (str): Le deuxième élément de la relation.
    relation (str): Le type de relation entre data1 et data2.
    dataJSON1 (dict): Dictionnaire JSON contenant des informations supplémentaires pour data1.
    dataJSON2 (dict): Dictionnaire JSON contenant des informations supplémentaires pour data2.

    Returns:
    list: Une liste de déductions, chaque déduction étant un dictionnaire contenant les informations suivantes :
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
    deductions = []
    data2_id = node_name_to_id(data2, dataJSON2)
    relation_id = relation_name_to_id(relation, dataJSON1)

    elements = recherche_generique(data1, dataJSON1)
    name_cache = {elem["element"]: node_id_to_name(elem["element"], dataJSON1) for elem in elements}
    data_cache = {name: load_data(name) for name in name_cache.values() if name is not None and contains_alphanumeric(name)}

    # Recherche des relations dans lesquelles data1 est un X, et X est en relation avec data2
    for element in elements:
        elem_name = element["element"]
        
        if elem_name in name_cache:
            name_cache_elem = name_cache[elem_name]
            if(name_cache_elem == "::" or "?" in name_cache_elem):
                continue
            dataJSON_element = data_cache[name_cache_elem]
            relations_dataJSON_element = dataJSON_element["relation"]
            for valeur in relations_dataJSON_element.values():
                if valeur["type"] == relation_id and valeur["node1"] == elem_name and valeur["node2"] == data2_id:
                    deductions.append({
                        "weight_relation": valeur["wnormed"] or 1.0,
                        "weight_element_1": element["poid"],
                        "element1": str(name_cache_elem),
                        "relation1": element["type"],
                    })
    return deductions

###################################################
#          Fonctions de déduction Propre          #
###################################################

def get_clean_deduction_results(data1, data2, relation, dataJSON1, dataJSON2):
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
    deductions = deduction(data1, data2, relation, dataJSON1, dataJSON2)

    resultat_global = 0
    for ded in deductions:
        weight_relation = ded["weight_relation"]
        resultat_global += weight_relation

        # On booste les relations négatives pour ne pas les rater
        if weight_relation < 0.0:
            resultat_global += 3.0 * weight_relation

        generique_weight = float(ded["weight_element_1"])
        confiance = moyenne_geo([abs(generique_weight), abs(weight_relation)])
        ded["confiance"] = confiance

    deductions.sort(key=lambda x: x["confiance"], reverse=True)

    return deductions, resultat_global
from math import sqrt, pow
from utility.utils import *

###################################################
#           Recherche d'éléments typiques         #
###################################################

def recherche_typique(data, dataJSON):
  relations = dataJSON["relation"]
  data_id = int(node_name_to_id(data, dataJSON))
  typiques = []
  nb_typiques = 0
  for cle, valeur in relations.items():
    if(nb_typiques >= 5):
       break
    try:
      if (int(valeur["node1"])==data_id) and (int(valeur["type"])==13 and int(valeur["rank"])<=10): # La relation r_agent a pour id 13
        typiques.append([valeur["rank"] or 11.0,valeur["node2"]])
        nb_typiques += 1
    except TypeError :
      continue
  return [typique[1] for typique in typiques][:8]

###################################################
#         Recherche d'éléments génériques         #
###################################################

def recherche_generique(data, dataJSON):
  relations_generiques = [relation_name_to_id("r_isa",dataJSON), relation_name_to_id("r_holo",dataJSON)]

  relations = dataJSON["relation"]
  generiques = []
  data_id = int(node_name_to_id(data, dataJSON))

  relations = {k: v for k, v in relations.items() if v["node1"] == data_id and v["type"] in relations_generiques}

  for relation in relations.values() :
    generiques.append({"rank": relation["rank"],"poid": relation["w"],"element": relation["node2"], "type": relation["type"]})

  generiques = sorted(generiques, key=lambda item: abs(item["poid"]), reverse=True)
  return generiques[:8]

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
    relations_dataJSON1 = dataJSON1["relation"]
    relations_dataJSON2 = dataJSON2["relation"]
    deductions = []
    data1_id = node_name_to_id(data1, dataJSON1)
    data2_id = node_name_to_id(data2, dataJSON2)
    relation_id = relation_name_to_id(relation, dataJSON1)

    # Recherche des éléments typiques de la donnée data2 (qui peut faire data2 ?)
    #typiques = recherche_typique(data2, dataJSON2)

    #if len(typiques) != 0:
        # Si l'élément a des typiques, on ne s'intéresse qu'à eux
        #if(data1_id in typiques):
          #elements1 = recherche_generique(data1, dataJSON1)
        #else: elements1 = typiques
    #else:
        # Sinon on prend tous les génériques
        #elements1 = recherche_generique(data1, dataJSON1)

    elements1 = recherche_generique(data1, dataJSON1)
    elements2 = recherche_generique(data2, dataJSON2)

    # Recherche des relations dans lesquelles data1 est un X, et X est en relation avec data2
    for element in elements1:
        for valeur in relations_dataJSON2.values():
            if valeur["type"] == relation_id and valeur["node1"] == element["element"] and valeur["node2"] == data2_id:
                deductions.append({
                    "rank_relation": valeur["rank"] if valeur["rank"] is not None else 11.0,
                    "weight_relation": valeur["w"],
                    "rank_element_1": element["rank"] if element["rank"] is not None else 11.0,
                    "weight_element_1": element["poid"],
                    "rank_element_2": None,
                    "weight_element_2": None,
                    "element1": str(node_id_to_name(element["element"], dataJSON1)),
                    "element2": None,
                    "relation1": element["type"],
                    "relation2": None
                })

    # Recherche des relations dans lesquelles data2 est un Y, et data1 est en relation avec Y
    for element in elements2:
        for valeur in relations_dataJSON1.values():
            if valeur["type"] == relation_id and valeur["node2"] == element["element"] and valeur["node1"] == data1_id:
                deductions.append({
                    "rank_relation": valeur["rank"] if valeur["rank"] is not None else 11.0,
                    "weight_relation": valeur["w"],
                    "rank_element_1": None,
                    "weight_element_1": None,
                    "rank_element_2": element["rank"] if element["rank"] is not None else 11.0,
                    "weight_element_2": element["poid"],
                    "element1": None,
                    "element2": str(node_id_to_name(element["element"], dataJSON2)),
                    "relation1": None,
                    "relation2": element["type"]
                })

    # Recherche des relations dans lesquelles data1 est un X, et data2 est un Y, et X est en relation avec Y
    for element1 in elements1:
        name = node_id_to_name(element1["element"], dataJSON1)
        if(not contains_alphanumeric(name)):
           continue
        dataJSON_element = load_data(name)  # Chargement des données nécessaires
        relations_dataJSON_element = dataJSON_element["relation"]

        for valeur in relations_dataJSON_element.values():
            if valeur["type"] == relation_id and valeur["node1"] == element1["element"] and valeur["node2"] in elements2:
                for element2 in elements2:
                    if valeur["node2"] == element2["element"]:
                        deductions.append({
                            "rank_relation": valeur["rank"] if valeur["rank"] is not None else 11.0,
                            "weight_relation": valeur["w"],
                            "rank_element_1": element1["rank"] if element1["rank"] is not None else 11.0,
                            "weight_element_1": element1["poid"],
                            "rank_element_2": element2["rank"] if element2["rank"] is not None else 11.0,
                            "weight_element_2": element2["poid"],
                            "element1": str(node_id_to_name(element1["element"], dataJSON1)),
                            "element2": str(node_id_to_name(element2["element"], dataJSON2)),
                            "relation1": element1["type"],
                            "relation2": element2["type"]
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
            resultat_global -= pow(weight_relation, 3.0)

        relation_weight = float(weight_relation)
        relation_rank = float(ded["rank_relation"])
        
        if ded["element1"] is not None and ded["element2"] is not None:
            generique_rank = float(ded["rank_element_1"]) + float(ded["rank_element_2"])
            generique_weight = float(ded["weight_element_1"]) + float(ded["weight_element_2"])
            confiance = math.sqrt(abs(moyenne_quad([generique_weight, relation_weight]) / moyenne_quad([generique_rank, relation_rank])))
        elif ded["element1"] is not None:
            generique_rank = float(ded["rank_element_1"])
            generique_weight = float(ded["weight_element_1"])
            confiance = abs(moyenne_quad([generique_weight, relation_weight]) / moyenne_quad([generique_rank, relation_rank]))
        elif ded["element2"] is not None:
            generique_rank = float(ded["rank_element_2"])
            generique_weight = float(ded["weight_element_2"])
            confiance = math.sqrt(abs(moyenne_quad([generique_weight, relation_weight]) / moyenne_quad([generique_rank, relation_rank])))
        else:
            confiance = 0.0

        ded["confiance"] = abs(confiance)
        
    unique_deductions = {}
    for ded in deductions:
        key = (ded["element1"], ded["element2"])
        if key in unique_deductions:
            if ded["confiance"] > unique_deductions[key]["confiance"]:
                unique_deductions[key] = ded
        else:
            unique_deductions[key] = ded

    deduped_deductions = list(unique_deductions.values())
    deduped_deductions.sort(key=lambda x: x["confiance"], reverse=True)

    return deduped_deductions[:10], resultat_global
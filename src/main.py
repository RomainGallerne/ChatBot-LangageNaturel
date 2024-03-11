import json
from data_collector.dataProcessing import *

###################################################
#         Trouve une relation directe             #
###################################################

def find_relation_with_nodes_and_type(data, word1, word2, relation_type):
    # Convertir les données JSON en dictionnaires Python
    data_dict = json.loads(data)

    # Extraire les noeuds et les relations
    nodes = data_dict["noeud"]
    relations = data_dict["relation"]
    types_relations = data_dict["type_relation"]

    # Vérifier si les mots spécifiés sont présents dans les noeuds
    word1_node = next((node for node in nodes if node["name"] == word1), None)
    word2_node = next((node for node in nodes if node["name"] == word2), None)

    # Vérifier si le type de relation spécifié est présent dans les types de relation
    relation_type_info = next((rt for rt in types_relations if rt["trname"] == relation_type), None)

    if word1_node is None or word2_node is None or relation_type_info is None:
        return None

    # Rechercher toutes les relations qui contiennent les deux mots et le type de relation spécifié
    matching_relations = [rel for rel in relations if
                          (rel["node1"] == word1_node["eid"] and rel["node2"] == word2_node["eid"] and
                           rel["type"] == relation_type_info["rtid"]) or
                          (rel["node2"] == word1_node["eid"] and rel["node1"] == word2_node["eid"] and
                           rel["type"] == relation_type_info["rtid"])]

    if not matching_relations:
        return None

    # Trier les relations en fonction du rang (si le rang est disponible)
    matching_relations.sort(key=lambda x: x.get('rank', float('inf')) if x.get('rank') is not None else float('inf'))

    # Renvoyer la relation avec le rang le plus élevé
    return matching_relations[0]

###################################################
#    Chargement des données et dl si nécessaire   #
###################################################

def load_data(data1 : str, data2 : str):
    processData(data1)
    processData(data2)

    # Charger les données JSON depuis un fichier ou une variable
    with open("data/data.json", "r", encoding="utf-8") as file:
        dataJSON = file.read()

    return dataJSON

def simple_answer(dataJSON, data1, data2, relation):
    # Rechercher la relation correspondante
    found = find_relation_with_nodes_and_type(dataJSON, data1, data2, relation)

    if found:
        print("Relation trouvée :", found)
    else:
        print("Aucune relation trouvée pour les mots et le type de relation spécifiés.")


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
#              Fonction Principal                 #
###################################################

def main():
    data1 = input("data 1 :")
    data2 = input("data 2 :")
    relation = input("relation :")
    dataJSON = load_data(data1, data2)
    simple_answer = find_relation_with_nodes_and_type(dataJSON, data1, data2, relation)
    print(simple_answer)
    print(JSON_to_nat(dataJSON, simple_answer))

if __name__ == "__main__":
    main()
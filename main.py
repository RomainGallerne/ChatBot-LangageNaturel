import json
from collections import deque

###########################################################
# Fonctions pour la recherche indirecte version inductive #
###########################################################

def find_indirect_relation_deep_inductive(word1_node, word2_node, relation_type_info, relations, nodes, list_arguments, list_chemin, types_relations, depth=0):
    """
    Chercher une relation indirecte entre deux mots en utilisant
    @param word1_node: le noeud du premier mot
    @param word_node_cible: le noeud du deuxieme mot
    @param relation_type_info: le type de relation de base
    @param relations: list de relations disponibles
    @param nodes: liste des noeuds disponibles
    @param list_arguments: liste des arguments qui permetra de repondre à la question 
    @param list_chemin: liste des noeuds parcourus
    @param types_relations : list de touts les types de relations possibles
    @param depth: la profondeur de la relation
    @return: 
    """
    # verif si y a pas le noeud 1 avec la relation de base et le noeud 2
    matching_relations = [rel for rel in relations if (rel["node1"] == word1_node["eid"] and rel["node2"] == word2_node["eid"] and rel["type"] == relation_type_info["rtid"])]
    # si pas de relation directe trouvé, on cherche une relation indirecte (inductive) recursivement pour avoir tous les niveaux de relations
    if not matching_relations:
        # recuperer l ensemble des relations ou le noeud 1 est == a word1_node et que le type est "is_a"
        list_relations_match = [relation for relation in relations if relation["node1"] == word1_node["eid"] and ([relations_is_a for relations_is_a in types_relations if relations_is_a["trname"] == "r_isa"][0]["rtid"] == relation["type"])]
        # trie les relations en fonction du rang (si le rang est disponible)
        list_relations_match.sort(key=lambda x: x.get('rank', float('inf')) if x.get('rank') is not None else float('inf'))
        # parours en profondeur les relations
        for relation in list_relations_match:
            # recuperer le noeud associe a word1_node
            node2 = next((node for node in nodes if node["eid"] == relation["node2"]), None)
            # save la relation
            list_chemin.append(relation)
            # appeler la fonction recursivement
            find_indirect_relation_deep_inductive(node2, word2_node, relation_type_info, relations, nodes, list_arguments, list_chemin, types_relations, depth=depth+relation["rank"] if relation.get('rank') is not None else depth+0)
            # supprimer la derniere relation
            list_chemin.pop()
    else:
        list_chemin.append(matching_relations[0])
        list_arguments.append((list_chemin.copy(), depth + (matching_relations[0].get('rank', 0) or 0)))
        list_chemin.pop()
        return
        
def find_relation_with_nodes_and_type(data, word1, word2, relation_type):
    """
    Rechercher une relation entre deux mots en utilisant les noeuds et le type de relation spécifiés
    @param data: les données JSON
    @param word1: le premier mot
    @param word2: le deuxième mot
    @param relation_type: le type de relation
    @return: la justifiaction qui permet de repondre à la question
    """
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
    #####################
    # Recherche directe #
    #####################
    matching_relations = [rel for rel in relations if
                          (rel["node1"] == word1_node["eid"] and rel["node2"] == word2_node["eid"] and
                           rel["type"] == relation_type_info["rtid"]) or
                          (rel["node2"] == word1_node["eid"] and rel["node1"] == word2_node["eid"] and
                           rel["type"] == relation_type_info["rtid"])]

    # si pas de relation directe trouvé, on cherche une relation indirecte recursivement pour avoir tous les niveaux de relations
    #######################
    # Recherche indirecte #
    #######################
    list_arguments = []
    list_chemin = []
    if not matching_relations:
        # Chercher une relation indirecte
        # parours toues les realtion qui contiennent le mot1
        find_indirect_relation_deep_inductive(word1_node, word2_node, relation_type_info, relations, nodes, list_arguments, list_chemin, types_relations)
            
    matching_relations = list_arguments
    print("matching_relations", matching_relations)
    # Trier les relations en fonction de depth
    matching_relations.sort(key=lambda x: x[1])
    # Renvoyer la relation avec le rang le plus élevé
    return matching_relations[0] if matching_relations else None

def main():
    # Charger les données JSON depuis un fichier ou une variable
    with open("data/example.json", "r", encoding="utf-8") as file:
        data = file.read()

    # Entrer les mots et le type de relation
    word1 = input("Entrez le premier mot : ")
    word2 = input("Entrez le deuxième mot : ")
    relation_type = input("Entrez le type de relation : ")

    # Rechercher la relation
    relation = find_relation_with_nodes_and_type(data, word1, word2, relation_type)

    if relation:
        print("Relation trouvée :", relation)
    else:
        print("Aucune relation trouvée pour les mots et le type de relation spécifiés.")

if __name__ == "__main__":
    main()# ok


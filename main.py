import json
from collections import deque
# note
    # fonction qui cherche une relation indirecte entre deux mots en profondeur
    # ce ne prend pas les deux sens comme je le fait dans la fonction find_relation_with_nodes_and_type
    # je parcours toutes les relations qui contiennent le noeud1 et pour chaque noeud associer a ce noeud1, je vais regarder si il n as pas la relation directe sinon je descend encore...
    # je neprend pas e ncompte non plus les types de relation dans le parcours en profondeur, je me contente de verifier profondeur par profondeur si il y a une relation directe avec le type de realtion correspondant a celle de base.
        # il  y a peut etre des specififite ou si on est une relation particuliere, meme si  c est pas exactement celle de base, cam arche quand meme...a voir
def find_indirect_relation_bfs(word1_node, word_node_cible, relation_type_info, relations, nodes, list_relations):
    """
    Chercher une relation indirecte entre deux mots en utilisant
    @param word1_node: le noeud du premier mot qui etait le second mot a l etape precedente (pigeon ass gris : existe pas donc on cherche prend une des realtion dont le premier mot est gris...)
    @param word_node_cible: le noeud du mot cible
    @param relation_type_info: le type de relation de base
    @param relations: les relations entre les mots
    @param nodes: les noeuds des mots  
    @return: la relation indirecte entre les deux mots
    """
    #print("word1_node", word1_node, "word2_node", word2_node, "relation_type_info", relation_type_info, "relations", relations)
    for rel in relations:
        if rel["node1"] == word1_node["eid"]:
            # si lien directe trouvé
            if rel["node2"] == word_node_cible["eid"] and rel["type"] == relation_type_info["rtid"]:
                list_relations.append(rel)
            # si pas de lien directe, on cherche une relation indirecte au la profondeur + 1
            # recherche du mot par rapport a l id noeud2
            word2_node_new = next((node for node in nodes if node["eid"] == rel["node2"]), None)
            if word2_node_new:
                # appel recursif pour chercher une ou des relations indirectes
                find_indirect_relation_bfs(word2_node_new, word_node_cible, relation_type_info, relations, nodes, list_relations)

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

    # si pas de relation directe trouvé, on cherche une relation indirecte recursivement pour avoir tous les niveaux de relations
    if not matching_relations:
        # Chercher une relation indirecte
        # parours toues les realtion qui contiennent le mot1
        list_relations = []
        for rel in relations:
            if rel["node1"] == word1_node["eid"]:
                # recherche du mot par rapport a l id noeud2
                word2_node_new = next((node for node in nodes if node["eid"] == rel["node2"]), None)
                if word2_node_new:
                    # appel recursif pour chercher une ou des relations indirectes
                    find_indirect_relation_bfs(word2_node_new, word2_node, relation_type_info, relations, nodes, list_relations)
            # faire pareil de l autre coté...
            # a dvp...

    matching_relations = list_relations
    print("matching_relations", matching_relations)
    # Trier les relations en fonction du rang (si le rang est disponible)
    matching_relations.sort(key=lambda x: x.get('rank', float('inf')))

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
    main()


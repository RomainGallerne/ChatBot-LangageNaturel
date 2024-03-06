import json

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
    matching_relations.sort(key=lambda x: x.get('rank', float('inf')))

    # Renvoyer la relation avec le rang le plus élevé
    return matching_relations[0]

def main():
    # Charger les données JSON depuis un fichier ou une variable
    with open("data/example.json", "r", encoding="utf-8") as file:
        data = file.read()

    # Entrer les mots et le type de relation
    word1 = input("Entrez le premier mot : ")
    word2 = input("Entrez le deuxième mot : ")
    relation_type = input("Entrez le type de relation : ")

    # Rechercher la relation correspondante
    relation = find_relation_with_nodes_and_type(data, word1, word2, relation_type)

    if relation:
        print("Relation trouvée :", relation)
    else:
        print("Aucune relation trouvée pour les mots et le type de relation spécifiés.")

if __name__ == "__main__":
    main()


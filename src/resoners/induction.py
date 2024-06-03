from resoners.deduction import *
from utility.utils import *

#############
# INDUCTION #
#############
def induction(data_1_, data_2_, relation, dataJSON1, dataJSON2):
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
    data_1 = node_name_to_id(data_1_, dataJSON1)
    data_2 = node_name_to_id(data_2_, dataJSON2)
    
    data_1 = int(data_1)
    data_2 = int(data_2)

    relations_inductions = ["r_syn", "r_hypo", "r_has_part", "r_similar", "r_variante", "r_alias", "r_domain_subst"]

    # num relation entrer
    relation_type_id_base = next((cle for cle, valeur in types_relations_2.items() if valeur["trname"] == relation), None)
    
    # type relation r_syn
    relation_type_id = next((rtid for rtid, relation in types_relations_1.items() if relation["trname"] in relations_inductions), None)
    if relation_type_id is None:
        relation_type_id = next((rtid for rtid, relation in types_relations_2.items() if relation["trname"] in relations_inductions), None)

    # chercher relation dans fichier 1
    list_relations_match = [cle for cle, valeur in relations_1.items() if valeur["node1"] == data_1 and valeur["type"] == int(relation_type_id)]

    # trie les relations en fonction du rang (si le rang est disponible)
    list_relations_match.sort(key=lambda x: relations_1[x].get('rank', float('inf')) if relations_1[x].get('rank') is not None else 11.0)

    for relation_key in list_relations_match:
        # si il y a plus de 10 element dans la liste on arrete
        if len(list_valide) > 10:
            break
        # recuperer la relation 1
        relation_1_ok = relations_1[str(relation_key)]

        for cle, valeur in relations_2.items():
            try:
              if valeur["node1"] == relation_1_ok["node2"] and valeur["type"] == int(relation_type_id_base) and valeur["node2"] == data_2:
                  list_valide.append(
                    {
                          "rank_relation": valeur["rank"] if valeur["rank"] is not None else 11.0, 
                          "weight_relation": valeur["w"], 
                          "relation" : relation["trname"],
                          "rank_element_1": (relation_1_ok["rank"] if relation_1_ok["rank"] is not None else 11.0), 
                          "weight_element_1": relation_1_ok["w"],
                          "rank_element_2": None, 
                          "weight_element_2": None, 
                          "element1": str(node_id_to_name(relation_1_ok["node2"], dataJSON1)), 
                          "element2": None,
                      }
                  )
            except TypeError:
              continue

    return list_valide[:8]


###################################################
#                 Induction propre                #
###################################################
  
def get_clean_induction_results(data1, data2, relation, dataJSON1, dataJSON2): 
  inductions = induction(data1, data2, relation, dataJSON1, dataJSON2)
    
  resultat_global = 0
  for ind in inductions:
      resultat_global += ind["weight_relation"]

      #On booste les relations négatives pour ne pas les rater
      if(ind["weight_relation"] < 0.0):
        resultat_global += 5.0 * ind["weight_relation"]
        
      generique_rank = float(ind["rank_element_1"])
      generique_weight = float(ind["weight_element_1"])
      relation_rank = float(ind["rank_relation"])
      relation_weight = float(ind["weight_relation"])

      confiance = abs(
            moyenne_quad([generique_weight,relation_weight]) 
            / 
            moyenne_quad([generique_rank,relation_rank])
          )
      
      ind["confiance"] = (abs(confiance))

  to_remove = []
  for ind1 in inductions:
    for ind2 in inductions:
      if(ind1 != ind2):
        if(ind1["element1"]==ind2["element1"]):
          if(ind1["confiance"]>ind2["confiance"]):
            to_remove.append(ind2)
          else:
            to_remove.append(ind1)

  for elem in to_remove:
    if elem in inductions:
      inductions.remove(elem)

  inductions = sorted(inductions, key=lambda x: x["confiance"], reverse=True)
  return inductions[:10], resultat_global
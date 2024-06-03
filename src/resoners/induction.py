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
    relations_dataJSON1 = dataJSON1["relation"]
    relations_dataJSON2 = dataJSON2["relation"]

    # Trouver les noeuds correspondant aux noms donnés
    data_1 = node_name_to_id(data_1_, dataJSON1)
    data_2 = node_name_to_id(data_2_, dataJSON2)
    # num relation entrer
    relation_id = relation_name_to_id(relation, dataJSON1)

    relations_inductions = [
       5, #r_syn 
       8, #r_hypo
       67, #r_similar 
       71, #r_variante 
       83, #r_alias
    ]
    # chercher relation dans fichier 1
    list_inductions = [cle for cle, valeur in relations_dataJSON1.items() if valeur["node1"] == data_1 and valeur["type"] in relations_inductions and valeur["rank"] is not None]

    # trie les relations en fonction du rang (si le rang est disponible)
    list_inductions.sort(key=lambda x: relations_dataJSON1[x].get('rank', float('inf')) if relations_dataJSON1[x].get('rank') is not None else 11.0)

    for key in list_inductions:
        # si il y a plus de 10 element dans la liste on arrete
        if len(list_valide) > 10:
            break
        # recuperer la relation 1
        relation_1_ok = relations_dataJSON1[str(key)]

        for cle, valeur in relations_dataJSON2.items():
            try:
              if valeur["node1"] == relation_1_ok["node2"]:
                if valeur["type"] == relation_id:
                  if valeur["node2"] == data_2:
                    val_wnormed = valeur["wnormed"]
                    rel1_wnormed = relation_1_ok["wnormed"]  
                    list_valide.append(
                       {
                        "weight_relation": val_wnormed if val_wnormed is not None else 1.0,
                        "relation" : str(relation_id_to_name(relation_1_ok["type"], dataJSON1)),
                        "weight_element_1": rel1_wnormed if rel1_wnormed is not None else 1.0,
                        "element": str(node_id_to_name(relation_1_ok["node2"], dataJSON1)),
                      }
                    )
            except TypeError:
              continue

    return list_valide


###################################################
#                 Induction propre                #
###################################################
  
def get_clean_induction_results(data1, data2, relation, dataJSON1, dataJSON2): 
  inductions = induction(data1, data2, relation, dataJSON1, dataJSON2)
  
  resultat_global = 0
  for ind in inductions:
      relation_weight = float(ind["weight_relation"])
      resultat_global += relation_weight

      #On booste les relations négatives pour ne pas les rater
      if(relation_weight < 0.0):
        resultat_global += 5.0 * relation_weight

      generique_weight = float(ind["weight_element_1"])
      relation_weight = float(relation_weight)

      confiance = moyenne_geo([abs(generique_weight),abs(relation_weight)])
      ind["confiance"] = (confiance)

  inductions = sorted(inductions, key=lambda x: x["confiance"], reverse=True)
  return inductions, resultat_global
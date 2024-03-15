from main import load_data

###################################################
#             Fonctions utilitaires               #
###################################################

def node_id_to_name(id, dataJSON):
  return dataJSON["noeud"][id]["name"]

def node_name_to_id(data, dataJSON):
  noeuds = dataJSON["noeud"]
  for cle, valeur in noeuds.items():
    if (valeur.get("name") == data):
      return int(cle)
    
def relation_id_to_name(id, dataJSON):
  return dataJSON["type_relation"][id]["trname"]

def relation_name_to_id(data, dataJSON):
  relations = dataJSON["type_relation"]
  for cle, valeur in relations.items():
    if (valeur.get("trname") == data):
      return int(cle)
    
###################################################
#        Fonctions d'interrogation simple         #
###################################################

def interrogation_simple(data1, data2, relation, dataJSON):
  relations = dataJSON["relation"]
  for cle, valeur in relations.items() :
    if(int(valeur["type"]) == relation_name_to_id(relation, dataJSON)):
      if (int(valeur["node1"]) == node_name_to_id(data1, dataJSON)):
        if (int(valeur["node2"]) == node_name_to_id(data2, dataJSON)):
          reponse = "["+data1+", "+relation+", "+data2+"]\n"
          return True, reponse
  return False, ""

###################################################
#             Fonctions d'induction               #
###################################################

def interrogation_induction(data1, data2, relation, dataJSON1, dataJSON2, antecedants = "", niveau_induction = 1):
  # On explore jusque 3 de profondeurs
  if(niveau_induction >= 3):
    return False, ""
  
  else:
    relations1 = dataJSON1["relation"]
    liste_element = {}

    for cle, valeur in relations1.items() :
      if(int(valeur["type"]) == 6): # La relation r_isa a pour id 6
        if (int(valeur["node1"]) == int(node_name_to_id(data1, dataJSON1))):
          liste_element[valeur["rank"]] = str(valeur["node2"])

    rang_trie = sorted(liste_element.keys())
    for rang in rang_trie[:3]:
      data_intermediaire = node_id_to_name(liste_element[rang], dataJSON1)
      validite, rep = interrogation_simple(data_intermediaire, data2, relation, dataJSON2)
      if(validite):
        reponse = "["+data1+", r_isa, "+data_intermediaire+"]\n"
        reponse += rep
        return True, reponse
      else :
        validite, rep =  interrogation_induction(data_intermediaire, data2, relation, load_data(data_intermediaire), dataJSON2, antecedants + "["+data1+", r_isa, "+data_intermediaire+"]\n", niveau_induction+1)
        if(validite):
          reponse = "["+data1+", r_isa, "+data_intermediaire+"]\n"
          reponse += rep
          return True, reponse
      
    return False, ""
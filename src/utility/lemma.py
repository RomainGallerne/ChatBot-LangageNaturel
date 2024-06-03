###################################################
#             Fonctions utilitaires               #
###################################################

def node_id_to_name(id, dataJSON):
  return str(dataJSON["noeud"][str(id)]["name"]).split(">")[0]

def node_name_to_id(data, dataJSON):
  noeuds = dataJSON["noeud"]
  for cle, valeur in noeuds.items():
    if (valeur.get("name") == data):
      return int(cle)
    
def relation_id_to_name(id, dataJSON):
  return str(dataJSON["type_relation"][id]["trname"]).split(">")[0]

def relation_name_to_id(data, dataJSON):
  relations = dataJSON["type_relation"]
  for cle, valeur in relations.items():
    if (valeur.get("trname") == data):
      return int(cle)

###################################################
#              Fonction Find_Lemma                #
###################################################

def find_Lemma(data, dataJSON):
  relations = dataJSON["relation"]
  lemmas = []
  data_id = int(node_name_to_id(data, dataJSON))
  valeurs = list(relations.values())
  for valeur in valeurs :
    if(int(valeur["type"])==19): # La relation r_lemma a pour id 19
      if (int(valeur["node1"])==data_id):
        lemmas.append(node_id_to_name(valeur["node2"],dataJSON))
  return lemmas
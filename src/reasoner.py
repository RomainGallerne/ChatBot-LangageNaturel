from main import load_data

###################################################
#             Fonctions utilitaires               #
###################################################

def node_id_to_name(id, dataJSON):
  return str(dataJSON["noeud"][str(id)]["name"])

def node_name_to_id(data, dataJSON):
  noeuds = dataJSON["noeud"]
  for cle, valeur in noeuds.items():
    if (valeur.get("name") == data):
      return int(cle)
    
def relation_id_to_name(id, dataJSON):
  return str(dataJSON["type_relation"][id]["trname"])

def relation_name_to_id(data, dataJSON):
  relations = dataJSON["type_relation"]
  for cle, valeur in relations.items():
    if (valeur.get("trname") == data):
      return int(cle)
    
###################################################
#        Fonctions d'interrogation simple         #
###################################################

def relation_existe(data1, data2, relation, dataJSON):
  relations = dataJSON["relation"]
  for cle, valeur in relations.items() :
    if(int(valeur["type"]) == relation_name_to_id(relation, dataJSON)):
      if (int(valeur["node1"]) == node_name_to_id(data1, dataJSON)):
        if (int(valeur["node2"]) == node_name_to_id(data2, dataJSON)):
          if (int(valeur["node2"]) == node_name_to_id(data2, dataJSON)):
            if (int(valeur["w"]) > 0.0):
              return "vrai"
            else :
              return "faux"
  return "nsp"

###################################################
#             Fonctions d'induction               #
###################################################

def recherche_generique(data, dataJSON):
  relations = dataJSON["relation"]
  generiques = []
  for cle, valeur in relations.items() :
    if (int(valeur["node1"]) == int(node_name_to_id(data, dataJSON))) and (int(valeur["type"]) == 6): # La relation r_isa a pour id 6
      generiques.append(valeur["node2"])
      if(len(generiques) >= 10):
        break
  return generiques


def deduction(data1, data2, relation, dataJSON1, dataJSON2):
  relations1 = dataJSON1["relation"]
  deductions = []
  data1_id = int(node_name_to_id(data1,dataJSON1))
  data2_id = int(node_name_to_id(data2,dataJSON2))
  relation_id = int(node_name_to_id(relation, dataJSON1))

  generiques_data1 = recherche_generique(data1,dataJSON1)

  for generique in generiques_data1 :
    dataJSON_G = load_data(str(node_id_to_name(generique, dataJSON1)))
    relationsG = dataJSON_G["relation"]
    for cle, valeur in relationsG.items() :
      if(int(valeur["type"]) == relation_id):
        if (int(valeur["node1"]) == generique):
          if (int(valeur["node2"]) == data2_id):
            deductions.append([valeur["rank"],valeur["w"],str(node_id_to_name(generique, dataJSON_G))])

  generiques_data2 = recherche_generique(data2,dataJSON2)

  for generique in generiques_data2 :
    dataJSON_G = load_data(str(node_id_to_name(generique, dataJSON2)))
    relationsG = dataJSON_G["relation"]
    for cle, valeur in relationsG.items() :
      if(int(valeur["type"]) == relation_id):
        if (int(valeur["node2"]) == generique):
          if (int(valeur["node1"]) == data1_id):
            deductions.append([valeur["rank"],valeur["w"],str(node_id_to_name(generique, dataJSON_G))])

  for generique1 in generiques_data1 :
    dataJSON_G1 = load_data(str(node_id_to_name(generique1, dataJSON1)))
    relations_G1 = dataJSON_G1["relation"]
    for cle, valeur in relations_G1.items() :
        if(int(valeur["type"]) == relation_id):
          if (int(valeur["node1"]) == generique1):
            for generique2 in generiques_data2 :
              if (int(valeur["node2"]) == generique2):
                deductions.append([valeur["rank"],valeur["w"],str(node_id_to_name(generique1, dataJSON_G1)),str(node_id_to_name(generique2, dataJSON_G1))])

  return deductions
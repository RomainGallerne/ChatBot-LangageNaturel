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
#            Fonctions de déduction               #
###################################################

def recherche_typique(data, dataJSON):
  relations = dataJSON["relation"]
  data_id = int(node_name_to_id(data, dataJSON))
  typiques = []
  for cle, valeur in relations.items() :
    if (int(valeur["node1"])==data_id) and (int(valeur["type"])==13 and int(valeur["rank"])<=10): # La relation r_agent a pour id 13
      typiques.append([valeur["rank"] or 50.0,valeur["node2"]])
  return [typique[1] for typique in typiques]


def recherche_generique(data, dataJSON):
  relations = dataJSON["relation"]
  generiques = []
  for cle, valeur in relations.items() :
    if (int(valeur["node1"])==int(node_name_to_id(data, dataJSON)) and int(valeur["type"])==6 and int(valeur["rank"])<=10): # La relation r_isa a pour id 6
      generiques.append([valeur["rank"],valeur["node2"]])
  return generiques


def deduction(data1, data2, relation, dataJSON1, dataJSON2):
  relations1 = dataJSON1["relation"]
  relations2 = dataJSON2["relation"]

  deductions = []
  data1_id = node_name_to_id(data1,dataJSON1)
  data2_id = node_name_to_id(data2,dataJSON2)
  relation_id = relation_name_to_id(relation, dataJSON1)

  generiques_data1 = recherche_generique(data1,dataJSON1)
  typiques = recherche_typique(data2,dataJSON2)


  for generique in generiques_data1 :
    #dataJSON_G = load_data(str(node_id_to_name(generique[1], dataJSON1)))
    #relationsG = dataJSON_G["relation"]
    for cle, valeur in relations1.items() :
      if(valeur["type"] == relation_id):
        #print(valeur["node1"])
        if (valeur["node1"] == generique[1] and (valeur["node1"] in typiques)):
          if (valeur["node2"] == data2_id):
            deductions.append([valeur["rank"],generique[0],None,valeur["w"],str(node_id_to_name(generique[1], dataJSON1)),None])

  generiques_data2 = recherche_generique(data2,dataJSON2)

  for generique in generiques_data2 :
    #dataJSON_G = load_data(str(node_id_to_name(generique[1], dataJSON2)))
    #relationsG = dataJSON_G["relation"]
    for cle, valeur in relations2.items() :
      if(valeur["type"] == relation_id):
        if (valeur["node2"] == generique[1]):
          if (valeur["node1"] == data1_id):
            deductions.append([valeur["rank"], None, generique[0],valeur["w"], None, str(node_id_to_name(generique[1], dataJSON2))])

  for generique1 in generiques_data1 :
    #dataJSON_G1 = load_data(str(node_id_to_name(generique1[1], dataJSON1)))
    #relations_G1 = dataJSON_G1["relation"]
    for cle, valeur in relations1.items() :
        if(valeur["type"] == relation_id):
           if (valeur["node1"] == generique[1] and (valeur["node1"] in typiques)):
             for generique2 in generiques_data2 :
                if (valeur["node2"] == generique2[1]):
                  deductions.append([valeur1["rank"],generique1[0],generique2[0],valeur1["w"],str(node_id_to_name(generique1[1], dataJSON1)),str(node_id_to_name(generique2[1], dataJSON2))])

  return deductions
from utils import *

###################################################
#           Recherche d'éléments typiques         #
###################################################

def recherche_typique(data, dataJSON):
  relations = dataJSON["relation"]
  data_id = int(node_name_to_id(data, dataJSON))
  typiques = []
  for cle, valeur in relations.items() :
    if (int(valeur["node1"])==data_id) and (int(valeur["type"])==13 and int(valeur["rank"])<=10): # La relation r_agent a pour id 13
      typiques.append([valeur["rank"] or 11.0,valeur["node2"]])
  return [typique[1] for typique in typiques]

###################################################
#         Recherche d'éléments génériques         #
###################################################

def recherche_generique(data, dataJSON):
  relations = dataJSON["relation"]
  generiques = []
  data_id = int(node_name_to_id(data, dataJSON))
  valeurs = list(relations.values())
  for valeur in valeurs :
    if (int(valeur["node1"])==data_id):
      #print("oui 1")
      if(int(valeur["type"])==6): # La relation r_isa a pour id 6
        #print("oui 2")
        if(int(valeur["rank"] or 11)<=10):
          #print("oui 3")
          generiques.append([valeur["rank"],valeur["w"],valeur["node2"]])
  val = 0
  try:
    # On cherche 8 génériques
    while(len(generiques)<8 and val<len(relations)):
      if(int(valeurs[val]["node1"])==data_id):
        if(int(valeurs[val]["type"])==6): # La relation r_isa a pour id 6
          generiques.append([valeurs[val]["rank"] or 11.0,valeurs[val]["w"],valeurs[val]["node2"]])
      val += 1
  except IndexError:
    None
  return generiques

def recherche_generique_spe(data, dataJSON, filtre):
  relations = dataJSON["relation"]
  generiques = []
  data_id = int(node_name_to_id(data, dataJSON))
  valeurs = list(relations.values())
  for valeur in valeurs :
    if (int(valeur["node1"]) in filtre):
      if(int(valeur["node1"])==data_id):
        if(int(valeur["type"])==6): # La relation r_isa a pour id 6
          if(int(valeur["rank"])<=10):
            generiques.append([valeur["rank"],valeur["w"],valeur["node2"]])
  val = 0
  try:
    while(len(generiques)<10 and val<len(relations)):
      if (int(valeurs[val]["node1"]) in filtre):
        if(int(valeurs[val]["node1"])==data_id):
          if(int(valeurs[val]["type"])==6): # La relation r_isa a pour id 6
            generiques.append([valeurs[val]["rank"] or 11.0,valeurs[val]["w"],valeurs[val]["node2"]])
      val += 1
  except IndexError:
    None
  return generiques

###################################################
#            Fonctions de déduction               #
###################################################

def deduction(data1, data2, relation, dataJSON1, dataJSON2):
  #Elements utilitaires
  relations_dataJSON1 = dataJSON1["relation"]
  relations_dataJSON2 = dataJSON2["relation"]
  deductions = []
  data1_id = node_name_to_id(data1,dataJSON1)
  data2_id = node_name_to_id(data2,dataJSON2)
  relation_id = relation_name_to_id(relation, dataJSON1)

  #Recherche des élements typiques de la donnée data2 (qui peut faire data2 ?)
  typiques = recherche_typique(data2,dataJSON2)

  if(len(typiques) == 0):
    #Si l'élément a des typiques, on ne s'intéresse qu'à eux
    elements1 = recherche_generique(data1,dataJSON1)
  else :
    #Sinon on prend tous les génériques
    elements1 = recherche_generique_spe(data1,dataJSON1,typiques)
  elements2 = recherche_generique(data2,dataJSON2)

  #On recherche les relations dans lesqueles data 1 est un X, et X est en relation avec data 2
  for element in elements1 :
    for cle, valeur in relations_dataJSON2.items() :
      if(int(valeur["type"]) == int(relation_id)):
        if (int(valeur["node1"]) == int(element[2])):
          if (int(valeur["node2"]) == int(data2_id)):
            deductions.append(
              {
                "rank_relation": (valeur["rank"] or 11.0), 
                "weight_relation": valeur["w"], 
                "rank_element_1": (element[0] or 11.0), 
                "weight_element_1": element[1],
                "rank_element_2": None, 
                "weight_element_2": None, 
                "element1": str(node_id_to_name(element[2], dataJSON1)), 
                "element2": None
              }
            )

  #On recherche les relations dans lesqueles data 2 est un Y, et data1 est en relation avec Y
  for element in elements2 :
    for cle, valeur in relations_dataJSON1.items() :
      if(int(valeur["type"]) == int(relation_id)):
        if (int(valeur["node2"]) == int(element[2])):
          if (int(valeur["node1"]) == int(data1_id)):
            deductions.append(
              {
                "rank_relation": (valeur["rank"] or 11.0), 
                "weight_relation": valeur["w"], 
                "rank_element_1": None, 
                "weight_element_1": None,
                "rank_element_2": (element[0] or 11.0), 
                "weight_element_2": element[1], 
                "element1": None, 
                "element2": str(node_id_to_name(element[2], dataJSON2))
              }
            )

  #On recherche les relations dans lesqueles data 1 est un X, et data2 est un Y, et X est en relation avec Y
  for element1 in elements1 :
    dataJSON_element = load_data(node_id_to_name(element1[2],dataJSON1)) #Il nous faut ici récupérer les données obligatoirement
    relations_dataJSON_element = dataJSON_element["relation"]

    for cle, valeur in relations_dataJSON_element.items() :
        if(int(valeur["type"]) == int(relation_id)):
           if (int(valeur["node1"]) == int(element1[2])):
             for element2 in elements2 :
                if (int(valeur["node2"]) == int(element2[2])):
                  deductions.append(
                    {
                      "rank_relation": (valeur["rank"] or 11.0), 
                      "weight_relation": valeur["w"], 
                      "rank_element_1": (element1[0] or 11.0), 
                      "weight_element_1": element1[1],
                      "rank_element_2": (element2[0] or 11.0), 
                      "weight_element_2": element2[1], 
                      "element1": str(node_id_to_name(element1[2], dataJSON1)), 
                      "element2": str(node_id_to_name(element2[2], dataJSON2))
                    }
                  )

  return deductions

###################################################
#          Fonctions de déduction Propre          #
###################################################

def get_clean_deduction_results(data1, data2, relation, dataJSON1, dataJSON2): 
  deductions = deduction(data1, data2, relation, dataJSON1, dataJSON2)
    
  resultat_global = 0
  for ded in deductions:
      resultat_global += ded["weight_relation"]

      #On booste les relations négatives pour ne pas les rater
      if(ded["weight_relation"] < 0.0):
        resultat_global += 5.0 * ded["weight_relation"]

      #On a un générique pour chaque terme
      if(ded["element1"] != None and ded["element2"] != None):
        generique_rank = float(ded["rank_element_1"]) + float(ded["rank_element_2"])
        generique_weight = float(ded["weight_element_1"]) + float(ded["weight_element_2"])
        relation_rank = float(ded["rank_relation"])
        relation_weight = float(ded["weight_relation"])
        confiance = ((generique_weight + relation_weight) / (generique_rank + relation_rank)) / 3.0

      #On a un générique pour le 1er terme
      elif(ded["element1"] != None):
        generique_rank = float(ded["rank_element_1"])
        generique_weight = float(ded["weight_element_1"])
        relation_rank = float(ded["rank_relation"])
        relation_weight = float(ded["weight_relation"])
        confiance = ((generique_weight + relation_weight) / (generique_rank + relation_rank)) * 5.0

      #On a un générique pour le 2nd terme
      elif(ded["element2"] != None):
        generique_rank = float(ded["rank_element_2"])
        generique_weight = float(ded["weight_element_2"])
        relation_rank = float(ded["rank_relation"])
        relation_weight = float(ded["weight_relation"])
        confiance = ((generique_weight + relation_weight) / (generique_rank + relation_rank)) / 3.0
      

      ded["confiance"] = (abs(confiance))

  to_remove = []
  for ded1 in deductions:
    for ded2 in deductions:
      if(ded1 != ded2):
        if(ded1["element1"]==ded2["element1"] and ded1["element2"]==ded2["element2"]):
          if(ded1["confiance"]>ded2["confiance"]):
            to_remove.append(ded2)
          else:
            to_remove.append(ded1)

  for elem in to_remove:
    if elem in deductions:
      deductions.remove(elem)

  deductions = sorted(deductions, key=lambda x: x["confiance"], reverse=True)
  return deductions[:10], resultat_global
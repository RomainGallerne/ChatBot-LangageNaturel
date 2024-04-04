import json
import os
from data_collector.dataProcessing import *
from reasoner import *

###################################################
#    Chargement des données et dl si nécessaire   #
###################################################

def load_data(data : str):
    splited_data = data.split(">")
    clean_data = splited_data[0]
    processData(clean_data)
    # Charger les données JSON depuis un fichier ou une variable
    with open("data/"+clean_data+".json", "r", encoding="utf-8") as file:
        dataJSON = json.load(file)
    return dataJSON

###################################################
#   Traitement du tuple JSON en langage naturel   #
###################################################

def JSON_to_nat(jsonFile : list, jsonLine : list):
    data_dict = json.loads(jsonFile)
    nodes = data_dict["noeud"]
    type_relations = data_dict["type_relation"]

    type, eid1, eid2 = jsonLine["type"], jsonLine["node1"], jsonLine["node2"]
    word1 = next((node for node in nodes if node["eid"] == eid1), None)
    word2 = next((node for node in nodes if node["eid"] == eid2), None)
    relation = next((type_relation for type_relation in type_relations if type_relation["rtid"] == type), None)

    return word1["name"], relation["trname"], word2["name"]

###################################################
#            Fonction de nettoyage               #
###################################################
def clear_console():
    # Efface la console en imprimant 100 retours à la ligne
    os.system('cls' if os.name == 'nt' else 'clear')  # Pour Windows et Unix/Linux

###################################################
#             Fonction d'Affichage                #
###################################################

def affichage(arguments_global, resultat_global, data1, data2, relation):
    if(resultat_global >= 5.0):
        print("Cette propriété est VRAIE :")
    elif(resultat_global <= -5.0):
        print("Cette propriété est FAUSSE :")
    else:
        print("Cette propriété est INDETERMINE :")

    rang, rang_affiche = 0, 0
    while(rang < 5):
        try:
            if(arguments_global[rang][3] > 0.0 and resultat_global >= 5.0): 
                verite = "oui"
            elif(arguments_global[rang][3] < 0.0 and resultat_global <= -5.0): 
                verite  ="non"
            elif(resultat_global >= -5.0 and resultat_global <= 5.0):
                if(arguments_global[rang][3] > 0.0): verite = "oui"
                else: verite = "non"
            else:
                rang += 1 
                continue
        except IndexError:
            break

        if(arguments_global[rang][1] != None and arguments_global[rang][2] != None):
            chaine = str(rang_affiche) + " | " + verite + " | [" + data1 + " r_isa " + str(arguments_global[rang][4]) + "] & ["
            chaine += data2 + " r_isa " + str(arguments_global[rang][5]) + "] & ["
            chaine += str(arguments_global[rang][4]) + " " + relation + " " + str(arguments_global[rang][5]) + "]"
            confiance = arguments_global[rang][6]

        elif(arguments_global[rang][2] == None):
            chaine = str(rang_affiche) + " | " + verite + " | [" + data1 + " r_isa " + str(arguments_global[rang][4]) + "] & ["
            chaine += str(arguments_global[rang][4]) + " " + relation + " " + data2 + "]"
            confiance = arguments_global[rang][6]

        elif(arguments_global[rang][1] == None):
            chaine = str(rang_affiche) + " | " + verite + " | [" +data2 + " r_isa "+str(arguments_global[rang][5])+"] & ["
            chaine += data1 + " " + relation + " " + str(arguments_global[rang][5]) + "]"
            confiance = arguments_global[rang][6]
        
        chaine += " | "
        chaine += str(confiance)
        print(chaine)
        rang_affiche += 1
        rang += 1

###################################################
#              Fonction Principal                 #
###################################################

def main():
    clear_console()
    print("---------------------\nEntrez la requête au format :\n 'pigeon r_agent-1 voler'\n---------------------\n")
    prompt = input()

    try :
        data1, relation, data2 = prompt.split(" ")
    except ValueError as ve :
        print("Saisi incorrect")
        return -1

    try:
        dataJSON1 = load_data(data1)
        dataJSON2 = load_data(data2)
    except AttributeError as ae :
        print("Saisi incorrect")
        return -1

    print("\n---------------------\n")
    resultats_deductions = 0
    resultats_induction = 0
    resultats_transitivite = 0

    deductions, resultats_deductions = get_clean_deduction_results(data1, data2, relation, dataJSON1, dataJSON2)
    inductions, resultats_inductions = [],0
    transitivite, resultats_transitivite = [],0

    resultat_global = resultats_deductions + resultats_induction + resultats_transitivite
    arguments_global = deductions + inductions + transitivite

    affichage(arguments_global, resultat_global, data1, data2, relation)

if __name__ == "__main__":
    main()
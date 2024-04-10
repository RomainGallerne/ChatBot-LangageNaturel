import json
import os
from data_collector.dataProcessing import *
from deduction import get_clean_deduction_results
from induction import get_clean_induction_results
from lemma import find_Lemma

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

def affichage(deductions, inductions, transitivite, resultat_global, data1, data2, relation):

    print("Score global de la propriété : ",resultat_global,"\n")

    if(resultat_global > 2.0):
        print("Cette propriété est VRAIE :")
    elif(resultat_global < -2.0):
        print("Cette propriété est FAUSSE :")
    else:
        print("Cette propriété est INDETERMINE :")

    #inférences
    #[relation_rank, relation_weight, element1_generique_w, rank_1, element2_generique_w, rank_2, element1_generique, element2_generique]
    
    arguments_global = deductions + inductions + transitivite
    arguments_global = sorted(arguments_global, key=lambda x: x[8], reverse=True)

    rang, rang_affiche = 0, 0
    while(rang < 5):
        try:
            if(arguments_global[rang][1] > 0.0 and resultat_global > 2.0): 
                verite = "oui"
            elif(arguments_global[rang][1] < 0.0 and resultat_global < -2.0): 
                verite  ="non"
            elif(resultat_global >= -2.0 and resultat_global <= 2.0):
                if(arguments_global[rang][1] > 0.0): verite = "oui"
                else: verite = "non"
            else:
                rang += 1 
                continue
        except IndexError:
            break

        chaine = str(rang_affiche) + " | " + verite + " | "
        if(arguments_global[rang] in deductions):
            if(arguments_global[rang][6] != None and arguments_global[rang][7] != None):
                chaine += "Déduction | [" + data1 + " r_isa " + str(arguments_global[rang][6]) + "] & ["
                chaine += data2 + " r_isa " + str(arguments_global[rang][7]) + "] & ["
                chaine += str(arguments_global[rang][6]) + " "
                if(verite == "non"): chaine += "¬"+relation
                else: chaine += relation
                chaine += " " + str(arguments_global[rang][7]) + "]"

            elif(arguments_global[rang][6] != None):
                chaine += "Déduction | [" + data1 + " r_isa " + str(arguments_global[rang][6]) + "] & ["
                chaine += str(arguments_global[rang][6]) + " "
                if(verite == "non"): chaine += "¬"+relation
                else: chaine += relation
                chaine += " " + data2 + "]"

            elif(arguments_global[rang][7] != None):
                chaine += "Déduction | [" + data2 + " r_isa "+str(arguments_global[rang][7])+"] & ["
                chaine += data1 + " "
                if(verite == "non"): chaine += "¬"+relation
                else: chaine += relation
                chaine += " " + str(arguments_global[rang][7]) + "]"

        elif(arguments_global[rang] in inductions):
            chaine += "Induction | [" + data1 + " r_syn " + str(arguments_global[rang][6]) + "] & ["
            chaine += str(arguments_global[rang][6]) + " "
            if(verite == "non"): chaine += "¬"+relation
            else: chaine += relation
            chaine += " " + data2 + "]"
        
        chaine += " | "
        chaine += str(arguments_global[rang][8])
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
    resultat_deductions = 0
    resultat_induction = 0
    resultat_transitivite = 0
    data1_LEMMAS = find_Lemma(data1,dataJSON1)
    data2_LEMMAS = find_Lemma(data2,dataJSON2)

    deductions, resultat_deductions = get_clean_deduction_results(data1, data2, relation, dataJSON1, dataJSON2)
    inductions, resultat_inductions = get_clean_induction_results(data1, data2, relation, dataJSON1, dataJSON2)
    transitivite, resultat_transitivite = [],0

    resultat_global = resultat_deductions + resultat_induction + resultat_transitivite

    """print(data1_LEMMAS)
    print(data2_LEMMAS)

    for data1_LEMMA in data1_LEMMAS:
        for data2_LEMMA in data2_LEMMAS:

            deductions_LEMMA1, resultat_deductions_LEMMA1 = get_clean_deduction_results(data1_LEMMA, data2, relation, dataJSON1, dataJSON2)
            inductions_LEMMA1, resultat_inductions_LEMMA1 = get_clean_induction_results(data1_LEMMA, data2, relation, dataJSON1, dataJSON2)
            transitivite_LEMMA1, resultat_transitivite_LEMMA1 = [],0

            deductions_LEMMA2, resultat_deductions_LEMMA2 = get_clean_deduction_results(data1, data2_LEMMA, relation, dataJSON1, dataJSON2)
            inductions_LEMMA2, resultat_inductions_LEMMA2 = get_clean_induction_results(data1, data2_LEMMA, relation, dataJSON1, dataJSON2)
            transitivite_LEMMA2, resultat_transitivite_LEMMA2 = [],0

            deductions_LEMAM12, resultat_deductions_LEMMA12 = get_clean_deduction_results(data1_LEMMA, data2_LEMMA, relation, dataJSON1, dataJSON2)
            inductions_LEMMA12, resultat_inductions_LEMMA12 = get_clean_induction_results(data1_LEMMA, data2_LEMMA, relation, dataJSON1, dataJSON2)
            transitivite_LEMMA12, resultat_transitivite_LEMMA12 = [],0

            resultat_global += resultat_deductions_LEMMA1 + resultat_inductions_LEMMA1 + resultat_transitivite_LEMMA1
            resultat_global += resultat_deductions_LEMMA2 + resultat_inductions_LEMMA2 + resultat_transitivite_LEMMA2
            resultat_global += resultat_deductions_LEMMA12 + resultat_inductions_LEMMA12 + resultat_transitivite_LEMMA12
    """
    #print("Résultat Deductions : ",resultat_deductions)
    #print("Résultat Inductions : ",resultat_induction)
    #print("Résultat Transitivite : ",resultat_transitivite)

    #print("Deductions : \n",deductions)
    #print("Inductions : \n",inductions)
    #print("Transitivite : \n",transitivite)

    #arguments_global
    #[relation_rank, relation_weight, element1_generique_w, rank_1, element2_generique_w, rank_2, element1_generique, element2_generique]

    affichage(deductions, inductions, transitivite, resultat_global, data1, data2, relation)

if __name__ == "__main__":
    main()
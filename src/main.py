import json
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
#              Fonction Principal                 #
###################################################

def main():
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
    val_relation = None

    validite1 = relation_existe(data1, data2, relation, dataJSON1)
    validite2 = relation_existe(data1, data2, relation, dataJSON2)

    deductions = deduction(data1, data2, relation, dataJSON1, dataJSON2)
    deductions = sorted(deductions, key=lambda x: x[0])

    if(validite1=="vrai" or validite2=="vrai"):
        #La relation est donc VRAIE
        print("Cette propriété est VRAIE :")
        val_relation = True
    elif(validite1=="faux" or validite2=="faux"):
        #La relation est donc FAUSSE
        print("Cette propriété est FAUSSE :")
        val_relation = False
    else :
        #La relation est de type INCONNUE
        print("Cette propriété est INDETERMINEE :")
        None

    rang = 0
    while(rang <= 10):
        if(deductions[rang][1] >= 0.0): verite = "oui"
        else: verite  ="non"
        chaine = rang+"|"+verite+"|"+deductions[rang][2]+"|"
        if(len(deductions[rang] > 3)):
            chaine += " & "
            chaine += deductions[rang][3]
        chaine += "|"
        chaine += str(float(deductions[rang][1]) / float(deductions[rang][0]))
        print(chaine)
        rang += 1

if __name__ == "__main__":
    main()
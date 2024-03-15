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
    data1 = input("data 1 : ")
    data2 = input("data 2 : ")
    relation = input("relation : ")

    try:
        dataJSON1 = load_data(data1)
        dataJSON2 = load_data(data2)
    except AttributeError as ae :
        print("Saisi incorrect")

    validite1, reponse1 = interrogation_simple(data1, data2, relation, dataJSON1)
    validite2, reponse2 = interrogation_simple(data1, data2, relation, dataJSON2)
    if(validite1):
        print(reponse1)
    elif(validite2):
        print("Cette propriété est VRAI.")
        print("Elle est obtenue de la manière suivante : ")
        print(reponse2)
    else :
        validite, reponse = interrogation_induction(data1, data2, relation, dataJSON1, dataJSON2)
        if(validite):
            print("Cette propriété est VRAI.")
            print("Elle est obtenue de la manière suivante : ")
            print(reponse)

        else :
            print("Cette propriété est FAUSSE.\n Rien ne permet de l'affirmer.")

if __name__ == "__main__":
    main()
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

    #validite1 = relation_existe(data1, data2, relation, dataJSON1)
    #validite2 = relation_existe(data1, data2, relation, dataJSON2)

    deductions = deduction(data1, data2, relation, dataJSON1, dataJSON2)
    #print(deductions)

    resultat_global = 0

    for ded in deductions:
        resultat_global += ded[3]
        if(ded[1] != None and ded[2] != None):
            confiance = 3.0*float(ded[3]) / (float(ded[0])+float(ded[1])/1.5+float(ded[2])/1.5)
        elif(ded[1] != None):
            confiance = 3.0*float(ded[3]) / (float(ded[0])+float(ded[1]))
        elif(ded[2] != None):
            confiance = 3.0*float(ded[3]) / (float(ded[0])+float(ded[2]))
        ded.append(abs(confiance))


    deductions = sorted(deductions, key=lambda x: x[6], reverse=True)
    #print(deductions)

    if(resultat_global >= 5.0):
        print("Cette propriété est VRAIE :")
    elif(resultat_global <= -5.0):
        print("Cette propriété est FAUSSE :")
    else:
        print("Cette propriété est INDETERMINE :")

    rang, rang_affiche = 0, 0
    while(rang < 5):
        try:
            if(deductions[rang][3] > 0.0 and resultat_global >= 5.0): 
                verite = "oui"
            elif(deductions[rang][3] < 0.0 and resultat_global <= -5.0): 
                verite  ="non"
            elif(resultat_global >= -5.0 and resultat_global <= 5.0):
                if(deductions[rang][3] > 0.0): verite = "oui"
                else: verite = "non"
            else:
                rang += 1 
                continue
        except IndexError:
            break

        if(deductions[rang][1] != None and deductions[rang][2] != None):
            chaine = str(rang_affiche)+"|"+verite+"|"+data1+" r_isa "+str(deductions[rang][4])+" & "
            chaine += data2+" r_isa "+str(nouvelles_deductions[rang][5])+"&"
            chaine += str(nouvelles_deductions[rang][4])+" "+relation+" "+str(deductions[rang][5])
            confiance = nouvelles_deductions[rang][6]

        elif(deductions[rang][2] == None):
            chaine = str(rang_affiche)+"|"+verite+"|"+data1+" r_isa "+str(deductions[rang][4])+" & "
            chaine += str(deductions[rang][4])+" "+relation+" "+data2
            confiance = deductions[rang][6]

        elif(deductions[rang][1] == None):
            chaine = str(rang_affiche)+"|"+verite+"|"+data2+" r_isa "+str(deductions[rang][5])+" & "
            chaine += data1+" "+relation+" "+str(deductions[rang][5])
            confiance = deductions[rang][6]
        
        chaine += "|"
        chaine += str(confiance)
        print(chaine)
        rang_affiche += 1
        rang += 1

if __name__ == "__main__":
    main()
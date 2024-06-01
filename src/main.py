from reasoner import *
from induction import *
from utils import *

###################################################
#             Fonction d'Affichage                #
###################################################

def affichage(deductions, inductions, transitivites, resultat_global, data1, data2, relation):
    clear_console()

    print(resultat_global)

    rang, rang_affiche = 0, 0

    print("---------------------\nEntrez la requête au format :\n 'pigeon/r_agent-1/voler'\n---------------------\n")
    print(data1+"/"+relation+"/"+data2)
    print("\n---------------------\n")

    if(resultat_global >= 5.0):
        print("Cette propriété est VRAIE :")
    elif(resultat_global <= -5.0):
        print("Cette propriété est FAUSSE :")
    else:
        print("Cette propriété est INDETERMINE :")

    arguments_global = deductions + inductions + transitivites
    arguments_global = sorted(arguments_global, key=lambda x: x["confiance"], reverse=True)

    while(rang < 5):
        try:
            if(arguments_global[rang]["weight_relation"] > 0.0 and resultat_global >= 5.0): 
                verite = "oui"
            elif(arguments_global[rang]["weight_relation"] < 0.0 and resultat_global <= -5.0): 
                verite  ="non"
            elif(resultat_global >= -5.0 and resultat_global <= 5.0):
                if(arguments_global[rang]["weight_relation"] > 0.0): verite = "oui"
                else: verite = "non"
            else:
                rang += 1 
                continue
        except IndexError:
            break

        confiance = arguments_global[rang]["confiance"]
        chaine = str(rang_affiche) + " | " + verite + " | "

        if(arguments_global[rang] in deductions):
            chaine += "(deduction) | "

            if(arguments_global[rang]["element1"] != None and arguments_global[rang]["element2"] != None):
                chaine += "[" + data1 + " r_isa " + str(arguments_global[rang]["element1"]) + "] & ["
                chaine += data2 + " r_isa " + str(arguments_global[rang]["element2"]) + "] & "
                if(verite == "non"):
                    chaine += "¬" 
                chaine += "["+str(arguments_global[rang]["element1"]) + " " + relation + " " + str(arguments_global[rang]["element2"]) + "]"

            elif(arguments_global[rang]["element1"] != None):
                chaine += "[" + data1 + " r_isa " + str(arguments_global[rang]["element1"]) + "] & "
                if(verite == "non"):
                    chaine += "¬" 
                chaine += "[" + str(arguments_global[rang]["element1"]) + " " + relation + " " + data2 + "]"

            elif(arguments_global[rang]["element2"] != None):
                chaine += "[" + data2 + " r_isa "+str(arguments_global[rang]["element2"])+"] & "
                if(verite == "non"):
                    chaine += "¬" 
                chaine += "[" + data1 + " " + relation + " " + str(arguments_global[rang]["element2"]) + "]"

        elif(arguments_global[rang] in inductions):
            chaine += "(induction) | "

            chaine += "[" + data1 + " r_syn " + str(arguments_global[rang]["element1"]) + "] & "
            if(verite == "non"):
                    chaine += "¬" 
            chaine += "[" + str(arguments_global[rang]["element1"]) + " " + relation + " " + data2 + "]"

        chaine +=  " | "
        chaine += str(confiance)
        print(chaine)
        rang_affiche += 1
        rang += 1

###################################################
#              Fonction Principal                 #
###################################################

def main():
    clear_console()
    print("---------------------\nEntrez la requête au format :\n 'pigeon/r_agent-1/voler'\n---------------------\n")
    prompt = input()
    print("\n---------------------\n")

    try :
        data1, relation, data2 = prompt.split("/")
    except ValueError as ve :
        print("Saisi incorrect")
        return -1

    try:
        dataJSON1 = load_data(data1)
        dataJSON2 = load_data(data2)
    except AttributeError as ae :
        print("Saisi incorrect")
        return -1

    print("\n")
    resultats_deductions = 0
    resultats_induction = 0
    resultats_transitivite = 0

    deductions, resultats_deductions = get_clean_deduction_results(data1, data2, relation, dataJSON1, dataJSON2)
    inductions, resultats_inductions = get_clean_induction_results(data1, data2, relation, dataJSON1, dataJSON2)
    transitivite, resultats_transitivites = [],0

    resultat_global = resultats_deductions + resultats_inductions + resultats_transitivites

    affichage(deductions, inductions, transitivite, resultat_global, data1, data2, relation)

if __name__ == "__main__":
    main()
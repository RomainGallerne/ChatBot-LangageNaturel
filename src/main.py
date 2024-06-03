import time
from resoners.deduction import *
from resoners.induction import *
from resoners.transitivite import *
from utility.utils import *

###################################################
#             Fonction d'Affichage                #
###################################################

def affichage(deductions, inductions, transitivites, resultat_global, data1, data2, relation, dataJSON1, dataJSON2):
    """
    Affiche les résultats des déductions, inductions et transitivités pour une relation entre deux entités.

    Args:
    - deductions (list): Liste des déductions trouvées pour la relation.
    - inductions (list): Liste des inductions trouvées pour la relation.
    - transitivites (list): Liste des transitivités trouvées pour la relation.
    - resultat_global (float): Résultat global de la relation.
    - data1 (str): Première entité de la relation.
    - data2 (str): Deuxième entité de la relation.
    - relation (str): Type de relation entre les deux entités.

    Returns:
    - None

    Cette fonction affiche les résultats des déductions, inductions et transitivités pour une relation donnée
    entre deux entités. Les résultats sont affichés dans la console avec les détails suivants :
    - L'entrée utilisateur au format "entité1/relation/entité2".
    - La vérité de la relation (VRAIE, FAUSSE ou INDETERMINE) basée sur le résultat global.
    - Les 6 arguments les plus pertinents avec leur type (déduction ou induction), les entités impliquées,
      la vérité de la relation (oui ou non) et la confiance associée.
    """
    clear_console()
    print("---------------------\nEntrez la requête au format :\n 'pigeon/r_agent-1/voler'\n---------------------\n")
    print(f"{data1}/{relation}/{data2}\n")

    if resultat_global > 0.0:
        print("Cette propriété est VRAIE (" + str(resultat_global) + ")")
    elif resultat_global < -0.0:
        print("Cette propriété est FAUSSE (" + str(resultat_global) + ")")
    else:
        print("Cette propriété est PROBABLEMENT FAUSSE (" + str(resultat_global) + ")\nRien ne permet de l'inférer de façon probante.\n")

    arguments_global = deductions + inductions + transitivites
    arguments_global = sorted(arguments_global, key=lambda x: x["confiance"], reverse=True)

    rang_affiche = 0
    for rang, argument in enumerate(arguments_global):
        if(rang_affiche >= 10):
            break

        confiance = argument["confiance"]

        if argument["weight_relation"] > 0.0 and resultat_global > 0.0:
            verite = "oui"
        elif argument["weight_relation"] < 0.0 and resultat_global < 0.0:
            verite = "non"
        else:
            #verite = "confus"
            continue
            
        
        chaine = f"{rang_affiche} | {verite} | "

        if argument in deductions:
            relation1 = relation_id_to_name(argument["relation1"], dataJSON1)

            chaine += "(deduction) | "
            if element1 := argument["element1"]:
                chaine += f"[{data1} {relation1} {element1}] & "
            if verite == "non":
                chaine += "¬"
            chaine += f"[{element1 if element1 else data1} {relation} {data2}]"

        elif argument in inductions:
            relation_ind = argument["relation"]
            chaine += "(induction) | "
            if element := argument["element"]:
                chaine += f"[{data1} {relation_ind} {element}] & "
            if verite == "non":
                chaine += "¬"
            chaine += f"[{element} {relation} {data2}]"
            
        elif argument in transitivites:
            chaine += "(transitivité) | "
            if element1 := argument["element1"]:
                chaine += f"[{data1} {relation} {element1}] & "
            if verite == "non":
                chaine += "¬"
            chaine += f"[{element1} {relation} {data2}]"    

        chaine += f" | {confiance}"
        print(chaine)
        rang_affiche += 1

###################################################
#              Fonction Principal                 #
###################################################

def main():
    clear_console()
    print("---------------------\nPour nettoyer le cache tappez : 'nettoyer cache'")
    print("---------------------\nEntrez la requête au format : 'aigle/r_agent-1/voler'\n---------------------\n")
    prompt = input()
    print("\n---------------------\n")

    try :
        data1, relation, data2 = prompt.split("/")
    except ValueError as ve :
        try:
            cache = prompt
            if(cache != "nettoyer cache"):
                print("Saisi incorrect")
                return -1
            else:
                for fichier in os.listdir("data"):
                    chemin_fichier = os.path.join("data", fichier)
                    if os.path.isfile(chemin_fichier):
                        print(chemin_fichier + "supprimé")
                        os.remove(chemin_fichier)
                print("---------------------\nLe cache a été correctement nettoyé\n---------------------\n")
                return 0
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

    temps_debut_total = time.time()

    deductions, resultats_deductions = get_clean_deduction_results(data1, data2, relation, dataJSON1, dataJSON2)
    inductions, resultats_inductions = get_clean_induction_results(data1, data2, relation, dataJSON1, dataJSON2)
    transitivite, resultats_transitivites = get_clean_transitivite_results(data1, data2, relation, dataJSON1, dataJSON2)
    
    resultat_global = resultats_deductions + resultats_inductions + resultats_transitivites

    affichage(deductions, inductions, transitivite, resultat_global, data1, data2, relation, dataJSON1, dataJSON2)

    temps_execution_total = time.time() - temps_debut_total
    print("\nTemps d'exécution (avec téléchargements):", format(temps_execution_total),"secondes")

if __name__ == "__main__":
    main()
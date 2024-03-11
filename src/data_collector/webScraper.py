import requests
from bs4 import BeautifulSoup

###################################################
#             HTTP Request Function               #
###################################################

def http_request(data : str):
    print("Telechargement des données requises...")
    url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + data + "&rel="
    try:
        reponse = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la récupération de la page :", e)
    print("Donnees acquises")
    return reponse.text

###################################################
#            Data Acquired Function               #
#  Retourne Vrai si les données ont déjà été dl   #
#            Retourne Faux sinon                  #
###################################################

def data_acquired(data : str):
    try:
        with open("data/data_list.txt", 'r', encoding='utf-8') as txt_file:
            contenu = txt_file.read()
            lines = contenu.split('\n')
            if not(data in lines) :
                with open("data/data_list.txt", 'w', encoding='utf-8') as txt_file:
                    chaine = contenu + str(data) + '\n'
                    txt_file.write(chaine)

                    return False
            else :
                print("Données déjà acquises.")
                return True

    except FileNotFoundError as fnfe :
        with open("data/data_list.txt", 'w', encoding='utf-8') as txt_file:
            chaine = str(data) + '\n'
            txt_file.write(chaine)

            return False

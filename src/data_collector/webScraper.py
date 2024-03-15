import requests
from bs4 import BeautifulSoup
from pathlib import Path

###################################################
#             HTTP Request Function               #
###################################################

def http_request(data : str):
    splited_data = data.split(">")
    clean_data = splited_data[0]
    print("Telechargement des données de : " + clean_data)
    url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + clean_data + "&rel="
    try:
        reponse = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la récupération de la page :", e)
    return reponse.text

###################################################
#            Data Acquired Function               #
#  Retourne Vrai si les données ont déjà été dl   #
#            Retourne Faux sinon                  #
###################################################

def data_already_acquired(data : str):
    splited_data = data.split(">")
    clean_data = splited_data[0]
    try:
        with open("data/"+clean_data+".json", 'r', encoding='utf-8') as json_file:
            #print("Données déjà acquises.")
            return True
    except FileNotFoundError as fnfe :
        try :
            Path("data").mkdir()
        except FileExistsError as fee :
            None
        return False

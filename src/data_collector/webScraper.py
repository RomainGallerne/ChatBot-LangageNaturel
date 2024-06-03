import requests
from bs4 import BeautifulSoup
from pathlib import Path

###################################################
#             HTTP Request Function               #
###################################################

def http_request(data: str):
    try:
        clean_data = data.split(">", 1)[0]
        print("Téléchargement des données de : '" + clean_data + "'...")
        url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + clean_data + "&rel="
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la récupération de la page :", e)
        return None

###################################################
#            Data Acquired Function               #
#  Retourne Vrai si les données ont déjà été dl   #
#            Retourne Faux sinon                  #
###################################################

def data_already_acquired(data: str):
    try:
        clean_data = data.split(">", 1)[0]
        file_path = f"data/{clean_data}.json"
        if Path(file_path).is_file():
            return True
        else:
            Path("data").mkdir(exist_ok=True)  # Crée le répertoire 'data' s'il n'existe pas
            return False
    except Exception as e:
        print("Une erreur est survenue :", e)
        return False
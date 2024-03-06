import requests
from bs4 import BeautifulSoup

url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=tigre&rel="  # Remplacez ceci par l'URL de la page que vous souhaitez récupérer

def get_data(file: str, test: bool = False):
    """
    Fonction qui va sauvegarder fichier dans un .txt
    @param file: str        
    """
    # Déclaration de la variable globale url
    global url
    # Envoi de la requête HTTP GET pour récupérer la page
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la récupération de la page :", e)
    else: 
        # Sauvegarde du contenu de la page dans un fichier
        with open(file, "w", encoding="utf-8") as f:  # Spécification de l'encodage utf-8
            f.write(response.text)
    # Si test est vrai, on affiche le contenu de la page
    if test:
        print(response.text)

def generate_json(file : str){
     # Crée un objet BeautifulSoup pour analyser le contenu HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouve toutes les balises <code> et extrait leur contenu
    code_tags = soup.find_all('CODE')
    for code_tag in code_tags:
        print(code_tag.text)
}

if __name__ == "__main__":
    get_data("data.txt", True)  # On sauvegarde le contenu de la page dans un fichier



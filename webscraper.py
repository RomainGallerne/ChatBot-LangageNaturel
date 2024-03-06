import requests

url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=tigre&rel="

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
        # Sauvegarde du contenu de la page dans un fichier qui sera dans un dossier data
        with open(f"data/{file}", "w", encoding="utf-8") as f:
            f.write(response.text)
    # Si test est vrai, on affiche le contenu de la page
    if test:
        print(response.text)

if __name__ == "__main__":
    get_data("data.txt", True)  # On sauvegarde le contenu de la page dans un fichier

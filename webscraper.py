import requests

url = "https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=tigre&rel="  # Remplacez ceci par l'URL de la page que vous souhaitez récupérer

# Envoi de la requête HTTP GET pour récupérer la page
response = requests.get(url)

# Vérification si la requête a réussi (code de statut 200)
if response.status_code != 200: #La requête a échoué
    print("Erreur lors de la récupération de la page :", response.status_code)
else: #La requête a réussi
    print(response.text)
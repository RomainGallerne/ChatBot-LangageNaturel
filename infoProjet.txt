Interface : 
	- Simple en console

Fonctionnement : 
	- Récupérer un fichier de type "view-source:https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=pigeon&rel=", ici pour les pigeons 
	et l'enregister (SQL, fichier, etc...) puis permettre d'interroger en réalisant des inférences.
	- Attention à la polysémie : un même mot peut avoir plusieurs sens : pigeon l'animal ou pigean celui qui se fait avoir.
	- Attention aux synonimes : livre synonyme de 500g ? Oui car une livre vaut 500g. Il ne faut pas faire ce genre d'inférence.
	- Possibilité de boucher les trous ou corriger les erreurs.
	- Réponse à une requête en moins d'une seconde.

Requêtes :
	- pigeon r.agent-1 voler ?

Types d'inférences :
	- Déductif
		"A isa C" et "C agent-1 B" => "A agent-1 B"
	- Inductif
	- Abductif
	- La relation la plus importante sera "isa"

Evaluation :
	- Soutenance après les examens (sans slides)
	- Via discord (avec les exemples les plus tordus et les polysémies les plus bizarres)
	- Code à rendre après la soutenance avec un README clair et simple pour installer
	- Pas de rapports
	- Groupe de 2

A l'examen écrit :
	- Questions sur inférence
	- Questions sur le projet (algorithme utilisés, problèmes trouvés)

Tâches :
	- Extraction des données brut vers format utilisable
		- Récupération page
		- Traitement code source (isolé les parties <CODES>...)
		- Initialisation BD SQL
		- Insertion BD SQL
	- Algorithme de Requetage
		- Interrogation "bête" -> Est-ce que le tuples est présent de base ?
		- Génération du tuple opposé
		- Inférence par ordre de rank (ordre anti-général) jusqu'à inférer le tuple souhaité ou le tuple opposé
			- Différents type inférence possibles
		- Enregistrement du chemin d'inférence
	- Interface utilisateur
		- Format des requêtes
		- Génération du texte d'explication
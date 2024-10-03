### Résumé
Développement d'un moteur permettant d'interroger une base de données en ligne et d'inférer des connaissances.

Le moteur interroge une base de connaissances en ligne, en l'occurrence la base JeuxDeMots de l'Université de Montpellier. À l'aide des connaissances présentes dans cette base, le moteur est capable d'effectuer une série d'opérations pour inférer de nouvelles connaissances.

Pour cela, trois types d'algorithmes d'inférence sont utilisés :
	* Algorithme de déduction
 	* Algotiyhme d'induction
  	* Algorithme de transitivité des propriétés

Le moteur est donc capable d'effectuer des raisonnements argumentés sur divers éléments. Il peut, par exemple, expliquer que :
	* Un pigeon vole car il s'agit d'un oiseau et qu'à défault d'exception les oiseaux volent.
 	* Une autruche ne vole pas car il s'agit d'un oiseau terrestre et les oiseaux terrestres sont une exception des oiseaux qui ne vole pas.
  	* Une feuille est une partie d'un arbre car il s'agit d'une partie d'une plante et un arbre est une plante.
   	...

### Utilisation
Il faut intéroger le modèle sous la forme suivante :
```
autruche/r_agent-1/voler
```
La liste des relations admises et le détails de leurs significations sont consultables sur le site officiel de la base de données de JeuxDeMots.

### Copyright
```
« Copyright © 19/05/2024, Romain GALLERNE, Loris BENAITHIER Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders X be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.
Except as contained in this notice, the name of Romain GALLERNE and Loris BENAITHIER shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization from Romain GALLERNE and Loris BENAITHIER. »
```

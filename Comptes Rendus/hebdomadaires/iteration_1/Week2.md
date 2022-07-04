# Compte-rendu hebdomadaire Semaine 2
##### 07/12/2020 - 13/12/2020

Au cours de cette semaine, nous avions prévu de chercher davantage d'informations sur la segmentation d'image et notamment de la croissance de régions, d'annoter plus d'images et également de commencer à utiliser pyTorch et Tensor Flow.
Cette semaine a été très chargée, notamment en raison d'un projet de java qui a monopolisé bien plus de temps que prévu, mais également en raison d'un projet d'IA lancé en cours de semaine (avec une échéance toute proche, annoncée seulement extrêmement récemment).

L'annotation d'images a mis un peu de temps à commencer, car nous souhaitions savoir si notre stratégie de créer 3 masques différents (dont un masque créé à l'aide de la croissance de région) était pertinente ou non, car cela influe sur notre façon d'annoter.
N'ayant pas eu de retour, nous sommes partis sur cette base, et pourrons changer en cours de route si besoin sans que cela soit handicapant. 
Plusieurs dizaines de radios de chiens et de chats ont ainsi déjà été annotées (pour chaque radio : une image avec vertèbres T4 et une image avec les points de mesure du coeur).

Pendant les annotations de Théophane et d'Anthony, François a cherché des informations sur la croissance de régions et a commencé à prendre en main de façon très basique PyTorch et Tensor Flow.

Concernant la base de données d'indices de Buchanan, le plus logique semblerait de faire cela en SQL, en utilisant la bibliothèque sqlite3 de Python. Ceci nous permettra de créer cette base de données en local et d'intégrer facilement la BDD à notre programme Python. 
Pour ce qui est de la structure, il ne semble pas spécialement nécessaire de faire plusieurs tables pour l'instant. Une seule table contenant les champs "type" (chien, chat) "race" et "indice" parait amplement suffisant pour l'instant mais il serait intéressant d'étudier la question plus en profondeur en intégrant le fait que de nombreux autres animaux devront être compatibles avec l'IA dans le futur.


Contenu du markdown concernant les méthodes de segmentation : 

# Méthodes de segmentation

3 Grandes familles : 
* segmentation par seuil
	- Seuil global
	- Seuil multiple
	- Seuil variable
* segmentation par région
	- Croissance de région
	- region splitting et region merging
* segmentation par cluster

## Region Split and Merge

### Split
Séparer une image en régions égales => découper la matrice de pixels en plusieurs carrés  de taille similaire.
La première chose à faire est de définir un seuil. Pour cela, on prend une région (au hasard?), et la valeur du seuil pour la suite sera la valeur maximale d'un pixel de la région - la valeur minimale d'un pixel de la région.
On gardera en tête ce seuil pour le reste de la méthode.

Dans chaque région, on effectue le même calcul (max - min). Si cette valeur est supérieure au seuil calculé précédemment, on on sépare en carrés de taille égale cette région (on coupe en 4). Sinon, on effectue le test sur d'autres régions. Une fois que le test a été effectué sur toutes les régions (y compris celles créées lorsque max - min était strictement supérieur au seuil s), on peut passer à la fusion des régions.

### Merge

On compare maintenant deux régions R1 et R2 voisines.
Si max(R1) - min(R2) <= seuil et que max(R2) - min(R1) <= seuil, on peut fusionner les deux régions

### Conclusion split & merge
Gros doutes sur la manière de définir le seuil. Cela reviendrait donc à dire que tout ceci ne dépend que de la première région choisie, et de plus que cette première région ne sera jamais split lors de la première opération. 


## Croissance de région

La segmentation par croissance de région permet de regrouper des régions de manière itératives.
Ces régions sont connexes et unir deux régions doit respecter une propriété d'homogénéité.

Cette homogénéité pourrait être par exemple une distance euclidienne. Dans le cas d'une image RGB, on pourrait représenter 2 pixels dans un espace en 3 dimensions, avec les axes R, G et B.
Calculer la distance entre ces deux pixels est aisé, et pourrait donner un critère d'homogénéité (unir les deux pixels en fonction de la distance calculée et d'un seuil paramétré).

Trois éléments sont à définir :
* Pixels de démarrage de croissance (seed points)
* un ensemble de critères de regroupement de  régions voisines
* une heuristique pour maîtriser la complexité


exemple d'algorithme de croissance de région donné en exemple dans une thèse portant sur la segmentation d'un cerveau :

1. Calculer l'histogramme de la région fusionnée par la dernière étape du split and merge.
2. Création automatique de seuil: calculer la mesure de divergence un utilisant la formule suivante, dans laquelle P(i) est l'histogramme .
	div(i) = (dy/dx)P(i)
3. Le seuil optimal est calculé comme étant la première valeur la plus proche de zéro après le maxima de divergence.
4. Sélection des seed points : tous les pixels de valeur supérieure au seuil optimal.
5. Croissance de région :  La valeur de ce 1er *seed pixel* devient la valeur moyenne de la région (*region mean*). Sélection de ce premier pixel et  faire croître la région en les comparant avec ses voisins (quelle méthode de comparaison??).
 6. Mesurer la différence entre le pixel comparé et la *region mean*. Le processus de croissance s'arrête lorsque cette différence d'intensité est supérieure à la différence entre la *region mean* et le seuil optimal.
 7. On répète les étapes 4 à 6 jusq'à ce qu'il n'y ait plus de *seed point* qui n'appartiennent à aucune région segmentée.


## Supplément

En réalité, (comme on peut le voir dans l'exemple plus haut) les deux méthodes vues ci-dessus peuvent être utilisées en simultané, notamment pour la sélection automatique de *seed points*. On commence par effectuer un split and merge, puis sélectionne automatiquement des seed points à partir des régions définies par le split and merge.

Il n'y aura sans doute pas besoin d'utiliser cette méthode dans notre cas, puisque nous pouvons assez aisément placer un pixel faisant office de seed point sur chaque vertèbre de chaque radio de la BDD.

La première étape de l'algo de croissance de région de l'exemple de segmentation de cerveau utilise l'histogramme d'une région trouvée à l'aide du split and merge, pour ainsi calculer le seuil optimal. Cependant, même si nous ne faisons pas de s&m, nous pouvons éventuellement calculer l'histogramme d'une vertèbre et normaliser cet histogramme comme étant commun à toutes les vertèbres de toutes les radios, pour avoir le seuil. Il est cependant possible que quelques radios soient rigoureusement différentes les unes des autres et que cette approximation soit trop grande. L'idéal serait de calculer l'histogramme d'une vertèbre pour chaque radio.


Autres méthodes  : 
k-means clustering algorithm, fuzzy c-means algorithm, gaussian mixture model w/ expectation maximization algorithm, statistical classification using Gaussian Hidden Markov Random Field model supervised method based on the k nearest neighbour rule.


# Segmentation d'image par K-means

Cet algorithme permet de classer des objets à partir de caractéristiques, dans un certain nombre (K) de classes.
L'algorithme des k-means vise à minimiser la variance intra-classe, ce qui revient à minimiser l'énergie suivante :

![image](https://i.ibb.co/1m9Ys3f/Capture-d-cran-2020-12-13-215242.jpg "minim energie")

ici, C est l'ensemble des clusters, c est un cluser, m_c sont centroïde, V(c) sa variance, #c le nombre d'éléments de c et D l'ensemble des pixels que l'on veut classer

Algorithme basique :

1. initialisation des centroïdes.
2. mise à jour des clusters.
3. réévaluation des centroïdes.
4. itérer les étapes 2. et 3. jusqu'à stabilisation des centroïdes.

## Initialisation

La qualité de cet algorithme dépend énormément du choix des centroPides initiaux, mais certains algos ed kmeans sont moins sensibles à cela que d'autre (comme le "global-k-means" ou le "k-harmonic means")

...

J'ai eu quelques doutes à partir d'ici donc j'ai décidé de lire d'autres articles, et après lecture de ceux-ci, il semblerait que cette méthode ne soit pas la plus pratique pour l'utilisation que l'on pourrait en faire (par rapport à la croissance de région) et introduit semblerait-il des problèmes de connexité spatiales, au niveau des frontières de classes.
# Méthodes de segmentation

Sources :
[https://www.electronique-mixte.fr/wp-content/uploads/2018/07/Formation-Traitement-dimage-cours-12.pdf](https://www.electronique-mixte.fr/wp-content/uploads/2018/07/Formation-Traitement-dimage-cours-12.pdf)

[https://en.wikipedia.org/wiki/Split_and_merge_segmentation](https://en.wikipedia.org/wiki/Split_and_merge_segmentation)

[https://www.researchgate.net/publication/264622966_Automated_Region_Growing_for_Segmentation_of_Brain_Lesion_in_Diffusion-weighted_MRI](https://www.researchgate.net/publication/264622966_Automated_Region_Growing_for_Segmentation_of_Brain_Lesion_in_Diffusion-weighted_MRI)

[http://ultra.sdk.free.fr/docs/Image-Processing/Courses/TRAITEMENT%20NUMERIQUE%20D'IMAGES%20MEDICALES/polyTexture.pdf](http://ultra.sdk.free.fr/docs/Image-Processing/Courses/TRAITEMENT%20NUMERIQUE%20D'IMAGES%20MEDICALES/polyTexture.pdf)

[https://www.researchgate.net/publication/4347685_Texture_Feature_based_Automated_Seeded_Region_Growing_in_Abdominal_MRI_Segmentation](https://www.researchgate.net/publication/4347685_Texture_Feature_based_Automated_Seeded_Region_Growing_in_Abdominal_MRI_Segmentation)

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

5. Croissance de région :  La valeur de ce 1er *seed pixel* devient la valeur moyenne de la région (*region mean*). Sélection de ce premier pixel et faire croître la région en les comparant avec ses voisins (quelle méthode de comparaison??). 

6. Mesurer la différence entre le pixel comparé et la *region mean*. Le processus de croissance s'arrête lorsque cette différence d'intensité est supérieure à la différence entre la *region mean* et le seuil optimal.

7. On répète les étapes 4 à 6 jusq'à ce qu'il n'y ait plus de *seed point* qui n'appartiennent à aucune région segmentée.


### Analyse de texture?

"Il n'existe pas d'approche formelle ni de définition précise de la texture"
Dire qu’*une texture est une région
d’une image présentant une organisation spatiale homogène des niveaux de luminance* est
correct mais très peu précis


2 types de textures : 

* les **macrotextures** (ou textures structurées) pour lesquelles il est facile d’extraire visuellement le motif de base et les lois d’assemblage des primitives entre elles. Ces textures peuvent même présenter une certaine périodicité ou cyclostationnarité
(processus aléatoire plaqué sur un processus périodique). Certains exemples sont représentatifs de ce type de textures, comme la texture d’un mur de brique, de certains tissus ou d’un grillage.
* les **microtextures** (ou textures aléatoires) qui présentent un aspect plus chaotique et plus désorganisé, mais dont l’impression visuelle reste globalement homogène. Les différentes régions d’une image aérienne, les bois, les champs, etc., représentent des textures microscopiques.

Algo proposé :
* initialisation de régions homogènes par leur texture
* croissance de ces régions
* réglage des frontières de régions

#### La mesure de l'information de la texture

Afin de décrire le contenu de la texture (intialisée par les seed points), on introduit des *blocs d'image*, ainsi qu'une *I-mesure*, une mesure de l'information d'une texture dépendant de la résolution de celle-ci.
La *I-mesure* indique la typicité (ensemble des caractéristiques qui font la particularité d'un élément) d'un bloc d'image en fonction des autres blocs de l'image.
Les propriétés de texture sont plus ou moins bien reconnues en fonction du niveau de résolution avec lequel est extrait/observé une caractéristique de l'image.
Il est conseillé d'e décrire l'information sous différents niveaux de résolutions.
Les caractéristiques de texture utilisées peuvent être le niveau de gris et le gradient (magnitude et direction) pour chaque niveau de résolution par exemple.

Afin d'extraire différents types de caractéristiques locales de textures, on utilise une *fenêtre d'observation*.

* **Fenêtre d'observation** : une fenêtre d'observation de niveau de résolution *m* notée *w^(m)* est un carré de taille *q(m)* pixels tels que *q(m) > q(m-1)*, *q(m)* étant un nombre impair égal à *B^(m-1)*.*B* est un nombre impair supérieur à 1, choisi de sorte à placer le centre de la fenêtre d'observation sur un pixel. 

* Soit *b^(m)(i,j)* le voisinage spécifié par *w^(m)* avec un centre (u,j),  et *B^(m) = {b^(m)(i,j)}* tous les voisinsages possibles observées à travers la fenêtre d'observation *w^(m)*.

* Soit *E_t = {k|k = 0,1,2,...,K_t - 1}* un ensemble fini de valeurs discrètes où *K_t* est le nombre d'événements distincts pour la caractéristique *t*. Le schéma d'extraction de caractéristiques est défini comme étant le *mapping* du contenu d'une caractéristique à l'intérieur du voisinage dans l'ensemble *E(T)*.
*f_t^(m): b^(m)(i,j) -> E_t*

La suite de l'article n'est visiblement pas de mon niveau, en plus d'être en anglais, ce qui ne simplifie pas la tâche...

#### Dans un autre article :

Extraction de 3 caractéristiques pour chaque pixel : *co-occurrence* (matrix définie à partir d'une image comme étant la distribution de valeurs de pixels co-occurents(valeurs de niveaux de gris ou de couleurs) pour un offset spécifique), *semi-variogramme* (le semi-variogramme illustre l'auto-corrélation spatiale des points d'échantillonnage mesurés) et le *filtre de Gabor*.

La co-occurence est apparemment extrêmement utilisée en extraction de caractéristique de texture (donc à voir plus en détail).

##### Extraction de caractéristiques de texture

Afin de déouvrir de similitudes entre les pixels, on a besoin d'une extraction de caractéristiques à l'échelle du pixel.  On prendra ici l'exemple d'une image en niveau de gris.
On peut utiliser une approche basée sur l'intensité des pixels, soit ici la valeur en niveau de gris d'un pixel. Cette valeur est donc ainsi une caractéristique. Mais cette approche est la plus basique et pas tout le tmeps suffisante.

Deux différentes approches (parmi d'autres) existent pour l'analyse de texure :
* *all-pairs* : la texture locale est calculée à partir des pixels voisins
* *direction distance pairs*, où la texture locale est calculée pour chaque direction et distance 

Direction et distance en question :
![image](https://i.ibb.co/tCKn20S/distance-pairs.jpg "direction distance pairs")

J'en déduis que les extractions de caractéristiques citées plus haut (co-occurrence, filtre de gabor et semi-variogramme) seront calculées dans 4 directions pour chaque pixel éloigné d'une distance d=1 du pixel initial. Cela veut-il dire que tous ces calculs sont faits à nouveau pour chaque nouveau pixel intégré à la région ?
Il s'agit cependant de l'étape d'extraction de caractéristiques, et non encore de la croissance de régions, donc cela est sans doute fait pour chaque *seed point* uniquement. Mais alors quel est l'avantage de cette deuxième méthode par rapport à la première, dans le cas d'une distance d=1? Car la méthode *all-pairs* semble être une application spécifique de la *direction distance pairs* (je l'appelerai *DDP* désormais) avec d=1 mais pour 8 directions à la fois. Effectuer les calculs pour plus de pixels parait intuitivement plus précis et fiable. A voir si la distance *d* évolue pour la *DDP* et s'il est possible d'éviter de perdre les informations en bas à gauche du pixel. 

##### Co-occurrence

La matrice de co-occurrence permet de caractériser la périodicité et la directivité des textures.
Cette méthode consiste à observer la texture à travers une fenêtre d'observation de la texture en comptabilisant le nombre de paires de pixels distants de *d* qui présentent une différence &Delta;z en niveaux de gris. En plus de la distance, on tient compte de la direction définie par toute paire de pixels.
Toute la matrice est définie à partir d'un critère, ou d'un relation géométrique entre deux pixel *(x1, y1)* et *(x2, y2)*. Exemple :
		*x2 = x1 + 1*					*y2 = y1*


Cette matrice est carrée et de dimension GxG, où G est le nombre de niveaux de gris présents dans la fenêtre d'observation.
Si une image a 4 niveaux de gris, alors la matrice sera 4x4 avec comme indices (0, 1, 2, 3).
Les lignes de cette matrice sont notées i, les colonnes j.
i = {0, 1, 2, 3}	j = {0, 1, 2, 3}
Soit C la matrice.
Soit une image f contenant des pixels (x, y), la valeur d'un pixel est f(x,y). 
Pour revenir à notre relation, f(x1, y1) = i et f(x2, y2) = j.
Trouver la valeur de C(i, j) revient alors à chercher les pixels (x1,y1) et (x2,y2), tels que f(x1, y1) = i et f(x2, y2) = j qui vérifient la relation précédente.
Dans le cas d'une direction de 0° (cad notre relation géométrique), cela revient à trouver toutes les occurences de f(x1,y1) = i ayant à sa droite f(x2,y2) = j.

Voici un exemple (image à gauche, matrice à droite) : 

![image](https://i.ibb.co/0CmY4f4/co-occurrence.jpg "Matrice co-occurrence")

Cet exemple est tiré d'un [cours](http://www.telecom.ulg.ac.be/teaching/notes/totali/elen016/node113_mn.html), et ne donne pas le même résultat que le mien, pour la même direction. J'ai passé du temps à comprendre pourquoi, mais en regardant d'autres cours ou même des vidéos, je trouvais le bon résultat avec ma technique.
Je mets ici la réponse donnée par le cours, qui me semble être fausse (pour la même relation géométrique et la même image), mais je peux m'être trompé.

![image](https://i.ibb.co/LtcY3hr/fausse-correction.jpg "correction")

On comprend maintenant mieux ces 4 directions 0°, 45°, 90° et 135° qui nous permettent de générer 4 matrices de co-occurrence.
Toutes ces matrices sont de taille GxG avec G nombre de niveaux de gris.

Pour une image contenant 256 niveaux de gris, la matrice de 256x256 est importante mais est encore raisonnable.
Seulement, les radiologies ont généralement bien plus de niveaux de gris (environ 1400), et une matrice 1400x1400 est tout de suite moins raisonnable.
Afin de réduire cette charge, on utilise un système de bins.
*Clipped binning strategy* est une méthode de bins, pour lequel un grand bin est alloué aux faibles intensités de niveaux de gris (de 0 à une seuil I1), un autre pour les fortes intensités (seuil I2 et plus) et 30 bins de même taille sont alloués pour le reste des seuils (entre I1 et I2).

I1 et I2 sont déterminés à partir de l'histogramme de l'image.
Plus précisément, I1 est initialisé à la valeur du premier minimum local (le premier creux), puisque les pixels les plus foncés seront majoritairement l'arrière plan.
Pour I2, il s'agit d'un minimum local à partri duquel il n'y a que très peu de pixels.

Nous n'avons donc plus que 32 "niveaux de gris" disponibles.
C'est seulement après cette opération que l'on crée la matrice de co-occurrence, dans les 4 directions.
A partir d'une matrice, nous pouvons calculer 14 caractéristiques  de texture à l'aide des méthodes de *Haralick*. Cela nous donne donc 14x4=56 caractéristiques de textre, qui consistent en l'espace de caractéristique de texture de co-occurrence pour chaque pixel.

Voici les Formules d'Haralick pour extraire chaque caractéristique :
![image](https://i.ibb.co/mRYHMSZ/haralick.jpg "Haralick Texture features")

##### Filtre de Gabor

Les ondelettes de Gabor sont également l'une des méthodes les plus populaires pur l'extraction de caractéristiques de texture.
Voici le filtre de Gabor et ses paramètres associés : 
![image](https://i.ibb.co/C0Zz0GV/Gabor.jpg "Gabor's filter")

Ce filtre est tout d'abord appliqué à tous les pixels de l'image, pour toutes les directions (0, 45, 90 et 135)
Afin de représenter les caractéristiques de texture, on fait la moyenne et la déviation standard de la magnitde des coefficients.
Ceci nous donne alors un vecteur de caractéristiques.

##### Semi-variogramme 2D

Pour chaque pixel, génération de 4 variogrammes directionnels (mêmes directions que d'habitude) avec une distance d=1.
Afin d'obtenir le semi-variogramme :

![image](https://i.ibb.co/SVVJNHg/semi-vraiogramme.jpg "semi-variogramme")

Ici, G(x,y) représente le niveau de gris pour un pixel (x,y) de l'image.
Pour une direction de 0°, cela revient à faire la somme des différences de niveaux de gris entre un pixel à droite d'un autre et de cet autre pixel.
Exemple en utilisant une fenêtre de d'observation de 3x3 pixels :

112
323
012

Ceci donne alors *sqrt(|1-1|+|1-2|+|3-2|+|2-3|+|0-1|+|1-1|+)/6*
soit *0.33*.



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

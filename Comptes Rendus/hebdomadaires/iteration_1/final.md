# Compte-rendu dernière semaine + itération 1/

#### 18/12/2020

## Itération 1

Voici le tout dernier rapport de cette première itération.
Le sentiment global de l'équipe est les projets annoncés au dernier moment ou bien les projets dont le rapport charge de travail/temps pour rendre le projet sont très importants impactent de façon particulièrement importante le planning de PTrans initialement prévu.

Dans ces derniers jours plus libres, nous avons pu rattraper une bonne partie de notre retard par rapport à ce que nous avions prévu de faire, l'itération 1 n'est selon nous pas tout à fait complète.

Au cours de cette itération, nous avions prévu ceci :

- Recherche bibliographique

  - Celle-ci a pris beaucoup plus de temps que prévu et peut potentiellement durer toute la phase de projet, puisqu'il peut toujours être intéressant de rechercher davantage de techniques ou de bonnes pratiques. De plus, nous devons anticiper que lors du développement d'une nouvelle fonctionnalité technique, il est probable que nous n'ayions pas pensé à tout et que cela nécessite alors quelques nouvelles recherches. Cette recherche bibliographique a notamment été longue car il m'est arrivé de chercher à décrypter pendant trop longtemps des articles scientifiques (en anglais) d'un niveau bien plus élevé que le mien et bien trop précis, nécessitant d'être spécialiste du domaine en amont. Malgré tout, j'ai recueilli bon nombre d'informations et de techniques, qui nous paraissent réalisables
  - Nous nous sommes mis d'accord sur le fonctionnement général du projet. Nous aurons donc besoin de segmenter les vertèbres (comme prévu) afin de pouvoir les compter. Cette segmentation se fera par croissance de région, en analysant les histogrammes des vertèbres mais également en extrayant des caractéristiques de texture à l'aide de la matrice de co-occurrence, du filtre de Gabor ou encore du semi-variogramme. Cette segmentation nous donne alors un premier masque.
  - En complément du masque des vertèbres, nous avons l'annotation des images, qui nous formera deux masques. Un premier masque sera la position de T4, un dernier sera les positions des points de mesure sur le coeur.
  - Avoir ces 3 masques nous permettra de faire évoluer graduellement le projet du mode semi-automatique au mode automatique. Ils seront les points d'entrée d'un réseau UNet, particulièrement adapté à la segmentation d'image et à l'imagerie en général.

- Annotation des radios

  - L'annotation a dû attendre que nous soyions sûrs de la façon dont nous allions procéder (pour les masques). Pour chaque radio de chien et de chat, il existe deux images annotées (une pour la vertèbre et une pour le coeur). Malheureusement, certaines radios étaient bien trop illisibles pour permettre à des élèves ingénieurs en informatique (bien que très attachés à ces petites boules de poils) de placer les points de mesure. Afin d'éviter d'annoter n'importe comment, Théophane et Anthony ont préféré laisser ces quelques radios de côté.
  - Avancement des annotations :

        | Animal                 | Chien | Chat |
        |------------------------|-------|------|
        | Nombre total de radios | 116   |   70 |
        | T4 annotées            | 108   |   63 |
        | Coeurs annotés         | 68    |   37 |
        | radios restantes       | 0     |    0 |

    - Je vous ai joint par mail des des exemples d'annotations ainsi que des exemples de radiographies difficilement annotables

* Prise en main des bases des PyTorch et TensorFlow

  - Ces derniers jours, j'ai essayé de prendre en main PyTorch et TensorFlow pour avoir un premier avis sur quelle bibliothèque utiliser. Les conditions de tests sont les suivantes :
  - J'ai commencé par tester TensorFlow, en élaborant un réseau de neurones classique de classification de vêtements (t shirt, pullover, chaussures etc). J'ai suivi pour cela un tutoriel disponible sur le site officiel de TensorFlow, qui était très facile à suivre. La documentation est bien faite et la prise en main très facile. En une vingtaine de lignes de codes, le réseau de neurones est fonctionnel. La bibliothèque ne donne cependant pas l'impression d'avoir un très grand contrôle sur ce que l'on fait. Cette impression est sûrement erronnée, et est en partie due au fait que l'on a pas l'impression de coder en python, mais d'utiliser en boucle des fonctions de Tensor Flow qui font automatiquement beaucoup de choses en arrière plan.
  - Afin de tester la facilité de prise en main de PyTorch, je me suis donné comme but de refaire le même exercice, avec les mêmes données, en essayant d'approcher le plus possible la structure du réseau du même programme avec Tensor Flow. Ceci a été fait avec l'aide de la documentation de PyTorch et de quelques recherches sur internet, mais je n'ai pas utilisé le "tutoriel en 1h" proposé par Pytorch présentant l'ensemble du fonctionnement de la bibliothèque. Après avoir passé beaucoup de temps sur le programme, avoir fait ce tuto aurait été un très gros +, et devra être fait par tout le monde dans le futur si nous choisissons cette bibliothèque. L'exercice était donc bien plus difficile qu'avec TensorFlow. Tout comme pour TensorFlow, la documentation est très bien faite. Contrairement à TensorFlow cette fois, la sensation de contrôle était bien plus présente avec Pytorch, ce qui augmente en contrepartie drastiquement le nombre de lignes de codes. Le code est bien plus _"pythonique"_, tout en faisant appel à plusieurs fonctions de PyTorch qui font tout un travail automatique derrière. Ces fonctions me paraissent cependant un peu plus atomique. Au lieu d'avoir quelques fonctions qui font énormément de tâches, il y en a davantage qui ont une tâche bien spécifique. Il faut cependant prendre nen compte le fait que je ne maîtrise pas les outils, et que certains de ces points peuvent ne pas être tout à fait véridiques. Le critère le plus objectif que je puisse trouver est qu'un programme PyTorch ressemble beaucoup plus à du Python qu'un programme TensorFlow. On notera aussi la qualité de la documentation dans les deux bibliothèques
  - Le choix est donc difficile, mais un élément supplémentaire fait penser la balance pour PyTorch : M. Normand semble maitriser l'outil. En cas de problème très spécifiqueou en cas de mauvaises pratiques de notre part, M. Normand pourra alors bien plus facilement nous aider. De plus, PyTorch (comme TensorFlow) possède une API C++, pour une intégration plus facile à ImedView. Nous pensons donc pour l'instant travailler avec PyTorch

* Création de la base de données des indices de Buchanan
  - Je devais m'occuper de la création de la base pendant cette itération, mais avec le temps raccourci par les différents projets de ces dernières semaines, j'ai préféré me concentrer sur des tâches bien plus primordiales. De plus, la création de cette unique table devrait être très rapide, et peut donc être repoussée sans contraintes à la prochaine itération selon nous. Cette base sera une base postgreSQL, comme demandé par M. Brouard.

Voici le résultat des mes recherches concernant l'analyse de texture. Le premier article que j'ai tenté de résumer était bien trop complexe, cela m'a fait perdre beaucoup de temps. La deuxième partie des recherches est sans doute plus intéressante.
Vous le verrez à la lecture mais je n'ai pas compris pourquoi la réponse donnée par un cours concernant la matrice de co-occurrence à un exemple différait du mien. Je serais ravi d'apprendre où est l'erreur.

### Analyse de texture

"Il n'existe pas d'approche formelle ni de définition précise de la texture"
Dire qu’_une texture est une région
d’une image présentant une organisation spatiale homogène des niveaux de luminance_ est
correct mais très peu précis

2 types de textures :

- les **macrotextures** (ou textures structurées) pour lesquelles il est facile d’extraire visuellement le motif de base et les lois d’assemblage des primitives entre elles. Ces textures peuvent même présenter une certaine périodicité ou cyclostationnarité
  (processus aléatoire plaqué sur un processus périodique). Certains exemples sont représentatifs de ce type de textures, comme la texture d’un mur de brique, de certains tissus ou d’un grillage.
- les **microtextures** (ou textures aléatoires) qui présentent un aspect plus chaotique et plus désorganisé, mais dont l’impression visuelle reste globalement homogène. Les différentes régions d’une image aérienne, les bois, les champs, etc., représentent des textures microscopiques.

Algo proposé :

- initialisation de régions homogènes par leur texture
- croissance de ces régions
- réglage des frontières de régions

#### La mesure de l'information de la texture

Afin de décrire le contenu de la texture (intialisée par les seed points), on introduit des _blocs d'image_, ainsi qu'une _I-mesure_, une mesure de l'information d'une texture dépendant de la résolution de celle-ci.
La _I-mesure_ indique la typicité (ensemble des caractéristiques qui font la particularité d'un élément) d'un bloc d'image en fonction des autres blocs de l'image.
Les propriétés de texture sont plus ou moins bien reconnues en fonction du niveau de résolution avec lequel est extrait/observé une caractéristique de l'image.
Il est conseillé d'e décrire l'information sous différents niveaux de résolutions.
Les caractéristiques de texture utilisées peuvent être le niveau de gris et le gradient (magnitude et direction) pour chaque niveau de résolution par exemple.

Afin d'extraire différents types de caractéristiques locales de textures, on utilise une _fenêtre d'observation_.

- **Fenêtre d'observation** : une fenêtre d'observation de niveau de résolution _m_ notée _w^(m)_ est un carré de taille _q(m)_ pixels tels que _q(m) > q(m-1)_, _q(m)_ étant un nombre impair égal à _B^(m-1)_._B_ est un nombre impair supérieur à 1, choisi de sorte à placer le centre de la fenêtre d'observation sur un pixel.

- Soit _b^(m)(i,j)_ le voisinage spécifié par _w^(m)_ avec un centre (u,j), et _B^(m) = {b^(m)(i,j)}_ tous les voisinsages possibles observées à travers la fenêtre d'observation _w^(m)_.

- Soit _E_t = {k|k = 0,1,2,...,K_t - 1}_ un ensemble fini de valeurs discrètes où _K_t_ est le nombre d'événements distincts pour la caractéristique _t_. Le schéma d'extraction de caractéristiques est défini comme étant le _mapping_ du contenu d'une caractéristique à l'intérieur du voisinage dans l'ensemble _E(T)_.
  _f_t^(m): b^(m)(i,j) -> E_t_

La suite de l'article n'est visiblement pas de mon niveau, en plus d'être en anglais, ce qui ne simplifie pas la tâche...

#### Dans un autre article :

Extraction de 3 caractéristiques pour chaque pixel : _co-occurrence_ (matrix définie à partir d'une image comme étant la distribution de valeurs de pixels co-occurents(valeurs de niveaux de gris ou de couleurs) pour un offset spécifique), _semi-variogramme_ (le semi-variogramme illustre l'auto-corrélation spatiale des points d'échantillonnage mesurés) et le _filtre de Gabor_.

La co-occurence est apparemment extrêmement utilisée en extraction de caractéristique de texture (donc à voir plus en détail).

##### Extraction de caractéristiques de texture

Afin de déouvrir de similitudes entre les pixels, on a besoin d'une extraction de caractéristiques à l'échelle du pixel. On prendra ici l'exemple d'une image en niveau de gris.
On peut utiliser une approche basée sur l'intensité des pixels, soit ici la valeur en niveau de gris d'un pixel. Cette valeur est donc ainsi une caractéristique. Mais cette approche est la plus basique et pas tout le tmeps suffisante.

Deux différentes approches (parmi d'autres) existent pour l'analyse de texure :

- _all-pairs_ : la texture locale est calculée à partir des pixels voisins
- _direction distance pairs_, où la texture locale est calculée pour chaque direction et distance

Direction et distance en question :
![image](https://i.ibb.co/tCKn20S/distance-pairs.jpg "direction distance pairs")

##### Co-occurrence

La matrice de co-occurrence permet de caractériser la périodicité et la directivité des textures.
Cette méthode consiste à observer la texture à travers une fenêtre d'observation de la texture en comptabilisant le nombre de paires de pixels distants de _d_ qui présentent une différence &Delta;z en niveaux de gris. En plus de la distance, on tient compte de la direction définie par toute paire de pixels.
Toute la matrice est définie à partir d'un critère, ou d'un relation géométrique entre deux pixel _(x1, y1)_ et _(x2, y2)_. Exemple :
x2 = x1 + 1
y2 = y1

Cette matrice est carrée et de dimension GxG, où G est le nombre de niveaux de gris présents dans la fenêtre d'observation.
Si une image a 4 niveaux de gris, alors la matrice sera 4x4 avec comme indices (0, 1, 2, 3).
Les lignes de cette matrice sont notées i, les colonnes j.
i = {0, 1, 2, 3} j = {0, 1, 2, 3}
Soit C la matrice.
Soit une image f contenant des pixels (x, y), la valeur d'un pixel est f(x,y).
Pour revenir à notre relation, f(x1, y1) = i et f(x2, y2) = j.
Trouver la valeur de C(i, j) revient alors à chercher les pixels (x1,y1) et (x2,y2), tels que f(x1, y1) = i et f(x2, y2) = j qui vérifient la relation précédente.
Dans le cas d'une direction de 0° (cad notre relation géométrique), cela revient à trouver toutes les occurences de f(x1,y1) = i ayant à sa droite f(x2,y2) = j.

Voici un exemple (image à gauche, matrice à droite) :

![image](https://i.ibb.co/0CmY4f4/co-occurrence.jpg "Matrice co-occurrence")

Cet exemple est tiré d'un cours, et ne donne pas le même résultat que le mien, pour la même direction. J'ai passé du temps à comprendre pourquoi, mais en regardant d'autres cours ou même des vidéos, je trouvais le bon résultat avec ma technique.
Je mets ici la réponse donnée par le cours, qui me semble être fausse (pour la même relation géométrique et la même image), mais je peux m'être trompé.

![image](https://i.ibb.co/LtcY3hr/fausse-correction.jpg "correction")

On comprend maintenant mieux ces 4 directions 0°, 45°, 90° et 135° qui nous permettent de générer 4 matrices de co-occurrence.
Toutes ces matrices sont de taille GxG avec G nombre de niveaux de gris.

Pour une image contenant 256 niveaux de gris, la matrice de 256x256 est importante mais est encore raisonnable.
Seulement, les radiologies ont généralement bien plus de niveaux de gris (environ 1400), et une matrice 1400x1400 est tout de suite moins raisonnable.
Afin de réduire cette charge, on utilise un système de bins.
_Clipped binning strategy_ est une méthode de bins, pour lequel un grand bin est alloué aux faibles intensités de niveaux de gris (de 0 à une seuil I1), un autre pour les fortes intensités (seuil I2 et plus) et 30 bins de même taille sont alloués pour le reste des seuils (entre I1 et I2).

I1 et I2 sont déterminés à partir de l'histogramme de l'image.
Plus précisément, I1 est initialisé à la valeur du premier minimum local (le premier creux), puisque les pixels les plus foncés seront majoritairement l'arrière plan.
Pour I2, il s'agit d'un minimum local à partri duquel il n'y a que très peu de pixels.

Nous n'avons donc plus que 32 "niveaux de gris" disponibles.
C'est seulement après cette opération que l'on crée la matrice de co-occurrence, dans les 4 directions.
A partir d'une matrice, nous pouvons calculer 14 caractéristiques de texture à l'aide des méthodes de _Haralick_. Cela nous donne donc 14x4=56 caractéristiques de textre, qui consistent en l'espace de caractéristique de texture de co-occurrence pour chaque pixel.

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

|     |     |     |
| --- | --- | --- |
| 1   | 1   | 2   |
| 3   | 2   | 3   |
| 0   | 1   | 2   |

Ceci donne alors _sqrt(|1-1|+|1-2|+|3-2|+|2-3|+|0-1|+|1-2|+)/6_
soit _0.33_.

## Itération 2

Dans cette partie, nous verrons quelles modifications apporter à notre planning initial pour cette itération 2.
Pour rappel, voici le GANTT que nous avions prévu lors du cahier des charges :

![image](https://i.ibb.co/4PKPYFM/GANTT.jpg "GANTT")

Pour cette itération 2, nous souhaitions donc commencer la segmentation des vertèbres, ainsi que la localisation de la vertèbre T4.
Nous comptions également commencer à nous familiariser avec ImedView, afin de repérer les interfaces avec lesquelles nous devrons travailler pour intégrer le projet au logiciel, récupérer les données comme la radio elle-même, les coordonnées des points de mesures faites par le vétérinaire etc.

Il n'y a selon nous pas de raison de ne pas traiter l'un de ces 3 sujets, qui sont primordiaux. L'accent sera porté sur la segmentation des vertèbres ainsi que la localisation de T4 en cas d'imprévus ou de surcharge de travail.
Il faut ajouter à cela la création de la BDD d'indices, qui sera très rapide.
Nous pouvons également compter quelques heures de recherches bibliographiques supplémentaires en cas de besoin (majoritairement pour la segmentation des vertèbres). Selon nous, la localisation de T4 sera bien plus évidente que la segmentation.

## Risques au cours de l'itération 2

L'itération 2 est sans doute l'itération comportant le plus de risques. Il y a tout d'abord les vacances de Décembre, qui ralentiront le rythme de travail avec les fêtes.
Nous avons une série de DS la première semaine de janvier, qui viendra bousculer également le rythme de travail.
Dernier risque : le Hyblab. Pendant une semaine, nous aurons à effectuer un projet avec des étudiants de l'école de design. Ayoub Massoudi nous a indiqué avoir envoyé un mail à tous les tuteurs et clients concernant ce projet.

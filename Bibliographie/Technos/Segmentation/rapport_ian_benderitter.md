rapport_ian_benderitter

# Résumé des points principaux du rapport de stage de Ian Benderitter

## Extraction de caractéristiques

Afin d'effectuer une segmentation (et cela peu importe la méthode), il faut lui fournir des informations sur l'image pour de meilleurs résultats.

L'analyse de texture (comme noté dans le rapport bibliographique de recherche sur l'analyse de texture) permet d'identifier des motifs ou des arrangements dans une image ou une partie de l'image.

Différentes méthodes d'analyses de textures exisitent, telles que la matrice de coocurrence, la matrice d'auto corrélation, les filtres de Gabor (3 techniques explicitées dans le rapport évoqué plus haut) ou encore la *mesire d'énergie des textures de laws*.

Rappel de la formule de calcul des filtres de Gabor ainsi que les effets de la variation des paramètres de la formule sur une image :

![image](https://i.ibb.co/xJ9hSgP/gabor-formule.jpg "Formule Gabor")

![image](https://i.ibb.co/HYY25rF/variantes-gabor.jpg "Variantes Gabor")

## Mesure d'énergie des textures de Laws

Mesure la quantité de variation d'énerie au sein d'une fenêtre de pixels de taille fie.
5 Vecteurs utilisés pour faire un set de matrices de 5x5. Chacun de ces vecteurs permet une détection de caractéristique particulière. 

![image](https://i.ibb.co/QfFK8pS/Laws-matrice.jpg "Matrice de Laws")

Ces vecteurs sont multipliés entre eux afin de créer 9 matrices 5x5.
Il ne faut pas oublier de calculer également ces matrices en miroir.
La première matrice est donc L5xE5 et son miroire est E5xL5. La matrice finale correspondante est la moyenne de ces deux matrices. 
Ces 9 matrices sont ensuite appliquées à une image afin de créer 9 *energy maps* différentes de la même image. Voici les 9 matrices en question :

```
L5E5/E5L5
L5R5/R5L5
E5S5/S5E5
S5S5
R5R5
L5S5/S5L5
E5E5
E5R5/R5E5
S5R5/R5S5
```

Formule permettant de calculer la matrice d'énergie pour chaque caractéristique: 

![image](https://i.ibb.co/QmbNCq5/laws-formule.jpg "Matrice d'énergie de Laws")

r ? c? i? j? k? F? c'est pas expliqué


## Unet

extrait intéressant : 

```
Le réseau DeepUNet est un réseau convolutionnel, c’est-à-dire qu’une grande partie
des couches le composant sont des étages appliquant une convolution sur l’image. Ainsi,
le réseau apprend au cours de l’entraînement en créant notamment des filtres permettant
de détecter les caractéristiques plus ou moins cachées de l’image qui vont lui permettre
de prendre la décision de quelle classe attribuer à chaque pixel.
Ainsi, il serait intéressant de fournir au réseau des informations qu’il ne pourrait pas
retrouver seul dans l’image ; c’est-à-dire des transformations plus complexes que des
convolutions. Parmi les caractéristiques précédemment introduites, celles qui pourraient
fournir des informations inédites au réseau sont le calcul de l’homogénéité et des niveaux
laplaciens. L’homogénéité est calculée à partir d’une convolution et du calcul de la
variance, et les niveaux laplaciens correspond à une soustraction entre des images convoluées,
dont une sous-échantillonnée.
```

Il est intéressant de voir que le Unet peut nous permettre de nous passer de passer en entrées certains caractéristiques. Le calcul d'homogénéité dont il est question ici est malheureusement trèèèès lourd (4min par image). Cela parait donc difficilement concevable si nous voulons approcher les 5 secondes de temps de calcul pour obtenir un résultat.
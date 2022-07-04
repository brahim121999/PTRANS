# Le réseau UNet

Le réseau UNet est une architecture spécifique de machine learning pour la segmentation d'images, regroupant plusieurs concepts. On y trouve un assemblage particulier d'éléments tel que les réseaux de neurones, le pooling etc.

Avant de s'intéresser spécifiquement au réseau UNet, il est primordial de s'intéresser au réseau de neurones convolutif (CNN).

## Réseaux de convolution CNN

source : [https://arxiv.org/abs/1603.07285](https://arxiv.org/abs/1603.07285)

Couche d'entrée d'un CNN : une image. Cette image est en 3 dimensions si celle-ci est en couleur (largeur, hauteur, RGB).

Chaque neurone de chaque couche n’est exposé qu’à un champ réceptif particulier de la couche précédente, et l’analyse faite par ce neurone pour ce champ récepteur est la même qu’un autre neurone pour un autre champ récepteur.


Un neurone observe un champ de pixels de la couche précédente et lui applique une matrice de convolution (ou convolution kernel), constituée de poids synaptiques. En multipliant cette matrice de convolution par les valeurs des pixels du champs, puis en faisant la somme des valeurs de cette nouvelle matrice, on obtient la nouvelle valeur du neurone. Ce neurone sera excité ou non selon sa fonction d’activation.

Certaines valeurs connues de matrice de convolution permettent d'exécuter certaines tâches. On trouve des valeurs de matrices dédiées à la détection des contours, à l'amélioration de la netteté, au floutage etc.

![image](https://linkpicture.com/q/kernel.png "Matrice de convolution")

Le processus d’apprentissage se traduit par l’amélioration des matrices de convolution. En gardant la même matrice de convolution par couche, on garantit une invariance par translation des images. En réalité, on génère plusieurs « cartes de caractéristiques » à partir de la couche précédente. Chaque carte de caractéristique est générée à partir d’une matrice de convolution différente. 

![image](https://www.linkpicture.com/q/carte_carac.png "Cartes de caractéristiques")

Par exemple : générer 8 cartes de caractéristiques à partir de la couche d’entrée reviendrait à effectuer 8 fois les mêmes calculs sur toute l’image à l’aide de 8 matrices de convolutions différentes. Dans le cas d’une image de 28x28 pixels, générer 8 cartes de caractéristiques génère alors un vecteur de 8 fois 28x28 pixels, avant phase de pooling. 


Nous ne voulons pas davantage augmenter les dimensions des données. D’où la phase de réduction de la dimension appelée pooling (average pooling ou max pooling, qui calculent la moyenne ou le maximum d’excitation de neurones voisins) -> résume l’information de plusieurs neurones voisins en une seule information. On a donc une représentation moins précise de l’image mais de dimension moindre.

![image](https://www.linkpicture.com/q/pooling.png "Pooling (méthode max)")

On recommence ensuite le process en boucle. 
Toute cette première partie du réseau permet l’extraction de caractéristiques (forme, texture, couleur) de l’image. Une fois fait, nous pouvons utiliser traiter ces caractéristiques à l’aide de nouvelles couches de neurones qui agissent en tant que classificateur par exemple. 


## Les spécificités du réseau UNet

![image](https://lmb.informatik.uni-freiburg.de/people/ronneber/u-net/u-net-architecture.png "Réseau Unet")

Le réseau Unet peut être séparé en deux parties. Une première de contraction, qui est la partie CNN expliquée précédemment.
Le but de la deuxième partie est cette fois d'augmenter en résolution afin d'appliquer les caractéristiques à une échelle plus petite (à l'échelle 1:1)

Il faut donc suréchantilloner les cartes de caractéristiques.
On "étire" ces cartes en ajoutant des zéros artificiels entre les pixels. On pourra ensuite obtenir la couche supérieure avec un [traitement de convolution transposée](https://arxiv.org/pdf/1603.07285.pdf), ou encore [ceci](https://medium.com/apache-mxnet/transposed-convolutions-explained-with-ms-excel-52d13030c7e8) (animations explicatives). Ce zéros servent donc à augmenter la résolution des cartes de caractéristiques, puis sont transformés en valeurs en fonction de la mathode de convolution transposée utilisée.

Une fois que les caractéristiques sont suréchantillonées, on copie à côté de la déconvolution le résultat de la convolution de même niveau en phase descendante (concaténation). Traitement de convolution sur tout l'ensemble. Ensuite, on refait un traitement de déconvolution, et ainsi de suite.

Une fois tous les traitements faits, on fait un dernier traitement de convolution de noyaux 1:1, et on doit avoir un nombre de couches égal au nombre d'objets que l'on veut faire reconnaitre au réseau de neurones (le  coeur et les vertèbres par exemple)

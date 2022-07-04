# Compte-rendu hebdomadaire Semaine 1
##### 29/11/2020 - 06/12/2020

Voici notre premier compe-rendu hebdomadaire depuis le kick off.
Au cours de cette semaine, nous avons très majoritairement fait des recherches sur les techniques d'IA de segmentation d'images, plus spéficiquement le réseau UNet, qui semble être un outil très puissant et en vogue, avec beaucoup de ressources disponibles. 
Cette recherche bibliographique était prévue sur une seule semaine, sur notre diagramme de GANTT, or il est maintenant évident que celle-ci aura sans lieu sur toute l'itération, voire même les suivantes.

Les annotations d'images ont commencé, et Anthony s'est également renseigné sur keras, une lib python très performante généralement utilisée avec Tensor Flow.


## 1 Segmentation d'images

L'un des points les plus importants de ce P-trans est la segmentation d'images, afin de repérer les différentes vertèbres, la vertèbre T4 et les points de mesure du coeur. 
Nous nous sommes d'ores et déjà majoritairement orientés vers le réseau UNet, une architecture de réseaux de neurones très en vogue, très performante et très utilisée dans le milieu médical. 

### 1.1 Le réseau U-Net

Le réseau UNet est une architecture spécifique de machine learning pour la segmentation d'images, regroupant plusieurs concepts. On y trouve un assemblage particulier d'éléments tel que les réseaux de neurones, le pooling etc.

Avant de s'intéresser spécifiquement au réseau UNet, il est primordial de s'intéresser au réseau de neurones convolutif (CNN).

#### 1.1.1 Réseaux de convolution CNN

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


#### 1.1.2 Les spécificités du réseau UNet

![image](https://lmb.informatik.uni-freiburg.de/people/ronneber/u-net/u-net-architecture.png "Réseau Unet")

Le réseau Unet peut être séparé en deux parties. Une première de contraction, qui est la partie CNN expliquée précédemment.
Le but de la deuxième partie est cette fois d'augmenter en résolution afin d'appliquer les caractéristiques à une échelle plus petite (à l'échelle 1:1)

Il faut donc suréchantilloner les cartes de caractéristiques.
On "étire" ces cartes en ajoutant des zéros artificiels entre les pixels. On pourra ensuite obtenir la couche supérieure avec un [traitement de convolution transposée](https://arxiv.org/pdf/1603.07285.pdf), ou encore [ceci](https://medium.com/apache-mxnet/transposed-convolutions-explained-with-ms-excel-52d13030c7e8) (animations explicatives). Ce zéros servent donc à augmenter la résolution des cartes de caractéristiques, puis sont transformés en valeurs en fonction de la mathode de convolution transposée utilisée.

Une fois que les caractéristiques sont suréchantillonées, on copie à côté de la déconvolution le résultat de la convolution de même niveau en phase descendante (concaténation). Traitement de convolution sur tout l'ensemble. Ensuite, on refait un traitement de déconvolution, et ainsi de suite.

Une fois tous les traitements faits, on fait un dernier traitement de convolution de noyaux 1:1, et on doit avoir un nombre de couches égal au nombre d'objets que l'on veut faire reconnaitre au réseau de neurones (le  coeur et les vertèbres par exemple)

#### 1.1.3 Résumé d'articles scientifiques du Réseau U-Net

##### **DoubleU-Net: A Deep Convolutional Neural Network for Medical Image Segmentation**

###### Abstract
Tentative d'améliorer les performances de l'architecture UNet pour la segmentation d'image (ici sémantique, c'est-à-dire la labellisation de chaque pixel des objets qui nous intéressent dans l'image).
Cette architecture : le *doubleUnet*, soit un empilement de deux UNet.
Le premier Unet (VGG-19) est pré entrainé, à partir de caractéristiques d'ImageNet. Ils ont ensuite ajouté un deuxième UNet en dessous afin de capter plus d'informations sémantiques plus efficacement.
Utilisation du **Atrous Spatial Pyramid Pooling** (ASPP) (voir ce qu'est la spécificité de ce pooling).
Le réseau a été testé sur la détection automatique de polyps, et semble plus performant que le Unet simple.

Description du VGG-19 par MathHelps: *VGG-19 is a convolutional neural network that is 19 layers deep. You can load a pretrained version of the network trained on more than a million images from the ImageNet database [1]. The pretrained network can classify images into 1000 object categories, such as keyboard, mouse, pencil, and many animals. As a result, the network has learned rich feature representations for a wide range of images. The network has an image input size of 224-by-224*

(segmentation sémantique. Est-ce que ça peut nous intéresser? à voir)

###### L'architecture

![image](https://i.ibb.co/kQtcYkP/double-Unet.jpg "Architectrue")

On voit ici les deux réseaux UNet utilisés. Les parties *encoder* semblent être la première partie d'un réseau UNet, soit la phase d'analyse et de découverte de caractéristiques. La phase *decoder* semble donc correspondre à la deuxième partie de synthèse d'un réseau UNet, soit la remontée jusqu'à l'affichage des caractéristiques.  
La première question que l'on peut se poser est "à quoi ressemble OUTPUT 1 en sortie de premier neurone. A-t-on déjà une première segmentation de l'input? Pourquoi réinsérer une image déjà segmentée peut faire apparaitre de nouvelles informations?"

Explications de l'article :

Particularité de l'architecture : l'utilisation de VGG-19 dans le premier réseau, couplé à l'ASPP et au décodage.
Le deuxième réseau est quant à lui est un réseau UNet tout à fait classique, mais sa particularité esst l'utilisation de l'ASPP.
Dans le premier réseau : le UNet modifié génère un masque  (OUTPUT 1). On multiplie ensuite le masque produit par le réseau 1 et l'INPUT de base (à quoi est-ce que ça correspond exactement?), pour s'en servir d'INPUT pour le deuxième réseau.

La concaténation du masque intermédiaire et du masque en sortie du 2ème UNet donne l'OUTPUT final, afin de foir la différence entre les deux OUTPUT.
Concernant l'ASPP : ce pooling s'est popularisé depuis peu en segmentation d'image car il présente de meilleures performances lors de l'extraction de caractéristiques de haute résolution.

Explications complémentaires pour l'encodeur:
Le premier encodeur est l'encodeur VGG-19 (décrit dans l'abstract). Le second est créé de toute pièce. Chaque bloc d'encodeur effectue une opération de convolution 3x3 ainsi qu'un "batch normalization" (normalisation de la couche précédente par centrage et réduction afin de rentdre un CNN plus stable).
La fonction d'activation utilisée est ReLU (Rectified Linear Unit)
![image](https://miro.medium.com/max/357/1*oePAhrm74RNnNEolprmTaQ.png "Fonction d'activation ReLu")

L'utilisation de cette fonction est justifiée comme ayant pour but d'introduire de la non-linéarité dans le modèle.
Cela est suivi par un block "d'excitation", qui améliore la qualité de la carte de caractéristiques (comment? sous quelle forme?).
Enfin, utilisation du max-pooling en 2x2 ainsi qu'un stride de 2. Si j'ai bien compris, un stride est l'ajout de colonnes de pixels qui agissent comme des buffers d'informations contenues dans les lignes suivantes. Seulement, il est indiqué que ce stride de 2 permet de réduire la dimension spatiale de chaque carte de caractéristique, ce qui ne colle pas avec l'idée d'ajouter des colonnes de pixels.

Explications complémentaires pour le décodeur:
Chaque bloc de décodage effectue un suréchantillonage bilinéaire de chaque caractéristique en input, ce qui double la dimension des cartes de caractéristiques. 
La concaténation avec les cartes de caractéristiques de l'encodeur est ensuite faite.
La particularité ici est que le décodeur du premier UNet reçoit les cartes caractéristiques de VGG-19 mais que le décodeur du deuxième réseau reçoit non seulement les cartes de caractéristiques de son encodeur mais également celles de VGG-19, ce qui est censé encore une fois améliorer la qualité des cartes de caractéristiques. 
Après concaténation, application de deux opérations de convulutions transposées 3x3, d'une opération de "batch normalization", d'une fonction d'activation ReLU puis à nouveau d'un bloc d'excitation.
Enfin, génération du masque à l'aide d'une couche de convolution (fonction d'activation utilisée : sigmoid).

![image](https://miro.medium.com/max/3268/1*a04iKNbchayCAJ7-0QlesA.png "Sigmoid Function")


###### Conclusion

L'article propose une architecture intéressante et qui semble efficace, mais cela ne semble pas applicable à notre projet. Le fait que le premier réseau UNet soit pré-entrainé sur des caractéristiques d'images réelles (et non de radiologies) à l'aide d'imageNet est très contraignant. Nous n'avons pas accès à autant de données ni à un encodeur pré-entrainé de radiologies vétérinaires. 
Nous devrons sans doute nous en tenir à un seul UNet (si nous utilisons cette architecture). 
Il peut cependant être intéressant de noter la présence de l'ASPP (Atrous Spatial Pyramid Pooling), qui peut nous être utile.



**Stride** - Dans le contexte d'une opération de convolution ou de pooling, la stride SS est un paramètre qui dénote le nombre de pixels par lesquels la fenêtre se déplace après chaque opération.

![image](https://stanford.edu/~shervine/teaching/cs-230/illustrations/stride.png?36b5b2e02f7e02c3c4075a9d836c048cg "Stride")

<br/>
<br/>
<br/>
<br/>

##### **Bi-Directional ConvLSTM U-Net with Densley Connected Convolutions**

###### Abstract

Amélioration de l'architecture UNet pour la segmentation d'images médicales, qui prend appui sur le réseau UNet, la convolution bidirectionnelle *ConvLSTM* et la convulution dense.
L'effort est majoritairement produit sur les "skip connections", les fameux liens entre phase d'encodage et décodage.
Cet article propose alors une autre méthode que la simple concaténation de cartes de caractéristiques lors de cette opération.
Afin renforcer la propagation de caractéristiques, la dernière couche de convolution de la phase **d'encodage** est une couche de convolution dense. Afin d'éviter une redondance d'apprentissage de caractéristiques, les blocs de cette couche sont reliés entre eux (décrit plus bas).
Utilisation également du **Batch normalization** comme dans l'article précédent.
Cette amélioration du réseau U-Net sera appelée BCDU-Net tout au long de ce résumé.

###### Architecture

![image](https://i.ibb.co/C9bG80w/BCDU-net.jpg "Architecture du BCDU-Net")

###### Encodage

4 étapes d'encodage. 
Chacune de ces étapes consiste à faire deux convolutions à l'aide de matrices 3x3, suivies de deux opérations de max pooling 2x2 ainsi que d'une fonction d'activation ReLu.
Le nombre de cartes de caractéristiques est doublé à chaque étape.
La dernière étape de la phase d'encodage d'un réseau U-Net est généralement constituée d'une suite de couches de convolution, or ces convolutions successives peuvent créer une redondance dans l'apprentissage des caractéristiques.
Afin d'éviter ce problème, le BCDU-Net utilise des convolutions denses, comme ci dessous :
![image](https://i.ibb.co/JxH1LmF/dense-layersot.jpg "dense layer")

En faisant cela, les cartes de caractéristiques sont réutilisées tout au long de cette phase. Ceci a un avantage sur la convolution classique.
Cela aide le réseau à apprendre différentes caractéristiques au lieu de caractéristiques redondantes.

###### Décodage

Chaque étape de décodage commence par un surréchantillonage de la couche précédente. Dans un U-Net classique, les cartes de caractéristiques de niveau correspondant pendant l'encodage sont concaténées aux cartes de caractéristiques obtenues.
Ici, BCDU-Net utilise BConvLSTM (une convolution plus complexe). 

![image](https://i.ibb.co/tz60wxm/Capture-d-cran-2020-12-04-175203.jpg "BConvLSTM")

Plus de détails techniques mathématiques sur l'article original.



\--------------------------------------------------------


Ces deux articles sont basés sur des IA écrites avec TensorFlow. C'est la bibliothèque qui semble la plus utilisée, mais il y avait tout de même de nombreux articles sur des IA faites à l'aide de PyTorch.

### 1.2 Croissance de région

Le principe de base de la croissance de région pour segmenter une image est de faire croître chaque région autour d'un pixel de départ.

Nous avons vu 3 méthodes de croissance de région, l'agrégation, la relaxation et la propagation. Mais les exemples trouvés ont l'air extrêmement peu satisfaisants sur une image contenant du bruit.

Les radios ne contiennent pas forcément de bruit mais les régions sont loin d'être facilement dinstinguables, il est difficile d'imaginer un algorithme de croissance de région fonctionner dessus, mais nous continuerons à nous pencher sur le sujet, et sur d'autre solutions existantes.


## 2 Prémices de fonctionnement

Les méthodes vues précédemment devraient nous permettre de segmenter les vertèbres à partir de radiologies. Mais un point très important est qu'un réseau UNet, comme n'importe quel réseau de neurones, doit apprendre à partir de données déjà segmentées. 

Pour localiser la vertèbre T4, il n'y pas nécessairement besoin de segmenter les données, une simple annotation sous forme de marque indiquant la vertèbre T4 suffit. De même pour les points de mesures sur le coeur. En revanche, compter les vertèbres nécessitera une segmentation.

Voici donc comment nous pourrions procéder.

![image](https://i.ibb.co/CsjJGVb/whiteboard.png "Fonctionnement")

Tout d'abord pour les vertèbres. Il nous faut les segmenter, et nous pourrions utiliser pour cela la technique de croissance de région (par exemple). Ceci nous génèrerait un masque (ici en vert) ne représentant que les vertèbres.

Pour la vertèbre T4, nous devons annoter sur chaque radio la position de la vertèbre T4. Une question se pose encore : colorier un seul pixel au lieu d'une petite zone est-il plus intéressant à faire pour l'IA? Ceci nous génère alors un masque supplémentaire (on ne voit pas bien sur le schéma mais il y a un point rouge représentant la vertèbre T4).

Pour les points de mesure du coeur, tout comme pour T4, nous pouvons placer les points sur la radio et ensuite générer un masque (ici bleu).

Avoir trois masques séparés nous permet de travailler plus facilement sous forme d'itération de fonctionnalité. Plus l'IA devra être capable de prédire de choses à la fois (plus nous nous rapprochons du mode automatique), plus nous pouvons ajouter de masques.

Nous pourrons ainsi également mesurer plus facilement la performance de notre modèle à l'aide des outils dédiés à cela et proposés par tensor flow et pytorch.


## 3 Pytorch ou Tensor Flow?

Nous avons continué à voir quelques comparaisons entre les deux bibliothèques, mais nous n'avons pas encore testé nous-même l'une d'entre elles. 

Cependant, après avoir lu de nombreux articles et vu des vidéos de présentation de concepts d'IA, il semblerait que Tensor Flow soit plus omniprésent que PyTorch. Malgré ça, la facilité d'utilisation (tout en étant efficace) de PyTorch ajoutée aux connaissances de Nicolas Normand sur cette bibliothèque nous attire suffisamment pour être encore indécis.





Très bonne semaine à vous, nous sommes toujours diisponibles sur Mattermost pour la moindre question concernant ce compte-rendu.
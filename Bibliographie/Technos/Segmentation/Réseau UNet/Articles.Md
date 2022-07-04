# Articles de recherche

[https://arxiv.org/abs/1603.07285](https://arxiv.org/abs/1603.07285)

## DoubleU-Net: A Deep Convolutional Neural Network for Medical Image Segmentation

Source : [https://arxiv.org/abs/2006.04868](https://arxiv.org/abs/2006.04868)

#### Abstract
Tentative d'améliorer les performances de l'architecture UNet pour la segmentation d'image (ici sémantique, c'est-à-dire la labellisation de chaque pixel des objets qui nous intéressent dans l'image).
Cette architecture : le *doubleUnet*, soit un empilement de deux UNet.
Le premier Unet (VGG-19) est pré entrainé, à partir de caractéristiques d'ImageNet. Ils ont ensuite ajouté un deuxième UNet en dessous afin de capter plus d'informations sémantiques plus efficacement.
Utilisation du **Atrous Spatial Pyramid Pooling** (ASPP) (voir ce qu'est la spécificité de ce pooling).
Le réseau a été testé sur la détection automatique de polyps, et semble plus performant que le Unet simple.

Description du VGG-19 par MathHelps: *VGG-19 is a convolutional neural network that is 19 layers deep. You can load a pretrained version of the network trained on more than a million images from the ImageNet database [1]. The pretrained network can classify images into 1000 object categories, such as keyboard, mouse, pencil, and many animals. As a result, the network has learned rich feature representations for a wide range of images. The network has an image input size of 224-by-224*

(segmentation sémantique. Est-ce que ça peut nous intéresser? à voir)

#### L'architecture

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


#### Conclusion

L'article propose une architecture intéressante et qui semble efficace, mais cela ne semble pas applicable à notre projet. Le fait que le premier réseau UNet soit pré-entrainé sur des caractéristiques d'images réelles (et non de radiologies) à l'aide d'imageNet est très contraignant. Nous n'avons pas accès à autant de données ni à un encodeur pré-entrainé de radiologies vétérinaires. 
Nous devrons sans doute nous en tenir à un seul UNet (si nous utilisons cette architecture). 
Il peut cependant être intéressant de noter la présence de l'ASPP (Atrous Spatial Pyramid Pooling), qui peut nous être utile.



**Stride** - Dans le contexte d'une opération de convolution ou de pooling, la stride SS est un paramètre qui dénote le nombre de pixels par lesquels la fenêtre se déplace après chaque opération.

![image](https://stanford.edu/~shervine/teaching/cs-230/illustrations/stride.png?36b5b2e02f7e02c3c4075a9d836c048cg "Stride")




## Bi-Directional ConvLSTM U-Net with Densley Connected Convolutions

source : [https://arxiv.org/abs/1909.00166](https://arxiv.org/abs/1909.00166)

#### Abstract

Amélioration de l'architecture UNet pour la segmentation d'images médicales, qui prend appui sur le réseau UNet, la convolution bidirectionnelle *ConvLSTM* et la convulution dense.
L'effort est majoritairement produit sur les "skip connections", les fameux liens entre phase d'encodage et décodage.
Cet article propose alors une autre méthode que la simple concaténation de cartes de caractéristiques lors de cette opération.
Afin renforcer la propagation de caractéristiques, la dernière couche de convolution de la phase **d'encodage** est une couche de convolution dense. Afin d'éviter une redondance d'apprentissage de caractéristiques, les blocs de cette couche sont reliés entre eux (décrit plus bas).
Utilisation également du **Batch normalization** comme dans l'article précédent.
Cette amélioration du réseau U-Net sera appelée BCDU-Net tout au long de ce résumé.

#### Architecture

![image](https://i.ibb.co/C9bG80w/BCDU-net.jpg "Architecture du BCDU-Net")

##### Encodage

4 étapes d'encodage. 
Chacune de ces étapes consiste à faire deux convolutions à l'aide de matrices 3x3, suivies de deux opérations de max pooling 2x2 ainsi que d'une fonction d'activation ReLu.
Le nombre de cartes de caractéristiques est doublé à chaque étape.
La dernière étape de la phase d'encodage d'un réseau U-Net est généralement constituée d'une suite de couches de convolution, or ces convolutions successives peuvent créer une redondance dans l'apprentissage des caractéristiques.
Afin d'éviter ce problème, le BCDU-Net utilise des convolutions denses, comme ci dessous :
![image](https://i.ibb.co/JxH1LmF/dense-layersot.jpg "dense layer")

En faisant cela, les cartes de caractéristiques sont réutilisées tout au long de cette phase. Ceci a un avantage sur la convolution classique.
Cela aide le réseau à apprendre différentes caractéristiques au lieu de caractéristiques redondantes.

##### Décodage

Chaque étape de décodage commence par un surréchantillonage de la couche précédente. Dans un U-Net classique, les cartes de caractéristiques de niveau correspondant pendant l'encodage sont concaténées aux cartes de caractéristiques obtenues.
Ici, BCDU-Net utilise BConvLSTM (une convolution plus complexe). 

![image](https://i.ibb.co/tz60wxm/Capture-d-cran-2020-12-04-175203.jpg "BConvLSTM")

Plus de détails techniques mathématiques sur l'article original.



## U-Net: Convolutional Networks for Biomedical
Image Segmentation

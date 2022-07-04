# PTrans Sujet3 Imedsys


Racine du dossier de dev du projet.
Contient les différentes données (statiques ou non), les scripts, les jeux de tests.

Nous avons travaillé avec un environnement virtuel.
Les requirements sont recensés dans requirements.txt.
Pour installer les requirements :
pip install -r requirements.txt


## Données 

Il y a deux types de données à manipuler : les vérités terrain et les indices de Buchanan.
Ces données sont à placer dans le dossier data.

### Indices de Buchanan

Dans le dossier data/buchanan sont recensés les indices de buchanan dans indices.csv.
L'essentiel pour créer la Base de données se trouve dans le dossier scripts/database.
Les identifiants de connexion à la base de données postgresql sont situés dans le fichier database.ini.
La création de la table des indices de buchanan se fait à l'aide de create_buchanan.py, qui fait
appel à connect.py mais également à config.py.
Config.py récupère les informations contenues dans database.ini et connext.py retourne l'objet de connexion
à la base de données (permettant d'effectuer des opérations dessus).

Pour créer la table, il suffit donc de changer les informations de database.ini puis de lancer le script create_buchanan.py.

### Vérité terrain

La vérité terrain se doit simplement de respecter l'architecture proposée afin que l'apprentissage 
se déroule sans problèmes.
Dans le dossier data, nous avons le dossier Verite_terrain.
Nous avons alors les deux types d'animaux (ici Chients et Chats), puis pour chacun de ces animaux, les masques et 
radios correspondants. Coeur, Process_epineux, Radios et Vertebres. 



## Apprentissage

L'apprentissage se fait à partir du fichier train.py dans le dossier src. 
train.py utilise les fichiers contenus dans le dossier model mais également du dossier dataset. 
Le dossier model contient deux modèles de réseau U-Net, une première version ainsi qu'une seconde.
La première version est entièrement contenue dans model.py.
La deuxième est séparée en deux fichiers : unet_model.py (initialisation du modle + forward) et unet_parts.py (blocs de contraction et d'expansion du réseau).
La structure du réseau est facilement interchangeable à partir des constructeurs des deux modèles.  

le dossier dataset contient le fichier dataset.py, créant l'outil Dataset de pytorch pour l'apprentissage.
Les chemins de la vérité terrain sont à fournir dans le constructeur de RadioDataset().

Lancement de l'apprentissage et des paramètres d'apprentissage avec train.py. 

## Prédiction

La prédiction du réseau à partir d'une radio se fait à l'aide du fichier predict.py dans le dossier src.
Il est nécessaire de fournir le chemin de la radio à prédire mais également le modèle utilisé.
Les différents apprentissages sont situés dans le dossier output.

## Post-Traitement

Il existe trois manières de lancer le post-traitement. On peut :
- soit lancer le calcul de l'indice de buchanan.
- soit lancer indépendamment les post-traitements du coeur et de t4.

### Indice

Pour lancer le calcul de l'indice de Buchanan, allez dans le fichier Dev/src/calcul_indice.py. 

Choisir l'animal à traiter en donnant le nom du fichier de la radiographie choisie dans la variable "img". 

Ensuite, éxécuter le fichier. 

Vous pouvez choisir d'afficher ou non les résultats en changeant la valeur booléenne de la variable "plot".

### Coeur

Pour lancer le post-traitement d'un coeur, aller à la fin du fichier, coeur.py situé dans "Dev/src/postprocess/" :

Choisir un fichier de coeur segmenté. Rentrez l'emplacement (paths) de la photo dans la variable "h_f".
Pour simplifier, l'image peut être directement dans le dossier "postprocess".

Vous pouvez choisir d'afficher ou non les résultats en changeant la valeur booléenne de la variable "plot".

### Vertèbre T4

Pour lancer le post traitement de T4, allez à la fin du fichier T4.py situé dans "Dev/src/postprocess/" :

Choisir les fichiers de vertèbres et processus épineux segmentés. Rentrez les emplacements (paths) des images dans les variables :
"p_f" pour les processus.
"v_f" pour les vertèbres. 

Pour simplifier, les images peuvent être directement dans le dossier "postprocess".


Vous pouvez choisir d'afficher ou non les résultats en changeant la valeur booléenne de la variable "plot".



## Project PTrans ImedIA : Semantic Segmentation using BCE with Logits (Binary class detection)

Ce projet a été réalisé dans le cadre du PTrans des 4A INFO à Polytech Nantes

## Pour commencer (très important)

Pour bien débuter ce projet il faut charger les 4 notebooks fournis dans ce dossier sur Google Colab.

Après il faut télécharger le dossier entier du git et le  charger sur votre compte google drive pour purvoir y accéder à travers Colab.

Ensuite, regrouper les radios des chats et chiens qui sont sous vérités terrains dans un seul dossier nommé "Radios".

Regrouper les masques des coeurs des chats et chiens dans un seul dossier "Coeurs".

Regrouper les masques des processus épineux des chats et chiens dans un seul dossier "Process_epineux".

Regrouper les masques des vertèbres des chats et chiens dans un seul dossier "Vertebres".

Pensez à faire certaines mises à jour des chemins des dossiers contenants les images selon votre architecture.

### Pré-requis

- Google Colab


## Démarrage

Pour lancer l'entrainement du coeur, veuillez ouvrir dans colab le fichier "PTRANS_coeur_BCE_With_Logits_Unet_2048.ipynb"
Ensuite exécutez les cellules de 1 à 24.
Après pour refaire les entrainements de zero vous n'avez qu'a relancé un nouveau training dans la cellule 25, puis n'oubliez pas
de l'enregistrer dans la cellule 26 et le charger dans la 27.
Pour reprendre les training à partir de la 550ème epochs vous n'aurez qu'a chargé le modèle fournit "model_01052022_UNET_2048_BCEWithLogits_epochs550_lr_1e-3.pth" dans la cellule 34.

Pour lancer l'entrainement des processus épineux, veuillez ouvrir dans Colab le fichier "PTRANS_process_BCE_With_Logits_Unet_2048.ipynb"
Ensuite exécutez les cellules de 1 à 27.
Après pour refaire les entrainements de zero vous n'avez qu'a relancé un nouveau training dans la cellule 28, puis n'oubliez pas
de l'enregistrer dans la cellule 29 et le charger dans la 30.
Pour reprendre les training à partir de la 850ème epochs vous n'aurez qu'a chargé le modèle fournit "model_10052022_Process_UNET_2048_BCEWL_epochs850.pth" dans la cellule 35.

Pour lancer l'entrainement des vertèbres, veuillez ouvrir dans Colab le fichier "PTRANS_vertebres_BCE_With_Logits_Unet_2048.ipynb"
Ensuite exécutez les cellules de 1 à 27.
Après pour refaire les entrainements de zero vous n'avez qu'a relancé un nouveau training dans la cellule 28, puis n'oubliez pas
de l'enregistrer dans la cellule 29 et le charger dans la 30.
Pour reprendre les training à partir de la 1200ème epochs vous n'aurez qu'a chargé le modèle fournit "model_10052022_Vertebres_UNET_2048_BCEWL_epochs1200_posweight20.pth" dans la cellule 35.

Pour visualiser les résultat des 3 modèles veuillez charger dans Colab le fichier "PTRANS_3masks_BCE_With_Logits_Unet_2048.ipynb"
Ensuite executez les cellules une à une depuis le début, qui chargera les modèles , montrera les images vérités terrains et enfin
affichera les prédictions regroupées sur une même radio. 

Vérifiez surtout les paths des modèles et des radios avant de les charger.


## Auteurs
* **Adam Creusevault**
* **Mattéo Boursault**
* **Ibrahim Braham**




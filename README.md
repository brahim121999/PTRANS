# 🩺 Projet PTrans – ImedIA

**Mattéo Boursault - Adam Creusevault - Ibrahim Braham**  
**Encadrants :**  
- Tuteur école : Nicolas Normand  
- Tuteur entreprise : Olivier Brouard (IMEDSYS)

---

## 📌 Contexte

Ce projet s'inscrit dans le cadre d'un partenariat entre notre école et l'entreprise **IMEDSYS**, qui développe depuis 2010 un logiciel de radiologie vétérinaire : **IMEDVIEW**.

Durée du projet : **1 an**  
Équipe : **3 étudiants**  
Objectif global : **Automatiser certaines mesures médicales à partir d'images radiographiques à l'aide de techniques de Computer Vision et d'IA**.

---

## 🎯 Objectifs du projet

Le projet vise à automatiser 3 mesures médicales utilisées dans le diagnostic vétérinaire :

- **Indice de Buchanan** → Pour diagnostiquer une **cardiomégalie**
- **Angle de Norberg-Olsson** → Pour détecter une **dysplasie de la hanche**
- **Angle du plateau tibial** → Pour les analyses orthopédiques

Ces mesures sont actuellement réalisées **manuellement** dans le logiciel IMEDVIEW.

---

## 🧠 Approche technique

### 🧬 Computer Vision & Réseaux de neurones

- Utilisation d’un **réseau de neurones convolutif U-NET**, adapté à la **segmentation d’images biomédicales**
- Objectif : identifier automatiquement les structures anatomiques nécessaires au calcul des mesures

### 🔄 Entraînement du modèle

- Constitution d’un **jeu de données** (radio labellisées)
- Application de **data augmentation**
- Séparation en :  
  - **Training set** (80%)  
  - **Validation set** (10%)  
  - **Test set** (10%)  

- Réglage progressif des **méta-paramètres**
- Calcul d’un **indice de confiance global**

---

## 🔗 Intégration logicielle

Une étape cruciale du projet est d’**interfacer le code Python (IA)** avec le **code C++ de l’interface IMEDVIEW**.

Solution envisagée : utilisation de **PyTorch C++ API** ou autres techniques de ponts Python-C++.

---

## 📈 Avancement par mesure

| Mesure                 | État d’avancement                            |
|------------------------|----------------------------------------------|
| **Cardiomégalie**      | 🟢 Codage U-NET, calcul Buchanan, test IA     |
| **Dysplasie**          | 🔴 Non abordée pour l’instant                |
| **Plateau tibial**     | 🔴 Non abordé                                |

---

## 🔁 Prochaines itérations

### 🧪 Itération 1 : Cardiomégalie
- Enrichissement du dataset
- Entraînement de l’IA + ajustement des paramètres
- Calcul d’un indice de confiance

### ⚙️ Itération 2 : Intégration C++/Python
- Lecture du code C++ d’IMEDVIEW
- Recherche de solutions d’interfaçage
- Implémentation et test

---

## 💬 Remarques

- Le projet touche un **domaine interdisciplinaire** : informatique, IA, radiologie vétérinaire
- Contrainte technique importante : **compatibilité Windows 10**

---

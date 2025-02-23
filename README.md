# Projet : Système de Recommandation (Notebook)

Bienvenue dans le dépôt **OC_IA_P10_Recommandation_contenu**. Ce dépôt contient principalement un Notebook me permettant d’explorer et de tester différentes approches de recommandation, d’entraîner des modèles (notamment **ALS**), et de documenter les résultats.

---

## Objectif du projet

L’objectif principal est de développer un système de recommandation capable de proposer des articles pertinents et personnalisés aux utilisateurs. Pour cela, j’explore diverses méthodes :  
- **Filtrage collaboratif** (modèle ALS, etc.)  
- **Filtrage basé sur le contenu** (approche exploratoire)  

---

## Méthodes de recommandation explorées

1. **Filtrage basé sur le contenu** : j’évalue la pertinence des articles en me basant sur leurs propriétés (titre, texte, tags, etc.) pour les rapprocher des préférences utilisateur.  
2. **Filtrage collaboratif** : j’étudie les interactions (clics, vues, notations) entre utilisateurs et articles pour recommander des articles semblables à ceux consultés par d’autres utilisateurs ayant des goûts similaires.  
3. **Modèle Alternating Least Squares (ALS)** : au sein du filtrage collaboratif, ce modèle se distingue par sa robustesse et sa capacité à gérer des données utilisateurs de grande dimension.

### 🏆 **Meilleure méthode et meilleur modèle**
L’évaluation des performances a démontré que **le filtrage collaboratif** est la méthode la plus performante.  
Dans cette approche, **le modèle Alternating Least Squares (ALS)** s’impose comme la meilleure option, obtenant les **meilleures performances globales** sur toutes les métriques clés (précision, MAP, NDCG, similitude moyenne).  
> **Conclusion** : L’approche **collaborative** combinée au **modèle ALS** constitue la **solution de référence** pour offrir des **recommandations pertinentes et personnalisées** aux utilisateurs de My Content.

---

## Contenu du dépôt

- **Notebook principal**  
  - Prétraitement et exploration des données (ex. `clicks_sample.csv`).  
  - Entraînement et évaluation des modèles (notamment ALS).  
  - Comparaison des performances sur plusieurs métriques (précision, rappel, MAP, NDCG).

- **Fichiers de configuration** (par ex. `requirements.txt`)  
  - Lister les dépendances Python nécessaires pour exécuter le Notebook.

---

## Installation et exécution

1. **Cloner le dépôt**  
   ```bash
   git clone https://github.com/preudh/OC_IA_P10_Recommandation_contenu.git
   ```
2. **Installer les dépendances** (dans un environnement virtuel recommandé)  
   ```bash
   pip install -r requirements.txt
   ```
3. **Lancer le Notebook**  
   ```bash
   jupyter notebook
   ```
   Ensuite, ouvrir le Notebook principal pour découvrir les analyses et le code d’entraînement.

---

## Architecture globale et lien avec les autres dépôts

Ce dépôt se concentre exclusivement sur la partie R&D :  
- **Expérimentation**,  
- **Entraînement** et  
- **Comparaison** des modèles.

La mise en production repose sur une **architecture serverless** grâce à Azure Functions, et l’application front-end est développée avec **Streamlit**. Les deux autres dépôts associés sont :

- **OC_IA_P10_RecoFunction** : mon projet Azure Functions, qui expose une API. [Lien GitHub](https://github.com/preudh/OC_IA_P10_RecoFunction)  
- **OC_IA_P10_STREAMLIT_APP** : l’interface Streamlit, accessible via [https://p10-streamlit-app-2025.azurewebsites.net/](https://p10-streamlit-app-2025.azurewebsites.net/), qui interagit avec l’API pour afficher des recommandations aux utilisateurs.

---

**Note** : L’implémentation finale (Azure + Streamlit) s’appuie sur les travaux effectués dans ce Notebook pour proposer un **système de recommandation robuste** (ALS) directement accessible et scalable dans le cloud.
```
** Plateforme de Streaming en Temps Réel pour la Gestion et l’Analyse d’Utilisateurs **

Ce projet propose de créer une pipeline de bout en bout pour ingérer, traiter et visualiser un flux de données en temps quasi réel. 

### **Objectifs du Projet** ###

- **Ingestion des données :** Collecte de profils fictifs via l'API Random User.
- **Traitement temps réel :** PySpark pour transformations et agrégations.
- **Stockage optimisé :** MongoDB (données brutes) & Cassandra (données agrégées).
- **Visualisation continue :** Tableau de bord Streamlit avec rafraîchissement automatique.

****

## **1. Architecture Générale** ##

```
+-----------------------+
|   Random User API     |
+-----------------------+
        |
        v
+-----------------------+
|   Producteur Kafka    |
+-----------------------+
        |
        v
+-----------------------+
|     Cluster Kafka     |
+-----------------------+
        |
        v
+-----------------------+
|  PySpark Streaming    |
+-----------------------+
    |         |         |
    v         v         v
 MongoDB   Cassandra   Streamlit
```

****

## **2. Mise en Place de Kafka et du Topic** ##

- **Installation :** Kafka + Zookeeper (ou Docker).
- **Démarrage :** Lancer Kafka et créer un topic `random_user_data`.

**Pourquoi Kafka ?**
- Découplage des sources et des traitements.
- Gestion automatique des messages et scalabilité.

****

## **3. Producteur Python (Ingestion)** ##

- **API Call :** `https://randomuser.me/api/?results=10`
- **Envoi Kafka :** Conversion JSON et push des messages.
- **Gestion des erreurs :** Retry + logs des requêtes.

****

## **4. Traitement Streaming avec PySpark** ##

- **Connexion Kafka :** Lecture en continu.
- **Parsing JSON :** Transformation des données.
- **Agrégations :** `count(*)`, `avg(age)` par pays.

**Stockage :**
- **MongoDB :** Données brutes.
- **Cassandra :** Données transformées + statistiques.

****

## **5. Bases de Données** ##

- **MongoDB :** Insertion automatique des documents.
- **Cassandra :** Tables optimisées pour agrégats.

****

## **6. Construction du Dashboard (Streamlit)** ##

- **Affichage brut :** Derniers utilisateurs.
- **Statistiques :** Graphiques démographiques.
- **Rafraîchissement :** Mise à jour automatique.

****

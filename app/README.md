# Application de Prédiction de Chiffres Manuscrits avec MNIST

Ce projet comprend une API FastAPI et une application Streamlit pour la prédiction de chiffres manuscrits à partir du jeu de données MNIST.

## Structure du Projet
```
├── app/
│   ├── streamlit_app.py        # Application Streamlit avec canvas de dessin
│   └── Dockerfile.streamlit    # Dockerfile pour l'application Streamlit
├── models/                     # Dossier pour les modèles entraînés
├── main.py                     # API FastAPI pour la prédiction
├── test_api.py                 # Tests unitaires pour l'API
├── Dockerfile                  # Dockerfile pour l'API
├── Dockerfile.test             # Dockerfile pour les tests
├── docker-compose.yml          # Configuration Docker Compose
└── README.md                   # Ce fichier
```

## Prérequis

* Docker et Docker Compose installés.

## Installation et Exécution

1.  **Cloner le dépôt :**

    ```bash
    git clone <URL_DU_REPO>
    cd <NOM_DU_DOSSIER>
    ```

2.  **Démarrer l'application avec Docker Compose :**

    ```bash
    docker-compose up --build
    ```

3.  **Accéder à l'application :**

    * L'API FastAPI sera accessible à l'adresse `http://localhost:8000`.
    * L'application Streamlit sera accessible à l'adresse `http://localhost:8501`.

4.  **Exécution des tests:**

    Les tests sont lancés automatiquement lors du lancement de docker-compose. Ils utilisent pytest.

## Fonctionnalités

### API FastAPI

* **`/predict` (POST) :** Prend une image en entrée et retourne la prédiction du chiffre manuscrit et les probabilités associées.
* **`/retrain` (POST) :** Réentraîne le modèle MNIST.

### Application Streamlit

* Interface de dessin pour dessiner des chiffres manuscrits.
* Bouton "Prédire" pour envoyer l'image à l'API et afficher les résultats.
* Affichage de la prédiction et des probabilités.

## Tests

Les tests unitaires pour l'API sont inclus dans le fichier `test_api.py`. Ils vérifient :

* La prédiction avec une image valide.
* La gestion des images invalides.
* Le réentraînement du modèle.

## Dépendances

* FastAPI
* Uvicorn
* Scikit-learn
* Joblib
* Python-multipart
* Pillow
* Streamlit
* Streamlit-drawable-canvas
* Requests
* pytest

## Docker

L'application est conteneurisée avec Docker pour une installation et une exécution faciles. Le fichier `docker-compose.yml` configure les services nécessaires :

* `api` : Conteneur pour l'API FastAPI.
* `test` : Conteneur pour les tests unitaires.
* `streamlit` : Conteneur pour l'application Streamlit.

## Utilisation

1.  Lancez l'application via docker compose.
2.  Ouvrez l'application Streamlit dans votre navigateur.
3.  Dessinez un chiffre dans le canvas.
4.  Cliquez sur le bouton "Prédire" pour voir le résultat.
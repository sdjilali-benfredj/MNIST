```
├── api/
│   ├── main.py                     # API FastAPI pour la prédiction et le réentraînement
│   ├── test_api.py                 # Tests unitaires pour l'API
│   ├── Dockerfile                  # Dockerfile pour l'API
│   ├── Dockerfile.test             # Dockerfile pour les tests
│   └── models/                     # Dossier pour les modèles entraînés
├── app/
│   ├── streamlit_app.py        # Application Streamlit avec canvas de dessin
│   ├── Dockerfile.streamlit    # Dockerfile pour l'application Streamlit
│   └── requirements.txt          # Dépendances Streamlit
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

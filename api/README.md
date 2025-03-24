# API de Prédiction de Chiffres Manuscrits avec FastAPI

Ce projet contient une API FastAPI qui permet de prédire des chiffres manuscrits à partir d'images, en utilisant un modèle de régression logistique entraîné sur le jeu de données MNIST.

## Prérequis

* Docker (pour construire et exécuter le conteneur)
* Python 3.9 (pour exécuter l'API localement)
* pip (gestionnaire de packages Python)

## Architecture
```
api/
├── ia_models/
│   └── mnist_model.joblib  # Le modèle sauvegardé
├── main.py                 # L'API FastAPI
└── requirements.txt        # Les dépendances Python
```

## Installation

1.  Clonez ce dépôt:

    ```bash
    git clone <URL_du_dépôt>
    cd <nom_du_dépôt>
    ```

2.  (Optionnel) Créez un environnement virtuel Python :

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Sur Linux/macOS
    venv\Scripts\activate  # Sur Windows
    ```

3.  Installez les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

## Exécution

### Avec Docker

1.  Construisez l'image Docker :

    ```bash
    docker build -t mnist-api .
    ```

2.  Exécutez le conteneur Docker :

    ```bash
    docker run -p 8000:8000 mnist-api
    ```

L'API sera disponible à l'adresse `http://localhost:8000`.

### Localement

1.  Exécutez l'API FastAPI :

    ```bash
    uvicorn main:app --reload
    ```

L'API sera disponible à l'adresse `http://127.0.0.1:8000`.

## Points de Terminaison

* **`/predict` (POST)** : Prédit le chiffre manuscrit à partir d'une image.
    * **Entrée** : Image (multipart/form-data)
    * **Sortie** : JSON avec les probabilités et la classe prédite.
* **`/retrain` (POST)** : Entraîne ou réentraîne le modèle MNIST.
    * **Sortie** : Message de confirmation.
* **`/save` (POST)** : Sauvegarde l'image envoyée.
    * **Entrée** : Image (multipart/form-data)
    * **Sortie** : Message de confirmation.

## Utilisation avec Streamlit

Voir les exemples de code dans le fichier `main.py` pour l'intégration avec une application Streamlit.

## Améliorations possibles

* Implémenter des validations d'entrée pour les images.
* Ajouter des tests unitaires.
* Remplacer la régression logistique par un réseau de neurones convolutif pour de meilleures performances.
* Améliorer la gestion des erreurs et la documentation.
 

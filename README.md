# MNIST API avec TensorFlow et FastAPI

Ce projet déploie un modèle de réseau de neurones convolutif (CNN) entraîné sur le dataset MNIST via une API FastAPI. Il inclut également des outils de monitoring avec Prometheus, Grafana et Node Exporter.

## Structure du Projet

```
mnist_api/
├── api/
│   ├── main.py         # Application FastAPI
│   ├── models.py       # Modèles Pydantic
│   ├── cnn5r.py        # Modèles de prédiction
│   ├── cnn_model.py    # Chargement du modèle CNN
│   ├── Dockerfile          # Configuration Docker
│   ├── requirements.txt    # Dépendances Python   
│   └── test/
│       └── test_api.py     # Tests Pytest pour l'API
│
├── prometheus/         # Configuration Prometheus
│   └── prometheus.yml
│
├── grafana/            # Configuration Grafana
│   └── provisioning/
│        ├── datasources/
│        │   └── datasources.yml
│        └── dashboards/
│            └── dashboards.yml
├── docker-compose.yml  # Orchestration Docker Compose  
└── README.md           # Procédure d'installation et documentation
```

## Composants

* **FastAPI :** Framework web Python moderne et rapide pour construire l'API.
* **TensorFlow :** Bibliothèque pour charger et utiliser le modèle CNN.
* **Pydantic :** Bibliothèque pour la validation des données.
* **Prometheus :** Outil de monitoring pour collecter des métriques.
* **Grafana :** Outil de visualisation pour les métriques Prometheus.
* **Node Exporter :** Exporte les métriques de la machine hôte pour Prometheus.
* **Docker Compose :** Outil pour orchestrer et déployer les services.

## Prérequis

* Docker et Docker Compose installés.
* Le modèle CNN entraîné (par exemple, `cnn5r.keras`) dans le dossier `cnn5r.keras` à la racine du projet.

## Installation

1.  Clonez le dépôt.
2.  Assurez-vous que le modèle CNN est présent (e.g., `cnn5r.keras`).
3.  Exécutez `docker-compose up --build` dans le répertoire du projet.

## Utilisation

###   API FastAPI

* L'API est accessible sur `http://localhost:8000`.
* La documentation interactive de l'API est disponible sur `http://localhost:8000/docs` ou `http://localhost:8000/redoc`.

####   Route de Prédiction

* **Endpoint :** `/predict/` (POST)
* **Input :** Un objet JSON avec une clé `"image_data"`. La valeur de `"image_data"` est une liste de listes de listes représentant une image 28x28x1.
* **Output :** Un objet JSON avec `prediction` (la classe prédite) et `confidence` (la confiance de la prédiction).

####   Exemple de requête (Python avec `requests`)

```python
import requests

url = "http://localhost:8000/predict/"
image_data = [[[0.0] for _ in range(28)] for _ in range(28)]
# exemple d'image avec un 1
image_data[10][14] = [1.0]

payload = {"image_data": image_data}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print(f"Prédiction : {data['prediction']}")
    print(f"Confiance : {data['confidence']}")
else:
    print(f"Erreur : {response.status_code}")
    print(response.text)
```

###   Monitoring

* **Prometheus :** Accessible sur `http://localhost:9090`.
* **Grafana :** Accessible sur `http://localhost:3000` (identifiants par défaut : `admin/admin`).

## Tests

Les tests pour l'API sont situés dans `test/test_api.py`. Ils peuvent être exécutés dans un environnement Python avec Pytest installé.

## Notes

* Assurez-vous d'avoir le fichier `cnn5r.keras` dans le dossier `app`.
* Ajustez les configurations des services (ports, volumes, etc.) dans `docker-compose.yml` si nécessaire.


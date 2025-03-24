# Benchmark de Modèles de Machine Learning et Réseaux de Neurones sur MNIST

Ce projet effectue un benchmark de différents modèles de machine learning et de réseaux de neurones sur le dataset MNIST (chiffres manuscrits 28x28).

## Structure du Projet

```
mnist_benchmark/
├── models/
│   ├── logistic_regression.py
│   ├── svc.py
│   ├── catboost_model.py
│   ├── dense_nn.py
│   ├── cnn_3layers.py
│   ├── cnn_5layers.py
│   └── cnn_5layers_regularized.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── results/
```

* `models/` : Contient les implémentations des différents modèles.
* `main.py` : Script principal pour exécuter le benchmark.
* `Dockerfile` : Configuration Docker pour construire l'image du projet.
* `docker-compose.yml` : Configuration Docker Compose pour orchestrer le conteneur.
* `requirements.txt` : Liste des dépendances Python.
* `results/` : Dossier où les résultats du benchmark sont sauvegardés.

## Modèles Implémentés

* Régression Logistique
* Support Vector Classifier (SVC)
* CatBoost
* Réseau de Neurones Dense
* Réseau de Neurones Convolutionnel (CNN) 3 couches
* Réseau de Neurones Convolutionnel (CNN) 5 couches
* Réseau de Neurones Convolutionnel (CNN) 5 couches avec régularisation (dropout)

## Dépendances

Les dépendances Python sont listées dans le fichier `requirements.txt` :

```
numpy
pandas
scikit-learn
tensorflow
catboost
```

Pour installer les dépendances :

```bash
pip install -r requirements.txt
```

## Exécution

### Avec Docker Compose (Recommandé)

1.  Assurez-vous que Docker et Docker Compose sont installés.
2.  Clonez le dépôt et naviguez vers le répertoire du projet.
3.  Exécutez :

```bash
docker-compose up --build
```

Les résultats seront sauvegardés dans le dossier `results/` sous le nom `model_comparison.csv`.

### Sans Docker

1.  Clonez le dépôt et naviguez vers le répertoire du projet.
2.  Installez les dépendances :

```bash
pip install -r requirements.txt
```

3.  Exécutez le script principal :

```bash
python main.py
```

Les résultats seront sauvegardés dans le dossier `results/` sous le nom `model_comparison.csv`.

## Résultats

Le fichier `results/model_comparison.csv` contient un tableau comparatif des performances de chaque modèle, avec les métriques suivantes :

* Accuracy
* Precision
* Recall
* F1-score

## Notes

* Les hyperparamètres des modèles peuvent être ajustés dans les fichiers respectifs du dossier `models/`.
* L'utilisation de Docker Compose est recommandée pour une exécution plus facile et reproductible, surtout si vous utilisez un GPU.



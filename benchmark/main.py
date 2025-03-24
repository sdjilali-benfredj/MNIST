import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from models import logistic_regression, svc, catboost_model, dense_nn, cnn_3layers, cnn_5layers, cnn_5layers_regularized
import time
import pickle
import os

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        result['execution_time'] = execution_time
        return result
    return wrapper

# Chargement du dataset MNIST
mnist = fetch_openml('mnist_784', version=1, cache=True, as_frame=False)
X, y = mnist["data"], mnist["target"].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalisation des données
X_train = X_train / 255.0
X_test = X_test / 255.0

# Dictionnaire pour stocker les résultats
results = {}

# Entraînement et évaluation des modèles
print("Training Logistic Regression...")
results['Logistic Regression'] = timer(logistic_regression.train_and_evaluate)(X_train, y_train, X_test, y_test)
print(f"Logistic Regression done in {results['Logistic Regression']['execution_time']:.2f} seconds.")

print("\nTraining SVC...")
results['SVC'] = timer(svc.train_and_evaluate)(X_train, y_train, X_test, y_test)
print(f"SVC done in {results['SVC']['execution_time']:.2f} seconds.")

print("\nTraining CatBoost...")
results['CatBoost'] = timer(catboost_model.train_and_evaluate)(X_train, y_train, X_test, y_test)
print(f"CatBoost done in {results['CatBoost']['execution_time']:.2f} seconds.")

print("\nTraining Dense NN...")
results['Dense NN'] = timer(dense_nn.train_and_evaluate)(X_train, y_train, X_test, y_test)
print(f"Dense NN done in {results['Dense NN']['execution_time']:.2f} seconds.")

# Reshape pour les CNN
X_train_cnn = X_train.reshape(-1, 28, 28, 1)
X_test_cnn = X_test.reshape(-1, 28, 28, 1)

print("\nTraining CNN 3 Layers...")
results['CNN 3 Layers'] = timer(cnn_3layers.train_and_evaluate)(X_train, y_train, X_test, y_test)
print(f"CNN 3 Layers done in {results['CNN 3 Layers']['execution_time']:.2f} seconds.")

print("\nTraining CNN 5 Layers...")
results['CNN 5 Layers'] = timer(cnn_5layers.train_and_evaluate)(X_train, y_train, X_test, y_test)
print(f"CNN 5 Layers done in {results['CNN 5 Layers']['execution_time']:.2f} seconds.")

print("\nTraining CNN 5 Layers Regularized...")
results['CNN 5 Layers Regularized'] = timer(cnn_5layers_regularized.train_and_evaluate)(X_train, y_train, X_test, y_test)
print(f"CNN 5 Layers Regularized done in {results['CNN 5 Layers Regularized']['execution_time']:.2f} seconds.")


# Création du dataframe et sauvegarde en CSV
df_results = pd.DataFrame(results).T
df_results.to_csv('results/model_comparison.csv')

print(df_results)
print("\nResults saved to results/model_comparison.csv")

# 1000 chiffres pour la prédiction pour calculer le temps moyen
X_predict = X_test[:1000]

# Chargement des modèles et mesure du temps de prédiction
models = {
    "Logistic Regression": pickle.load(os.path.join("models", "logistic_regression.joblib")),
    "SVC": pickle.load(os.path.join("models", "svc.joblib")),
    "CatBoost": pickle.load(os.path.join("models", "catboost.joblib")),
    "Dense NN": tf.keras.models.load_model(os.path.join("models", "dense_nn.h5")),
    "CNN 3 Layers": tf.keras.models.load_model(os.path.join("models", "cnn_3layers.h5")),
    "CNN 5 Layers": tf.keras.models.load_model(os.path.join("models", "cnn_5layers.h5")),
    "CNN 5 Layers Regularized": tf.keras.models.load_model(os.path.join("models", "cnn_5layers_regularized.h5")),
    "Transfer Learning": tf.keras.models.load_model(os.path.join("models", "transfer_learning.h5"))
}

average_prediction_times = []

for model_name, model in models.items():
    start_time = time.time()
    if model_name in ["Dense NN", "CNN 3 Layers", "CNN 5 Layers", "CNN 5 Layers Regularized", "Transfer Learning"]:
      X_predict_resized = X_predict.reshape(-1,28,28,1) if "CNN" in model_name else X_predict
      X_predict_resized = np.stack((X_predict_resized,) * 3, axis=-1) if model_name == "Transfer Learning" else X_predict_resized
      X_predict_resized = tf.image.resize(X_predict_resized, (32, 32)) if model_name == "Transfer Learning" else X_predict_resized
      model.predict(X_predict_resized)
    else:
        model.predict(X_predict)
    end_time = time.time()
    total_time = end_time - start_time
    average_time = total_time / 1000
    average_prediction_times.append({"Model": model_name, "Average Prediction Time": average_time})

# Sauvegarde des résultats
df_average_times = pd.DataFrame(average_prediction_times)
df_average_times.to_csv(os.path.join("results", "average_time_per_model.csv"), index=False)
print("Average prediction times saved to results/average_time_per_model.csv")
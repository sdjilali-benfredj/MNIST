import os
import joblib
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
import numpy as np
from PIL import Image
from tqdm import tqdm
from sklearn.metrics import confusion_matrix

app = FastAPI()

MODEL_PATH = "models/mnist_model.joblib"
IMAGE_SIZE = 28


def load_or_train_model():
    """Charge le modèle pré-entraîné s'il existe, sinon l'entraîne et le sauvegarde."""
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        mnist = fetch_openml("mnist_784", version=1, as_frame=False)
        X, y = mnist["data"], mnist["target"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        model = SGDClassifier(max_iter=1000, tol=1e-4, loss='log_loss', alpha=0.0001)
        batch_size = 100
        n_batches = len(X_train) // batch_size

        for i in tqdm(range(n_batches)):
            start = i * batch_size
            end = start + batch_size
            model.partial_fit(X_train[start:end], y_train[start:end], classes=np.unique(y_train))

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)
    return model

model = load_or_train_model()

@app.post("/predict")
async def predict(file: UploadFile):
    """Prédit le chiffre d'une image."""
    try:
        image = Image.open(file.file).convert("L").resize((IMAGE_SIZE, IMAGE_SIZE))
        image_array = np.array(image).reshape(1, IMAGE_SIZE * IMAGE_SIZE) / 255.0
        probabilities = model.predict_proba(image_array)[0]

        # Remplacer NaN et inf par 0
        probabilities = np.nan_to_num(probabilities, nan=0.0, posinf=0.0, neginf=0.0).tolist()

        predicted_class = int(model.predict(image_array)[0])
        return JSONResponse({"probabilities": probabilities, "predicted_class": predicted_class})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/retrain")
async def retrain():
    """Réentraîne le modèle et renvoie la matrice de confusion."""
    try:
        mnist = fetch_openml("mnist_784", version=1, as_frame=False)
        X, y = mnist["data"], mnist["target"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        model = SGDClassifier(max_iter=1000, tol=1e-4, loss='log_loss', alpha=0.0001)
        batch_size = 100
        n_batches = len(X_train) // batch_size

        for i in tqdm(range(n_batches)):
            start = i * batch_size
            end = start + batch_size
            model.partial_fit(X_train[start:end], y_train[start:end], classes=np.unique(y_train))

        joblib.dump(model, MODEL_PATH)

        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred).tolist()  # Convertir en liste pour JSON
        return JSONResponse({"message": "Modèle réentraîné avec succès", "confusion_matrix": cm})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
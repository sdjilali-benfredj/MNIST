import numpy as np
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Gauge
from models import UserCreate, UserLogin, UserResponse, TokenResponse, ImageInput, PredictionOutput 
from cnn_model import cnn_model
from tensorflow import keras
from fastapi import Response
from PIL import Image
from db import get_db, create_user_db, authenticate_user_db, initialize_db, save_prediction
from typing import Annotated, List  
import sqlite3
from contextlib import asynccontextmanager
import os 

async def lifespan(app: FastAPI):
    print("🔥 Vérification de la base de données...")
    if not os.path.exists("users.db"):  # ⚠️ Vérifie si la BDD n'existe pas
        initialize_db()
        print("✅ Base de données créée !")
    else:
        print("✅ Base de données déjà existante.")
    yield  # Démarrage de l'application

app = FastAPI(lifespan=lifespan)

IMAGE_SIZE = 28

# CORS Middleware (Adjust as needed for your setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_db()

# Metrics setup
prediction_counter = Counter("prediction_count", "Number of predictions made")
model_load_time = Gauge("model_load_time", "Time to load the CNN model")
import time

start_time = time.time()
model = keras.models.load_model('cnn5r.keras')
end_time = time.time()

model_load_time.set(end_time - start_time)

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict/", response_model=PredictionOutput)
async def predict(file: UploadFile, db: Annotated[sqlite3.Connection, Depends(get_db)], user_id: str):
    """
    Predicts the digit in the input image using the loaded CNN model.
    """
    image = Image.open(file.file).convert("L").resize((IMAGE_SIZE, IMAGE_SIZE))
    image = np.array(image).reshape(1, IMAGE_SIZE , IMAGE_SIZE) / 255.0

    predictions = cnn_model.predict(image)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = float(np.max(predictions, axis=1)[0])
    print("="*20)
    print("user id", user_id)
    print("predicted_class", predicted_class)
    print("confidence", confidence)
    print("="*20)
    prediction_counter.inc()
    
    # Sauvegarder le résultat dans la base de données
    save_prediction(db, int(user_id), predicted_class, confidence)
    return PredictionOutput(prediction=int(predicted_class), confidence=confidence)


# Routes d'authentification

@app.post("/register/", response_model=UserResponse)
async def register_user(user: UserCreate, db: Annotated[sqlite3.Connection, Depends(get_db)]):
    return create_user_db(db, user.username, user.email, user.password)


@app.post("/login/", response_model=TokenResponse)
async def authenticate_user(form_data: UserLogin, db: Annotated[sqlite3.Connection, Depends(get_db)]):
    return authenticate_user_db(db, form_data.username, form_data.password)

@app.get("/results/")
def get_results(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    
    # Récupérer les résultats liés à cet utilisateur
    cursor.execute("""
        SELECT r.prediction, r.confidence 
        FROM resultats r
        JOIN user_resultats ur ON r.id = ur.resultat_id
        WHERE ur.user_id = ?
    """, (user_id,))
    
    results = cursor.fetchall()
    
    # Transformer en liste de dictionnaires
    return [{"prediction": row["prediction"], "confidence": row["confidence"]} for row in results]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
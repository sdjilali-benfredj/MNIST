import os
import sys

sys.path.insert(0,
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        ".."
                    )
                ))

import os
import sys
import sqlite3
import pytest
import numpy as np
from fastapi.testclient import TestClient
from main import app
from db import get_db, initialize_db

from PIL import Image
# Utiliser une base de données temporaire pour les tests
DB_PATH = "/api/data/test_users.db"

# Remplace la dépendance de la BDD par la BDD de test
def get_test_db():
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)


### 🔹 TESTS DE PREDICTION 🔹 ###

def test_prediction():
    """Test d'envoi d'une image pour une prédiction."""

    # Créer une image 28x28 avec un fond noir
    image = np.zeros((28, 28), dtype=np.uint8)
    
    # Dessiner un "1" en blanc (valeur 255)
    image[5:23, 13:15] = 255  # Trait vertical
    image[4:7, 10:16] = 255    # Barre supérieure
    
    # Sauvegarder l'image
    img = Image.fromarray(image, mode="L")
    img.save('test_image.png')
    print(f"Image sauvegardée sous {'test_image.png'}")

    user_id = 1
    with open("test_image.png", "rb") as img:
        response = client.post("/predict_test/", params={"user_id": user_id}, files={"file": img})
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert isinstance(data["prediction"], int)
    assert isinstance(data["confidence"], float)


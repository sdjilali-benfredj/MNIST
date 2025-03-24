from fastapi.testclient import TestClient
import os
from main import app, MODEL_PATH
from io import BytesIO
from PIL import Image
import numpy as np
from sklearn.datasets import fetch_openml

client = TestClient(app)

IMAGE_SIZE = 28

def get_mnist_image():
    """Récupère une image MNIST du jeu de données."""
    mnist = fetch_openml("mnist_784", version=1, as_frame=False)
    image_array = mnist.data[0].reshape(IMAGE_SIZE, IMAGE_SIZE)  # Récupérer la première image
    image = Image.fromarray(image_array.astype(np.uint8), 'L')

    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)
    return image_bytes

def create_bad_image():
    """Crée un fichier qui n'est pas une image."""
    with open('bad_image', 'w') as f:
        f.write("Not an image")
    return open('bad_image', 'rb')

def check_model_exists():
    """Vérifie si le modèle existe."""
    return os.path.exists(MODEL_PATH)

def delete_model():
    """Supprime le modèle s'il existe."""
    if os.path.exists(MODEL_PATH):
        os.remove(MODEL_PATH)

def test_predict_with_model():
    """Teste la prédiction avec un modèle entraîné."""
    #delete_model() #On ne supprime plus le modèle
    response = client.post("/retrain")
    assert response.status_code == 200

    image = get_mnist_image()
    files = {"file": ("test.png", image, "image/png")}
    response = client.post("/predict", files=files)

    if response.status_code != 200:
        print(f"Erreur 400 : {response.json()}")
    assert response.status_code == 200
    assert "probabilities" in response.json()
    assert "predicted_class" in response.json()
    assert len(response.json()["probabilities"]) == 10  # 10 classes pour MNIST
    assert isinstance(response.json()["predicted_class"], int)

def test_predict_invalid_image():
    """Teste la prédiction avec une image invalide."""
    #delete_model() #On ne supprime plus le modèle
    response = client.post("/retrain")
    assert response.status_code == 200

    image = create_bad_image()
    files = {"file": ("test.png", image, "image/png")}
    response = client.post("/predict", files=files)
    assert response.status_code == 400

def test_retrain_only_if_no_model():
  """Teste le réentraînement du modèle uniquement s'il n'existe pas."""
  delete_model() #On supprime le modèle seulement ici.
  response = client.post("/retrain")
  assert response.status_code == 200

  # Essaie de réentraîner à nouveau, cela ne devrait pas avoir d'effet car le modèle existe déjà
  response2 = client.post("/retrain")
  assert response2.status_code == 200
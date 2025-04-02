import os
import sys 
sys.path.insert(0,
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        ".."
                    )
                ))

import pytest
import requests
import numpy as np
from PIL import Image
import io
import requests_mock
import streamlit.testing.v1 as st_test
import streamlit as st
from streamlit_app import *

@pytest.fixture
def mock_api():
    """Simule les réponses de l'API FastAPI avec requests-mock."""
    with requests_mock.Mocker() as m:
        yield m

def test_register(mock_api):
    """Test de la création d'un compte utilisateur."""
    mock_api.post("http://fastapi:8000/register/", json={"username": "testuser", "email": "test@example.com"})
    
    app = st_test.App()
    app.text_input("Nouveau nom d'utilisateur").set_value("testuser")
    app.text_input("Email").set_value("test@example.com")
    app.text_input("Nouveau mot de passe").set_value("password123")
    app.button("Créer un compte").click()
    
    assert "Compte créé!" in app.text

def test_login(mock_api):
    """Test de connexion utilisateur avec succès."""
    mock_api.post("http://fastapi:8000/login/", json={"access_token": "fake_token", "user_id": 1})
    
    app = st_test.App()
    app.text_input("Nom d'utilisateur").set_value("testuser")
    app.text_input("Mot de passe").set_value("password123")
    app.button("Se connecter").click()
    
    assert "Connexion réussie!" in app.text
    assert st.session_state.token == "fake_token"

def test_prediction(mock_api):
    """Test de prédiction avec une image MNIST simulée."""
    mock_api.post("http://fastapi:8000/predict/?user_id=1", json={"prediction": 7, "confidence": 0.98})
    
    # Création d'une image MNIST factice (chiffre "1")
    img = Image.new("L", (28, 28), color=255)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    app = st_test.App()
    app.button("Prédire").click()
    
    assert "Prédiction : 7" in app.text
    assert "Probabilités : 0.98" in app.text

def test_logout():
    """Test de déconnexion."""
    st.session_state.token = "fake_token"
    app = st_test.App()
    app.sidebar.button("Déconnexion 🔒").click()
    
    assert st.session_state.token is None
    assert "Déconnecté avec succès." in app.text

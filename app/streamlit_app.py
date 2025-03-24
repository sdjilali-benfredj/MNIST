import streamlit as st
from streamlit_drawable_canvas import st_canvas
import requests
from PIL import Image
import numpy as np
import io
import pandas as pd

# Configuration de l'application
st.title("Prédiction de chiffres manuscrits avec MNIST")

# Création du canvas de dessin
stroke_width = st.slider("Largeur du trait :", 1, 25, 12)
stroke_color = st.color_picker("Couleur du trait :", "#FFFFFF")
bg_color = st.color_picker("Couleur de fond :", "#000000")
bg_image = None
drawing_mode = "freedraw"

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=bg_image,
    update_streamlit=True,
    height=250,
    width=250,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Bouton de prédiction
if st.button("Prédire"):
    if canvas_result.image_data is not None:
        # Préparation de l'image pour l'API
        img = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")
        img = img.convert("L")  # Conversion en niveaux de gris
        img = img.resize((28, 28))  # Redimensionnement pour MNIST
        img_array = np.array(img)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        # Appel à l'API FastAPI
        files = {"file": ("canvas.png", img_bytes, "image/png")}
        response = requests.post("http://api:8000/predict", files=files)  # Assurez-vous que l'URL correspond à votre API
        if response.status_code == 200:
            result = response.json()
            st.write("Prédiction :", result["predicted_class"])
            st.write("Probabilités :", result["probabilities"])
        else:
            st.error("Erreur lors de la prédiction.")
    else:
        st.warning("Veuillez dessiner un chiffre.")

# Bouton d'entraînement
if st.button("Entraîner le modèle et afficher la matrice de confusion"):
    response = requests.post("http://api:8000/retrain")
    if response.status_code == 200:
        result = response.json()
        st.success(result["message"])
        st.subheader("Matrice de confusion:")
        df_cm = pd.DataFrame(result["confusion_matrix"])
        st.dataframe(df_cm) #afficher sous forme de dataframe
    else:
        st.error("Erreur lors du réentraînement du modèle.")
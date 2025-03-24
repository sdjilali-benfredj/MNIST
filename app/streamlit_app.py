import streamlit as st
from streamlit_drawable_canvas import st_canvas
import requests
from PIL import Image
import numpy as np
import io
import pandas as pd
from loguru import logger
from db import create_user, login_user 

logger.add("main_logs.log")

if "token" not in st.session_state.keys():
    st.session_state.token = None
    logger.info("Token initiated")

# Configuration de l'application
st.title("Prédiction de chiffres manuscrits avec MNIST")



# login form if not already logged in 
if st.session_state.token is None:
    st.subheader("Connexion")
    username_login = st.text_input("Nom d'utilisateur")
    password_login = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if login_user(username_login, password_login):
            st.session_state.token = username_login
            logger.info(f"Token assigned for {username_login}")
            st.success("Connexion réussie !")
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

    st.subheader("Créer un compte")
    username_new = st.text_input("Nouveau nom d'utilisateur")
    email_new = st.text_input("Email")
    password_new = st.text_input("Nouveau mot de passe", type="password")

    if st.button("Créer un compte"): 
        if create_user(username_new, email_new, password_new):
            st.success("Compte créé ! Vous pouvez vous connecter.")
            logger.info(f"Nouvel utilisateur créé : {username_new}")
        else:
            st.error("Nom d'utilisateur ou email déjà utilisé.")


else:
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
            response = requests.post("http://fastapi:8000/predict", files=files)  # Assurez-vous que l'URL correspond à votre API
            if response.status_code == 200:
                result = response.json()
                st.write("Prédiction :", result["prediction"])
                st.write("Probabilités :", result["confidence"])
            else:
                st.error("Erreur lors de la prédiction.")
        else:
            st.warning("Veuillez dessiner un chiffre.")

    if st.sidebar.button("Déconnexion 🔒"):
        st.session_state.token = None
        st.success("Déconnecté avec succès.")
        logger.info("Utilisateur déconnecté")
        st.rerun()
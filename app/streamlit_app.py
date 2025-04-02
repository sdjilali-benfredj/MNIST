import streamlit as st
import requests
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import io
from loguru import logger

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
        login_data = {"username": username_login, "password": password_login}
        response = requests.post("http://fastapi:8000/login/", json=login_data)

        if response.status_code == 200:
            result = response.json()    
            st.session_state.token = result["access_token"]  # Stocker le token
            st.session_state.user_id = result["user_id"]  # Stocker l'id            
            st.success("Connexion réussie!")
            st.rerun()
        else:
            try:
                error_message = response.json()["detail"]
            except (ValueError, KeyError):
                error_message = "Erreur lors de la connexion."
            st.error(error_message)


    st.subheader("Créer un compte")
    username_new = st.text_input("Nouveau nom d'utilisateur")
    email_new = st.text_input("Email")
    password_new = st.text_input("Nouveau mot de passe", type="password")

    if st.button("Créer un compte"):
        register_data = {"username": username_new, "email": email_new, "password": password_new}
        response = requests.post("http://fastapi:8000/register/", json=register_data)
        if response.status_code == 200:
            st.success("Compte créé! Vous pouvez vous connecter.")
            logger.info(f"Nouvel utilisateur créé : {username_new}")
        else:
            try:
                error_message = response.json()["detail"]
            except (ValueError, KeyError):
                error_message = "Erreur lors de la création du compte."
            st.error(error_message)

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
            # Vérification si tous les pixels sont identiques
            img_data = canvas_result.image_data.astype("uint8")
            if np.all(img_data == img_data[0, 0, :]):
                st.error("Veuillez faire un dessin, l'image est vide ou uniforme.")
            else:            
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
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                files = {"file": ("canvas.png", img_bytes, "image/png")}
                response = requests.post(f"http://fastapi:8000/predict/?user_id={st.session_state.user_id}", files=files, headers=headers)

                if response.status_code == 200:
                    result = response.json()
                    st.write("Prédiction :", result["prediction"])
                    st.write("Probabilités :", result["confidence"])
                else:
                    st.error("Erreur lors de la prédiction.")
                    try:
                        error_message = response.json()["detail"]
                    except (ValueError, KeyError):
                        error_message = "Erreur lors de la prédiction."
                    st.error(error_message)
        else:
            st.warning("Veuillez dessiner un chiffre.")

    if st.sidebar.button("Déconnexion 🔒"):
        st.session_state.token = None
        st.success("Déconnecté avec succès.")
        logger.info("Utilisateur déconnecté")
        st.rerun()
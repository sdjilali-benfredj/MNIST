# app.py
import streamlit as st
import sqlite3
import bcrypt
import requests
import base64
import datetime
from streamlit_drawable_canvas import st_canvas

# Configuration de la base de données
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Utilisateur (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identifiant TEXT UNIQUE NOT NULL,
                    mot_de_passe_hash TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Historique (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    utilisateur_id INTEGER,
                    chiffre TEXT,
                    resultat_ia INTEGER,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(utilisateur_id) REFERENCES Utilisateur(id))''')
    conn.commit()
    conn.close()

# Exécuter l'initialisation au démarrage
init_db()

# Fonction d'inscription
def register_user(identifiant, mot_de_passe):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    hashed_pw = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO Utilisateur (identifiant, mot_de_passe_hash) VALUES (?, ?)", (identifiant, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

# Fonction de connexion
def login_user(identifiant, mot_de_passe):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, mot_de_passe_hash FROM Utilisateur WHERE identifiant = ?", (identifiant,))
    user = c.fetchone()
    conn.close()
    if user and bcrypt.checkpw(mot_de_passe.encode(), user[1]):
        return user[0]
    return None

# Fonction d'appel à l'API externe
def call_api(image_data):
    try:
        response = requests.post("https://api.example.com/mnist", json={"image": image_data})
        response.raise_for_status()
        return response.json().get("resultat")
    except requests.RequestException:
        return None

# Interface utilisateur
st.title("Reconnaissance de chiffres manuscrits")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""

if not st.session_state.logged_in:
    choix = st.sidebar.radio("Navigation", ["Connexion", "Inscription"])
    if choix == "Inscription":
        identifiant = st.text_input("Identifiant")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        if st.button("S'inscrire"):
            if register_user(identifiant, mot_de_passe):
                st.success("Inscription réussie, veuillez vous connecter.")
            else:
                st.error("L'identifiant existe déjà.")
    else:
        identifiant = st.text_input("Identifiant")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            user_id = login_user(identifiant, mot_de_passe)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = identifiant
            else:
                st.error("Identifiants incorrects.")
else:
    st.sidebar.write(f"Connecté en tant que {st.session_state.username}")
    if st.sidebar.button("Se déconnecter"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.rerun()
    
    canvas = st_canvas(width=280, height=280, stroke_width=10, stroke_color="white", background_color="black")
    if st.button("Valider") and canvas.image_data is not None:
        image_data = base64.b64encode(canvas.image_data.tobytes()).decode()
        result = call_api(image_data)
        if result is not None:
            st.write(f"Chiffre reconnu : {result}")
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("INSERT INTO Historique (utilisateur_id, chiffre, resultat_ia) VALUES (?, ?, ?)", (st.session_state.user_id, image_data, result))
            conn.commit()
            conn.close()
        else:
            st.error("Erreur lors de l'appel à l'API.")
    
    st.subheader("Historique des soumissions")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT resultat_ia, date FROM Historique WHERE utilisateur_id = ? ORDER BY date DESC", (st.session_state.user_id,))
    history = c.fetchall()
    conn.close()
    for item in history:
        st.write(f"{item[1]} : {item[0]}")

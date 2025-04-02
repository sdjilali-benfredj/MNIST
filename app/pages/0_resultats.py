import streamlit as st
import requests
import sqlite3


# Vérifier si l'utilisateur est connecté
if "user_id" not in st.session_state:
    st.error("Veuillez vous connecter pour accéder aux prédictions.")
    st.stop()
else:

    st.header("Mes Résultats")
    
    # Requête API pour récupérer les prédictions
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"http://fastapi:8000/results/?user_id={st.session_state.user_id}", headers=headers)

    if response.status_code == 200:
        results = response.json()
        if results:
            for res in results:
                st.write(f"📌 **Prédiction** : {res['prediction']} (🔍 Confiance : {res['confidence']:.2f})")
        else:
            st.info("Aucune prédiction enregistrée.")
    else:
        st.error("Impossible de récupérer les résultats.")

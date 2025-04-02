import sqlite3
import bcrypt
from fastapi import HTTPException
import os
from fastapi.responses import JSONResponse

DB_PATH = "/api/data/users.db"  # Nouvelle localisation pour SQLite

def get_db():
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()

def initialize_db():
    if os.path.exists(DB_PATH):
        print("✅ La base de données existe déjà.")
        return
    print("🔥 Création de la base de données...")
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Table des prédictions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction INTEGER NOT NULL,
            confidence REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table de liaison entre users et resultats
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_resultats (
            user_id INTEGER,
            resultat_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (resultat_id) REFERENCES resultats(id)
        )
    """)
    db.commit()
    db.close()
    print("✅ Base de données initialisée")

def save_prediction(db: sqlite3.Connection, user_id: int, prediction: int, confidence: float):
    cursor = db.cursor()
    
    # Insérer le résultat dans la table resultats
    cursor.execute("INSERT INTO resultats (prediction, confidence) VALUES (?, ?)", 
                   (int(prediction), float(confidence)))
    resultat_id = cursor.lastrowid  # Récupérer l'ID du résultat inséré

    # Associer l'utilisateur et la prédiction
    cursor.execute("INSERT INTO user_resultats (user_id, resultat_id) VALUES (?, ?)", 
                   (user_id, resultat_id))
    
    db.commit()


# Fonctions d'interaction avec la base de données
def create_user_db(db: sqlite3.Connection, username: str, email: str, password: str):
    cursor = db.cursor()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, hashed.decode('utf-8')))
        db.commit()
        return {"username": username, "email": email}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")




def authenticate_user_db(db: sqlite3.Connection, username: str, password: str):
    cursor = db.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        stored_hashed = result["password"].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed):
            # En production, utilisez une vraie génération de JWT (JSON Web Tokens)
            access_token = "some_secure_token"  # Placeholder!  Replace with real JWT
            print("="*20)
            print(int(result[0]))
            print("="*20)
            response_data = {"user_id": int(result[0])}#, "access_token": access_token, "token_type": "bearer"}
            print("Response:", response_data)
            print("="*20)            
            # return response_data
            return JSONResponse(content={"user_id": int(result[0]), "access_token": access_token, "token_type": "bearer"})
        else:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


if __name__ == "__main__":
    initialize_db()
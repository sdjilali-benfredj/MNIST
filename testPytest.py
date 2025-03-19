import pytest
import sqlite3
import bcrypt
from app import register_user, login_user, init_db

@pytest.fixture(scope="function")
def setup_database():
    """Initialise une base de données de test."""
    conn = sqlite3.connect("test_database.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Utilisateur")
    c.execute("DROP TABLE IF EXISTS Historique")
    c.execute('''CREATE TABLE Utilisateur (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identifiant TEXT UNIQUE NOT NULL,
                    mot_de_passe_hash TEXT NOT NULL)''')
    c.execute('''CREATE TABLE Historique (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    utilisateur_id INTEGER,
                    chiffre TEXT,
                    resultat_ia INTEGER,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(utilisateur_id) REFERENCES Utilisateur(id))''')
    conn.commit()
    conn.close()
    yield
    conn = sqlite3.connect("test_database.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Utilisateur")
    c.execute("DROP TABLE IF EXISTS Historique")
    conn.commit()
    conn.close()


def test_register_user(setup_database):
    """Test de l'inscription d'un utilisateur."""
    assert register_user("testuser", "password123") == True
    assert register_user("testuser", "password123") == False  # Doit échouer car l'utilisateur existe déjà


def test_login_user(setup_database):
    """Test de la connexion d'un utilisateur."""
    register_user("testuser", "password123")
    user_id = login_user("testuser", "password123")
    assert user_id is not None  # L'utilisateur doit être trouvé

    wrong_user = login_user("testuser", "wrongpassword")
    assert wrong_user is None  # Mauvais mot de passe, connexion doit échouer

    non_existent_user = login_user("nouveau", "password")
    assert non_existent_user is None  # Utilisateur inexistant
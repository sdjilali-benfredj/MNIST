import sqlite3
import bcrypt

# Connexion à SQLite
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Création table users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# Création d'utilisateur avec hashage
def create_user(username, email, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, hashed.decode('utf-8')))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Utilisateur déjà existant

# Vérification login
def login_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        stored_hashed = result[0].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed)
    return False

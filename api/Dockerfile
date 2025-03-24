# Utilise une image de base Python
FROM python:3.9-slim-buster

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source de l'API
COPY . .

# Expose le port sur lequel l'API FastAPI s'exécute
EXPOSE 8000

# Commande pour exécuter l'API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
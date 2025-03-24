# Utilisation de l'image Python officielle comme image de base
FROM python:3.9-slim

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copie des fichiers requirements.txt et installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste des fichiers de l'application
COPY . .

# Définition de la commande à exécuter lors du lancement du conteneur
CMD ["python", "main.py"]
# Utiliser une image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . /app

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir flask notion_client ics pytz python-dotenv

# Exposer le port 8080
EXPOSE 8080

# Définir la commande pour démarrer le serveur Flask
CMD ["python", "Notion_To_Ical_Server.py"]

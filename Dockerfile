# Image Python officielle
FROM python:3.10-slim

# Empêcher Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .
# ton port interne
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]

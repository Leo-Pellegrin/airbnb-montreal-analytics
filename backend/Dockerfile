# Étape 1 : builder
FROM python:3.12-slim AS builder

# Variables d’environnement pour pip et cache
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Crée un dossier pour l’app et installe les dépendances
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY backend/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# Étape 2 : image finale
FROM python:3.12-slim

# Copy de pip-installed packages
COPY --from=builder /install /usr/local

WORKDIR /app
# Copies ton code backend dans l’image
COPY backend/ ./

# Crée un user non-root
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Expose le port (celui sur lequel Uvicorn écoute)
EXPOSE 8000

# Définition de la commande de démarrage
# On se sert de uvicorn pour lancer l’app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
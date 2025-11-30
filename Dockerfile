# 1. On part d'une version légère et stable de Python (Linux)
FROM python:3.9-slim

# 2. INSTALLATION SYSTÈME (Moteur Audio & Build Tools)
# Ceci installe FluidSynth et toutes les dépendances de compilation pour les libs scientifiques (Scipy, Librosa, Numba, etc.)
RUN apt-get update && apt-get install -y \
    fluidsynth \
    build-essential \
    libsndfile1 \
    libsamplerate0-dev \
    libffi-dev \
    libtool \
    && rm -rf /var/lib/apt/lists/*

# 3. Dossier de travail
WORKDIR /app

# 4. GESTION DES DÉPENDANCES PYTHON
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. COPIE DU PROJET
COPY . .

# 6. COMMANDE DE DÉMARRAGE (Streamlit sur le port $PORT)
CMD sh -c "streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0"
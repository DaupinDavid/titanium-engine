# 1. On part d'une version légère et stable de Python (Linux)
FROM python:3.9-slim

# 2. INSTALLATION SYSTÈME (Moteur Audio)
# C'est ici qu'on installe FluidSynth et les outils audio pour Linux
# "build-essential" sert à compiler certaines libs mathématiques si besoin
RUN apt-get update && apt-get install -y \
    fluidsynth \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 3. On définit le dossier de travail dans le conteneur
WORKDIR /app

# 4. GESTION DES DÉPENDANCES PYTHON
# On copie d'abord le fichier requirements pour profiter du cache Docker
COPY requirements.txt .
# On installe les librairies
RUN pip install --no-cache-dir -r requirements.txt

# 5. COPIE DU PROJET
# On met tout ton code (main.py, assets, modules...) dans le conteneur
COPY . .

# 6. DÉMARRAGE (CRITIQUE POUR RENDER)
# On utilise "sh -c" pour que la variable $PORT de Render soit bien lue
# On force l'adresse 0.0.0.0 pour être accessible de l'extérieur
CMD sh -c "streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0"
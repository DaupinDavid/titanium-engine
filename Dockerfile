# 1. On part d'une version légère de Python (Linux)
FROM python:3.9-slim

# 2. On installe les outils système (Le moteur audio Linux)
# C'est l'équivalent de ton "téléchargement zip" sur Windows
RUN apt-get update && apt-get install -y \
    fluidsynth \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 3. On prépare le dossier de travail
WORKDIR /app

# 4. On copie et installe les librairies Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. On copie tout ton code dans le conteneur
COPY . .

# 6. COMMANDE DE DÉMARRAGE
# C'est ce qui se lance quand le serveur s'allume
CMD streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0
# Utiliser une image de base
FROM nvcr.io/nvidia/pytorch:24.05-py3


COPY requirement.txt .

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    libffi-dev \
    libssl-dev \
    git \
    espeak \
    && apt-get clean

# Installer les dépendances
RUN pip install -r requirement.txt 
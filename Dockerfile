# L'image du serveur du jeu.
#
# Construction explicite, jamais devinée : le fichier dit ce qu'il installe et
# comment il démarre. C'est aussi ce qui permet de lire, dans un an, pourquoi
# l'image est ce qu'elle est.

FROM python:3.12-slim

WORKDIR /app

# Les dépendances AVANT le code : tant que requirements.txt ne bouge pas, cette
# couche est réutilisée telle quelle et la construction ne réinstalle rien.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# L'écoute. `0.0.0.0` est indispensable EN CONTENEUR : sur le `127.0.0.1` par
# défaut du code, le serveur ne serait joignable que depuis l'intérieur de
# l'image — il démarrerait, les journaux seraient propres, et l'adresse ne
# répondrait pas. Le défaut du code, lui, reste le bon pour qui joue chez lui.
ENV HOTE=0.0.0.0
ENV PORT=8000
EXPOSE 8000

# ⚠️ Sans ceci, le journal du conteneur est VIDE — mesuré. Hors terminal, Python
# met sa sortie en tampon, et les deux seules lignes que le serveur imprime (dont
# « Sombreval écoute sur 0.0.0.0:8000 ») n'atteignent jamais `docker logs`. Or
# uvicorn est en `log_level="warning"` : il n'y a pas d'autre signal. On se
# retrouverait à diagnostiquer « l'adresse ne répond pas » sans une ligne pour
# dire sur quoi le serveur écoute vraiment.
ENV PYTHONUNBUFFERED=1

# `python -m jeu.serveur`, et NON `uvicorn jeu.serveur:app` : l'application
# démarre en production par le MÊME chemin qu'en local. Un démarrage qui
# diffère entre les deux est une divergence qui finit par coûter une soirée.
CMD ["python", "-m", "jeu.serveur"]

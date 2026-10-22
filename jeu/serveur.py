"""Le guichet : il reçoit les demandes du navigateur et rend des écrans.

Lancement, depuis la racine du dépôt :

    python3 -m jeu.serveur

Puis ouvrir http://localhost:8000.

Les variables `HOTE` et `PORT` permettent de changer l'écoute sans toucher au
code : elles servent en conteneur, où il faut écouter `0.0.0.0`. Sans elles,
rien ne change pour qui lance le jeu chez lui.

Ce fichier ne contient aucune règle du jeu. Il traduit une demande HTTP en
un appel à jeu/application.py, et une erreur de jeu en message lisible.
C'est voulu : tout le jeu se teste sans serveur.
"""

import os
import pathlib

try:
    import uvicorn
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
except ModuleNotFoundError as manque:
    raise SystemExit(
        f"Il manque une bibliothèque ({manque.name}).\n"
        "\n"
        "Si c'est la première fois, installe-les dans un dossier .venv :\n"
        "    python3 -m venv .venv\n"
        "    .venv/bin/pip install -r requirements.txt\n"
        "\n"
        "Si c'est déjà fait, c'est que ce terminal ne s'en sert pas encore :\n"
        "    source .venv/bin/activate\n"
        "    python3 -m jeu.serveur"
    )

from jeu.application import Application
from jeu.erreurs import ErreurDeJeu

DOSSIER_SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

# Les deux réglages d'écoute, et leurs valeurs par DÉFAUT — celles de qui lance
# le jeu sur son ordinateur. `127.0.0.1` est le bon réglage en local : le
# serveur n'est alors joignable que depuis la machine, et c'est voulu.
#
# En conteneur, l'environnement fournit `HOTE=0.0.0.0` : sans quoi personne ne
# peut atteindre le serveur de l'extérieur, et c'est la panne silencieuse
# classique — le conteneur tourne, les journaux sont propres, l'adresse ne
# répond pas. Les deux réglages COEXISTENT, aucun ne remplace l'autre.
HOTE = "127.0.0.1"
PORT = 8000

app = FastAPI(title="Sombreval")
application = Application()


class Arrivee(BaseModel):
    pseudo: str
    univers: str = ""


class Demande(BaseModel):
    jeton: str


class Action(BaseModel):
    jeton: str
    action: str
    valeur: object


@app.exception_handler(ErreurDeJeu)
def repondre_une_erreur_de_jeu(requete, erreur):
    """Une erreur prévue devient un message pour le joueur, pas un plantage."""
    return JSONResponse(status_code=400, content={"erreur": str(erreur)})


@app.get("/api/univers")
def univers():
    return application.univers_proposes()


@app.post("/api/parties")
def creer_une_partie(arrivee: Arrivee):
    return application.creer_une_partie(arrivee.pseudo, arrivee.univers)


@app.post("/api/parties/{identifiant}/joueurs")
def rejoindre(identifiant: str, arrivee: Arrivee):
    return application.rejoindre(identifiant, arrivee.pseudo)


@app.post("/api/parties/{identifiant}/commencer")
def commencer(identifiant: str, demande: Demande):
    return application.commencer(identifiant, demande.jeton)


@app.get("/api/parties/{identifiant}/vue")
def vue(identifiant: str, jeton: str):
    return application.vue(identifiant, jeton)


@app.post("/api/parties/{identifiant}/actions")
def agir(identifiant: str, action: Action):
    return application.agir(identifiant, action.jeton, action.action, action.valeur)


@app.get("/sante")
def sante():
    """Le signe de vie, pour la sonde de l'hébergeur.

    Une ligne, aucune information, aucun secret : elle répond « ok » si le
    processus répond. Sans elle, l'hébergeur ne sait pas si le conteneur est
    vivant et peut l'écarter du proxy SANS UN MOT — l'adresse ne répond plus
    alors que tout va bien à l'intérieur.

    Elle doit être déclarée AVANT le montage statique ci-dessous, qui prend
    tout ce qui reste : déclarée après, elle serait avalée par lui.
    """
    return {"etat": "ok"}


# Les écrans (HTML, CSS, JavaScript) sont servis à la racine. Cette ligne
# doit rester la dernière : ce qui commence par /api, et /sante, sont déjà pris.
app.mount("/", StaticFiles(directory=DOSSIER_SITE, html=True), name="site")


def lancer(hote=None, port=None):
    """Démarre le serveur. Sans argument ni variable d'environnement : en local.

    L'ordre est : l'argument, puis l'environnement, puis le défaut. Un appelant
    qui passe une valeur commande ; sinon l'environnement décide ; sinon on est
    sur l'ordinateur de quelqu'un, et c'est `127.0.0.1`.
    """
    hote = hote or os.environ.get("HOTE") or HOTE
    port = int(port or os.environ.get("PORT") or PORT)

    # On annonce l'hôte RÉEL, pas « localhost » : en conteneur, ce mot est faux
    # et envoie chercher la panne au mauvais endroit.
    print(f"Sombreval écoute sur {hote}:{port}")
    print("Pour arrêter : Ctrl-C")
    uvicorn.run(app, host=hote, port=port, log_level="warning")


if __name__ == "__main__":
    lancer()

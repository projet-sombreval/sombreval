"""Le guichet : il reçoit les demandes du navigateur et rend des écrans.

Lancement, depuis la racine du dépôt :

    python3 -m jeu.serveur

Puis ouvrir http://localhost:8000.

Ce fichier ne contient aucune règle du jeu. Il traduit une demande HTTP en
un appel à jeu/application.py, et une erreur de jeu en message lisible.
C'est voulu : tout le jeu se teste sans serveur.
"""

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


# Les écrans (HTML, CSS, JavaScript) sont servis à la racine. Cette ligne
# doit rester la dernière : ce qui commence par /api est déjà pris.
app.mount("/", StaticFiles(directory=DOSSIER_SITE, html=True), name="site")


def lancer(port=PORT):
    print(f"Sombreval tourne sur http://localhost:{port}")
    print("Pour arrêter : Ctrl-C")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")


if __name__ == "__main__":
    lancer()

"""Le serveur local : il sert les écrans du dossier site/ dans le navigateur.

Lancement, depuis la racine du dépôt :

    python3 -m jeu.serveur

Puis ouvrir http://localhost:8000 dans un navigateur.

On utilise http.server, qui vient avec Python : rien à installer, ni sur ta
machine ni sur le serveur du lycée.
"""

import http.server
import pathlib

PORT = 8000

# Le dossier site/ est le voisin du dossier jeu/. On calcule son chemin à
# partir de celui de ce fichier, pour que le serveur démarre depuis n'importe
# quel dossier.
DOSSIER_SITE = pathlib.Path(__file__).resolve().parent.parent / "site"


def lancer(port=PORT):
    """Démarre le serveur et ne rend la main qu'au Ctrl-C."""
    adresse = ("", port)
    gestionnaire = _gestionnaire_du_site()

    with http.server.ThreadingHTTPServer(adresse, gestionnaire) as serveur:
        print(f"Sombreval tourne sur http://localhost:{port}")
        print("Pour arrêter : Ctrl-C")
        try:
            serveur.serve_forever()
        except KeyboardInterrupt:
            print("\nServeur arrêté.")


def _gestionnaire_du_site():
    """Construit le gestionnaire qui sert les fichiers du dossier site/."""

    class GestionnaireDuSite(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DOSSIER_SITE), **kwargs)

    return GestionnaireDuSite


if __name__ == "__main__":
    lancer()

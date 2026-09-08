"""Le jeu, sans le web.

Ce module est le jeu complet : créer une partie, la rejoindre, la
commencer, demander son écran, jouer. Il ne connaît ni HTTP, ni FastAPI, ni
navigateur — on peut le faire tourner entièrement depuis les tests.

jeu/serveur.py n'est qu'un guichet posé par-dessus.
"""

import random
import secrets
import time

from jeu import automates, jour, phases, pouvoirs, vues
from jeu.configuration import Configuration
from jeu.erreurs import ErreurDeJeu
from jeu.partie import Partie, ajouter_un_joueur


class Application:

    def __init__(self, configuration=None, hasard=None):
        self.configuration = configuration or Configuration()
        self.hasard = hasard or random.Random()
        self.parties = {}

    def maintenant(self):
        """L'heure qu'il est. Les tests remplacent cette méthode."""
        return time.time()

    # --- avant la partie ---------------------------------------------------

    def univers_proposes(self):
        """Les trois univers, dans l'ordre, avec ceux qui ne sont pas prêts."""
        return [
            {
                "nom": univers["nom"],
                "titre": univers["titre"],
                "annee": univers["annee"],
                "sous_titre": univers["sous_titre"],
                "disponible": bool(univers.get("disponible")),
                # Les couleurs servent dès l'écran d'accueil : aucune n'est
                # écrite dans la feuille de style.
                "couleurs": univers.get("couleurs", {}),
            }
            for univers in sorted(
                self.configuration.univers.values(),
                key=lambda u: not u.get("disponible"),
            )
        ]

    def creer_une_partie(self, pseudo, nom_univers):
        univers = self.configuration.univers_choisi(nom_univers)
        identifiant = secrets.token_urlsafe(6)

        partie = Partie(identifiant, univers, self.configuration, self.hasard)
        partie.derniere_arrivee = self.maintenant()
        joueur = ajouter_un_joueur(partie, pseudo)
        self.parties[identifiant] = partie

        return {"partie": identifiant, "jeton": joueur.jeton}

    def rejoindre(self, identifiant, pseudo):
        partie = self._partie(identifiant)
        joueur = ajouter_un_joueur(partie, pseudo)
        return {"partie": identifiant, "jeton": joueur.jeton}

    def commencer(self, identifiant, jeton):
        partie = self._partie(identifiant)
        joueur = partie.joueur_par_jeton(jeton)
        if joueur.numero != partie.createur:
            raise ErreurDeJeu("Seul celui qui a ouvert la partie peut la lancer.")
        phases.commencer_la_partie(partie, self.maintenant())
        return self.vue(identifiant, jeton)

    # --- pendant la partie -------------------------------------------------

    def vue(self, identifiant, jeton):
        """L'écran d'un joueur : rien de plus que ce qu'il a le droit de voir."""
        partie = self._partie(identifiant)
        joueur = partie.joueur_par_jeton(jeton)
        maintenant = self._mettre_a_jour(partie)
        return vues.vue_pour(partie, joueur, maintenant)

    def agir(self, identifiant, jeton, action, valeur):
        """Enregistre ce qu'un joueur vient de faire, puis lui rend son écran."""
        partie = self._partie(identifiant)
        joueur = partie.joueur_par_jeton(jeton)
        self._mettre_a_jour(partie)

        if action == "choisir":
            pouvoirs.choisir_une_cible(partie, joueur, valeur)
        elif action == "voter":
            jour.voter(partie, joueur, valeur)
        elif action == "dire":
            jour.dire(partie, joueur, valeur)
        else:
            raise ErreurDeJeu(f"Action inconnue : {action}")

        return self.vue(identifiant, jeton)

    # --- le temps qui passe ------------------------------------------------

    def _mettre_a_jour(self, partie):
        """Rattrape le temps écoulé depuis la dernière fois.

        Appelée à chaque demande d'écran : c'est elle qui fait tomber la
        nuit, lever le jour et arriver les joueurs factices.
        """
        maintenant = self.maintenant()
        automates.completer_le_village(partie, maintenant)
        phases.faire_avancer_le_temps(partie, maintenant)
        return maintenant

    def _partie(self, identifiant):
        if identifiant not in self.parties:
            raise ErreurDeJeu("Cette partie n'existe pas (ou elle est finie).")
        return self.parties[identifiant]

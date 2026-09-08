"""Une petite fabrique de parties, pour les tests.

Elle sert à poser une situation précise — « deux loups, un chevalier, trois
manants » — sans passer par la salle d'attente et le tirage au sort.
"""

import random

from jeu.configuration import Configuration
from jeu.partie import Partie, ajouter_un_joueur

CONFIGURATION = Configuration()


def partie_pour_les_tests(roles, graine=0, phase="nuit"):
    """Une partie où chaque joueur a le rôle qu'on lui donne."""
    partie = Partie(
        "essai",
        CONFIGURATION.univers_choisi("sombreval"),
        CONFIGURATION,
        random.Random(graine),
    )
    for numero, role in enumerate(roles, start=1):
        joueur = ajouter_un_joueur(partie, f"Joueur{numero}")
        joueur.role = role

    partie.phase = phase
    partie.numero_de_nuit = 1
    partie.fin_de_phase = 1000.0
    return partie

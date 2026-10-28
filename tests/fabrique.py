"""Une petite fabrique de parties, pour les tests.

Elle sert à poser une situation précise — « deux loups, un chevalier, trois
manants » — sans passer par la salle d'attente et le tirage au sort.
"""

import random
import shutil
import tempfile
from pathlib import Path

import yaml

from jeu.configuration import DOSSIER_REGLES, Configuration
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


def configuration_avec_un_monde_pas_encore_ecrit():
    """Les vraies règles, plus un monde fabriqué en « disponible: false ».

    On ne prend PAS Salem pour exemple : le jour où son équipe l'allume, un
    test qui exigeait qu'il soit refusé tomberait sur une contribution juste,
    avec pour seul message « ErreurDeJeu not raised ».
    """
    dossier = Path(tempfile.mkdtemp())
    for nom in ("roles.yaml", "partie.yaml", "defauts.yaml"):
        shutil.copy(DOSSIER_REGLES / nom, dossier / nom)
    shutil.copytree(DOSSIER_REGLES / "univers", dossier / "univers")
    (dossier / "univers" / "brouillon.yaml").write_text(
        yaml.safe_dump({"nom": "brouillon", "titre": "Brouillon",
                        "disponible": False}, allow_unicode=True),
        encoding="utf-8")
    return dossier

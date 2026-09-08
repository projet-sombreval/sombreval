"""Lecture des fichiers du dossier regles/.

Le moteur ne connaît aucun nom de rôle, aucun texte, aucune couleur : il les
lit ici. Changer regles/univers/sombreval.yaml change le jeu sans toucher au
code.
"""

import pathlib

import yaml

from jeu.erreurs import ErreurDeJeu

DOSSIER_REGLES = pathlib.Path(__file__).resolve().parent.parent / "regles"


class Configuration:
    """Tout ce qui est lu dans regles/, chargé une fois au démarrage."""

    def __init__(self, dossier=DOSSIER_REGLES):
        self.dossier = pathlib.Path(dossier)
        mecanique = _lire(self.dossier / "roles.yaml")
        self.roles = mecanique["roles"]
        self.compositions = mecanique["compositions"]
        self.parametres = _lire(self.dossier / "partie.yaml")
        self.univers = _lire_les_univers(self.dossier / "univers")

    def role(self, nom):
        """La mécanique d'un rôle (son camp, son action, quand il agit)."""
        if nom not in self.roles:
            raise ErreurDeJeu(f"Rôle inconnu dans regles/roles.yaml : {nom}")
        return self.roles[nom]

    def univers_choisi(self, nom):
        """L'univers demandé, s'il est prêt à être joué."""
        if nom not in self.univers:
            raise ErreurDeJeu(f"Univers inconnu : {nom}")
        univers = self.univers[nom]
        if not univers.get("disponible"):
            raise ErreurDeJeu(
                f"L'univers {univers['titre']} n'est pas encore écrit."
            )
        return univers

    def composition(self, nombre_de_joueurs):
        """Qui joue quoi, pour ce nombre de joueurs.

        On vérifie ici que tous les rôles demandés sont implémentés : mieux
        vaut refuser de lancer la partie que la voir se bloquer en pleine
        séance.
        """
        if nombre_de_joueurs not in self.compositions:
            raise ErreurDeJeu(
                f"Aucune composition pour {nombre_de_joueurs} joueurs "
                "dans regles/roles.yaml."
            )
        composition = self.compositions[nombre_de_joueurs]
        for nom in composition:
            if not self.role(nom).get("implemente"):
                raise ErreurDeJeu(
                    f"Le rôle « {nom} » est décrit mais pas encore joué "
                    "par le moteur (implemente: false)."
                )
        return composition

    def duree(self, phase):
        """La durée d'une phase, en secondes."""
        durees = self.parametres["durees"]
        if phase not in durees:
            raise ErreurDeJeu(f"Aucune durée pour la phase {phase}.")
        return durees[phase]


def _lire(fichier):
    if not fichier.is_file():
        raise ErreurDeJeu(f"Fichier de règles manquant : {fichier}")
    return yaml.safe_load(fichier.read_text(encoding="utf-8"))


def _lire_les_univers(dossier):
    """Un fichier .yaml par univers, rangé par son nom court."""
    univers = {}
    for fichier in sorted(dossier.glob("*.yaml")):
        donnees = _lire(fichier)
        univers[donnees["nom"]] = donnees
    return univers

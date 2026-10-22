"""Lecture des fichiers du dossier regles/.

Le moteur ne connaît aucun nom de rôle, aucun texte, aucune couleur : il les
lit ici. Changer regles/univers/sombreval.yaml change le jeu sans toucher au
code.
"""

import copy
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
        self.defauts = _lire(self.dossier / "defauts.yaml")
        self.univers = _lire_les_univers(self.dossier / "univers", self.defauts)

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


def _lire_les_univers(dossier, defauts):
    """Un fichier .yaml par univers, rangé par son nom court.

    Chaque univers est complété par `regles/defauts.yaml` : ce qu'il n'a pas
    encore écrit reçoit une valeur d'attente, visible à l'écran. C'est ce qui
    permet de MONTRER un monde en cours de remplissage au lieu d'attendre
    qu'il soit fini.
    """
    univers = {}
    for fichier in sorted(dossier.glob("*.yaml")):
        donnees = _lire(fichier)
        univers[donnees["nom"]] = _avec_les_defauts(defauts, donnees)
    return univers


def _avec_les_defauts(defauts, univers):
    """Les valeurs de l'univers par-dessus celles d'attente, en profondeur.

    UN SEUL point de fusion, et c'est le propos : le moteur lit `univers[...]`
    en indexation dure à vingt-six endroits, dans sept modules. Combler ici
    les couvre tous par construction — il n'y a pas vingt-six gardes à écrire,
    ni à maintenir d'accord.

    La fusion est RÉCURSIVE parce que les trous sont imbriqués : un univers
    peut avoir ses couleurs mais pas ses camps, ou le nom d'un rôle sans son
    pouvoir. Et elle est faite dans ce sens-là — l'univers écrase le défaut,
    jamais l'inverse.
    """
    complet = copy.deepcopy(defauts)
    for cle, valeur in univers.items():
        if isinstance(valeur, dict) and isinstance(complet.get(cle), dict):
            complet[cle] = _avec_les_defauts(complet[cle], valeur)
        else:
            complet[cle] = valeur
    return complet

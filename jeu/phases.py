"""L'enchaînement des phases et la minuterie.

Le temps n'est pas géré par une horloge qui tourne dans le serveur : à
chaque fois qu'un joueur demande son écran, on regarde l'heure et on
rattrape les phases terminées. C'est plus simple à lire, à tester, et ça
marche même si personne ne regarde.
"""

from jeu import automates, jour, nuit, victoire
from jeu.erreurs import ErreurDeJeu
from jeu.partie import distribuer_les_roles

PHASE_SUIVANTE = {"decouverte": "nuit", "nuit": "jour", "jour": "nuit"}

DUREE_DE_LA_PHASE = {
    "decouverte": "decouverte_du_role",
    "nuit": "nuit",
    "jour": "jour",
}

# Garde-fou : si le serveur a dormi longtemps (l'ordinateur s'est mis en
# veille), on ne rattrape pas mille phases d'un coup.
PHASES_RATTRAPEES_AU_MAXIMUM = 20


def commencer_la_partie(partie, maintenant):
    attendus = partie.configuration.parametres["nombre_de_joueurs"]
    if partie.phase != "attente":
        raise ErreurDeJeu("La partie a déjà commencé.")
    if len(partie.joueurs) != attendus:
        raise ErreurDeJeu(
            f"Le village n'est pas au complet : {len(partie.joueurs)} "
            f"joueurs sur {attendus}."
        )

    distribuer_les_roles(partie)
    _entrer_dans(partie, "decouverte", maintenant)


def faire_avancer_le_temps(partie, maintenant):
    """Termine les phases dont le temps est écoulé."""
    for _ in range(PHASES_RATTRAPEES_AU_MAXIMUM):
        if partie.phase in ("attente", "fin"):
            return
        if maintenant < partie.fin_de_phase:
            break
        _terminer_la_phase(partie, maintenant)

    if partie.phase == "jour":
        automates.finir_de_voter(partie, maintenant)


def _terminer_la_phase(partie, maintenant):
    phase_finie = partie.phase

    if phase_finie == "nuit":
        nuit.resoudre_la_nuit(partie)
    elif phase_finie == "jour":
        jour.resoudre_le_jour(partie)

    gagnant = victoire.camp_gagnant(partie)
    if gagnant and phase_finie != "decouverte":
        partie.camp_gagnant = gagnant
        partie.phase = "fin"
        partie.fin_de_phase = None
        return

    _entrer_dans(partie, PHASE_SUIVANTE[phase_finie], maintenant)


def _entrer_dans(partie, phase, maintenant):
    partie.phase = phase
    partie.fin_de_phase = maintenant + partie.configuration.duree(
        DUREE_DE_LA_PHASE[phase]
    )

    if phase == "nuit":
        partie.numero_de_nuit += 1
        partie.actions_de_nuit = {}
        automates.jouer_la_nuit(partie)
    elif phase == "jour":
        partie.votes = {}
        partie.discussion = []
        automates.jouer_le_jour(partie)

"""La vue filtrée : ce qu'un joueur, et lui seul, a le droit de voir.

C'est ici que se joue l'honnêteté du jeu. Le rôle d'un joueur vivant ne
part JAMAIS vers les autres navigateurs : ce qui n'est pas affiché n'est
pas non plus dans la page. On peut ouvrir l'inspecteur du navigateur
pendant la partie, il n'y a rien à y trouver.

Chaque joueur a deux identités : un numéro public (« j3 ») qui circule, et
un jeton secret qui reste dans son navigateur. Seuls les numéros sortent
d'ici.
"""

import math

from jeu.jour import compter_les_voix
from jeu.pouvoirs import cibles_possibles
from jeu.victoire import CAMP_MENACE


def vue_pour(partie, observateur, maintenant):
    vue = {
        "partie": partie.identifiant,
        "phase": partie.phase,
        "univers": _univers(partie),
        "moi": _moi(partie, observateur),
        "joueurs": [
            _joueur_vu_par(partie, joueur, observateur)
            for joueur in partie.joueurs
        ],
        "je_suis_le_createur": partie.createur == observateur.numero,
        "secondes_restantes": _secondes_restantes(partie, maintenant),
        "numero_de_nuit": partie.numero_de_nuit,
        "journal": partie.journal,
        "mes_revelations": partie.revelations.get(observateur.numero, []),
        "joueurs_attendus": partie.configuration.parametres["nombre_de_joueurs"],
    }

    if partie.phase == "nuit":
        vue.update(_vue_de_nuit(partie, observateur))
    elif partie.phase == "jour":
        vue.update(_vue_de_jour(partie, observateur))
    elif partie.phase == "fin":
        vue["resultat"] = _resultat(partie)

    return vue


def _univers(partie):
    """Le décor : il est public, tout le monde reçoit le même."""
    return {
        "nom": partie.univers["nom"],
        "titre": partie.univers["titre"],
        "annee": partie.univers["annee"],
        "sous_titre": partie.univers["sous_titre"],
        "presentation": partie.univers["presentation"],
        "couleurs": partie.univers["couleurs"],
        "textes": partie.univers["textes"],
    }


def _moi(partie, observateur):
    moi = {
        "numero": observateur.numero,
        "pseudo": observateur.pseudo,
        "vivant": observateur.vivant,
        "role": None,
    }
    if observateur.role:
        role = partie.univers["roles"][observateur.role]
        camp = partie.camp_de(observateur)
        moi["role"] = {
            "nom": role["nom"],
            "pouvoir": role["pouvoir"],
            "camp": partie.univers["camps"][camp]["nom"],
        }
    return moi


def _joueur_vu_par(partie, joueur, observateur):
    """Un joueur, tel que l'observateur a le droit de le voir.

    Le rôle n'est ajouté que dans trois cas : c'est moi, il est mort (son
    rôle est révélé aussitôt), ou nous sommes de la même menace — elle se
    concerte la nuit, donc elle se connaît.
    """
    vu = {
        "numero": joueur.numero,
        "pseudo": joueur.pseudo,
        "vivant": joueur.vivant,
    }
    if _role_visible(partie, joueur, observateur):
        vu["role"] = partie.nom_du_role(joueur)
    return vu


def _role_visible(partie, joueur, observateur):
    if joueur.role is None:
        return False
    if joueur is observateur or not joueur.vivant:
        return True
    if partie.phase == "fin":
        return True
    return (
        observateur.role is not None
        and partie.camp_de(observateur) == CAMP_MENACE
        and partie.camp_de(joueur) == CAMP_MENACE
    )


def _vue_de_nuit(partie, observateur):
    if not observateur.vivant:
        return {"instruction": partie.texte("nuit_mort"), "cibles": []}

    cibles = cibles_possibles(partie, observateur)
    if not cibles:
        return {"instruction": partie.texte("nuit_sans_pouvoir"), "cibles": []}

    return {
        "instruction": partie.univers["roles"][observateur.role]["instruction_nuit"],
        "cibles": [cible.numero for cible in cibles],
        "mon_choix": partie.actions_de_nuit.get(observateur.numero),
        "choix_des_allies": _choix_des_allies(partie, observateur),
    }


def _choix_des_allies(partie, observateur):
    """Le vote interne de la menace : ses membres voient leurs choix.

    Vide pour tous les autres : personne d'autre ne voit qui vise qui.
    """
    if partie.camp_de(observateur) != CAMP_MENACE:
        return []

    choix = []
    for joueur in partie.vivants():
        if partie.camp_de(joueur) != CAMP_MENACE:
            continue
        numero_cible = partie.actions_de_nuit.get(joueur.numero)
        choix.append({
            "pseudo": joueur.pseudo,
            "cible": partie.joueur_par_numero(numero_cible).pseudo
            if numero_cible else None,
        })
    return choix


def _vue_de_jour(partie, observateur):
    return {
        "instruction": partie.texte(
            "jour_consigne" if observateur.vivant else "jour_mort"
        ),
        "discussion": partie.discussion,
        "messages": partie.univers["messages"] if observateur.vivant else [],
        "voix": compter_les_voix(partie),
        "mon_vote": partie.votes.get(observateur.numero),
    }


def _resultat(partie):
    camp = partie.univers["camps"][partie.camp_gagnant]
    return {
        "camp": camp["nom"],
        "texte": camp["victoire"],
        "roles": [
            {"pseudo": joueur.pseudo, "role": partie.nom_du_role(joueur)}
            for joueur in partie.joueurs
        ],
    }


def _secondes_restantes(partie, maintenant):
    if partie.fin_de_phase is None:
        return None
    return max(0, math.ceil(partie.fin_de_phase - maintenant))

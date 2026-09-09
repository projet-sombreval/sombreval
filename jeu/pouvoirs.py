"""Qui peut agir la nuit, et sur qui.

Tout ce qui est ici se lit dans regles/roles.yaml. Le moteur ne sait pas ce
qu'est un loup ou un bailli : il sait qu'un rôle a une action, un moment et
une liste de cibles permises.
"""

from jeu.erreurs import ErreurDeJeu


def action_de(partie, joueur):
    """Le type d'action du rôle : aucune, eliminer, proteger, reveler_*."""
    return partie.configuration.role(joueur.role).get("action", "aucune")


def peut_agir_cette_nuit(partie, joueur):
    """Ce joueur a-t-il quelque chose à faire cette nuit ?"""
    if not joueur.vivant:
        return False

    regle = partie.configuration.role(joueur.role)
    if regle.get("action", "aucune") == "aucune":
        return False

    quand = regle.get("quand", "jamais")
    if quand == "chaque_nuit":
        return True
    if quand == "une_nuit_sur_deux":
        return partie.numero_de_nuit % 2 == 1
    if quand == "une_seule_fois":
        return joueur.numero not in partie.pouvoirs_utilises
    return False


def cibles_possibles(partie, joueur):
    """La liste des joueurs que celui-ci a le droit de viser cette nuit."""
    if not peut_agir_cette_nuit(partie, joueur):
        return []

    regle = partie.configuration.role(joueur.role)
    quelles_cibles = regle.get("cible", "autre_vivant")

    if quelles_cibles == "mort":
        cibles = [j for j in partie.joueurs if not j.vivant]
    elif quelles_cibles == "vivant":
        cibles = partie.vivants()
    else:  # autre_vivant
        cibles = [j for j in partie.vivants() if j is not joueur]

    if regle.get("epargne_son_camp"):
        mon_camp = partie.camp_de(joueur)
        cibles = [j for j in cibles if partie.camp_de(j) != mon_camp]

    # « Jamais le même deux nuits de suite. »
    if not regle.get("meme_cible_deux_nuits", True):
        derniere = partie.cible_precedente.get(joueur.numero)
        cibles = [j for j in cibles if j.numero != derniere]

    return cibles


def choisir_une_cible(partie, joueur, numero_cible):
    """Enregistre le choix de nuit d'un joueur, après l'avoir vérifié.

    On revérifie toujours ici : la liste envoyée à la page peut avoir été
    modifiée dans le navigateur, c'est le serveur qui décide.
    """
    if partie.phase != "nuit":
        raise ErreurDeJeu("Ce n'est pas la nuit.")
    if not joueur.vivant:
        raise ErreurDeJeu("Tu es mort : tu ne joues plus.")

    permises = [cible.numero for cible in cibles_possibles(partie, joueur)]
    if numero_cible not in permises:
        raise ErreurDeJeu("Tu ne peux pas viser ce joueur cette nuit.")

    partie.actions_de_nuit[joueur.numero] = numero_cible


def camp_apparent(partie, joueur):
    """Le camp que les autres CROIENT voir.

    Presque toujours le vrai camp : seul un rôle avec « apparait_comme »
    (le Traître) en montre un autre.
    """
    regle = partie.configuration.role(joueur.role)
    return regle.get("apparait_comme", regle["camp"])

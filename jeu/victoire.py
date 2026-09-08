"""Qui a gagné, et quand.

Deux conditions, et pas une de plus :
- le village gagne quand la menace est entièrement éliminée ;
- la menace gagne quand elle égale ou dépasse en nombre les autres vivants.
"""

# Les deux camps sont de la mécanique, pas du décor : leurs noms affichés
# sont dans regles/univers/<nom>.yaml.
CAMP_MENACE = "menace"
CAMP_VILLAGE = "village"


def camp_gagnant(partie):
    """Renvoie le camp gagnant, ou None si la partie continue."""
    vivants = partie.vivants()
    menace = [j for j in vivants if partie.camp_de(j) == CAMP_MENACE]
    autres = [j for j in vivants if partie.camp_de(j) != CAMP_MENACE]

    if not menace:
        return CAMP_VILLAGE
    if len(menace) >= len(autres):
        return CAMP_MENACE
    return None

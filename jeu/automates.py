"""Les joueurs factices.

Ils remplissent le village pour qu'on puisse jouer seul devant une classe.
Leurs choix sont simples et au hasard : ils ne réfléchissent pas, ils ne
trichent pas non plus — ils passent par les mêmes vérifications que les
joueurs humains.
"""

from jeu.jour import compter_les_voix, dire, voter
from jeu.partie import ajouter_un_joueur
from jeu.pouvoirs import choisir_une_cible, cibles_possibles

MESSAGES_PAR_JOUR = 3

# Un automate sur deux suit le village au lieu de voter au hasard. Sans ça,
# les voix se dispersent et personne n'est jamais éliminé le jour.
CHANCES_DE_SUIVRE_LE_VILLAGE = 0.5


def jouer_la_nuit(partie):
    """Chaque automate qui a un pouvoir choisit une cible au hasard."""
    for joueur in _automates_vivants(partie):
        cibles = cibles_possibles(partie, joueur)
        if cibles:
            choisir_une_cible(partie, joueur, partie.hasard.choice(cibles).numero)


def jouer_le_jour(partie):
    """Les automates parlent au lever du jour et votent à la fin du temps.

    Ils votent tard exprès : s'ils votaient tout de suite, la majorité
    serait faite avant que le joueur humain ait cliqué et sa voix ne
    changerait jamais rien. Là, ils suivent ce qui a été dit — donc souvent
    son accusation.
    """
    partie.retardataires = _automates_vivants(partie)
    partie.hasard.shuffle(partie.retardataires)

    for joueur in partie.retardataires[:MESSAGES_PAR_JOUR]:
        dire(partie, joueur, partie.hasard.randrange(len(partie.univers["messages"])))


def finir_de_voter(partie, maintenant):
    """Les automates restants votent dans la dernière moitié du temps.

    Ils suivent ce que le village a déjà dit — donc, souvent, le joueur
    humain qui vient de voter.
    """
    if not partie.retardataires:
        return
    duree = partie.configuration.duree("jour")
    if maintenant < partie.fin_de_phase - duree / 2:
        return

    for joueur in partie.retardataires:
        if joueur.vivant:
            _accuser(partie, joueur)
    partie.retardataires = []


def _accuser(partie, joueur):
    cible = _qui_accuser(partie, joueur)
    if cible:
        voter(partie, joueur, cible.numero)


def _qui_accuser(partie, joueur):
    """Qui un automate accuse : le plus accusé, ou n'importe qui.

    Il ne regarde que les voix déjà exprimées — il ne connaît le rôle de
    personne, il ne triche pas.
    """
    autres = [j for j in partie.vivants() if j is not joueur]
    if not autres:
        return None

    voix = compter_les_voix(partie)
    deja_accuses = [j for j in autres if voix.get(j.numero)]
    if deja_accuses and partie.hasard.random() < CHANCES_DE_SUIVRE_LE_VILLAGE:
        return max(deja_accuses, key=lambda j: voix[j.numero])
    return partie.hasard.choice(autres)


def _automates_vivants(partie):
    return [j for j in partie.vivants() if j.automate]


def completer_le_village(partie, maintenant):
    """Fait entrer un joueur factice en salle d'attente, un à la fois.

    Ils arrivent doucement, l'un après l'autre : c'est plus vivant à montrer
    qu'un village qui apparaît d'un coup. Le délai est dans
    regles/partie.yaml. Si de vraies personnes rejoignent par le lien, elles
    prennent les places avant eux.
    """
    parametres = partie.configuration.parametres
    if partie.phase != "attente":
        return
    if len(partie.joueurs) >= parametres["nombre_de_joueurs"]:
        return
    if maintenant - partie.derniere_arrivee < parametres["delai_entre_les_arrivees"]:
        return

    pris = {joueur.pseudo for joueur in partie.joueurs}
    libres = [p for p in partie.univers["pseudos_factices"] if p not in pris]
    if not libres:
        return

    ajouter_un_joueur(partie, libres[0], automate=True)
    partie.derniere_arrivee = maintenant

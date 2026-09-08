"""La résolution de la nuit, dans l'ordre, du côté du serveur.

L'ordre compte, et c'est la partie la plus délicate du jeu :

1. on fige l'état du village ;
2. on applique les protections ;
3. on applique les éliminations — viser un joueur protégé échoue ;
4. on calcule les révélations SUR L'ÉTAT FIGÉ à l'étape 1.

Sans l'étape 4, le Bailli apprendrait la mort d'un joueur avant le reste du
village : il saurait au matin quelque chose que personne d'autre ne peut
savoir.
"""

from jeu.pouvoirs import action_de, camp_apparent, peut_agir_cette_nuit


def resoudre_la_nuit(partie):
    etat = _figer_letat(partie)
    # La liste de ceux qui agissent est arrêtée elle aussi avant les morts :
    # un Bailli tué cette nuit apprend quand même ce qu'il est allé chercher.
    agissants = _ceux_qui_ont_agi(partie)

    proteges = _appliquer_les_protections(partie, agissants)
    _appliquer_les_eliminations(partie, agissants, proteges)
    _calculer_les_revelations(partie, agissants, etat)
    _preparer_la_nuit_suivante(partie, agissants)


def _figer_letat(partie):
    """Une photographie du village avant que rien ne se passe."""
    return {
        joueur.numero: {
            "vivant": joueur.vivant,
            "role": joueur.role,
            "camp_apparent": camp_apparent(partie, joueur),
        }
        for joueur in partie.joueurs
    }


def _ceux_qui_ont_agi(partie):
    """Les joueurs qui ont choisi une cible cette nuit, et leur cible.

    Celui qui n'a pas joué avant la fin du temps ne fait rien : le jeu ne
    choisit jamais à sa place.
    """
    agissants = []
    for numero, numero_cible in partie.actions_de_nuit.items():
        joueur = partie.joueur_par_numero(numero)
        if peut_agir_cette_nuit(partie, joueur):
            agissants.append((joueur, numero_cible))
    return agissants


def _appliquer_les_protections(partie, agissants):
    """Renvoie les numéros des joueurs que quelqu'un a mis à l'abri."""
    proteges = set()
    for joueur, numero_cible in agissants:
        if action_de(partie, joueur) != "proteger":
            continue
        proteges.add(numero_cible)
        _confirmer(partie, joueur, partie.joueur_par_numero(numero_cible))
    return proteges


def _appliquer_les_eliminations(partie, agissants, proteges):
    victimes = _victimes_designees(partie, agissants)

    for numero_cible in victimes:
        if numero_cible in proteges:
            continue
        cible = partie.joueur_par_numero(numero_cible)
        cible.vivant = False
        partie.noter_au_journal(partie.texte(
            "elimine_nuit",
            pseudo=cible.pseudo,
            role=partie.nom_du_role(cible),
        ))

    if not victimes or set(victimes) <= proteges:
        partie.noter_au_journal(partie.texte("personne_eliminee_nuit"))


def _victimes_designees(partie, agissants):
    """Qui les rôles qui éliminent ont désigné cette nuit.

    Une décision collective (la Menace) est un vote interne : la majorité
    l'emporte, une égalité est tranchée au hasard.
    """
    victimes = []
    for nom, regle in partie.configuration.roles.items():
        if regle.get("action") != "eliminer":
            continue

        choix = [cible for joueur, cible in agissants if joueur.role == nom]
        if not choix:
            continue

        if regle.get("decision") == "collective":
            victime = _majorite(partie, choix)
            victimes.append(victime)
            _confirmer_a_tous(partie, nom, agissants, victime)
        else:
            victimes.extend(choix)
    return victimes


def _majorite(partie, choix):
    """Le plus choisi ; en cas d'égalité, le hasard tranche."""
    compte = {}
    for numero in choix:
        compte[numero] = compte.get(numero, 0) + 1
    meilleur = max(compte.values())
    a_egalite = [numero for numero, voix in compte.items() if voix == meilleur]
    return partie.hasard.choice(a_egalite)


def _calculer_les_revelations(partie, agissants, etat):
    """Ce que les rôles qui apprennent quelque chose ont appris.

    On lit l'état figé, jamais l'état d'après : c'est tout l'objet de
    l'étape 4.
    """
    for joueur, numero_cible in agissants:
        if not action_de(partie, joueur).startswith("reveler_"):
            continue

        cible = partie.joueur_par_numero(numero_cible)
        etat_cible = etat[numero_cible]
        camp = partie.univers["camps"][etat_cible["camp_apparent"]]
        partie.noter_pour(joueur, partie.texte_du_role(
            joueur,
            "revelation",
            cible=cible.pseudo,
            apparence=camp["apparence"],
            role=partie.univers["roles"][etat_cible["role"]]["nom"],
        ))


def _preparer_la_nuit_suivante(partie, agissants):
    for joueur, numero_cible in agissants:
        partie.cible_precedente[joueur.numero] = numero_cible
        regle = partie.configuration.role(joueur.role)
        if regle.get("quand") == "une_seule_fois":
            partie.pouvoirs_utilises.add(joueur.numero)
    partie.actions_de_nuit = {}


def _confirmer(partie, joueur, cible):
    """Dit à un joueur, à lui seul, ce qu'il vient de faire."""
    texte = partie.texte_du_role(joueur, "confirmation", cible=cible.pseudo)
    if texte:
        partie.noter_pour(joueur, texte)


def _confirmer_a_tous(partie, role, agissants, numero_victime):
    """Après un vote interne, chaque membre apprend la décision du groupe."""
    victime = partie.joueur_par_numero(numero_victime)
    for joueur, _ in agissants:
        if joueur.role == role:
            _confirmer(partie, joueur, victime)

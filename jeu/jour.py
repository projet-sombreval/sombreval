"""Le jour : la discussion et le vote du village.

La discussion se fait avec des phrases toutes faites, jamais en saisie
libre. Personne n'écrit ce qu'il veut : ni insulte, ni règlement de comptes.
Les phrases sont dans regles/univers/<nom>.yaml.
"""

from jeu.erreurs import ErreurDeJeu

MESSAGES_PAR_JOUR = 3


def voter(partie, joueur, numero_cible):
    """Enregistre le vote d'un joueur ; il peut en changer jusqu'au bout."""
    if partie.phase != "jour":
        raise ErreurDeJeu("Ce n'est pas l'heure du vote.")
    if not joueur.vivant:
        raise ErreurDeJeu("Tu es mort : tu ne votes plus.")

    cible = partie.joueur_par_numero(numero_cible)
    if not cible.vivant:
        raise ErreurDeJeu("On ne juge pas un mort.")
    if cible is joueur:
        raise ErreurDeJeu("On ne vote pas contre soi-même.")

    partie.votes[joueur.numero] = numero_cible


def dire(partie, joueur, numero_du_message):
    """Ajoute une phrase toute faite à la discussion du jour."""
    if partie.phase != "jour":
        raise ErreurDeJeu("Ce n'est pas l'heure de parler.")
    if not joueur.vivant:
        raise ErreurDeJeu("Tu es mort : tu ne parles plus.")

    phrases = partie.univers["messages"]
    if not 0 <= numero_du_message < len(phrases):
        raise ErreurDeJeu("Cette phrase n'existe pas.")

    deja_dites = [m for m in partie.discussion if m["numero"] == joueur.numero]
    if len(deja_dites) >= MESSAGES_PAR_JOUR:
        raise ErreurDeJeu("Tu as déjà assez parlé aujourd'hui.")

    partie.discussion.append({
        "numero": joueur.numero,
        "pseudo": joueur.pseudo,
        "texte": phrases[numero_du_message],
    })


def compter_les_voix(partie):
    """Combien de voix chaque joueur a reçues : numéro -> nombre."""
    compte = {}
    for numero_cible in partie.votes.values():
        compte[numero_cible] = compte.get(numero_cible, 0) + 1
    return compte


def resoudre_le_jour(partie):
    """Élimine celui qui a le plus de voix. Une égalité n'élimine personne."""
    compte = compter_les_voix(partie)

    if not compte:
        partie.noter_au_journal(partie.texte("egalite_jour"))
        return

    meilleur = max(compte.values())
    a_egalite = [numero for numero, voix in compte.items() if voix == meilleur]

    if len(a_egalite) > 1:
        partie.noter_au_journal(partie.texte("egalite_jour"))
        return

    juge = partie.joueur_par_numero(a_egalite[0])
    juge.vivant = False
    partie.noter_au_journal(partie.texte(
        "elimine_jour",
        pseudo=juge.pseudo,
        role=partie.nom_du_role(juge),
    ))

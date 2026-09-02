"""Les trois univers historiques proposés au joueur.

Un univers ne change pas les règles : il change le décor, l'année et le nom
des rôles. C'est la seule chose que le meneur choisit avant de lancer la
partie (exigence E3 du cahier des charges).
"""

# Chaque univers est un dictionnaire. La clé du dictionnaire du dessus est le
# nom court : sans accent et en minuscules, parce qu'il sert aussi de nom de
# dossier dans roles/ et de nom de classe CSS dans les cartes.
UNIVERS = {
    "sombreval": {
        "titre": "Sombreval",
        "annee": 1348,
        "sous_titre": "La peste remonte la vallée.",
        "camp_village": "Village",
        "camp_traitre": "Semeurs de peste",
    },
    "salem": {
        "titre": "Salem",
        "annee": 1692,
        "sous_titre": "Le village accuse, le tribunal écoute.",
        "camp_village": "Fidèles",
        "camp_traitre": "Sorcières",
    },
    "serenissime": {
        "titre": "Sérénissime",
        "annee": 1487,
        "sous_titre": "Venise complote derrière ses masques.",
        "camp_village": "Citoyens",
        "camp_traitre": "Conjurés",
    },
}


def noms_univers():
    """Renvoie la liste des noms courts des univers."""
    return list(UNIVERS)


def chercher_univers(nom):
    """Renvoie l'univers portant ce nom court.

    Lève une ValueError si le nom est inconnu : mieux vaut une erreur claire
    au lancement de la partie qu'un écran vide en pleine séance.
    """
    if nom not in UNIVERS:
        raise ValueError(
            f"Univers inconnu : {nom!r}. Univers possibles : {noms_univers()}"
        )
    return UNIVERS[nom]
